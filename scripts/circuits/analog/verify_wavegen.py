"""模电·波形发生电路 —— 独立验算（文氏桥、LC 三点式、石英晶体、方波/三角波、VCO、CMOS 多谐）。

    cd scripts/circuits/analog && ../../../.venv/bin/python verify_wavegen.py
"""
import math

import numpy as np
import sympy as sp


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol * max(abs(b), 1e-30), (a, b)


# ================= 文氏桥反馈系数 =================
w, R, C = sp.symbols("omega R C", positive=True)
Z1 = R + 1 / (sp.I * w * C)
Z2 = 1 / (1 / R + sp.I * w * C)
Fw = sp.simplify(Z2 / (Z1 + Z2))
target = 1 / (3 + sp.I * (w * R * C - 1 / (w * R * C)))
assert sp.simplify(Fw - target) == 0
assert sp.simplify(Fw.subs(w, 1 / (R * C)) - sp.Rational(1, 3)) == 0
print("Wien: F(jω) = 1/(3 + j(ωRC − 1/ωRC)), F(ω0) = 1/3")

# 图卡例
f0 = 1 / (2 * math.pi * 10e3 * 10e-9)
close(f0, 1591.5, 1e-4)
assert 1 + 20 / 10 == 3
A = 1 + 22 / 10
close(A, 3.2, 1e-12); close(A / 3, 1.0667, 1e-4)
print("card: f0 = %.1f Hz, A(22k) = %.1f, AF = %.4f" % (f0, A, A / 3))
# 可调：R 1k~10k，C = 0.1 µF
lo, hi = 1 / (2 * math.pi * 10e3 * 0.1e-6), 1 / (2 * math.pi * 1e3 * 0.1e-6)
close(lo, 159.15, 1e-4); close(hi, 1591.5, 1e-4)
print("tunable: %.2f Hz ~ %.1f Hz" % (lo, hi))
# 偏离 ω0 时相移（ω = 2ω0）
ph = math.degrees(np.angle(1 / (3 + 1j * (2 - 0.5))))
close(ph, -26.57, 1e-3)
close(abs(1 / (3 + 1j * 1.5)), 0.298, 2e-3)
# 练习：f0=1 kHz，C=0.01 µF → R = 15.9k
Rw = 1 / (2 * math.pi * 1e3 * 0.01e-6)
close(Rw, 15.92e3, 1e-3)
close(1 / (2 * math.pi * 16e3 * 0.01e-6), 994.7, 1e-3)    # 取标称 16k
print("ex Wien: R = %.0f Ω" % Rw)

# 二极管稳幅例：Rg=10k，Rf1=15k，Rf2=10k（并二极管）
A_small = 1 + (15 + 10) / 10
A_big = 1 + 15 / 10
close(A_small, 3.5, 1e-12); close(A_big, 2.5, 1e-12)
print("diode AGC: A from %.1f (small) to %.1f (diodes fully on)" % (A_small, A_big))

# ================= 电容三点式 =================
L, C1, C2 = 50e-6, 2e-9, 2e-9
Ceq = C1 * C2 / (C1 + C2)
fc = 1 / (2 * math.pi * math.sqrt(L * Ceq))
close(Ceq, 1e-9, 1e-12); close(fc, 711.8e3, 1e-3)
print("Colpitts: Ceq = %.3g F, f0 = %.1f kHz" % (Ceq, fc / 1e3))
# 练习：L=100 µH，C1=1 nF，C2=4 nF
Ceq2 = 1e-9 * 4e-9 / 5e-9
f2 = 1 / (2 * math.pi * math.sqrt(100e-6 * Ceq2))
close(Ceq2, 0.8e-9, 1e-12); close(f2, 562.7e3, 1e-3)
print("ex Colpitts: Ceq = 0.8 nF, f0 = %.1f kHz" % (f2 / 1e3))
# 电感三点式（无互感）L1=L2=20 µH，C=1 nF
fh = 1 / (2 * math.pi * math.sqrt(40e-6 * 1e-9))
close(fh, 795.8e3, 1e-3)
print("Hartley: f0 = %.1f kHz" % (fh / 1e3))

# ================= 石英晶体 =================
Lq, Cq, Rq, C0 = 50e-3, 0.02e-12, 10.0, 5e-12
fs = 1 / (2 * math.pi * math.sqrt(Lq * Cq))
fp = fs * math.sqrt(1 + Cq / C0)
close(fs, 5.033e6, 1e-3)
close(fp - fs, 10.05e3, 2e-3)
close(fs * Cq / (2 * C0), 10.07e3, 2e-3)
Qx = 2 * math.pi * fs * Lq / Rq
close(Qx, 1.58e5, 2e-3)
# 精确并联谐振（阻抗最大）位置与近似式一致
f = np.linspace(fs - 5e3, fp + 5e3, 200001)
Zs = Rq + 1j * 2 * np.pi * f * Lq + 1 / (1j * 2 * np.pi * f * Cq)
Zc0 = 1 / (1j * 2 * np.pi * f * C0)
Z = Zs * Zc0 / (Zs + Zc0)
close(f[np.argmax(abs(Z))], fp, 1e-6)
close(f[np.argmin(abs(Z))], fs, 1e-6)
# fs < f < fp 时呈感性
mid = (fs + fp) / 2
k = np.argmin(abs(f - mid))
assert Z[k].imag > 0
print("crystal: fs = %.4f MHz, fp - fs = %.2f kHz, Q = %.3g" % (fs / 1e6, (fp - fs) / 1e3, Qx))

