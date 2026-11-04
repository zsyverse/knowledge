---
date: 2026-11-04
description: 初始值、一阶 RC/RL 三要素、电荷与磁链守恒、受控源与级联电路（第七章作业）、二阶 RLC，共 10 题。
tags:
  - 电路
  - 习题
---

# 习题：动态电路的时域分析

对应知识点：[动态电路的时域分析](../notes/dynamic-circuits.md)

以下各题中，"换路前已达稳态"指换路前电路处于直流稳态（电感短路、电容开路）；所有结果均对 $t\ge0_+$ 成立。

## 初始值

### 1. 概念判断 :material-star::material-star-outline::material-star-outline:

判断下列说法是否正确：

1. 换路瞬间电容电流不能突变。
2. 同一个一阶电路中，各支路电压、电流的时间常数都相同。
3. 求时间常数 $\tau$ 时，应使用换路前电路从储能元件看进去的等效电阻。
4. 换路后若出现只由电容（和理想电压源）构成的回路，电容电压可能在换路瞬间跳变。
5. RLC 串联零输入电路中，$R$ 越大，振荡越剧烈。

??? success "答案"
    1 ✗　2 ✓　3 ✗　4 ✓　5 ✗

??? note "解析"
    1. 连续的只是 $u_C$ 和 $i_L$；电容**电流**、电感**电压**、电阻上的量都可以跳变。
    2. 一阶电路只有一个固有频率 $s=-1/\tau$，任何响应都按同一个 $e^{-t/\tau}$ 衰减。
    3. 应使用**换路后**的电路（独立源置零）。
    4. 此时 KVL 强迫电容电压之和等于某个定值，换路定则的前提"电容电流有限"不再成立，要用电荷守恒。
    5. $R$ 越大衰减越快；$R\ge2\sqrt{L/C}$ 时根本不振荡。

### 2. 开关切换后的各初始值 :material-star::material-star-outline::material-star-outline:

（作业 7-3 改编）$t<0$ 时开关 $S$ 在位置 1，电路已达稳态；$t=0$ 时 $S$ 由 1 扳向 2。求 $i(0_+)$、$u_C(0_+)$、$u_L(0_+)$ 和 $i_C(0_+)$。

![作业 7-3](../images/ex/d-73.svg){ .circuit }

??? success "答案"
    $i(0_+)=4\,\mathrm A$，$u_C(0_+)=20\,\mathrm V$，$u_L(0_+)=-20\,\mathrm V$，$i_C(0_+)=0$。

??? note "解析"
    1. **$0_-$**：电感短路、电容开路，$R_1$ 与 $R_2$ 串联在 $24\,\mathrm V$ 上：

        $$
        i(0_-)=\frac{24}{1+5}=4\,\mathrm A,\qquad u_C(0_-)=5\times4=20\,\mathrm V .
        $$

    2. **换路定则**：$i(0_+)=4\,\mathrm A$，$u_C(0_+)=20\,\mathrm V$。
    3. **$0_+$ 等效电路**：电感换成 $4\,\mathrm A$ 电流源、电容换成 $20\,\mathrm V$ 电压源，开关动端经触点 2 接到下边线（电位 $0$）。
        - $u_L$ 左正右负：$u_L(0_+)=0-u_C(0_+)=-20\,\mathrm V$；
        - $R_2$ 中电流 $20/5=4\,\mathrm A$，$i_C(0_+)=i(0_+)-4=0$。

    !!! warning "易错"
        不能拿换路后的稳态电路算 $0_+$ 值——那只能得到 $t\to\infty$ 时的终值（这里 $i(\infty)=0$、$u_C(\infty)=0$）。$u_L$ 从 $0_-$ 的 $0$ 跳到了 $-20\,\mathrm V$，正是"电感电压可以跳变"。

## 一阶电路的三要素法

### 3. 开关断开后的 RC 电路 :material-star::material-star::material-star-outline:

换路前电路已达稳态，$t=0$ 时 $S$ 断开。求 $u_C(t)$ 与 $i_C(t)$。

