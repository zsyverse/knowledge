"""模电·集成功能电路 —— 例题与练习数值的独立验算。

    cd scripts/circuits/analog && ../../../.venv/bin/python verify_special.py
"""
import math

import numpy as np
import sympy as sp

pi = math.pi


def near(a, b, tol=0.01):
    assert abs(a - b) <= tol * max(abs(b), 1e-12), (a, b)


# ---------------- 三运放仪用放大器：节点方程 ----------------
v1, v2, o1, o2, vo, R, RG, R3, R4 = sp.symbols("v1 v2 o1 o2 vo R R_G R3 R4")
# A1、A2 虚短：反相端电位 = v1、v2；R—R_G—R 串联电流相同
eqs = [sp.Eq((o1 - v1) / R, (v1 - v2) / RG), sp.Eq((v1 - v2) / RG, (v2 - o2) / R)]
s12 = sp.solve(eqs, [o1, o2], dict=True)[0]
# A3：o1 经 R3 → (−)，R4 反馈；o2 经 R3 → (+)，R4 对地
vp = s12[o2] * R4 / (R3 + R4)
vo_ = sp.solve(sp.Eq((s12[o1] - vp) / R3, (vp - vo) / R4), vo)[0]
G = (1 + 2 * R / RG) * R4 / R3
assert sp.simplify(vo_ - G * (v2 - v1)) == 0          # 注意符号：v_O = G (v_I2 − v_I1)
# 第一级共模增益为 1
assert sp.simplify(s12[o1].subs({v1: 1, v2: 1}) - 1) == 0

# 图卡例题：G = 100，R3 = R4，R = 10 k
near(100 * 10e-3, 1.0)
RGv = 2 * 10e3 / 99
near(RGv, 202)
print("card INA R_G:", RGv)

# 例：R = 25 k，R_G = 1 k，R3 = 10 k，R4 = 20 k，v_I1 = 2.010 V，v_I2 = 2.000 V
sub = {R: 25e3, RG: 1e3, R3: 10e3, R4: 20e3, v1: 2.010, v2: 2.000}
O1, O2, VO = float(s12[o1].subs(sub)), float(s12[o2].subs(sub)), float(vo_.subs(sub))
near(O1, 2.260, 1e-4); near(O2, 1.750, 1e-4); near(VO, -1.02, 1e-4)
near(float(G.subs(sub)), 102)
near((2.010 - 2.000) / 1e3, 10e-6)
print("INA example:", O1, O2, VO)


def diff_cm_gain(K, delta):
    """差分级 R4/R3 = K，同相端 R4 偏大 (1+δ) 时的共模增益。"""
    return (1 + K) * K * (1 + delta) / (1 + K * (1 + delta)) - K


# 练习 2：G1 = 100（R = 24.75 k，R_G = 500 Ω），R3 = R4，比值失配 1 %，共模 5 V
near(1 + 2 * 24.75e3 / 500, 100)
Ac = diff_cm_gain(1, 0.01)
near(Ac, 0.004975, 1e-3)
cmrr = 100 / Ac
near(cmrr, 20100, 1e-3); near(20 * math.log10(cmrr), 86.1, 1e-3)
near(5 * Ac * 1e3, 24.9, 2e-3)
# 若不要第一级（只用差分级，增益 1），CMRR = 1/Ac
near(20 * math.log10(1 / Ac), 46.1, 1e-3)
print("ex INA CMRR:", cmrr, 20 * math.log10(cmrr))

# ---------------- 乘法器 ----------------
w, t, A, B, k = sp.symbols("omega t A B k", positive=True)
prod = sp.expand(sp.expand_trig(k * A * sp.sin(w * t) * B * sp.sin(w * t)))
assert sp.simplify(prod - (k * A * B / 2 - k * A * B / 2 * sp.cos(2 * w * t))) == 0
print("sin^2 ok")

