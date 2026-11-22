"""验算 docs/basics/math/linalg/determinant.md 里的例题。

    .venv/bin/python scripts/linalg/verify_determinant.py
"""
import math
import warnings

import numpy as np
import sympy as sp

warnings.simplefilter("ignore", RuntimeWarning)   # det 上溢/下溢时 NumPy 会给警告，这里正是要测这种情况
R = sp.Rational


def col(*a):
    return sp.Matrix(list(a))


# ---- 第 1 节：面积伸缩比 ----
assert sp.Matrix([[3, 1], [1, 2]]).det() == 5
assert sp.Matrix([[1, 3], [2, 1]]).det() == -5
assert sp.Matrix([[2, 4], [1, 2]]).det() == 0

# ---- 第 2 节：性质 ----
A = sp.Matrix([[0, 2, 1], [1, 1, 2], [2, 1, 1]])
B = sp.Matrix([[1, 2, 0], [0, 1, 0], [0, 0, -2]])
assert A.det() == 5 and B.det() == -2
assert (2 * A).det() == 40 and A.inv().det() == R(1, 5)
assert (A.T * B).det() == -10
assert (A * A * B.inv()).det() == R(-25, 2)
A2 = A.copy()
A2.row_swap(0, 1)
A2[2, :] = 4 * A2[2, :]
assert A2.det() == -20
# det(A+B) 一般不等于 det A + det B
I2 = sp.eye(2)
assert (I2 + I2).det() == 4 and I2.det() + I2.det() == 2
# 倍加（剪切）不改变面积：插图里的三步
assert sp.Matrix([[3, 1], [1, 2]]).det() == sp.Matrix([[3, 1], [0, R(5, 3)]]).det() == sp.Matrix([[3, 0], [0, R(5, 3)]]).det() == 5
assert col(1, 2) - R(1, 3) * col(3, 1) == col(0, R(5, 3))
assert col(3, 1) - R(3, 5) * col(0, R(5, 3)) == col(3, 0)

# ---- 例：三阶行列式的两种算法 ----
# 按第 1 行展开
M12 = A.minor_submatrix(0, 1).det()
M13 = A.minor_submatrix(0, 2).det()
assert M12 == -3 and M13 == -1
assert 0 - 2 * M12 + 1 * M13 == 5
# 消元：先交换第 1、2 行
E = sp.Matrix([[1, 1, 2], [0, 2, 1], [2, 1, 1]])
E[2, :] = E[2, :] - 2 * E[0, :]
assert E[2, :] == sp.Matrix([[0, -1, -3]])
E[2, :] = E[2, :] + R(1, 2) * E[1, :]
assert E == sp.Matrix([[1, 1, 2], [0, 2, 1], [0, 0, R(-5, 2)]])
assert 1 * 2 * R(-5, 2) == -5 and -(1 * 2 * R(-5, 2)) == 5

# ---- 例：含参数的行列式 ----
t = sp.symbols("t")
V = sp.Matrix([[1, 1, 1], [1, 2, t], [1, 4, t**2]])
assert sp.expand(V.det() - (t - 1) * (t - 2)) == 0
assert sorted(sp.solve(V.det(), t)) == [1, 2]
assert V.subs(t, 1).rank() == 2 and V.subs(t, 2).rank() == 2 and V.subs(t, 3).det() == 2

# ---- 分块三角 ----
Mb = sp.Matrix([[2, 1, 5, 7], [1, 1, 3, 4], [0, 0, 3, 1], [0, 0, 2, 4]])
assert Mb[:2, :2].det() == 1 and Mb[2:, 2:].det() == 10 and Mb.det() == 10

# ---- 例：伴随矩阵求逆与 Cramer 法则 ----
Cof = sp.Matrix(3, 3, lambda i, j: A.cofactor(i, j))
assert Cof == sp.Matrix([[-1, 3, -1], [-1, -2, 4], [3, 1, -2]])
adj = Cof.T
assert adj == sp.Matrix([[-1, -1, 3], [3, -2, 1], [-1, 4, -2]]) == A.adjugate()
assert A * adj == 5 * sp.eye(3) and A.inv() == adj / 5
b = col(3, 4, 4)
assert A.solve(b) == col(1, 1, 1)
for i in range(3):
    Ai = A.copy()
    Ai[:, i] = b
    assert Ai.det() == 5
