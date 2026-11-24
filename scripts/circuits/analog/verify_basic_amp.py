"""模电·基本放大电路 —— 独立验算。

直流：BJT 用"V_BE=0.7 V + I_C=βI_B"模型，对原电路（不做戴维南化简）列节点方程求 Q 点；
交流：用 hybrid-π 小信号模型（忽略 r_o、r_bb'）对各组态列节点方程，求 A_v、R_i、R_o。
电阻 kΩ、电流 mA、电压 V、电导 mS。
"""
import math
import sympy as sp

VT = 0.026


def close(a, b, tol=5e-3, rel=True):
    a, b = float(a), float(b)
    err = abs(a - b) / (abs(b) if rel and b != 0 else 1)
    assert err < tol, (a, b)


def par(*rs):
    return 1 / sum(1 / r for r in rs)


# ---------------------------------------------------------------- Q 点（分压式偏置）
def q_point(Vcc, RB1, RB2, RC, RE, beta, VBE=0.7):
    """节点电压 VB、VE、VC 与 IB 未知，直接对原电路列 KCL。"""
    VB, VE, VC, IB = sp.symbols("VB VE VC IB")
    eqs = [
        (Vcc - VB) / RB1 - VB / RB2 - IB,            # 基极节点
        VB - VE - VBE,                               # 发射结
        (1 + beta) * IB - VE / RE,                   # 射极节点
        (Vcc - VC) / RC - beta * IB,                 # 集电极节点（RC=0 时另行处理）
    ] if RC else [
        (Vcc - VB) / RB1 - VB / RB2 - IB, VB - VE - VBE, (1 + beta) * IB - VE / RE, VC - Vcc]
    s = sp.solve(eqs, [VB, VE, VC, IB], dict=True)[0]
    IB_ = float(s[IB]); IC = beta * IB_
    return dict(IB=IB_, IC=IC, IE=(1 + beta) * IB_, VCE=float(s[VC] - s[VE]), VB=float(s[VB]))


# 主例：V_CC=12, R_B1=40k, R_B2=10k, R_C=3k, R_E=1k, β=100
Vcc, RB1, RB2, RC, RE, RL, beta, Rs = 12, 40, 10, 3, 1, 6, 100, 1
VBB, RBB = Vcc * RB2 / (RB1 + RB2), par(RB1, RB2)
assert VBB == 2.4 and abs(RBB - 8) < 1e-12
Q = q_point(Vcc, RB1, RB2, RC, RE, beta)
close(Q["IB"], 0.0156, 3e-3); close(Q["IC"], 1.56, 3e-3); close(Q["IE"], 1.575, 3e-3); close(Q["VCE"], 5.75, 2e-3)
# 估算法
IE_est = (VBB - 0.7) / RE
close(IE_est, 1.7); close(Vcc - IE_est * (RC + RE), 5.2)
print("Q exact:", {k: round(v, 4) for k, v in Q.items()}, " estimate IE=1.7 VCE=5.2")
ICQ, VCEQ = Q["IC"], Q["VCE"]
# 小信号参数
gm = ICQ / VT
rpi = beta / gm
close(gm, 60.0, 2e-3); close(rpi, 1.667, 2e-3)
print("gm, rpi:", gm, rpi)

# 负载线与最大不失真幅度（V_CE(sat)=0.2 V）
VCES = 0.2
RLp = par(RC, RL)
assert abs(RLp - 2) < 1e-12
v_ac0 = VCEQ + ICQ * RLp
close(v_ac0, 8.87, 2e-3)
Uom = min(VCEQ - VCES, ICQ * RLp)
close(VCEQ - VCES, 5.55, 2e-3); close(ICQ * RLp, 3.12, 2e-3); close(Uom, 3.12, 2e-3)
print("ac load line intercept, Uom:", v_ac0, Uom)


