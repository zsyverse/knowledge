"""拓展·电路方程的矩阵形式与状态方程 —— 独立验算（numpy / sympy）。

图：节点 ①②③，参考节点 ④；支路方向 1:①→②  2:②→③  3:①→④  4:②→④  5:③→④  6:③→①。
标准支路：I_k = G_k (U_k + U_sk) − I_sk（电压源 + 在支路"出口"端，电流源与支路方向相反）。"""
import numpy as np
import sympy as sp

br = {1: (1, 2), 2: (2, 3), 3: (1, 4), 4: (2, 4), 5: (3, 4), 6: (3, 1)}
A = np.zeros((3, 6), int)
for k, (a, b) in br.items():
    if a <= 3:
        A[a - 1, k - 1] += 1
    if b <= 3:
        A[b - 1, k - 1] -= 1
assert (A == np.array([[1, 0, 1, 0, 0, -1], [-1, 1, 0, 1, 0, 0], [0, -1, 0, 0, 1, 1]])).all()

# 树 {3,4,5}，基本回路（方向同连支）
B = np.array([[1, 0, -1, 1, 0, 0],    # 连支 1
              [0, 1, 0, -1, 1, 0],    # 连支 2
              [0, 0, 1, 0, -1, 1]])   # 连支 6
assert (A @ B.T == 0).all()
Q = np.array([[1, 0, 1, 0, 0, -1], [-1, 1, 0, 1, 0, 0], [0, -1, 0, 0, 1, 1]])   # 树支 3,4,5
assert (Q @ B.T == 0).all() and (Q == A).all()
tw, lk = [2, 3, 4], [0, 1, 5]
assert (B[:, tw] == -Q[:, lk].T).all()
# 每个基本回路的 KVL 都由 u = A^T un 自动满足
un = np.array([3.0, -1.0, 2.0])
assert np.allclose(B @ (A.T @ un), 0)
print("A, B, Q ok")

# ---- 例：节点方程 ----
G = np.diag([0.5, 1, 1, 0.5, 0.5, 0.5])
Us = np.array([0, 0, 6, 0, 0, 0.0])
Is = np.array([0, 0, 0, 6, 0, 0.0])
Yn = A @ G @ A.T
Jn = A @ Is - A @ G @ Us
print("Yn=\n", Yn, "\nJn=", Jn)
Un = np.linalg.solve(Yn, Jn)
print("Un=", Un)
# 独立核对：直接用物理元件列节点 KCL（流出 = 0）
# b3：①—2Ω—(4 V 源，+ 在 ④ 侧)—④：从①流向④的电流 = (V1 − (−4))/2? 源 + 在④侧，即 ④ 侧电位比中点高 4 V：
#     中点电位 = 0 − 4 = −4，电流 (V1 + 4)/2
# b4：②—1Ω—④ 并联 2 A 电流源（由④流向②，即注入②）
V = sp.symbols("V1:4")
eqs = [(V[0] - V[1]) / 2 + (V[0] + 6) / 1 + (V[0] - V[2]) / 2,
       (V[1] - V[0]) / 2 + (V[1] - V[2]) / 1 + V[1] / 2 - 6,
       (V[2] - V[1]) / 1 + V[2] / 2 + (V[2] - V[0]) / 2]
sol = sp.solve(eqs, V)
ref = np.array([float(sol[v]) for v in V])
assert np.allclose(ref, Un), (ref, Un)
Ub = A.T @ Un
Ib = G @ (Ub + Us) - Is
assert np.allclose(A @ Ib, 0)                 # KCL
assert abs(Ub @ Ib) < 1e-12                   # 特勒根：支路功率之和为零
assert np.allclose(Un, [-2, 3, 1]) and np.allclose(Yn, [[2, -0.5, -0.5], [-0.5, 2, -1], [-0.5, -1, 2]]) and np.allclose(Jn, [-6, 6, 0])
print("Un exact:", [sol[v] for v in V], "Ub=", Ub, "Ib=", Ib)