# AM：k = 0.1，V0 = 5，Vm = 2.5，Vc = 2；载波 1 V，边频 0.25 V
kk, V0, Vm, Vc = 0.1, 5.0, 2.5, 2.0
near(kk * V0 * Vc, 1.0); near(kk * Vm * Vc / 2, 0.25); near(Vm / V0, 0.5)
# 数值 FFT 验证频谱
fs, fc, F = 2e6, 100e3, 1e3
tt = np.arange(0, 0.01, 1 / fs)
vam = kk * (V0 + Vm * np.cos(2 * pi * F * tt)) * Vc * np.cos(2 * pi * fc * tt)
spec = np.abs(np.fft.rfft(vam)) * 2 / len(tt)
fr = np.fft.rfftfreq(len(tt), 1 / fs)
amp = lambda f0: spec[np.argmin(abs(fr - f0))]
near(amp(100e3), 1.0, 1e-3); near(amp(99e3), 0.25, 1e-3); near(amp(101e3), 0.25, 1e-3)
# 同步检波：再乘 k·(2 cos ωc t)，低通（取平均）后 0.1 + 0.05 cos Ωt
det = kk * vam * 2 * np.cos(2 * pi * fc * tt)
sd = np.abs(np.fft.rfft(det)) * 2 / len(tt)
near(np.mean(det), 0.1, 1e-3); near(sd[np.argmin(abs(fr - 1e3))], 0.05, 1e-3)
# 相位差 60° 时输出减半
det60 = kk * vam * 2 * np.cos(2 * pi * fc * tt + pi / 3)
near(np.mean(det60), 0.05, 1e-3)
print("AM / sync detect ok")

# 除法器：KCL v_X/R1 + k v_O v_Y / R2 = 0
vX, vY, vO, R1, R2 = sp.symbols("v_X v_Y v_O R_1 R_2")
sol = sp.solve(sp.Eq(vX / R1 + k * vO * vY / R2, 0), vO)[0]
assert sp.simplify(sol + R2 / R1 * vX / (k * vY)) == 0
near(float(sol.subs({vX: 2, vY: 4, k: 0.1, R1: 1, R2: 1})), -5)
near(float(sol.subs({vX: 1, vY: 2, k: 0.1, R1: 1, R2: 1})), -5)
near(float(sol.subs({vX: 1, vY: 0.5, k: 0.1, R1: 1, R2: 1})), -20)
# 开方器：v_I/R1 + k v_O^2 / R2 = 0
vI = sp.Symbol("v_I")
sq = sp.solve(sp.Eq(vI / R1 + k * vO**2 / R2, 0), vO)
pos = [x for x in sq if float(x.subs({vI: -3.6, k: 0.1, R1: 1, R2: 1})) > 0][0]
near(float(pos.subs({vI: -3.6, k: 0.1, R1: 1, R2: 1})), 6.0)
print("divider / sqrt ok")

# ---------------- ICL8038 ----------------
Vcc, Rr, Cc = sp.symbols("V_CC R C", positive=True)
I = sp.Rational(1, 5) * Vcc / Rr
t1 = Cc * (Vcc / 3) / I
assert sp.simplify(t1 - sp.Rational(5, 3) * Rr * Cc) == 0
f = 1 / (2 * t1)
assert sp.simplify(f - sp.Rational(3, 10) / (Rr * Cc)) == 0
near(0.3 / (10e3 * 3.3e-9), 9091, 1e-3)
near(0.33 / (10e3 * 3.3e-9), 10000, 1e-3)
print("8038 f:", 0.3 / (10e3 * 3.3e-9))

# ---------------- 开关电容 ----------------
near(1 / (1e-12 * 100e3), 10e6)
tau = 10e-12 / (1e-12 * 100e3)
near(tau, 1e-4)
near(1 / (2 * pi * tau), 1592, 1e-3)
near(100e3 / 100, 1000); near(100e3 / 50, 2000)
# 离散时间验证：每周期 C1 搬运 C1 v_I 电荷到 C2，v_O 每周期下降 (C1/C2) v_I
vo_k, C1, C2, vin = 0.0, 1e-12, 10e-12, 1.0
for _ in range(100):
    vo_k -= C1 / C2 * vin