# ================= RC 方波发生器 =================
# 反相滞回 F = R2/(R1+R2)，T = 2RC ln((1+F)/(1−F)) = 2RC ln(1+2R2/R1)
Rr, Cc = 10e3, 0.1e-6
Fh = 0.5
T = 2 * Rr * Cc * math.log((1 + Fh) / (1 - Fh))
close(T, 2.197e-3, 1e-3); close(1 / T, 455.1, 1e-3)
assert abs(math.log((1 + Fh) / (1 - Fh)) - math.log(1 + 2 * 1)) < 1e-12
# 数值积分检查：电容从 −F UZ 向 +UZ 充电到 +F UZ 所需时间
UZ = 6.0
uc, t, dt = -Fh * UZ, 0.0, 1e-8
while uc < Fh * UZ:
    uc += (UZ - uc) / (Rr * Cc) * dt
    t += dt
close(2 * t, T, 1e-3)
print("square: T = %.4g s, f = %.1f Hz" % (T, 1 / T))

# ================= 方波–三角波 =================
# 图卡例：斜率 2 V/ms，UT = 1 V
th = 2 * 1 / 2e3
close(th, 1e-3, 1e-12); close(1 / (2 * th), 500, 1e-12)
# 本文例：UZ=6，R1=10k，R2=20k，R=10k，C=0.05 µF
UZ, R1, R2, R, C = 6.0, 10e3, 20e3, 10e3, 0.05e-6
UT = R1 / R2 * UZ
slope = UZ / (R * C)
th = 2 * UT / slope
close(UT, 3, 1e-12); close(slope, 12e3, 1e-12); close(th, 0.5e-3, 1e-12)
close(4 * R1 * R * C / R2, 1e-3, 1e-12)
print("sq-tri: UT = %g V, slope = %g V/ms, f = %g Hz" % (UT, slope / 1e3, 1 / (2 * th)))


# 仿真：同相滞回（R1 接三角波输出，R2 接方波输出，− 端接地）+ 反相积分器
def simulate(T_end=4e-3, dt=1e-7):
    usq, utri = UZ, 0.0
    ts, sq, tr = [], [], []
    t = 0.0
    while t < T_end:
        utri += -usq / (R * C) * dt
        up = (utri * R2 + usq * R1) / (R1 + R2)
        usq = UZ if up > 0 else -UZ
        ts.append(t); sq.append(usq); tr.append(utri)
        t += dt
    return np.array(ts), np.array(sq), np.array(tr)


ts, sq, tr = simulate()
steady = ts > 1.5e-3
close(tr[steady].max(), UT, 1e-2); close(tr[steady].min(), -UT, 1e-2)
edges = ts[1:][np.diff(sq) > 0]
period = np.diff(edges).mean()
close(period, 1e-3, 1e-3)
# 方波为 +UZ 时三角波下降（反相积分）
k = np.where(steady & (sq > 0))[0][5]
assert tr[k + 1] < tr[k]
print("simulated: period = %.4g s, triangle peak = %.3f V" % (period, tr[steady].max()))

# ================= VCO =================
kf = 1 / (4 * UT * R * C)
close(kf, 166.7, 1e-3)
close(1 * kf, 166.7, 1e-3); close(10 * kf, 1667, 1e-3)
print("VCO: f = %.1f Hz/V × uC" % kf)
# 练习：要 1 kHz/V，UT=3 V，C=0.05 µF → R = 1/(4·3·0.05e-6·1000)
Rv = 1 / (4 * 3 * 0.05e-6 * 1000)
close(Rv, 1667, 1e-3)

# ================= 锯齿波：充放电电阻不同 =================
# 正向积分用 Ra，反向用 Rb（二极管选通），UT=3V，UZ=6V，C=0.05µF，Ra=1k，Rb=10k
Ra, Rb = 1e3, 10e3
t1 = 2 * UT * Ra * C / UZ
t2 = 2 * UT * Rb * C / UZ
close(UZ / (Ra * C), 120e3, 1e-12); close(UZ / (Rb * C), 12e3, 1e-12)
close(t1, 0.05e-3, 1e-12); close(t2, 0.5e-3, 1e-12)
close(1 / (t1 + t2), 1818, 1e-3)
close(t1 / (t1 + t2), 1 / 11, 1e-12)
print("sawtooth: t1 = %.3g, t2 = %.3g, f = %.0f Hz" % (t1, t2, 1 / (t1 + t2)))

# ================= CMOS 门多谐振荡器 =================
close(2 * math.log(3), 2.197, 1e-3)      # 无钳位
close(2 * math.log(2), 1.386, 1e-3)      # 输入保护二极管钳位
print("wavegen: all checks passed")
