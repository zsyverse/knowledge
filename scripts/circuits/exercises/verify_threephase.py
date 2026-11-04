"""习题·三相电路 —— 独立验算。三相题一律用完整网络的节点方程求解，再与单相/公式结果比对。"""
import numpy as np
import sympy as sp

a = np.exp(-2j * np.pi / 3)          # 正序：B 滞后 A 120°
deg = np.degrees
P2 = lambda z: f"{abs(z):.4f}∠{deg(np.angle(z)):.3f}°"
close = lambda x, y, tol=1e-6: abs(complex(x) - complex(y)) < tol


def solve_nodes(n, branches, fixed):
    """通用节点法。n 个节点(0..n-1)，fixed={节点: 电位} 由理想电压源钉住，
    branches=[(p,q,Z)] 无源阻抗支路。返回各节点电位。"""
    free = [k for k in range(n) if k not in fixed]
    idx = {k: i for i, k in enumerate(free)}
    Y = np.zeros((len(free), len(free)), complex); I = np.zeros(len(free), complex)
    for p, q, Z in branches:
        y = 1 / Z
        for u, v in ((p, q), (q, p)):
            if u in idx:
                Y[idx[u], idx[u]] += y
                if v in idx:
                    Y[idx[u], idx[v]] -= y
                else:
                    I[idx[u]] += y * fixed[v]
    V = dict(fixed)
    if free:
        sol = np.linalg.solve(Y, I)
        V.update({k: sol[idx[k]] for k in free})
    return V


# 题 2：由 U_BC=380∠0° 求相电压与其他线电压
UBC = 380
UB = UBC / np.sqrt(3) * np.exp(-1j * np.pi / 6)
UA = UB / a; UC = UB * a
assert close(UA, 380 / np.sqrt(3) * 1j)
assert close(UA - UB, 380 * np.exp(1j * np.radians(120))) and close(UC - UA, 380 * np.exp(-1j * np.radians(120)))
print("2: UA", P2(UA), "UAB", P2(UA - UB), "UCA", P2(UC - UA))

# 题 3：Δ 负载 Z=30+j40 直接接 U_l=380（取 U_AB=380∠30°，U_A=380/√3∠0°）
Up = 380 / np.sqrt(3)
EA, EB, EC = Up, Up * a, Up * a**2
Z = 30 + 40j
# 节点：0=N,1=A,2=B,3=C
V = solve_nodes(4, [(1, 2, Z), (2, 3, Z), (3, 1, Z)], {0: 0, 1: EA, 2: EB, 3: EC})
IAB = (V[1] - V[2]) / Z; ICA = (V[3] - V[1]) / Z; IBC = (V[2] - V[3]) / Z
IA = IAB - ICA; IB = IBC - IAB; IC = ICA - IBC
assert close(IAB, 7.6 * np.exp(1j * np.radians(30 - 53.130102354)))
assert close(abs(IA), 7.6 * np.sqrt(3))
assert close(np.angle(IA, True), -53.130102354, 1e-6)
P = 3 * abs(IAB)**2 * 30; Q = 3 * abs(IAB)**2 * 40
assert close(P, 5198.4) and close(Q, 6931.2)
# 改成 Y 联结
IY = Up / Z
PY = 3 * abs(IY)**2 * 30
assert close(P / PY, 3)
print("3: IAB", P2(IAB), "IBC", P2(IBC), "ICA", P2(ICA), "IA", P2(IA), "IB", P2(IB), "IC", P2(IC),
      "P", P, "Q", Q, "PY", PY, "IY", abs(IY))

# 题 4：Δ 负载 Z=24+j33 经线路 Zl=1+j1，电源相电压 220 V（Y 形，U_A=220∠0°）
Up = 220; EA, EB, EC = Up, Up * a, Up * a**2
Zl, ZD = 1 + 1j, 24 + 33j
# 节点：0=N,1=A,2=B,3=C(电源端),4=A',5=B',6=C'(负载端)
V = solve_nodes(7, [(1, 4, Zl), (2, 5, Zl), (3, 6, Zl), (4, 5, ZD), (5, 6, ZD), (6, 4, ZD)],
                {0: 0, 1: EA, 2: EB, 3: EC})
