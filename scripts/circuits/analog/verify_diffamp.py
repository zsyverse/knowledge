"""模电·差分放大与集成运放 —— 独立验算。

差分对：对完整的两管小信号电路（两只 hybrid-π + 尾电阻）列节点方程，分别加差模、共模输入，
求单端/双端增益，再与半电路公式比较；大信号用 i_C1 = I_EE/(1+e^{−v_d/V_T})。
运放非理想参数：失调的节点方程、GBW 与 SR 的数值。电阻 kΩ、电流 mA、电导 mS。
"""
import math
import sympy as sp

VT = 0.026


def close(a, b, tol=5e-3):
    a, b = float(a), float(b)
    assert abs(a - b) <= tol * abs(b), (a, b)


def par(*r):
    return 1 / sum(1 / x for x in r)


# ---------------------------------------------------------------- 静态
Vcc = Vee = 12
RC, REE, beta = 10, 11.3, 100
IEE = (Vee - 0.7) / REE
close(IEE, 1.0, 1e-9)
IC = IEE / 2                      # α≈1
VC = Vcc - IC * RC
close(VC, 7.0, 1e-9)
gm = IC / VT
rpi = beta / gm
close(gm, 19.23, 1e-3); close(rpi, 5.2, 1e-3)
print("Q: IEE, IC, VC, gm, rpi =", IEE, IC, VC, gm, rpi)


def pair_ss(v1, v2, Rtail, RL_between=None, rc=RC, g=None, rp=None):
    """两管小信号节点方程：未知 ve、vc1、vc2。返回 (vc1, vc2, i_b1)。"""
    g = gm if g is None else g
    rp = rpi if rp is None else rp
    ve, c1, c2 = sp.symbols("ve c1 c2")
    yl = 0 if RL_between is None else 1 / RL_between
    eqs = [
        (v1 - ve) / rp + g * (v1 - ve) + (v2 - ve) / rp + g * (v2 - ve) - ve / Rtail,   # 射极节点
        g * (v1 - ve) + c1 / rc + (c1 - c2) * yl,                                     # 集电极 1
        g * (v2 - ve) + c2 / rc + (c2 - c1) * yl,                                     # 集电极 2
    ]
    s = sp.solve(eqs, [ve, c1, c2], dict=True)[0]
    return float(s[c1]), float(s[c2]), float((v1 - s[ve]) / rp)


# 差模：v1 = +vd/2，v2 = −vd/2，vd = 1
c1, c2, ib = pair_ss(0.5, -0.5, REE)
Ad1, Ad2, Ad = c1, c2, c1 - c2
close(Ad1, -96.15, 1e-3); close(Ad2, 96.15, 1e-3); close(Ad, -192.3, 1e-3)
close(Ad, -gm * RC, 1e-9)
Rid = 1 / ib
close(Rid, 10.4, 1e-3)
# 共模：v1 = v2 = 1
c1c, c2c, _ = pair_ss(1, 1, REE)
Ac1 = c1c
close(Ac1, -0.4371, 1e-3); close(c1c - c2c + 1, 1, 1e-12)
close(-beta * RC / (rpi + (1 + beta) * 2 * REE), Ac1, 1e-9)
close(-RC / (2 * REE), -0.4425, 1e-3)
CMRR = abs(Ad1 / Ac1)
close(CMRR, 220, 2e-3); close(20 * math.log10(CMRR), 46.8, 2e-3)
print("diff pair: Ad1, Ad, Rid, Ac1, CMRR, dB =", Ad1, Ad, Rid, Ac1, CMRR, 20 * math.log10(CMRR))

