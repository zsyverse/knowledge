---
date: 2026-11-04
description: 叠加（含受控源）、线性关系、戴维南/诺顿、含受控源的等效电阻、最大功率、作业 4-36，共 8 题。
tags:
  - 电路
  - 习题
---

# 习题：电路定理

对应知识点：[电路定理](../notes/circuit-theorems.md)

## 概念

### 1. 概念判断 :material-star::material-star-outline::material-star-outline:

判断下列说法是否正确：

1. 叠加定理可以用来直接计算电阻的功率。
2. 用叠加定理时，受控源也要像独立源一样"单独作用"、其余时间置零。
3. 含受控源的二端网络，其戴维南等效电阻可能为负。
4. 负载从戴维南等效电路获得最大功率时，传输效率为 $50\%$。
5. 任何线性含源二端网络都同时存在戴维南和诺顿两种等效电路。

??? success "答案"
    1 ✗　2 ✗　3 ✓　4 ✓　5 ✗

??? note "解析"
    1. 功率是电流（电压）的二次函数，$R(i'+i'')^2\neq Ri'^2+Ri''^2$，只能先叠加电流、电压再算功率。
    2. 受控源不是激励，它在每个分电路中都**保留**，控制量按该分电路重新计算。
    3. 受控源能向外输出能量，外加电源法算出的 $R_{eq}=u/i$ 可以为负。
    4. $R_L=R_{eq}$ 时 $R_{eq}$ 与 $R_L$ 中电流相同、电阻相同，各消耗一半。
    5. $R_{eq}=0$ 时只有戴维南形式（$I_{sc}$ 无穷大），$R_{eq}=\infty$ 时只有诺顿形式。

## 叠加定理与线性关系

### 2. 叠加求电流 :material-star::material-star-outline::material-star-outline:

用叠加定理求 $3\,\Omega$ 电阻中的电流 $I$ 及其功率，并说明为什么不能把两个分电路中的功率相加。

![叠加定理](../images/ex/t-super.svg){ .circuit }

??? success "答案"
    $I=2\,\mathrm A$，$P_{3\Omega}=12\,\mathrm W$（两分量功率之和只有 $6\,\mathrm W$）。

??? note "解析"
    **$12\,\mathrm V$ 单独作用**（$3\,\mathrm A$ 开路）：$b$ 点只剩 $2\,\Omega$、$4\,\Omega$ 串联，从 $a$ 到地为 $6\,\Omega$，与 $3\,\Omega$ 并联得 $2\,\Omega$：

    $$
    U_a'=12\times\frac{2}{6+2}=3\,\mathrm V,\qquad I'=\frac{3}{3}=1\,\mathrm A .
    $$

    **$3\,\mathrm A$ 单独作用**（$12\,\mathrm V$ 短路）：从 $b$ 看，$4\,\Omega$ 与"$2\,\Omega$ 串 $(6\parallel3)=2\,\Omega$"即 $4\,\Omega$ 并联，电流各半，$1.5\,\mathrm A$ 流向 $a$；再在 $6\,\Omega$、$3\,\Omega$ 间分流：

    $$
    I''=1.5\times\frac{6}{6+3}=1\,\mathrm A .
    $$

    **叠加**：$I=I'+I''=2\,\mathrm A$，$P=3\times2^2=12\,\mathrm W$。若把功率相加，$3\times1^2+3\times1^2=6\,\mathrm W$，漏掉了交叉项 $2RI'I''=6\,\mathrm W$。

### 3. 含受控源的叠加 :material-star::material-star::material-star-outline:

图中受控电压源 $2i$（上正下负）受 $2\,\Omega$ 电阻中的电流 $i$ 控制。用叠加定理求 $U$ 和 $i$。

![含 CCVS 的叠加](../images/ex/t-super-ccvs.svg){ .circuit }

??? success "答案"
    $U=10.5\,\mathrm V$，$i=-0.25\,\mathrm A$。

??? note "解析"
    受控源在两个分电路中都保留。

    **$10\,\mathrm V$ 单独作用**（$3\,\mathrm A$ 开路）：单回路，竖支路电流也是 $i'$，

    $$
    U'=4i'+2i'=6i',\qquad 10=2i'+6i'\ \Rightarrow\ i'=1.25\,\mathrm A,\ U'=7.5\,\mathrm V .
    $$

    **$3\,\mathrm A$ 单独作用**（$10\,\mathrm V$ 短路）：$i''=\dfrac{0-U''}{2}$，竖支路向下的电流为 $i''+3$，

    $$
    U''=4(i''+3)+2i''=6i''+12,\qquad U''=-2i''\ \Rightarrow\ i''=-1.5\,\mathrm A,\ U''=3\,\mathrm V .
    $$

    **叠加**：$U=7.5+3=10.5\,\mathrm V$，$i=1.25-1.5=-0.25\,\mathrm A$。

    **检验**（直接列方程）：$i=\dfrac{10-U}{2}$，$U=4(i+3)+2i$ ⇒ $10-2i=6i+12$，$i=-0.25\,\mathrm A$，$U=10.5\,\mathrm V$ ✓

    !!! warning "易错"
        第二个分电路里控制量 $i''$ 不是零——受控源的电压 $2i''=-3\,\mathrm V$ 照样存在。把受控源置零会得到 $U''=12\times\frac{2}{6}$ 之类的错误结果。

### 4. 由测量数据确定线性关系 :material-star::material-star::material-star-outline:

（作业 4-31 改编）$N$ 为线性电阻网络（可含线性受控源），外接电压源 $U_S$ 和电流源 $I_S$，$U$ 为电流源两端电压。

1. 若 $N$ 内**不含**独立源，测得：$U_S=2\,\mathrm V$、$I_S=1\,\mathrm A$ 时 $U=4\,\mathrm V$；$U_S=1\,\mathrm V$、$I_S=2\,\mathrm A$ 时 $U=5\,\mathrm V$。求 $U_S=3\,\mathrm V$、$I_S=3\,\mathrm A$ 时的 $U$；若 $U_S=4\,\mathrm V$，$I_S$ 为多少时 $U=0$？
2. 若 $N$ 内**含**独立源，测得 $U_S=0$、$I_S=0$ 时 $U=1\,\mathrm V$；$U_S=2\,\mathrm V$、$I_S=1\,\mathrm A$ 时 $U=5\,\mathrm V$；$U_S=1\,\mathrm V$、$I_S=2\,\mathrm A$ 时 $U=6\,\mathrm V$。求 $U_S=3\,\mathrm V$、$I_S=3\,\mathrm A$ 时的 $U$。

![线性网络](../images/ex/t-linear.svg){ .circuit }

??? success "答案"
    1. $U=9\,\mathrm V$；$I_S=-2\,\mathrm A$（即电流源反向、大小 $2\,\mathrm A$）。
    2. $U=10\,\mathrm V$。

??? note "解析"
    1. 无内部独立源时，由叠加与齐次性 $U=aU_S+bI_S$：

        $$
        2a+b=4,\quad a+2b=5\ \Rightarrow\ a=1,\ b=2\,\Omega .
        $$

        $U=3+2\times3=9\,\mathrm V$；$4+2I_S=0\Rightarrow I_S=-2\,\mathrm A$。
    2. 内部独立源相当于第三个激励，贡献常数项：$U=aU_S+bI_S+c$。第一组数据给出 $c=1\,\mathrm V$，代入另两组得 $2a+b=4$、$a+2b=5$，同样 $a=1$、$b=2$：

        $$
        U=3+6+1=10\,\mathrm V .
        $$

    !!! warning "易错"
        受控源**不是**激励，不单独占一项；它的作用已经包含在系数 $a$、$b$ 里。含内部独立源时，$U$ 与外加激励不再成正比，必须保留常数项 $c$。

## 戴维南与诺顿等效

### 5. 戴维南等效与负载功率 :material-star::material-star::material-star-outline:

求 $a$、$b$ 左侧网络的戴维南等效电路；$R_L=3\,\Omega$ 时 $R_L$ 中电流是多少？$R_L$ 为何值时获得最大功率，最大功率是多少？

![戴维南](../images/ex/t-thevenin.svg){ .circuit }

??? success "答案"
    $U_{oc}=36\,\mathrm V$（$a$ 正），$R_{eq}=9\,\Omega$；$R_L=3\,\Omega$ 时 $I=3\,\mathrm A$；$R_L=9\,\Omega$ 时 $P_{\max}=36\,\mathrm W$。

??? note "解析"
    **开路电压**：移去 $R_L$，$2\,\mathrm A$ 只能经 $6\,\Omega$ 由 $a$ 流向 $c$。节点 $c$（以下边线为参考）：

    $$
    \frac{V_c-24}{4}+\frac{V_c}{12}=2\ \Rightarrow\ V_c=24\,\mathrm V,\qquad U_{oc}=V_c+6\times2=36\,\mathrm V .
    $$

    **等效电阻**：电压源短路、电流源开路，$R_{eq}=6+4\parallel12=6+3=9\,\Omega$。

    **接负载**：$I=\dfrac{36}{9+3}=3\,\mathrm A$；最大功率 $R_L=R_{eq}=9\,\Omega$，$P_{\max}=\dfrac{36^2}{4\times9}=36\,\mathrm W$。

### 6. 诺顿等效 :material-star::material-star::material-star-outline:

求 $a$、$b$ 端口的诺顿等效电路（$I_{sc}$ 取从 $a$ 经短路线流向 $b$），并求接 $R_L=4\,\Omega$ 时 $R_L$ 中的电流。

![诺顿](../images/ex/t-norton.svg){ .circuit }

??? success "答案"
    $I_{sc}=2\,\mathrm A$，$R_{eq}=4\,\Omega$（等价于 $U_{oc}=8\,\mathrm V$ 串 $4\,\Omega$）；$R_L=4\,\Omega$ 时电流 $1\,\mathrm A$。

??? note "解析"
    **短路电流**：$a$、$b$ 短接后 $2\,\Omega$ 下端接地，节点 $c$：

    $$
    \frac{V_c-18}{3}+\frac{V_c}{6}+\frac{V_c}{2}=0\ \Rightarrow\ V_c=6\,\mathrm V .
    $$

    $2\,\Omega$ 中流向 $a$ 的电流 $6/2=3\,\mathrm A$，其中 $1\,\mathrm A$ 被电流源从 $a$ 拉到 $b$，其余经短路线：$I_{sc}=3-1=2\,\mathrm A$。

    **等效电阻**：$R_{eq}=2+3\parallel6=4\,\Omega$。

    **检验**（开路电压）：$\dfrac{V_c-18}{3}+\dfrac{V_c}{6}+1=0\Rightarrow V_c=10\,\mathrm V$，$U_{oc}=V_c-2\times1=8\,\mathrm V=R_{eq}I_{sc}$ ✓

    **接 $R_L$**：$I_{sc}$ 在 $R_{eq}$、$R_L$ 间分流，$I_L=2\times\dfrac{4}{4+4}=1\,\mathrm A$。

### 7. 含受控源的戴维南等效与最大功率 :material-star::material-star::material-star:

受控电压源 $2i_1$ 的 $+$ 端朝向 $a$，$i_1$ 为左侧 $4\,\Omega$ 中的电流。求 $a$、$b$ 端戴维南等效电路，以及在 $a$、$b$ 间接入可调电阻 $R_L$ 时的最大功率。

![含 CCVS 的戴维南](../images/ex/t-ccvs-thevenin.svg){ .circuit }

??? success "答案"
    $U_{oc}=9\,\mathrm V$（$a$ 正），$I_{sc}=9\,\mathrm A$，$R_{eq}=1\,\Omega$；$R_L=1\,\Omega$ 时 $P_{\max}=20.25\,\mathrm W$。

??? note "解析"
    **开路电压**：受控源支路无电流，$i_1=\dfrac{12}{4+4}=1.5\,\mathrm A$，$V_c=6\,\mathrm V$，

    $$
    U_{oc}=V_c+2i_1=6+3=9\,\mathrm V .
    $$

    **短路电流**：$V_a=0\Rightarrow V_c=-2i_1$；又 $i_1=\dfrac{12-V_c}{4}$，解得 $V_c=-12\,\mathrm V$，$i_1=6\,\mathrm A$。节点 $c$：

    $$
    I_{sc}=i_1-\frac{V_c}{4}=6+3=9\,\mathrm A,\qquad R_{eq}=\frac{U_{oc}}{I_{sc}}=1\,\Omega .
    $$

    **校验**（外加电源法）：$12\,\mathrm V$ 短路，端口加 $u$、流入 $a$ 的电流为 $i$。$i_1=-\dfrac{V_c}{4}$，$V_c=u-2i_1=u+\dfrac{V_c}{2}\Rightarrow V_c=2u$，$i_1=-\dfrac u2$；节点 $c$：$i+i_1=\dfrac{V_c}{4}\Rightarrow i=u$，$R_{eq}=1\,\Omega$ ✓

    **最大功率**：$R_L=1\,\Omega$，$P_{\max}=\dfrac{9^2}{4\times1}=20.25\,\mathrm W$。

    !!! warning "易错"
        把受控源当导线、只看电阻会得到 $4\parallel4=2\,\Omega$——受控源"抵消"了一部分电阻，必须用外加电源法或 $U_{oc}/I_{sc}$。

### 8. 由开关两种状态求有源网络的戴维南等效 :material-star::material-star::material-star:

（作业 4-36）$A$ 为线性有源二端网络，$U_{S1}=10\,\mathrm V$，$R_1=2\,\Omega$，$R_2=4\,\Omega$。开关 $S$ 断开时 $I_2=0$；$S$ 闭合时 $I_3=8\,\mathrm A$。求 $A$ 的戴维南等效电路。

![作业 4-36](../images/ex/t-4-36.svg){ .circuit }

??? success "答案"
    $U_{oc}=\dfrac{20}{3}\approx6.67\,\mathrm V$（$a$ 正），$R_{eq}=\dfrac{20}{9}\approx2.22\,\Omega$。

??? note "解析"
    1. **$S$ 断开，$I_2=0$**：左侧电路不向 $A$ 送电流，$A$ 的端口电流为零，相当于开路，它的端口电压就是 $U_{oc}$；此时左侧 $R_1$、$R_2$ 构成分压器：

        $$
        U_{oc}=U_{ab}=10\times\frac{4}{2+4}=\frac{20}{3}\,\mathrm V .
        $$

    2. **$S$ 闭合**：$a$、$b$ 短接，$R_2$ 被短路，左侧经 $R_1$ 送入短路线 $10/2=5\,\mathrm A$。$I_3=8\,\mathrm A$ 中其余部分由 $A$ 提供，这就是 $A$ 的短路电流：

        $$
        I_{sc}=8-5=3\,\mathrm A .
        $$

    3. $R_{eq}=\dfrac{U_{oc}}{I_{sc}}=\dfrac{20/3}{3}=\dfrac{20}{9}\,\Omega$。

    !!! warning "易错"
        $I_3=8\,\mathrm A$ 是左侧电路和 $A$ 共同送入开关的电流，不能直接当作 $A$ 的短路电流。
