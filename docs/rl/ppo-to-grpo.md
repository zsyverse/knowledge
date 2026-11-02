---
date: 2026-11-02
description: 大模型对齐的 RL 算法演进，主线是不断拿掉组件：从 PPO 的四个模型，到 DPO 去掉 RL，再到 GRPO 去掉 Critic。
tags:
  - 强化学习
  - 大模型
  - 对齐
  - 算法
---

# 从 PPO 到 GRPO：大模型 RL 训练在简化什么

!!! abstract "TL;DR"
    大模型对齐的 RL 算法演进，主线是**不断拿掉组件**：PPO 需要 策略 + 参考模型 + 奖励模型 + Critic 四个模型；DPO 把奖励模型和在线采样都拿掉；GRPO 保留在线采样，但用组内相对奖励替代 Critic。拿掉什么、保留什么，决定了各自适用的场景。

## 1. 起点：PPO-RLHF 为什么重

InstructGPT 式的 RLHF 在训练时要同时维护四个模型：

| 模型 | 作用 | 是否更新 |
| --- | --- | --- |
| 策略 $\pi_\theta$ | 生成回答 | ✓ |
| 参考模型 $\pi_\text{ref}$ | 计算 KL 惩罚 | ✗ |
| 奖励模型 $r_\phi$ | 给回答打分 | ✗ |
| Critic $V_\psi$ | 估计价值，用于 GAE 算优势 | ✓ |

优化目标是带 KL 约束的奖励最大化：

$$
\max_{\pi_\theta}\ \mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi_\theta}\big[r_\phi(x,y)\big] - \beta\,\mathrm{KL}\big(\pi_\theta\,\|\,\pi_\text{ref}\big)
$$

问题在于：显存开销大、超参多，而且 Critic 在语言任务上很难训好——奖励通常只在序列末尾给出，逐 token 的价值估计噪声很大。

## 2. DPO：把 RL 变成分类

DPO 的关键观察是，上面这个 KL 约束问题有闭式最优解：

$$
\pi^*(y\mid x) \propto \pi_\text{ref}(y\mid x)\exp\!\big(r(x,y)/\beta\big)
$$

反解出奖励 $r = \beta \log \frac{\pi^*}{\pi_\text{ref}} + \text{const}$，代入 Bradley–Terry 偏好模型，常数项相消，得到只依赖策略本身的损失：

$$
\mathcal{L}_\text{DPO} = -\log\sigma\!\left(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_\text{ref}(y_w\mid x)} - \beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_\text{ref}(y_l\mid x)}\right)
$$

**代价**：离线训练，只能从固定的偏好数据里学，没有探索。

## 3. GRPO：保留在线探索，拿掉 Critic

GRPO（DeepSeekMath 提出，DeepSeek-R1 采用）对每个问题采样 $G$ 个回答，用组内统计量当基线：

$$
\hat A_i = \frac{r_i - \mathrm{mean}(\{r_j\}_{j=1}^G)}{\mathrm{std}(\{r_j\}_{j=1}^G)}
$$

同一回答的所有 token 共享这个优势，再代入 PPO-Clip 目标并加 KL 项。

**为什么有效**：同一个问题的多个回答天然构成了"对照组"，组均值就是一个不需要学习的价值估计。配合**可验证奖励**（答案对不对、代码能不能跑通），连奖励模型也可以换成规则。

## 4. 对比

| | 奖励模型 | Critic | 在线采样 | 适合场景 |
| --- | --- | --- | --- | --- |
| PPO-RLHF | ✓ | ✓ | ✓ | 通用对齐，资源充足 |
| DPO | ✗ | ✗ | ✗ | 有现成偏好数据，追求简单稳定 |
| GRPO | 可用规则 | ✗ | ✓ | 数学、代码等可验证任务 |

## 5. 我的疑问

- [ ] 组内 std 很小时（全对或全错）优势会怎样？——后续工作如 DAPO 对此有讨论
- [ ] 序列级优势分配到每个 token，长回答是否被不公平地加权？

## 参考

1. Ouyang et al. *Training language models to follow instructions with human feedback.* 2022.
2. Rafailov et al. *Direct Preference Optimization: Your Language Model is Secretly a Reward Model.* 2023.
3. Shao et al. *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models.* 2024.
4. DeepSeek-AI. *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.* 2025.

??? quote "引用本文"
    ```bibtex
    @article{zsyverse2026ppo2grpo,
      title  = {从 PPO 到 GRPO：大模型 RL 训练在简化什么},
      author = {zsyverse},
      year   = {2026},
      url    = {https://zsyverse.github.io/knowledge/rl/ppo-to-grpo/}
    }
    ```
