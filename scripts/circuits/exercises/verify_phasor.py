"""习题·相量法 —— 独立验算（sin 约定、有效值相量）。运行无断言失败即通过。"""
import cmath
import math

import numpy as np

P = lambda m, deg: cmath.rect(m, math.radians(deg))          # 极坐标 → 复数
ang = lambda z: math.degrees(cmath.phase(z))
close = lambda a, b, tol=1e-6: abs(a - b) < tol

# 题 1：三要素与相位差（ω=314）
# i2 = -10cos(ωt+60°) = 10 sin(ωt-30°)；u = 220√2 cos(ωt-30°) = 220√2 sin(ωt+60°)
t = np.linspace(0, 0.04, 2001); w = 314
assert np.allclose(-10 * np.cos(w * t + math.radians(60)), 10 * np.sin(w * t - math.radians(30)))
assert np.allclose(220 * math.sqrt(2) * np.cos(w * t - math.radians(30)),
                   220 * math.sqrt(2) * np.sin(w * t + math.radians(60)))
I2 = 10 / math.sqrt(2)
assert close(I2, 7.0711, 1e-4)
assert close(w / (2 * math.pi), 49.97, 0.01)       # 314 rad/s ≈ 50 Hz
print("1: I2=%.4f  φ(u,i1)=%d  φ(u,i2)=%d" % (I2, 60 - 30, 60 - (-30)))

# 题 2：i1 = 6√2 sin(ωt+30°)，i2 = 8√2 cos(ωt+30°) = 8√2 sin(ωt+120°)
I = P(6, 30) + P(8, 120)
assert close(abs(I), 10) and close(ang(I), 30 + math.degrees(math.atan2(8, 6)))
print("2: I=%.4f∠%.2f°" % (abs(I), ang(I)))

# 题 3：电感、电容
UL = 1j * 314 * 0.02 * P(0.010, -30)
assert close(abs(UL), 0.0628) and close(ang(UL), 60)
XC = 1 / (1e6 * 500e-12)
UC = -1j * XC * P(0.010, -30)
assert close(XC, 2000) and close(abs(UC), 20) and close(ang(UC), -120)
print("3: UL=%.4f V ∠%.1f, XC=%.0f, UC=%.2f∠%.1f" % (abs(UL), ang(UL), XC, abs(UC), ang(UC)))

# 题 4：电表读数
assert close(math.hypot(3, 8 - 4), 5)                 # 并联：I=√(IR²+(IL-IC)²)
assert close(math.hypot(30, 80 - 40), 50)              # 串联：U=√(UR²+(UL-UC)²)
print("4: 5 A, 50 V")

# 题 5：阻抗与频率
par = lambda a, b: a * b / (a + b)
Z1 = 4 + par(6j, 3 - 3j)
assert close(Z1, 10)
Z2 = 4 + par(12j, 3 - 1.5j)
print("5: Z(ω)=", Z1, " Z(2ω)=%.4f%+.4fj |Z|=%.4f ∠%.2f" % (Z2.real, Z2.imag, abs(Z2), ang(Z2)))
assert close(Z2, 4 + (432 - 81j) / 119.25) and close(Z2, 7.6226 - 0.6792j, 1e-4)

# 题 6：作业 5-14
Iin = 1.0
Uc = -6j * Iin
IL = Iin + 0.5 * Uc
U = 6 * Iin + Uc + 12j * IL
assert close(U / Iin, 42 + 6j)
print("6: Z=", U / Iin)

# 题 7：作业 5-19
Rl = 40 / 0.36**2
Zm = 220 / 0.36
XL = math.sqrt(Zm**2 - Rl**2)
L = XL / (2 * math.pi * 50)
cosphi = 40 / (220 * 0.36)
assert close(Rl, 308.642, 1e-3) and close(Zm, 611.111, 1e-3) and close(XL, 527.44, 0.01) and close(L, 1.679, 1e-3)
print("7: R=%.3f |Z|=%.3f XL=%.2f L=%.4f cosφ=%.4f" % (Rl, Zm, XL, L, cosphi))

# 题 8：作业 5-12（以 U_C 为参考）
I1 = 10j                       # 电容电流超前 U_C 90°
I2_ = P(10 * math.sqrt(2), -45)  # R2=XL → 滞后 45°
Itot = I1 + I2_
assert close(Itot, 10)
UR1 = 10 * Itot
UCm = 200 - abs(UR1)           # U、U_R1、U_C 同相
XC = UCm / 10
Z2 = UCm / abs(I2_)
R2 = XL2 = Z2 / math.sqrt(2)
UL_ = 1j * XL2 * I2_
UR2 = R2 * I2_
Utot = UR1 + UCm
assert close(UCm, 100) and close(XC, 10) and close(R2, 5) and close(abs(UL_), 50 * math.sqrt(2)) and close(ang(UL_), 45)
assert close(abs(Utot), 200)
assert close(UR2 + UL_, UCm)   # 右支路 KVL
print("8: Uc=%.1f XC=%.1f R2=XL=%.2f UL=%.3f∠%.1f UR2=%s" % (UCm, XC, R2, abs(UL_), ang(UL_), UR2))

# 题 9：正弦节点法  us1=10√2 sin1000t → 10∠0；us2=10√2 cos1000t → 10∠90°
w = 1000; Rr = 5; C = 200e-6; Lh = 5e-3
ZC, ZL = 1 / (1j * w * C), 1j * w * Lh
assert close(ZC, -5j) and close(ZL, 5j)
U1, U2 = 10, P(10, 90)
Ua = (U1 / Rr + U2 / ZL) / (1 / Rr + 1 / ZC + 1 / ZL)
assert close(Ua, 20)
Ic = Ua / ZC
assert close(Ic, 4j)
IL9 = (Ua - U2) / ZL            # 由 a 流向 us2
IR9 = (U1 - Ua) / Rr            # 由 us1 流向 a
assert close(IR9, -2) and close(IR9, Ic + IL9)
print("9: Ua=", Ua, "Ic=", Ic, "IL(a→b)=", IL9, "|IL|=%.4f ∠%.2f" % (abs(IL9), ang(IL9)), "IR=", IR9)
print("all ok")
