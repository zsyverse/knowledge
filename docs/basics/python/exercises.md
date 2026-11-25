---
date: 2026-11-05
description: 10 道综合练习：词频统计、配置展平、滑窗切分、早停、按 token 数动态分 batch、BPE 训练、top-k / top-p 采样、GRPO 组内优势、SFT 标签构造、RMSNorm。每题附参考答案和测试。
tags:
  - Python
---

# 综合练习

题目都来自大模型方向的实际工作。参考答案后附测试代码，可用来检查自己的实现。

## 1. 词频统计

写函数 `top_words(text, k)`，返回出现次数最多的 `k` 个英文单词及其次数。要求忽略大小写，单词只由字母和撇号组成（`don't` 算一个词），次数相同时按字母序排列。

??? success "参考答案"

    ```python
    import re
    from collections import Counter

    def top_words(text, k):
        words = re.findall(r"[a-z']+", text.lower())
        cnt = Counter(w for w in words if w.strip("'"))
        return sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:k]

    text = "The cat and the hat. The CAT doesn't care; don't, don't!"
    print(top_words(text, 3))     # [('the', 3), ('cat', 2), ("don't", 2)]
    ```

    `Counter.most_common(k)` 在次数相同时保持首次出现的顺序，不满足"按字母序"的要求，所以自己排序。排序的 key 用 `(-次数, 单词)`，一次完成"次数降序、单词升序"。

## 2. 展平嵌套配置

实现 `flatten(d)` 和 `unflatten(d)`：

```py
flatten({"model": {"name": "qwen", "lora": {"r": 8}}, "lr": 1e-4})
# {'model.name': 'qwen', 'model.lora.r': 8, 'lr': 0.0001}
```

`unflatten` 是它的逆操作。命令行里用 `--model.lora.r 16` 覆盖嵌套配置，就需要这两个函数。

??? success "参考答案"

    ```python
    def flatten(d, prefix=""):
        out = {}
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict) and v:
                out.update(flatten(v, key))
            else:
                out[key] = v
        return out

    def unflatten(flat):
        out = {}
        for key, v in flat.items():
            node = out
            *parents, last = key.split(".")
            for p in parents:
                node = node.setdefault(p, {})
            node[last] = v
        return out

    cfg = {"model": {"name": "qwen", "lora": {"r": 8}}, "lr": 1e-4}
    flat = flatten(cfg)
    print(flat)                      # {'model.name': 'qwen', 'model.lora.r': 8, 'lr': 0.0001}
    flat["model.lora.r"] = 16
    print(unflatten(flat))           # {'model': {'name': 'qwen', 'lora': {'r': 16}}, 'lr': 0.0001}
    assert unflatten(flatten(cfg)) == cfg
    ```

    `node.setdefault(p, {})`：key 存在时返回已有的值，不存在时先插入 `{}` 再返回它，正好用来"沿路径往下走，没有就新建"。

## 3. 滑动窗口切分

长文档超过模型上下文长度时，常切成有重叠的片段。写生成器 `sliding_windows(ids, size, stride)`：每个窗口长 `size`，相邻窗口起点相差 `stride`；最后一个窗口要覆盖到序列末尾（可以比前面的窗口重叠更多），序列比 `size` 短时只返回一个窗口。

??? success "参考答案"

    ```python
    def sliding_windows(ids, size, stride):
        n = len(ids)
        if n <= size:
            yield ids
            return
        start = 0
        while True:
            if start + size >= n:
                yield ids[n - size:]
                return
            yield ids[start:start + size]
            start += stride

    print(list(sliding_windows(list(range(10)), size=4, stride=3)))
    # [[0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9]]
    print(list(sliding_windows(list(range(9)), size=4, stride=3)))
    # [[0, 1, 2, 3], [3, 4, 5, 6], [5, 6, 7, 8]]
    print(list(sliding_windows([1, 2], size=4, stride=3)))
    # [[1, 2]]

    for n in range(1, 30):
        ws = list(sliding_windows(list(range(n)), 5, 2))
        covered = set(x for w in ws for x in w)
        assert covered == set(range(n)) and all(len(w) == min(n, 5) for w in ws)
    ```

## 4. 早停

