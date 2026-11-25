---
date: 2026-11-02
description: 从易采样的提议分布中抽样，用权重 p/q 修正，恢复目标分布下的期望；方差、最优提议分布、自归一化，以及在 RL 中的离策略修正。
tags:
  - 强化学习
  - 数学基础
---

# 重要性采样

难以从目标概率分布中直接采样，或者目标分布中的某些区域对估计结果贡献特别大时，可以从另一个更容易采样的分布中抽取样本，再通过权重修正（weight correction）恢复原本的期望。

!!! abstract "要点"

    - 恒等式：$\mathbb E_p[f(x)]=\mathbb E_q\!\left[\dfrac{p(x)}{q(x)}f(x)\right]$，权重 $w=p/q$。
    - 成立条件：凡是 $p(x)f(x)\neq 0$ 的地方都要有 $q(x)>0$。
    - 估计无偏，但方差取决于 $q$ 与 $|f|p$ 的形状有多接近；$q$ 选得好，方差可以比直接采样小几百倍，选得差则会大得多。
    - 只知道 $p$ 的未归一化形式时，用自归一化估计 $\sum w_if_i/\sum w_i$（有偏、一致）。
    - RL 中权重是策略比值 $\pi(a|s)/\beta(a|s)$；整条轨迹的权重是逐步比值的连乘，方差随步数爆炸，所以 PPO 等方法只用单步比值并裁剪或截断。

## 数学推导

要计算目标分布 $p(x)$ 下的期望：

$$
\mathbb E_{p}[f(x)] =\int f(x)p(x)\,dx
$$

直接从 $p(x)$ 采样可能比较困难，于是引入一个容易采样的提议分布（proposal distribution）$q(x)$，在积分中乘除 $q(x)$：

$$
\begin{aligned}
\mathbb E_p[f(x)] &=\int f(x)p(x)\,dx\\
&=\int f(x)\frac{p(x)}{q(x)}q(x)\,dx\\
&=\mathbb E_q\left[ f(x)\frac{p(x)}{q(x)} \right]
\end{aligned}
$$

于是可以从 $q(x)$ 中采样 $N$ 个样本 $x_i$，定义重要性权重（importance weight）：

$$
w_i=\frac{p(x_i)}{q(x_i)}
$$

得到重要性采样估计量：

$$
\boxed{ \hat\mu_{\text{IS}}=\frac{1}{N}\sum_{i=1}^{N}w_i f(x_i)\ \approx\ \mathbb E_p[f(x)] }
$$

样本虽然来自 $q(x)$，但权重 $p(x)/q(x)$ 修正了不同区域的采样概率：$q$ 采多了的地方（$q>p$）权重小于 1，采少了的地方权重大于 1，最终估计逼近目标分布 $p(x)$ 下的真实期望。

推导成立需要一个条件：凡是 $p(x)f(x)\neq 0$ 的地方，都要有 $q(x)>0$。否则这部分区域永远采不到，估计会系统性地偏掉，而且样本再多也看不出来。

## 方差与提议分布的选择

$\hat\mu_{\text{IS}}$ 是无偏的，$\mathbb E_q[\hat\mu_{\text{IS}}]=\mu$，其中 $\mu=\mathbb E_p[f]$。单个样本的方差是

$$
\operatorname{Var}_q\!\big[w f\big]=\mathbb E_q\!\left[\frac{p^2f^2}{q^2}\right]-\mu^2=\int\frac{p(x)^2f(x)^2}{q(x)}\,dx-\mu^2
$$

$N$ 个样本的平均再除以 $N$。积分里 $q$ 在分母上：只要某处 $q$ 远小于 $pf$，这一项就很大。这就是"$p/q$ 在少数样本上很大，少数样本主导整个估计"的数学来源。

令方差最小的提议分布是