IA = (V[1] - V[4]) / Zl
IAB = (V[4] - V[5]) / ZD
ZY = ZD / 3
assert close(ZY + Zl, 9 + 12j)
assert close(IA, 220 / (9 + 12j))
assert close(abs(IA), 220 / 15)
UAB_load = V[4] - V[5]
Pload = 3 * abs(IAB)**2 * 24; Pline = 3 * abs(IA)**2 * 1
Psrc = (np.conj(IA) * EA * 3).real
assert close(Psrc, Pload + Pline)
assert close(abs(IAB), abs(IA) / np.sqrt(3))
print("4: IA", P2(IA), "IAB", P2(IAB), "|U_A'B'|", abs(UAB_load), "Pload", Pload, "Pline", Pline, "Psrc", Psrc,
      "UA'N(eq)", abs(IA * ZY))

# 题 5：作业 5-51 改编。U_A=100∠0°，Y 形纯电容 C=100μF（ω=314），Δ 形 300Ω
Up = 100; EA, EB, EC = Up, Up * a, Up * a**2
w = 314; ZC = 1 / (1j * w * 100e-6); R = 300
# 节点：0=N,1=A,2=B,3=C,4=N'(电容星点)
V = solve_nodes(5, [(1, 4, ZC), (2, 4, ZC), (3, 4, ZC), (1, 2, R), (2, 3, R), (3, 1, R)],
                {0: 0, 1: EA, 2: EB, 3: EC})
IA1 = (V[1] - V[4]) / ZC
IAB = (V[1] - V[2]) / R; ICA = (V[3] - V[1]) / R
IA_D = IAB - ICA
IA = IA1 + IA_D
S = 3 * EA * np.conj(IA)
assert abs(V[4]) < 1e-9
assert abs(IA1 - 3.14j) < 1e-9
assert close(IAB, 1 / np.sqrt(3) * np.exp(1j * np.pi / 6))
assert close(IA_D, 1)
assert close(S, 300 - 942j)
print("5: IA1", P2(IA1), "IAB", P2(IAB), "IA", P2(IA), "S", S)

# 题 6：Y 负载 Z=15+j8，Q=1536 var
Zr, X = 15, 8
I2 = 1536 / (3 * X); Il = np.sqrt(I2)
P = 3 * I2 * Zr
Upp = Il * abs(Zr + 1j * X); Ul = np.sqrt(3) * Upp
assert close(Il, 8) and close(P, 2880) and close(Upp, 136)
lam = Zr / 17
print("6: Il", Il, "P", P, "Up", Upp, "Ul", Ul, "λ", lam, "S", np.hypot(P, 1536))

# 题 7：两瓦特表。Y 负载 6+j8，U_l=380（U_A=380/√3∠0°），W1：i_A 与 u_AB；W2：i_C 与 u_CB
Up = 380 / np.sqrt(3); EA, EB, EC = Up, Up * a, Up * a**2
Z = 6 + 8j
# 节点：0=N,1=A,2=B,3=C,4=N'
V = solve_nodes(5, [(1, 4, Z), (2, 4, Z), (3, 4, Z)], {0: 0, 1: EA, 2: EB, 3: EC})
IA = (V[1] - V[4]) / Z; IC = (V[3] - V[4]) / Z
W1 = ((V[1] - V[2]) * np.conj(IA)).real
W2 = ((V[3] - V[2]) * np.conj(IC)).real
Il = abs(IA); phi = np.angle(Z)
assert close(W1, 380 * Il * np.cos(phi + np.pi / 6)) and close(W2, 380 * Il * np.cos(phi - np.pi / 6))
P = 3 * Il**2 * 6; Q = 3 * Il**2 * 8
assert close(W1 + W2, P) and close(np.sqrt(3) * (W2 - W1), Q)
print("7: Il", Il, "W1", W1, "W2", W2, "P", P, "Q", Q)
# 改为纯电感负载 Z=j10 时的读数（看符号）
V = solve_nodes(5, [(1, 4, 10j), (2, 4, 10j), (3, 4, 10j)], {0: 0, 1: EA, 2: EB, 3: EC})
IA = (V[1] - V[4]) / 10j; IC = (V[3] - V[4]) / 10j
W1b = ((V[1] - V[2]) * np.conj(IA)).real; W2b = ((V[3] - V[2]) * np.conj(IC)).real
print("7b (Z=j10): W1", W1b, "W2", W2b)
assert close(W1b + W2b, 0, 1e-9)

