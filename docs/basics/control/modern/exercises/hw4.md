---
date: 2026-11-05
description: 可交换时变系统的状态转移矩阵及其性质、离散状态转移矩阵的 z 变换法与特征值规范型法、离散阶跃响应与稳态值、零阶保持精确离散化与前向差分近似、不可交换时变系统的 Peano–Baker 级数与指数公式反例，共 4 题。
tags:
  - 控制理论
  - 现代控制
  - 习题
---

# 习题：时变系统与离散系统的运动分析

对应知识点：[时变系统与离散系统的运动分析](../notes/tv-discrete-response.md)（时变状态转移矩阵的求法与性质、离散系统的递推解与 $z$ 变换解、连续系统的离散化）。除特别声明外，初始时刻取 $t_0=0$ 或 $k_0=0$。

## 1. 可交换时变系统的状态转移矩阵

试求线性时变系统

$$
\dot x(t)=\begin{bmatrix}1&0\\0&2t\end{bmatrix}x(t)
$$

的状态转移矩阵 $\Phi(t,0)$，并完成下列各问。

（1）先做可交换性检验：计算 $A(t_1)A(t_2)$ 与 $A(t_2)A(t_1)$，判断应当用矩阵指数式还是 Peano–Baker 级数。

（2）求 $\Phi(t,0)$，并代回矩阵微分方程 $\dot\Phi(t,t_0)=A(t)\Phi(t,t_0)$、$\Phi(t_0,t_0)=I$ 逐项验证。

（3）求一般的 $\Phi(t,t_0)$，并据此写出 $\Phi(t,1)$。由这一结果说明：本系统的 $\Phi$ 不能写成时间差 $t-t_0$ 的函数，即 $\Phi(t,t_0)\ne\Phi(t-t_0)$。

（4）用所得结果验证分段转移性质 $\Phi(2,1)\Phi(1,0)=\Phi(2,0)$ 与可逆性 $\Phi^{-1}(t,0)=\Phi(0,t)$。

（5）设初始状态 $x(0)=[1\ \ 1]\tp$，写出受扰运动 $x(t)$，并指出 $t\to\infty$ 时哪个分量增长得更快、为什么。

??? success "解答"
    已知 $\dot x=A(t)x$，$A(t)=\diag(1,2t)$，初始时刻为 $0$。

    **（1）可交换性检验**

    任取 $t_1,t_2$，有

    $$
    A(t_1)A(t_2)=A(t_2)A(t_1)
    =\begin{bmatrix}1&0\\0&4t_1t_2\end{bmatrix}.
    $$

    故各时刻的系数矩阵可交换，可直接使用

    $$
    \Phi(t,0)=\exp\left(\int_0^t A(\tau)\,d\tau\right).
    $$

    **（2）求状态转移矩阵并验证**

    $$
    \int_0^t A(\tau)\,d\tau=
    \begin{bmatrix}t&0\\0&t^2\end{bmatrix},\qquad
    \boxed{\Phi(t,0)=\begin{bmatrix}e^t&0\\0&e^{t^2}\end{bmatrix}.}
    $$

    逐项求导：

    $$
    \dot\Phi(t,0)=\begin{bmatrix}e^t&0\\0&2te^{t^2}\end{bmatrix}
    =A(t)\Phi(t,0).
    $$

    且 $\Phi(0,0)=\diag(1,1)=I$，满足定义。

    **（3）一般初始时刻与 $\Phi(t,1)$**

    $$
    \boxed{\Phi(t,t_0)=
    \begin{bmatrix}e^{t-t_0}&0\\0&e^{t^2-t_0^2}\end{bmatrix},}
    $$

    故

    $$
    \boxed{\Phi(t,1)=
    \begin{bmatrix}e^{t-1}&0\\0&e^{t^2-1}\end{bmatrix}.}
    $$

    第二个指数 $t^2-t_0^2=(t-t_0)(t+t_0)$ 还依赖 $t+t_0$，因此不能只用时间差表示。比如同为间隔 $1$：

    $$
    \Phi(1,0)=\diag(e,e),\qquad
    \Phi(2,1)=\diag(e,e^3).
    $$

    两者不同，故不存在只依赖 $t-t_0$ 的统一状态转移函数。

    **（4）分段转移与可逆性**

    $$
    \begin{aligned}
    \Phi(2,1)\Phi(1,0)
    &=\begin{bmatrix}e&0\\0&e^3\end{bmatrix}
    \begin{bmatrix}e&0\\0&e\end{bmatrix}\\
    &=\begin{bmatrix}e^2&0\\0&e^4\end{bmatrix}=\Phi(2,0).
    \end{aligned}
    $$

    一般地，两个对角指数分别相加，得到$\Phi(t,t_1)\Phi(t_1,t_0)=\Phi(t,t_0)$。

    又因为两个对角元均非零，

    $$
    \boxed{\Phi^{-1}(t,0)=
    \begin{bmatrix}e^{-t}&0\\0&e^{-t^2}\end{bmatrix}=\Phi(0,t).}
    $$

    这里 $\Phi(0,t)$ 表示从时刻 $t$ 反向转移到 $0$。

    **（5）初值响应与增长速度**

    取 $x(0)=[1,1]\tp$，零输入受扰运动为

    $$
    \boxed{x(t)=\Phi(t,0)x(0)=\begin{bmatrix}e^t\\e^{t^2}\end{bmatrix}.}
    $$

    当 $t\to\infty$，

    $$
    \frac{x_2(t)}{x_1(t)}=e^{t^2-t}\to\infty,
    $$

    所以第二分量增长更快。第一分量的对数增长为 $t$，第二分量为 $t^2$。

