"""习题·一般分析方法 —— 独立验算。"""
import sympy as sp

R = sp.Rational

# 题 1：方程数（n=4, b=7）
n, b = 4, 7
assert (n - 1, b - n + 1) == (3, 4)

# 题 2：作业 4-12 支路电流法。R1=10, R=20, Us1=10(上正), 右源 20 V(上负下正), Is2=3 A 向下
I1, I3 = sp.symbols("I1 I3")
s = sp.solve([I1 + I3 - 3, (10 - 10 * I1) - (-20 * I3 - 20)], [I1, I3])
assert s[I1] == 3 and s[I3] == 0
V = 10 - 10 * s[I1]
assert V == -20 and -20 * s[I3] - 20 == V
P_R1 = 10 * 3**2
P_Us1_out = 10 * s[I1]              # I1 自下而上穿过 Us1（− → +），发出
P_Is_abs = V * 3                    # 电流由上(+)端流入：关联，吸收 V*3
assert P_R1 == 90 and P_Us1_out == 30 and P_Is_abs == -60
assert P_Us1_out - P_Is_abs == P_R1
print("2:", s, "V_top =", V, "Is delivers", -P_Is_abs)

# 题 3：超网孔。左：28V(上正)，上左 4Ω；中：2A 向上；右：上右 2Ω，右竖 6Ω
Ia, Ib, Uis = sp.symbols("Ia Ib Uis")
s = sp.solve([28 - 4 * Ia - 2 * Ib - 6 * Ib, Ib - Ia - 2], [Ia, Ib])
assert s[Ia] == 1 and s[Ib] == 3
U = 28 - 4 * s[Ia]
assert U == 24 and U == 2 * s[Ib] + 6 * s[Ib]
P_res = 4 * 1**2 + 2 * 3**2 + 6 * 3**2
assert P_res == 76 == 28 * s[Ia] + U * 2
print("3:", s, "U_Is =", U)

# 题 4：节点法标准形式。2A 串 5Ω 注入 ①；①–地 2Ω；①–② 4Ω；②–地 4Ω；24V 串 4Ω 接 ②
U1, U2 = sp.symbols("U1 U2")
s = sp.solve([(R(1, 2) + R(1, 4)) * U1 - R(1, 4) * U2 - 2,
              -R(1, 4) * U1 + (R(1, 4) + R(1, 4) + R(1, 4)) * U2 - R(24, 4)], [U1, U2])
assert s[U1] == 6 and s[U2] == 10
U_is = s[U1] + 2 * 5          # 电流源端电压（上正）
assert U_is == 16
I_vs = (24 - s[U2]) / 4
P_res = s[U1]**2 / 2 + (s[U1] - s[U2])**2 / 4 + s[U2]**2 / 4 + I_vs**2 * 4 + 2**2 * 5
assert P_res == U_is * 2 + 24 * I_vs
print("4:", s, "U_Is =", U_is, "I_24V =", I_vs, "P:", P_res)

# 题 5：超节点。6A 注入 a；a–地 4Ω；a、b 间 8V（b 正）；b–地 4Ω；b–2Ω–c；c 由 24V 接地
Ua, Ub = sp.symbols("Ua Ub")
s = sp.solve([Ua / 4 + Ub / 4 + (Ub - 24) / 2 - 6, Ub - Ua - 8], [Ua, Ub])
assert s[Ua] == 12 and s[Ub] == 20
i_ab = 6 - s[Ua] / 4        # 由 a 经电压源流向 b
assert i_ab == 3 and i_ab == s[Ub] / 4 + (s[Ub] - 24) / 2
i24 = (24 - s[Ub]) / 2       # 24V 源从 + 端流出
P_res = s[Ua]**2 / 4 + s[Ub]**2 / 4 + (24 - s[Ub])**2 / 2
assert P_res == 144 == 6 * s[Ua] + 8 * i_ab + 24 * i24
print("5:", s, "i_ab =", i_ab, "i24 =", i24)