![RC 电路](../images/ex/d-rc.svg){ .circuit }

??? success "答案"
    $u_C(t)=18-12e^{-t/4}\ \mathrm V$，$i_C(t)=1.5e^{-t/4}\ \mathrm A$。

??? note "解析"
    1. **初始值**：$S$ 闭合时电容开路，$R_3$ 无电流，$u_C=u_a=18\times\dfrac{3}{6+3}=6\,\mathrm V$，故 $u_C(0_+)=6\,\mathrm V$。
    2. **稳态值**：$S$ 断开后电路中只剩一条串联通路，电容开路时无电流，$u_C(\infty)=18\,\mathrm V$。
    3. **时间常数**：电压源短路，从电容看入 $R_{eq}=R_1+R_3=8\,\Omega$（$R_2$ 已断开），$\tau=8\times0.5=4\,\mathrm s$。
    4. 三要素：

        $$
        u_C(t)=18+(6-18)e^{-t/4}=18-12e^{-t/4}\ \mathrm V,\qquad
        i_C=C\frac{\mathrm du_C}{\mathrm dt}=0.5\times3e^{-t/4}=1.5e^{-t/4}\ \mathrm A .
        $$

    **校验**：$i_C(0_+)=\dfrac{18-6}{6+2}=1.5\,\mathrm A$ ✓（$i_C(0_-)=0$，跳变）。

### 4. 开关闭合后的 RL 电路 :material-star::material-star::material-star-outline:

换路前电路已达稳态，$t=0$ 时 $S$ 闭合。求 $i_L(t)$ 及节点 $a$ 的电位 $u_a(t)$。

![RL 电路](../images/ex/d-rl.svg){ .circuit }

??? success "答案"
    $i_L(t)=4+0.5e^{-1.5t}\ \mathrm A$，$u_a(t)=4-e^{-1.5t}\ \mathrm V$。

??? note "解析"
    1. **初始值**：$S$ 断开时电感短路，$6\,\mathrm A$ 在 $R_1=3\,\Omega$ 与 $R_2=1\,\Omega$ 之间分流：

        $$
        i_L(0_+)=i_L(0_-)=6\times\frac{3}{3+1}=4.5\,\mathrm A .
        $$

    2. **稳态值**：$S$ 闭合后 $R_1\parallel R_3=2\,\Omega$，$i_L(\infty)=6\times\dfrac{2}{2+1}=4\,\mathrm A$。
    3. **时间常数**：电流源开路，从电感看入 $R_{eq}=R_2+R_1\parallel R_3=1+2=3\,\Omega$，$\tau=\dfrac{2}{3}\,\mathrm s$。
    4. $i_L(t)=4+(4.5-4)e^{-1.5t}=4+0.5e^{-1.5t}\ \mathrm A$。
    5. $u_a$ 有两种求法：
        - 用 VCR：$u_a=R_2i_L+L\dfrac{\mathrm di_L}{\mathrm dt}=4+0.5e^{-1.5t}+2\times(-0.75)e^{-1.5t}=4-e^{-1.5t}\ \mathrm V$；
        - 用三要素：$0_+$ 时 $a$ 点 KCL $6=\dfrac{u_a}{3}+\dfrac{u_a}{6}+4.5\Rightarrow u_a(0_+)=3\,\mathrm V$，$u_a(\infty)=R_2i_L(\infty)=4\,\mathrm V$，于是 $u_a=4+(3-4)e^{-1.5t}$ ✓

    !!! warning "易错"
        $u_a(0_-)=3\times(6-4.5)=4.5\,\mathrm V$，而 $u_a(0_+)=3\,\mathrm V$——非储能量会跳变，必须在 $0_+$ 电路里重新求。

## 换路定则失效：磁链与电荷守恒

### 5. 两电感并联 :material-star::material-star::material-star:

