---
date: 2026-11-05
description: 张量与 device / dtype、常用形状操作、自动求导、nn.Module、Dataset 与 DataLoader（动态 padding 的 collate_fn）、完整训练循环、语言模型的 shift 与 ignore_index、用 gather 计算 token 级 log 概率、保存与加载。
tags:
  - Python
  - PyTorch
---

# PyTorch 基础

本章只讲写训练代码最基本的部分，模型结构和分布式训练放在其他文章里。张量的索引、广播、形状变换规则与 [NumPy](numpy.md) 相同，这里不再重复。

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)
```

## 1. 张量

```python
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(x.shape, x.dtype, x.device)        # torch.Size([2, 2]) torch.float32 cpu

print(torch.zeros(2, 3).shape, torch.ones_like(x).dtype)   # torch.Size([2, 3]) torch.float32
print(torch.arange(5))                   # tensor([0, 1, 2, 3, 4])
print(torch.randn(2, 3).shape)           # 标准正态
print(torch.randint(0, 100, (2, 4)).dtype)   # torch.int64
```

Python 的浮点数默认变成 `float32`（NumPy 是 `float64`），整数变成 `int64`。token id、类别标签一般用 `int64`（`torch.long`）：`F.cross_entropy` 的类别标签必须是 `int64`，`nn.Embedding` 的输入必须是整数类型。

### 与 NumPy 互转

```python
import numpy as np

a = np.ones(3)
t = torch.from_numpy(a)      # 共享内存
a[0] = 5
print(t)                     # tensor([5., 1., 1.], dtype=torch.float64)
print(t.numpy().dtype)       # float64，同样共享内存
t2 = torch.tensor(a)         # torch.tensor 总是复制
a[1] = 7
print(t2[1].item())          # 1.0，不受影响
```

GPU 上的张量、或者 `requires_grad=True` 的张量，要先 `.detach().cpu()` 再 `.numpy()`。

### device

```python
device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(4, 4, device=device)
y = x.to("cpu")
print(y.device)              # cpu
```

参与同一个运算的张量必须在同一个设备上，否则报 `Expected all tensors to be on the same device`。模型用 `model.to(device)` 移过去（原地修改并返回自身），张量用 `t = t.to(device)`（返回新张量，必须重新赋值）。

### dtype 转换

```python
x = torch.randn(2, 2)
print(x.to(torch.bfloat16).dtype, x.half().dtype, x.long().dtype)
# torch.bfloat16 torch.float16 torch.int64
```

### 取出数值

```python
loss = torch.tensor(0.6931)
print(loss.item(), type(loss.item()))   # 0.6930999755859375 <class 'float'>
```

记录日志时用 `loss.item()`，不要存 `loss` 本身，否则会一直持有计算图。`.item()` 在 GPU 张量上会触发一次同步，每一步都调用会拖慢训练，可以每隔 N 步调用一次。

## 2. 常用形状操作

```python
x = torch.arange(12).reshape(3, 4)
print(x.view(4, 3).shape, x.reshape(-1).shape)    # torch.Size([4, 3]) torch.Size([12])
print(x.unsqueeze(0).shape, x[None].shape)         # torch.Size([1, 3, 4]) torch.Size([1, 3, 4])
print(x.unsqueeze(-1).squeeze(-1).shape)           # torch.Size([3, 4])
print(x.transpose(0, 1).shape, x.permute(1, 0).shape)   # torch.Size([4, 3]) torch.Size([4, 3])
print(torch.cat([x, x], dim=0).shape, torch.stack([x, x]).shape)   # torch.Size([6, 4]) torch.Size([2, 3, 4])
print(x.expand(2, 3, 4).shape)                     # torch.Size([2, 3, 4])，广播式扩展，不复制数据
a, b = x.chunk(2, dim=1)
print(a.shape)                                     # torch.Size([3, 2])
print([t.shape[1] for t in x.split([1, 3], dim=1)])   # [1, 3]
```

PyTorch 用 `dim` 表示维度（NumPy 用 `axis`，PyTorch 也接受 `axis`）。

### view 与 reshape、contiguous

`view` 要求张量在内存中是连续的；`transpose`、`permute` 之后张量通常不再连续：

```python
y = x.transpose(0, 1)
print(y.is_contiguous())                 # False
try:
    y.view(-1)
except RuntimeError as e:
    print("view failed")                 # view failed
