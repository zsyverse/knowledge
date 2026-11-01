---
tags:
  - 强化学习
---

# 基础概念

## 马尔可夫决策过程（MDP）

$(\mathcal{S}, \mathcal{A}, P, R, \gamma)$：状态、动作、转移概率、奖励、折扣因子。

回报：$G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k}$

## 价值函数

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid s_t = s], \qquad
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid s_t = s, a_t = a]
$$

优势函数：$A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s)$

## Bellman 方程

$$
V^\pi(s) = \sum_a \pi(a\mid s) \sum_{s'} P(s'\mid s,a)\big[R(s,a) + \gamma V^\pi(s')\big]
$$

## 方法分类

| 类别 | 代表算法 |
| --- | --- |
| 基于价值 | Q-Learning, DQN |
| 基于策略 | REINFORCE, PPO |
| Actor-Critic | A2C, SAC |
