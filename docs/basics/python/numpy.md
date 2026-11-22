---
date: 2026-11-05
description: ndarray 的 shape 与 dtype、索引（视图与拷贝）、reshape 与转置、按 axis 规约、广播规则、向量化、数值稳定的 softmax 与 logsumexp、matmul 与 einsum，最后用 NumPy 实现带因果掩码的多头注意力。
tags:
  - Python
  - NumPy
---

# NumPy

NumPy 的数组操作和 PyTorch 的张量操作几乎一一对应：shape、广播、索引、`einsum` 的规则完全相同。在 NumPy 里把这些概念弄清楚，读模型代码时就不会被维度变换卡住。

```python
import numpy as np
```

## 1. 创建数组

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape, a.ndim, a.size, a.dtype)    # (2, 3) 2 6 int64

print(np.zeros((2, 3)).dtype)              # float64
print(np.ones(3, dtype=np.float32))        # [1. 1. 1.]
print(np.full((2, 2), -np.inf))            # 全是 -inf 的 2x2 数组
print(np.arange(0, 10, 3))                 # [0 3 6 9]，不含终点
print(np.linspace(0, 1, 5))                # [0.   0.25 0.5  0.75 1.  ]，含终点
print(np.eye(3).shape)                     # (3, 3) 单位阵
```

随机数用新的 Generator 接口，固定种子保证可复现：

```python
rng = np.random.default_rng(0)
x = rng.standard_normal((2, 3))   # 标准正态
u = rng.uniform(0, 1, size=4)
idx = rng.permutation(5)          # 0..4 的随机排列
pick = rng.choice(10, size=3, replace=False)
print(x.shape, u.shape, sorted(idx.tolist()), len(set(pick.tolist())))   # (2, 3) (4,) [0, 1, 2, 3, 4] 3
```

## 2. dtype

```python
x = np.array([1.5, 2.5])
print(x.dtype, x.itemsize, x.nbytes)        # float64 8 16
y = x.astype(np.float16)
print(y.dtype, y.nbytes)                    # float16 4
print(np.array([1, 2]) / 2)                 # [0.5 1. ]，int 除法结果是 float
print(float(np.finfo(np.float16).max))      # 65504.0
print(np.float16(70000))                    # inf，溢出（同时给出 RuntimeWarning）
print(np.float32(1) + np.float32(1e-8) == 1)   # True，精度不够，加不上去
```

估算显存时要用到 `itemsize`：一个 7B 参数的模型，bf16/fp16 每个参数 2 字节，光权重就是 14 GB。fp16 的最大值只有 65504，这是 fp16 训练需要 loss scaling、而 bf16 一般不需要的原因（bf16 的指数位和 fp32 一样多，表示范围相同，只是精度更低）。NumPy 没有 bf16 类型。

## 3. 索引与切片

```python
a = np.arange(12).reshape(3, 4)
print(a)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
print(a[1, 2], a[-1])        # 6 [ 8  9 10 11]
print(a[:, 1])               # [1 5 9]，第 1 列
print(a[:2, 1:3])            # [[1 2] [5 6]]
print(a[..., -1])            # [ 3  7 11]，... 表示前面所有维度
```

### 视图与拷贝

**切片返回视图**，和原数组共享内存，修改视图会改到原数组：

```python
a = np.arange(6)
v = a[1:4]
v[0] = 100
print(a)                       # [  0 100   2   3   4   5]
print(np.shares_memory(a, v))  # True
c = a[1:4].copy()              # 需要独立的数据时显式 copy
```

这和 Python list 的切片（会复制）相反，是最容易出错的地方之一。

### 花式索引与布尔索引

用整数数组或布尔数组做索引，结果是**拷贝**：

```python
a = np.arange(10) * 10
print(a[[0, 3, 3, 7]])        # [ 0 30 30 70]
mask = a > 50
print(mask.sum(), a[mask])    # 4 [60 70 80 90]
a[a > 50] = 0                 # 赋值时会直接写回原数组
print(a)                      # [ 0 10 20 30 40 50  0  0  0  0]
```

二维情况下，用两个整数数组分别指定行和列，按位置配对取元素：

```python
logits = np.array([[0.1, 0.7, 0.2],
                   [0.5, 0.3, 0.2]])
