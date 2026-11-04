---
date: 2026-11-04
description: 同名端与耦合方程、顺接反接测互感、T 形去耦、含互感的回路方程、反映阻抗、理想变压器的匹配与方向陷阱，共 8 题。
tags:
  - 电路
  - 习题
---

# 习题：互感与理想变压器

对应知识点：[互感与理想变压器](../notes/coupled-inductors.md)。相量采用 sin 约定、有效值。

## 同名端与耦合方程

### 1. 概念判断 :material-star::material-star-outline::material-star-outline:

判断下列说法是否正确：

1. 空心变压器的反映阻抗 $\dfrac{(\omega M)^2}{Z_{22}}$ 与同名端的位置无关。
2. 耦合系数 $k$ 可以大于 1。
3. T 形去耦等效电路中出现的 $-M$ 是一个真实存在的元件。
4. 两线圈顺接串联（电流都从同名端流入）时，等效电感为 $L_1+L_2+2M$。
5. 理想变压器既不储能也不耗能。

??? success "答案"
    1 ✓　2 ✗　3 ✗　4 ✓　5 ✓

??? note "解析"
    1. 改变同名端只改变 $M$ 前的符号，反映阻抗里是 $(\pm\omega M)^2$，符号消失。
    2. $k=\dfrac{M}{\sqrt{L_1L_2}}\le1$，否则储能 $\tfrac12L_1i_1^2+\tfrac12L_2i_2^2\pm Mi_1i_2$ 可以为负。
    3. $-M$ 只是数学等效，单独拿出来不能实现；去耦后的整体端口特性才与原电路相同。
    4. 磁通相助，$L=L_1+L_2+2M$；反接为 $L_1+L_2-2M$。
    5. $u_1i_1+u_2i_2=0$（两电流都流入同名端）：任何时刻吸收的总功率为零。

### 2. 写出耦合电感的伏安关系 :material-star::material-star-outline::material-star-outline:

图中 $L_1$ 的同名端在上，$L_2$ 的同名端在下；$i_1$、$i_2$ 都从各自线圈的上端流入，$u_1$、$u_2$ 都是上正下负。写出 $u_1$、$u_2$ 的时域表达式和相量形式。

![耦合方程](../images/ex/m-eq.svg){ .circuit }

??? success "答案"
    $$
    u_1=L_1\frac{\mathrm di_1}{\mathrm dt}-M\frac{\mathrm di_2}{\mathrm dt},\qquad
    u_2=-M\frac{\mathrm di_1}{\mathrm dt}+L_2\frac{\mathrm di_2}{\mathrm dt}
    $$

    $$
    \dot U_1=j\omega L_1\dot I_1-j\omega M\dot I_2,\qquad \dot U_2=-j\omega M\dot I_1+j\omega L_2\dot I_2
    $$

??? note "解析"
    - **自感项**：两线圈各自的 $u$、$i$ 都是关联方向（电流从 $+$ 端流入），自感项都取 $+$。
    - **$u_1$ 中的互感项**：$i_2$ 从 $L_2$ 的**上端**（非同名端）流入，$u_1$ 的 $+$ 在 $L_1$ 的**上端**（同名端），二者不是同名端 → 取 $-$。
    - **$u_2$ 中的互感项**：$i_1$ 从 $L_1$ 的同名端流入，$u_2$ 的 $+$ 在 $L_2$ 的非同名端 → 取 $-$。

    **另一种想法**：把 $i_2$ 改写成"从 $L_2$ 同名端流入的电流" $-i_2$，就回到两电流都入同名端的标准形式：$u_1=L_1\dfrac{\mathrm di_1}{\mathrm dt}+M\dfrac{\mathrm d(-i_2)}{\mathrm dt}$。$u_2$ 的 $+$ 在非同名端，先写出以同名端为 $+$ 的电压 $L_2\dfrac{\mathrm d(-i_2)}{\mathrm dt}+M\dfrac{\mathrm di_1}{\mathrm dt}$，再整体乘 $-1$。两种想法结果一致。

### 3. 顺接、反接测互感 :material-star::material-star::material-star-outline:

两个线圈 A（端子 $1$、$1'$）、B（端子 $2$、$2'$）同名端未知。按图 (a)、(b) 两种方式串联后，分别接 $50\,\mathrm{Hz}$ 正弦电源测量：

- 接法 (a)：$U=74\,\mathrm V$，$I=2\,\mathrm A$，$P=48\,\mathrm W$；
- 接法 (b)：$U=26\,\mathrm V$，$I=2\,\mathrm A$，$P=48\,\mathrm W$。

判断哪种是顺接、哪两个端子是同名端，并求互感 $M$ 与 $L_1+L_2$。

![顺接与反接](../images/ex/m-series.svg){ .circuit }

