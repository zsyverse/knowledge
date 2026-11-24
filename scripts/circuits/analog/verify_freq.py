"""模电·频率响应 —— 独立验算。

一阶 RC、放大器传递函数直接算复数；共射电路的 f_L、f_H 用完整小信号电路（含 C_1、C_2、C_E、C_π、C_μ）
列节点导纳矩阵逐频求解，再二分求 −3 dB 点，与"主导极点/米勒近似"对比。
"""
import math
import numpy as np

TAU = 2 * math.pi


def close(a, b, tol=5e-3):
    assert abs(a - b) <= tol * abs(b), (a, b)


def db(x):
    return 20 * math.log10(abs(x))


# ---------------------------------------------------------------- 例 1：一阶 RC（图卡 11）
R, C = 1e3, 0.1e-6
fc = 1 / (TAU * R * C)
close(fc, 1591.5, 1e-4)
for k, lp_db, lp_ph, hp_db, hp_ph in ((0.1, -0.043, -5.71, -20.04, 84.29), (1, -3.01, -45, -3.01, 45),
                                      (10, -20.04, -84.29, -0.043, 5.71)):
    x = 1j * k
    HL, HH = 1 / (1 + x), x / (1 + x)
    close(db(HL), lp_db, 1e-2); close(math.degrees(np.angle(HL)), lp_ph, 1e-3)
    close(db(HH), hp_db, 1e-2); close(math.degrees(np.angle(HH)), hp_ph, 1e-3)
print("RC fc =", fc)


# ---------------------------------------------------------------- 例 2：A = −100 /((1 − j f_L/f)(1 + j f/f_H))
def A2(f, Am=-100, fL=20, fH=1e6):
    return Am / ((1 - 1j * fL / f) * (1 + 1j * f / fH))


def phase_unwrapped(f):
    # −180° + arctan(f_L/f) − arctan(f/f_H)
    return -180 + math.degrees(math.atan(20 / f)) - math.degrees(math.atan(f / 1e6))


for f, mag_db, ph in ((2, 19.96, -95.7), (20, 36.99, -135), (1e3, 40.0, -178.9), (1e6, 36.99, -225), (1e7, 19.96, -264.3)):
    close(db(A2(f)), mag_db, 1e-3)
    close(phase_unwrapped(f), ph, 2e-3)
    # 与复数辐角一致（模 360°）
    assert abs(((math.degrees(np.angle(A2(f))) - phase_unwrapped(f) + 180) % 360) - 180) < 1e-6
print("ex2 ok")

# ---------------------------------------------------------------- 共射电路（basic-amplifiers 例 4 参数）
Vcc, RB1, RB2, RC, RE, RL, beta, Rs = 12, 40e3, 10e3, 3e3, 1e3, 6e3, 100, 1e3
RB = RB1 * RB2 / (RB1 + RB2)
IB = (2.4 - 0.7) / (RB + (1 + beta) * RE)
IC = beta * IB
gm = IC / 0.026
rpi = beta / gm
close(gm * 1e3, 60.0, 2e-3); close(rpi, 1667, 2e-3)
C1v, C2v, CEv = 10e-6, 10e-6, 100e-6
fT, Cmu = 300e6, 2e-12
Cpi = gm / (TAU * fT) - Cmu
close(Cpi * 1e12, 29.8, 3e-3)
fbeta = 1 / (TAU * rpi * (Cpi + Cmu))
close(fbeta / 1e6, 3.0, 3e-3)


