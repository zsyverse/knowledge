"""拓展·非线性电阻电路 —— 独立验算（sympy 解析解 + 数值精确解对比小信号近似）。"""
import math
import sympy as sp

u, i = sp.symbols("u i", real=True)

# ---- 例：负载线。Us=12, R1=R2=2 → Uoc=6, Req=1；非线性 i = u^2 (u>=0) ----
Uoc, Req = sp.Rational(12 * 2, 4), sp.Rational(2 * 2, 4)
assert (Uoc, Req) == (6, 1)
sol = [r for r in sp.solve(sp.Eq(u**2, (Uoc - u) / Req), u) if r >= 0]
assert sol == [2]
U0, I0 = 2, 4
R_static = sp.Rational(U0, I0); gd = 2 * U0; rd = sp.Rational(1, gd)
assert (R_static, rd) == (sp.Rational(1, 2), sp.Rational(1, 4))
# 小信号：Δus = sin t → ΔUoc = 0.5 sin t
dUoc = sp.Rational(1, 2)
du = dUoc * rd / (Req + rd); di = du / rd
assert (du, di) == (sp.Rational(1, 10), sp.Rational(2, 5))
# 精确值：峰、谷
up = (-1 + math.sqrt(1 + 4 * 6.5)) / 2; ud = (-1 + math.sqrt(1 + 4 * 5.5)) / 2
print("exact peak/trough u:", up, ud, "approx 2.1 / 1.9")
assert abs(up - 2.0981) < 1e-4 and abs(ud - 1.8979) < 1e-4
print("i exact:", up**2, ud**2, "approx 4.4 / 3.6")

# ---- 例：分段线性。u<1 时 i=0；u>=1 时 i=(u−1)/0.5；Thevenin Req=1 ----
def pwl_solve(Uoc):
    i2 = (Uoc - 1) / sp.Rational(3, 2)          # 假设第 2 段
    if i2 >= 0:
        return 1 + sp.Rational(1, 2) * i2, i2
    return Uoc, 0                                # 第 1 段：i=0，u=Uoc，需 u<1
assert pwl_solve(4) == (2, 2)
assert pwl_solve(sp.Rational(1, 2)) == (sp.Rational(1, 2), 0)
print("pwl ok")

# ================= 练习 =================
# 2. u = 2i + i^3，i=1
f = 2 * i + i**3
assert f.subs(i, 1) == 3 and f.diff(i).subs(i, 1) == 5
print("x2 ok")

# 3. R=1 串 i=u^2 → u_total = i + sqrt(i)；并 → i_total = u + u^2
x = sp.symbols("x", positive=True)
assert sp.simplify((x + sp.sqrt(x)).subs(x, 4) - 6) == 0          # i=4：1Ω 上 4 V，非线性元件 2 V
assert (2 + 2**2) == 6
print("x3 ok")

# 4. 二极管：Us=5, R=1k, Is=1e-14, UT=0.026
Us, R, Is, UT = 5.0, 1e3, 1e-14, 0.026
uk = 0.7
seq = []
for _ in range(6):
    uk = UT * math.log((Us - uk) / (R * Is) + 1)
    seq.append(uk)
print("diode iter:", [round(v, 5) for v in seq])
ud_ = seq[-1]; id_ = (Us - ud_) / R
assert abs(Is * (math.exp(ud_ / UT) - 1) - id_) < 1e-9
print("diode u=%.4f V, i=%.4f mA" % (ud_, id_ * 1e3))
assert abs(ud_ - 0.6966) < 5e-4 and abs(id_ * 1e3 - 4.303) < 2e-3
rd_d = UT / id_
print("rd = %.3f ohm" % rd_d)

# 5. Us=3 + 0.1 sin, R=1, i=2u^2
sol = [r for r in sp.solve(sp.Eq(3, u + 2 * u**2), u) if r > 0]
assert sol == [1]
gd = 4 * 1; rd = sp.Rational(1, gd)
du = sp.Rational(1, 10) * rd / (1 + rd); di = du / rd
assert (du, di) == (sp.Rational(1, 50), sp.Rational(2, 25))
upk = (-1 + math.sqrt(1 + 8 * 3.1)) / 4
print("x5 exact peak u:", upk, "approx 1.02")
assert abs(upk - 1.02) < 5e-4
print("all ok")