## 2. 离散状态转移矩阵与阶跃响应

已知线性定常离散系统的状态方程为

$$
x(k+1)=\begin{bmatrix}0&1\\-0.1&-0.7\end{bmatrix}x(k)+\begin{bmatrix}0\\1\end{bmatrix}u(k).
$$

以下依次用两种方法求 $\Phi(k)$，再求状态解与稳态值。

（1）求预解矩阵 $(zI-G)^{-1}$，并用 $z$ 变换法 $\Phi(k)=\Zt^{-1}\left[(zI-G)^{-1}z\right]$ 求出状态转移矩阵 $\Phi(k)=G^k$。

（2）再用特征值规范型法（$G$ 为能控规范型，特征向量可取 $[1\ \ \lambda_i]\tp$）独立地求一次 $G^k$，与第（1）问的结果比较。

（3）用 $\Phi(0)=I$、$\Phi(1)=G$、$\Phi(2)=G^2$ 三处回代验算。

（4）设 $x(0)=[1\ \ 0]\tp$，输入为单位阶跃序列 $u(k)=1(k)$。用 $z$ 变换法求状态解 $x(k)$，并用递推法算出 $x(1),x(2),x(3)$ 加以校核。

（5）求 $k\to\infty$ 时的稳态值 $x(\infty)=(I-G)^{-1}H$，说明它与第（4）问结果中哪一项对应；并由 $G$ 的特征值说明该稳态值为什么存在。

