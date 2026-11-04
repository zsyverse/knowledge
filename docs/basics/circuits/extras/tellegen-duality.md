---
date: 2026-11-04
description: 特勒根定理的两种形式及证明，用它处理"同一电阻网络两次测量"类问题；互易定理的三种形式（统一端口参考方向下的符号）及与二端口参数的关系；对偶原理与平面电路的对偶电路。
tags:
  - 电路
  - 拓展
---

# 特勒根定理、互易定理与对偶原理

!!! abstract "TL;DR"
    - **特勒根定理**：同一个有向图上，任意一组满足 KCL 的支路电流与任意一组满足 KVL 的支路电压，有 $\sum_k u_k i_k=0$。两组量来自同一电路就是**功率守恒**（形式一），来自拓扑相同的两个电路就是"似功率"守恒（形式二）。
    - **互易定理**：线性电阻网络 $N_R$ 的两个端口，"在 1 激励、2 处响应"与"在 2 激励、1 处响应"的比值相同，等价于二端口参数 $Z_{12}=Z_{21}$。
    - **对偶原理**：把一个成立的关系式里的对偶量全部互换（$u\leftrightarrow i$、$R\leftrightarrow G$、$L\leftrightarrow C$、串联 ↔ 并联、网孔 ↔ 节点……），得到的关系式也成立。

[电路定理](../notes/circuit-theorems.md) 已经介绍了互易定理的一种形式，本页把它和特勒根定理放在一起系统化。

## 1. 特勒根定理

设电路有 $b$ 条支路，每条支路的 $u_k$、$i_k$ 取**关联参考方向**。

=== "形式一（功率守恒）"

    $$
    \sum_{k=1}^{b}u_ki_k=0 .
    $$

    任一时刻全部支路吸收的功率之和为零。[功率守恒自检](../notes/problem-patterns.md) 和"复功率守恒"都是它的特例。

=== "形式二（似功率守恒）"

    两个电路 $N$、$\hat N$ 的**有向图相同**（元件可以完全不同），则

    $$
    \sum_{k=1}^{b}u_k\hat i_k=0,\qquad \sum_{k=1}^{b}\hat u_ki_k=0 .
    $$

    $u_k\hat i_k$ 不是任何实际功率，只是数学上的"似功率"。

**证明**（一行）：KVL 给出 $\mathbf u=\mathbf A^{\mathsf T}\mathbf u_n$，KCL 给出 $\mathbf A\hat{\mathbf i}=\mathbf 0$（$\mathbf A$ 是 [关联矩阵](matrix-state.md)），所以

$$
\mathbf u^{\mathsf T}\hat{\mathbf i}=\mathbf u_n^{\mathsf T}\mathbf A\hat{\mathbf i}=0 .
$$

证明只用了 KCL、KVL，**与元件性质无关**：线性、非线性、时变电路都适用。

### 两次测量问题

对只含线性电阻的网络 $N_R$（引出两个端口，端口电流都从 $+$ 端**流入** $N_R$），分别做两次实验 (a)、(b)。在形式二中把端口支路和内部支路分开写：端口支路作为外接支路，其关联方向下的电流是 $-I$，所以

$$
-U_1\hat I_1-U_2\hat I_2+\sum_{\text{内部}}u_k\hat i_k=0,\qquad
-\hat U_1I_1-\hat U_2I_2+\sum_{\text{内部}}\hat u_ki_k=0 .
$$

内部都是电阻：$u_k\hat i_k=R_ki_k\hat i_k=\hat u_ki_k$，两个求和相等，于是

$$
\boxed{U_1\hat I_1+U_2\hat I_2=\hat U_1I_1+\hat U_2I_2}
$$

已知一次实验的全部端口量和另一次的端接情况，就能求出另一次的未知量，而**不必知道 $N_R$ 内部结构**。