$$
q^*(x)=\frac{|f(x)|\,p(x)}{\int |f(x')|\,p(x')\,dx'}
$$

当 $f\ge 0$ 时，代入可得 $w f=\int fp\,dx=\mu$ 对每个样本都成立，方差为零。$q^*$ 里含有要求的 $\mu$ 本身，实际用不了，但它指明了方向：**$q$ 应该在 $|f|p$ 大的地方多采样**，形状越接近 $|f|p$ 越好，尾部不能比 $p$ 更薄。

实际中常用有效样本量（effective sample size）检查权重是否失衡：

$$
\text{ESS}=\frac{\left(\sum_i w_i\right)^2}{\sum_i w_i^2}
$$

权重全相等时 $\text{ESS}=N$；只有一个样本权重非零时 $\text{ESS}=1$。例如 10 个样本中 9 个权重为 1、1 个权重为 4，$\text{ESS}=13^2/25=6.76$，相当于只有不到 7 个独立样本。

## 例题：估计小概率事件

$X\sim\mathcal N(0,1)$，估计 $\mu=P(X>3)$，真值约 $1.35\times10^{-3}$。取 $f(x)=\mathbf 1\{x>3\}$，样本数 $N=10^4$。

??? example "直接采样与重要性采样的比较"

    **直接采样。** 从 $\mathcal N(0,1)$ 采样，数落在 $x>3$ 的比例。一万个样本里平均只有约 13.5 个命中，估计的相对标准差为

    $$
    \frac{\sqrt{\mu(1-\mu)/N}}{\mu}=\sqrt{\frac{1-\mu}{N\mu}}\approx 0.27
    $$

    也就是每次估计大约有 27% 的误差。

    **重要性采样。** 按 $q^*\propto \mathbf 1\{x>3\}\,p(x)$ 的提示，把采样分布挪到 3 附近，取 $q=\mathcal N(3,1)$。权重

    $$
    w(x)=\frac{p(x)}{q(x)}=\frac{e^{-x^2/2}}{e^{-(x-3)^2/2}}=e^{-3x+4.5}
    $$

    估计量为 $\hat\mu=\frac1N\sum_i \mathbf 1\{x_i>3\}\,e^{-3x_i+4.5}$，$x_i\sim\mathcal N(3,1)$。约一半样本落在 $x>3$，每个命中样本贡献一个很小的权重（$x=3$ 时 $w=e^{-4.5}\approx0.011$）。

    单样本二阶矩可以写成闭式：$\mathbb E_q[w^2f^2]=\mathbb E_p[wf]=e^{9}P(X>6)$，由此得相对标准差约 $0.018$。

    **结论。** 同样一万个样本，相对误差从约 27% 降到约 1.8%，方差缩小约 218 倍；直接采样要达到同样精度需要大约 218 万个样本。

    反过来，若取 $q=\mathcal N(-3,1)$，几乎采不到 $x>3$，偶尔采到一个时权重是 $e^{3x+4.5}$，极大。估计在绝大多数次数下接近 0，偶尔一次巨大，方差比直接采样还糟。

## 自归一化重要性采样

很多场景只知道 $p$ 的未归一化形式 $\tilde p(x)=Z\,p(x)$，常数 $Z$ 算不出来（例如贝叶斯后验、能量模型）。这时用 $\tilde w_i=\tilde p(x_i)/q(x_i)$，并用权重之和归一化：

$$
\hat\mu_{\text{SNIS}}=\frac{\sum_{i=1}^N \tilde w_i f(x_i)}{\sum_{i=1}^N \tilde w_i}
$$

$Z$ 在分子分母中约掉。这个估计量有偏（分母也是随机的），但 $N\to\infty$ 时收敛到 $\mu$；它的输出始终是 $f$ 值的加权平均，不会因为个别大权重跑到 $f$ 的取值范围之外，实践中往往比普通估计更稳。

| | 普通重要性采样 | 自归一化重要性采样 |
| --- | --- | --- |
| 需要 | 归一化的 $p$ | 只需 $\tilde p\propto p$ |
| 偏差 | 无偏 | 有偏，偏差为 $O(1/N)$ |
| 估计值范围 | 可能超出 $f$ 的取值范围 | 始终在 $f$ 的取值范围内 |

## 在 RL 中的应用

智能体（agent）根据状态 $s$ 选择动作 $a$。策略（policy）记为 $\pi(a|s)$，表示在状态 $s$ 下选择动作 $a$ 的概率。设有两个策略：

- $\pi(a|s)$：目标策略（target policy），即要评估或优化的策略。
- $\beta(a|s)$：行为策略（behavior policy），实际生成训练数据的策略。

训练数据由旧策略 $\beta$ 生成，现在要评估新策略 $\pi$。数据来自旧策略而目标是新策略，这正是"从 $q$ 采样、求 $p$ 下的期望"，权重为

$$
\boxed{ w(s,a)=\frac{\pi(a|s)}{\beta(a|s)} }
$$

它衡量新旧策略对同一个动作的概率分配差异。例如 $\pi(a|s)=0.8$，$\beta(a|s)=0.2$，则

$$
w(s,a)=\frac{0.8}{0.2}=4
$$

目标策略选这个动作的概率是行为策略的 4 倍，这个样本要算 4 份。反之，目标策略很少选、行为策略常选的动作，权重小于 1。成立条件对应为：凡是 $\pi(a|s)>0$ 的动作，$\beta(a|s)$ 也要大于 0，即行为策略要有足够的探索。

### 轨迹权重

对一整条轨迹 $\tau=(s_0,a_0,s_1,a_1,\dots,s_{T-1},a_{T-1})$，两种策略下的轨迹概率分别为

$$
p_\pi(\tau)=\rho(s_0)\prod_{t}\pi(a_t|s_t)\,P(s_{t+1}|s_t,a_t),\qquad
p_\beta(\tau)=\rho(s_0)\prod_{t}\beta(a_t|s_t)\,P(s_{t+1}|s_t,a_t)
$$

初始分布 $\rho$ 和环境转移概率 $P$ 在分子分母中相同、可以约掉，所以不需要知道环境模型，权重只是逐步比值的连乘：

$$
w(\tau)=\prod_{t=0}^{T-1}\frac{\pi(a_t|s_t)}{\beta(a_t|s_t)}
$$

步数一多，这个连乘的方差会非常大。即使每步比值只在 $1.1$ 和 $0.9$ 之间，20 步后也可能是 $1.1^{20}\approx6.7$ 或 $0.9^{20}\approx0.12$，个别轨迹的权重主导整个估计。

### 实际算法怎么控制方差

- **逐步加权（per-decision IS）**：第 $t$ 步的奖励只依赖前 $t$ 步的动作，所以只乘到第 $t$ 步的比值 $\prod_{k\le t}\pi(a_k|s_k)/\beta(a_k|s_k)$，比整条轨迹连乘方差小。
- **截断（truncated IS）**：把权重截到一个上限，$\min(w,c)$，用少量偏差换方差。Retrace、V-trace（IMPALA）都属于这一类；大模型 RL 中推理引擎与训练引擎的概率不一致时，也用截断的重要性权重修正，见 [从 SFT 到 Agentic RL](sft-to-agentic-rl.md)。
- **单步比值加裁剪**：PPO 只用单步比值 $r_t(\theta)=\pi_\theta(a_t|s_t)/\pi_{\theta_\text{old}}(a_t|s_t)$，忽略状态分布的差异，再用裁剪把比值限制在 $[1-\epsilon,1+\epsilon]$ 内。新旧策略只差一小步时这种近似误差小，见 [策略梯度与 PPO](ppo.md)。

重要性采样在 RL 中主要用于离策略评估（off-policy evaluation，用旧数据估计新策略的价值）和离策略学习（off-policy learning，用旧数据或其他策略的数据更新当前策略）。

## 公式速查

| 内容 | 公式 |
| --- | --- |
| 恒等式 | $\mathbb E_p[f]=\mathbb E_q[(p/q)f]$ |
| 估计量 | $\hat\mu=\frac1N\sum w_if(x_i)$，$w_i=p(x_i)/q(x_i)$ |
| 方差（单样本） | $\int p^2f^2/q\,dx-\mu^2$ |
| 最优提议分布 | $q^*\propto\lvert f\rvert p$ |
| 有效样本量 | $(\sum w_i)^2/\sum w_i^2$ |
| 自归一化 | $\sum \tilde w_if_i/\sum\tilde w_i$ |
| 策略比值 | $\pi(a\mid s)/\beta(a\mid s)$ |
| 轨迹权重 | $\prod_t\pi(a_t\mid s_t)/\beta(a_t\mid s_t)$ |
