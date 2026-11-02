# LLM / VLM

```mermaid
graph LR
  A[数据] --> B[预训练]
  B --> C[SFT 监督微调]
  C --> D[偏好对齐 RLHF/DPO/GRPO]
  D --> E[推理与部署]
```

| 主题 | 笔记 |
| --- | --- |
| 模型结构 | [Transformer 架构](transformer.md) |
| 训练第一阶段 | [预训练](pretraining.md) |
| 训练第二阶段 | [监督微调 SFT](sft.md) |
| 训练第三阶段 | [RLHF / DPO / GRPO](../rl/rlhf.md) |

## 全部文章

<!-- articles -->
