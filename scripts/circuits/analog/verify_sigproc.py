"""模电·信号运算与处理 —— 独立验算（对数/指数、精密整流、I–V/V–I、有源滤波、比较器）。

    cd scripts/circuits/analog && ../../../.venv/bin/python verify_sigproc.py
"""
import math

import numpy as np
import sympy as sp


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol * max(abs(b), 1e-30), (a, b)


VT = 0.026

# ================= 图卡例：反相积分器 RC=10 ms，1 V 持续 2 ms =================
du = -1.0 * 2e-3 / 10e-3
close(du, -0.2, 1e-12)
close(-1.0 / 10e-3 * 1e-3, -0.1, 1e-12)        # 斜率 −0.1 V/ms
print("integrator: Δuo = %.2f V" % du)

# ================= 对数 / 指数 =================
IS, R = 1e-14, 10e3
# 对数：虚地，iC = ui/R = IS e^{uBE/VT}，uo = −uBE
uo_log = lambda ui: -VT * math.log(ui / (IS * R))
close(uo_log(1.0), -0.5987, 1e-3)
dec = uo_log(10) - uo_log(1)
close(dec, -0.0599, 1e-3)
print("log: uo(1V) = %.4f V, per decade %.4f V" % (uo_log(1.0), dec))
# 用二极管方程反解验证：uBE 产生的电流确实等于 ui/R
uBE = -uo_log(1.0)
close(IS * math.exp(uBE / VT), 1.0 / R, 1e-9)
# 指数：uo = −R IS e^{ui/VT}
uo_exp = lambda u: -R * IS * math.exp(u / VT)
close(uo_exp(0.6), -1.054, 2e-3)
print("exp: uo(0.6V) = %.4f V" % uo_exp(0.6))
# 练习：ui 0.1 → 10 V
d = uo_log(10) - uo_log(0.1)
close(d, -0.1197, 1e-3)
print("ex log: Δuo = %.4f V" % d)

# ================= 精密整流 =================
A0, UD = 1e5, 0.7
close(UD / A0, 7e-6, 1e-9)


def halfwave(u):
    """半波：ui>0 时 uo1 = −ui（R1=R2），ui<0 时 uo1 = 0。"""
    return -u if u > 0 else 0.0


def fullwave(u):
    """A2 反相加法：ui 经 2R... 这里 ui 经 R，uo1 经 R/2，Rf=R → uo = −(ui + 2 uo1)。"""
    return -(u + 2 * halfwave(u))


for u in np.linspace(-1, 1, 41):
    close(fullwave(u) + 1e-30, abs(u) + 1e-30, 1e-9)
assert halfwave(-0.3) == 0 and abs(fullwave(-0.3) - 0.3) < 1e-12
assert abs(halfwave(0.5) + 0.5) < 1e-12 and abs(fullwave(0.5) - 0.5) < 1e-12
print("full-wave = |ui| ok; ex: ui=-0.3 → uo1=0, uo=0.3; ui=0.5 → uo1=-0.5, uo=0.5")

# ================= I–V / V–I =================
close(-5e-6 * 200e3, -1.0, 1e-12)
# Howland：− 端 R1 对地、R2 接输出；+ 端 R3 接 ui、R4 接输出、RL 对地
ui, uo, uL, RL = sp.symbols("u_i u_o u_L R_L", real=True)
R1 = R2 = R3 = R4 = 10e3
s = sp.solve([uL - uo * R1 / (R1 + R2),
              (ui - uL) / R3 + (uo - uL) / R4 - uL / RL], [uo, uL], dict=True)[0]
iL = sp.simplify(s[uL] / RL)
assert sp.simplify(iL - ui / R3) == 0
print("Howland: iL =", iL, "(independent of RL)")
# ui=1 V：iL = 0.1 mA，uo = 2 uL = 2 iL RL ≤ 12 → RL ≤ 60k
close(12 / (2 * 1e-4), 60e3, 1e-12)