labels = np.array([1, 0])
print(logits[np.arange(2), labels])    # [0.7 0.5]，每行取 label 对应的那一列
```

这就是计算交叉熵时"取出正确类别的概率"的方法，PyTorch 里对应 `torch.gather`。

## 4. 形状变换

```python
x = np.arange(24)
y = x.reshape(2, 3, 4)
print(y.shape, x.reshape(4, -1).shape)    # (2, 3, 4) (4, 6)，-1 表示自动推断
print(y.transpose(0, 2, 1).shape)         # (2, 4, 3)，交换后两维
print(y.T.shape)                          # (4, 3, 2)，反转所有维度
print(np.swapaxes(y, 0, 1).shape)         # (3, 2, 4)
print(y[:, None].shape, y[..., None].shape)   # (2, 1, 3, 4) (2, 3, 4, 1)，插入长度为 1 的维度
print(np.expand_dims(x, 0).shape)         # (1, 24)
print(np.zeros((1, 3, 1)).squeeze().shape)    # (3,)
print(y.reshape(-1).shape)                # (24,) 展平
```

`reshape` 按"行优先"（最后一维变化最快）的顺序重新解释数据。理解这一点才能正确地拆分注意力头：

```python
B, T, H, D = 2, 5, 4, 8                     # batch、序列长度、头数、每头维度
x = np.arange(B * T * H * D).reshape(B, T, H * D)   # 投影后的 [B, T, d_model]
heads = x.reshape(B, T, H, D).transpose(0, 2, 1, 3) # [B, H, T, D]
print(heads.shape)                                   # (2, 4, 5, 8)
back = heads.transpose(0, 2, 1, 3).reshape(B, T, H * D)
print(np.array_equal(back, x))                       # True
```

注意 `x.reshape(B, H, T, D)` 虽然 shape 也对，但数据的排列完全错了：它把同一个 token 的特征拆散到了不同的位置。正确做法是先把最后一维拆成 `(H, D)`，再用转置把 `H` 移到前面。

### 拼接与堆叠

```python
a, b = np.zeros((2, 3)), np.ones((2, 3))
print(np.concatenate([a, b], axis=0).shape)   # (4, 3)，沿已有维度拼接
print(np.concatenate([a, b], axis=1).shape)   # (2, 6)
print(np.stack([a, b], axis=0).shape)         # (2, 2, 3)，新增一个维度
```

## 5. 按 axis 规约

`axis=k` 表示沿第 k 维做运算，**这一维消失**：

```python
x = np.array([[1, 2, 3],
              [4, 5, 6]])
print(x.sum(), x.sum(axis=0), x.sum(axis=1))   # 21 [5 7 9] [ 6 15]
print(x.mean(axis=1, keepdims=True))           # [[2.] [5.]]，保留长度为 1 的维度，shape (2, 1)
print(x.max(axis=1), x.argmax(axis=1))         # [3 6] [2 2]
print(np.cumsum(x, axis=1))                    # [[ 1  3  6] [ 4  9 15]]
```

`keepdims=True` 让结果可以直接和原数组做广播运算，下面实现 softmax 时就要用到。

## 6. 广播

两个数组形状不同时，NumPy 按以下规则自动扩展：

1. 从**最后一维**开始向前逐维对齐；维数少的数组在前面补 1。
2. 每一维上，两者长度相等，或者其中一个是 1，就可以广播；长度为 1 的那个被复制扩展。
3. 否则报错。

```python
x = np.ones((4, 3))
print((x + np.array([1, 2, 3])).shape)   # (4, 3)：(4,3) 和 (3,) → (4,3) 和 (1,3)
print((x + np.ones((4, 1))).shape)       # (4, 3)
print((np.ones((5, 1, 3)) + np.ones((4, 1))).shape)   # (5, 4, 3)
try:
    x + np.ones(4)
except ValueError as e:
    print("error:", e)
# error: operands could not be broadcast together with shapes (4,3) (4,)
```

常见用法：

```python
X = rng.standard_normal((100, 8))
Xn = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)       # 按列标准化
print(np.allclose(Xn.mean(axis=0), 0), np.allclose(Xn.std(axis=0), 1, atol=1e-6))   # True True

