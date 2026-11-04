"""习题·正弦稳态功率与谐振 —— 独立验算。sin 约定、有效值相量。运行无断言失败即通过。"""
import cmath
import math

import numpy as np

d2r = math.radians
P = lambda m, a: cmath.rect(m, d2r(a))
ang = lambda z: math.degrees(cmath.phase(z))
close = lambda a, b, tol=1e-6: abs(a - b) < tol

# ---- 题 2：一端口功率；i = 5√2 cos(ωt-70°) = 5√2 sin(ωt+20°)
U = P(100, 50); I = P(5, -70 + 90)
# 数值核对 cos→sin 换算：在若干时刻比较
for t in np.linspace(0, 1, 7):
    assert close(5 * math.cos(t - d2r(70)), 5 * math.sin(t + d2r(20)), 1e-12)
S = U * I.conjugate()
Z = U / I
assert close(abs(S), 500) and close(ang(S), 30)
assert close(S.real, 250 * math.sqrt(3)) and close(S.imag, 250)
assert close(Z.real, 10 * math.sqrt(3)) and close(Z.imag, 10)
print("2: S=", S, "lambda=", math.cos(d2r(30)), "Z=", Z)

# ---- 题 3：逐支路复功率
Us = 100
Z1 = 1 - 1j; Z2 = 6 + 8j; Z3 = 8 - 6j
Zp = Z2 * Z3 / (Z2 + Z3)
assert close(Zp, 7 + 1j)
I1 = Us / (Z1 + Zp)
assert close(I1, 12.5)
Uab = I1 * Zp
I2, I3 = Uab / Z2, Uab / Z3
assert close(Uab, 87.5 + 12.5j) and close(I2, 6.25 - 6.25j) and close(I3, 6.25 + 6.25j)
S1, S2, S3 = abs(I1)**2 * Z1, abs(I2)**2 * Z2, abs(I3)**2 * Z3
assert close(S1, 156.25 - 156.25j) and close(S2, 468.75 + 625j) and close(S3, 625 - 468.75j)
assert close(S1 + S2 + S3, Us * I1.conjugate())
print("3: S1,S2,S3=", S1, S2, S3, " |S| sum=", abs(S1) + abs(S2) + abs(S3), " S=", abs(Us * I1))
print("   |I2|=", abs(I2), "|S1|=", abs(S1), "|S2|=", abs(S2))

# ---- 题 4：输电线路（作业 5-23 改编）：负载 10 kW、220 V、cos=0.8 滞后；线路 0.1+j0.1
P2, U2, pf = 10000, 220, 0.8
Iabs = P2 / (U2 * pf)
Q2 = P2 * math.tan(math.acos(pf))
Il = cmath.rect(Iabs, -math.acos(pf))
Zl = 0.1 + 0.1j
U1 = U2 + Il * Zl
S1 = U1 * Il.conjugate()
dP = Iabs**2 * 0.1
assert close(Q2, 7500) and close(S1.real, P2 + dP) and close(S1.imag, Q2 + dP)
eta = P2 / S1.real
lam1 = S1.real / abs(S1)
print(f"4: I={Iabs:.4f} Q2={Q2:.1f} dP={dP:.3f} P1={S1.real:.3f} Q1={S1.imag:.3f}"
      f" U1={abs(U1):.4f}∠{ang(U1):.4f} lam1={lam1:.5f} eta={eta:.5f}")

# ---- 题 5：功率因数补偿 P=10 kW, cos 0.6 -> 0.9, 220 V 50 Hz
w = 100 * math.pi
P_, U_ = 10000, 220
t1, t2 = 4 / 3, math.tan(math.acos(0.9))
C = P_ * (t1 - t2) / (w * U_**2)
I_before, I_after = P_ / (U_ * 0.6), P_ / (U_ * 0.9)
Q1, Q2c = P_ * t1, P_ * t2
QC = Q1 - Q2c
assert close(QC, w * C * U_**2)
# 直接用相量校验：负载电流 + 电容电流
IL = cmath.rect(I_before, -math.acos(0.6)); IC = 1j * w * C * U_
assert close(abs(IL + IC), I_after, 1e-9) and close(math.cos(-cmath.phase(IL + IC)), 0.9, 1e-9)
C1 = P_ * t1 / (w * U_**2)  # 补偿到 1
print(f"5: tan2={t2:.4f} QC={QC:.1f} C={C*1e6:.1f}uF I:{I_before:.2f}->{I_after:.2f}  C(λ=1)={C1*1e6:.1f}uF")

