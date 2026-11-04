"""拓展·特勒根定理、互易定理与对偶原理 —— 独立验算。端口电流一律从 + 端流入网络 N。"""
import sympy as sp

I1, I2, U1, U2 = sp.symbols("I1 I2 U1 U2")


def solve(Z, conds):
    eqs = [sp.Eq(U1, Z[0][0] * I1 + Z[0][1] * I2), sp.Eq(U2, Z[1][0] * I1 + Z[1][1] * I2)] + conds
    return sp.solve(eqs, [U1, U2, I1, I2], dict=True)[0]


# ---- 特勒根定理第二形式对互易网络的推论：U1Î1+U2Î2 = Û1I1+Û2I2（任意两组端接）----
z11, z12, z22 = sp.symbols("z11 z12 z22")
a = sp.symbols("a1:5"); b = sp.symbols("b1:5")
Zs = [[z11, z12], [z12, z22]]
Ia, Ib = sp.symbols("Ia1 Ia2"), sp.symbols("Ib1 Ib2")
Ua = [z11 * Ia[0] + z12 * Ia[1], z12 * Ia[0] + z22 * Ia[1]]
Ub = [z11 * Ib[0] + z12 * Ib[1], z12 * Ib[0] + z22 * Ib[1]]
assert sp.expand(Ua[0] * Ib[0] + Ua[1] * Ib[1] - Ub[0] * Ia[0] - Ub[1] * Ia[1]) == 0
# 三种互易形式
us, is_ = sp.symbols("u_s i_s")
# 形式一
sa = solve(Zs, [sp.Eq(U1, us), sp.Eq(U2, 0)]); sb = solve(Zs, [sp.Eq(U1, 0), sp.Eq(U2, us)])
assert sp.simplify(sa[I2] - sb[I1]) == 0
# 形式二
sa = solve(Zs, [sp.Eq(I1, is_), sp.Eq(I2, 0)]); sb = solve(Zs, [sp.Eq(I1, 0), sp.Eq(I2, is_)])
assert sp.simplify(sa[U2] - sb[U1]) == 0
# 形式三：1 端加电流源 is、2 端短路测 I2；2 端加电压源 us、1 端开路测 Û1 → Û1/us = −I2/is
sa = solve(Zs, [sp.Eq(I1, is_), sp.Eq(U2, 0)]); sb = solve(Zs, [sp.Eq(I1, 0), sp.Eq(U2, us)])
assert sp.simplify(sb[U1] / us + sa[I2] / is_) == 0
print("reciprocity forms ok")

# ---- 例：Z = [[6,4],[4,6]]（T 形 2、4、2 Ω）----
Z = [[6, 4], [4, 6]]
sa = solve(Z, [sp.Eq(U1, 10), sp.Eq(U2, 0)])
assert (sa[I1], sa[I2]) == (3, -2)
Ihat1 = sp.Rational(20) * sa[I2] / (10 + 2 * sa[I1])
assert Ihat1 == sp.Rational(-5, 2)
sb = solve(Z, [sp.Eq(U1, -2 * I1), sp.Eq(U2, 20)])
assert sb[I1] == Ihat1 and sb[U1] == 5
# 特勒根等式逐项核对
assert 10 * sb[I1] + 0 * sb[I2] == sb[U1] * sa[I1] + sb[U2] * sa[I2]
print("example:", sa, sb)

# ================= 练习 =================
# 2. Z=[[5,2],[2,6]]：(a) U1=10, I2=0 → I1=2, U2=4；(b) U1=0, I2=3 → Î1 = −1.2
Z = [[5, 2], [2, 6]]
sa = solve(Z, [sp.Eq(U1, 10), sp.Eq(I2, 0)])
assert (sa[I1], sa[U2]) == (2, 4)
Ih = sp.solve(sp.Eq(10 * sp.Symbol("x") + 4 * 3, 0 * 2 + sp.Symbol("y") * 0), sp.Symbol("x"))[0]
assert Ih == sp.Rational(-6, 5)
sb = solve(Z, [sp.Eq(U1, 0), sp.Eq(I2, 3)])
assert sb[I1] == Ih
print("ex2:", Ih)

# 3. (a) U1=12, U2=0：I1=4, I2=−1.5 → Y11=1/3, Y21=Y12=−1/8
Y11, Y21 = sp.Rational(4, 12), sp.Rational(-3, 2) / 12
Ih1 = Y21 * 6                       # (b) 端口 2 加 6 V、端口 1 短路
assert Ih1 == sp.Rational(-3, 4)
I1c = Y11 * 12 + Y21 * 6
assert I1c == sp.Rational(13, 4)
# 用一个具体的互易网络核对：取 Y22 = 1/4 → Y 正定，存在电阻网络（Π：Ya=Y11+Y12, Yb=−Y12, Yc=Y22+Y12，全为正）
Y = sp.Matrix([[Y11, Y21], [Y21, sp.Rational(1, 4)]])
assert all(v > 0 for v in (Y[0, 0] + Y[0, 1], -Y[0, 1], Y[1, 1] + Y[0, 1]))
assert (Y * sp.Matrix([12, 0]))[1] == sp.Rational(-3, 2)
assert (Y * sp.Matrix([0, 6]))[0] == Ih1 and (Y * sp.Matrix([12, 6]))[0] == I1c
print("ex3:", Ih1, I1c)

# ---- 对偶例：网孔 (2+4)Ia − 4Ib = 10，−4Ia + (4+1+3)Ib = 0 ----
Ia_, Ib_ = sp.symbols("Ia Ib")
s = sp.solve([6 * Ia_ - 4 * Ib_ - 10, -4 * Ia_ + 8 * Ib_], [Ia_, Ib_])
assert (s[Ia_], s[Ib_]) == (sp.Rational(5, 2), sp.Rational(5, 4))
# 对偶电路直接按节点列：Is=10 注入 a；a 对地 G1=2，a–b 之间 G3=4，b 对地 G2=1、G4=3
Va, Vb = sp.symbols("Va Vb")
s2 = sp.solve([2 * Va + 4 * (Va - Vb) - 10, 4 * (Vb - Va) + 1 * Vb + 3 * Vb], [Va, Vb])
assert (s2[Va], s2[Vb]) == (s[Ia_], s[Ib_])
print("dual ok")

# 4. 串联 RLC（R=3, L=2, C=0.5）↔ 并联 GCL（G=3, C=2, L=0.5）
w0a = 1 / sp.sqrt(2 * sp.Rational(1, 2)); w0b = 1 / sp.sqrt(sp.Rational(1, 2) * 2)
assert w0a == w0b == 1
# 串联 α = R/2L = 0.75；并联 α = G/2C = 0.75
assert sp.Rational(3, 4) == sp.Rational(3, 2 * 2)
print("all ok")
