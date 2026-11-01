---
tags:
  - 大模型
  - 训练
---

# 监督微调 SFT

用 (prompt, response) 对继续训练，**只在 response 部分计算 loss**：

$$
\mathcal{L}_{\text{SFT}} = -\sum_{t \in \text{response}} \log p_\theta(y_t \mid x, y_{<t})
$$

## 要点

- 数据质量 > 数量（LIMA：约 1000 条高质量数据即可显著对齐格式）
- 使用 chat template，注意特殊 token 与 loss mask
- 参数高效微调：**LoRA** 将 $\Delta W = BA$，$B\in\mathbb{R}^{d\times r}, A\in\mathbb{R}^{r\times k}$，$r \ll d$

??? tip "LoRA 常用超参"
    rank 8–64，alpha 通常取 rank 的 1–2 倍，作用于 attention 和 MLP 的线性层。
