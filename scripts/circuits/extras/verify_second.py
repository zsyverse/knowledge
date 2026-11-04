"""拓展·二阶电路与卷积积分 —— 独立验算（dsolve + 拉氏变换 + 数值卷积）。"""
import numpy as np
import sympy as sp

t = sp.symbols("t", positive=True)
tau = sp.symbols("tau", positive=True)
s = sp.symbols("s")
E = sp.exp


def same(a, b):
    assert sp.simplify(sp.expand(sp.nsimplify(a) - sp.nsimplify(b))) == 0, (a, b)


def rlc_series(R, L, C, U, u0, i0):
    """LC u'' + RC u' + u = U，u(0)=u0，u'(0)=i0/C。"""
    u = sp.Function("u")
    sol = sp.dsolve(L * C * u(t).diff(t, 2) + R * C * u(t).diff(t) + u(t) - U, u(t),
                    ics={u(0): u0, u(t).diff(t).subs(t, 0): sp.nsimplify(i0 / C)})
    return sp.simplify(sol.rhs)


# ---- 例 1：临界阻尼阶跃 R=4, L=1, C=1/4, U=10 ----
uC = rlc_series(4, 1, sp.Rational(1, 4), 10, 0, 0)
same(uC, 10 - 10 * (1 + 2 * t) * E(-2 * t))
i = sp.Rational(1, 4) * uC.diff(t)
same(i, 10 * t * E(-2 * t))
assert sp.solve(i.diff(t), t) == [sp.Rational(1, 2)]
assert abs(float(i.subs(t, sp.Rational(1, 2))) - 5 / np.e) < 1e-12
print("ex1:", uC, i, 5 / np.e)

# ---- 例 2：GCL 并联，R=0.5, L=0.2, C=1, Is=1（阶跃，零状态），求 iL ----
iL = sp.Function("iL")
# LC iL'' + (L/R) iL' + iL = Is
sol = sp.dsolve(sp.Rational(1, 5) * iL(t).diff(t, 2) + sp.Rational(2, 5) * iL(t).diff(t) + iL(t) - 1, iL(t),
                ics={iL(0): 0, iL(t).diff(t).subs(t, 0): 0})
same(sol.rhs, 1 - E(-t) * (sp.cos(2 * t) + sp.sin(2 * t) / 2))
# 电压 u = L iL'
same(sp.Rational(1, 5) * sol.rhs.diff(t), sp.Rational(1, 2) * E(-t) * sp.sin(2 * t))
# 临界电阻 R = 1/2 sqrt(L/C)
assert sp.Rational(1, 2) * sp.sqrt(sp.Rational(1, 5)) < sp.Rational(1, 2)
print("ex2 ok")

# ---- 卷积例：h = e^{-t}，e = ε(t) − ε(t−1) ----
r1 = sp.integrate(E(-(t - tau)), (tau, 0, t))                   # 0<t<1
same(r1, 1 - E(-t))
r2 = sp.integrate(E(-(t - tau)), (tau, 0, 1))                   # t>1
same(r2, (sp.E - 1) * E(-t))
# 数值卷积核对
dt = 1e-4
tt = np.arange(0, 4, dt)
ee = ((tt >= 0) & (tt < 1)).astype(float)
hh = np.exp(-tt)
rr = np.convolve(ee, hh)[:len(tt)] * dt
for tv in (0.5, 1.0, 2.0, 3.0):
    k = int(round(tv / dt))
    ex = 1 - np.exp(-tv) if tv <= 1 else (np.e - 1) * np.exp(-tv)
    assert abs(rr[k] - ex) < 2e-3, (tv, rr[k], ex)
print("conv pulse ok; r(1) =", 1 - np.exp(-1))

# ================= 练习 =================
# 2. R=6, L=1, C=0.04，U=10，零状态
uC = rlc_series(6, 1, sp.Rational(1, 25), 10, 0, 0)
same(uC, 10 - 10 * E(-3 * t) * (sp.cos(4 * t) + sp.Rational(3, 4) * sp.sin(4 * t)))
i = sp.Rational(1, 25) * uC.diff(t)
same(i, sp.Rational(5, 2) * E(-3 * t) * sp.sin(4 * t))
tp = sp.pi / 4
same(uC.subs(t, tp), 10 + 10 * E(-3 * sp.pi / 4))
print("x2: peak", float(uC.subs(t, tp)), "overshoot %", float(100 * E(-3 * sp.pi / 4)))

# 3. GCL：L=1, C=0.25，临界 R = 0.5 sqrt(L/C) = 1；R=2 时 α = 1/(2RC)=1，ω0=2 → 欠阻尼 −1±j√3
assert sp.Rational(1, 2) * sp.sqrt(1 / sp.Rational(1, 4)) == 1
roots = sp.solve(s**2 + s / (2 * sp.Rational(1, 4)) + 1 / sp.Rational(1, 4), s)
assert set(roots) == {-1 - sp.sqrt(3) * sp.I, -1 + sp.sqrt(3) * sp.I}
# R = 0.4：α = 1/(2*0.4*0.25) = 5 → s = −5 ± sqrt(25−4) = −5 ± √21 → 过阻尼
roots = sp.solve(s**2 + s / (sp.Rational(2, 5) * sp.Rational(1, 4)) + 4, s)
assert set(roots) == {-5 - sp.sqrt(21), -5 + sp.sqrt(21)}
print("x3 ok")

# 4. 卷积：e = t ε(t)，h = e^{-t}
r = sp.integrate(tau * E(-(t - tau)), (tau, 0, t))
same(r, t - 1 + E(-t))
same(sp.inverse_laplace_transform(1 / (s**2 * (s + 1)), s, t), t - 1 + E(-t))
print("x4 ok")

# 5. R=3, L=1, C=0.5, U=6, uC(0+)=2, i(0+)=1
uC = rlc_series(3, 1, sp.Rational(1, 2), 6, 2, 1)
same(uC, 6 - 6 * E(-t) + 2 * E(-2 * t))
i = sp.Rational(1, 2) * uC.diff(t)
same(i, 3 * E(-t) - 2 * E(-2 * t))
print("x5 ok")
print("all ok")
