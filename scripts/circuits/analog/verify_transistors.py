"""模电·双极型晶体管与场效应管 —— 独立验算（直流用 KVL/KCL + 假设—验证，MOS 偏置解二次方程并舍根）。"""
import math

import sympy as sp

VT = 0.026


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol * max(1, abs(b)), (a, b)


# ================= 管型、管脚判断 =================
def identify(vs):
    """由放大区三个管脚电位判断：返回 (类型, 材料, E, B, C)。"""
    s = sorted(vs)
    pairs = [(abs(a - b), a, b) for i, a in enumerate(vs) for b in vs[i + 1:]]
    d, a, b = min(pairs)
    mat = "Si" if 0.5 <= d <= 0.8 else ("Ge" if 0.1 <= d <= 0.4 else "?")
    c = [v for v in vs if v not in (a, b)][0]
    if c == s[-1]:          # 集电极电位最高 → NPN，基极居中
        typ = "NPN"; B, E = max(a, b), min(a, b)
    else:                   # 集电极电位最低 → PNP
        typ = "PNP"; B, E = min(a, b), max(a, b)
    return typ, mat, E, B, c


assert identify([2.0, 2.7, 6.0]) == ("NPN", "Si", 2.0, 2.7, 6.0)
assert identify([-6.0, -2.2, -2.0]) == ("PNP", "Ge", -2.0, -2.2, -6.0)
assert identify([12.0, 11.3, 6.0]) == ("PNP", "Si", 12.0, 11.3, 6.0)
assert identify([5.0, 1.2, 0.5]) == ("NPN", "Si", 0.5, 1.2, 5.0)
print("identify ok")

# α、β、穿透电流
beta = 100
close(beta / (1 + beta), 0.990, 1e-3)
close((1 + beta) * 10e-9 * 1e6, 1.01)        # µA


# ================= 固定偏置 =================
def fixed_bias(VCC, RB, RC, beta, RE=0.0, VBE=0.7, VCEs=0.2):
    """kΩ、mA。先设放大区，V_CE < V_CE(sat) 则改按饱和区。"""
    IB = (VCC - VBE) / (RB + (1 + beta) * RE)
    IC = beta * IB
    VCE = VCC - IC * RC - (1 + beta) * IB * RE
    if VCE > VCEs:
        return "active", IB, IC, VCE
    # 饱和：V_CE = V_CEs，基极回路与集电极回路联立
    ib, ic = sp.symbols("ib ic")
    sol = sp.solve([VCC - ib * RB - VBE - (ib + ic) * RE, VCC - ic * RC - VCEs - (ib + ic) * RE], [ib, ic], dict=True)[0]
    return "sat", float(sol[ib]), float(sol[ic]), VCEs


st, IB, IC, VCE = fixed_bias(12, 565, 3, 100)
assert st == "active"; close(IB * 1e3, 20); close(IC, 2.0); close(VCE, 6.0)
close(IC * VCE, 12)                              # mW
st, IB, IC, VCE = fixed_bias(12, 113, 3, 100)
assert st == "sat"; close(IC, 3.933); close(IC / IB, 39.3, 2e-3)
close((12 - 0.2) / 3, 3.933)
RBedge = (12 - 0.7) / ((12 - 0.2) / 3 / 100)
close(RBedge, 287.3, 1e-3)
print("fixed bias ok; RB edge", RBedge)

# 练习：带 R_E
st, IB, IC, VCE = fixed_bias(12, 430, 2, 100, RE=1)
assert st == "active"; close(IB * 1e3, 21.28, 2e-3); close(IC, 2.128, 2e-3); close(VCE, 5.595, 2e-3)
print("RE bias:", IB, IC, VCE)

# ================= 小信号参数 =================
gm = 1e-3 / VT
close(gm * 1e3, 38.46)
rpi = 100 / gm
close(rpi, 2600)
ro = 100 / 1e-3
close(ro, 100e3)
close(gm * ro, 3846, 1e-3)
rbe = 200 + 101 * VT / 1.01e-3
close(rbe, 2800)
print("small signal:", gm, rpi, ro, gm * ro, rbe)


# ================= MOSFET =================
def nmos(VGS, VDS, K=0.5, Vt=1.0):
    """返回 (区, I_D/mA)。"""
    if VGS <= Vt:
        return "cutoff", 0.0
    vov = VGS - Vt
    if VDS >= vov:
        return "sat", K * vov ** 2
    return "triode", K * (2 * vov * VDS - VDS ** 2)


assert nmos(3, 4) == ("sat", 2.0)
close(2 * 0.5 * 2, 2.0)                           # g_m = 2K V_ov
close(2 * math.sqrt(0.5 * 2), 2.0)                # g_m = 2√(K I_D)
assert nmos(3, 1) == ("triode", 1.5)
close(1 / (0.02 * 2e-3), 25e3)
# 练习 4
assert nmos(0.8, 5)[0] == "cutoff"
r, i = nmos(2.5, 0.5); assert r == "triode"; close(i, 0.625)
r, i = nmos(2.5, 5); assert r == "sat"; close(i, 1.125)
r, i = nmos(3, 1); assert r == "triode"; close(i, 1.5)    # PMOS 例用绝对值换成 NMOS 形式
print("nmos ok")

# 分压偏置共源：V_G = 4 V，R_S = 1k，K = 0.5，V_T = 1
VG = 12 * 100 / 300
assert VG == 4
I = sp.Symbol("I")
roots = sp.solve(sp.Eq(I, sp.Rational(1, 2) * (VG - I - 1) ** 2), I)
good = [float(x) for x in roots if VG - float(x) > 1]
assert len(good) == 1
ID = good[0]
close(ID, 4 - math.sqrt(7)); close(ID, 1.354, 2e-3)
VGS = VG - ID
close(VGS, 2.646, 2e-3)
VDS = 12 - ID * (3 + 1)
close(VDS, 6.584, 2e-3)
assert VDS >= VGS - 1
close(2 * 0.5 * (VGS - 1), 1.646, 2e-3)
print("cs bias:", ID, VGS, VDS)

# ================= JFET =================
IDSS, VP = 8.0, -4.0
jf = lambda v: IDSS * (1 - v / VP) ** 2
close(jf(-2), 2.0)
close(-2 * IDSS / VP * (1 - (-2) / VP), 2.0)
# 自偏压 R_S = 1k：V_GS = -I_D
roots = sp.solve(sp.Eq(I, 8 * (1 - (-I) / -4) ** 2), I)
good = [float(x) for x in roots if -float(x) > VP]
assert good == [2.0], roots
print("jfet ok")
print("transistors: all checks passed")
