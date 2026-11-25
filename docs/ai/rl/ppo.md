---
date: 2026-11-01
description: 策略梯度定理、PPO-Clip 目标与 GAE 优势估计。
tags:
  - 强化学习
  - 算法
---

# 策略梯度与 PPO

## 策略梯度定理

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta}\big[\nabla_\theta \log \pi_\theta(a_t\mid s_t)\, A_t\big]
$$

## PPO-Clip

令 $r_t(\theta) = \dfrac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_\text{old}}(a_t\mid s_t)}$：

$$
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\Big[\min\big(r_t(\theta)A_t,\ \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)A_t\big)\Big]
$$

这个比值就是[重要性采样](importance-sampling.md)的权重：数据由旧策略采集，用它修正到新策略。裁剪限制每次更新的步幅，是对 TRPO 信赖域约束的简单近似。$A_t>0$ 时比值超过 $1+\epsilon$ 后不再有梯度，$A_t<0$ 时比值低于 $1-\epsilon$ 后不再有梯度；外层的 $\min$ 取未裁剪项与裁剪项中较小的一个，得到原目标的一个下界（悲观估计）。

## GAE

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t), \qquad
\hat A_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}
$$

这里的 $r_t$ 是第 $t$ 步的奖励，与上一节的比值 $r_t(\theta)$ 不是一回事（PPO 原文沿用了这两个记号）。$\delta_t$ 是一步 TD 误差。

$\lambda$ 在偏差与方差之间折中：$\lambda=0$ 时 $\hat A_t=\delta_t$，方差小，但完全依赖 $V$ 的准确性，偏差大；$\lambda=1$ 时 $\hat A_t=\sum_l\gamma^l r_{t+l}-V(s_t)$，即蒙特卡洛回报减基线，偏差小而方差大。常用 $\lambda\approx0.95$。
