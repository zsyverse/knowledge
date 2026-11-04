"""拓展·含理想运放的电路 —— 独立验算（节点方程 + 虚短虚断，sympy 求解）。"""
import sympy as sp

t = sp.symbols("t", nonnegative=True)


def same(a, b):
    assert sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0, (a, b)


# ---- 例：有限增益的反相放大器 ----
ui, un, uo, A = sp.symbols("u_i u_n u_o A")
R1, Rf = 10e3, 100e3
sol = sp.solve([(ui - un) / R1 - (un - uo) / Rf, uo + A * un], [un, uo], dict=True)[0]
g = sp.simplify(sol[uo] / ui)
gA = float(g.subs(A, 1e5))
assert abs(gA - (-10 / (1 + 11e-5))) < 1e-12
print("finite A:", gA, "err %", (10 + gA) / 10 * 100)      # -9.99890, 0.011 %

# ---- 基本电路公式 ----
u1, u2, R1, R2, R3, Rf = sp.symbols("u1 u2 R1 R2 R3 Rf", positive=True)
# 差分：u1 经 R1 → −，Rf 反馈；u2 经 R2 → +，R3 对地
up = u2 * R3 / (R2 + R3)
uo_ = sp.solve((u1 - up) / R1 - (up - sp.Symbol("x")) / Rf, sp.Symbol("x"))[0]
same(uo_ - ((1 + Rf / R1) * R3 / (R2 + R3) * u2 - Rf / R1 * u1), 0)
same(uo_.subs(R3, Rf * R2 / R1), Rf / R1 * (u2 - u1))

# ---- 例：两级运放 ----
# A1 同相：R1=10k(− 对地)、Rf1=20k → uo1 = 3 ui1；A2：uo1 经 10k 进 −，Rf2=30k，+ 端直接接 ui2
ui1, ui2 = sp.Rational(1, 2), sp.Rational(3, 2)
uo1 = (1 + sp.Rational(20, 10)) * ui1
x = sp.Symbol("x")
uo = sp.solve((uo1 - ui2) / 10 - (ui2 - x) / 30, x)[0]
assert uo == 4 * ui2 - 9 * ui1 == sp.Rational(3, 2), uo
print("two-stage:", uo1, uo)

# ---- 例：有损积分器（R1=10k, Rf=20k ∥ C=0.1µF）----
R1, Rf, C = 10e3, 20e3, 0.1e-6
uC = sp.Function("uC")
# u− = 0；KCL：ui/R1 = uC/Rf + C uC'，uo = −uC
s = sp.dsolve(sp.Eq(1 / R1, uC(t) / Rf + C * uC(t).diff(t)), uC(t), ics={uC(0): 0})
uo_t = sp.nsimplify(-s.rhs, rational=True)
same(uo_t, -2 * (1 - sp.exp(-500 * t)))
w = 500
H = -(Rf / R1) / (1 + 1j * w * Rf * C)
import cmath, math
assert abs(abs(H) - math.sqrt(2)) < 1e-12 and abs(math.degrees(cmath.phase(H)) - 135) < 1e-9
print("lossy integ:", uo_t, abs(H), math.degrees(cmath.phase(H)))

# ================= 练习 =================
# 2. 反相加法：Rf=60k, R1=20k, R2=30k, R3=60k
u = {1: sp.Rational(1, 5), 2: sp.Rational(-1, 2), 3: sp.Integer(1)}
R = {1: 20, 2: 30, 3: 60}
uo = -60 * sum(u[k] / R[k] for k in u)
assert uo == sp.Rational(-3, 5), uo
# 系数 3、2、1；Rf 改为 120k 时保持系数：R1=40k, R2=60k, R3=120k
assert [sp.Rational(60, R[k]) for k in (1, 2, 3)] == [3, 2, 1]
assert [sp.Rational(120, r) for r in (40, 60, 120)] == [3, 2, 1]
print("ex2:", uo)

# 3. T 型反馈网络：R1=10k, R2=R3=100k, R4=10k（kΩ、mA）
um, uo, uin = sp.symbols("um uo uin")
sol = sp.solve([uin / 10 - (0 - um) / 100,                  # 虚地：流过 R1 的电流全部流过 R2
                (0 - um) / 100 - um / 10 - (um - uo) / 100], [um, uo], dict=True)[0]
assert sp.simplify(sol[uo] / uin) == -120 and sp.simplify(sol[um] / uin) == -10
print("ex3:", sol)

# 4. 负阻抗变换：R=1k(+ 与输出之间)，R1=2k(− 与输出之间)，R2=1k(− 对地)
u_ = sp.Symbol("u")
uo = u_ * (1 + sp.Rational(2, 1))
i_in = (u_ - uo) / 1          # mA（kΩ）
Rin = sp.simplify(u_ / i_in)
assert Rin == sp.Rational(-1, 2)
# 与 1 kΩ 并联：1 ∥ (−0.5) = −1 kΩ
Rp = 1 * Rin / (1 + Rin)
assert Rp == -1
# a 端加 u = 1 V 时：uo = 3 V，i = −2 mA（电流从 a 端流出）
assert (3 * 1, (1 - 3) / 1) == (3, -2)
print("ex4:", Rin, Rp)

# 5. 积分器：R=100k, C=1µF, ui=0.5 V 阶跃，Usat=±12
RC = 100e3 * 1e-6
k = 0.5 / RC                       # 5 V/s
assert abs(k - 5) < 1e-12
tsat = 12 / k
assert abs(tsat - 2.4) < 1e-12
# 若 t=1 s 时 ui 变为 −1 V：uo(1)=−5，之后斜率 +10 V/s，过零时刻
uo1 = -k * 1
t0 = 1 + (-uo1) / (1 / RC)
assert abs(uo1 + 5) < 1e-12 and abs(t0 - 1.5) < 1e-12
# t=3 s 时
uo3 = uo1 + (1 / RC) * 2
assert abs(uo3 - 15) < 1e-9     # 超过 12 → 在 t = 1 + 17/10 = 2.7 s 时正饱和
tps = 1 + (12 - uo1) / (1 / RC)
assert abs(tps - 2.7) < 1e-12
print("ex5:", k, tsat, t0, tps)
print("all ok")