（作业 7-4）$I_S=6\,\mathrm A$，$L_1=1\,\mathrm H$，$L_2=2\,\mathrm H$，$R=1\,\Omega$，已知 $i_1(0_-)=1\,\mathrm A$，$i_2(0_-)=2\,\mathrm A$，$t=0$ 时 $S$ 闭合。求 $i_2(0_+)$、$i_2(\infty)$ 及 $i_2(t)$。

![作业 7-4](../images/ex/d-74.svg){ .circuit }

??? success "答案"
    $i_2(0_+)=2\,\mathrm A$，$i_2(\infty)=3\,\mathrm A$，$i_2(t)=3-e^{-1.5t}\ \mathrm A$（同时 $i_1(t)=3-2e^{-1.5t}\ \mathrm A$）。

??? note "解析"
    1. **初始值**：换路后两电感与 $R$ 并联、并联电压有限，电感电流连续：$i_2(0_+)=2\,\mathrm A$。
    2. **终值需要两个条件**。稳态时并联电压为零，$R$ 中无电流，$i_1(\infty)+i_2(\infty)=6$——一个方程两个未知量，还缺一个。
    3. **磁链关系**：两电感始终承受同一电压，$L_1\dfrac{\mathrm di_1}{\mathrm dt}=L_2\dfrac{\mathrm di_2}{\mathrm dt}$，积分得

        $$
        L_1i_1-L_2i_2=\text{常数}=1\times1-2\times2=-3 .
        $$

        与 $i_1+i_2=6$ 联立：$i_1(\infty)=i_2(\infty)=3\,\mathrm A$。
    4. **全过程**：总电流 $i=i_1+i_2$ 流过等效电感 $L_1\parallel L_2=\tfrac23\,\mathrm H$，$\tau=\dfrac{2/3}{1}=\dfrac23\,\mathrm s$，$i=6+(3-6)e^{-1.5t}$。由 $i_1=2i_2-3$ 得 $i=3i_2-3$，

        $$
        i_2(t)=\frac{i+3}{3}=3-e^{-1.5t}\ \mathrm A,\qquad i_1(t)=3-2e^{-1.5t}\ \mathrm A .
        $$

    !!! warning "易错"
        有初始储能时，不能按"电感反比分流"直接写 $i_2(\infty)=6\times\dfrac{L_1}{L_1+L_2}=2\,\mathrm A$——那只对零初始状态成立。

### 6. 两电容中点突然相连 :material-star::material-star::material-star:

（作业 7-5 改编）$C_1=1\,\mathrm F$，$C_2=2\,\mathrm F$，$R_1=1\,\Omega$，$R_2=2\,\Omega$，$U_S=9\,\mathrm V$。$S$ 断开已久，$t=0$ 时闭合。（1）求 $u_{C1}(0_+)$、$u_{C2}(0_+)$；（2）求 $t>0$ 时的 $u_{C2}(t)$。

![作业 7-5](../images/ex/d-75.svg){ .circuit }

??? success "答案"
    （1）$u_{C1}(0_+)=3\,\mathrm V$，$u_{C2}(0_+)=6\,\mathrm V$；（2）$u_{C2}(t)=6\,\mathrm V$（恒定，没有过渡过程）。

