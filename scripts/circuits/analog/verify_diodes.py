"""模电·半导体与二极管 —— 独立验算（指数模型用牛顿迭代，分段模型用"假设—验证"逐一枚举）。"""
import itertools
import math

VT = 0.026


def close(a, b, tol=1e-3):
    assert abs(a - b) <= tol * max(1, abs(b)), (a, b)


# ================= 1. 半导体 =================
ni, NA, ND = 1.5e10, 1e17, 1e16
pn = ni**2 / ND
close(pn, 2.25e4)
Vho = VT * math.log(NA * ND / ni**2)
close(Vho, 0.757, 2e-3)
print("minority p:", pn, " V_ho:", Vho)

# ================= 2. 指数特性 =================
close(VT * math.log(10) * 1e3, 59.9, 1e-3)          # 60 mV/十倍频程
Is = 1e-3 / math.exp(0.7 / VT)                       # 0.7 V 时 1 mA 的管子
close(1e-3 * math.exp(0.1 / VT) * 1e3, 46.8, 2e-3)   # 0.8 V 时约 47 mA
assert 1e-16 < Is < 1e-14
print("I_S for 0.7V@1mA:", Is, " i(0.8V) mA:", 1e-3 * math.exp(0.1 / VT) * 1e3)


def diode_exp(V, R, Is=1e-14):
    """V–R–二极管串联，牛顿法解 (V - v)/R = Is(e^{v/VT}-1)。"""
    v = 0.6
    for _ in range(100):
        f = (V - v) / R - Is * (math.exp(v / VT) - 1)
        df = -1 / R - Is / VT * math.exp(v / VT)
        v -= f / df
    return v, (V - v) / R


# 例：三种模型比较 V=2 V，R=100 Ω
I_ideal = 2 / 100
I_cvd = (2 - 0.7) / 100
v, I_exp = diode_exp(2, 100)
close(I_ideal * 1e3, 20); close(I_cvd * 1e3, 13); close(I_exp * 1e3, 12.75, 2e-3); close(v, 0.725, 2e-3)
print("models: ideal", I_ideal * 1e3, "cvd", I_cvd * 1e3, "exp", I_exp * 1e3, v)
# 同一电路 V=5 V, R=1 kΩ
v5, I5 = diode_exp(5, 1000)
close(I5 * 1e3, 4.30, 2e-3)
print("5V/1k exp:", v5, I5 * 1e3)

# 例：图卡 04 改：串 10 kΩ，V_BR = 50 V
close((5 - 0.7) / 10, 0.43)          # mA
close((60 - 50) / 10, 1.0)           # mA（反向）

# 例：小信号
ID = (5 - 0.7) / 4.3
close(ID, 1.0)
rd = VT / (ID * 1e-3)
close(rd, 26)
dv = 0.1 * rd / (4300 + rd)
close(dv * 1e3, 0.601, 2e-3)
print("small signal: rd", rd, "dv mV", dv * 1e3)


# ================= 3. 两二极管电路（恒压降模型，枚举状态） =================
def two_diode(V1, V2, Vcc=10, R=2, Von=0.7):
    """+Vcc–R–节点 O；D_k 阳极接 O、阴极接 V_k。返回 (VO, I, 状态)。"""
    sols = []
    for s1, s2 in itertools.product((0, 1), repeat=2):
        on = [V for V, s in ((V1, s1), (V2, s2)) if s]
        if on:
            if len(set(on)) > 1:
                continue
            VO = on[0] + Von
        else:
            VO = Vcc                      # 无电流
        I = (Vcc - VO) / R
        ok = I >= -1e-12
        ok &= all((VO - V >= Von - 1e-9) if s else (VO - V < Von - 1e-9) for V, s in ((V1, s1), (V2, s2)))
        # 导通管电流须为正：两管同时导通时平分（对称），单管时全部电流
        if ok and on:
            ok &= I > 0
        if ok and (s1 or s2):
            sols.append((VO, I, (s1, s2)))
    return sols


s = two_diode(0, 3)
assert len(s) == 1 and s[0][2] == (1, 0)
close(s[0][0], 0.7); close(s[0][1], 4.65)
s = two_diode(5, 3)
assert len(s) == 1 and s[0][2] == (0, 1)
close(s[0][0], 3.7); close(s[0][1], 3.15)
s = two_diode(0, 0)
assert s[0][2] == (1, 1)
close(s[0][1] / 2, 2.325)
print("two-diode ok")

# ================= 4. 限幅 =================
th = math.degrees(math.asin(2.7 / 5))
close(th, 32.68)
close((180 - 2 * th) / 360, 0.3184, 2e-3)
print("clip angle", th)

# ================= 5. 稳压管 =================
IZ = (13 - 5) / 2
assert IZ == 4 and 5 * IZ == 20


def zener(VI, R, RL, VZ):
    """返回 (VO, IZ)；R、RL 单位 kΩ，电流 mA。RL=None 表示空载。"""
    Vopen = VI if RL is None else VI * RL / (R + RL)
    if Vopen <= VZ:
        return Vopen, 0.0
    IL = 0 if RL is None else VZ / RL
    return VZ, (VI - VZ) / R - IL


assert zener(13, 2, None, 5) == (5, 4.0)
VO, IZ = zener(13, 2, 2.5, 5)
assert VO == 5; close(IZ, 2.0)
VO, IZ = zener(13, 2, 1.0, 5)
close(VO, 4.333); assert IZ == 0
close(5 / (4 - 1), 1.667)            # R_L,min (I_Zmin = 1 mA)
print("zener ok")

# ================= 练习 =================
close((5 - 2) / 10e-3, 300)
close((5 - 2) * 10e-3 * 1e3, 30)     # mW
# 4. 稳压管限流电阻范围：VI 10~14 V，VZ=6 V，RL=1.2k，IZmin=1 mA，IZM=25 mA
IL = 6 / 1.2
close(IL, 5)
Rmax = (10 - 6) / (IL + 1)
Rmin = (14 - 6) / (IL + 25)
close(Rmax * 1e3, 666.7); close(Rmin * 1e3, 266.7)
# 5.
close(0.65 - 2e-3 * 50, 0.55)
close(VT / 2e-3, 13)
print("diodes: all checks passed")