实现一个 `EarlyStopping` 类：

- 构造参数 `patience`、`mode`（`"min"` 表示指标越小越好，如 loss；`"max"` 表示越大越好，如准确率）、`min_delta`（提升不足这个值不算提升）。
- 方法 `step(metric) -> bool`：记录本轮指标，需要停止时返回 `True`。
- 属性 `best` 记录最佳指标。

??? success "参考答案"

    ```python
    import math

    class EarlyStopping:
        def __init__(self, patience=3, mode="min", min_delta=0.0):
            if mode not in ("min", "max"):
                raise ValueError(f"mode must be 'min' or 'max', got {mode!r}")
            self.patience = patience
            self.sign = 1 if mode == "min" else -1
            self.min_delta = min_delta
            self.best = math.inf if mode == "min" else -math.inf
            self.bad_rounds = 0

        def improved(self, metric):
            return self.sign * (self.best - metric) > self.min_delta

        def step(self, metric):
            if self.improved(metric):
                self.best = metric
                self.bad_rounds = 0
            else:
                self.bad_rounds += 1
            return self.bad_rounds >= self.patience

    es = EarlyStopping(patience=2, mode="min", min_delta=0.01)
    for epoch, loss in enumerate([1.0, 0.8, 0.795, 0.792, 0.7]):
        stop = es.step(loss)
        print(epoch, loss, es.best, stop)
        if stop:
            break
    # 0 1.0 1.0 False
    # 1 0.8 0.8 False
    # 2 0.795 0.8 False
    # 3 0.792 0.8 True
    ```

    用 `sign` 把两种模式统一成一个比较式，避免写两套 `if`。第 2、3 轮的 0.795 和 0.792 比最佳值 0.8 低得不到 `min_delta`，都不算提升，连续两轮没有提升就停止。比较浮点数时要注意边界：`0.8 - 0.79` 的计算结果是 `0.010000000000000009`，会被判为大于 0.01。

## 5. 按 token 数动态分 batch

给定每条样本的长度 `lengths`，把样本分成若干 batch，要求每个 batch 补齐后的 token 数（`batch 内最大长度 × 样本数`）不超过 `max_tokens`。为了减少 padding，先按长度排序再分组。返回由样本下标组成的 batch 列表。单条样本就超过 `max_tokens` 时抛出 `ValueError`。

??? success "参考答案"

    ```python
    def token_budget_batches(lengths, max_tokens):
        order = sorted(range(len(lengths)), key=lambda i: lengths[i])
        batches, cur, cur_max = [], [], 0
        for i in order:
            L = lengths[i]
            if L > max_tokens:
                raise ValueError(f"sample {i} has length {L} > max_tokens {max_tokens}")
            new_max = max(cur_max, L)
            if cur and new_max * (len(cur) + 1) > max_tokens:
                batches.append(cur)
                cur, new_max = [], L
            cur.append(i)
            cur_max = new_max
        if cur:
            batches.append(cur)
        return batches

    lengths = [5, 30, 8, 12, 7, 25, 3, 9]
    bs = token_budget_batches(lengths, max_tokens=32)
    print(bs)
    # [[6, 0, 4, 2], [7, 3], [5], [1]]
    print([max(lengths[i] for i in b) * len(b) for b in bs])
    # [32, 24, 25, 30]

    import random
    random.seed(0)
    lens = [random.randint(1, 100) for _ in range(500)]
    bs = token_budget_batches(lens, 256)
    assert sorted(i for b in bs for i in b) == list(range(500))
    assert all(max(lens[i] for i in b) * len(b) <= 256 for b in bs)
    ```

    训练时通常还要把得到的 batch 顺序打乱，否则模型会依次看到从短到长的数据。

## 6. 训练一个最简 BPE

输入一个词频字典，例如 `{"low": 5, "lower": 2, "newest": 6, "widest": 3}`。每个词先拆成字符，词尾加 `</w>` 标记。重复 `num_merges` 次：统计所有相邻符号对的出现次数（按词频加权），把次数最多的符号对合并成一个新符号（次数相同时取字典序最小的对）。返回合并规则列表。

再写 `encode(word, merges)`：按合并规则学到的顺序，把一个新词切分成符号。

