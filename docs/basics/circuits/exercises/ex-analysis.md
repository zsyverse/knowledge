---
date: 2026-11-04
description: 独立方程数、支路电流法、超网孔、节点法标准形式、超节点、含受控源的节点法、理想二极管、指定树的回路电流法，共 8 题。
tags:
  - 电路
  - 习题
---

# 习题：电路的一般分析方法

对应知识点：[电路的一般分析方法](../notes/analysis-methods.md)

## 独立方程数

### 1. 方程数与方法选择 :material-star::material-star-outline::material-star-outline:

某平面电路有 $n=4$ 个节点、$b=7$ 条支路。

1. 独立的 KCL、KVL 方程各有几个？
2. 用支路电流法、网孔电流法、节点电压法分别要解几个联立方程？
3. 若其中一条支路是**只属于一个网孔**（在外侧）的理想电流源，网孔法实际要解几个方程？

??? success "答案"
    1. KCL $3$ 个，KVL $4$ 个；
    2. 支路电流法 $7$ 个，网孔法 $4$ 个，节点法 $3$ 个；
    3. $3$ 个。

??? note "解析"
    1. 独立 KCL 数 $n-1=3$，独立 KVL 数 $b-n+1=7-4+1=4$。
    2. 支路电流法以 $b=7$ 个支路电流为未知量；网孔数 $=b-n+1=4$；节点法以 $n-1=3$ 个节点电压为未知量。
    3. 该网孔的网孔电流直接等于（或等于负的）电流源值，不必再列它的 KVL，只剩 $4-1=3$ 个方程。

## 支路电流法与网孔法

### 2. 支路电流法 :material-star::material-star-outline::material-star-outline:

（作业 4-12）用支路电流法求 $I_1$、$I_3$，并求各电源的功率。

![支路电流法](../images/ex/a-branch.svg){ .circuit }

??? success "答案"
    $I_1=3\,\mathrm A$，$I_3=0$；$U_{S1}$ 发出 $30\,\mathrm W$，$I_{S2}$ 发出 $60\,\mathrm W$，$U_{S3}$ 功率为 $0$。

??? note "解析"
    以下边线为参考点，上节点电位记为 $V$。

    1. **KCL**（上节点）：$I_1+I_3=I_{S2}=3$。
    2. **KVL**：左、右两条支路给出同一个 $V$。左支路自下而上：经 $U_{S1}$ 升 $10\,\mathrm V$，顺着 $I_1$ 经 $R_1$ 降 $10I_1$；右支路自下而上：顺着 $I_3$ 经 $R_3$ 降 $20I_3$，再经 $U_{S3}$ 从 $+$ 到 $-$ 降 $20\,\mathrm V$：

        $$
        V=10-10I_1=-20I_3-20 .
        $$

    3. 代入 $I_1=3-I_3$：$10-30+10I_3=-20I_3-20\Rightarrow 30I_3=0$，所以 $I_3=0$，$I_1=3\,\mathrm A$，$V=-20\,\mathrm V$。
    4. **功率**：
        - $U_{S1}$：$I_1$ 从其 $+$ 端流出，发出 $10\times3=30\,\mathrm W$；
        - $I_{S2}$：上端电位 $-20\,\mathrm V$，电流从上端流入（关联），吸收 $(-20)\times3=-60\,\mathrm W$，即**发出** $60\,\mathrm W$；
        - $U_{S3}$：电流为零，功率为零。

    **校验**：只有 $R_1$ 耗能 $10\times3^2=90\,\mathrm W=30+60$ ✓

### 3. 公共支路上的电流源：超网孔 :material-star::material-star::material-star-outline:

两网孔电流 $I_1$、$I_2$ 均取顺时针，电流源两端电压为 $U$（上正下负）。求 $I_1$、$I_2$、$U$，并检验功率平衡。

![超网孔](../images/ex/a-supermesh.svg){ .circuit }

??? success "答案"
    $I_1=1\,\mathrm A$，$I_2=3\,\mathrm A$，$U=24\,\mathrm V$。

