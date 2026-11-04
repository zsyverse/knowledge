"""拓展·均匀传输线 —— 独立验算（无损线输入阻抗用 ABCD 链矩阵直接计算后比较）。"""
import cmath
import math


def zin_chain(Zc, beta, l, ZL):
    """无损线 x'=l 处：U = U2 cos βl + j Zc I2 sin βl，I = j U2/Zc sin βl + I2 cos βl（I2 流入负载）。"""
    U2 = ZL * 1.0; I2 = 1.0
    if ZL == math.inf:
        U2, I2 = 1.0, 0.0
    U = U2 * math.cos(beta * l) + 1j * Zc * I2 * math.sin(beta * l)
    I = 1j * U2 / Zc * math.sin(beta * l) + I2 * math.cos(beta * l)
    return U / I


def zin_formula(Zc, beta, l, ZL):
    t = math.tan(beta * l)
    return Zc * (ZL + 1j * Zc * t) / (Zc + 1j * ZL * t)


close = lambda a, b, tol=1e-9: abs(a - b) < tol * max(1, abs(b))

# 例：L0 = 0.25 µH/m, C0 = 100 pF/m, f = 100 MHz
L0, C0, f = 0.25e-6, 100e-12, 100e6
Zc = math.sqrt(L0 / C0); v = 1 / math.sqrt(L0 * C0); lam = v / f; beta = 2 * math.pi / lam
assert close(Zc, 50) and close(v, 2e8) and close(lam, 2) and close(beta, math.pi)
for ZL in (100, 25, 50, 30 + 40j):
    for l in (0.1, 0.5, 0.37):
        assert close(zin_chain(Zc, beta, l, ZL), zin_formula(Zc, beta, l, ZL), 1e-9)
assert close(zin_chain(Zc, beta, 0.5, 100), 25)          # λ/4
assert close(zin_chain(Zc, beta, 1.0, 100), 100)         # λ/2
assert close(zin_chain(Zc, beta, 0.37, 50), 50)          # 匹配
G = (100 - 50) / (100 + 50); assert close(G, 1 / 3)
assert close(math.sqrt(50 * 100), 70.71067811865476)
print("example ok")

# 练习 1：L0 = 0.4 µH/m, C0 = 40 pF/m, f = 50 MHz
L0, C0, f = 0.4e-6, 40e-12, 50e6
Zc = math.sqrt(L0 / C0); v = 1 / math.sqrt(L0 * C0); lam = v / f
assert close(Zc, 100) and close(v, 2.5e8) and close(lam, 5)
print("x1:", Zc, v, lam, 2 * math.pi / lam)

# 练习 2：Zc=50，λ/8，f=100 MHz
w = 2 * math.pi * 100e6
zs = zin_chain(50, math.pi, 0.25, 0.0)          # 短路
zo = zin_chain(50, math.pi, 0.25, math.inf)     # 开路
assert close(zs, 50j) and close(zo, -50j)
Leq = 50 / w; Ceq = 1 / (w * 50)
print("x2: L = %.2f nH, C = %.2f pF" % (Leq * 1e9, Ceq * 1e12))
assert abs(Leq * 1e9 - 79.58) < 0.01 and abs(Ceq * 1e12 - 31.83) < 0.01

# 练习 3：负载 200 Ω，主线 50 Ω
assert close((200 - 50) / (200 + 50), 0.6)
Zq = math.sqrt(50 * 200); assert close(Zq, 100)
assert close(zin_chain(100, math.pi, 0.5, 200), 50)
print("all ok")