# 题 6：VCCS。3A 注入 ①；①–地 4Ω；①–② 2Ω（u_x，① 正）；②–地 2Ω；g u_x 由地注入 ②，g=1 S
s = sp.solve([U1 / 4 + (U1 - U2) / 2 - 3, (U2 - U1) / 2 + U2 / 2 - 1 * (U1 - U2)], [U1, U2])
assert s[U1] == 8 and s[U2] == 6
ux = s[U1] - s[U2]
# 标准形式整理后第二式：-1.5 U1 + 2 U2 = 0
assert -R(3, 2) * s[U1] + 2 * s[U2] == 0
P_res = s[U1]**2 / 4 + ux**2 / 2 + s[U2]**2 / 2
assert P_res == 36 == 3 * s[U1] + s[U2] * 1 * ux
print("6:", s, "u_x =", ux, "P_vccs =", s[U2] * ux)

# 题 7：理想二极管。6V—1kΩ—D1→o；V2—1kΩ—D2→o；o—2kΩ—地（kΩ、mA）
def diodes(V1, V2):
    for on1 in (True, False):
        for on2 in (True, False):
            Vo = sp.Symbol("Vo")
            eq = -Vo / 2
            if on1: eq += (V1 - Vo) / 1
            if on2: eq += (V2 - Vo) / 1
            vo = sp.solve(eq, Vo)[0]
            i1 = (V1 - vo) if on1 else 0
            i2 = (V2 - vo) if on2 else 0
            ok1 = (i1 >= 0) if on1 else (V1 - vo <= 0)
            ok2 = (i2 >= 0) if on2 else (V2 - vo <= 0)
            if ok1 and ok2:
                return on1, on2, vo, i1, i2

r = diodes(6, 2)
assert r == (True, False, 4, 2, 0)
r2 = diodes(6, 5)
assert r2[:2] == (True, True) and r2[2] == R(22, 5) and r2[3] == R(8, 5) and r2[4] == R(3, 5)
# D2 开始导通的临界：V2 > 4 V
print("7:", r, r2)

# 题 8：作业 4-17 指定树。R1=R5=2, R2=R4=1, R3=R6=3, R7=4, IS4=6, IS5=1
# 全节点法核对：节点 L,T1,T2,Rt,B1,B2；L 为参考
nodes = ["T1", "T2", "Rt", "B1", "B2"]
Vs = {k: sp.Symbol("V" + k) for k in nodes}
Vs["L"] = 0
res = [("L", "T1", 1), ("T1", "T2", 3), ("T2", "Rt", 2), ("L", "B1", 2), ("B1", "B2", 3), ("B2", "Rt", 1), ("L", "Rt", 4)]
src = [("B1", "T1", 6), ("B2", "T2", 1)]
eqs = []
for nd in nodes:
    e = 0
    for a, b_, r_ in res:
        if a == nd: e += (Vs[a] - Vs[b_]) / r_
        if b_ == nd: e += (Vs[b_] - Vs[a]) / r_
    for a, b_, i in src:
        if b_ == nd: e -= i
        if a == nd: e += i
    eqs.append(e)
sol = sp.solve(eqs, [Vs[k] for k in nodes])
V = {k: sol[Vs[k]] for k in nodes}; V["L"] = 0
I6 = (V["T1"] - V["T2"]) / 3
I7 = (V["L"] - V["Rt"]) / 4
assert I6 == 1 and I7 == R(1, 2)
j1 = (V["L"] - V["B1"]) / 2; j2 = (V["B2"] - V["Rt"]) / 1; j3 = (V["B1"] - V["B2"]) / 3
j4 = (V["L"] - V["T1"]) / 1; j5 = (V["T2"] - V["Rt"]) / 2
assert (j1, j2, j3, j4, j5) == (R(9, 2), R(-5, 2), R(-3, 2), -5, 2)
# 回路方程
I6s, I7s = sp.symbols("I6 I7")
s = sp.solve([12 * I6s + 6 * I7s - 15, 6 * I6s + 10 * I7s - 11], [I6s, I7s])
assert s[I6s] == 1 and s[I7s] == R(1, 2)
print("8: I6 =", I6, "I7 =", I7, "tree:", j1, j2, j3, j4, j5)
# 附：题 4 消元中间式；题 7 临界 U2=4（D1 通 D2 断时 Uo=4）
assert all(diodes(6, v)[:2] == (True, False) for v in (0, 2, 3, R(39, 10)))
assert diodes(6, 4)[2] == 4 and diodes(6, 4)[4] == 0   # 临界：两种假设都给出 Uo=4、I_D2=0
assert diodes(6, R(41, 10))[:2] == (True, True)
print("all ok")