??? success "答案"
    接法 (a) 为顺接，$1$ 与 $2$（以及 $1'$ 与 $2'$）为同名端；$M=\dfrac{7.5}{100\pi}\approx23.9\,\mathrm{mH}$，$L_1+L_2=\dfrac{20}{100\pi}\approx63.7\,\mathrm{mH}$。

??? note "解析"
    1. 两种接法电流相同、功率相同，电阻不变：$R=\dfrac{P}{I^2}=\dfrac{48}{4}=12\,\Omega$（两线圈电阻之和）。
    2. 电抗：

        $$
        |Z_a|=\frac{74}{2}=37\ \Rightarrow\ X_a=\sqrt{37^2-12^2}=35\,\Omega,\qquad
        |Z_b|=\frac{26}{2}=13\ \Rightarrow\ X_b=\sqrt{13^2-12^2}=5\,\Omega .
        $$

    3. 电抗大的是顺接：$\omega(L_1+L_2+2M)=35$，$\omega(L_1+L_2-2M)=5$。相减得 $4\omega M=30$，$\omega M=7.5\,\Omega$；相加得 $\omega(L_1+L_2)=20\,\Omega$。以 $\omega=100\pi\,\mathrm{rad/s}$ 代入得上面的结果。
    4. **同名端**：接法 (a) 中电流从 $1$ 流入 A、从 $1'$ 流出后从 $2$ 流入 B。顺接要求两电流都从同名端流入，所以 $1$ 与 $2$ 为同名端。

    （检查：$M\le\sqrt{L_1L_2}\le\dfrac{L_1+L_2}{2}\approx31.8\,\mathrm{mH}$，$23.9\,\mathrm{mH}$ 合理。）

## 去耦与回路方程

### 4. 异名端相连的 T 形去耦 :material-star::material-star::material-star-outline:

$\dot U=50\angle0^\circ\,\mathrm V$，$\omega L_1=4\,\Omega$（$a$–$n$），$\omega L_2=8\,\Omega$（$n$–地），$\omega M=2\,\Omega$；$L_1$ 的同名端在 $a$ 端，$L_2$ 的同名端在 $n$ 端（上端），$6\,\Omega$ 电阻与 $L_2$ 并联。求输入阻抗 $Z_{in}$ 和电流 $\dot I$。

![T 形去耦](../images/ex/m-tdec.svg){ .circuit }

??? success "答案"
    $Z_{in}=6+j8\,\Omega$，$\dot I=5\angle(-53.13^\circ)=3-j4\,\mathrm A$。

??? note "解析"
    1. **判断接法**：公共节点 $n$ 上，$L_1$ 接的是非同名端，$L_2$ 接的是同名端——**异名端相连**。
    2. **去耦**：$L_1$ 一侧臂 $j(\omega L_1+\omega M)=j6$，$L_2$ 一侧臂 $j(\omega L_2+\omega M)=j10$，通向 $n$ 的臂 $-j\omega M=-j2$。
    3. 去耦后，从内部节点到地有两条路径：$j10$ 臂，以及"$-j2$ 臂 + $6\,\Omega$"：

        $$
        j10\parallel(6-j2)=\frac{j10(6-j2)}{6+j8}=\frac{20+j60}{6+j8}=6+j2\,\Omega ,
        $$

        $$
        Z_{in}=j6+6+j2=6+j8=10\angle53.13^\circ\,\Omega,\qquad \dot I=\frac{50}{10\angle53.13^\circ}=5\angle(-53.13^\circ)\,\mathrm A .
        $$

    **用耦合方程校验**：设 $L_2$ 中向下电流 $\dot I_2$、节点电压 $\dot U_n$，两电流都从同名端流入，互感项取 $+$：

    $$
    \dot U-\dot U_n=j4\dot I+j2\dot I_2,\qquad \dot U_n=j8\dot I_2+j2\dot I,\qquad \dot I=\dot I_2+\frac{\dot U_n}{6}.
    $$

    解得 $\dot I_2=-1.8-j2.6\,\mathrm A$，$\dot U_n=28.8-j8.4\,\mathrm V$，$\dot I=\dot I_2+\dot U_n/6=3-j4\,\mathrm A$ ✓

    !!! warning "同名端一错，全题皆错"
        若误当成同名端相连（臂为 $j2$、$j6$、$+j2$），会得到 $Z_{in}=2.16+j5.12\,\Omega$，与正确结果相差很大。

### 5. 含互感的电路列方程 :material-star::material-star::material-star-outline:

（作业 5-34 改编）$\dot U_S=20\angle0^\circ\,\mathrm V$（上正），$\dot I_S=j2\,\mathrm A$（向上），$R=5\,\Omega$，$\omega L_1=\omega L_2=4\,\Omega$，$\omega M=2\,\Omega$；$L_1$ 的同名端在上端，$L_2$ 的同名端在左端。求 $\dot I_1$ 及两个电源各自**发出**的有功功率。

