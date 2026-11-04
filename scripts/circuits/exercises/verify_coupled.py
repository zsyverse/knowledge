"""习题·互感与理想变压器 —— 独立验算（完整耦合方程求解，不只依赖去耦公式）。"""
import cmath
import math

import numpy as np
import sympy as sp

close = lambda a, b, tol=1e-9: abs(a - b) < tol
ang = lambda z: math.degrees(cmath.phase(z))

# ---- 题 2：耦合方程（符号检查）：L1 同名端在上，L2 同名端在下；i1、i2 都从上端流入，u1、u2 都上正
# 用"磁链"写法核对：ψ1 = L1 i1 + M*(L2 中从同名端流入的电流) = L1 i1 + M*(-i2)
#                   ψ2(从同名端看) = L2*(-i2) + M i1，而 u2 的 + 在非同名端 → u2 = -dψ2/dt = L2 di2 - M di1
t = sp.symbols("t"); i1 = sp.Function("i1")(t); i2 = sp.Function("i2")(t); L1, L2, M = sp.symbols("L1 L2 M")
u1 = sp.diff(L1 * i1 + M * (-i2), t)
u2 = -sp.diff(L2 * (-i2) + M * i1, t)
assert sp.simplify(u1 - (L1 * sp.diff(i1, t) - M * sp.diff(i2, t))) == 0
assert sp.simplify(u2 - (L2 * sp.diff(i2, t) - M * sp.diff(i1, t))) == 0
print("2: u1 =", u1, "; u2 =", sp.expand(u2))

# ---- 题 3：顺接/反接测 M
w = 100 * math.pi
R = 48 / 2**2
X1 = math.sqrt((74 / 2)**2 - R**2); X2 = math.sqrt((26 / 2)**2 - R**2)
assert close(R, 12) and close(X1, 35) and close(X2, 5)
wM = (X1 - X2) / 4
Mval = wM / w
print(f"3: R={R} X+={X1} X-={X2} wM={wM} M={Mval*1e3:.2f} mH  w(L1+L2)={(X1+X2)/2}")

# ---- 题 4：T 形去耦（异名端相连）+ 完整方程校验
U = 50; a, b, m, Rr = 4, 8, 2, 6   # ωL1, ωL2, ωM, R
# 去耦
Zin = 1j * (a + m) + (1j * (b + m)) * (Rr - 1j * m) / (1j * (b + m) + Rr - 1j * m)
assert close(Zin, 6 + 8j)
I = U / Zin
# 完整方程：未知 I (=L1 电流, a→n)，IL2 (L2 电流 n→g)，Vn
# L1：同名端在 a 端；L2：同名端在 n 端（上端）。I 从 L1 同名端流入；IL2 从 L2 同名端流入
# U - Vn = j a I + j m IL2 ;  Vn = j b IL2 + j m I ;  I = IL2 + Vn/R
A = np.array([[1j * a, 1j * m, 1], [1j * m, 1j * b, -1], [1, -1, -1 / Rr]], dtype=complex)
x = np.linalg.solve(A, np.array([U, 0, 0], dtype=complex))
assert close(x[0], I)
# 同名端相连时（对比）
Zs = 1j * (a - m) + (1j * (b - m)) * (Rr + 1j * m) / (1j * (b - m) + Rr + 1j * m)
A2 = np.array([[1j * a, -1j * m, 1], [-1j * m, 1j * b, -1], [1, -1, -1 / Rr]], dtype=complex)
x2 = np.linalg.solve(A2, np.array([U, 0, 0], dtype=complex))
assert close(U / x2[0], Zs)
print(f"4: Zin={Zin} I={abs(I)}∠{ang(I):.2f}  IL2={x[1]:.4f} Vn={x[2]:.4f}  same-dot Zin={Zs:.4f}")
print("   arm j10 || (6-j2) =", (10j) * (6 - 2j) / (6 + 8j))