# ================= 一阶低通（图卡例） =================
Ap = 10
mag = Ap / math.sqrt(1 + 10 ** 2)
close(mag, 0.995, 1e-3); close(mag / Ap, 0.0995, 1e-3)
print("LP1: |A|(10fc) = %.4f, ratio = %.4f (%.1f dB)" % (mag, mag / Ap, 20 * math.log10(mag / Ap)))

# ================= 二阶 Sallen–Key 低通：推导传递函数 =================
s_ = sp.symbols("s")
Ra, Rb, Ca, Cb, K = sp.symbols("R_1 R_2 C_1 C_2 K", positive=True)
Vi, Va, Vp, Vo = sp.symbols("V_i V_a V_p V_o")
# Vi —R1— a —R2— p(+)；C1 由 a 接输出（反馈电容），C2 由 p 对地；Vo = K Vp
sol = sp.solve([(Vi - Va) / Ra - (Va - Vp) / Rb - (Va - Vo) * s_ * Ca,
                (Va - Vp) / Rb - Vp * s_ * Cb,
                Vo - K * Vp], [Va, Vp, Vo], dict=True)[0]
H = sp.simplify(sol[Vo] / Vi)
num, den = sp.fraction(sp.together(H))
den = sp.Poly(sp.expand(den), s_)
a2, a1, a0 = den.all_coeffs()
w0 = sp.sqrt(a0 / a2)
Q = sp.simplify(sp.sqrt(a0 * a2) / a1)
# 文中给出的一般式
Q_text = sp.sqrt(Ra * Rb * Ca * Cb) / ((Ra + Rb) * Cb + (1 - K) * Ra * Ca)
assert sp.simplify(Q - Q_text) == 0
assert sp.simplify(w0 - 1 / sp.sqrt(Ra * Rb * Ca * Cb)) == 0
assert sp.simplify(num / sp.Poly(sp.expand(sp.fraction(sp.together(H))[1]), s_).all_coeffs()[0] - K * a0 / a2) == 0
# 等 R、等 C：w0 = 1/RC，Q = 1/(3−K)
Rr, Cc = sp.symbols("R C", positive=True)
eq = {Ra: Rr, Rb: Rr, Ca: Cc, Cb: Cc}
assert sp.simplify(w0.subs(eq) - 1 / (Rr * Cc)) == 0
assert sp.simplify(Q.subs(eq) - 1 / (3 - K)) == 0
# 单位增益、等 R：Q = sqrt(C1/C2)/2
Qu = sp.simplify(Q.subs({K: 1, Ra: Rr, Rb: Rr}))
assert sp.simplify(Qu - sp.sqrt(Ca / Cb) / 2) == 0
print("Sallen-Key: equal R,C → Q = 1/(3-K); unity gain equal R → Q = sqrt(C1/C2)/2")