??? note "解析"
    电流源在两个网孔的**公共支路**上，它的电压未知，不能直接写进单个网孔的 KVL。

    1. **电流约束**：顺时针的 $I_2$ 在中间支路向上、$I_1$ 向下，所以

        $$
        I_2-I_1=2 .
        $$

    2. **超网孔**（绕开电流源，沿外圈顺时针）：

        $$
        28=4I_1+2I_2+6I_2 .
        $$

    3. 代入 $I_2=I_1+2$：$28=12I_1+16\Rightarrow I_1=1\,\mathrm A$，$I_2=3\,\mathrm A$。
    4. 求 $U$：网孔 1 的 KVL，$28=4I_1+U\Rightarrow U=24\,\mathrm V$（网孔 2 校验：$U=(2+6)\times3=24$ ✓）。

    **功率**：电压源发出 $28\times1=28\,\mathrm W$；电流源 $2\,\mathrm A$ 从其 $+$ 端流出，发出 $24\times2=48\,\mathrm W$；电阻吸收 $4\times1^2+2\times3^2+6\times3^2=76\,\mathrm W=28+48$ ✓

    !!! tip "另一种写法"
        把 $U$ 设为未知量，两个网孔分别写 $4I_1+U=28$、$8I_2-U=0$，再加约束 $I_2-I_1=2$，三式联立结果相同。超网孔只是把前两式相加消去了 $U$。

## 节点电压法

### 4. 标准形式与"电流源串电阻" :material-star::material-star::material-star-outline:

以图中接地点为参考，（1）写出节点 ①、② 的标准形式节点电压方程；（2）求 $U_1$、$U_2$；（3）求 $2\,\mathrm A$ 电流源发出的功率。

![节点法](../images/ex/a-node.svg){ .circuit }

??? success "答案"
    （1）$\big(\tfrac12+\tfrac14\big)U_1-\tfrac14U_2=2$，$-\tfrac14U_1+\big(\tfrac14+\tfrac14+\tfrac14\big)U_2=\tfrac{24}{4}$；
    （2）$U_1=6\,\mathrm V$，$U_2=10\,\mathrm V$；
    （3）$32\,\mathrm W$。

??? note "解析"
    **（1）** 与电流源串联的 $5\,\Omega$ **不计入**自电导（那条支路的电流就是 $2\,\mathrm A$）；$24\,\mathrm V$ 串 $4\,\Omega$ 支路贡献电导 $\tfrac14$ 和注入电流 $\tfrac{24}{4}=6\,\mathrm A$：

    $$
    \begin{cases}
    0.75\,U_1-0.25\,U_2=2\\
    -0.25\,U_1+0.75\,U_2=6
    \end{cases}
    $$

    **（2）** 由第一式 $U_2=3U_1-8$，代入第二式 $-0.25U_1+2.25U_1-6=6\Rightarrow U_1=6\,\mathrm V$，$U_2=10\,\mathrm V$。

    **（3）** 电流源端电压（上正）要把 $5\,\Omega$ 上的压降算进去：

    $$
    U_{I_S}=U_1+2\times5=16\,\mathrm V,\qquad P_{\text{发}}=16\times2=32\,\mathrm W .
    $$

    **校验**：$24\,\mathrm V$ 源输出 $\tfrac{24-10}{4}=3.5\,\mathrm A$，发出 $84\,\mathrm W$；电阻吸收 $\tfrac{6^2}{2}+\tfrac{4^2}{4}+\tfrac{10^2}{4}+3.5^2\times4+2^2\times5=18+4+25+49+20=116\,\mathrm W=32+84$ ✓

    !!! warning "易错"
        $5\,\Omega$ 不影响任何节点电压，但会改变电流源自身的电压和功率——不能用 $U_1\times2=12\,\mathrm W$。

### 5. 浮置电压源：超节点 :material-star::material-star::material-star-outline:

$8\,\mathrm V$ 电压源跨接在 $a$、$b$ 之间（$b$ 正），两端都不接地。求 $U_a$、$U_b$，以及 $8\,\mathrm V$ 电压源中的电流和它的功率。

![超节点](../images/ex/a-supernode.svg){ .circuit }

??? success "答案"
    $U_a=12\,\mathrm V$，$U_b=20\,\mathrm V$；$8\,\mathrm V$ 源中电流 $3\,\mathrm A$（由 $a$ 流向 $b$），发出 $24\,\mathrm W$。

