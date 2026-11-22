"""验算 docs/basics/math/linalg/orthogonality.md 里的例题。

    .venv/bin/python scripts/linalg/verify_orthogonality.py
"""
import numpy as np
import sympy as sp

R = sp.Rational
sqrt = sp.sqrt


def col(*a):
    return sp.Matrix(list(a))


# ---- 例：标准正交基下的坐标 ----
q1, q2 = col(1, 1) / sqrt(2), col(1, -1) / sqrt(2)
x = col(3, 1)
assert q1.dot(q2) == 0 and q1.dot(q1) == 1 and q2.dot(q2) == 1
c1, c2 = q1.dot(x), q2.dot(x)
assert sp.simplify(c1 - 2 * sqrt(2)) == 0 and sp.simplify(c2 - sqrt(2)) == 0
assert sp.simplify(c1 * q1 + c2 * q2 - x) == sp.zeros(2, 1)
assert sp.simplify(c1 * q1 - col(2, 2)) == sp.zeros(2, 1) and sp.simplify(c2 * q2 - col(1, -1)) == sp.zeros(2, 1)
assert sp.simplify(c1**2 + c2**2) == 10 == x.dot(x)

# ---- 例：验证正交矩阵 ----
Q = sp.Matrix([[1, 2, 2], [2, 1, -2], [2, -2, 1]]) / 3
assert Q.T * Q == sp.eye(3) and Q * Q.T == sp.eye(3) and Q.det() == -1
xv = col(1, 2, 2)
assert Q * xv == col(3, 0, 0) and xv.dot(xv) == 9
yv = col(2, 0, 1)
assert Q * yv == col(R(4, 3), R(2, 3), R(5, 3))
assert (Q * xv).dot(Q * yv) == xv.dot(yv) == 4
u = col(1, -1, -1) / sqrt(3)
assert sp.simplify(sp.eye(3) - 2 * u * u.T - Q) == sp.zeros(3, 3)

# ---- 例：向平面投影 ----
A = sp.Matrix([[1, 0], [0, 1], [1, 1]])
b = col(1, 1, 0)
assert A.T * A == sp.Matrix([[2, 1], [1, 2]]) and A.T * b == col(1, 1)
xh = (A.T * A).solve(A.T * b)
assert xh == col(R(1, 3), R(1, 3))
p = A * xh
e = b - p
assert p == col(R(1, 3), R(1, 3), R(2, 3)) and e == col(R(2, 3), R(2, 3), R(-2, 3))
assert A.T * e == sp.zeros(2, 1) and p.dot(e) == 0
assert p.dot(p) + e.dot(e) == b.dot(b) == 2
P = A * (A.T * A).inv() * A.T
assert P == sp.Matrix([[2, -1, 1], [-1, 2, 1], [1, 1, 2]]) / 3
assert P * P == P and P.T == P and P * b == p and P.rank() == 2 and P.trace() == 2
nrm = col(1, 1, -1)
assert A.T * nrm == sp.zeros(2, 1)
assert P == sp.eye(3) - nrm * nrm.T / nrm.dot(nrm)
assert (sp.eye(3) - P) * b == e

# ---- 例：最小二乘拟合直线 ----
A = sp.Matrix([[1, 0], [1, 1], [1, 2], [1, 3]])
b = col(1, 2, 2, 4)
assert A.T * A == sp.Matrix([[4, 6], [6, 14]]) and A.T * b == col(9, 18)
xh = (A.T * A).solve(A.T * b)
assert xh == col(R(9, 10), R(9, 10))
fit = A * xh
res = b - fit
assert fit == col(R(9, 10), R(18, 10), R(27, 10), R(36, 10))
assert res == col(R(1, 10), R(2, 10), R(-7, 10), R(4, 10))
assert sum(res) == 0 and A[:, 1].dot(res) == 0 and res.dot(res) == R(7, 10)
An, bn = np.array(A, dtype=float), np.array([1.0, 2.0, 2.0, 4.0])
assert np.allclose(np.linalg.lstsq(An, bn, rcond=None)[0], [0.9, 0.9])