??? example "例：两次测量求未知电流"
    $N_R$ 仅由线性电阻构成。图 (a) 中测得 $I_1=3\,\mathrm A$，$I_2=-2\,\mathrm A$；求图 (b) 中的 $\hat I_1$ 与 $\hat U_1$。

    === "(a)"

        ![实验 a](../images/extras/td-tel-a.svg){ .circuit }

    === "(b)"

        ![实验 b](../images/extras/td-tel-b.svg){ .circuit }

    已知：(a) $U_1=10\,\mathrm V$，$U_2=0$（短路），$I_1=3\,\mathrm A$，$I_2=-2\,\mathrm A$；(b) $\hat U_2=20\,\mathrm V$，$\hat U_1=-2\hat I_1$（$2\,\Omega$ 电阻上，$\hat I_1$ 流入 $N_R$ 就是从电阻下端流向上端）。

    代入 $U_1\hat I_1+U_2\hat I_2=\hat U_1I_1+\hat U_2I_2$：

    $$
    10\hat I_1+0=(-2\hat I_1)\times3+20\times(-2)\ \Rightarrow\ 16\hat I_1=-40,\quad \hat I_1=-2.5\,\mathrm A,\quad \hat U_1=5\,\mathrm V .
    $$

    $U_2=0$ 让未知的 $\hat I_2$ 自动消失，这是此类题设计的关键。

    **验证**：若 $N_R$ 是 $2\,\Omega$、$4\,\Omega$（并臂）、$2\,\Omega$ 的 T 形网络（$\mathbf Z=\begin{bmatrix}6&4\\4&6\end{bmatrix}\Omega$），(a) 中正好 $I_1=3$、$I_2=-2$；(b) 中直接解得 $\hat I_1=-2.5\,\mathrm A$ ✓

## 2. 互易定理

线性、时不变、**只含电阻（以及 L、C、耦合电感）、不含受控源和独立源**的网络称为互易网络。按本页统一的参考方向（端口电压上 $+$ 下 $-$，端口电流流入网络），互易定理有三种形式：

| | 实验 (a) | 实验 (b) | 结论 |
| --- | --- | --- | --- |
| 形式一 | 端口 1 加电压源 $u_s$，端口 2 **短路**，测 $I_2$ | 端口 2 加电压源 $\hat u_s$，端口 1 **短路**，测 $\hat I_1$ | $\dfrac{I_2}{u_s}=\dfrac{\hat I_1}{\hat u_s}$ |
| 形式二 | 端口 1 加电流源 $i_s$，端口 2 **开路**，测 $U_2$ | 端口 2 加电流源 $\hat i_s$，端口 1 **开路**，测 $\hat U_1$ | $\dfrac{U_2}{i_s}=\dfrac{\hat U_1}{\hat i_s}$ |
| 形式三 | 端口 1 加电流源 $i_s$，端口 2 **短路**，测 $I_2$ | 端口 2 加电压源 $\hat u_s$，端口 1 **开路**，测 $\hat U_1$ | $\dfrac{\hat U_1}{\hat u_s}=-\dfrac{I_2}{i_s}$ |

三种形式都是上面方框等式的直接推论（把各自的开路、短路条件代进去）。从二端口的角度看，形式一就是 $Y_{12}=Y_{21}$，形式二就是 $Z_{12}=Z_{21}$，形式三就是 $H_{12}=-H_{21}$——见 [二端口网络](two-port.md)。

!!! note "形式三的负号"
    很多教材说形式三"数值相等"，是因为它把短路电流取为**从端口 2 流出网络**（沿短路线流向下端）的方向，即 $-I_2$。在端口电流统一流入网络的约定下，负号必须保留。做题时先看图上的方向，再决定有没有负号。

!!! warning "适用条件"
    - 只适用于单一激励；激励与响应必须是"电压源—短路电流"或"电流源—开路电压"的配对（形式三是混合配对）；
    - 网络内含受控源时一般**不**互易（见二端口页的例子：$Z_{12}=4\ne Z_{21}=6$）。

## 3. 对偶原理

把电路中的一组概念换成另一组，方程的形式不变：

| | | | |
| --- | --- | --- | --- |
| 电压 $u$ | 电流 $i$ | KVL | KCL |
| 电阻 $R$ | 电导 $G$ | 串联 | 并联 |
| 电感 $L$ | 电容 $C$ | 网孔电流 | 节点电压 |
| 电压源 | 电流源 | 短路 | 开路 |
| 阻抗 $Z$ | 导纳 $Y$ | 戴维南等效 | 诺顿等效 |
| VCVS | CCCS | CCVS | VCCS |