![含互感的电路](../images/ex/m-mesh.svg){ .circuit }

??? success "答案"
    $\dot I_1=\dfrac{80-j64}{41}\approx1.951-j1.561=2.50\angle(-38.66^\circ)\,\mathrm A$；电压源发出 $\dfrac{1600}{41}\approx39.02\,\mathrm W$，电流源发出 $-\dfrac{320}{41}\approx-7.80\,\mathrm W$（实际吸收 $7.80\,\mathrm W$）。

??? note "解析"
    1. **$L_2$ 的电流**：电流源把 $\dot I_S$ 送到右上节点，它只能经 $L_2$ 从右向左流，所以 $L_2$ 中"从左端（同名端）流入"的电流为 $-\dot I_S=-j2\,\mathrm A$。
    2. **中间支路 KVL**（$\dot I_1$ 从 $L_1$ 同名端流入，电压以同名端为 $+$，互感项按"$L_2$ 中流入同名端的电流"取 $+$）：

        $$
        \dot U_S=(R+j\omega L_1)\dot I_1+j\omega M(-\dot I_S)\ \Rightarrow\ 20=(5+j4)\dot I_1+4,
        $$

        $$
        \dot I_1=\frac{16}{5+j4}=\frac{80-j64}{41}\approx1.951-j1.561\,\mathrm A .
        $$

    3. **电压源**：从 $+$ 端流出的电流 $\dot I_U=\dot I_1+(-\dot I_S)=1.951-j3.561\,\mathrm A$，

        $$
        P_U=\mathrm{Re}[\dot U_S\dot I_U^*]=20\times1.951=\frac{1600}{41}\approx39.02\,\mathrm W .
        $$

    4. **电流源**：$L_2$ 左端到右端的电压 $j\omega L_2(-\dot I_S)+j\omega M\dot I_1=8+j2\dot I_1$，所以右上节点电位

        $$
        \dot V=20-8-j2\dot I_1=12-j2\dot I_1\approx8.878-j3.902\,\mathrm V ,
        $$

        $$
        P_I=\mathrm{Re}[\dot V\dot I_S^*]=\mathrm{Re}[(8.878-j3.902)(-j2)]=-\frac{320}{41}\approx-7.80\,\mathrm W .
        $$

    5. **校验**：电阻消耗 $5|\dot I_1|^2=5\times\dfrac{10496}{1681}\approx31.22\,\mathrm W=39.02-7.80$ ✓

    !!! warning "易错"
        $L_2$ 的电压不只是 $j\omega L_2\dot I_{L2}$，还要加上 $\dot I_1$ 通过互感产生的 $j\omega M\dot I_1$；反过来 $L_1$ 支路的 KVL 也不能漏掉 $j\omega M\dot I_{L2}$。

## 空心变压器与理想变压器

### 6. 反映阻抗 :material-star::material-star::material-star-outline:

$\dot U_S=100\angle0^\circ\,\mathrm V$，$R_1=10\,\Omega$，$\omega L_1=20\,\Omega$，$\omega L_2=10\,\Omega$，$\omega M=10\,\Omega$，$R_L=10\,\Omega$，同名端都在上。求反映阻抗、$\dot I_1$、$\dot I_2$ 及负载功率 $P_L$。

![空心变压器](../images/ex/m-reflect.svg){ .circuit }

??? success "答案"
    $Z_r=5-j5\,\Omega$；$\dot I_1\approx4.714\angle(-45^\circ)\,\mathrm A$，$\dot I_2=\tfrac{10}{3}\angle0^\circ\approx3.333\angle0^\circ\,\mathrm A$；$P_L=\tfrac{1000}{9}\approx111.1\,\mathrm W$。

??? note "解析"
    1. 二次回路总阻抗 $Z_{22}=R_L+j\omega L_2=10+j10\,\Omega$，反映阻抗

        $$
        Z_r=\frac{(\omega M)^2}{Z_{22}}=\frac{100}{10+j10}=5-j5\,\Omega
        $$

        （$Z_{22}$ 感性，反映到一次侧呈容性）。
    2. $Z_{in}=R_1+j\omega L_1+Z_r=15+j15\,\Omega$，$\dot I_1=\dfrac{100}{15\sqrt2\angle45^\circ}\approx4.714\angle(-45^\circ)\,\mathrm A$。
    3. 二次回路：$\dot I_1$ 流入一次同名端，$\dot I_2$ 从二次同名端流出，$j\omega M\dot I_1=Z_{22}\dot I_2$：

        $$
        \dot I_2=\frac{j10\times4.714\angle(-45^\circ)}{14.14\angle45^\circ}=3.333\angle0^\circ\,\mathrm A .
        $$

    4. $P_L=I_2^2R_L=\tfrac{100}{9}\times10\approx111.1\,\mathrm W$；它恰好等于反映电阻吸收的功率 $5\times I_1^2=5\times\tfrac{200}{9}\approx111.1\,\mathrm W$ ✓——反映阻抗的实部就代表二次侧取走的有功。