??? success "参考答案"

    ```python
    from collections import Counter

    def get_pair_counts(vocab):
        pairs = Counter()
        for symbols, freq in vocab.items():
            for a, b in zip(symbols, symbols[1:]):
                pairs[a, b] += freq
        return pairs

    def merge_symbols(symbols, pair):
        out, i = [], 0
        while i < len(symbols):
            if i + 1 < len(symbols) and (symbols[i], symbols[i + 1]) == pair:
                out.append(symbols[i] + symbols[i + 1])
                i += 2
            else:
                out.append(symbols[i])
                i += 1
        return tuple(out)

    def train_bpe(word_freqs, num_merges):
        vocab = {tuple(w) + ("</w>",): f for w, f in word_freqs.items()}
        merges = []
        for _ in range(num_merges):
            pairs = get_pair_counts(vocab)
            if not pairs:
                break
            best = min(pairs, key=lambda p: (-pairs[p], p))
            merges.append(best)
            vocab = {merge_symbols(s, best): f for s, f in vocab.items()}
        return merges

    def encode(word, merges):
        symbols = tuple(word) + ("</w>",)
        for pair in merges:
            symbols = merge_symbols(symbols, pair)
        return list(symbols)

    corpus = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
    merges = train_bpe(corpus, 6)
    print(merges)
    # [('e', 's'), ('es', 't'), ('est', '</w>'), ('l', 'o'), ('lo', 'w'), ('e', 'w')]
    print(encode("lowest", merges))     # ['low', 'est</w>']
    print(encode("newer", merges))      # ['n', 'ew', 'e', 'r', '</w>']
    ```

    这个 `encode` 对每条规则都扫描一遍整个词，规则有几万条时很慢。实际实现会在当前符号序列里找"在合并表中排名最靠前的相邻对"先合并，反复进行直到没有可合并的对，并配合缓存。GPT 系列使用的是在 UTF-8 字节上做的 byte-level BPE，思路相同。

## 7. top-k 与 top-p 采样

用 NumPy 实现 `sample(logits, temperature=1.0, top_k=0, top_p=1.0, rng=None)`，`logits` 形状为 `[V]`，返回采样得到的 token id。

- 先除以温度；`temperature == 0` 时直接返回 argmax。
- `top_k > 0` 时只保留概率最大的 `k` 个 token。
- `top_p < 1` 时按概率从大到小累加，保留累计概率刚好达到 `top_p` 的最小集合（至少保留一个 token）。
- 被过滤的 token 概率为 0，剩下的重新归一化。

??? success "参考答案"

    ```python
    import numpy as np

    def softmax(x):
        z = x - x.max()
        e = np.exp(z)
        return e / e.sum()

    def filter_probs(logits, temperature=1.0, top_k=0, top_p=1.0):
        probs = softmax(logits / temperature)
        keep = np.ones_like(probs, dtype=bool)
        if top_k > 0:
            kth = np.sort(probs)[-top_k]
            keep &= probs >= kth
        if top_p < 1.0:
            order = np.argsort(-probs)
            cum = np.cumsum(probs[order])
            # 累计概率"在加入该 token 之前"还没达到 top_p 的 token 都保留
            keep_sorted = (cum - probs[order]) < top_p
            mask = np.zeros_like(keep)
            mask[order[keep_sorted]] = True
            keep &= mask
        probs = np.where(keep, probs, 0.0)
        return probs / probs.sum()

    def sample(logits, temperature=1.0, top_k=0, top_p=1.0, rng=None):
        if temperature == 0:
            return int(np.argmax(logits))
        rng = rng or np.random.default_rng()
        p = filter_probs(logits, temperature, top_k, top_p)
        return int(rng.choice(len(p), p=p))

    logits = np.log(np.array([0.5, 0.2, 0.15, 0.1, 0.05]))
    print(np.round(filter_probs(logits, top_k=2), 3))      # [0.714 0.286 0.    0.    0.   ]
    print(np.round(filter_probs(logits, top_p=0.8), 3))    # [0.588 0.235 0.176 0.    0.   ]
    print(np.round(filter_probs(logits, top_p=0.01), 3))   # [1. 0. 0. 0. 0.]
    print(sample(logits, temperature=0))                   # 0

    rng = np.random.default_rng(0)
    draws = [sample(logits, top_p=0.8, rng=rng) for _ in range(20000)]
    freq = np.bincount(draws, minlength=5) / len(draws)
    print(np.round(freq, 2))       # [0.58 0.24 0.18 0.   0.  ]，与上面的概率接近
    ```

    `top_p=0.8` 时，前两个 token 的累计概率 0.7 还不到 0.8，所以第三个也要保留，累计到 0.85。判断条件写成"加入之前的累计概率 < top_p"，自然保证了概率最大的那个 token 一定被保留。`np.sort(probs)[-top_k]` 取第 k 大的概率，概率相同的 token 会一起被保留，可能略多于 k 个，这一点和多数框架的实现一致。

