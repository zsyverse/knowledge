"""习题·电路定理 —— 独立验算。运行无断言失败即通过。"""
import sympy as sp

R = sp.Rational

# 题 2：叠加（Us=12V, R1=6, R2=3, R3=2, R4=4, Is=3A 注入 b）
Va, Vb = sp.symbols("Va Vb")
def solve2(Us, Is):
    s = sp.solve([(Va - Us) / 6 + Va / 3 + (Va - Vb) / 2,
                  (Vb - Va) / 2 + Vb / 4 - Is], [Va, Vb])
    return s[Va] / 3                     # R2 中向下电流
I1, I2, I = solve2(12, 0), solve2(0, 3), solve2(12, 3)
assert (I1, I2, I) == (1, 1, 2)
assert 3 * I**2 == 12 and 3 * I1**2 + 3 * I2**2 == 6
print("2:", I1, I2, I)

# 题 3：叠加 + CCVS（Us=10, R1=2 中 i 向右, a 到地：R2=4 串 CCVS 2i(+上), Is=3A 注入 a）
U, i = sp.symbols("U i")
def solve3(Us, Is):
    s = sp.solve([i - (Us - U) / 2,               # R1 电流
                  U - (4 * (i + Is) + 2 * i)], [U, i])  # 竖支路向下电流 i+Is
    return s[U], s[i]
a1, a2, a = solve3(10, 0), solve3(0, 3), solve3(10, 3)
assert a1 == (R(15, 2), R(5, 4)) and a2 == (3, R(-3, 2)) and a == (R(21, 2), R(-1, 4))
print("3:", a1, a2, a)

# 题 4：线性关系
a_, b_, c_ = sp.symbols("a b c")
s = sp.solve([2 * a_ + b_ - 4, a_ + 2 * b_ - 5], [a_, b_])
assert s == {a_: 1, b_: 2}
assert 3 * 1 + 2 * 3 == 9 and -4 / 2 == -2
s2 = sp.solve([c_ - 1, 2 * a_ + b_ + c_ - 5, a_ + 2 * b_ + c_ - 6], [a_, b_, c_])
assert s2 == {a_: 1, b_: 2, c_: 1}
assert 3 + 6 + 1 == 10
print("4:", s, s2)

# 题 5：戴维南（Us=24, R1=4, R2=12, R3=6, Is=2A 注入 a）
Vc = sp.symbols("Vc")
vc = sp.solve((Vc - 24) / 4 + Vc / 12 - 2, Vc)[0]
Uoc = vc + 2 * 6
Req = 6 + R(4 * 12, 16)
assert (vc, Uoc, Req) == (24, 36, 9)
assert Uoc / (Req + 3) == 3 and Uoc**2 / (4 * Req) == 36
print("5:", Uoc, Req)

# 题 6：诺顿（Us=18, R1=3, R2=6, R3=2, Is=1A 由 a 流向 b）
vc = sp.solve((Vc - 18) / 3 + Vc / 6 + Vc / 2, Vc)[0]   # a 短接到地
Isc = vc / 2 - 1
Req6 = 2 + R(3 * 6, 9)
vco = sp.solve((Vc - 18) / 3 + Vc / 6 + 1, Vc)[0]       # 开路
Uoc6 = vco - 2 * 1
assert (vc, Isc, Req6, vco, Uoc6) == (6, 2, 4, 10, 8) and Uoc6 == Isc * Req6
# 接 RL=4：电流
assert Isc * Req6 / (Req6 + 4) == 1
print("6:", Isc, Req6, Uoc6)

# 题 7：含 CCVS（Us=12, R1=4 中 i1 向右, R2=4 c 到地, c→a 串 CCVS 2i1，a 端为 +）
Va7, Vc7, i1, I7 = sp.symbols("Va Vc i1 I")
op = sp.solve([i1 - (12 - Vc7) / 4, i1 - Vc7 / 4, Va7 - (Vc7 + 2 * i1)], [Va7, Vc7, i1])
assert op[Va7] == 9 and op[i1] == R(3, 2)
sc = sp.solve([i1 - (12 - Vc7) / 4, i1 - Vc7 / 4 - I7, 0 - (Vc7 + 2 * i1)], [Vc7, i1, I7])
assert sc[I7] == 9 and sc[Vc7] == -12 and sc[i1] == 6
# 外加电源：Us 置零，端口加 u，流入 a 的电流 Ii
u, Ii = sp.symbols("u Ii")
ex = sp.solve([i1 - (0 - Vc7) / 4, Ii + i1 - Vc7 / 4, u - (Vc7 + 2 * i1)], [Vc7, i1, Ii])
assert sp.simplify(u / ex[Ii]) == 1 and ex[Vc7] == 2 * u and ex[i1] == -u / 2
assert R(9**2, 4 * 1) == R(81, 4) and float(R(81, 4)) == 20.25
print("7:", op, sc, ex)

# 题 8：作业 4-36
Uoc8 = R(10 * 4, 6)
Isc8 = 8 - R(10, 2)
assert Uoc8 == R(20, 3) and Isc8 == 3 and Uoc8 / Isc8 == R(20, 9)
print("8:", Uoc8, Isc8, Uoc8 / Isc8)
print("all ok")