# 图卡 13 例：v1 = 1.01，v2 = 0.99
v1, v2 = 1.01, 0.99
vd, vc = v1 - v2, (v1 + v2) / 2
close(vd, 0.02, 1e-9); close(vc, 1.0, 1e-9)
close(v1, vc + vd / 2, 1e-12); close(v2, vc - vd / 2, 1e-12)
dvo1 = Ad1 * vd + Ac1 * vc
close(dvo1, -2.36, 3e-3)
close(Ad * vd, -3.85, 2e-3)
# 直接把 v1、v2 代入两管方程，结果应与分解法相同（线性叠加）
c1x, c2x, _ = pair_ss(v1, v2, REE)
close(c1x, dvo1, 1e-9); close(c1x - c2x, Ad * vd, 1e-9)
# 大信号：每管电流变化
di_lin = gm * vd / 2
di_big = IEE / 2 * math.tanh(vd / (2 * VT))
close(di_lin, 0.1923, 1e-3); close(di_big, 0.1834, 1e-3)
close(1 - di_big / di_lin, 0.047, 0.05)
# 共模 1 V 的大信号核对：I_EE → (12 + 1 − 0.7)/11.3
close(((Vee + 1 - 0.7) / REE / 2 - 0.5) * RC, 0.442, 3e-3)
print("card13: vd, vc, dvo1, vod, di_lin, di_big =", vd, vc, dvo1, Ad * vd, di_lin, di_big)

# 尾电流源 r_o = 1 MΩ
_, _, _ = pair_ss(1, 1, 1000)
Ac1_cs = pair_ss(1, 1, 1000)[0]
close(Ac1_cs, -0.00495, 2e-3)
CMRR_cs = abs(Ad1 / Ac1_cs)
close(CMRR_cs, 1.94e4, 3e-3); close(20 * math.log10(CMRR_cs), 85.8, 1e-3)
close(gm * 1000, CMRR_cs, 0.02)        # CMRR ≈ g_m R_EE
print("current-source tail: Ac1, CMRR, dB =", Ac1_cs, CMRR_cs, 20 * math.log10(CMRR_cs))

# ---------------------------------------------------------------- 有源负载：I_T = 0.2 mA，V_A = 100 V
IT, VA = 0.2, 100
gm_a = IT / 2 / VT
ro = VA / (IT / 2)
Ad_act = gm_a * par(ro, ro)
close(gm_a, 3.846, 1e-3); close(ro, 1000, 1e-9); close(Ad_act, 1923, 1e-3)
close(20 * math.log10(Ad_act), 65.7, 1e-3)
# 节点方程核对：T1..T4（忽略 T3、T4 基极电流），镜像节点 m、输出 o，r_o 跨接在 c–e
vm, vo, ve = sp.symbols("vm vo ve")
gm3 = gm_a
vd_ = 1
eqs = [
    # 镜像节点 m（T1 集电极 = T3 二极管）：T3 二极管导纳 g_m3 + 1/r_o3，T1 拉走 g_m(v1−ve) + (vm−ve)/r_o1
    -(gm3 + 1 / ro) * vm - (gm_a * (vd_ / 2 - ve) + (vm - ve) / ro),
    # 输出节点 o：T4 供出 −g_m3 vm（镜像），r_o4 到交流地，T2 拉走 g_m(v2−ve) + (vo−ve)/r_o2
    -gm3 * vm - vo / ro - (gm_a * (-vd_ / 2 - ve) + (vo - ve) / ro),
    # 射极节点（理想尾电流源，交流开路）
    gm_a * (vd_ / 2 - ve) + (vm - ve) / ro + gm_a * (-vd_ / 2 - ve) + (vo - ve) / ro
    + (vd_ / 2 - ve) / (100 / gm_a) + (-vd_ / 2 - ve) / (100 / gm_a),
]
s = sp.solve(eqs, [vm, vo, ve], dict=True)[0]
Ad_node = float(s[vo])
close(Ad_node, 1923, 0.02)
print("active load: gm, ro, Ad (formula, nodal) =", gm_a, ro, Ad_act, Ad_node)

# ---------------------------------------------------------------- 失调：反相放大 R1=10k, Rf=100k
UIO, IIB, IIO = 2e-3, 80e-6, 20e-6     # V, mA
R1, Rf = 10, 100


def offset_out(Rp, IBp, IBm, Uio=UIO, r1=R1, rf=Rf):
    """输入接地；U_IO 串在同相端（+ 接运放），I_B 流入两输入端。解反相端 KCL。"""
    Uo = sp.Symbol("Uo")
    up = Uio - IBp * Rp
    s = sp.solve(sp.Eq((0 - up) / r1 + (Uo - up) / rf, IBm), Uo)[0]
    return float(s)


