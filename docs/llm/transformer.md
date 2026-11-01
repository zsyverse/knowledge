---
tags:
  - 大模型
  - 架构
---

# Transformer 架构

## 自注意力

给定输入 $X \in \mathbb{R}^{n \times d}$，投影得到 $Q = XW_Q,\ K = XW_K,\ V = XW_V$：

$$
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V
$$

- 除以 $\sqrt{d_k}$：防止点积随维度增大导致 softmax 饱和、梯度消失
- $M$ 是因果掩码（decoder-only 模型中未来位置为 $-\infty$）
- 复杂度：时间与显存都是 $O(n^2)$，这是长上下文的核心瓶颈

## 多头注意力（MHA）与变体

| 变体 | K/V 头数 | 作用 |
| --- | --- | --- |
| MHA | = Q 头数 | 原始设计 |
| MQA | 1 | 极大减少 KV Cache |
| GQA | 分组共享 | Llama 2/3 等采用，效果与速度折中 |

## 现代 LLM 的常见改动

- **Pre-Norm + RMSNorm**：训练更稳定
- **RoPE 旋转位置编码**：相对位置信息，便于长度外推
- **SwiGLU** 激活的 FFN
- 去掉 bias

```python
import torch, torch.nn.functional as F

def attention(q, k, v, causal=True):
    d = q.size(-1)
    scores = q @ k.transpose(-2, -1) / d ** 0.5
    if causal:
        n = q.size(-2)
        mask = torch.triu(torch.ones(n, n, dtype=torch.bool), 1)
        scores = scores.masked_fill(mask, float("-inf"))
    return F.softmax(scores, dim=-1) @ v
```

!!! note "参考"
    Vaswani et al., *Attention Is All You Need*, 2017
