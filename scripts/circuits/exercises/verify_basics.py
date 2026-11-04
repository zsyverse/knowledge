"""习题·基本概念 —— 独立验算（numpy/sympy）。运行无断言失败即通过。"""
import sympy as sp

ok = lambda a, b, tol=1e-9: abs(float(a) - float(b)) < tol

# 题 2：四个元件吸收功率（关联 p=ui，非关联 p=-ui）
pA, pB, pC, pD = 5 * -2, -(-3 * 4), (-6) * (-1.5), -(5.5 * 2)
assert (pA, pB, pC, pD) == (-10, 12, 9.0, -11)
assert pA + pB + pC + pD == 0
print("2:", pA, pB, pC, pD)

# 题 3：作业 2-4（KCL）
I2 = 1 + 3                 # 节点3：流入 1A(来自④) + 3A(左支路向上) = 流出 I2
I5 = -(1 + 2)              # 节点4：1A、2A、I5 均流出
I6 = I5 - 3                # 节点5：流入 I5 = 流出 3A + I6
I7 = I6 + 1                # 节点6：流入 I6 + 1A = 流出 I7
I1 = 2 + I7                # 节点1：流入 2A + I7 = 流出 I1
assert I1 + I2 == 1        # 节点2 校验
print("3:", I1, I2, I5, I6, I7)

# 题 4：作业 2-5（KVL，节点5为地）
V5 = 0; V4 = 8; V3 = V4 + 3; V2 = -8; V1 = V2 + 2
U2, U3, U5, U7 = V2 - V3, V4 - V1, V3 - V5, V1 - V5
assert (U2, U3, U5, U7) == (-19, 14, 11, -6)
print("4:", U2, U3, U5, U7)

# 题 5：作业 2-9（下方为地）
Vb = -5; VL = Vb + 3; VR = 14
I1 = VL / 2
It = (VL - VR) / (2 + 6)
I2 = I1 + It - 1           # 节点L：I2 + 1 = I1 + It
Va = VL - 2 * It
assert (I1, It, I2, Va, Va - Vb) == (-1, -2, -4, 2, 7)
# 5Ω 电流、各源电流（附带）
I5 = (VR - Vb) / 5
print("5:", I1, I2, Va - Vb, "I(5Ω, R→b)=", I5)

# 题 6：VCCS
u = sp.symbols("u")
usol = sp.solve(sp.Eq((u - 10) / 2 + u / 3 - sp.Rational(1, 2) * u, 0), u)[0]
I = (10 - usol) / 2
P_R1, P_R2 = 2 * I**2, usol**2 / 3
P_vs = -10 * I            # 电流 I 从 + 端流出（非关联）→ 吸收 -10I
P_ccs = -usol * sp.Rational(1, 2) * usol   # 电流从 + 端（a）流出 → 吸收 -u*0.5u
assert usol == 15 and I == sp.Rational(-5, 2)
assert P_R1 + P_R2 + P_vs + P_ccs == 0
print("6:", usol, I, P_R1, P_R2, P_vs, P_ccs)

# 题 7：并联电源 + 电流源串电阻
IR = 10 / 2
Ivs = IR - 3              # 电压源从 + 端流出的电流
Vm = 10 + 3 * 4           # 3A 向上流经 4Ω：Vm - Vtop = 12
P_vs_out, P_cs_out = 10 * Ivs, Vm * 3
P_R2, P_R4 = 10**2 / 2, 3**2 * 4
assert (Ivs, Vm, P_vs_out, P_cs_out, P_R2, P_R4) == (2, 22, 20, 66, 50, 36)
assert P_vs_out + P_cs_out == P_R2 + P_R4
print("7:", Ivs, Vm, P_vs_out, P_cs_out)

# 题 8：直流稳态储能
iL = 12 / (2 + 4); uC = 4 * iL
WC, WL = 0.5 * 2 * uC**2, 0.5 * 1 * iL**2
assert (iL, uC, WC, WL) == (2, 8, 64, 2)
print("8:", iL, uC, WC, WL)
print("all ok")