def ce_gain(f, cap1=C1v, cap2=C2v, capE=CEv, cpi=Cpi, cmu=Cmu):
    """节点：i(R_s 与 C_1 之间)、b、e、c、o。返回 v_o / v_s。"""
    s = 1j * TAU * f
    Y = np.zeros((5, 5), complex)
    I = np.zeros(5, complex)
    i, b, e, c, o = range(5)

    def g(n1, n2, y):
        Y[n1, n1] += y
        if n2 is not None:
            Y[n2, n2] += y
            Y[n1, n2] -= y
            Y[n2, n1] -= y

    g(i, None, 1 / Rs); I[i] += 1 / Rs                 # v_s = 1 经 R_s 注入
    g(i, b, s * cap1 if cap1 else 1e9)
    g(b, None, 1 / RB)
    g(b, e, 1 / rpi + s * cpi)
    g(b, c, s * cmu)
    g(e, None, 1 / RE + (s * capE if capE else 0) if capE != "short" else 1e9)
    g(c, None, 1 / RC)
    g(c, o, s * cap2 if cap2 else 1e9)
    g(o, None, 1 / RL)
    # VCCS g_m v_be 由 c 流向 e：c 节点流出 +g_m(vb−ve)，e 节点流入
    Y[c, b] += gm; Y[c, e] -= gm
    Y[e, b] -= gm; Y[e, e] += gm
    v = np.linalg.solve(Y, I)
    return v[o]


def corner(fun, lo, hi, ref):
    target = abs(ref) / math.sqrt(2)
    flo = abs(fun(lo)) < target
    for _ in range(200):
        m = math.sqrt(lo * hi)
        if (abs(fun(m)) < target) == flo:
            lo = m
        else:
            hi = m
    return math.sqrt(lo * hi)


Amid = ce_gain(10e3)
close(abs(Amid), 69.6, 2e-3)
# 低频：各电容单独作用时的转折频率
fL1 = 1 / (TAU * (Rs + RB * rpi / (RB + rpi)) * C1v)
fL2 = 1 / (TAU * (RC + RL) * C2v)
Rth_b = Rs * RB / (Rs + RB)
RE_eq = 1 / (1 / RE + (1 + beta) / (rpi + Rth_b))
fLE = 1 / (TAU * RE_eq * CEv)
close(fL1, 6.69, 2e-3); close(fL2, 1.77, 2e-3); close(RE_eq, 24.7, 3e-3); close(fLE, 64.5, 2e-3)
fL_est = 1.1 * math.sqrt(fL1 ** 2 + fL2 ** 2 + fLE ** 2)
fL_exact = corner(lambda f: ce_gain(f, cpi=0, cmu=0), 0.1, 1e4, abs(ce_gain(1e4, cpi=0, cmu=0)))
close(fL_est, 71.3, 2e-3); close(fL_exact, 69.5, 2e-3)
print("fL1, fL2, fLE, est, exact =", fL1, fL2, fLE, fL_est, fL_exact)
assert 64 < fL_exact < 72

# 高频：米勒近似
Av_bc = -gm * (RC * RL / (RC + RL))
CM = Cmu * (1 - Av_bc)
Cin = Cpi + CM
Rp = 1 / (1 / rpi + 1 / Rs + 1 / RB)
fH_miller = 1 / (TAU * Rp * Cin)
close(CM * 1e12, 242, 3e-3); close(Cin * 1e12, 271.8, 3e-3); close(Rp, 580, 3e-3); close(fH_miller / 1e6, 1.01, 5e-3)
fHo = 1 / (TAU * 2e3 * Cmu * (1 - 1 / Av_bc))
close(fHo / 1e6, 39.5, 1e-2)
fH_exact = corner(lambda f: ce_gain(f, cap1="", cap2="", capE="short"), 1e4, 1e9,
                  abs(ce_gain(1e3, cap1="", cap2="", capE="short")))
print("Cpi, CM, Cin, R', fH(Miller), fHo, fH(exact) =", Cpi, CM, Cin, Rp, fH_miller, fHo, fH_exact)
assert abs(fH_exact - fH_miller) / fH_miller < 0.1
close(120 * fH_miller / 1e6, 121, 1e-2)
close(abs(Amid) * fH_exact / 1e6, 69, 1e-2)       # 源电压增益带宽积