print(y.contiguous().view(-1).shape, y.reshape(-1).shape)   # torch.Size([12]) torch.Size([12])
```

`reshape` 在能返回视图时返回视图，不能时自动复制，一般直接用它就行。多头注意力合并头时常见的写法 `out.transpose(1, 2).contiguous().view(B, T, C)` 就是这个原因。

## 3. 自动求导

```python
w = torch.tensor([2.0, -1.0], requires_grad=True)
x = torch.tensor([3.0, 4.0])
y = (w * x).sum() ** 2          # y = (w·x)^2
y.backward()
print(y.item(), w.grad)         # 4.0 tensor([12., 16.])
```

$y=(w\cdot x)^2$，$\partial y/\partial w = 2(w\cdot x)\,x = 2\times2\times[3,4]=[12,16]$，和结果一致。

- `requires_grad=True` 的张量参与的运算会被记录成计算图。
- 对**标量**调用 `backward()`，梯度累加到叶子张量的 `.grad` 上。
- 梯度是**累加**的，不会自动清零。这既是训练循环里要 `optimizer.zero_grad()` 的原因，也是梯度累积的实现方式。

```python
w.grad = None
for _ in range(2):
    ((w * x).sum() ** 2).backward()
print(w.grad)                   # tensor([24., 32.])，两次累加
```

### 不需要梯度的时候

```python
with torch.no_grad():
    z = w * 2
print(z.requires_grad)          # False

d = (w * 2).detach()            # 从计算图中分离，得到不需要梯度的张量
print(d.requires_grad)          # False
```

推理和评测时包在 `torch.no_grad()`（或 `torch.inference_mode()`）里，可以节省大量显存。`detach()` 用在"这个值参与后续计算但不希望梯度传回去"的地方，例如强化学习中计算优势函数时用到的价值估计、蒸馏时教师模型的输出。

## 4. nn.Module

```python
class MLP(nn.Module):
    def __init__(self, d_in, d_hidden, d_out, dropout=0.1):
        super().__init__()
        self.fc1 = nn.Linear(d_in, d_hidden)
        self.fc2 = nn.Linear(d_hidden, d_out)
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        return self.fc2(self.drop(F.gelu(self.fc1(x))))

model = MLP(16, 64, 4)
print(model)
print(sum(p.numel() for p in model.parameters()))   # 1348
for name, p in model.named_parameters():
    print(name, tuple(p.shape))
