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

裁剪限制每次更新的步幅，是对 TRPO 信赖域约束的简单近似。

## GAE

$$
\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t), \qquad
\hat A_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}
$$

$\lambda$ 在偏差与方差之间折中。