# Q=1/2 时 −3 dB 频率 = sqrt(sqrt2 − 1) f0
x = math.sqrt(math.sqrt(2) - 1)
close(x, 0.6436, 1e-3)
Hq = lambda w, q: 1 / (1 - w ** 2 + 1j * w / q)
close(abs(Hq(x, 0.5)), 1 / math.sqrt(2), 1e-9)
close(abs(Hq(1.0, 1 / math.sqrt(2))), 1 / math.sqrt(2), 1e-9)
# 例：R=10k, C=10nF
f0 = 1 / (2 * math.pi * 10e3 * 10e-9)
close(f0, 1591.5, 1e-4); close(x * f0, 1024, 1e-3)
Kb = 3 - math.sqrt(2)
close(Kb, 1.586, 1e-3)
print("SK example: f0 = %.1f Hz, unity fc = %.0f Hz, Butterworth K = %.3f (%.2f dB)" % (f0, x * f0, Kb, 20 * math.log10(Kb)))
# 设计：f0 = 1 kHz, C = 10 nF → R = 15.9k；Rf/R1 = 0.586
Rd = 1 / (2 * math.pi * 1e3 * 10e-9)
close(Rd, 15.92e3, 1e-3)
close(Kb - 1, 0.586, 1e-3)
# 单位增益 Butterworth：C1 = 2C2 = 20 nF，C2 = 10 nF，f0 = 1 kHz → R = 11.25k
Ru = 1 / (2 * math.pi * 1e3 * math.sqrt(20e-9 * 10e-9))
close(Ru, 11.25e3, 1e-3)
assert abs(float(Qu.subs({Ca: 20e-9, Cb: 10e-9})) - 1 / math.sqrt(2)) < 1e-12
print("design: R = %.0f Ω (K=1.586), unity-gain Butterworth R = %.0f Ω" % (Rd, Ru))
# 练习：R=22k, C=10nF
f0e = 1 / (2 * math.pi * 22e3 * 10e-9)
close(f0e, 723.4, 1e-3); close(x * f0e, 465.6, 1e-3)
print("ex SK: f0 = %.1f Hz, unity fc = %.1f Hz" % (f0e, x * f0e))
# Q=2 时峰值
qq = 2
wp = math.sqrt(1 - 1 / (2 * qq ** 2))
peak = abs(Hq(wp, qq))
close(peak, qq / math.sqrt(1 - 1 / (4 * qq ** 2)), 1e-9)
# 4 阶 Butterworth 的两节 Q
Qs = sorted(1 / (2 * math.cos(math.pi * (2 * k - 1) / 8)) for k in (1, 2))
close(Qs[0], 0.541, 1e-3); close(Qs[1], 1.307, 1e-3)
print("4th-order Butterworth Qs:", [round(q, 3) for q in Qs])

# ================= 比较器 =================
# 图卡例：反相滞回，β=0.2，±10 V
assert abs(0.2 * 10 - 2) < 1e-12
# 反相滞回带参考：UREF 经 R1 → +，RF 由输出 → +
R1, RF, UR, UZ = 10e3, 40e3, 3.0, 6.0
up = lambda uo: (RF * UR + R1 * uo) / (R1 + RF)
close(up(UZ), 3.6, 1e-12); close(up(-UZ), 1.2, 1e-12)
print("inv Schmitt with ref: UT+ = %.2f, UT- = %.2f, ΔU = %.2f" % (up(UZ), up(-UZ), up(UZ) - up(-UZ)))
# 同相滞回（练习）：ui 经 R1 → +，R2 由输出 → +，− 端接 UREF
R1, R2, UR, UZ = 10e3, 30e3, 1.0, 6.0
u = sp.symbols("u")
UTp = float(sp.solve((u * R2 + (-UZ) * R1) / (R1 + R2) - UR, u)[0])   # 输出为 −UZ 时上升门限
UTm = float(sp.solve((u * R2 + UZ * R1) / (R1 + R2) - UR, u)[0])
close(UTp, 10 / 3, 1e-9); close(UTm, -2 / 3, 1e-9)
print("non-inv Schmitt: UT+ = %.3f, UT- = %.3f, ΔU = %.2f" % (UTp, UTm, UTp - UTm))


# 数值仿真反相滞回：三角波输入，确认翻转点
def schmitt_inv(uin, UTp=2.0, UTm=-2.0, U=10.0):
    out, state = [], U
    for v in uin:
        if state > 0 and v > UTp:
            state = -U
        elif state < 0 and v < UTm:
            state = U
        out.append(state)
    return np.array(out)


tt = np.linspace(0, 2, 2001)
tri = 3 * (2 * np.abs(2 * ((tt + 0.25) % 1) - 1) - 1)    # ±3 V 三角波
o = schmitt_inv(tri)
flips = np.where(np.diff(o) != 0)[0]
for k in flips:
    assert abs(abs(tri[k + 1]) - 2) < 0.02
print("comparators: ok")
print("sigproc: all checks passed")