# 两组向量之间的两两距离：[N,1,D] - [1,M,D] → [N,M,D]
A, Bm = rng.standard_normal((3, 2)), rng.standard_normal((4, 2))
dist = np.sqrt(((A[:, None, :] - Bm[None, :, :]) ** 2).sum(-1))
print(dist.shape)        # (3, 4)
```

广播很方便，也很容易"悄悄地算错"：shape 为 `(N,)` 和 `(N, 1)` 的数组相减，得到的是 `(N, N)`，不会报错。

```python
pred = np.array([1.0, 2.0, 3.0])        # (3,)
target = pred.reshape(3, 1)              # (3, 1)
print((pred - target).shape)             # (3, 3)，本意是逐元素相减
```

计算 loss 前检查一下两边的 shape 是否完全一致，能避免很多这样的错误。

## 7. 向量化

能用数组运算表达的，就不要写 Python 循环。

```python
import time

x = rng.standard_normal(1_000_000)

t0 = time.perf_counter()
s = 0.0
for v in x:
    s += v * v
t_loop = time.perf_counter() - t0

t0 = time.perf_counter()
s2 = np.dot(x, x)
t_vec = time.perf_counter() - t0

print(np.isclose(s, s2), t_loop > 20 * t_vec)    # True True
```

在一般的机器上，两者速度相差两个数量级左右。Python 循环里每一步都要做类型检查、创建对象；NumPy 的运算在编译好的 C 代码里完成，还能利用 SIMD 指令。

一些常用的向量化函数：

```python
x = np.array([-2.0, -0.5, 0.0, 1.5])
print(np.where(x > 0, x, 0.0))         # [0.  0.  0.  1.5]，相当于 relu
print(np.clip(x, -1, 1))               # [-1.  -0.5  0.   1. ]
print(np.maximum(x, 0))                # 与 np.where 那行相同
print(np.abs(x).max(), np.sign(x))     # 2.0 [-1. -1.  0.  1.]
print(np.unique([3, 1, 3, 2], return_counts=True))   # (array([1, 2, 3]), array([1, 1, 2]))
print(np.argsort([0.3, 0.1, 0.2]))     # [1 2 0]
```

## 8. 数值稳定的 softmax 与 logsumexp

直接按定义计算 $\mathrm{softmax}(x)_i = e^{x_i}/\sum_j e^{x_j}$，当 $x$ 中有较大的值时 $e^{x}$ 会溢出：

```python
def softmax_naive(x):
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)

with np.errstate(over="ignore", invalid="ignore"):
    print(softmax_naive(np.array([1000.0, 1000.0])))   # [nan nan]
```

利用 $\mathrm{softmax}(x) = \mathrm{softmax}(x - c)$ 对任意常数 $c$ 成立，先减去最大值，指数的参数就都不大于 0：

```python
def softmax(x, axis=-1):
    z = x - x.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)

def logsumexp(x, axis=-1):
    m = x.max(axis=axis, keepdims=True)
    return (m + np.log(np.exp(x - m).sum(axis=axis, keepdims=True))).squeeze(axis)

def log_softmax(x, axis=-1):
    return x - np.expand_dims(logsumexp(x, axis), axis)

x = np.array([[1000.0, 1000.0], [1.0, 2.0]])
print(softmax(x))
# [[0.5        0.5       ]
#  [0.26894142 0.73105858]]
print(logsumexp(x))         # [1000.69314718    2.31326169]
print(np.allclose(np.exp(log_softmax(x)), softmax(x)))   # True
```

交叉熵就是负的 log_softmax 在正确类别上的值。计算 log 概率时应当直接用 `log_softmax`，而不是先算 softmax 再取 log：后者在概率很小时会得到 `log(0) = -inf`。

```python
def cross_entropy(logits, labels):
    logp = log_softmax(logits)
    return -logp[np.arange(len(labels)), labels].mean()

logits = np.array([[2.0, 0.5, -1.0], [0.1, 0.2, 3.0]])
print(round(cross_entropy(logits, np.array([0, 2])), 4))   # 0.1755
```

## 9. 矩阵乘法与 einsum

```python
A = rng.standard_normal((2, 3))
B = rng.standard_normal((3, 4))
print((A @ B).shape)                   # (2, 4)
print((A * A).shape)                   # (2, 3)，* 是逐元素乘法，不是矩阵乘法