# ---------------------------------------------------------------- 小信号：通用节点求解
def ce_ss(RE_unbyp, RLp_, Rb=RBB, rpi_=rpi, gm_=gm, Rs_=Rs):
    """共射：b、e、c 三个节点 + 信号源（v_s 经 R_s 接 b 前的节点 i）。返回 A_v, R_i, A_vs, R_o。"""
    vs, vi, vb, ve, vc = sp.symbols("vs vi vb ve vc")
    # 输入端 vi=vb（耦合电容短路）
    eqs = [
        (vs - vi) / Rs_ - vi / Rb - (vi - ve) / rpi_,                       # 节点 i(=b)
        ((vi - ve) / rpi_ + gm_ * (vi - ve) - ve / RE_unbyp) if RE_unbyp else ve,   # 节点 e
        gm_ * (vi - ve) + vc / RLp_,                                          # 节点 c
    ]
    s = sp.solve(eqs, [vi, ve, vc], dict=True)[0]
    Av = float(s[vc] / s[vi]); Avs = float(s[vc] / vs)
    Ri = float(s[vi] / ((vs - s[vi]) / Rs_))
    return Av, Ri, Avs


Av, Ri, Avs = ce_ss(0, RLp)
close(Av, -120, 2e-3); close(Ri, 1.379, 2e-3); close(Avs, -69.6, 2e-3)
print("CE bypassed: Av, Ri, Avs =", Av, Ri, Avs)
Av2, Ri2, Avs2 = ce_ss(RE, RLp)
close(Av2, -1.948, 2e-3); close(Ri2, 7.42, 2e-3); close(Avs2, -1.717, 3e-3)
close(Av2, -beta * RLp / (rpi + (1 + beta) * RE), 1e-9)
print("CE unbypassed: Av, Ri, Avs =", Av2, Ri2, Avs2)
# R_o：v_s=0，在集电极加测试电压（g_m v_π 是理想电流源，与 R_C 无关）→ R_o = R_C
print("CE Ro = RC =", RC)

# ---------------------------------------------------------------- 共集（同一偏置，R_C=0，R_L=1k，R_s=1k）
Qcc = q_point(Vcc, RB1, RB2, 0, RE, beta)
close(Qcc["IC"], ICQ, 1e-9); close(Qcc["VCE"], 10.42, 2e-3)
RLcc = 1
vs, vb, ve = sp.symbols("vs vb ve")
REp = par(RE, RLcc)
s = sp.solve([(vs - vb) / Rs - vb / RBB - (vb - ve) / rpi,
              (vb - ve) / rpi + gm * (vb - ve) - ve / REp], [vb, ve], dict=True)[0]
Av_cc = float(s[ve] / s[vb]); Ri_cc = float(s[vb] / ((vs - s[vb]) / Rs))
# R_o：v_s 置零，在射极加测试电压 vx，求流入电流
vx, vb2 = sp.symbols("vx vb2")
sb = sp.solve([-vb2 / par(Rs, RBB) - (vb2 - vx) / rpi], [vb2], dict=True)[0]
ix = vx / RE - ((sb[vb2] - vx) / rpi + gm * (sb[vb2] - vx))
Ro_cc = float(vx / ix)
close(Av_cc, 0.968, 2e-3); close(Ri_cc, 6.94, 2e-3); close(Ro_cc * 1000, 24.7, 3e-3)
print("CC: Av, Ri, Ro(Ω) =", Av_cc, Ri_cc, Ro_cc * 1000)

# ---------------------------------------------------------------- 共基（同一偏置，基极旁路，R_C=3k，R_L=6k，R_s=50Ω）
Rs_cb = 0.05
vs, ve, vc = sp.symbols("vs ve vc")
# 基极交流接地：v_π = 0 − v_e
s = sp.solve([(vs - ve) / Rs_cb - ve / RE + (0 - ve) / rpi + gm * (0 - ve),
              gm * (0 - ve) + vc / RLp], [ve, vc], dict=True)[0]
Av_cb = float(s[vc] / s[ve]); Ri_cb = float(s[ve] / ((vs - s[ve]) / Rs_cb)); Avs_cb = float(s[vc] / vs)
close(Av_cb, 120, 2e-3); close(Ri_cb * 1000, 16.2, 3e-3); close(Avs_cb, 29.4, 3e-3)
print("CB: Av, Ri(Ω), Avs =", Av_cb, Ri_cb * 1000, Avs_cb)

