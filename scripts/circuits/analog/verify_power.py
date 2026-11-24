"""模电·功率放大与直流电源 —— 例题与练习数值的独立验算。

    cd scripts/circuits/analog && ../../../.venv/bin/python verify_power.py
"""
import math

import numpy as np
import sympy as sp

pi = math.pi


def near(a, b, tol=0.01):
    """相对误差 tol 内相等（b=0 时用绝对误差）。"""
    assert abs(a - b) <= tol * max(abs(b), 1e-12), (a, b)


# ---------------- 乙类 OCL 公式：由瞬时功率积分推导 ----------------
th, Vcc, Uom, RL = sp.symbols("theta V_CC U_om R_L", positive=True)
iC1 = Uom / RL * sp.sin(th)                       # T1 只在正半周导通
PV = 2 * sp.integrate(Vcc * iC1, (th, 0, sp.pi)) / (2 * sp.pi)        # 两管电源功率
PT1 = sp.integrate((Vcc - Uom * sp.sin(th)) * iC1, (th, 0, sp.pi)) / (2 * sp.pi)
Po = Uom**2 / (2 * RL)
assert sp.simplify(PV - 2 * Vcc * Uom / (sp.pi * RL)) == 0
assert sp.simplify(PT1 - (Vcc * Uom / sp.pi - Uom**2 / 4) / RL) == 0
assert sp.simplify(2 * PT1 - (PV - Po)) == 0
# 满输出时单管管耗 / P_om = (4−π)/(2π)
near(float(sp.simplify(PT1.subs(Uom, Vcc) / (Vcc**2 / (2 * RL)))), 0.137, 3e-3)
# 单管最大管耗
u_star = sp.solve(sp.diff(PT1, Uom), Uom)[0]
assert sp.simplify(u_star - 2 * Vcc / sp.pi) == 0
PT1max = sp.simplify(PT1.subs(Uom, u_star))
assert sp.simplify(PT1max - Vcc**2 / (sp.pi**2 * RL)) == 0
ratio = float(PT1max / (Vcc**2 / (2 * RL)))
near(ratio, 0.2026, 1e-3)
print("P_T1max/P_om =", ratio)


def ocl(V, U, R):
    po = U**2 / (2 * R)
    pv = 2 * V * U / (pi * R)
    return po, pv, po / pv, (pv - po) / 2


# 例 1（图卡例题更正）：±12 V，8 Ω，U_om = 8 V
po, pv, eta, pt = ocl(12, 8, 8)
near(po, 4.0); near(pv, 7.64); near(eta, 0.524, 2e-3); near(pt, 1.82)
near(8 / math.sqrt(2), 5.66)
near(12**2 / 16, 9.0); near(12**2 / (pi**2 * 8), 1.824, 2e-3); near(2 * 12 / pi, 7.64)
print("ex1:", po, pv, eta, pt, 12**2 / (pi**2 * 8))
# 图卡的错误算法：P_in = P_o / η_max
near(4 / (pi / 4), 5.09)

# 例 2：±15 V，8 Ω，V_CES = 1 V，选管 + 散热
Pom = (15 - 1)**2 / 16
near(Pom, 12.25)
near(pi / 4 * 14 / 15, 0.733, 2e-3)
PT1m = 15**2 / (pi**2 * 8)
near(PT1m, 2.85)
near(0.2 * 15**2 / 16, 2.81)
near(15 / 8, 1.875)
Rsa = (150 - 45) / PT1m - 3 - 0.5
near(Rsa, 33.3)
print("ex2:", Pom, PT1m, Rsa)

# 例 3：OTL，单电源 24 V，8 Ω
near((24 / 2)**2 / 16, 9.0)
Cmin = 1 / (2 * pi * 20 * 8)
near(Cmin * 1e6, 995)
print("ex3: Cmin uF", Cmin * 1e6)

# 达林顿：β ≈ β1 β2，精确 β1+β2+β1β2
near(50 * 40 + 50 + 40, 2090)

# ---------------- 整流 ----------------
V2 = 1.0
t = np.linspace(0, 2 * pi, 200001)
hw = np.mean(np.clip(np.sqrt(2) * V2 * np.sin(t), 0, None))
fw = np.mean(np.abs(np.sqrt(2) * V2 * np.sin(t)))
near(hw, 0.45, 2e-3); near(fw, 0.90, 2e-3)
near(2 * math.sqrt(2) / pi, 0.9003, 1e-4)

