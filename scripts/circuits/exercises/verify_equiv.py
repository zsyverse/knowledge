"""习题·等效变换 —— 独立验算（节点法通用求解 + 化简公式对照）。"""
import sympy as sp

R = sp.Rational


def par(*rs):
    return 1 / sum(1 / sp.nsimplify(r) for r in rs)


def nodal(nodes, resistors, isrc=(), ground="0"):
    """resistors: [(n1,n2,R)]；isrc: [(from,to,I)] 电流由 from 经电源流向 to（注入 to）。"""
    V = {n: (0 if n == ground else sp.Symbol("V_" + n)) for n in nodes}
    eqs = []
    for n in nodes:
        if n == ground:
            continue
        e = 0
        for a, b, r in resistors:
            if a == n:
                e += (V[a] - V[b]) / r
            elif b == n:
                e += (V[b] - V[a]) / r
        for a, b, i in isrc:
            if b == n:
                e -= i
            elif a == n:
                e += i
        eqs.append(e)
    sol = sp.solve(eqs, [V[n] for n in nodes if n != ground], dict=True)[0]
    return {n: (0 if n == ground else sp.nsimplify(sol[V[n]])) for n in nodes}


def rin(nodes, resistors, a, b):
    """端口 a-b 注入 1 A 求等效电阻（以 b 为地）。"""
    V = nodal(nodes, resistors, [(b, a, 1)], ground=b)
    return V[a]


# 题 2：串并联（5Ω 被导线短接）
Rab = 4 + par(6, 2 + par(3, 6))
assert Rab == R(32, 5)
# 用节点法核对：节点 a,c,d,x,y(=b)，5Ω 两端都是 b
r2 = rin(["a", "c", "d", "b"], [("a", "c", 4), ("c", "b", 6), ("c", "d", 2), ("d", "b", 3), ("d", "b", 6)], "a", "b")
assert r2 == Rab
print("2: Rab =", Rab, float(Rab))

# 题 3：平衡电桥
assert 3 * 8 == 6 * 4
Rab3 = par(3 + 6, 4 + 8)
r3 = rin(["a", "b", "c", "d"], [("a", "c", 3), ("c", "b", 6), ("a", "d", 4), ("d", "b", 8), ("c", "d", 10)], "a", "b")
assert Rab3 == r3 == R(36, 7)
print("3: Rab =", Rab3, float(Rab3))

# 题 4：Y–Δ（Δ 三边均 6Ω → Y 每臂 2Ω）
Rab4 = 2 + par(2 + 4, 2 + 10)
nodes4 = ["a", "b", "c", "d"]
res4 = [("a", "c", 6), ("a", "d", 6), ("c", "d", 6), ("c", "b", 4), ("d", "b", 10)]
assert Rab4 == rin(nodes4, res4, "a", "b") == 6
# 外加 12 V：注入电流 2 A
V = nodal(nodes4, res4, [("b", "a", 2)], ground="b")
assert V["a"] == 12
Icd = (V["c"] - V["d"]) / 6
Iac, Iad = (V["a"] - V["c"]) / 6, (V["a"] - V["d"]) / 6
print("4: Rab=6, Va,Vc,Vd =", V["a"], V["c"], V["d"], " Icd =", Icd, " Iac,Iad=", Iac, Iad)
# Y 形等效里：o 点电位 = 12 - 2*2 = 8；两路 6Ω、12Ω 分流
Vo = sp.Integer(12 - 2 * 2)
Ic_path, Id_path = Vo / 6, Vo / 12
assert V["c"] == Ic_path * 4 and V["d"] == Id_path * 10
assert Icd == R(-2, 9) and Iac == R(10, 9) and Iad == R(8, 9)