例如：串联 $R_{eq}=\sum R_k$、分压 $u_k=\dfrac{R_k}{R_{eq}}u$ ↔ 并联 $G_{eq}=\sum G_k$、分流 $i_k=\dfrac{G_k}{G_{eq}}i$；RC 电路 $\tau=RC$ ↔ RL 电路 $\tau=GL=L/R$；RLC 串联 ↔ GCL 并联（见 [二阶电路](second-order.md#2-gcl-并联与对偶)）。

### 平面电路的对偶电路

**平面电路**（能画在平面上而支路不交叉）的网孔方程，可以"翻译"成另一个电路的节点方程：

1. 每个网孔内放一个节点，网孔外放参考节点；
2. 原电路中两个网孔共用的元件，换成对偶元件接在对应两个节点之间；只属于一个网孔的（外边界上的）元件，换成对偶元件接在该节点与参考节点之间；
3. 网孔电流顺时针时，沿顺时针方向使电位升高的电压源，对偶为流入对应节点的电流源。

??? example "例：两网孔电路与它的对偶电路"
    === "原电路（网孔法）"

        ![两网孔电路](../images/extras/td-mesh.svg){ .circuit }

        $$
        \begin{cases}(2+4)I_a-4I_b=10\\-4I_a+(4+1+3)I_b=0\end{cases}
        \quad\Rightarrow\quad I_a=2.5\,\mathrm A,\ I_b=1.25\,\mathrm A .
        $$

    === "对偶电路（节点法）"

        ![对偶电路](../images/extras/td-node.svg){ .circuit }

        $$
        \begin{cases}(2+4)U_a-4U_b=10\\-4U_a+(4+1+3)U_b=0\end{cases}
        \quad\Rightarrow\quad U_a=2.5\,\mathrm V,\ U_b=1.25\,\mathrm V .
        $$

    两组方程的数字完全相同：网孔 $a$ 中的 $10\,\mathrm V$ 电压源和 $R_1$ 变成节点 $a$ 与地之间的 $10\,\mathrm A$ 电流源和 $G_1$；两网孔共用的 $R_3$ 变成节点 $a$、$b$ 之间的 $G_3$；网孔 $b$ 中**串联**的 $R_2$、$R_4$ 变成节点 $b$ 对地**并联**的 $G_2$、$G_4$。

!!! tip "对偶不等于等效"
    对偶电路的**方程形式**相同、数值可以相同，但它与原电路**不等效**——一个解出的是电流，另一个解出的是电压。对偶的用处是"一个结论顶两个用"：推出串联电路的结论，并联电路的对应结论不用再推。

## 练习

### 1. 概念判断 :material-star::material-star-outline::material-star-outline:

判断下列说法是否正确：

1. 特勒根定理只适用于线性电路。
2. 特勒根定理形式二要求两个电路的元件参数相同。
3. 含受控源的线性网络一般不满足互易定理。
4. 对偶电路与原电路等效。
5. 电阻串联的分压公式与电导并联的分流公式互为对偶。

??? success "答案"
    1 ✗　2 ✗　3 ✓　4 ✗　5 ✓

??? note "解析"
    1. 证明只用了 KCL、KVL，对任何集总电路都成立。
    2. 只要求**有向图相同**（支路编号与方向一致），元件可以完全不同。
    3. 受控源使 $Z_{12}\ne Z_{21}$。
    4. 对偶是方程形式的对应，不是端口特性的等效。
    5. $u_k=\dfrac{R_k}{\sum R}u$ ↔ $i_k=\dfrac{G_k}{\sum G}i$。

### 2. 两次测量 :material-star::material-star::material-star-outline:

$N_R$ 仅由线性电阻构成。图 (a) 中端口 2 开路，测得 $I_1=2\,\mathrm A$、$U_2=4\,\mathrm V$；图 (b) 中端口 1 短路、端口 2 接 $3\,\mathrm A$ 电流源。求图 (b) 中的 $\hat I_1$。

=== "(a)"

    ![实验 a](../images/extras/td-x2-a.svg){ .circuit }

=== "(b)"

    ![实验 b](../images/extras/td-x2-b.svg){ .circuit }

??? success "答案"
    $\hat I_1=-1.2\,\mathrm A$（即 $1.2\,\mathrm A$ 从端口 1 的上端子流出，经短路线回到下端子）。

??? note "解析"
    (a)：$U_1=10$，$I_1=2$，$U_2=4$，$I_2=0$；(b)：$\hat U_1=0$，$\hat I_2=3$。代入

    $$
    U_1\hat I_1+U_2\hat I_2=\hat U_1I_1+\hat U_2I_2:\qquad 10\hat I_1+4\times3=0\times2+\hat U_2\times0,
    $$

    $\hat I_1=-1.2\,\mathrm A$。(b) 中本有两个未知量 $\hat I_1$、$\hat U_2$，正是 $I_2=0$ 让 $\hat U_2$ 从等式中消失。

    **验证**：取 $\mathbf Z=\begin{bmatrix}5&2\\2&6\end{bmatrix}\Omega$ 的网络，(a) 中 $I_1=10/5=2$、$U_2=2\times2=4$ 与题设相符；(b) 中 $0=5\hat I_1+2\times3$，$\hat I_1=-1.2\,\mathrm A$ ✓

### 3. 互易 + 叠加 :material-star::material-star::material-star-outline:

互易网络 $N_R$：端口 1 加 $12\,\mathrm V$ 电压源、端口 2 短路时，测得 $I_1=4\,\mathrm A$，$I_2=-1.5\,\mathrm A$（端口电流均流入网络）。（1）端口 2 加 $6\,\mathrm V$ 电压源、端口 1 短路，求 $\hat I_1$；（2）两个端口同时分别加 $12\,\mathrm V$、$6\,\mathrm V$ 电压源，求 $I_1$。

??? success "答案"
    （1）$\hat I_1=-0.75\,\mathrm A$；（2）$I_1=3.25\,\mathrm A$。

??? note "解析"
    1. 互易定理形式一：$\dfrac{\hat I_1}{6}=\dfrac{I_2}{12}\Rightarrow\hat I_1=\dfrac{6}{12}\times(-1.5)=-0.75\,\mathrm A$。
    2. 叠加：端口 1 的电流 = 仅 $12\,\mathrm V$ 作用时的 $4\,\mathrm A$ + 仅 $6\,\mathrm V$ 作用时的 $-0.75\,\mathrm A$ = $3.25\,\mathrm A$。

    用 Y 参数看：$Y_{11}=\dfrac4{12}=\dfrac13\,\mathrm S$，$Y_{21}=\dfrac{-1.5}{12}=-\dfrac18\,\mathrm S=Y_{12}$，$I_1=Y_{11}\times12+Y_{12}\times6=4-0.75=3.25\,\mathrm A$ ✓。（若要求 $I_2$，还需要 $Y_{22}$，题目条件不够。）

### 4. 写出对偶电路 :material-star::material-star-outline::material-star-outline:

RLC 串联电路：$R=3\,\Omega$，$L=2\,\mathrm H$，$C=0.5\,\mathrm F$，由电压源 $u_s$ 激励，以回路电流 $i$ 为变量。（1）写出它的对偶电路及参数；（2）写出两者的方程；（3）比较两者的谐振角频率和衰减系数 $\alpha$。

??? success "答案"
    （1）GCL 并联：$G=3\,\mathrm S$，$C'=2\,\mathrm F$，$L'=0.5\,\mathrm H$，由电流源 $i_s$ 激励，以节点电压 $u$ 为变量；（2）见解析；（3）都是 $\omega_0=1\,\mathrm{rad/s}$，$\alpha=0.75\,\mathrm s^{-1}$。

??? note "解析"
    1. 串联 → 并联，$R\to G$、$L\to C'$、$C\to L'$、$u_s\to i_s$，数值不变。
    2. 方程：

        $$
        Ri+L\frac{\mathrm di}{\mathrm dt}+\frac1C\int i\,\mathrm dt=u_s\quad\longleftrightarrow\quad Gu+C'\frac{\mathrm du}{\mathrm dt}+\frac1{L'}\int u\,\mathrm dt=i_s ,
        $$

        即 $3i+2\dfrac{\mathrm di}{\mathrm dt}+2\int i\,\mathrm dt=u_s$ 与 $3u+2\dfrac{\mathrm du}{\mathrm dt}+2\int u\,\mathrm dt=i_s$，形式、系数完全相同。
    3. $\omega_0=\dfrac{1}{\sqrt{LC}}=\dfrac1{\sqrt{2\times0.5}}=1\,\mathrm{rad/s}$，对偶电路 $\dfrac{1}{\sqrt{L'C'}}$ 相同；$\alpha=\dfrac{R}{2L}=0.75$，对偶电路 $\alpha=\dfrac{G}{2C'}=0.75$。