assert sp.Matrix([[2, 1], [5, 3]]).inv() == sp.Matrix([[3, -1], [-5, 2]])

# ---- 例：三角形面积 ----
P, Q, S = col(1, 1), col(4, 2), col(2, 5)
Dm = sp.Matrix.hstack(Q - P, S - P)
assert Dm == sp.Matrix([[3, 1], [1, 4]]) and Dm.det() == 11 and R(1, 2) * abs(Dm.det()) == R(11, 2)

# ---- 第 5 节：slogdet ----
n = 400
assert np.linalg.det(0.1 * np.eye(n)) == 0.0 and np.isinf(np.linalg.det(10 * np.eye(n)))
s1, l1 = np.linalg.slogdet(0.1 * np.eye(n))
s2, l2 = np.linalg.slogdet(10 * np.eye(n))
assert s1 == 1 and s2 == 1 and abs(l1 + 921.034) < 1e-3 and abs(l2 - 921.034) < 1e-3
assert abs(400 * math.log(10) - 921.034) < 1e-3
assert np.isclose(np.linalg.cond(0.1 * np.eye(3)), 1.0)

# ---- 例：一维变量替换 ----
logpz = lambda z: -0.5 * z * z - 0.5 * math.log(2 * math.pi)
z = (3 - 1) / 2
assert z == 1.0
assert abs(logpz(1.0) - (-1.4189)) < 1e-4 and abs(math.exp(logpz(1.0)) - 0.2420) < 1e-4
lp = logpz(1.0) + math.log(0.5)
assert abs(lp - (-2.1121)) < 1e-4 and abs(math.exp(lp) - 0.1210) < 1e-4
# 与 N(1, 2^2) 的密度一致
assert abs(lp - (-0.5 * ((3 - 1) / 2) ** 2 - math.log(2) - 0.5 * math.log(2 * math.pi))) < 1e-12

# ---- 例：二维线性变换 ----
Af = sp.Matrix([[2, 0], [1, 1]])
assert Af.det() == 2 and Af.inv() == sp.Matrix([[R(1, 2), 0], [R(-1, 2), 1]])
zz = Af.inv() * col(2, 2)
assert zz == col(1, 1)
lpz = -0.5 * 2 - math.log(2 * math.pi)
assert abs(lpz - (-2.8379)) < 1e-4
lpx = lpz - math.log(2)
assert abs(lpx - (-3.5310)) < 1e-4
Sig = Af * Af.T
assert Sig == sp.Matrix([[4, 2], [2, 2]]) and Sig.det() == 4 == Af.det() ** 2
xq = (col(2, 2).T * Sig.inv() * col(2, 2))[0]
assert xq == 2
assert abs(lpx - (-0.5 * 2 - 0.5 * math.log(4) - math.log(2 * math.pi))) < 1e-12

# ---- 例：仿射耦合层（二维手算）----
x1, x2 = sp.symbols("x1 x2")
y = sp.Matrix([x1, x2 * sp.exp(x1 / 2) + x1**2])
J = y.jacobian([x1, x2])
assert J[0, 0] == 1 and J[0, 1] == 0
assert sp.simplify(J.det() - sp.exp(x1 / 2)) == 0
at = {x1: 2, x2: 3}
assert sp.simplify(y.subs(at)[1] - (3 * sp.E + 4)) == 0 and abs(float(y.subs(at)[1]) - 12.1548) < 1e-4
assert sp.simplify(J.subs(at)[1, 0] - (sp.Rational(3, 2) * sp.E + 4)) == 0 and abs(float(J.subs(at)[1, 0]) - 8.0774) < 1e-4
assert sp.simplify(J.subs(at).det() - sp.E) == 0 and sp.log(J.subs(at).det()) == 1
# 逆变换
y1v, y2v = 2, 3 * sp.E + 4
assert sp.simplify((y2v - y1v**2) * sp.exp(-sp.Rational(y1v, 2)) - 3) == 0

