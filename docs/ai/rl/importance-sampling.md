---
date: 2026-11-02
description: 从易采样的提议分布中抽样，用权重 p/q 修正，恢复目标分布下的期望；在 RL 中用于离策略评估与学习。
tags:
  - 强化学习
  - 数学基础
---

# 重要性采样

> 当我们难以从目标概率分布中直接采样，或者目标分布中的某些区域对估计结果贡献特别大时，可以从另一个更容易采样的分布中抽取样本，再通过权重修正（Weight Correction）恢复原本的期望。

## 数学推导

假设我们希望计算目标分布 \(p(x)\) 下的期望：

\[ \mathbb E_{p(x)}[f(x)] =\int f(x)p(x)dx \]

由于直接从 \(p(x)\) 采样可能比较困难，因此引入一个容易采样的提议分布（Proposal Distribution，提议分布）\(q(x)\)，在积分中乘除 \(q(x)\)，得到：

\[ \begin{aligned} \mathbb E_p[f(x)] &=\int f(x)p(x)dx\\ &=\int f(x)\frac{p(x)}{q(x)}q(x)dx\\ &=\mathbb E_q\left[ f(x)\frac{p(x)}{q(x)} \right] \end{aligned} \]

因此，我们可以从 \(q(x)\) 中采样 \(N\) 个样本 \(x_i\)，并定义重要性权重（Importance Weight，重要性权重）：

\[ w_i=\frac{p(x_i)}{q(x_i)} \]

最终得到重要性采样估计量：

\[ \boxed{ \mathbb E_p[f(x)] \approx \frac{1}{N}\sum_{i=1}^{N}w_i f(x_i) } \]

核心直觉： 样本虽然来自 \(q(x)\)，但通过权重 \(p(x)/q(x)\) 修正不同区域的采样概率，使最终估计能够逼近目标分布 \(p(x)\) 下的真实期望。

## 在RL中的应用

智能体（Agent，智能体）需要根据状态 \(s\) 选择动作 \(a\)。

策略（Policy，策略）表示：

\[ \pi(a|s) \]

它表示在状态 \(s\) 下，选择动作 \(a\) 的概率。

假设我们有两个策略：

- \(\pi(a|s)\)：目标策略（Target Policy），我们希望优化的策略。
- \(\beta(a|s)\)：行为策略（Behavior Policy），实际生成训练数据的策略。

假设训练数据是由旧策略 \(\beta\) 生成的，但我们现在希望评估新策略 \(\pi\)。

这时就出现了一个问题：

数据来自旧策略，目标却是新策略。

我们可以使用重要性采样：

\[ \boxed{ w(s,a)=\frac{\pi(a|s)}{\beta(a|s)} } \]

这个权重衡量了新旧策略对同一个动作的概率分配差异。

例如：

\[ \pi(a|s)=0.8 \]

\[ \beta(a|s)=0.2 \]

那么：

\[ w(s,a)=\frac{0.8}{0.2}=4 \]

说明目标策略选择这个动作的概率是旧策略的 4 倍，因此需要给予这个样本更大的权重。

在 RL 中，这种方法常用于 Off-policy Evaluation（离策略评估）和 Off-policy Learning（离策略学习）。