??? success "解答"
    记

    $$
    G=\begin{bmatrix}0&1\\-\frac1{10}&-\frac7{10}\end{bmatrix},\qquad
    H=\begin{bmatrix}0\\1\end{bmatrix}.
    $$

    采用单边 $z$ 变换，$\mathcal Z\{a^k\}=z/(z-a)$，$k\ge0$。

    **（1）预解矩阵与 $z$ 变换法**

    $$
    zI-G=\begin{bmatrix}z&-1\\\frac1{10}&z+\frac7{10}\end{bmatrix},
    $$

    $$
    D(z)=z^2+\frac7{10}z+\frac1{10}
    =\left(z+\frac15\right)\left(z+\frac12\right).
    $$

    所以

    $$
    \boxed{(zI-G)^{-1}=\frac1{D(z)}
    \begin{bmatrix}z+\frac7{10}&1\\-\frac1{10}&z\end{bmatrix}.}
    $$

    将 $z(zI-G)^{-1}$ 分解为

    $$
    \begin{aligned}
    z(zI-G)^{-1}
    ={}&\frac{z}{z+\frac15}\,
    \frac13\begin{bmatrix}5&10\\-1&-2\end{bmatrix}\\
    &+\frac{z}{z+\frac12}\,
    \frac13\begin{bmatrix}-2&-10\\1&5\end{bmatrix}.
    \end{aligned}
    $$

    记 $a_k=(-1/5)^k$、$b_k=(-1/2)^k$，逐项反变换得

    $$
    \boxed{\Phi(k)=G^k=\frac13
    \begin{bmatrix}
    5a_k-2b_k&10a_k-10b_k\\
    -a_k+b_k&-2a_k+5b_k
    \end{bmatrix}.}
    $$

    **（2）特征值规范型法**

    特征值为 $\lambda_1=-1/5$、$\lambda_2=-1/2$。由能控伴随型结构，取

    $$
    P=\begin{bmatrix}1&1\\-\frac15&-\frac12\end{bmatrix},\qquad
    P^{-1}=\begin{bmatrix}\frac53&\frac{10}3\\-\frac23&-\frac{10}3\end{bmatrix}.
    $$

    $\det P=-3/10\ne0$，且

    $$
    P^{-1}GP=\diag(-1/5,-1/2).
    $$

    于是

    $$
    G^k=P\begin{bmatrix}a_k&0\\0&b_k\end{bmatrix}P^{-1},
    $$

    相乘恰好得到第（1）问的同一个矩阵。

    **（3）三个时刻回代**

    当 $k=0$，$a_0=b_0=1$，回代得 $\Phi(0)=I$；当 $k=1$，$a_1=-1/5$、$b_1=-1/2$，回代得 $\Phi(1)=G$。当 $k=2$，$a_2=1/25$、$b_2=1/4$，得

    $$
    \boxed{\Phi(2)=G^2=
    \begin{bmatrix}-\frac1{10}&-\frac7{10}\\\frac7{100}&\frac{39}{100}\end{bmatrix}.}
    $$

    三个回代均一致。

    **（4）非零初值下的阶跃响应**

    取 $x(0)=[1,0]\tp$、$u(k)=1$（$k\ge0$），有

    $$
    zX(z)-zx(0)=GX(z)+HU(z),\quad U(z)=\frac{z}{z-1}.
    $$

    故

    $$
    X(z)=(zI-G)^{-1}\left(zx(0)+H\frac{z}{z-1}\right).
    $$

    展开为

    $$
    \begin{aligned}
    X_1(z)&=\frac{z(z+\frac7{10})}{D(z)}+
    \frac{z}{(z-1)D(z)},\\
    X_2(z)&=-\frac{z}{10D(z)}+
    \frac{z^2}{(z-1)D(z)}.
    \end{aligned}
    $$

    部分分式为

    $$
    X_1(z)=\frac59\frac{z}{z-1}
    -\frac{10}9\frac{z}{z+\frac15}
    +\frac{14}9\frac{z}{z+\frac12},
    $$

    $$
    X_2(z)=\frac59\frac{z}{z-1}
    +\frac29\frac{z}{z+\frac15}
    -\frac79\frac{z}{z+\frac12}.
    $$

    因此

    $$
    \boxed{\begin{aligned}
    x_1(k)&=\frac59-\frac{10}9a_k+\frac{14}9b_k,\\
    x_2(k)&=\frac59+\frac29a_k-\frac79b_k.
    \end{aligned}}
    $$

    递推式为 $x_1(k+1)=x_2(k)$、$x_2(k+1)=-0.1x_1(k)-0.7x_2(k)+1$。

    | $k$ | $x_1(k)$ | $x_2(k)$ |
    |:---:|:---:|:---:|
    | 0 | 1 | 0 |
    | 1 | 0 | 0.9 |
    | 2 | 0.9 | 0.37 |
    | 3 | 0.37 | 0.651 |

    代入闭式结果也得到以上数值。

    **（5）稳态值与存在条件**

    $$
    I-G=\begin{bmatrix}1&-1\\\frac1{10}&\frac{17}{10}\end{bmatrix},\qquad
    \boxed{x(\infty)=(I-G)^{-1}H=\begin{bmatrix}5/9\\5/9\end{bmatrix}.}
    $$

    它就是第（4）问中的常数项。两个特征值的模分别为 $0.2$、$0.5$，均小于 $1$，所以 $a_k,b_k\to0$；初值产生的暂态衰减，状态收敛到上述稳态。

