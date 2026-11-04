"""拓展·二端口网络 —— 独立验算。
约定：I1、I2 都从端口的 + 端流入网络；T 参数 U1 = A U2 − B I2，I1 = C U2 − D I2。"""
import sympy as sp

z11, z12, z21, z22 = sp.symbols("z11 z12 z21 z22")
U1, U2, I1, I2 = sp.symbols("U1 U2 I1 I2")
Zeq = [sp.Eq(U1, z11 * I1 + z12 * I2), sp.Eq(U2, z21 * I1 + z22 * I2)]
dZ = z11 * z22 - z12 * z21


def from_eqs(eqs, out, inn):
    """把 Z 方程改写成以 inn 为自变量、out 为因变量的形式，返回系数矩阵。"""
    s = sp.solve(eqs, out, dict=True)[0]
    return sp.Matrix([[sp.simplify(s[o].diff(i)) for i in inn] for o in out])


# ---- 换算公式 ----
Y = from_eqs(Zeq, [I1, I2], [U1, U2])
assert sp.simplify(Y - sp.Matrix([[z22, -z12], [-z21, z11]]) / dZ) == sp.zeros(2)
H = from_eqs(Zeq, [U1, I2], [I1, U2])
assert sp.simplify(H - sp.Matrix([[dZ / z22, z12 / z22], [-z21 / z22, 1 / z22]])) == sp.zeros(2)
# T：U1 = A U2 + B(−I2)，I1 = C U2 + D(−I2)
Tm = from_eqs(Zeq, [U1, I1], [U2, I2])
A, B, C, D = Tm[0, 0], -Tm[0, 1], Tm[1, 0], -Tm[1, 1]
assert sp.simplify(sp.Matrix([[A, B], [C, D]]) - sp.Matrix([[z11 / z21, dZ / z21], [1 / z21, z22 / z21]])) == sp.zeros(2)
# 互易：AD − BC = z12/z21；对称：ΔH = z11/z22
assert sp.simplify(A * D - B * C - z12 / z21) == 0
assert sp.simplify(H.det() - z11 / z22) == 0
# T → Z
a, b, c, dd = sp.symbols("a b c d")
Zt = from_eqs([sp.Eq(U1, a * U2 - b * I2), sp.Eq(I1, c * U2 - dd * I2)], [U1, U2], [I1, I2])
assert sp.simplify(Zt - sp.Matrix([[a / c, (a * dd - b * c) / c], [1 / c, dd / c]])) == sp.zeros(2)
# 端接：Zin = (A ZL + B)/(C ZL + D) = z11 − z12 z21/(z22 + ZL)；Zout、Uoc
ZL, Zs, Us = sp.symbols("Z_L Z_s U_s")
s = sp.solve([sp.Eq(U1, a * U2 - b * I2), sp.Eq(I1, c * U2 - dd * I2), sp.Eq(U2, -ZL * I2)], [U1, U2, I2], dict=True)[0]
assert sp.simplify(s[U1] / I1 - (a * ZL + b) / (c * ZL + dd)) == 0
s = sp.solve(Zeq + [sp.Eq(U2, -ZL * I2)], [U1, U2, I2], dict=True)[0]
assert sp.simplify(s[U1] / I1 - (z11 - z12 * z21 / (z22 + ZL))) == 0
s = sp.solve([sp.Eq(U1, a * U2 - b * I2), sp.Eq(I1, c * U2 - dd * I2), sp.Eq(U1, -Zs * I1)], [U1, U2, I1], dict=True)[0]
assert sp.simplify(s[U2] / I2 - (dd * Zs + b) / (c * Zs + a)) == 0
s = sp.solve([sp.Eq(U1, a * U2), sp.Eq(I1, c * U2), sp.Eq(Us, Zs * I1 + U1)], [U1, U2, I1], dict=True)[0]
assert sp.simplify(s[U2] - Us / (a + c * Zs)) == 0
# 非互易 T 形等效：Z1=z11−z12, Z2=z12, Z3=z22−z12, CCVS (z21−z12) I1（+ 在端口 2 一侧）
U1e = (z11 - z12) * I1 + z12 * (I1 + I2)
U2e = (z22 - z12) * I2 + (z21 - z12) * I1 + z12 * (I1 + I2)
assert sp.expand(U1e - (z11 * I1 + z12 * I2)) == 0 and sp.expand(U2e - (z21 * I1 + z22 * I2)) == 0
# 非互易 Π 形：Ya=y11+y12, Yb=−y12, Yc=y22+y12, VCCS (y21−y12) U1（端口 2 侧，从上向下）
y11, y12, y21, y22 = sp.symbols("y11 y12 y21 y22")
I1e = (y11 + y12) * U1 + (-y12) * (U1 - U2)
I2e = (y22 + y12) * U2 + (-y12) * (U2 - U1) + (y21 - y12) * U1
assert sp.expand(I1e - (y11 * U1 + y12 * U2)) == 0 and sp.expand(I2e - (y21 * U1 + y22 * U2)) == 0
print("formulas ok")