# ---------------------------------------------------------------- 图卡 08 例（射极接地，Q 给定）
Vcc8, Rc8, IC8, VCE8 = 12, 3, 2, 6
assert Vcc8 - IC8 * Rc8 == VCE8 and Vcc8 / Rc8 == 4
RLp8 = par(3, 3)
assert RLp8 == 1.5
assert VCE8 + IC8 * RLp8 == 9
assert min(VCE8 - VCES, IC8 * RLp8) == 3.0
close(min(VCE8 - VCES, IC8 * Rc8), 5.8)
# 带负载时使摆幅最大的 Q 点：V_CEQ − V_CES = I_CQ R_L'，V_CEQ = 12 − 3 I_CQ
I = sp.Symbol("I")
Iopt = float(sp.solve(sp.Eq(12 - 3 * I - VCES, 1.5 * I), I)[0])
close(Iopt, 2.622, 2e-3); close(12 - 3 * Iopt, 4.133, 2e-3); close(1.5 * Iopt, 3.93, 2e-3)
print("card08: Uom with RL = 3 V; optimum Q:", Iopt, 12 - 3 * Iopt, 1.5 * Iopt)

# 图卡 09 例：A_v = −g_m (R_C∥R_L) = −40 mS × 2k
assert -40 * 2 == -80

# ---------------------------------------------------------------- 共源（V_DD=12, R_G1=2M, R_G2=1M, R_S=1k, R_D=5k, K_n=1 mA/V², V_th=2 V）
Kn, Vth = 1.0, 2.0
VG = 12 * 1 / 3
ID, VGS = sp.symbols("ID VGS", positive=True)
sols = sp.solve([ID - Kn * (VGS - Vth) ** 2, VGS - (VG - ID * 1)], [ID, VGS], dict=True)
sol = [x for x in sols if x[VGS] > Vth][0]           # 舍去 V_GS < V_th 的增根
ID_, VGS_ = float(sol[ID]), float(sol[VGS])
assert abs(ID_ - 1) < 1e-12 and abs(VGS_ - 3) < 1e-12
VDS = 12 - ID_ * (5 + 1)
assert abs(VDS - 6) < 1e-12 and VDS >= VGS_ - Vth
gm_fet = 2 * Kn * (VGS_ - Vth)
assert abs(gm_fet - 2) < 1e-12 and abs(gm_fet - 2 * math.sqrt(Kn * ID_)) < 1e-12
RDp = par(5, 5)
close(-gm_fet * RDp, -5, 1e-9)
close(-gm_fet * RDp / (1 + gm_fet * 1), -1.667, 2e-3)
close(par(2000, 1000), 666.7, 1e-3)
print("CS: ID, VGS, VDS, gm, Av, Av(unbyp) =", ID_, VGS_, VDS, gm_fet, -gm_fet * RDp, -gm_fet * RDp / 3)

# ---------------------------------------------------------------- 电流镜
def mirror_io(Iref, beta_):
    """T1、T2 匹配：I_C1 = I_C2 = I_C，I_REF = I_C + 2 I_C/β。"""
    Ic = sp.Symbol("Ic")
    return float(sp.solve(sp.Eq(Iref, Ic + 2 * Ic / beta_), Ic)[0])


Io = mirror_io(0.5, 100)
close(Io, 0.490, 1e-3)
VA = 100
Io_early = Io * (1 + 2.0 / VA) / (1 + 0.7 / VA)
close(Io_early, 0.4965, 1e-3)
close(VA / Io, 204, 3e-3)
print("mirror: Io, Io(Early, VCE2=2V), ro =", Io, Io_early, VA / Io)
# Widlar：I_REF = 1 mA，I_O = 10 µA
RE_w = VT * math.log(1 / 0.01) / 0.01
close(RE_w, 11.97, 2e-3)
print("Widlar RE (kΩ):", RE_w)
close((15 - 0.7) / 0.01, 1430, 1e-9)          # 基本镜像得 10 µA 需 R≈1.43 MΩ
# 主例的 I_REF：V_CC = 15 V，R = 14.3k → 1 mA，β=100 → 0.980 mA
close((15 - 0.7) / 14.3, 1.0, 1e-9); close(mirror_io(1.0, 100), 0.980, 1e-3)