# ---- 例：Gram–Schmidt 与 QR ----
a1, a2, a3 = col(1, 1, 0), col(1, 0, 1), col(0, 1, 1)
g1 = a1 / sqrt(2)
B2 = a2 - g1.dot(a2) * g1
assert g1.dot(a2) == 1 / sqrt(2) and sp.simplify(B2 - col(R(1, 2), R(-1, 2), 1)) == sp.zeros(3, 1)
assert sp.simplify(B2.norm() - sqrt(6) / 2) == 0
g2 = B2 / B2.norm()
assert sp.simplify(g2 - col(1, -1, 2) / sqrt(6)) == sp.zeros(3, 1)
B3 = a3 - g1.dot(a3) * g1 - g2.dot(a3) * g2
assert sp.simplify(g1.dot(a3) - 1 / sqrt(2)) == 0 and sp.simplify(g2.dot(a3) - 1 / sqrt(6)) == 0
assert sp.simplify(B3 - col(R(-2, 3), R(2, 3), R(2, 3))) == sp.zeros(3, 1)
assert sp.simplify(B3.norm() - 2 / sqrt(3)) == 0
g3 = B3 / B3.norm()
assert sp.simplify(g3 - col(-1, 1, 1) / sqrt(3)) == sp.zeros(3, 1)
Qg = sp.Matrix.hstack(g1, g2, g3)
Rg = sp.Matrix([[sqrt(2), 1 / sqrt(2), 1 / sqrt(2)], [0, sqrt(6) / 2, 1 / sqrt(6)], [0, 0, 2 / sqrt(3)]])
assert sp.simplify(Qg.T * Qg - sp.eye(3)) == sp.zeros(3, 3)
assert sp.simplify(Qg * Rg - sp.Matrix.hstack(a1, a2, a3)) == sp.zeros(3, 3)
assert sp.simplify(Qg.T * sp.Matrix.hstack(a1, a2, a3) - Rg) == sp.zeros(3, 3)

# ---- 例：用 QR 解最小二乘 ----
h1 = col(1, 1, 1, 1) / 2
a2 = A[:, 1]
assert h1.dot(a2) == 3
B2 = a2 - 3 * h1
assert B2 == col(R(-3, 2), R(-1, 2), R(1, 2), R(3, 2)) and B2.norm() == sqrt(5)
h2 = B2 / sqrt(5)
assert sp.simplify(h2 - col(-3, -1, 1, 3) / (2 * sqrt(5))) == sp.zeros(4, 1)
Qh = sp.Matrix.hstack(h1, h2)
Rh = sp.Matrix([[2, 3], [0, sqrt(5)]])
assert sp.simplify(Qh * Rh - A) == sp.zeros(4, 2)
rhs = Qh.T * b
assert sp.simplify(rhs - col(R(9, 2), 9 / (2 * sqrt(5)))) == sp.zeros(2, 1)
dd = sp.simplify(rhs[1] / sqrt(5))
cc = (rhs[0] - 3 * dd) / 2
assert dd == R(9, 10) and cc == R(9, 10)

# ---- 正规方程把条件数平方：数值例 ----
errs = {}
for eps in (1e-4, 1e-8):
    A2 = np.array([[1.0, 1.0], [eps, 0.0], [0.0, eps]])
    w_true = np.array([1.0, 2.0])
    b2 = A2 @ w_true
    Q2, R2 = np.linalg.qr(A2)
    err_qr = abs(np.linalg.solve(R2, Q2.T @ b2) - w_true).max()
    try:
        err_ne = abs(np.linalg.solve(A2.T @ A2, A2.T @ b2) - w_true).max()
    except np.linalg.LinAlgError:
        err_ne = None
    errs[eps] = (err_ne, err_qr)
assert errs[1e-4][0] > 1e-9 and errs[1e-4][1] < 1e-14
assert errs[1e-8][0] is None and errs[1e-8][1] < 1e-14
A2 = np.array([[1.0, 1.0], [1e-8, 0.0], [0.0, 1e-8]])
assert np.array_equal(A2.T @ A2, np.ones((2, 2)))