## 3. 零阶保持离散化与闭环响应

采样控制系统的结构为：参考输入 $r$ 经单位负反馈后，误差信号以周期 $T$ 采样，再经零阶保持器 $\dfrac{1-\e^{-Ts}}{s}$ 驱动连续被控对象 $\dfrac{1}{s(s+2)}$，对象输出 $y$ 即为被反馈的量。取连续对象的状态为 $x_1=y$、$x_2=\dot y$。

（1）写出连续对象的状态空间表达式 $(A,B,C)$，并求 $\e^{At}$。

（2）以采样周期 $T$ 为参数，求零阶保持精确离散化后的 $G(T)=\e^{AT}$ 与 $H(T)=\left(\int_0^T\e^{At}\dd t\right)B$，写出离散化后的状态空间表达式。

（3）取 $T=0.1\,\mathrm s$，求出 $G,H$ 的数值（保留 6 位有效数字，可用 $\e^{-0.2}=0.818731$）。

（4）数字控制器取 $u(k)=r(k)-y(k)$，写出闭环离散系统 $x(k+1)=G_cx(k)+Hr(k)$ 中的 $G_c=G-HC$。

（5）设 $x(0)=0$、$r(k)=1(k)$ 为单位阶跃，用递推法求 $y(kT)$，$k=0,1,\dots,5$。

（6）求 $G_c$ 的特征值及其模，判断闭环离散系统是否收敛；再求稳态输出 $y(\infty)=C(I-G_c)^{-1}H$，并说明它与第（5）问的递推趋势是否一致。

（7）写出同一对象按近似（前向差分）离散化得到的 $G_{\rm app}=I+TA$、$H_{\rm app}=TB$，与第（3）问的精确结果逐元素比较，指出差别出现在哪些元素上、量级如何随 $T$ 变化。