# ---------------------------------------------------------------- 图卡 12
assert 2 * (1 + 50) == 102
close(1 - math.exp(-1), 0.632, 1e-3)
tau = 10e-9
tr = tau * math.log(9)
close(tr * 1e9, 22.0, 2e-3)
close(0.35 / 22e-9 / 1e6, 15.9, 2e-3); close(1 / (TAU * tau) / 1e6, 15.9, 2e-3)
close(math.log(10), 2.303, 1e-3); close(math.log(10 / 9), 0.105, 1e-2)

# ---------------------------------------------------------------- 多级：n 级相同
def shrink(n):
    return math.sqrt(2 ** (1 / n) - 1)


close(1e6 * shrink(2) / 1e6, 0.644, 1e-3); close(1e6 * shrink(3) / 1e6, 0.510, 1e-3)
close(20 / shrink(2), 31.1, 2e-3); close(20 / shrink(3), 39.2, 2e-3)
# 直接数值验证：两级 −3 dB 点
fH2 = corner(lambda f: 1 / (1 + 1j * f / 1e6) ** 2, 1e3, 1e8, 1)
close(fH2 / 1e6, 0.644, 1e-3)
print("multistage:", shrink(2), shrink(3))

# ---------------------------------------------------------------- 阶跃：平顶降落与上升时间
fL, tp = 10, 1e-3
close(TAU * fL * tp, 0.0628, 1e-3)
close(1 - math.exp(-TAU * fL * tp), 0.0609, 2e-3)
close(0.35 / 1e6 * 1e6, 0.35, 1e-9)
close(0.01 / (TAU * 1e-3), 1.59, 2e-3)

# ================================================================ 练习
# 2. R=2k, C=10nF
fc2 = 1 / (TAU * 2e3 * 10e-9)
close(fc2, 7958, 1e-3)
close(db(1 / (1 + 1j * 100e3 / fc2)), -22.0, 3e-3)
close(fc2 * math.tan(math.radians(30)), 4595, 1e-3)
close(-20 * math.log10(100e3 / fc2), -21.98, 1e-3)
print("ex2:", fc2, db(1 / (1 + 1j * 100e3 / fc2)), fc2 * math.tan(math.radians(30)))


# 3. A(jf) = 100 (j f/50) / ((1 + j f/50)(1 + j f/2e5)(1 + j f/2e6))
def A3(f):
    x = 1j * f
    return 100 * (x / 50) / ((1 + x / 50) * (1 + x / 2e5) * (1 + x / 2e6))


fH3 = corner(A3, 1e4, 1e8, 100)
fL3 = corner(A3, 1, 1e3, 100)
close(fH3 / 1e3, 198, 2e-3); close(fL3, 50.0, 2e-3)
g20 = db(A3(20e6))
close(40 - 20 * 1 - 40 * 1, -20, 1e-12)
print("ex3: fL, fH, |A(20MHz)| dB =", fL3, fH3, g20)

# 4. CS：g_m=2 mS，R_D'=5k，C_gs=4 pF，C_gd=1 pF，R_sig=100k / 10k
Av4 = -2e-3 * 5e3
Cin4 = 4e-12 + 1e-12 * (1 - Av4)
close(Cin4 * 1e12, 15, 1e-9)
close(1 / (TAU * 100e3 * Cin4) / 1e3, 106.1, 2e-3)
close(1 / (TAU * 10e3 * Cin4) / 1e6, 1.061, 2e-3)
close(1 / (TAU * 5e3 * 1e-12 * (1 - 1 / Av4)) / 1e6, 28.9, 3e-3)

# 5. 三级相同：A=−20，f_L=50 Hz，f_H=200 kHz
assert (-20) ** 3 == -8000
close(db(8000), 78.06, 1e-3); close(3 * db(20), 78.06, 1e-3)
close(200e3 * shrink(3) / 1e3, 102.0, 2e-3); close(50 / shrink(3), 98.1, 2e-3)
close(0.35 / (200e3 * shrink(3)) * 1e6, 3.43, 3e-3)
print("freq: all checks passed")