??? note "解析"
    $c$ 点被 $24\,\mathrm V$ 电压源钉住：$U_c=24\,\mathrm V$。把 $a$、$b$ 和 $8\,\mathrm V$ 源圈成超节点：

    $$
    \frac{U_a}{4}+\frac{U_b}{4}+\frac{U_b-24}{2}=6,\qquad U_b-U_a=8 .
    $$

    代入 $U_b=U_a+8$：$\tfrac{U_a}{4}+\tfrac{U_a+8}{4}+\tfrac{U_a-16}{2}=6\Rightarrow U_a-6=6$，$U_a=12\,\mathrm V$，$U_b=20\,\mathrm V$。

    电压源电流回到单个节点 $a$ 求：$6=\tfrac{12}{4}+i_{ab}\Rightarrow i_{ab}=3\,\mathrm A$（由 $a$ 经电源流向 $b$）。它从 $-$ 端流入、$+$ 端流出，发出 $8\times3=24\,\mathrm W$。

    **校验**：节点 $b$：$3=\tfrac{20}{4}+\tfrac{20-24}{2}=5-2$ ✓；电源发出 $6\times12+24+24\times2=144\,\mathrm W$，电阻吸收 $\tfrac{12^2}{4}+\tfrac{20^2}{4}+\tfrac{4^2}{2}=36+100+8=144\,\mathrm W$ ✓

### 6. 含受控源的节点法 :material-star::material-star::material-star-outline:

受控电流源 $gu_x$ 由地注入节点 ②，$g=1\,\mathrm S$，$u_x$ 为 ①、② 间 $2\,\Omega$ 电阻的电压（① 正）。求 $U_1$、$U_2$ 及受控源发出的功率。

![含 VCCS 的节点法](../images/ex/a-vccs.svg){ .circuit }

??? success "答案"
    $U_1=8\,\mathrm V$，$U_2=6\,\mathrm V$；受控源发出 $12\,\mathrm W$。

??? note "解析"
    1. 受控源先当独立源写进方程：

        $$
        \begin{cases}
        \big(\tfrac14+\tfrac12\big)U_1-\tfrac12U_2=3\\
        -\tfrac12U_1+\big(\tfrac12+\tfrac12\big)U_2=gu_x
        \end{cases}
        $$

    2. 补控制量方程 $u_x=U_1-U_2$，代入第二式并移项：$-1.5U_1+2U_2=0$，即 $U_2=0.75U_1$。（系数矩阵不再对称，这是正常的。）
    3. 代入第一式：$0.75U_1-0.375U_1=3\Rightarrow U_1=8\,\mathrm V$，$U_2=6\,\mathrm V$，$u_x=2\,\mathrm V$。
    4. 受控源电流 $gu_x=2\,\mathrm A$ 从其 $+$ 端（②）流出，发出 $6\times2=12\,\mathrm W$。

    **校验**：独立源发出 $8\times3=24\,\mathrm W$；电阻吸收 $\tfrac{8^2}{4}+\tfrac{2^2}{2}+\tfrac{6^2}{2}=16+2+18=36\,\mathrm W=24+12$ ✓

## 理想二极管

### 7. 两只二极管的"或"电路 :material-star::material-star::material-star-outline:

$D_1$、$D_2$ 为理想二极管。（1）$U_2=2\,\mathrm V$ 时求 $U_o$、$I_{D1}$、$I_{D2}$；（2）$U_2=5\,\mathrm V$ 时再求；（3）$U_2$ 在什么范围内 $D_2$ 截止（$D_1$ 导通）？

![二极管电路](../images/ex/a-diode.svg){ .circuit }

??? success "答案"
    （1）$U_o=4\,\mathrm V$，$I_{D1}=2\,\mathrm{mA}$，$I_{D2}=0$；
    （2）$U_o=4.4\,\mathrm V$，$I_{D1}=1.6\,\mathrm{mA}$，$I_{D2}=0.6\,\mathrm{mA}$；
    （3）$U_2\le4\,\mathrm V$。

??? note "解析"
    （电阻用 $\mathrm{k\Omega}$、电流用 $\mathrm{mA}$。）

    **（1）** 两管同时导通会要求 $U_o$ 同时等于两支路给出的值——先试"$D_1$ 通、$D_2$ 断"：$6\,\mathrm V$ 经 $1\,\mathrm k\Omega$、$2\,\mathrm k\Omega$ 分压，

    $$
    I_{D1}=\frac{6}{1+2}=2\,\mathrm{mA}>0,\qquad U_o=2\times2=4\,\mathrm V .
    $$

    验证 $D_2$：其支路无电流，阳极电位为 $U_2=2\,\mathrm V$，阴极为 $U_o=4\,\mathrm V$，$u_{D2}=2-4=-2\,\mathrm V\le0$，截止 ✓

    **（2）** 若仍假设 $D_2$ 截止，则 $u_{D2}=5-4=1\,\mathrm V>0$，矛盾。改设两管都导通，节点 $o$：

    $$
    \frac{6-U_o}{1}+\frac{5-U_o}{1}=\frac{U_o}{2}\ \Rightarrow\ 2.5U_o=11,\ U_o=4.4\,\mathrm V,
    $$

    $I_{D1}=6-4.4=1.6\,\mathrm{mA}>0$，$I_{D2}=5-4.4=0.6\,\mathrm{mA}>0$，假设成立 ✓

    **（3）** $D_1$ 导通、$D_2$ 截止时 $U_o=4\,\mathrm V$，$D_2$ 截止要求 $U_2-U_o\le0$，即 $U_2\le4\,\mathrm V$（等号为临界）。

    !!! warning "易错"
        理想二极管导通时压降为零，不要加 $0.7\,\mathrm V$；判断截止看**两端电压**，不能只看"哪边电源大"——这里 $U_2=5\,\mathrm V<6\,\mathrm V$，$D_2$ 仍然导通。

