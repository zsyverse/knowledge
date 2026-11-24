"""模电·负反馈放大电路 —— 独立验算（框图公式、四种组态的有限增益节点方程、稳定性）。

    cd scripts/circuits/analog && ../../../.venv/bin/python verify_feedback.py
"""
import math

import numpy as np
import sympy as sp


def close(a, b, tol=1e-3, rel=True):
    err = abs(a - b) / (abs(b) if rel and b != 0 else 1)
    assert err < tol, (a, b)


# ================= 图卡例：A=1000, F=0.1 =================
A, F = 1000, 0.1
Af = A / (1 + A * F)
close(Af, 9.90, 1e-3)
print("card: Af =", round(Af, 4), " 1/F =", 1 / F, " err% =", round((1 / F - Af) / (1 / F) * 100, 2))
# A 降 20%：精确相对变化 = (ΔA/A1)/(1+A2 F)
Af2 = 800 / (1 + 800 * F)
rel = (Af2 - Af) / Af
close(rel, -0.2 / (1 + 800 * F), 1e-9)
close(rel * 100, -0.247, 2e-3)
print("A 1000→800: Af", round(Af, 4), "→", round(Af2, 4), "rel %", round(rel * 100, 3), " 微分估算 %", round(-20 / 101, 3))

# ================= 四种组态：有限 A 的节点方程（A→∞ 时趋于 1/F） =================
Ao = sp.symbols("A", positive=True)
up, un, uo, ui, x = sp.symbols("u_p u_n u_o u_i x")

# 1) 电压串联：同相放大 R1=10k, Rf=90k
R1, Rf = 10e3, 90e3
s = sp.solve([uo - Ao * (ui - un), un - uo * R1 / (R1 + Rf)], [uo, un], dict=True)[0]
g = sp.simplify(s[uo] / ui)
assert sp.limit(g, Ao, sp.oo) == 10
close(float(g.subs(Ao, 1e5)), 10 / (1 + 1e-4), 1e-9)
print("电压串联: Auf → 10, at A=1e5:", float(g.subs(Ao, 1e5)))

# 2) 电压并联：反相放大 R1=10k, Rf=100k；Arf = uo/ii → −Rf
R1, Rf = 10e3, 100e3
s = sp.solve([(ui - un) / R1 - (un - uo) / Rf, uo + Ao * un], [uo, un], dict=True)[0]
Aus = sp.limit(s[uo] / ui, Ao, sp.oo)
assert Aus == -10
ii = (ui - s[un]) / R1
Arf = sp.limit(sp.simplify(s[uo] / ii), Ao, sp.oo)
assert abs(float(Arf) + 100e3) < 1e-6
print("电压并联: Ausf → -10, Arf → -100 kΩ (F = -1/Rf = -0.01 mS)")

# 3) 电流串联：负载 RL 跨接在输出与 − 端之间，R=1k 接地；io = ui/R
R, RL = 1e3, 1e3
s = sp.solve([uo - Ao * (ui - un), (uo - un) / RL - un / R], [uo, un], dict=True)[0]
io = (s[uo] - s[un]) / RL
assert abs(float(sp.limit(io / ui, Ao, sp.oo)) - 1e-3) < 1e-12
close(float((io / ui).subs(Ao, 1e5)) * 2, 2e-3, 1e-4)
print("电流串联: io/ui → 1 mS, ui=2V → io = 2 mA")
# 练习 3：Usat=12 V 时 RL_max = 12/2mA - 1k = 5k
assert abs(12 / 2e-3 - 1e3 - 5e3) < 1e-9

# 4) 电流并联：us 经 R1=10k 进 − 端（虚地）；RF=90k 由 − 端到 M；R=10k 由 M 到地；RL=1k 由输出到 M
R1, RF, R, RL = 10e3, 90e3, 10e3, 1e3
uM = sp.symbols("u_M")
us = sp.symbols("u_s")
s = sp.solve([(us - un) / R1 - (un - uM) / RF,             # − 端 KCL（虚断）
              (un - uM) / RF + (uo - uM) / RL - uM / R,    # M 点 KCL
              uo + Ao * un], [uo, un, uM], dict=True)[0]
