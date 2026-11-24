"""模电·信号与放大器 —— 独立验算（放大器模型用节点方程/分压求解，运放用虚短虚断 + 饱和检查）。"""
import math

import sympy as sp


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol * max(1, abs(b)), (a, b)


def dB(x):
    return 20 * math.log10(abs(x))


# ================= 1. 采样与量化 =================
R = 8000 * 16 * 1
assert R == 128_000
cd = 44_100 * 16 * 2
assert cd == 1_411_200
per_min_MB = cd * 60 / 8 / 1e6
close(per_min_MB, 10.584)
cd74_MB = cd * 74 * 60 / 8 / 1e6
close(cd74_MB, 783.2, 1e-3)
print("data rate:", R, cd, per_min_MB, cd74_MB)


def alias(f, fs):
    """采样后显示的频率（折叠到 0~fs/2）。"""
    r = f % fs
    return min(r, fs - r)


assert alias(7e3, 8e3) == 1e3
close(alias(25e3, 44.1e3), 19.1e3)
assert alias(3e3, 8e3) == 3e3
print("alias:", alias(7e3, 8e3), alias(25e3, 44.1e3))

D = 5 / 2 ** 12
close(D * 1e3, 1.2207)
close(D / 2 * 1e3, 0.6104)
sqnr = 6.02 * 12 + 1.76
close(sqnr, 74.0, 1e-3)
# 6.02N+1.76 的来历：满幅正弦功率 (A²/2)，量化噪声功率 Δ²/12，Δ = 2A/2^N
N = sp.symbols("N", positive=True)
A = 1
expr = 10 * sp.log((sp.Rational(1, 2) * A**2) / ((2 * A / 2**N) ** 2 / 12), 10)
close(float(expr.subs(N, 12)), 6.0206 * 12 + 1.7609, 1e-4)
print("ADC:", D * 1e3, "mV, SQNR", sqnr)

# ================= 2. 放大器模型 =================
# 例：电压放大模型带源与负载（kΩ）
vs, vi, vo = sp.symbols("vs vi vo")
Rs, Ri, Avo, Ro, RL = 2, 8, 100, 1, 4
sol = sp.solve([(vs - vi) / Rs - vi / Ri,                    # 输入回路
                (Avo * vi - vo) / Ro - vo / RL], [vi, vo], dict=True)[0]
Avs = sol[vo] / vs
Av = sol[vo] / sol[vi]
assert Avs == 64 and Av == 80
close(dB(64), 36.12)
Ai = Av * Ri / RL          # i_o/i_i = (vo/RL)/(vi/Ri)
assert Ai == 160
Ap = Av * Ai
assert Ap == 12800
close(10 * math.log10(Ap), 41.07)
close(float(Avs) * 10e-3, 0.64)
print("loaded amp:", Avs, Av, Ai, Ap, dB(64), 10 * math.log10(Ap))

# 例：两级级联
def cascade(Rs, stages, RL):
    g = 1
    src = Rs
    for k, (Ri, A, Ro) in enumerate(stages):
        g *= Ri / (src + Ri) * A
        src = Ro
    return g * RL / (src + RL)


g12 = cascade(1, [(9, 20, 2), (8, 50, 1)], 1)
close(g12, 360)
close(dB(g12), 51.13)
g21 = cascade(1, [(8, 50, 1), (9, 20, 2)], 1)
close(g21, 266.67)
print("cascade:", g12, dB(g12), "swapped", g21)

# 四种模型互换：由电压模型 (Ri, Avo, Ro) 得到其余参数
Ri_, Avo_, Ro_, ii = sp.symbols("R_i A_vo R_o i_i", positive=True)
voc = Avo_ * ii * Ri_
isc = voc / Ro_
assert sp.simplify(voc / ii - Avo_ * Ri_) == 0          # R_m
assert sp.simplify(isc / (ii * Ri_) - Avo_ / Ro_) == 0   # G_m
assert sp.simplify(isc / ii - Avo_ * Ri_ / Ro_) == 0     # A_is

# ================= 3. dB =================
for x, v in ((math.sqrt(2), 3.01), (2, 6.02), (10, 20), (100, 40), (0.5, -6.02), (1 / math.sqrt(2), -3.01), (1000, 60)):
    close(dB(x), v, 1e-3)

# ================= 4. 运放：饱和检查 =================
# 图卡 02：同相放大 R1=10k, Rf=90k, vi=0.1 V, ±12 V 电源、设 V_OM=11 V
Av = 1 + 90 / 10
assert Av == 10
close(Av * 0.10, 1.0)
close(11 / Av, 1.1)
# 图卡 03：反相放大 Rin=10k, Rf=30k
x = sp.Symbol("x")
uo = sp.solve((sp.Rational(1, 5) - 0) / 10 + (x - 0) / 30, x)[0]
assert uo == sp.Rational(-3, 5)
# vi = 5 V，V_OM = 13 V：理想 −15 V，实际 −13 V，u− = 0.5 V
assert -3 * 5 == -15
un = sp.solve((5 - x) / 10 - (x - (-13)) / 30, x)[0]
assert un == sp.Rational(1, 2)
close(13 / 3, 4.333)
print("opamp sat:", uo, un)

# 削波：增益 −10，1.5 V 峰值，±12 V
th = math.degrees(math.asin(12 / 15))
close(th, 53.13)
frac = 2 * (180 - 2 * th) / 360
close(frac, 0.4097)
close(12 / 10, 1.2)
print("clipping:", th, frac)

# ================= 练习 =================
# 3. R_o：开路 2 V，接 3k 后 1.5 V
Ro_m = (2 / 1.5 - 1) * 3
close(Ro_m, 1.0)
# R_i：串入 10k 后输出 2 V → 1.6 V
r = sp.Symbol("r", positive=True)
Ri_m = sp.solve(sp.Eq(r / (r + 10), sp.Rational(16, 20)), r)[0]
assert Ri_m == 40
print("ex3:", Ro_m, Ri_m)

# 4. 级联 dB
tot = 20 + 26 - 6
assert tot == 40
close(10 ** (tot / 20), 100)
close(10 ** (26 / 20), 19.95)
close(5e-3 * 100, 0.5)

# 5. 同相放大 1+100/10=11，V_OM=11 V
G = 1 + 100 / 10
assert G == 11
close(G * (0.3 + 0.8), 12.1)
close(G * (0.3 - 0.8), -5.5)
close((11 - G * 0.3) / G, 0.7)
close(11 / G, 1.0)
print("ex5 ok")
print("signals: all checks passed")