### 7. 理想变压器的阻抗匹配 :material-star::material-star::material-star-outline:

信号源 $\dot U_S=12\angle0^\circ\,\mathrm V$，内阻 $R_S=800\,\Omega$，经理想变压器向 $R_L=8\,\Omega$ 的扬声器供电。（1）$n$ 为多少时扬声器功率最大？最大功率和扬声器电压各多少？（2）若 $n=5$，扬声器功率多少？（3）不用变压器直接连接呢？

![理想变压器匹配](../images/ex/m-match.svg){ .circuit }

??? success "答案"
    （1）$n=10$，$P_{\max}=45\,\mathrm{mW}$，$U_L=0.6\,\mathrm V$；（2）$28.8\,\mathrm{mW}$；（3）约 $1.76\,\mathrm{mW}$。

??? note "解析"
    1. 一次侧看入 $R_{in}=n^2R_L$，匹配条件 $n^2\times8=800\Rightarrow n=10$。

        $$
        P_{\max}=\frac{U_S^2}{4R_S}=\frac{144}{3200}=0.045\,\mathrm W .
        $$

        此时一次电压 $U_1=12/2=6\,\mathrm V$，$U_L=U_1/n=0.6\,\mathrm V$，$0.6^2/8=0.045\,\mathrm W$ ✓
    2. $n=5$：$R_{in}=200\,\Omega$，$I_1=\dfrac{12}{1000}=12\,\mathrm{mA}$，$P=I_1^2R_{in}=0.0288\,\mathrm W$（理想变压器不耗能，一次侧吸收的就是负载功率）。
    3. 直接连接：$P=\Big(\dfrac{12}{808}\Big)^2\times8\approx1.76\,\mathrm{mW}$，只有匹配时的约 $1/25$。

### 8. 同名端与电流方向的陷阱 :material-star::material-star::material-star:

$\dot U_S=20\angle0^\circ\,\mathrm V$，理想变压器变比 $2:1$，一次同名端在上，**二次同名端在下**。$\dot U_2$ 以二次上端为正，$\dot I_2$ 为从负载流入二次**上端**的电流。求 $\dot I_1$、$\dot U_2$、$\dot I_2$。

![理想变压器方向](../images/ex/m-trap.svg){ .circuit }

??? success "答案"
    $\dot I_1=\tfrac53\angle0^\circ\approx1.667\,\mathrm A$，$\dot U_2=-\tfrac{20}{3}\approx-6.667\,\mathrm V$（即 $6.667\angle180^\circ\,\mathrm V$），$\dot I_2=\tfrac{10}{3}\approx3.333\angle0^\circ\,\mathrm A$。

??? note "解析"
    1. **大小**：阻抗折算与同名端无关，$R_{in}=n^2R_L=4\times2=8\,\Omega$，

        $$
        \dot I_1=\frac{20}{4+8}=\frac53\,\mathrm A,\qquad \dot U_1=8\times\frac53=\frac{40}{3}\,\mathrm V .
        $$

    2. **电压**：变比关系只对"都以同名端为 $+$"的电压成立。二次同名端在下，以下端为 $+$ 的电压是 $-\dot U_2$：

        $$
        \dot U_1=n(-\dot U_2)\ \Rightarrow\ \dot U_2=-\frac{\dot U_1}{2}=-\frac{20}{3}\,\mathrm V .
        $$

    3. **电流**：电流关系只对"都流入同名端"的电流成立。流入二次同名端（下端）的电流是 $-\dot I_2$：

        $$
        \dot I_1=-\frac1n(-\dot I_2)\ \Rightarrow\ \dot I_2=n\dot I_1=\frac{10}{3}\,\mathrm A .
        $$

    4. **校验**：$\dot I_2$ 在负载中由下向上流，负载上端电位比下端低 $2\times\tfrac{10}{3}=\tfrac{20}{3}\,\mathrm V$，与 $\dot U_2=-\tfrac{20}{3}$ 一致；功率 $\dot U_1\dot I_1+\dot U_2\dot I_2=\tfrac{200}{9}-\tfrac{200}{9}=0$ ✓，负载得到 $22.2\,\mathrm W$。

    !!! warning "易错"
        把 $\dot U_2=\dot U_1/n$、$\dot I_2=-n\dot I_1$ 直接套用会得到两个符号全错的答案。先把题目的参考方向**翻译**成"以同名端为 $+$、流入同名端"，再套 $u_1=nu_2$、$i_1=-i_2/n$。