# 题 5：作业 4-47（对称）
# 节点：L(左上) R(右上) M(中上) BL(左下) BR(右下) Bc(中下，电压源负端) P(1Ω 与 6V 正端之间)
nodes5 = ["L", "Rt", "M", "BL", "BR", "Bc", "P"]
res5 = [("L", "Rt", 7), ("L", "M", 1), ("M", "Rt", 1), ("L", "BL", 3), ("L", "BL", 6),
        ("Rt", "BR", 3), ("Rt", "BR", 6), ("BL", "Bc", 1), ("Bc", "BR", 1), ("M", "P", 1)]
# 6V 源：P 为 +，Bc 为 −。用戴维南形式：把 6V 与 P–M 的 1Ω 合成 6V 串 1Ω：M 与 Bc 之间
res5b = [r for r in res5 if r[:2] != ("M", "P")]
nodes5b = [n for n in nodes5 if n != "P"]
# 诺顿：6 A（Bc→M）并 1Ω
V5 = nodal(nodes5b, res5b + [("M", "Bc", 1)], [("Bc", "M", 6)], ground="Bc")
I = (6 - (V5["M"] - V5["Bc"])) / 1
assert I == 2 and V5["L"] == V5["Rt"]
print("5: I =", I, " P_delivered =", 6 * I, " V_L=V_R=", V5["L"])

# 题 6：作业 4-5（a 为桥左端，右端 r 为参考）
V6 = nodal(["a", "p", "q", "r"], [("a", "p", 4), ("a", "q", 6), ("p", "q", 10), ("p", "r", 10), ("q", "r", 5)],
           [("r", "a", 5)], ground="r")
U = V6["p"] - V6["q"]
Uab = V6["a"] + 5 * 24
assert (V6["a"], V6["p"], V6["q"], U, Uab) == (30, 20, 15, 5, 150)
print("6: U =", U, " Uab =", Uab, " currents:", (30 - 20) / 4, (30 - 15) / 6, (20 - 15) / 10, 20 / 10, 15 / 5)

# 题 7：电源等效变换。t 节点：12V 串 6Ω、3A(串 4Ω) 注入、3Ω 到地；t—2Ω—a
Is_tot = R(12, 6) + 3
Rp = par(6, 3)
Uoc, Req = Is_tot * Rp, Rp + 2
assert (Uoc, Req) == (10, 4)
# 节点法核对 Uoc
t = sp.Symbol("t")
assert sp.solve((t - 12) / 6 + t / 3 - 3, t)[0] == 10
IL = Uoc / (Req + 6)
assert IL == 1
# 原电路中接 6Ω 后：t 点电压，6Ω 支路电流，3Ω 电流
tv = sp.solve((t - 12) / 6 + t / 3 - 3 + (t) / (2 + 6), t)[0]
print("7: Uoc =", Uoc, " Req =", Req, " IL =", IL, " t =", tv, " I(12V src out of +) =", (12 - tv) / 6)

# 题 8：含 CCCS 的输入电阻。a—1Ω—x，x—4Ω—b（i1 向下），CCCS 3 i1 由 b 注入 x；3Ω 并在 a、b
u, i = sp.symbols("u i")
# 只看右支路：流入 a 的电流 i_r 流过 1Ω 到 x；x 处 KCL：i_r + 3 i1 = i1 → i1 = -i_r/2
ir = sp.Symbol("ir")
i1 = -ir / 2
ur = 1 * ir + 4 * i1
Rr = sp.simplify(ur / ir)
assert Rr == -1
Rin = sp.simplify(1 / (R(1, 3) + 1 / Rr))
assert Rin == R(-3, 2)
print("8: R_branch =", Rr, " Rin =", Rin)
# 附：题 3 短接桥支路结果相同；题 6 Δ→Y 数值；题 8 受控源被错误置零时的结果
assert par(3, 4) + par(6, 8) == R(36, 7)
assert (R(4 * 6, 20), R(4 * 10, 20), R(6 * 10, 20)) == (R(6, 5), 2, 3)
assert R(6, 5) + par(12, 8) == 6 and 5 * R(8, 20) == 2
assert par(3, 1 + 4) == R(15, 8)
print("all ok")