io = (s[uo] - s[uM]) / RL          # 由输出流向 M
ii = (us - s[un]) / R1
Aif = sp.limit(sp.simplify(io / ii), Ao, sp.oo)
assert abs(float(Aif) + 10) < 1e-9
assert abs(float(sp.limit(io, Ao, sp.oo).subs(us, 1)) + 1e-3) < 1e-12
print("电流并联: Aif → -(1+RF/R) = -10; us=1V → ii=0.1 mA, io=-1 mA; |F| =", R / (R + RF))

# ================= 例：电压串联负反馈的 Rif、Rof =================
Rid, Ro, A0 = 2e6, 75.0, 1e5
R1, Rf = 1e3, 99e3
Fv = R1 / (R1 + Rf)
D = 1 + A0 * Fv
print("Rif≈(1+AF)Rid =", D * Rid, " Rof≈Ro/(1+AF) =", Ro / D)
# 精确：运放模型 = 差模电阻 Rid + 受控源 A·ud 串 Ro
# 输入电阻：在 + 端加 ui，求 ii
ud, ii_, uo_ = sp.symbols("u_d i_i u_o")
un_ = ui - ud
eqs = [ud / Rid - ii_,                                      # 输入电流流过 Rid
       ii_ + (uo_ - un_) / Rf - un_ / R1,                   # − 端 KCL
       (A0 * ud - uo_) / Ro - (uo_ - un_) / Rf]             # 输出端（空载）KCL
s = sp.solve(eqs, [ud, ii_, uo_], dict=True)[0]
Rif = float(ui / s[ii_])
close(Rif, D * Rid, 0.02)
# 输出电阻：ui=0，在输出端加 ut，求 it
ut, it = sp.symbols("u_t i_t")
un2 = sp.symbols("u_n2")
eqs = [(-un2) / Rid + (ut - un2) / Rf - un2 / R1,           # − 端 KCL（+ 端接地，Rid 跨接）
       it - (ut - A0 * (0 - un2)) / Ro - (ut - un2) / Rf]
s = sp.solve(eqs, [un2, it], dict=True)[0]
Rof = float(ut / s[it])
close(Rof, Ro / D, 0.02)
print("exact Rif = %.4g Ω, Rof = %.4g Ω" % (Rif, Rof))

# ================= 例：带宽展宽 =================
A0, fH, F = 1e5, 10.0, 0.01
Af0 = A0 / (1 + A0 * F)
fHf = fH * (1 + A0 * F)
close(Af0, 99.9, 1e-3); close(fHf, 10.01e3, 1e-6)
assert abs(Af0 * fHf - A0 * fH) < 1e-6
print("bandwidth: Af =", Af0, " fHf =", fHf, " GBW =", A0 * fH)

# ================= 例：三个相同极点的稳定性 =================
A0, fp = 1e4, 1e6
Aj = lambda f: A0 / (1 + 1j * f / fp) ** 3
f180 = math.sqrt(3) * fp
assert abs(math.degrees(np.angle(Aj(f180))) - (-180)) < 1e-6 or abs(math.degrees(np.angle(Aj(f180))) - 180) < 1e-6
close(abs(Aj(f180)), 1250, 1e-9)
print("f180 =", f180, " |A(f180)| =", abs(Aj(f180)), "=", 20 * math.log10(1250), "dB")
assert abs(1e4 / 8 - 1250) < 1e-9 and abs(1 / 1250 - 8e-4) < 1e-15
# F=0.01：|T(f180)| = 12.5 > 1 → 不稳定
close(abs(Aj(f180)) * 0.01, 12.5, 1e-9)
# F=2e-4：PM 与 GM
F = 2e-4
xc = math.sqrt(2 ** (2 / 3) - 1)
close(abs(Aj(xc * fp)) * F, 1.0, 1e-9)
PM = 180 - 3 * math.degrees(math.atan(xc))
GM = 20 * math.log10(1 / (abs(Aj(f180)) * F))
close(xc, 0.766, 1e-3); close(PM, 67.6, 2e-3); close(GM, 12.04, 1e-3)
close(A0 / (1 + A0 * F), 3333.3, 1e-4)
print("F=2e-4: fc = %.3f MHz, PM = %.2f°, GM = %.2f dB, Af = %.1f" % (xc, PM, GM, A0 / (1 + A0 * F)))
# GM ≥ 10 dB 的最大 F
Fmax = 1 / (1250 * 10 ** 0.5)
close(Fmax, 2.53e-4, 2e-3)
print("GM>=10dB: F <= %.3g, Af >= %.0f" % (Fmax, A0 / (1 + A0 * Fmax)))