??? success "解答"
    连续对象为 $1/[s(s+2)]$，取 $x_1=y$、$x_2=\dot y$。输入 $u(k)$ 在 $[kT,(k+1)T)$ 内保持常值。

    **（1）连续状态方程与 $e^{At}$**

    由 $\ddot y+2\dot y=u$ 得

    $$
    A=\begin{bmatrix}0&1\\0&-2\end{bmatrix},\quad
    B=\begin{bmatrix}0\\1\end{bmatrix},\quad C=[1\ \ 0],\quad D=0.
    $$

    先解 $\dot x_2=-2x_2$，再积分 $\dot x_1=x_2$，得到

    $$
    \boxed{e^{At}=\begin{bmatrix}1&\frac{1-e^{-2t}}2\\0&e^{-2t}\end{bmatrix}.}
    $$

    在 $t=0$ 为 $I$，且求导后等于 $Ae^{At}$。

    **（2）精确离散化**

    记 $q=e^{-2T}$，则

    $$
    \boxed{G(T)=\begin{bmatrix}1&\frac{1-q}2\\0&q\end{bmatrix}.}
    $$

    输入矩阵由积分得

    $$
    \begin{aligned}
    H(T)&=\int_0^T e^{A\tau}B\,d\tau\\
    &=\begin{bmatrix}\int_0^T\frac{1-e^{-2\tau}}2\,d\tau\\
    \int_0^T e^{-2\tau}\,d\tau\end{bmatrix}
    =\boxed{\begin{bmatrix}\frac{2T-1+q}4\\\frac{1-q}2\end{bmatrix}}.
    \end{aligned}
    $$

    离散状态空间表达式为

    $$
    x(k+1)=G(T)x(k)+H(T)u(k),\qquad y(k)=Cx(k).
    $$

    **（3）$T=0.1\,\mathrm{s}$ 的数值**

    用未截断的 $q=e^{-0.2}$ 计算，结果保留六位有效数字：

    $$
    \boxed{G=\begin{bmatrix}1&0.0906346\\0&0.818731\end{bmatrix},\qquad
    H=\begin{bmatrix}0.00468269\\0.0906346\end{bmatrix}.}
    $$

    若直接使用截断值 $q=0.818731$，会得到 $H_1=0.00468275$；这是提前截断引起的末位差别，以下递推统一使用精确指数。

    **（4）单位负反馈闭环矩阵**

    代入 $u(k)=r(k)-Cx(k)$：

    $$
    x(k+1)=(G-HC)x(k)+Hr(k).
    $$

    故

    $$
    \boxed{G_c=\begin{bmatrix}
    1-\frac{2T-1+q}4&\frac{1-q}2\\
    -\frac{1-q}2&q
    \end{bmatrix}.}
    $$

    在 $T=0.1$ 时，

    $$
    \boxed{G_c=\begin{bmatrix}
    0.995317&0.0906346\\-0.0906346&0.818731
    \end{bmatrix}.}
    $$

    **（5）单位阶跃的前六个采样值**

    $x(0)=0$、$r(k)=1$，递推公式为

    $$
    \begin{aligned}
    x_1(k+1)&=(1-H_1)x_1(k)+H_2x_2(k)+H_1,\\
    x_2(k+1)&=-H_2x_1(k)+qx_2(k)+H_2.
    \end{aligned}
    $$

    其中 $y(kT)=x_1(k)$。用未截断的矩阵递推：

    | $k$ | $y(kT)=x_1(k)$ | $x_2(k)$ |
    |:---:|:---:|:---:|
    | 0 | 0 | 0 |
    | 1 | 0.004682688 | 0.090634623 |
    | 2 | 0.017558084 | 0.164415563 |
    | 3 | 0.037060296 | 0.223655331 |
    | 4 | 0.061840359 | 0.270389175 |
    | 5 | 0.090740089 | 0.306405679 |

    **（6）收敛性与稳态输出**

    数值特征方程为

    $$
    \lambda^2-1.81404806481\lambda+0.823111527155=0.
    $$

    所以

    $$
    \boxed{\lambda_{1,2}=0.9070240324\pm0.0204678234j,}
    $$

    $$
    \boxed{|\lambda_{1,2}|=\sqrt{\det G_c}=0.9072549406<1.}
    $$

    闭环离散系统渐近稳定，恒定输入下存在唯一稳态。

    为了直接求稳态，写成

    $$
    I-G_c=\begin{bmatrix}H_1&-H_2\\H_2&1-q\end{bmatrix}.
    $$

    有 $(I-G_c)[1,0]\tp=H$，且其行列式非零，故

    $$
    \boxed{x(\infty)=[1,0]\tp,\qquad y(\infty)=1.}
    $$

    前五步输出由零逐渐上升，与最终趋于 $1$ 一致。此表只显示初期趋势；复共轭特征值并不保证整个过程严格单调。

    **（7）前向差分近似及误差量级**

    $$
    \boxed{G_{\rm app}=I+TA=\begin{bmatrix}1&T\\0&1-2T\end{bmatrix},\quad
    H_{\rm app}=TB=\begin{bmatrix}0\\T\end{bmatrix}.}
    $$

    在 $T=0.1$ 时，$G_{\rm app}=[\begin{smallmatrix}1&0.1\\0&0.8\end{smallmatrix}]$、$H_{\rm app}=[0,0.1]\tp$。

    用“精确值减近似值”比较：

    $$
    G-G_{\rm app}\approx\begin{bmatrix}0&-0.00936538\\0&0.0187308\end{bmatrix},
    $$

    $$
    H-H_{\rm app}\approx\begin{bmatrix}0.00468269\\-0.00936538\end{bmatrix}.
    $$

    差别出现在 $G_{12},G_{22},H_1,H_2$，而 $G_{11},G_{21}$ 完全相同。由

    $$
    e^{-2T}=1-2T+2T^2-\frac43T^3+O(T^4)
    $$

    得到

    $$
    \begin{aligned}
    G_{12}-T&=-T^2+\frac23T^3+O(T^4),\\
    G_{22}-(1-2T)&=2T^2-\frac43T^3+O(T^4),\\
    H_1-0&=\frac12T^2-\frac13T^3+O(T^4),\\
    H_2-T&=-T^2+\frac23T^3+O(T^4).
    \end{aligned}
    $$

    因此这四项的单步矩阵误差均为 $O(T^2)$。

## 4. 不可交换时变系统与 Peano–Baker 级数