## 8. GRPO 的组内优势

GRPO 对每个 prompt 采样 `G` 条回答，用组内奖励的均值和标准差做归一化，得到每条回答的优势：

$$
A_i = \frac{r_i - \mathrm{mean}(r_{1..G})}{\mathrm{std}(r_{1..G}) + \epsilon}
$$

给定一维数组 `rewards`，长度为 `num_prompts * G`，同一个 prompt 的 `G` 条回答是相邻的。实现 `group_advantages(rewards, G, eps=1e-6)`，不使用 Python 循环。另外返回一个布尔数组，标出组内奖励全部相同（标准差为 0、这一组不提供学习信号）的 prompt。

??? success "参考答案"

    ```python
    import numpy as np

    def group_advantages(rewards, G, eps=1e-6):
        r = np.asarray(rewards, dtype=np.float64).reshape(-1, G)   # [num_prompts, G]
        mean = r.mean(axis=1, keepdims=True)
        std = r.std(axis=1, keepdims=True)
        adv = (r - mean) / (std + eps)
        degenerate = std.squeeze(1) == 0
        return adv.reshape(-1), degenerate

    rewards = [1, 0, 0, 1,   1, 1, 1, 1,   0, 0, 0, 1]
    adv, deg = group_advantages(rewards, G=4)
    print(np.round(adv.reshape(3, 4), 3))
    # [[ 1.    -1.    -1.     1.   ]
    #  [ 0.     0.     0.     0.   ]
    #  [-0.577 -0.577 -0.577  1.732]]
    print(deg)        # [False  True False]
    ```

    `reshape(-1, G)` 依赖"同一个 prompt 的回答相邻"这个前提。如果数据是按 `[G, num_prompts]` 的顺序排列的（先是每个 prompt 的第 1 条回答，再是第 2 条……），要改成 `reshape(G, -1)` 并沿 `axis=0` 计算，弄错了不会报错，只会悄悄地算出错误的优势。另外 `np.std` 默认除以 $G$（`ddof=0`），而 PyTorch 的 `tensor.std()` 默认除以 $G-1$，两者相差 $\sqrt{G/(G-1)}$ 倍，对照框架实现时要注意。实际训练中常把全部奖励相同的组过滤掉，DAPO 中的动态采样就是这样做的。

## 9. 构造 SFT 的 batch

给定若干条 `(prompt_ids, response_ids)`（都是 Python list），用 PyTorch 构造训练用的 batch：

- `input_ids`：prompt 和 response 拼接，末尾加 `eos_id`，右侧用 `pad_id` 补齐。
- `labels`：与 `input_ids` 相同，但 prompt 部分和 padding 部分设为 `-100`；response 和 `eos` 部分保留。
- `attention_mask`：真实 token 为 1，padding 为 0。
- 拼接后超过 `max_len` 的从右侧截断。

再用随机 logits 验证：对这个 batch 计算的 loss，只和 response 部分的 logits 有关。