# 100 个周期 = 1 ms，连续积分器 −v_I t/τ = −10 V
near(vo_k, -10.0, 1e-9)
print("SC ok")

# ---------------- Buck ----------------
D, Vi = sp.symbols("D V_I", positive=True)
Vo_s = sp.Symbol("V_O")
# 电感伏秒平衡
assert sp.solve(sp.Eq((Vi - Vo_s) * D, Vo_s * (1 - D)), Vo_s)[0] == D * Vi


def buck(Vi, Vo, L, fs, C, Io):
    D = Vo / Vi
    dI = Vo * (1 - D) / (L * fs)
    dV = dI / (8 * fs * C)
    return D, dI, dV, Io + dI / 2, dI / 2


near(0.25 * 12, 3.0)
D_, dI, dV, Ipk, Ib = buck(12, 3, 100e-6, 50e3, 100e-6, 1.0)
near(dI, 0.45); near(dV * 1e3, 11.25); near(Ipk, 1.225); near(Ib, 0.225); near(3 / Ib, 13.3, 5e-3)
near(3 / 12, 0.25)
print("buck ex1:", dI, dV, Ipk)
# 数值仿真（理想开关，CCM）检验 ΔI_L 与 ΔV_O
L, Cv, RLv, fsv = 100e-6, 100e-6, 3.0, 50e3
dt = 1 / fsv / 400
iL, vC = 1.0, 3.0
hist = []
for n in range(400 * 400):
    ph = (n % 400) / 400
    vx = 12.0 if ph < 0.25 else 0.0
    iL += (vx - vC) / L * dt
    vC += (iL - vC / RLv) / Cv * dt
    if n >= 400 * 390:
        hist.append((iL, vC))
h = np.array(hist)
near(h[:, 0].max() - h[:, 0].min(), 0.45, 0.03)
near((h[:, 1].max() - h[:, 1].min()) * 1e3, 11.25, 0.1)
near(h[:, 1].mean(), 3.0, 0.01)
print("   sim dI, dV:", h[:, 0].max() - h[:, 0].min(), h[:, 1].max() - h[:, 1].min())

# 设计例：24 V → 5 V，2 A，100 kHz，ΔI ≤ 0.6 A，ΔV ≤ 50 mV
Dd = 5 / 24
near(Dd, 0.208, 2e-3)
Lmin = 5 * (1 - Dd) / (100e3 * 0.6)
near(Lmin * 1e6, 66.0, 2e-3)
Cmin = 0.6 / (8 * 100e3 * 0.05)
near(Cmin * 1e6, 15)
near(5 * (1 - Dd) / (68e-6 * 100e3), 0.582, 2e-3)
print("buck design:", Lmin, Cmin)

# 练习 4：12 V → 5 V，200 kHz，22 µH，47 µF，R_L = 5 Ω
D_, dI, dV, Ipk, Ib = buck(12, 5, 22e-6, 200e3, 47e-6, 1.0)
near(D_, 0.417, 2e-3); near(dI, 0.663, 2e-3); near(dV * 1e3, 8.82, 2e-3); near(Ib, 0.331, 3e-3)
near(5 / Ib, 15.1, 3e-3); near(Ipk, 1.33, 3e-3)
print("ex buck:", D_, dI, dV, Ib)

# ---------------- PLL ----------------
near(10 * 100e3, 1e6)
near(10e6 / 400, 25e3)
near(88e6 / 25e3, 3520); near(108e6 / 25e3, 4320)
# 锁定时控制电压与相位误差
uc = (1000 - 900) / 50
near(uc, 2.0)
phi = math.degrees(math.asin(uc / (4 * 1.0)))
near(phi, 30.0)
near(900 + 50 * 4, 1100); near(900 - 50 * 4, 700)
print("PLL lock: uc, phi =", uc, phi)
# 练习 5：4 MHz 晶振，12.5 kHz 步进，430~440 MHz
near(4e6 / 12.5e3, 320)
near(430e6 / 12.5e3, 34400); near(440e6 / 12.5e3, 35200)
near(35200 - 34400 + 1, 801)

print("special: all checks passed")