四旋翼投放载荷后等效惯量按 $J(t)\propto(1+t)$ 缓慢增大，其单通道线性化模型为

$$
\dot x(t)=A(t)x(t),\qquad A(t)=\begin{bmatrix}0&1\\0&-\dfrac{1}{1+t}\end{bmatrix},\qquad t\ge0.
$$

以下各问把精确解、指数公式与 Peano–Baker 级数三者逐项比较。

（1）计算 $A(t_1)A(t_2)-A(t_2)A(t_1)$，给出一组具体的 $t_1\ne t_2$ 作为反例；并说明 $A(t)$ 与 $\int_0^tA(\tau)\dd\tau$ 不可交换。

（2）本题的 $A(t)$ 为上三角，可以逐行直接积分：先由第二个方程解出 $x_2(t)$，再代入第一个方程解出 $x_1(t)$，由此写出精确的 $\Phi(t,0)$，并代回矩阵微分方程验证。

（3）算出 $M(t)=\int_0^tA(\tau)\dd\tau$ 与 $\e^{M(t)}$，把 $\e^{M(t)}$ 代入 $\dot\Phi=A(t)\Phi$ 检验，说明“时变系统一律套指数公式”为什么是错的。

（4）写出 Peano–Baker 级数的前三项

$$
I+\int_0^tA(\tau)\dd\tau+\int_0^tA(\tau)\int_0^\tau A(\tau_1)\dd\tau_1\dd\tau .
$$

（5）把第（2）（3）（4）问三个结果的 $(1,2)$ 元在 $t=0$ 处展开到 $t^3$ 项，列表比较：指出三者从第几阶起不同，并说明“前两项相同”并不能保证公式正确。

（6）用分段转移性质与可逆性，由 $\Phi(t,0)$ 求 $\Phi(t,1)$。