# ---- 题 6：最大功率 Us=20∠0，串 4Ω，并 j4Ω
Uoc = 20 * 4j / (4 + 4j); Zeq = 4 * 4j / (4 + 4j)
assert close(Uoc, 10 + 10j) and close(Zeq, 2 + 2j)
Pm = abs(Uoc)**2 / (4 * Zeq.real)
RL = abs(Zeq)
PR = abs(Uoc)**2 * RL / ((Zeq.real + RL)**2 + Zeq.imag**2)
# 数值扫描验证纯电阻最优
rs = np.linspace(0.01, 20, 200001)
pr = abs(Uoc)**2 * rs / ((2 + rs)**2 + 4)
assert abs(rs[pr.argmax()] - RL) < 1e-3 and close(pr.max(), PR, 1e-6)
# 共轭匹配下直接电路校验
ZL = Zeq.conjugate(); IL_ = Uoc / (Zeq + ZL)
assert close(abs(IL_)**2 * ZL.real, Pm)
print(f"6: Uoc={Uoc} Zeq={Zeq} Pmax={Pm} RL={RL:.4f} P_R={PR:.4f} I(conj)={abs(IL_):.4f}")

# ---- 题 7：瓦特表读数为负
Ua, Ub = 100, P(100, -90)
I = (Ua - Ub) / 10j                     # 从左向右
assert close(I, 10 - 10j)
W = (Ub * (-I).conjugate()).real        # 表的电流取从右向左流入 * 端，电压取 Ub
Pa = (Ua * I.conjugate()).real          # 左源发出
Pb_abs = (Ub * I.conjugate()).real      # 右源吸收（I 从其 + 端流入）
assert close(W, -1000) and close(Pa, 1000) and close(Pb_abs, 1000)
print("7: I=", I, "W=", W, "Pa_out=", Pa, "Pb_abs=", Pb_abs)

# ---- 题 8：串联谐振（作业 5-26 改编）L=250 μH，R=12.5 Ω，f0=1 MHz，U=10 μV
L, R, f0, U = 250e-6, 12.5, 1e6, 10e-6
w0 = 2 * math.pi * f0
C = 1 / (w0**2 * L)
X = w0 * L
I0 = U / R
Q = X / R
UC = I0 * X
BW = f0 / Q
print(f"8: C={C*1e12:.2f}pF X={X:.2f} I0={I0*1e6:.3f}uA Q={Q:.2f} UC={UC*1e3:.4f}mV BW={BW/1e3:.3f}kHz")
assert close(I0, 0.8e-6, 1e-15)

# ---- 题 9：多支路（作业 5-28 改编）ω=500，R1=100，R2=50，C1=C2=20 μF，L=0.4 H，U=200∠30°
w = 500
XL, XC = w * 0.4, 1 / (w * 20e-6)
assert close(XL, 200) and close(XC, 100)
Zb = 1j * XL - 2j * XC
assert close(Zb, 0)
U = P(200, 30)
# 一般求解（不预设短路）：节点法求 c 点电压
# 节点 c：(Vc-U)/R1 + Vc/R2 + Vc/Zb = 0 —— Zb=0 时 Vc=0；用小扰动验证极限
for eps in (1e-3, 1e-6):
    Zb_e = Zb + eps
    Vc = (U / 100) / (1 / 100 + 1 / 50 + 1 / Zb_e)
    assert abs(Vc) < 1e-2
I1 = U / 100
UL = 1j * XL * I1; UC1 = -1j * XC * I1
print("9: I1=", abs(I1), ang(I1), " UL=", abs(UL), ang(UL), " UC1=", abs(UC1), ang(UC1),
      " P=", (U * I1.conjugate()).real)
# 若换成 ω=1000 rad/s 时端口阻抗（附：说明不再谐振）
print("all ok")