# fc1.weight (64, 16)
# fc1.bias (64,)
# fc2.weight (4, 64)
# fc2.bias (4,)
out = model(torch.randn(8, 16))
print(out.shape)        # torch.Size([8, 4])
```

- 在 `__init__` 中把子模块赋值为属性，它的参数就会被自动注册，`model.parameters()` 能找到。
- 子模块放在普通 Python list 里**不会**被注册，要用 `nn.ModuleList`（字典用 `nn.ModuleDict`）。这是自己写多层 Transformer 时的常见错误：参数没被优化器更新，也不会随 `model.to(device)` 移动。
- `nn.Linear(d_in, d_out)` 的权重 shape 是 `(d_out, d_in)`，计算 $y = xW^\top + b$。

```python
class Bad(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [nn.Linear(4, 4) for _ in range(3)]

class Good(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([nn.Linear(4, 4) for _ in range(3)])

print(len(list(Bad().parameters())), len(list(Good().parameters())))   # 0 6
```

不是参数、但需要跟模型一起保存和移动设备的张量（例如 RoPE 的频率表、因果掩码），用 `self.register_buffer("name", tensor)` 注册。

### train 与 eval 模式

```python
model.train()       # 训练模式：Dropout 生效
model.eval()        # 评测模式：Dropout 关闭，BatchNorm 使用统计值
print(model.training)   # False
```

`eval()` 不会关闭梯度计算，`no_grad()` 不会切换模式，两者作用不同，评测时一般都要用上。

## 5. Dataset 与 DataLoader

```python
from torch.utils.data import Dataset, DataLoader
from functools import partial

class ToyLMDataset(Dataset):
    def __init__(self, n, vocab_size=50, min_len=3, max_len=10):
        g = torch.Generator().manual_seed(0)
        lens = torch.randint(min_len, max_len + 1, (n,), generator=g)
        self.data = [torch.randint(1, vocab_size, (int(l),), generator=g) for l in lens]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return {"input_ids": self.data[idx]}

def collate(batch, pad_id=0):
    """把长度不同的样本补齐到这个 batch 内的最大长度。"""
    max_len = max(len(b["input_ids"]) for b in batch)
    input_ids = torch.full((len(batch), max_len), pad_id, dtype=torch.long)
    attention_mask = torch.zeros((len(batch), max_len), dtype=torch.long)
    for i, b in enumerate(batch):
        n = len(b["input_ids"])
        input_ids[i, :n] = b["input_ids"]
        attention_mask[i, :n] = 1
    return {"input_ids": input_ids, "attention_mask": attention_mask}

ds = ToyLMDataset(100)
loader = DataLoader(ds, batch_size=4, shuffle=True, collate_fn=partial(collate, pad_id=0))
batch = next(iter(loader))
print(batch["input_ids"].shape, batch["attention_mask"].sum(1).tolist())
# torch.Size([4, 10]) [3, 6, 10, 6]，每条样本的真实长度；shuffle 后每次不同
```

- `DataLoader` 负责打乱、分 batch、多进程加载（`num_workers`）。
- 默认的 collate 函数要求所有样本 shape 相同，文本长度不一时必须自己写 `collate_fn`。
- 每个 batch 只 pad 到该 batch 内的最大长度（动态 padding），比统一 pad 到全局最大长度省很多计算。
- 这里是右侧填充（padding 在序列末尾），训练时常用。批量生成时通常用左侧填充，让所有序列的最后一个 token 对齐。
- `num_workers > 0` 时数据在子进程中加载，`pin_memory=True` 可以加快从 CPU 到 GPU 的拷贝。

## 6. 训练循环

用一个小的语言模型把上面的内容串起来。语言模型训练的标签就是输入本身向左错一位：用位置 $t$ 及之前的 token 预测位置 $t+1$ 的 token。

```python
class TinyLM(nn.Module):
    def __init__(self, vocab_size, d_model=64):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, d_model)
        self.rnn = nn.GRU(d_model, d_model, batch_first=True)   # 用 GRU 代替 Transformer，保持简短
        self.head = nn.Linear(d_model, vocab_size)

    def forward(self, input_ids):
        h, _ = self.rnn(self.emb(input_ids))
        return self.head(h)                     # [B, T, V]

def lm_loss(logits, input_ids, attention_mask):
    labels = input_ids.clone()
    labels[attention_mask == 0] = -100          # padding 位置不计算 loss
    shift_logits = logits[:, :-1]               # 位置 t 的输出 ...
    shift_labels = labels[:, 1:]                # ... 预测位置 t+1 的 token
    return F.cross_entropy(
        shift_logits.reshape(-1, shift_logits.size(-1)),
        shift_labels.reshape(-1),
        ignore_index=-100,
    )

def evaluate(model, loader):
    model.eval()
    total, n = 0.0, 0
    with torch.no_grad():
        for b in loader:
            logits = model(b["input_ids"].to(device))
            total += lm_loss(logits, b["input_ids"].to(device), b["attention_mask"].to(device)).item()
            n += 1
    model.train()
    return total / n

torch.manual_seed(0)
model = TinyLM(vocab_size=50).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=0.01)
total_steps = 3 * len(loader)
scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=3e-3, total_steps=total_steps)

print(f"before: {evaluate(model, loader):.3f}")
model.train()
for epoch in range(3):
    for step, b in enumerate(loader):
        input_ids = b["input_ids"].to(device)
        mask = b["attention_mask"].to(device)

        logits = model(input_ids)
        loss = lm_loss(logits, input_ids, mask)

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
print(f"after: {evaluate(model, loader):.3f}")
# before: 3.928
# after: 3.618
```

这里的数据是均匀随机生成的 token（取值 1～49），理论上无法预测，loss 的下限约为 $\ln 49 \approx 3.89$。训练后低于这个值，是因为模型记住了这 100 条样本。换成真实文本，loss 才会持续下降。

每一步固定是这五件事：前向、算 loss、清梯度、反向、更新参数。`clip_grad_norm_` 把所有参数梯度的整体 L2 范数裁剪到不超过 `max_norm`，返回裁剪前的范数，这个值值得记录下来：突然变大通常是训练即将发散的信号。

`F.cross_entropy` 接收**未归一化的 logits**，内部用数值稳定的方式做 log_softmax，不要先自己做 softmax。它要求输入形状为 `[N, V]`、标签为 `[N]`，所以要先把 batch 和时间两个维度展平。标签等于 `ignore_index`（默认就是 -100）的位置不参与计算，这也是 Hugging Face 模型里 `labels` 用 -100 标记 prompt 和 padding 部分的原因：SFT 只对回答部分计算 loss，就是把 prompt 对应的 label 设为 -100。

### 梯度累积

显存放不下想要的 batch size 时，多跑几个小 batch 再更新一次：

```py
accum = 4
for step, b in enumerate(loader):
    loss = compute_loss(model, b) / accum      # 除以累积步数，让梯度等于大 batch 的平均
    loss.backward()
    if (step + 1) % accum == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)