# ---- 题 5：网孔/支路方程（作业 5-34 改编）U=20∠0，R=5，ωL1=4，ωL2=4，ωM=2，Is=j2
# 结构：左电压源（上+）；中支路 L1(同名端在上)+R 到地，电流 I1 向下；上方 L2 从中节点到右节点，同名端在左；
# 右侧电流源 Is 向上（从地流到右节点），于是 L2 中从左到右的电流 = -Is
Us, R5, wL1, wL2, wM, Is = 20, 5, 4, 4, 2, 2j
IL2 = -Is                               # 从左（同名端）流入
I1 = sp.symbols("I1")
I1v = complex(sp.solve(sp.Eq(Us, (R5 + 1j * wL1) * I1 + 1j * wM * IL2), I1)[0])
assert close(I1v, (80 - 64j) / 41)
IU = I1v + IL2                          # 电压源从 + 端流出的电流 = I1 + (L2 中向右电流)
# 右节点电位 Vs = Us - (L2 左端到右端电压降)
U_L2 = 1j * wL2 * IL2 + 1j * wM * I1v
Vs = Us - U_L2
PU = (Us * IU.conjugate()).real          # 电压源发出
PI = (Vs * Is.conjugate()).real          # 电流源发出（电流从其 + 端（上）流出）
assert close(PU, 1600 / 41) and close(PI, -320 / 41)
assert close(PU + PI, R5 * abs(I1v)**2)
print(f"5: I1={I1v:.5f} |I1|={abs(I1v):.5f}∠{ang(I1v):.3f} IU={IU:.5f} Vs={Vs:.5f} PU={PU:.4f} PI={PI:.4f}")

# ---- 题 6：空心变压器反映阻抗：Us=100，R1=10，ωL1=20，ωM=10，ωL2=10，RL=10
R1, wL1, wM, wL2, RL = 10, 20, 10, 10, 10
Z11, Z22 = R1 + 1j * wL1, 1j * wL2 + RL
Zr = wM**2 / Z22
assert close(Zr, 5 - 5j)
Zin = Z11 + Zr
# 完整方程：I1 流入一次同名端，I2 从二次同名端流出流向负载
# 一次：Us = Z11 I1 - jωM I2 ；二次：0 = -jωM I1 + Z22 I2
A = np.array([[Z11, -1j * wM], [-1j * wM, Z22]])
I1c, I2c = np.linalg.solve(A, np.array([100, 0], dtype=complex))
assert close(I1c, 100 / Zin)
PL = abs(I2c)**2 * RL
assert close(PL, Zr.real * abs(I1c)**2) and close(PL, 1000 / 9)
print(f"6: Zr={Zr} Zin={Zin} I1={abs(I1c):.4f}∠{ang(I1c):.2f} I2={abs(I2c):.4f}∠{ang(I2c):.2f} PL={PL:.3f}")

# ---- 题 7：理想变压器匹配：Us=12 V，Rs=800，RL=8
n = math.sqrt(800 / 8)
Pmax = 12**2 / (4 * 800)
U1 = 12 / 2; U2 = U1 / n
assert close(n, 10) and close(U2**2 / 8, Pmax)
n5 = 5; Rin = n5**2 * 8; I1 = 12 / (800 + Rin); P5 = I1**2 * Rin
Pdirect = (12 / 808)**2 * 8
assert close(P5, 0.0288) and Pdirect < P5 < Pmax
# 校验 L 的物理可实现性（题 3、6）
assert 7.5**2 <= 10 * 10 and 10**2 <= 20 * 10
print(f"7: n={n} Pmax={Pmax} U2={U2}  n=5: Rin={Rin} P={P5}  direct P={Pdirect*1e3:.4f} mW")

# ---- 题 8：理想变压器方向陷阱：n=2，一次同名端在上，二次同名端在下；Us=20，R1=4，RL=2
# 未知：U1(一次上+), I1(流入一次上端=同名端), U2(二次上+), I2(流入二次上端)
# 约束：u_dot1 = n u_dot2：U1 = n*(-U2)；电流：i_dot1 = -i_dot2/n，i_dot2 = -I2 → I1 = I2/n
# 外电路：Us = 4 I1 + U1；负载接在二次上下端，I2 从负载上端流向绕组上端：U2 = -RL*I2
n = 2
Aa = np.array([[1, 0, n, 0], [0, 1, 0, -1 / n], [1, 4, 0, 0], [0, 0, 1, 2]], dtype=float)
U1, I1, U2, I2 = np.linalg.solve(Aa, np.array([0, 0, 20, 0], dtype=float))
assert close(U2, -20 / 3) and close(I2, 10 / 3) and close(I1, 5 / 3) and close(U1, 40 / 3)
assert close(U1 * I1 + U2 * I2, 0)       # 理想变压器不耗能
print(f"8: U1={U1:.4f} I1={I1:.4f} U2={U2:.4f} I2={I2:.4f}  P_RL={2*I2**2:.4f}")
print("all ok")