??? note "解析"
    1. **$0_-$**：$S$ 断开，两条支路中电容都开路、无电流，各自承受全部电源电压：$u_{C1}(0_-)=u_{C2}(0_-)=9\,\mathrm V$。
    2. **为什么不能用换路定则**：$S$ 闭合后 $U_S$、$C_1$、$C_2$ 构成纯电容（加电压源）回路，KVL 要求 $u_{C1}+u_{C2}=9$，而 $9+9\neq9$，电容电压必须跳变（瞬间有冲激电流）。
    3. **电荷守恒**：中点处相连的是 $C_1$ 的下极板（电荷 $-C_1u_{C1}$）和 $C_2$ 的上极板（电荷 $+C_2u_{C2}$）。冲激电流只在电容和电压源之间流动，电阻在无限短时间内搬运不了有限电荷，所以该节点总电荷不变：

        $$
        -C_1u_{C1}(0_+)+C_2u_{C2}(0_+)=-1\times9+2\times9=9 .
        $$

        与 $u_{C1}(0_+)+u_{C2}(0_+)=9$ 联立：$u_{C2}(0_+)=6\,\mathrm V$，$u_{C1}(0_+)=3\,\mathrm V$。
    4. **$t>0$**：中点电位 $u_{C2}$ 满足 KCL（上方 $R_1\parallel C_1$ 流入 = 下方 $R_2\parallel C_2$ 流出）

        $$
        \frac{9-u_{C2}}{1}+1\cdot\frac{\mathrm d(9-u_{C2})}{\mathrm dt}=\frac{u_{C2}}{2}+2\frac{\mathrm du_{C2}}{\mathrm dt}
        \ \Rightarrow\ 3\frac{\mathrm du_{C2}}{\mathrm dt}+1.5u_{C2}=9 .
        $$

        稳态 $u_{C2}(\infty)=6\,\mathrm V$，恰好等于初值，所以 $u_{C2}(t)\equiv6\,\mathrm V$，$u_{C1}(t)\equiv3\,\mathrm V$——跳变之后直接就是新的稳态（这是本题参数的巧合，一般情况下跳变后仍有指数过渡过程，时间常数 $\tau=\dfrac{C_1+C_2}{1/R_1+1/R_2}=2\,\mathrm s$）。

## 含受控源与级联的电路

### 7. 受控源参数突变 :material-star::material-star::material-star:

（作业 7-10）$I_S=1\,\mathrm A$，受控电压源 $\beta i$ 中 $\beta=0.5$，电路已达稳态；$t=0$ 时 $\beta$ 突然变为 $1.5$。求 $u(t)$。

![作业 7-10](../images/ex/d-710.svg){ .circuit }

??? success "答案"
    $u(t)=\dfrac23-\dfrac4{15}e^{-3t}\ \mathrm V$。

