"""习题·非正弦周期电路与频率响应 —— 独立验算（相量逐频求解 + 时域数值积分交叉核对）。"""
import numpy as np

deg = np.degrees
P2 = lambda z: f"{abs(z):.4f}∠{deg(np.angle(z)):.3f}°"
close = lambda x, y, tol=1e-6: abs(complex(x) - complex(y)) < tol
ph = lambda m, d: m * np.exp(1j * np.radians(d))
T = 2 * np.pi; t = np.linspace(0, T, 400001)[:-1]      # ω=1 的一个周期
avg = lambda f: f.mean()

# 题 2：有效值与平均功率（含 cos 项与只在电流中出现的 5 次谐波）
u = 10 + 20 * np.sqrt(2) * np.sin(t) + 10 * np.sqrt(2) * np.cos(3 * t)
i = 2 + 4 * np.sqrt(2) * np.sin(t - np.pi / 3) + np.sqrt(2) * np.sin(3 * t + np.pi / 6) + 2 * np.sqrt(2) * np.sin(5 * t)
U = np.sqrt(avg(u**2)); I = np.sqrt(avg(i**2)); P = avg(u * i)
assert close(U, np.sqrt(600), 1e-6) and close(I, 5, 1e-6) and close(P, 65, 1e-6)
print("2:", U, I, P, "λ", P / (U * I))

# 题 3：直流电压源 12V 串 4Ω 与交流电流源 2√2 sin ωt 并入节点 a，a 经 4Ω 接地
Va0 = 12 * 4 / 8; Va1 = 2 * (4 * 4 / 8)
PR2 = (Va0**2 + Va1**2) / 4
I_R1_dc = (12 - Va0) / 4; I_R1_ac = Va1 / 4
PR1 = (I_R1_dc**2 + I_R1_ac**2) * 4
Pvs = 12 * I_R1_dc; Pcs = Va1 * 2
# 时域核对
ua = Va0 + Va1 * np.sqrt(2) * np.sin(t)
i_vs = (12 - ua) / 4                    # 电压源 + 端流出电流
assert close(avg(12 * i_vs), 18) and close(avg(ua * 2 * np.sqrt(2) * np.sin(t)), 8)
assert (Va0, Va1, PR1, PR2, Pvs, Pcs) == (6, 4, 13, 13, 18, 8)
print("3:", Va0, Va1, PR1, PR2, Pvs, Pcs, "U_a rms", np.sqrt(Va0**2 + Va1**2))

# 题 4：由读数反求 R、ωL。u = 12 + 20√2 sin ωt，I=5 A，P=100 W
R = 100 / 25; I0 = 12 / R; I1 = np.sqrt(25 - I0**2); Z1 = 20 / I1; XL = np.sqrt(Z1**2 - R**2)
assert (R, I0, I1, Z1, XL) == (4, 3, 4, 5, 3)
assert close(I0**2 * R + I1**2 * R, 100)
print("4:", R, I0, I1, Z1, XL, "U", np.sqrt(144 + 400))

# 题 5：RC 低通 R=1kΩ，C=1μF，输入 10√2 sin(1000t) + 10√2 sin(10^4 t)
R, C = 1e3, 1e-6
H = lambda w: 1 / (1 + 1j * w * R * C)
o1, o2 = 10 * H(1e3), 10 * H(1e4)
assert close(abs(o1), 10 / np.sqrt(2)) and close(deg(np.angle(o1)), -45)
print("5: wc", 1 / (R * C), "out1", P2(o1), "out2", P2(o2), "ratio in", 1, "out ratio", abs(o2) / abs(o1),
      "Uout rms", np.hypot(abs(o1), abs(o2)))

# 题 6：RLC 串联，R=10，ωL=3，1/(ωC)=27，u = 10 + 100√2 sin ωt + 30√2 sin 3ωt
R, XL, XC = 10, 3, 27
Z = lambda k: R + 1j * (k * XL - XC / k)
I1 = 100 / Z(1); I3 = 30 / Z(3)
assert close(Z(3), 10)
I = np.sqrt(abs(I1)**2 + abs(I3)**2)
P = I**2 * R
UC0 = 10; UC1 = abs(I1) * XC; UC3 = abs(I3) * XC / 3
UC = np.sqrt(UC0**2 + UC1**2 + UC3**2)
UR = I * R
# 时域核对：稳态电流
i = np.sqrt(2) * (abs(I1) * np.sin(t + np.angle(I1)) + abs(I3) * np.sin(3 * t + np.angle(I3)))
uu = 10 + 100 * np.sqrt(2) * np.sin(t) + 30 * np.sqrt(2) * np.sin(3 * t)
assert close(avg(uu * i), P, 1e-6)
print("6: Z1", P2(Z(1)), "I1", P2(I1), "I3", P2(I3), "I", I, "P", P, "UC0,1,3", UC0, UC1, UC3, "UC", UC,
      "UR", UR, "UL", np.sqrt((abs(I1) * 3)**2 + (abs(I3) * 9)**2))

# 题 7：滤波器设计。ω=1000，C1=10μF 与 L1 并联（3ω 并联谐振），再串 C2，负载 R=50
w = 1000; C1 = 10e-6
L1 = 1 / (9 * w**2 * C1)
Ztank = lambda W: 1 / (1 / (1j * W * L1) + 1j * W * C1)
X = Ztank(w)
C2 = 1 / (w * X.imag)
assert close(L1, 1 / 90) and close(X, 12.5j) and close(C2, 80e-6)
R = 50
for k, Us in ((1, 100), (3, 20)):
    W = k * w
    Ys = 1 / (1j * W * L1) + 1j * W * C1
    if abs(Ys) < 1e-12:
        print("   k=3: tank open, U_R = 0")
        continue
    Zs = 1 / Ys + 1 / (1j * W * C2)
    UR = Us * R / (Zs + R)
    print(f"   k={k}: U_R", P2(UR))
    assert close(UR, 100)
print("7: L1", L1 * 1e3, "mH  tank@ω", X, " C2", C2 * 1e6, "uF")
print("all ok")