# ---- 例：状态方程 R1=1, C=1, L=1, R2=1 ----
s = sp.symbols("s")
Am = sp.Matrix([[-1, -1], [1, -1]])
assert sp.factor((s * sp.eye(2) - Am).det()) == s**2 + 2 * s + 2
assert set(Am.eigenvals()) == {-1 + sp.I, -1 - sp.I}
# 用运算法核对 u_C 对 u_s 的网络函数极点
Z = 1 + 1 / (1 / (1 / s) + 1 / (s + 1))   # R1 + C ∥ (L + R2)
H = sp.simplify((Z - 1) / Z)
assert sp.factor(sp.denom(sp.together(H))) in (s**2 + 2 * s + 2, 2 * (s**2 + 2 * s + 2)) or \
    sp.simplify(sp.denom(sp.together(H)) - (s**2 + 2 * s + 2)) == 0, H
print("state ex ok:", H)

# ================= 练习 =================
# 1. n=5, b=8
assert (5 - 1, 8 - 5 + 1) == (4, 4)
# 2. 树 {1,2,3}；连支 4,5,6
# 连支4 ②→④：回路 ④→①（b3 反向 −）①→②（b1 +）→ ②：l4 = b4 + b1 − b3 ... 方向同连支：②→④→①→②
B2 = np.array([[1, 0, -1, 1, 0, 0],      # 连支 4：②→④，④→①(b3 反)，①→②(b1)
               [1, 1, -1, 0, 1, 0],      # 连支 5：③→④，④→①(b3 反)，①→②(b1)，②→③(b2)
               [1, 1, 0, 0, 0, 1]])      # 连支 6：③→①，①→②(b1)，②→③(b2)
assert (A @ B2.T == 0).all()
# 基本割集（方向同树支）：树支 1、2、3
Q2 = np.array([[1, 0, 0, -1, -1, -1],    # 树支 1
               [0, 1, 0, 0, -1, -1],     # 树支 2
               [0, 0, 1, 1, 1, 0]])      # 树支 3
assert (Q2 @ B2.T == 0).all()
tw2, lk2 = [0, 1, 2], [3, 4, 5]
assert (B2[:, tw2] == -Q2[:, lk2].T).all()
# 割集与 A 的行组合一致（割集的 KCL 是节点 KCL 的线性组合）
assert np.linalg.matrix_rank(np.vstack([A, Q2])) == 3
print("ex2 ok")

# 3. 全部 G=1，I_s3 = 4 A
Yn3 = A @ A.T
assert (Yn3 == np.array([[3, -1, -1], [-1, 3, -1], [-1, -1, 3]])).all()
J3 = A @ np.array([0, 0, 4, 0, 0, 0])
assert (J3 == np.array([4, 0, 0])).all()
U3 = np.linalg.solve(Yn3, J3)
assert np.allclose(U3, [2, 1, 1])
print("ex3:", U3)

# 4. Us—R1=1—a；C1=1 (a 对地)；L=1 (a→b)；C2=1 (b 对地)；R2=1 (b 对地)
A4 = sp.Matrix([[-1, 0, -1], [0, -1, 1], [1, -1, 0]])     # x = [u1, u2, iL]
B4 = sp.Matrix([1, 0, 0])
p = sp.factor((s * sp.eye(3) - A4).det())
print("ex4 char:", p, sp.Poly(p, s).nroots())
assert sp.expand(p - (s**3 + 2 * s**2 + 3 * s + 2)) == 0
assert sp.factor(p) == (s + 1) * (s**2 + s + 2)
# 直流稳态：x' = 0 → u1 = u2 = iL·1, Us = u1 + iL → u1 = u2 = iL = Us/2
xs = -A4.inv() * B4
assert list(xs) == [sp.Rational(1, 2)] * 3
print("all ok")