??? success "解答"
    记

    $$
    A(t)=\begin{bmatrix}0&1\\0&-\frac1{1+t}\end{bmatrix},\qquad t\ge0.
    $$

    以下记 $L(t)=\ln(1+t)$，$M(t)=\int_0^t A(\tau)\,d\tau$。

    **（1）不可交换性的具体反例**

    $$
    A(t_1)A(t_2)=\begin{bmatrix}
    0&-\frac1{1+t_2}\\0&\frac1{(1+t_1)(1+t_2)}
    \end{bmatrix},
    $$

    交换顺序后，右上元变为 $-1/(1+t_1)$，所以

    $$
    \boxed{[A(t_1),A(t_2)]=
    \begin{bmatrix}0&\frac1{1+t_1}-\frac1{1+t_2}\\0&0\end{bmatrix}.}
    $$

    例如 $t_1=0,t_2=1$，交换子为 $[\begin{smallmatrix}0&1/2\\0&0\end{smallmatrix}]\ne0$。

    进一步，$M=[\begin{smallmatrix}0&t\\0&-L\end{smallmatrix}]$，

    $$
    \boxed{A(t)M(t)-M(t)A(t)=
    \begin{bmatrix}0&-L+\frac{t}{1+t}\\0&0\end{bmatrix}.}
    $$

    当 $t>0$，$L-t/(1+t)>0$（其导数为 $t/(1+t)^2>0$，且在 $0$ 为零），故 $A(t)$ 与自身积分也不可交换。

    **（2）逐行积分求精确解**

    由 $\dot x_2=-x_2/(1+t)$ 得

    $$
    x_2(t)=\frac{x_2(0)}{1+t}.
    $$

    再积分 $\dot x_1=x_2$：

    $$
    x_1(t)=x_1(0)+x_2(0)\ln(1+t).
    $$

    因此

    $$
    \boxed{\Phi(t,0)=\begin{bmatrix}1&L\\0&\frac1{1+t}\end{bmatrix}.}
    $$

    验证：

    $$
    \dot\Phi=\begin{bmatrix}0&\frac1{1+t}\\0&-\frac1{(1+t)^2}\end{bmatrix}
    =A(t)\Phi,\qquad \Phi(0,0)=I.
    $$

    **（3）检验积分后直接取指数的错误**

    $$
    M(t)=\begin{bmatrix}0&t\\0&-L\end{bmatrix}.
    $$

    对上三角矩阵取指数，$t>0$ 时有

    $$
    e^{M(t)}=\begin{bmatrix}1&F(t)\\0&\frac1{1+t}\end{bmatrix},\qquad
    F(t)=\frac{t(1-e^{-L})}{L}=\frac{t^2}{(1+t)L}.
    $$

    在 $t=0$ 按极限令 $F(0)=0$，于是 $e^{M(0)}=I$。但矩阵微分方程要求 $F'(t)=1/(1+t)$，实际

    $$
    F'(t)-\frac1{1+t}
    =\frac{t(t+2)L-t^2-(1+t)L^2}{(1+t)^2L^2}.
    $$

    它不恒为零。例如 $t=1$ 时差值约为 $0.0616790$。所以

    $$
    \boxed{e^{\int_0^t A(\tau)d\tau}\ne\Phi(t,0)\quad(t>0).}
    $$

    只满足初始条件还不够；不可交换时不能直接套积分指数式。

    **（4）Peano–Baker 的前三项**

    写为 $S_2=I+M+B_2$，其中

    $$
    B_2=\int_0^t A(\tau)\left[\int_0^\tau A(\tau_1)\,d\tau_1\right]d\tau.
    $$

    被积矩阵为

    $$
    A(\tau)M(\tau)=\begin{bmatrix}0&-\ln(1+\tau)\\0&\frac{\ln(1+\tau)}{1+\tau}\end{bmatrix}.
    $$

    故

    $$
    \boxed{B_2=\begin{bmatrix}0&t-(1+t)L\\0&\frac12L^2\end{bmatrix},}
    $$

    $$
    \boxed{S_2(t)=\begin{bmatrix}1&2t-(1+t)L\\0&1-L+\frac12L^2\end{bmatrix}.}
    $$

    前三项指 $I$、一次积分、二重积分；这里只是截断近似，不能视为完整级数的精确解。

    **（5）右上元的三阶展开**

    精确解：

    $$
    \Phi_{12}=L=t-\frac12t^2+\frac13t^3+O(t^4).
    $$

    直接指数：

    $$
    F(t)=t-\frac12t^2+\frac5{12}t^3+O(t^4).
    $$

    Peano–Baker 前三项：

    $$
    S_{2,12}=2t-(1+t)L
    =t-\frac12t^2+\frac16t^3+O(t^4).
    $$

    | 右上元 | $t$ 系数 | $t^2$ 系数 | $t^3$ 系数 |
    |:---:|:---:|:---:|:---:|
    | 精确 $\Phi$ | 1 | $-1/2$ | $1/3$ |
    | 直接指数 $e^M$ | 1 | $-1/2$ | $5/12$ |
    | PB 前三项 $S_2$ | 1 | $-1/2$ | $1/6$ |

    三者从 $t^3$ 阶起不同。直接指数的偏差是 $+t^3/12+O(t^4)$；PB截断的偏差是 $-t^3/6+O(t^4)$。

    PB 的下一项 $B_3=\int_0^t A(\tau)B_2(\tau)\,d\tau$ 的右上元为$\frac12\int_0^t\ln^2(1+\tau)\,d\tau=t^3/6+O(t^4)$，正好补上所缺三阶项。完整 PB 级数收敛到精确解；直接指数的三阶误差则来自错误公式。低阶一致不能证明恒等式成立。

    **（6）由分段转移与可逆性求 $\Phi(t,1)$**

    $$
    \Phi(1,0)=\begin{bmatrix}1&\ln2\\0&1/2\end{bmatrix},\qquad
    \Phi^{-1}(1,0)=\begin{bmatrix}1&-2\ln2\\0&2\end{bmatrix}.
    $$

    因此

    $$
    \begin{aligned}
    \Phi(t,1)&=\Phi(t,0)\Phi^{-1}(1,0)\\
    &=\boxed{\begin{bmatrix}1&2\ln\frac{1+t}{2}\\0&\frac2{1+t}\end{bmatrix}}.
    \end{aligned}
    $$

    $\Phi(1,1)=I$，求导也满足 $\partial_t\Phi(t,1)=A(t)\Phi(t,1)$。公式对 $t\ge0$ 都成立；$t<1$ 表示反向转移。