??? note "解析"
    1. **列方程**（$\beta$ 先保留为参数）。右节点：$i=\dfrac u1+1\cdot\dfrac{\mathrm du}{\mathrm dt}=u+u'$。左上节点电位 $u+i$（经上方 $1\,\Omega$），左竖支路电流 $\dfrac{(u+i)-\beta i}{1}$。左上节点 KCL：

        $$
        1=(u+i-\beta i)+i=u+(2-\beta)i=u+(2-\beta)(u+u')
        $$

        $$
        \Rightarrow\ (2-\beta)u'+(3-\beta)u=1 .
        $$

    2. **初始值**（$\beta=0.5$ 的稳态，$u'=0$）：$u(0_-)=\dfrac1{2.5}=0.4\,\mathrm V$，电容电压连续，$u(0_+)=0.4\,\mathrm V$。
    3. **$\beta=1.5$ 后**：$0.5u'+1.5u=1$，即 $u'+3u=2$。$u(\infty)=\dfrac23\,\mathrm V$，$\tau=\dfrac13\,\mathrm s$。

        $$
        u(t)=\frac23+\Big(\frac25-\frac23\Big)e^{-3t}=\frac23-\frac4{15}e^{-3t}\ \mathrm V .
        $$

    !!! tip "另一种看法"
        $\tau$ 也可用外加电源法：$\beta=1.5$ 时从电容看入的等效电阻 $R_{eq}=\dfrac{2-\beta}{3-\beta}=\dfrac13\,\Omega$，$\tau=R_{eq}C=\dfrac13\,\mathrm s$。受控源"改变参数"本身也是一次换路。

### 8. CCVS 驱动的两级 RC :material-star::material-star::material-star:

（作业 7-12）$R_1=20\,\Omega$，$R_2=10\,\Omega$，$r=20\,\Omega$，$C_1=C_2=0.1\,\mathrm F$，$u_S=12\,\mathrm V$（直流）。$S$ 闭合已久，$t=0$ 时打开。求开关两端电压 $u_0(t)$ 与 $u_C(t)$。

![作业 7-12](../images/ex/d-712.svg){ .circuit }

??? success "答案"
    $u_0(t)=12\big(1-e^{-t/2}\big)\ \mathrm V$，$u_C(t)=12e^{-t/2}-6e^{-t}\ \mathrm V$。

??? note "解析"
    1. **$0_-$**：两电容开路，$C_1$ 与受控源经闭合的 $S$ 并联，$u_{C1}=ri_1$；回路 $12=R_1i_1+ri_1=40i_1$，$i_1=0.3\,\mathrm A$，$u_{C1}(0_-)=6\,\mathrm V$；$R_2$ 无电流，$u_C(0_-)=6\,\mathrm V$。
    2. **左侧**（$S$ 打开后是独立的 RC 电路）：$\tau_1=R_1C_1=2\,\mathrm s$，

        $$
        u_{C1}=12-6e^{-t/2}\ \mathrm V,\qquad i_1=\frac{12-u_{C1}}{20}=0.3e^{-t/2}\ \mathrm A .
        $$

    3. **开关电压**：开关右端电位就是受控源电压 $ri_1=6e^{-t/2}$，

        $$
        u_0=u_{C1}-ri_1=12-12e^{-t/2}\ \mathrm V .
        $$

    4. **右侧**：受控源电压 $6e^{-t/2}$ 经 $R_2$ 给 $C_2$ 充电，$R_2C_2=1\,\mathrm s$：

        $$
        \frac{\mathrm du_C}{\mathrm dt}+u_C=6e^{-t/2},\qquad u_C(0_+)=6 .
        $$

        激励是指数函数，**三要素法不适用**。设特解 $Ae^{-t/2}$：$-\tfrac A2+A=6\Rightarrow A=12$；通解 $u_C=12e^{-t/2}+Be^{-t}$，由 $u_C(0_+)=6$ 得 $B=-6$。

    **校验**：$u_0(0_+)=0$——打开瞬间左端 $u_{C1}(0_+)=6\,\mathrm V$，右端 $ri_1(0_+)=20\times\dfrac{12-6}{20}=6\,\mathrm V$，两端仍等电位；$u_C(\infty)=0$，因为受控源电压随 $i_1$ 衰减到零。

    !!! note "关于教材答案"
        有资料给出的 $u_C(t)$ 系数与本题参数不符；上式满足初值 $6\,\mathrm V$ 和右侧的微分方程。

### 9. CCCS 驱动的 RL 支路 :material-star::material-star::material-star:

（作业 7-28）$R=10\,\Omega$，$U_S=12\,\mathrm V$，$C=0.01\,\mathrm F$，$L=0.2\,\mathrm H$，受控电流源 $\beta i$ 中 $\beta=\tfrac13$（方向向下）。$S$ 闭合已久，$t=0$ 时打开。求开关两端电压 $u_k(t)$ 与电感电流 $i_L(t)$。（原题把开关电压记作 $u_S$，这里改记 $u_k$，以免与电源 $U_S$ 混淆。）

![作业 7-28](../images/ex/d-728.svg){ .circuit }

??? success "答案"
    $i_L(t)=0.78e^{-50t}-0.3e^{-10t}\ \mathrm A$，$u_k(t)=12-5.4e^{-10t}+7.8e^{-50t}\ \mathrm V$。

??? note "解析"
    1. **$0_-$**（电感短路、电容开路，$S$ 闭合）：$i$ 流到中间节点后，$\beta i$ 经受控源向下，其余 $(1-\beta)i$ 经右侧 $R$ 流入电感（与电感并联的 $R$ 被短路）：

        $$
        i=\frac{12-u_C}{10},\qquad u_C=10(1-\beta)i=\frac{20}{3}i\ \Rightarrow\ i=0.72\,\mathrm A,\ u_C(0_-)=4.8\,\mathrm V,\ i_L(0_-)=0.48\,\mathrm A .
        $$

    2. **左侧**（$S$ 打开后为独立 RC，$\tau=RC=0.1\,\mathrm s$）：

        $$
        u_C=12-7.2e^{-10t}\ \mathrm V,\qquad i=\frac{12-u_C}{10}=0.72e^{-10t}\ \mathrm A .
        $$

    3. **右侧**：开关右端节点只连受控源和右侧 $R$，所以流过该 $R$（向右）的电流为 $-\beta i=-0.24e^{-10t}$，它流入"$R\parallel L$"：

        $$
        i_L+\frac{L}{R}\frac{\mathrm di_L}{\mathrm dt}=-0.24e^{-10t}\ \Rightarrow\ 0.02\frac{\mathrm di_L}{\mathrm dt}+i_L=-0.24e^{-10t} .
        $$

        特解 $Ae^{-10t}$：$A(1-0.2)=-0.24\Rightarrow A=-0.3$；固有项 $Be^{-50t}$（$\tau=L/R=0.02\,\mathrm s$），由 $i_L(0_+)=0.48$ 得 $B=0.78$。
    4. **开关电压**：开关右端电位 $=u_L+R\cdot(-\beta i)$，其中 $u_L=L\dfrac{\mathrm di_L}{\mathrm dt}=0.6e^{-10t}-7.8e^{-50t}$，$R\beta i=2.4e^{-10t}$：

        $$
        v_B=-1.8e^{-10t}-7.8e^{-50t},\qquad u_k=u_C-v_B=12-5.4e^{-10t}+7.8e^{-50t}\ \mathrm V .
        $$

    **校验**：$u_k(0_+)=12-5.4+7.8=14.4\,\mathrm V$，而 $u_k(0_-)=0$。打开瞬间右侧 $R$ 的电流被受控源强制从 $(1-\beta)i=0.48\,\mathrm A$ 变为 $-\beta i=-0.24\,\mathrm A$，开关右端电位从 $4.8\,\mathrm V$ 跳到 $-9.6\,\mathrm V$，所以开关电压跳变；$i_L(0_+)=0.78-0.3=0.48\,\mathrm A$ 保持连续 ✓

## 二阶电路

### 10. RLC 放电 :material-star::material-star::material-star-outline:

$u_C(0_-)=10\,\mathrm V$，电感无初始电流，$t=0$ 时 $S$ 闭合。判断响应类型，并求 $u_C(t)$ 和 $i(t)$。

![RLC 电路](../images/ex/d-rlc.svg){ .circuit }

??? success "答案"
    欠阻尼。$u_C(t)=e^{-6t}\big(10\cos8t+7.5\sin8t\big)=12.5e^{-6t}\sin(8t+53.13^\circ)\ \mathrm V$，$i(t)=2.5e^{-6t}\sin8t\ \mathrm A$。

??? note "解析"
    1. **判断**：临界电阻 $2\sqrt{L/C}=2\sqrt{0.5/0.02}=10\,\Omega$，$R=6\,\Omega<10\,\Omega$，欠阻尼。
    2. **特征根**：$\alpha=\dfrac{R}{2L}=6$，$\omega_0^2=\dfrac1{LC}=100$，$\omega_d=\sqrt{100-36}=8\,\mathrm{rad/s}$，$s=-6\pm j8$。
    3. **定系数**：$u_C=e^{-6t}(A\cos8t+B\sin8t)$。$u_C(0_+)=10\Rightarrow A=10$；$i(0_+)=0$ 且 $i=-C\dfrac{\mathrm du_C}{\mathrm dt}$（$i$ 从 $+$ 极板流出），故 $u_C'(0_+)=0$：$-6A+8B=0\Rightarrow B=7.5$。
    4. 合成：$\sqrt{10^2+7.5^2}=12.5$，$\arctan\dfrac{10}{7.5}=53.13^\circ$。

        $$
        i=-C\frac{\mathrm du_C}{\mathrm dt}=-0.02\times e^{-6t}\big[(-6\times10+8\times7.5)\cos8t+(-6\times7.5-8\times10)\sin8t\big]=2.5e^{-6t}\sin8t\ \mathrm A .
        $$

    **校验**：$i(0)=0$ ✓；$t>0$ 刚开始 $i>0$，电容经 $R$、$L$ 放电 ✓。