# ---- 仿射耦合层（四维，数值 Jacobian）----
rng = np.random.default_rng(0)
W1, W2 = rng.standard_normal((8, 2)), rng.standard_normal((4, 8)) * 0.5


def st(xa):
    out = W2 @ np.tanh(W1 @ xa)
    return out[:2], out[2:]


def forward(x):
    xa, xb = x[:2], x[2:]
    s, tt = st(xa)
    return np.concatenate([xa, xb * np.exp(s) + tt]), s.sum()


def inverse(yv):
    ya, yb = yv[:2], yv[2:]
    s, tt = st(ya)
    return np.concatenate([ya, (yb - tt) * np.exp(-s)])


x = np.array([0.5, -1.0, 2.0, 0.3])
yv, logdet = forward(x)
eps = 1e-6
Jn = np.stack([(forward(x + eps * e)[0] - forward(x - eps * e)[0]) / (2 * eps) for e in np.eye(4)], axis=1)
assert np.allclose(np.triu(Jn, 1), 0, atol=1e-8) and np.allclose(Jn[:2, :2], np.eye(2))
sign, logabsdet = np.linalg.slogdet(Jn)
assert sign == 1 and abs(logdet - logabsdet) < 1e-8 and abs(logdet - 0.2303) < 1e-4
assert np.allclose(np.diag(Jn)[2:], np.exp(st(x[:2])[0]))
assert np.allclose(inverse(yv), x)

# ---- 例：二维高斯的对数密度 ----
Sg = sp.Matrix([[2, 1], [1, 2]])
xg = col(1, -1)
assert Sg.det() == 3 and Sg.inv() == sp.Matrix([[2, -1], [-1, 2]]) / 3
assert (xg.T * Sg.inv() * xg)[0] == 2
lg = -0.5 * 2 - 0.5 * math.log(3) - math.log(2 * math.pi)
assert abs(lg - (-3.3872)) < 1e-4
Lc = Sg.cholesky()
assert Lc == sp.Matrix([[sp.sqrt(2), 0], [sp.sqrt(2) / 2, sp.sqrt(6) / 2]])
assert sp.simplify(2 * (sp.log(Lc[0, 0]) + sp.log(Lc[1, 1])) - sp.log(3)) == 0
assert abs(float(Lc[0, 0]) - 1.4142) < 1e-4 and abs(float(Lc[1, 0]) - 0.7071) < 1e-4 and abs(float(Lc[1, 1]) - 1.2247) < 1e-4


def gaussian_logpdf(xv, mu, Sigma):
    d = len(mu)
    L = np.linalg.cholesky(Sigma)
    u = np.linalg.solve(L, xv - mu)
    return -0.5 * (u @ u) - np.log(np.diag(L)).sum() - 0.5 * d * np.log(2 * np.pi)


assert abs(gaussian_logpdf(np.array([1.0, -1.0]), np.zeros(2), np.array([[2.0, 1.0], [1.0, 2.0]])) - lg) < 1e-12
# 1000 维：det 下溢为 0，Cholesky 的写法照常给出对数密度
rng = np.random.default_rng(0)
dh = 1000
Gh = rng.standard_normal((dh, dh)) / np.sqrt(dh)
Sh = 0.2 * (Gh @ Gh.T + 0.1 * np.eye(dh))
xh = rng.standard_normal(dh)
assert np.linalg.det(Sh) == 0.0
assert abs(gaussian_logpdf(xh, np.zeros(dh), Sh) - (-6747.5)) < 0.05
# 对角协方差：log det = sum log sigma^2
sig = np.array([0.5, 2.0, 1.5])
assert np.isclose(np.linalg.slogdet(np.diag(sig**2))[1], 2 * np.log(sig).sum())

print("determinant: all checks passed")