# ================= 例：主极点补偿 =================
A0 = 1e4
poles = [1e6, 10e6, 100e6]


def T(f, ps, F=1.0):
    v = A0 * F
    for p in ps:
        v = v / (1 + 1j * f / p)
    return v


def crossover(ps, F=1.0):
    lo, hi = 1.0, 1e10
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if abs(T(mid, ps, F)) > 1:
            lo = mid
        else:
            hi = mid
    return lo


def pm(ps, F=1.0):
    fc = crossover(ps, F)
    ph = -sum(math.degrees(math.atan(fc / p)) for p in ps)
    return fc, 180 + ph


fc0, pm0 = pm(poles)
print("uncompensated follower: fc = %.3g Hz, PM = %.1f°" % (fc0, pm0))
assert pm0 < 0
close(fc0, 208e6, 0.01); close(pm0 - 180, -241.3, 1e-3)
# 把第一个极点压到 f_p2 / A0 = 1 kHz（米勒补偿的极点分离效果）
p1n = poles[1] / A0
assert p1n == 1e3
fc1, pm1 = pm([p1n, poles[1], poles[2]])
print("compensated (p1→1 kHz): fc = %.3g Hz, PM = %.1f°" % (fc1, pm1))
close(fc1 / 1e6, 7.8, 0.02)
close(pm1, 47.6, 0.02)
# 开环 -3 dB 带宽变为 1 kHz，单位增益带宽 ≈ 7.8 MHz

# ================= 例：发射极电阻引入的电流串联负反馈 =================
beta, rbe, RC, RL, RE = 100, 1.5e3, 4e3, 4e3, 0.5e3
RLp = RC * RL / (RC + RL)
Au = -beta * RLp / (rbe + (1 + beta) * RE)
close(Au, -3.846, 1e-3)
print("CE with RE: exact Au = %.3f, deep-feedback estimate = %.1f" % (Au, -RLp / RE))

# ================= 例：两级运放级间电压并联负反馈 =================
# A1 反相端：ui 经 R1=10k，uo 经 RF=100k；A1 开环（+ 端接地）；A2 同相放大 1+R4/R3 = 2
A1 = sp.symbols("A_1", positive=True)
n, o1, o = sp.symbols("n o1 o")
R1, RF = 10e3, 100e3
s = sp.solve([(ui - n) / R1 + (o - n) / RF,          # A1 反相端 KCL（虚断）
              o1 + A1 * n,                            # A1：o1 = A1(0 − n)
              o - 2 * o1], [n, o1, o], dict=True)[0]          # A2 同相放大（理想），增益 2
g2 = sp.simplify(s[o] / ui)
assert sp.limit(g2, A1, sp.oo) == -10
print("two-stage global feedback: Ausf → -RF/R1 = -10; at A1=1e5:", float(g2.subs(A1, 1e5)))
# A2 改为反相（增益 −2）时：环路变为正反馈——闭环表达式的分母出现 1 − ...
s = sp.solve([(ui - n) / R1 + (o - n) / RF, o1 + A1 * n, o + 2 * o1], [n, o1, o], dict=True)[0]
den = sp.fraction(sp.together(s[o] / ui))[1]
print("A2 inverting: denominator", sp.factor(den), "(changes sign at finite A1 → positive feedback)")
assert sp.solve(den, A1)[0] > 0

# ================= 练习 2 =================
# Af=20，A 变化 10% 时 Af 变化 ≤ 0.1%：1+AF ≥ 100 → A = 20*100 = 2000，F = 99/2000
A_ = 20 * 100
F_ = 99 / A_
close(A_ / (1 + A_ * F_), 20, 1e-12)
close(F_, 0.0495, 1e-12)
worst = (1800 / (1 + 1800 * F_) - 20) / 20 * 100
print("ex2: A =", A_, " F =", F_, " exact change when A→1800: %.3f %%" % worst)
close(worst, -0.111, 0.01)

# ================= 练习 5：A0=1e3、三个 1 MHz 极点、F=0.1 =================
A0 = 1e3
T180 = A0 / 8 * 0.1
close(T180, 12.5, 1e-12)
Fcrit = 8 / A0
Afmin = A0 / (1 + A0 * Fcrit)
close(Afmin, 111.1, 1e-3)
print("ex5: |T(f180)| =", T180, " F <", Fcrit, " Af >", round(Afmin, 1))
print("feedback: all checks passed")
