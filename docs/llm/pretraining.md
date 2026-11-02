---
date: 2026-11-01
description: 下一个 token 预测目标、Scaling Law、并行策略与训练稳定性。
tags:
  - 大模型
  - 训练
---

# 预训练

## 目标：下一个 token 预测

$$
\mathcal{L}(\theta) = -\sum_{t=1}^{T} \log p_\theta(x_t \mid x_{<t})
$$

## 关键要素

- **数据**：网页、代码、书籍、论文；去重、质量过滤、配比是效果的大头
- **Scaling Law**：Chinchilla 的经验结论是计算最优时 token 数约为参数量的 ~20 倍
- **并行**：数据并行（DP/ZeRO/FSDP）、张量并行（TP）、流水线并行（PP）、序列并行
- **稳定性**：warmup + cosine 衰减、梯度裁剪、BF16 混合精度、监控 loss spike

## 待补充

- [ ] 数据配比实验
- [ ] MoE 训练
