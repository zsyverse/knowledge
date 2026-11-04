"""习题·动态电路 —— 独立验算。直接对换路后电路列微分方程（sympy dsolve / 状态方程）求解，
再与页面上写出的三要素结果逐项比较。"""
import sympy as sp

t = sp.symbols("t", nonnegative=True)
E = sp.exp


def same(a, b):
    assert sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0, (a, b)


def first_order(a, b, x0):
    """解 x' = a x + b, x(0)=x0。"""
    x = sp.Function("x")
    sol = sp.dsolve(sp.Eq(x(t).diff(t), a * x(t) + b), x(t), ics={x(0): x0})
    return sp.simplify(sol.rhs)


# ---- 题2：作业 7-3 ----
i0 = sp.Rational(24, 1 + 5); uC0 = 5 * i0
uL0 = 0 - uC0                    # u_L 左正右负；左端经触点 2 接地
iC0 = i0 - uC0 / 5
assert (i0, uC0, uL0, iC0) == (4, 20, -20, 0)
print("2:", i0, uC0, uL0, iC0)

# ---- 题3：RC，S 打开 ----
uC0 = sp.Rational(18 * 3, 6 + 3)          # 6 V
# 换路后：18V—6Ω—a—2Ω—C，(18-uC)/8 = C uC'
uC = first_order(-sp.Rational(1, 8) / sp.Rational(1, 2), sp.Rational(18, 8) / sp.Rational(1, 2), uC0)
same(uC, 18 - 12 * E(-t / 4))
iC = sp.Rational(1, 2) * uC.diff(t)
same(iC, sp.Rational(3, 2) * E(-t / 4))
print("3:", uC, iC)

# ---- 题4：RL，S 闭合 ----
iL0 = sp.Rational(6 * 3, 3 + 1)           # 4.5
# 换路后：a 点 KCL 6 = ua/3 + ua/6 + iL，ua = 1*iL + 2 iL'
# => ua = 2(6 - iL) ; 2 iL' = 2(6-iL) - iL  => iL' = 6 - 1.5 iL
iL = first_order(-sp.Rational(3, 2), 6, iL0)
same(iL, 4 + sp.Rational(1, 2) * E(-sp.Rational(3, 2) * t))
ua = 1 * iL + 2 * iL.diff(t)
same(ua, 4 - E(-sp.Rational(3, 2) * t))
ua0m = 3 * (6 - iL0)
assert ua0m == sp.Rational(9, 2) and ua.subs(t, 0) == 3
print("4:", iL, ua, "ua(0-)=", ua0m)

# ---- 题5：作业 7-4 ----
Is, L1, L2, R = 6, 1, 2, 1
i1, i2 = sp.Function("i1"), sp.Function("i2")
# 并联电压 u = R (Is - i1 - i2) = L1 i1' = L2 i2'
sol = sp.dsolve([sp.Eq(i1(t).diff(t), R * (Is - i1(t) - i2(t)) / L1),
                 sp.Eq(i2(t).diff(t), R * (Is - i1(t) - i2(t)) / L2)], [i1(t), i2(t)],
                ics={i1(0): 1, i2(0): 2})
I1, I2 = [sp.simplify(s.rhs) for s in sol]
same(I2, 3 - E(-sp.Rational(3, 2) * t))
same(I1, 3 - 2 * E(-sp.Rational(3, 2) * t))
assert sp.limit(I2, t, sp.oo) == 3 and sp.limit(I1, t, sp.oo) == 3
print("5:", I1, I2)

# ---- 题6：作业 7-5 ----
C1, C2, R1, R2, Us = 1, 2, 1, 2, 9
a, b = sp.symbols("a b")
s0 = sp.solve([a + b - Us, -C1 * a + C2 * b - (-C1 * 9 + C2 * 9)], [a, b])
assert (s0[a], s0[b]) == (3, 6)
# 换路后中点 m：(9-Vm)/R1 + C1 d(9-Vm)/dt = Vm/R2 + C2 dVm/dt
Vm = first_order(-(sp.Rational(1, R1) + sp.Rational(1, R2)) / (C1 + C2), sp.Rational(Us, R1) / (C1 + C2), 6)
same(Vm, 6)
print("6:", s0, "uC2(t)=", Vm)

# ---- 题7：作业 7-10 ----
u = sp.Function("u")
def ss(beta):  # (2-β)u' + (3-β)u = 1 的稳态
    return sp.Rational(1) / (3 - beta)