## 回路电流法

### 8. 按指定的树列回路电流方程 :material-star::material-star::material-star:

（作业 4-17）$R_1=R_5=2\,\Omega$，$R_2=R_4=1\,\Omega$，$R_3=R_6=3\,\Omega$，$R_7=4\,\Omega$，$I_{S4}=6\,\mathrm A$，$I_{S5}=1\,\mathrm A$。以 $R_1\sim R_5$ 五条支路为树，用回路电流法求连支电流 $I_6$、$I_7$（方向如图：$I_6$ 向右流过 $R_6$，$I_7$ 向右流过 $R_7$ 后经右侧导线向上）。

![指定树](../images/ex/a-tree.svg){ .circuit }

??? success "答案"
    $I_6=1\,\mathrm A$，$I_7=0.5\,\mathrm A$。

??? note "解析"
    记左侧竖线为节点 $L$、右侧中间节点为 $Q$。树 $R_1\sim R_5$ 连通全部 6 个节点；连支为 $R_6$、$R_7$、$I_{S4}$、$I_{S5}$，每条连支与树支构成一个基本回路，回路电流就是该连支电流：

    | 连支 | 基本回路（沿连支电流方向） | 回路电流 |
    | --- | --- | --- |
    | $R_6$ | $R_6\to R_5\to Q\to R_2\to R_3\to R_1\to L\to R_4$ | $I_6$ |
    | $R_7$ | $L\to R_7\to Q\to R_2\to R_3\to R_1\to L$ | $I_7$ |
    | $I_{S4}$ | $I_{S4}$ 向上 $\to R_4$（向左）$\to L\to R_1$（向右） | $6\,\mathrm A$（已知） |
    | $I_{S5}$ | $I_{S5}$ 向上 $\to R_5$（向右）$\to Q\to R_2$（向左） | $1\,\mathrm A$（已知） |

    只需对 $I_6$、$I_7$ 两个回路列 KVL（电路中没有电压源，右边为零）：

    - 回路 6 自电阻 $R_6+R_5+R_2+R_3+R_1+R_4=12$；与回路 7 共用 $R_2$、$R_3$、$R_1$ 且同向，互电阻 $+6$；与 $I_{S4}$ 回路共用 $R_4$、$R_1$ 且反向，$-3$；与 $I_{S5}$ 回路共用 $R_5$、$R_2$ 且同向，$+3$：

        $$
        12I_6+6I_7-3\times6+3\times1=0\ \Rightarrow\ 12I_6+6I_7=15 .
        $$

    - 回路 7 自电阻 $R_7+R_2+R_3+R_1=10$；与回路 6 互电阻 $+6$；与 $I_{S4}$ 回路共用 $R_1$（反向）$-2$；与 $I_{S5}$ 回路共用 $R_2$（同向）$+1$：

        $$
        6I_6+10I_7-2\times6+1\times1=0\ \Rightarrow\ 6I_6+10I_7=11 .
        $$

    第二式乘 2 减第一式：$14I_7=7$，$I_7=0.5\,\mathrm A$，$I_6=\dfrac{15-3}{12}=1\,\mathrm A$。

    **校验**：各树支电流（向右为正）$R_1:4.5$、$R_2:-2.5$、$R_3:-1.5$、$R_4:-5$、$R_5:2\ (\mathrm A)$，例如 $I_{S4}$ 上端节点 $-5+6=1=I_6$ ✓，$I_{S5}$ 上端节点 $1+1=2=I_{R5}$ ✓（已用全电路节点法独立核对）。

    !!! tip "为什么这样选树"
        让每个电流源都是连支，它所在回路的电流就是已知值，未知回路电流只剩 $b-n+1-2=2$ 个——比网孔法（要处理两个公共支路上的电流源）省事得多。