# ---------------------------------------------------------------- 多级：CE（主例）→ CC（R_L = 1k）
Ri2 = Ri_cc
RL1 = par(RC, Ri2)
Av1 = -gm * RL1
Av2_ = Av_cc
Avt = Av1 * Av2_
close(RL1, 2.095, 2e-3); close(Av1, -125.6, 2e-3); close(Avt, -121.6, 2e-3)
# 第二级输出电阻：其信号源内阻为第一级 R_o = R_C
Ro2 = par(RE, (rpi + par(RC, RBB)) / (1 + beta))
close(Ro2 * 1000, 36.7, 3e-3)
close(-gm * par(RC, 1), -45.0, 2e-3)
print("two-stage: RL1, Av1, Av2, Av, Ro(Ω), direct =", RL1, Av1, Av2_, Avt, Ro2 * 1000, -gm * par(RC, 1))
assert -20 * 0.8 == -16

# ================================================================ 练习
# 2. V_CC=15, R_B1=50k, R_B2=10k, R_C=5.1k, R_E=1.8k, β=80 / 160
Q2 = q_point(15, 50, 10, 5.1, 1.8, 80)
close(2.5, 15 * 10 / 60, 1e-12)
close((2.5 - 0.7) / 1.8, 1.0, 1e-12); close(15 - 1.0 * (5.1 + 1.8), 8.1, 1e-12)
close(Q2["IC"], 0.934, 2e-3); close(Q2["VCE"], 8.53, 2e-3)
Q2b = q_point(15, 50, 10, 5.1, 1.8, 160)
close(Q2b["IC"], 0.966, 2e-3)
close(Q2b["IC"] / Q2["IC"] - 1, 0.034, 0.05)
print("ex2:", Q2["IC"], Q2["VCE"], "β=160:", Q2b["IC"], Q2b["VCE"])

# 3. 主例射极电阻分为 R_E1=0.2k（不旁路）+ R_E2=0.8k（旁路）
Av3, Ri3, _ = ce_ss(0.2, RLp)
close(Av3, -9.15, 2e-3); close(Ri3, 5.86, 2e-3)
sat_lim = (VCEQ - VCES) * RLp / (RLp + 0.2)
close(sat_lim, 5.04, 2e-3)
close(min(sat_lim, ICQ * RLp), 3.12, 2e-3)
print("ex3: Av, Ri, sat-limited swing =", Av3, Ri3, sat_lim)

# 4. 源极跟随器：V_DD=12，R_G1=R_G2=1M，R_S=3k，R_L=3k，K_n=1 mA/V²，V_th=2 V
sols = sp.solve([ID - Kn * (VGS - Vth) ** 2, VGS - (6 - ID * 3)], [ID, VGS], dict=True)
sol = [x for x in sols if x[VGS] > Vth][0]
assert abs(float(sol[ID]) - 1) < 1e-12 and abs(float(sol[VGS]) - 3) < 1e-12
gm4 = 2.0
RSp = par(3, 3)
vg, vs_ = sp.symbols("vg vs_")
s = sp.solve([gm4 * (vg - vs_) - vs_ / RSp], [vs_], dict=True)[0]
Av4 = float(s[vs_] / vg)
close(Av4, 0.75, 1e-9)
Ro4 = par(3, 1 / gm4)
close(Ro4 * 1000, 428.6, 1e-3)
print("ex4: Av, Ro(Ω), Ri =", Av4, Ro4 * 1000, par(1000, 1000))

# 5. β=50：基本镜像 vs 带射极跟随器的电流镜（I_REF=1 mA）
close(mirror_io(1.0, 50), 0.9615, 1e-3)
Ic = sp.Symbol("Ic")
b = 50
# 助推管 T3：其射极电流 = 2I_C/β，基极电流 = 2I_C/(β(1+β))
Io5 = float(sp.solve(sp.Eq(1.0, Ic + 2 * Ic / (b * (1 + b))), Ic)[0])
close(Io5, 0.99922, 1e-5)
print("ex5:", mirror_io(1.0, 50), Io5)
print("basic_amp: all checks passed")