??? success "参考答案"

    ```python
    import torch
    import torch.nn.functional as F

    def build_sft_batch(pairs, eos_id, pad_id, max_len):
        rows = []
        for prompt, response in pairs:
            ids = (prompt + response + [eos_id])[:max_len]
            labels = ([-100] * len(prompt) + response + [eos_id])[:max_len]
            rows.append((ids, labels))
        T = max(len(ids) for ids, _ in rows)
        B = len(rows)
        input_ids = torch.full((B, T), pad_id, dtype=torch.long)
        labels = torch.full((B, T), -100, dtype=torch.long)
        attention_mask = torch.zeros((B, T), dtype=torch.long)
        for i, (ids, lab) in enumerate(rows):
            n = len(ids)
            input_ids[i, :n] = torch.tensor(ids)
            labels[i, :n] = torch.tensor(lab)
            attention_mask[i, :n] = 1
        return {"input_ids": input_ids, "labels": labels, "attention_mask": attention_mask}

    def lm_loss(logits, labels):
        return F.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)),
                               labels[:, 1:].reshape(-1), ignore_index=-100)

    pairs = [([11, 12, 13], [21]), ([14], [23, 24, 25, 26])]
    b = build_sft_batch(pairs, eos_id=2, pad_id=0, max_len=16)
    for k, v in b.items():
        print(k, v.tolist())
    # input_ids [[11, 12, 13, 21, 2, 0], [14, 23, 24, 25, 26, 2]]
    # labels [[-100, -100, -100, 21, 2, -100], [-100, 23, 24, 25, 26, 2]]
    # attention_mask [[1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1]]

    b2 = build_sft_batch([([1, 2, 3, 4], [5, 6])], eos_id=2, pad_id=0, max_len=5)
    print(b2["input_ids"].tolist(), b2["labels"].tolist())   # [[1, 2, 3, 4, 5]] [[-100, -100, -100, -100, 5]]

    torch.manual_seed(0)
    b3 = build_sft_batch([([1, 2, 3], [4]), ([1], [4, 5, 6, 7])], eos_id=2, pad_id=0, max_len=16)
    logits = torch.randn(2, 6, 10, requires_grad=True)
    lm_loss(logits, b3["labels"]).backward()
    used = logits.grad.abs().sum(-1) > 0           # 哪些位置的 logits 收到了梯度
    print(used.int().tolist())
    # [[0, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0]]
    ```

    位置 $t$ 的 logits 预测位置 $t+1$ 的 token，所以收到梯度的是"下一个 label 不为 -100"的位置：第一条样本里 prompt 最后一个 token（位置 2）预测回答的第一个 token，位置 3 预测 `eos`；位置 4 是 `eos`，后面没有要预测的 token，位置 5 是 padding。验证 mask 的这种方法，比肉眼检查张量可靠得多。

## 10. RMSNorm

Llama 等模型用 RMSNorm 代替 LayerNorm：

$$
\mathrm{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^d x_i^2 + \epsilon}} \odot g
$$

其中 $g$ 是可学习的缩放参数，初始化为全 1。用 `nn.Module` 实现，要求：输入可以是任意形状 `[..., d]`；计算在 float32 下进行，输出转回输入的 dtype。用 `torch.nn.RMSNorm`（PyTorch 2.4+）验证结果。

??? success "参考答案"

    ```python
    import torch
    import torch.nn as nn

    class RMSNorm(nn.Module):
        def __init__(self, dim, eps=1e-6):
            super().__init__()
            self.eps = eps
            self.weight = nn.Parameter(torch.ones(dim))

        def forward(self, x):
            dtype = x.dtype
            x = x.float()
            x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
            return (self.weight * x).to(dtype)

    torch.manual_seed(0)
    x = torch.randn(2, 5, 64)
    ours = RMSNorm(64)
    ref = nn.RMSNorm(64, eps=1e-6)
    with torch.no_grad():
        ours.weight.uniform_(0.5, 1.5)
        ref.weight.copy_(ours.weight)
    print(torch.allclose(ours(x), ref(x), atol=1e-6))           # True
    print(ours(x.bfloat16()).dtype)                              # torch.bfloat16
    y = ours(x) / ours.weight
    print(round(y.pow(2).mean(-1).mean().item(), 4))             # 1.0，归一化后均方值约为 1
    print(sum(p.numel() for p in ours.parameters()))             # 64
    ```

    `nn.Parameter` 包装后的张量会被注册为模块参数。`torch.rsqrt` 计算 $1/\sqrt{x}$。在 bf16 下直接求平方和误差较大，所以先转 float32，这也是 Hugging Face 中 `LlamaRMSNorm` 的写法。