# 无平衡电阻：最坏情况 U_IO 与 I_B− 同号，I_B− = I_IB + I_IO/2
worst0 = offset_out(0, 0, IIB + IIO / 2)
close(worst0 * 1e3, 31.0, 1e-3)
close(11 * UIO * 1e3, 22.0, 1e-9); close(IIB * Rf * 1e3, 8.0, 1e-9)
Rp = par(R1, Rf)
close(Rp, 9.09, 1e-3)
worstp = offset_out(Rp, IIB - IIO / 2, IIB + IIO / 2)
close(worstp * 1e3, 24.0, 1e-3)
close(offset_out(Rp, IIB, IIB) * 1e3, 22.0, 1e-6)       # I_IO = 0 时偏置电流误差完全抵消
print("offset: no Rp worst, with Rp worst (mV) =", worst0 * 1e3, worstp * 1e3)

# ---------------------------------------------------------------- SR、GBW
close(2 * math.pi * 1e5 * 2 / 1e6, 1.256, 1e-3)               # 图卡 14：1.26 V/µs
fp = 0.5e6 / (2 * math.pi * 10)
close(fp, 7958, 1e-3)
# 例：GBW=1 MHz, SR=0.5 V/µs, 同相增益 10，20 kHz、5 V 峰值正弦
close(1e6 / 10, 1e5, 1e-12)
close(2 * math.pi * 20e3 * 5 / 1e6, 0.628, 1e-3)
close(0.5e6 / (2 * math.pi * 20e3), 3.98, 1e-3)
print("SR/GBW: fp =", fp)

# ================================================================ 练习
# 2. v1 = 2.005, v2 = 1.995；A_d1 = −50，A_c1 = −0.05
vd2, vc2 = 2.005 - 1.995, (2.005 + 1.995) / 2
close(vd2, 0.01, 1e-9); close(vc2, 2.0, 1e-12)
close(-50 * vd2 - 0.05 * vc2, -0.6, 1e-9)
close(20 * math.log10(50 / 0.05), 60, 1e-12)

# 3. V_CC=V_EE=15，R_C=15k，I_T=0.4 mA（r_o=500k），β=150，R_L=30k 接在两集电极之间
gm3_, rpi3 = 0.2 / VT, 150 / (0.2 / VT)
close(gm3_, 7.692, 1e-3); close(rpi3, 19.5, 1e-3)
close(15 - 0.2 * 15, 12, 1e-12)
c1, c2, ib = pair_ss(0.5, -0.5, 500, RL_between=30, rc=15, g=gm3_, rp=rpi3)
close(c1 - c2, -57.7, 1e-3); close(c1 - c2, -gm3_ * par(15, 15), 1e-9)
close(1 / ib, 39.0, 1e-3)
c1c, c2c, _ = pair_ss(1, 1, 500, RL_between=30, rc=15, g=gm3_, rp=rpi3)
close(c1c, -0.0149, 3e-3); close(c1c - c2c + 1, 1, 1e-12)
print("ex3: Ad, Rid, Ac1 =", c1 - c2, 1 / ib, c1c)

# 4. 同相放大 R1=1k，Rf=99k，U_IO=1 mV，I_IB=100 nA，I_IO=10 nA
o_bal = offset_out(par(1, 99), 100e-6 - 5e-6, 100e-6 + 5e-6, Uio=1e-3, r1=1, rf=99)
close(o_bal * 1e3, 100.99, 1e-4)
o_nobal = offset_out(0, 0, 105e-6, Uio=1e-3, r1=1, rf=99)
close(o_nobal * 1e3, 110.4, 1e-3)
print("ex4:", o_bal * 1e3, o_nobal * 1e3)

# 5. A_0 = 2e5，GBW = 1 MHz，SR = 0.5 V/µs；反相 −10；2 V 峰值
close(1e6 / 2e5, 5, 1e-12)
close(1e6 / 11 / 1e3, 90.9, 1e-3)
close(0.5e6 / (2 * math.pi * 2) / 1e3, 39.8, 1e-3)
close(0.5e6 / (2 * math.pi * 1e6 / 11), 0.875, 2e-3)
print("diffamp: all checks passed")