# ---- 线性探针 ----
rng = np.random.default_rng(0)
n, d = 2000, 64
u_ = rng.standard_normal(d)
u_ /= np.linalg.norm(u_)
H = rng.standard_normal((n, d))
y = np.sign(H @ u_ + 0.5 * rng.standard_normal(n))
Htr, ytr, Hte, yte = H[:1500], y[:1500], H[1500:], y[1500:]
w, *_ = np.linalg.lstsq(Htr, ytr, rcond=None)
acc = np.mean(np.sign(Hte @ w) == yte)
cos = w @ u_ / np.linalg.norm(w)
assert abs(acc - 0.854) < 1e-9 and abs(cos - 0.9759) < 1e-4
w2, *_ = np.linalg.lstsq(Htr, ytr[rng.permutation(1500)], rcond=None)
assert abs(np.mean(np.sign(Hte @ w2) == yte) - 0.496) < 1e-9

# ---- 例：岭回归 ----
X = sp.Matrix([[1, 0], [0, 1], [1, 1]])
yv = col(2, 0, 1)
assert X.T * X == sp.Matrix([[2, 1], [1, 2]]) and X.T * yv == col(3, 1)
expect = {0: (col(R(5, 3), R(-1, 3)), sqrt(26) / 3, 1.6997), 1: (col(1, 0), 1, 1.0), 3: (col(R(7, 12), R(1, 12)), 5 * sqrt(2) / 12, 0.5893)}
for lam, (w_exp, nrm_exp, nrm_num) in expect.items():
    w = (X.T * X + lam * sp.eye(2)).solve(X.T * yv)
    assert w == w_exp and sp.simplify(w.norm() - nrm_exp) == 0 and abs(float(w.norm()) - nrm_num) < 1e-4
assert (X.T * X + sp.eye(2)).inv() == sp.Matrix([[3, -1], [-1, 3]]) / 8
assert (X.T * X + 3 * sp.eye(2)).inv() == sp.Matrix([[5, -1], [-1, 5]]) / 24
# 增广最小二乘与岭回归等价（lambda = 1）
Xa = sp.Matrix.vstack(X, sp.eye(2))
ya = sp.Matrix.vstack(yv, sp.zeros(2, 1))
assert (Xa.T * Xa).solve(Xa.T * ya) == col(1, 0)
# 带 weight decay 的梯度下降收敛到岭回归的解
Xn, yn = np.array(X, dtype=float), np.array([2.0, 0.0, 1.0])
w = np.zeros(2)
for _ in range(500):
    w = (1 - 2 * 0.05 * 1.0) * w - 0.05 * 2 * Xn.T @ (Xn @ w - yn)
assert np.allclose(w, [1.0, 0.0])

# ---- 正交初始化 ----
rng = np.random.default_rng(0)
d, depth = 64, 50
x0 = rng.standard_normal(d)
x0 /= np.linalg.norm(x0)


def run(make):
    xx, M = x0.copy(), np.eye(d)
    for _ in range(depth):
        W = make()
        xx, M = W @ xx, W @ M
    s = np.linalg.svd(M, compute_uv=False)
    return np.linalg.norm(xx), s[0], s[-1]


orth = lambda: np.linalg.qr(rng.standard_normal((d, d)))[0]
gauss = lambda sc: (lambda: rng.standard_normal((d, d)) * sc / np.sqrt(d))
r = run(orth)
assert np.allclose(r, [1, 1, 1])
r = run(gauss(1.0))
assert abs(r[0] - 0.356) < 1e-3 and abs(r[1] - 4.29) < 1e-2 and r[2] < 1e-15
r = run(gauss(0.9))
assert abs(r[0] - 0.0024) < 1e-4
r = run(gauss(1.1))
assert abs(r[0] - 67.5) < 0.1

# ---- 例：去掉一个方向 ----
xv = col(3, 1, 2)
u = col(1, 2, 2) / 3
assert u.dot(u) == 1 and u.dot(xv) == 3
xc = xv - u.dot(xv) * u
assert xc == col(2, -1, 0) and u.dot(xc) == 0
Pp = sp.eye(3) - u * u.T
assert Pp == sp.Matrix([[8, -2, -2], [-2, 5, -4], [-2, -4, 5]]) / 9
assert Pp * Pp == Pp and Pp * u == sp.zeros(3, 1) and Pp * xv == xc
assert xc.dot(xc) + 3**2 == xv.dot(xv) == 14
rng = np.random.default_rng(0)
Xr = rng.standard_normal((5, 3))
un = np.array([1.0, 2.0, 2.0]) / 3
assert np.allclose((Xr - np.outer(Xr @ un, un)) @ un, 0)

print("orthogonality: all checks passed")