# 题 8：相序指示器。A 相电容 1/(ωC)=R，B、C 相电阻 R，无中线，U_p=220
Up = 220; EA, EB, EC = Up, Up * a, Up * a**2
R = 100.0
V = solve_nodes(5, [(1, 4, -1j * R), (2, 4, R), (3, 4, R)], {0: 0, 1: EA, 2: EB, 3: EC})
UNN = V[4]
UB_ = EB - UNN; UC_ = EC - UNN; UA_ = EA - UNN
s = sp.sqrt(3)
UNN_exact = sp.nsimplify((sp.I * 1 + sp.exp(-2 * sp.pi * sp.I / 3) + sp.exp(2 * sp.pi * sp.I / 3)) / (2 + sp.I))
assert close(UNN / Up, complex(UNN_exact))
assert close(UNN / Up, (-1 + 3j) / 5)
print("8: UN'N", P2(UNN), "UA'", P2(UA_), "UB'", P2(UB_), abs(UB_) / Up, "UC'", P2(UC_), abs(UC_) / Up)
# 精确值
kB = abs(complex(sp.exp(-2 * sp.pi * sp.I / 3) - (-1 + 3 * sp.I) / 5))
print("   |UB'|/Up exact^2 =", sp.nsimplify(sp.Abs(sp.expand_complex(sp.exp(-2*sp.pi*sp.I/3) - (-1+3*sp.I)/5))**2))
print("   |UC'|/Up exact^2 =", sp.nsimplify(sp.Abs(sp.expand_complex(sp.exp(2*sp.pi*sp.I/3) - (-1+3*sp.I)/5))**2))

# 题 9：作业 5-58 移相网络（R=10Ω，f=50Hz）
# 节点：A(上端，电位 U)、Bm(中点)、Cn(下端，0)、O(三电阻公共点)
U = 1.0
XL, XC, Rr = sp.symbols("X_L X_C R", positive=True)
VB, VO = sp.symbols("V_B V_O")
w = 100 * np.pi; Rv = 10.0
L = np.sqrt(3) * Rv / w; C = 1 / (w * np.sqrt(3) * Rv)
ZL, ZC2 = 1j * w * L, 1 / (1j * w * C)
# 数值解：节点 0=C端(地)，1=A端(U)，2=B中点，3=O
V = solve_nodes(4, [(1, 2, ZL), (2, 0, ZC2), (1, 3, Rv), (2, 3, Rv), (0, 3, Rv)], {0: 0, 1: U})
UA_ = V[1] - V[3]; UB_ = V[2] - V[3]; UC_ = V[0] - V[3]
assert close(UB_, UA_ * a) and close(UC_, UA_ * a**2)
print("9: L", L * 1e3, "mH  C", C * 1e6, "uF  |UA|/U", abs(UA_), "ang", deg(np.angle(UA_)),
      "VB", V[2], "VO", V[3])
assert close(abs(UA_), 1 / np.sqrt(3))
# 反过来：若 L、C 互换会怎样（负序）
V2 = solve_nodes(4, [(1, 2, ZC2), (2, 0, ZL), (1, 3, Rv), (2, 3, Rv), (0, 3, Rv)], {0: 0, 1: U})
print("   swapped L/C:", P2(V2[1]-V2[3]), P2(V2[2]-V2[3]), P2(V2[0]-V2[3]))
print("all ok")