# ---- 例 1：含 CCVS 的 T 形（2Ω、4Ω 并臂、3Ω，右臂串 CCVS 2I1，+ 在端口 2 一侧）----
U1v = 2 * I1 + 4 * (I1 + I2)
U2v = 3 * I2 + 2 * I1 + 4 * (I1 + I2)
Z = sp.Matrix([[U1v.diff(I1), U1v.diff(I2)], [U2v.diff(I1), U2v.diff(I2)]])
assert Z == sp.Matrix([[6, 4], [6, 7]])
Yn = Z.inv()
assert Yn == sp.Matrix([[sp.Rational(7, 18), -sp.Rational(2, 9)], [-sp.Rational(1, 3), sp.Rational(1, 3)]])
sub = {z11: 6, z12: 4, z21: 6, z22: 7}
Hn = H.subs(sub); Tn = sp.Matrix([[A, B], [C, D]]).subs(sub)
assert Hn == sp.Matrix([[sp.Rational(18, 7), sp.Rational(4, 7)], [-sp.Rational(6, 7), sp.Rational(1, 7)]])
assert Tn == sp.Matrix([[1, 3], [sp.Rational(1, 6), sp.Rational(7, 6)]])
assert Tn.det() == sp.Rational(2, 3)
# 直接由电路验证 T 参数：端口 2 开路（I2=0）：U1=6I1，U2=6I1 → A=1，C=1/6
# 端口 2 短路（U2=0）：0 = 6 I1 + 7 I2 → I1 = −7/6 I2，U1 = 6I1 + 4I2 = −3 I2 → B = 3，D = 7/6
print("ex1:", Z.tolist(), Yn.tolist(), Hn.tolist(), Tn.tolist())

# ---- 例 2：Z = [[5,3],[3,4]]，Us=16 V，Rs=1 Ω，RL 可调 ----
Zs_, Us_ = 1, 16
I1o = sp.Rational(Us_, Zs_ + 5); Uoc = 3 * I1o
Zo = 4 - sp.Rational(9, 5 + Zs_)
assert (Uoc, Zo) == (8, sp.Rational(5, 2))
Pmax = Uoc ** 2 / (4 * Zo)
assert Pmax == sp.Rational(32, 5)
# T 形等效：2、3（并臂）、1 Ω → 同样结果
assert 16 * sp.Rational(3, 6) == 8 and 1 + sp.Rational(3 * 3, 6) == sp.Rational(5, 2)
# 用完整方程核对：RL = 2.5 时负载功率
RL = Zo
s = sp.solve([sp.Eq(U1, 5 * I1 + 3 * I2), sp.Eq(U2, 3 * I1 + 4 * I2), sp.Eq(Us_, Zs_ * I1 + U1), sp.Eq(U2, -RL * I2)],
             [U1, U2, I1, I2], dict=True)[0]
assert s[U2] ** 2 / RL == Pmax
print("ex2:", Uoc, Zo, Pmax, s)

# ================= 练习 =================
# 2. Π：左并 2Ω，串 1Ω，右并 2Ω
Yp = sp.Matrix([[sp.Rational(1, 2) + 1, -1], [-1, sp.Rational(1, 2) + 1]])
Zp = Yp.inv()
assert Zp == sp.Matrix([[sp.Rational(6, 5), sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(6, 5)]])
print("ex2:", Yp.tolist(), Zp.tolist())