u0 = ss(sp.Rational(1, 2))
beta = sp.Rational(3, 2)
# 独立推导：右节点 i = u + u'；左节点电压 V1 = u + i；左竖支路电流 (V1 - β i)/1；Is = 左竖 + i
uu = sp.Function("uu")
i_expr = uu(t) + uu(t).diff(t)
V1 = uu(t) + i_expr
eq = sp.Eq(1, (V1 - beta * i_expr) + i_expr)
sol = sp.dsolve(eq, uu(t), ics={uu(0): u0})
same(sol.rhs, sp.Rational(2, 3) - sp.Rational(4, 15) * E(-3 * t))
assert u0 == sp.Rational(2, 5)
print("7:", u0, sol.rhs)

# ---- 题8：作业 7-12 ----
R1, R2, r, C1, C2, us = 20, 10, 20, sp.Rational(1, 10), sp.Rational(1, 10), 12
i10 = sp.Rational(us, R1 + r); uC10 = r * i10
assert (i10, uC10) == (sp.Rational(3, 10), 6)
uC1 = first_order(-1 / (R1 * C1), us / (R1 * C1), uC10)
i1t = (us - uC1) / R1
vB = r * i1t
uc2 = sp.Function("uc2")
uC2 = sp.dsolve(sp.Eq(uc2(t).diff(t), (vB - uc2(t)) / (R2 * C2)), uc2(t), ics={uc2(0): uC10}).rhs
u0 = sp.simplify(uC1 - vB)
same(uC1, 12 - 6 * E(-t / 2)); same(i1t, sp.Rational(3, 10) * E(-t / 2))
same(u0, 12 - 12 * E(-t / 2)); same(uC2, 12 * E(-t / 2) - 6 * E(-t))
print("8:", u0, sp.simplify(uC2))

# ---- 题9：作业 7-28 ----
R, Us, C, L, beta = 10, 12, sp.Rational(1, 100), sp.Rational(1, 5), sp.Rational(1, 3)
i_, uc_ = sp.symbols("i_ uc_")
st = sp.solve([sp.Eq(i_, (Us - uc_) / R), sp.Eq(i_ - beta * i_, uc_ / R)], [i_, uc_])
iL0 = st[i_] - beta * st[i_]
assert (st[uc_], st[i_], iL0) == (sp.Rational(24, 5), sp.Rational(18, 25), sp.Rational(12, 25))
uCt = first_order(-1 / (R * C), Us / (R * C), st[uc_])
it = (Us - uCt) / R
iLf = sp.Function("iLf")
# 右节点 D：流入 -βi = iL + uL/R，uL = L iL'
iLt = sp.dsolve(sp.Eq(-beta * it, iLf(t) + L * iLf(t).diff(t) / R), iLf(t), ics={iLf(0): iL0}).rhs
uL = L * iLt.diff(t)
vB = uL + R * (-beta * it)       # B 点电位 = D 点电位 + R 上压降（B→D 电流 -βi）
uk = sp.simplify(uCt - vB)
same(uCt, 12 - sp.Rational(36, 5) * E(-10 * t))
same(it, sp.Rational(18, 25) * E(-10 * t))
same(iLt, sp.Rational(39, 50) * E(-50 * t) - sp.Rational(3, 10) * E(-10 * t))
same(uk, 12 - sp.Rational(27, 5) * E(-10 * t) + sp.Rational(39, 5) * E(-50 * t))
assert uk.subs(t, 0) == sp.Rational(72, 5)
print("9:", sp.expand(iLt), sp.expand(uk))

# ---- 题10：二阶 RLC ----
R, L, C = 6, sp.Rational(1, 2), sp.Rational(1, 50)
Rc = 2 * sp.sqrt(L / C)
assert Rc == 10
x = sp.Function("x")
sol = sp.dsolve(sp.Eq(L * C * x(t).diff(t, 2) + R * C * x(t).diff(t) + x(t), 0), x(t),
                ics={x(0): 10, x(t).diff(t).subs(t, 0): 0})
same(sp.expand(sol.rhs), sp.expand(E(-6 * t) * (10 * sp.cos(8 * t) + sp.Rational(15, 2) * sp.sin(8 * t))))
iC = C * sol.rhs.diff(t)   # 电容电流（u_C 关联方向，即流入 + 极板）
i = -iC                    # 图中 i 从 + 极板流出
same(sp.simplify(i), sp.Rational(5, 2) * E(-6 * t) * sp.sin(8 * t))
print("10:", sp.simplify(sol.rhs), sp.simplify(i))
print("all ok")
