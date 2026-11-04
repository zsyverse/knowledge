"""拓展·运算法 —— 独立验算：sympy 拉氏反变换 + 时域微分方程（dsolve）互相核对。"""
import sympy as sp

s = sp.symbols("s")
t = sp.symbols("t", positive=True)
ilt = lambda F: sp.simplify(sp.inverse_laplace_transform(F, s, t))
E = sp.exp


def same(a, b):
    assert sp.simplify(sp.expand(sp.nsimplify(a) - sp.nsimplify(b))) == 0, (a, b)


# ---- 变换表（抽查）----
a, w = sp.symbols("a omega", positive=True)
for f, F in [(E(-a * t), 1 / (s + a)), (t, 1 / s**2), (t * E(-a * t), 1 / (s + a)**2),
             (sp.sin(w * t), w / (s**2 + w**2)), (sp.cos(w * t), s / (s**2 + w**2)),
             (E(-a * t) * sp.sin(w * t), w / ((s + a)**2 + w**2)),
             (E(-a * t) * sp.cos(w * t), (s + a) / ((s + a)**2 + w**2))]:
    assert sp.simplify(sp.laplace_transform(f, t, s, noconds=True) - F) == 0, f

# ---- 部分分式三例 ----
same(ilt((s + 3) / ((s + 1) * (s + 2))), 2 * E(-t) - E(-2 * t))
f = ilt((s + 3) / (s**2 + 2 * s + 5))
same(f, E(-t) * (sp.cos(2 * t) + sp.sin(2 * t)))
same(f, sp.sqrt(2) * E(-t) * sp.cos(2 * t - sp.pi / 4))
p = -1 + 2 * sp.I
K = sp.simplify(((s + 3) / (s - sp.conjugate(p))).subs(s, p))
assert sp.simplify(K - (sp.Rational(1, 2) - sp.I / 2)) == 0
assert sp.simplify(sp.Abs(K) - sp.sqrt(2) / 2) == 0 and sp.simplify(sp.arg(K) + sp.pi / 4) == 0
same(ilt(1 / (s * (s + 1)**2)), 1 - E(-t) - t * E(-t))
print("partial fractions ok")

# ---- 例：RLC（S 打开后 Us=10, R1=2, L=1, C=0.2；i(0-)=2, uC(0-)=6）----
R1, R2, L, C, Us = 2, 3, 1, sp.Rational(1, 5), 10
i0 = sp.Rational(Us, R1 + R2); u0 = R2 * i0
assert (i0, u0) == (2, 6)
I = sp.solve(sp.Eq(sp.Rational(Us) / s + L * i0, (R1 + s * L + 1 / (s * C)) * sp.Symbol("I") + u0 / s), sp.Symbol("I"))[0]
same(I - (2 * s + 4) / (s**2 + 2 * s + 5), 0)
i_t = ilt(I)
same(i_t, 2 * E(-t) * (sp.cos(2 * t) + sp.sin(2 * t) / 2))
UC = I / (s * C) + u0 / s
uC_t = ilt(UC)
same(uC_t, 10 - 4 * E(-t) * sp.cos(2 * t) + 3 * E(-t) * sp.sin(2 * t))
# 时域核对：L di/dt + R1 i + uC = 10，C duC/dt = i
ii, uu = sp.Function("i"), sp.Function("u")
sol = sp.dsolve([sp.Eq(ii(t).diff(t), (10 - R1 * ii(t) - uu(t)) / L), sp.Eq(uu(t).diff(t), ii(t) / C)],
                [ii(t), uu(t)], ics={ii(0): 2, uu(0): 6})
same(sol[0].rhs, i_t); same(sol[1].rhs, uC_t)
# 部分分式手算：10(s+2)/(s(s^2+2s+5)) = 4/s + (−4s+2)/(s^2+2s+5)
assert sp.simplify(10 * (s + 2) / (s * (s**2 + 2 * s + 5)) - (4 / s + (-4 * s + 2) / (s**2 + 2 * s + 5))) == 0
print("RLC example ok:", i_t, uC_t)

# ---- 网络函数：H = UC/Us = 5/(s^2+2s+5) ----
H = (1 / (s * C)) / (R1 + s * L + 1 / (s * C))
same(sp.simplify(H) - 5 / (s**2 + 2 * s + 5), 0)
same(ilt(H), sp.Rational(5, 2) * E(-t) * sp.sin(2 * t))
same(ilt(H / s), 1 - E(-t) * (sp.cos(2 * t) + sp.sin(2 * t) / 2))
print("H ok")

# ================= 练习 =================
# 1
same(ilt((2 * s + 5) / (s**2 + 5 * s + 6)), E(-2 * t) + E(-3 * t))
same(ilt((s + 2) / (s * (s + 1)**2)), 2 - 2 * E(-t) - t * E(-t))
F3 = (s**2 + 3) / (s**2 + 2 * s + 2)
assert sp.simplify(F3 - (1 + (-2 * s + 1) / (s**2 + 2 * s + 2))) == 0
same(ilt((-2 * s + 1) / (s**2 + 2 * s + 2)), -2 * E(-t) * sp.cos(t) + 3 * E(-t) * sp.sin(t))
print("ex1 ok")

# 2. RL，us = 10 e^{-2t}（t=0 接入），R=2，L=1，零状态
I = (10 / (s + 2)) / (s + 2)
same(ilt(I), 10 * t * E(-2 * t))
sol = sp.dsolve(sp.Eq(ii(t).diff(t) + 2 * ii(t), 10 * E(-2 * t)), ii(t), ics={ii(0): 0})
same(sol.rhs, 10 * t * E(-2 * t))
same(ilt(s * I), 10 * (1 - 2 * t) * E(-2 * t))     # u_L = L di/dt（i(0)=0）
print("ex2 ok")

# 3. C=0.5 F 放电，u0=4，经 R=3、L=1，i(0-)=1（i 从 C 的 + 极板流出）
I = (4 + s) / (s**2 + 3 * s + 2)
Isym = sp.Symbol("I")
I2 = sp.solve(sp.Eq(4 / s - 2 * Isym / s, (3 + s) * Isym - 1), Isym)[0]
same(I2 - I, 0)
same(ilt(I), 3 * E(-t) - 2 * E(-2 * t))
sol = sp.dsolve([sp.Eq(ii(t).diff(t), uu(t) - 3 * ii(t)), sp.Eq(uu(t).diff(t), -2 * ii(t))], [ii(t), uu(t)],
                ics={ii(0): 1, uu(0): 4})
same(sol[0].rhs, 3 * E(-t) - 2 * E(-2 * t))
uL = ilt(s * I - 1)          # u_L = L di/dt
same(uL, -3 * E(-t) + 4 * E(-2 * t))
print("ex3 ok")

# 4. RLC：R=3, L=1, C=0.5 → H = 2/(s^2+3s+2)
H = 2 / (s**2 + 3 * s + 2)
same(ilt(H), 2 * E(-t) - 2 * E(-2 * t))
same(ilt(H / s), 1 - 2 * E(-t) + E(-2 * t))
# R=0 时 H = 2/(s^2+2)，极点 ±j√2
assert sp.solve(s**2 + 2, s) == [-sp.sqrt(2) * sp.I, sp.sqrt(2) * sp.I]
print("ex4 ok")

# 5. 两电容：C1=1 F（6 V）、C2=2 F（0）
I = sp.solve(sp.Eq(6 / s - Isym / s, Isym / (2 * s)), Isym)[0]
assert I == 4
assert sp.simplify(Isym / (2 * s)).subs(Isym, I) == 2 / s
print("ex5 ok")
print("all ok")