```

### 混合精度

```py
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    logits = model(input_ids)
    loss = lm_loss(logits, input_ids, mask)
loss.backward()
```

bf16 一般不需要 `GradScaler`；用 fp16 时需要 `torch.amp.GradScaler` 防止梯度下溢。

## 7. token 级 log 概率

强化学习（PPO、GRPO、DPO）里经常要计算"模型生成某条回答的 log 概率"，也就是每个位置上实际 token 的 log 概率：

```python
def token_logprobs(logits, input_ids):
    """logits: [B, T, V]，input_ids: [B, T]，返回 [B, T-1]：第 t 个值是 log p(x_{t+1} | x_{<=t})"""
    logp = F.log_softmax(logits[:, :-1].float(), dim=-1)          # [B, T-1, V]
    target = input_ids[:, 1:].unsqueeze(-1)                         # [B, T-1, 1]
    return logp.gather(dim=-1, index=target).squeeze(-1)            # [B, T-1]

logits = torch.randn(2, 5, 10)
ids = torch.randint(0, 10, (2, 5))
lp = token_logprobs(logits, ids)
print(lp.shape, bool((lp <= 0).all()))      # torch.Size([2, 4]) True

# 只对回答部分求和：response_mask 为 1 的位置属于回答
response_mask = torch.tensor([[0, 0, 1, 1], [0, 1, 1, 1]])
seq_logp = (lp * response_mask).sum(-1)
print(seq_logp.shape)                        # torch.Size([2])

# 与 cross_entropy 的结果对照
ce = F.cross_entropy(logits[:, :-1].reshape(-1, 10), ids[:, 1:].reshape(-1), reduction="none").view(2, 4)
print(torch.allclose(-ce, lp, atol=1e-6))    # True
```

`gather(dim=-1, index)` 沿最后一维、按 `index` 给出的下标取值，`index` 的维数必须与输入相同，所以要先 `unsqueeze(-1)`。转成 `float()` 再做 log_softmax，是因为 bf16 下直接计算 log 概率误差较大。

## 8. 保存与加载

```python
import tempfile, os

path = os.path.join(tempfile.mkdtemp(), "ckpt.pt")
torch.save({
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "scheduler": scheduler.state_dict(),
    "epoch": 3,
}, path)

ckpt = torch.load(path, map_location="cpu")
model2 = TinyLM(vocab_size=50)
model2.load_state_dict(ckpt["model"])
print(list(ckpt["model"].keys())[:3])     # ['emb.weight', 'rnn.weight_ih_l0', 'rnn.weight_hh_l0']
```

- 保存 `state_dict()`（参数名到张量的字典），不要 `torch.save(model)` 保存整个对象：后者依赖类定义的位置，代码一改就加载不了。
- 断点续训需要同时保存优化器状态（AdamW 的一阶、二阶动量）和学习率调度器状态，只存模型参数会导致恢复后训练曲线跳变。
- `map_location="cpu"` 先加载到 CPU，避免所有进程都把权重加载到 0 号卡上。
- `load_state_dict` 默认要求 key 完全匹配。用 `DataParallel`/`DDP` 包装后保存的权重，key 前面会多一个 `module.`，加载到未包装的模型前要去掉。

## 9. 可复现性

```python
import random

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

set_seed(42)
```

固定种子能让同一台机器、同一份代码的结果基本一致，但 GPU 上部分算子（如 `index_add`、某些卷积和 attention 实现）本身是非确定性的。要求完全确定时，可以开启 `torch.use_deterministic_algorithms(True)`，代价是变慢。

## 10. 排查问题的几个习惯

- 第一次跑新代码，先用很小的数据过拟合一个 batch：loss 降不到接近 0，说明模型或 loss 写错了。
- 打印每个关键张量的 `shape`、`dtype`、`device`，对照预期。
- 训练出现 `nan`：检查输入中有没有 `nan`/`inf`，学习率是否过大，是否在 fp16 下溢出，有没有对 0 取 log 或除以 0。`torch.autograd.set_detect_anomaly(True)` 可以定位产生 `nan` 的反向操作（很慢，只在调试时开）。
- 显存不够：减小 batch、开梯度累积、用 bf16、开 gradient checkpointing（`model.gradient_checkpointing_enable()`）。`torch.cuda.max_memory_allocated()` 查看峰值显存。