# 3. 晶体管 H 参数模型：rbe=1k，β=50（CCCS β I1 由端口 2 上端流向下端），rce=10k；RL=2k
rbe, beta, rce = 1, 50, 10
Hh = sp.Matrix([[rbe, 0], [beta, sp.Rational(1, rce)]])
# 直接验证：U1 = rbe I1；I2 = β I1 + U2/rce
RL = 2
s = sp.solve([sp.Eq(U1, rbe * I1), sp.Eq(I2, beta * I1 + U2 / rce), sp.Eq(U2, -RL * I2)], [U1, U2, I2], dict=True)[0]
Au = sp.simplify(s[U2] / s[U1])
assert Au == sp.Rational(-250, 3)
assert Hh[1, 1] == sp.Rational(1, 10)
# 输出电阻（I1 = 0 → 受控源为 0）= rce
print("ex3:", Au, float(Au))

# 4. 级联：串 1Ω + 并 2Ω 的 L 节，两节级联，RL = 2Ω
Ts = sp.Matrix([[1, 1], [0, 1]]); Tp = sp.Matrix([[1, 0], [sp.Rational(1, 2), 1]])
TL = Ts * Tp
assert TL == sp.Matrix([[sp.Rational(3, 2), 1], [sp.Rational(1, 2), 1]])
T2 = TL * TL
assert T2 == sp.Matrix([[sp.Rational(11, 4), sp.Rational(5, 2)], [sp.Rational(5, 4), sp.Rational(3, 2)]])
assert T2.det() == 1
RL = 2
Zin = (T2[0, 0] * RL + T2[0, 1]) / (T2[1, 0] * RL + T2[1, 1])
gain = 1 / (T2[0, 0] + T2[0, 1] / RL)
assert Zin == 2 and gain == sp.Rational(1, 4)
# 用 T 参数的定义直接验证单个串联/并联元件
# 串联 Z：U1 = U2 − Z I2，I1 = −I2 → A=1,B=Z,C=0,D=1；并联 Y：U1 = U2，I1 = Y U2 − I2 → A=1,B=0,C=Y,D=1
print("ex4:", T2.tolist(), Zin, gain)

# 5. 回转器 r = 1 kΩ：u1 = −r i2，u2 = r i1
r = sp.Symbol("r", positive=True)
w, Cc = sp.symbols("omega C", positive=True)
ZLc = 1 / (sp.I * w * Cc)
s = sp.solve([sp.Eq(U1, -r * I2), sp.Eq(U2, r * I1), sp.Eq(U2, -ZLc * I2)], [U1, U2, I2], dict=True)[0]
Zin = sp.simplify(s[U1] / I1)
assert sp.simplify(Zin - sp.I * w * r ** 2 * Cc) == 0
Leq = (10 ** 3) ** 2 * sp.Rational(1, 10 ** 6)
assert Leq == 1
assert Zin.subs({r: 1000, Cc: sp.Rational(1, 10 ** 6), w: 1000}) == 1000 * sp.I
# 接 500 Ω 电阻：Zin = r²/R = 2000
s = sp.solve([sp.Eq(U1, -r * I2), sp.Eq(U2, r * I1), sp.Eq(U2, -500 * I2)], [U1, U2, I2], dict=True)[0]
assert sp.simplify(s[U1] / I1).subs(r, 1000) == 2000
# 无损：u1 i1 + u2 i2 = 0
assert sp.expand((-r * I2) * I1 + (r * I1) * I2) == 0
print("ex5 ok")

# 负阻抗变换器：电流反向型 u1 = u2, i2 = k i1；电压反向型 u1 = −k u2, i2 = −i1
k = sp.Symbol("k", positive=True)
s = sp.solve([sp.Eq(U1, U2), sp.Eq(I2, k * I1), sp.Eq(U2, -ZL * I2)], [U1, U2, I2], dict=True)[0]
assert sp.simplify(s[U1] / I1 + k * ZL) == 0
s = sp.solve([sp.Eq(U1, -k * U2), sp.Eq(I2, -I1), sp.Eq(U2, -ZL * I2)], [U1, U2, I2], dict=True)[0]
assert sp.simplify(s[U1] / I1 + k * ZL) == 0
print("all ok")