# 批量矩阵乘：前面的维度做广播，最后两维做矩阵乘法
Q = rng.standard_normal((2, 4, 5, 8))  # [B, H, T, D]
K = rng.standard_normal((2, 4, 5, 8))
print((Q @ K.swapaxes(-1, -2)).shape)  # (2, 4, 5, 5)
```

`einsum` 用下标字符串描述运算：输入中出现、输出中不出现的下标会被求和。

```python
print(np.einsum("ij,jk->ik", A, B).shape)            # 矩阵乘法 (2, 4)
print(np.einsum("ii->", np.eye(3)))                  # 3.0，迹
print(np.einsum("ij->ji", A).shape)                  # (3, 2)，转置
scores = np.einsum("bhqd,bhkd->bhqk", Q, K)          # 注意力分数
print(scores.shape, np.allclose(scores, Q @ K.swapaxes(-1, -2)))   # (2, 4, 5, 5) True
v1, v2 = np.ones(3), np.arange(3.0)
print(np.einsum("i,j->ij", v1, v2).shape)            # (3, 3)，外积
```

维度多、需要转置的运算，`einsum` 往往比 `@` 加一堆 `transpose` 清楚。

## 10. 综合：多头因果自注意力

把前面的内容合在一起，实现一个 decoder 中的多头自注意力（前向计算）：

$$
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d}} + M\right)V
$$

其中 $M$ 是因果掩码：位置 $i$ 只能看到 $j \le i$，其余位置填 $-\infty$。

```python
def causal_self_attention(x, Wq, Wk, Wv, Wo, n_heads):
    """x: [B, T, C]，W*: [C, C]，返回 [B, T, C]"""
    B, T, C = x.shape
    D = C // n_heads

    def split(t):                              # [B, T, C] -> [B, H, T, D]
        return t.reshape(B, T, n_heads, D).transpose(0, 2, 1, 3)

    q, k, v = split(x @ Wq), split(x @ Wk), split(x @ Wv)
    scores = q @ k.transpose(0, 1, 3, 2) / np.sqrt(D)          # [B, H, T, T]

    mask = np.triu(np.ones((T, T), dtype=bool), k=1)           # 对角线以上为 True
    scores = np.where(mask, -np.inf, scores)                    # [T, T] 广播到 [B, H, T, T]

    attn = softmax(scores, axis=-1)
    out = attn @ v                                              # [B, H, T, D]
    out = out.transpose(0, 2, 1, 3).reshape(B, T, C)            # 合并头
    return out @ Wo, attn

B, T, C, H = 2, 4, 16, 4
x = rng.standard_normal((B, T, C))
Ws = [rng.standard_normal((C, C)) / np.sqrt(C) for _ in range(4)]
y, attn = causal_self_attention(x, *Ws, n_heads=H)
print(y.shape, attn.shape)                    # (2, 4, 16) (2, 4, 4, 4)
print(np.allclose(attn.sum(-1), 1))           # True，每行是一个概率分布
print((attn[0, 0] > 0).astype(int))
# [[1 0 0 0]
#  [1 1 0 0]
#  [1 1 1 0]
#  [1 1 1 1]]，被掩码的位置权重严格为 0
```

验证因果性：修改最后一个位置的输入，前面位置的输出不应该改变。

```python
x2 = x.copy()
x2[:, -1] += 10.0
y2, _ = causal_self_attention(x2, *Ws, n_heads=H)
print(np.allclose(y[:, :-1], y2[:, :-1]), np.allclose(y[:, -1], y2[:, -1]))   # True False
```

这类"改输入、看输出"的检查，在自己实现模型组件时很有用。

## 11. 其他要点

- `np.save("a.npy", arr)` / `np.load("a.npy")` 保存单个数组；`np.savez` 保存多个；大数组可以用 `np.load(..., mmap_mode="r")` 以内存映射方式打开，不必整体读入。预训练语料 tokenize 之后常存成一个巨大的 `uint16`/`uint32` 一维数组，训练时用 `np.memmap` 随机切片读取。
- `arr.tolist()` 转回 Python list；`arr.item()` 取出单元素数组的 Python 标量。
- `np.isnan(x).any()`、`np.isfinite(x).all()` 检查数值异常。
- 比较浮点数组用 `np.allclose(a, b)`，不要用 `(a == b).all()`。