# 例 4（图卡例题补全）：桥式 + 电容，V_2 = 7.5 V，50 Hz，I_L = 0.1 A，C = 1000 µF
Vp = math.sqrt(2) * 7.5 - 2 * 0.7
near(Vp, 9.21, 2e-3)
Vr = 0.1 / (100 * 1000e-6)
near(Vr, 1.0)
Vmin = Vp - Vr
near(Vmin, 8.21, 2e-3)
Vavg = Vp - Vr / 2
near(Vavg, 8.71, 2e-3)
P = (Vavg - 5) * 0.1
near(P, 0.371, 3e-3)
# 电网 −10 %
Vp_low = 0.9 * math.sqrt(2) * 7.5 - 1.4
near(Vp_low, 8.15, 2e-3); near(Vp_low - 1, 7.15, 3e-3)
print("ex4:", Vp, Vmin, Vavg, P, Vp_low - 1)
# 数值仿真：理想二极管桥 + RC 放电，等效负载 R = V/I ≈ 87 Ω，看纹波 ≈ 1 V 的量级
RLs = Vavg / 0.1
dt = 1e-6
tt = np.arange(0, 0.1, dt)
vr = Vp * np.abs(np.sin(2 * pi * 50 * tt))
v = 0.0; out = np.empty_like(tt)
for i, x in enumerate(vr):
    v = x if x >= v else v - v / (RLs * 1000e-6) * dt
    out[i] = v
m = tt > 0.06
sim_r = out[m].max() - out[m].min()
assert 0.85 < sim_r < 1.0, sim_r
print("   simulated ripple:", sim_r)

# 例 5：稳压管限流电阻
VImin, VImax, VZ = 10.8, 13.2, 6.0
Rmax = (VImin - VZ) / (5e-3 + 20e-3)
Rmin = (VImax - VZ) / (45e-3 + 0)
near(Rmax, 192); near(Rmin, 160)
R = 180
# 校核：最坏情况 I_Z
near((VImin - VZ) / R - 20e-3, 6.67e-3, 3e-3)
near((VImax - VZ) / R, 40e-3)
near((VImax - VZ)**2 / R, 0.288, 3e-3)
near(VZ * 40e-3, 0.24)
print("ex5:", Rmin, Rmax, (VImin - VZ) / R - 20e-3)

# 例 6：串联稳压：V_REF = 6 V，R1 = 3k，R2 = 2k；V_I = 22 V，I_O ≤ 0.5 A
Vo = sp.Symbol("Vo")
# 误差放大器虚短：V_- = V_O R2/(R1+R2) = V_REF
sol = sp.solve(sp.Eq(Vo * 2 / (3 + 2), 6), Vo)[0]
assert sol == 15
near((22 - 15) * 0.5, 3.5)
near(15 / 22, 0.682, 2e-3)
near(15 + 3, 18)
print("ex6:", sol)

# 例 7：LM317
R1 = 240
R2 = R1 * (12 / 1.25 - 1)
near(R2, 2064)
near(1.25 * (1 + R2 / R1) + 50e-6 * R2, 12.10, 1e-3)
near(1.25 * (1 + 2.0e3 / R1) + 50e-6 * 2.0e3, 11.77, 1e-3)
print("ex7:", R2)

# ================= 练习 =================
# 练习 2：±18 V，8 Ω，V_CES = 2 V
po, pv, eta, pt = ocl(18, 16, 8)
near(po, 16); near(pv, 22.92); near(eta, 0.698, 2e-3); near(pt, 3.46)
near(18**2 / (pi**2 * 8), 4.10)
near(36, 2 * 18); near(18 / 8, 2.25)
print("ex-2:", po, pv, eta, pt)

# 练习 3：桥式 + 电容，V_2 = 15 V，R_L = 100 Ω
VO = 1.2 * 15
near(VO, 18); near(VO / 100, 0.18); near(VO / 100 / 2, 0.09)
near(math.sqrt(2) * 15, 21.2)
near(5 * 0.02 / (2 * 100) * 1e6, 500)
near(0.18 / (100 * 1000e-6), 1.8)
print("ex-3 ok")

# 练习 4：7805 散热器
P = (12 - 5) * 1.0
near(P, 7)
near(25 + P * 65, 480)
near((125 - 40) / P - 5 - 0.5, 6.64, 2e-3)
print("ex-4:", (125 - 40) / P - 5.5)

# 练习 5：LM317 + 5 kΩ 电位器
near(1.25 * (1 + 5000 / 240), 27.29, 1e-3)
near(1.25 * (1 + 5000 / 240) + 50e-6 * 5000, 27.54, 1e-3)
near(27.29 + 3, 30.3, 2e-3)
# V_BE 倍增器（文中）：V = 0.7 (1 + R1/R2)
near(0.7 * (1 + 1.0 / 1.0), 1.4)

print("power: all checks passed")
