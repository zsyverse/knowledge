"""验算 docs/basics/math/linalg/subspaces.md 里的例题。

    .venv/bin/python scripts/linalg/verify_subspaces.py
"""
import numpy as np
import sympy as sp

R = sp.Rational


def col(*a):
    return sp.Matrix(list(a))


# ---- 例：判断是否为子空间 ----
# (c) 两条坐标轴的并集对加法不封闭；(d) 第一象限对数乘不封闭
assert (1 * 0 == 0) and (0 * 1 == 0) and (1 * 1 != 0)          # (1,0)+(0,1)=(1,1) 不满足 x1*x2=0
assert not all(t >= 0 for t in (-1 * 1, -1 * 2))               # (-1)*(1,2) 出了第一象限

# ---- 例：线性相关、基与坐标 ----
v1, v2, v3 = col(1, 1, 0), col(0, 1, 1), col(1, 2, 1)
M = sp.Matrix.hstack(v1, v2, v3)
Rm, piv = M.rref()
assert Rm == sp.Matrix([[1, 0, 1], [0, 1, 1], [0, 0, 0]]) and piv == (0, 1)
assert v3 == v1 + v2 and M.rank() == 2
w3 = col(1, 0, 1)
Bm = sp.Matrix.hstack(v1, v2, w3)
assert Bm.det() == 2
assert Bm.solve(col(2, 3, 3)) == col(1, 2, 1)

# ---- 例：秩一矩阵 ----
u, v = col(2, 1, 3), col(1, 2, 3)
A1 = sp.Matrix([[2, 4, 6], [1, 2, 3], [3, 6, 9]])
assert A1 == u * v.T and A1.rank() == 1
x = col(1, 1, 1)
assert v.dot(x) == 6 and A1 * x == 6 * u
assert A1 * col(-2, 1, 0) == sp.zeros(3, 1) and A1 * col(-3, 0, 1) == sp.zeros(3, 1)
assert len(A1.nullspace()) == 2

# ---- 例：BA 能否可逆 ----
rng = np.random.default_rng(0)
A_ = rng.standard_normal((3, 5))
B_ = rng.standard_normal((5, 3))
assert np.linalg.matrix_rank(A_ @ B_) == 3 and np.linalg.matrix_rank(B_ @ A_) == 3
assert abs(np.linalg.det(B_ @ A_)) < 1e-10

# ---- 例：四个基本子空间 ----
A = sp.Matrix([[1, 2, 0, 1], [2, 4, 1, 4], [3, 6, 1, 5]])
Rm, piv = A.rref()
assert Rm == sp.Matrix([[1, 2, 0, 1], [0, 0, 1, 2], [0, 0, 0, 0]]) and piv == (0, 2)
r = A.rank()
assert r == 2
s1, s2 = col(-2, 1, 0, 0), col(-1, 0, -2, 1)
assert A * s1 == sp.zeros(3, 1) and A * s2 == sp.zeros(3, 1)
assert len(A.nullspace()) == 4 - r == 2
yl = col(1, 1, -1)
assert A.T * yl == sp.zeros(4, 1) and len(A.T.nullspace()) == 3 - r == 1
# 列空间的基取 A 的第 1、3 列；R 的第 1、3 列张成的不是 C(A)
c1, c3 = A[:, 0], A[:, 2]
assert c1 == col(1, 2, 3) and c3 == col(0, 1, 1)
assert A[:, 1] == 2 * c1 and A[:, 3] == c1 + 2 * c3
assert sp.Matrix.hstack(c1, c3, Rm[:, 0]).rank() == 3          # e1 不在 C(A) 里
# 正交关系
rows = [col(1, 2, 0, 1), col(0, 0, 1, 2)]
assert all(rw.dot(s) == 0 for rw in rows for s in (s1, s2))
assert yl.dot(c1) == 0 and yl.dot(c3) == 0

# ---- 例：通解 ----
b = col(1, 4, 5)
assert yl.dot(b) == 0
aug = sp.Matrix.hstack(A, b).rref()[0]
assert aug == sp.Matrix([[1, 2, 0, 1, 1], [0, 0, 1, 2, 2], [0, 0, 0, 0, 0]])
xp = col(1, 0, 2, 0)
c1s, c2s = sp.symbols("c1 c2")
assert A * (xp + c1s * s1 + c2s * s2) - b == sp.zeros(3, 1)
b2 = col(1, 4, 6)
assert yl.dot(b2) == -1 and sp.Matrix.hstack(A, b2).rank() == 3
assert sp.Matrix.hstack(A, b2).rref()[0][2, 4] != 0

# ---- LoRA 参数量 ----
d, rk = 4096, 8
assert d * d == 16_777_216 and 2 * d * rk == 65_536 and d * d // (2 * d * rk) == 256
assert abs(2 * d * rk / (d * d) - 0.00390625) < 1e-15
rng = np.random.default_rng(0)
Bm_, Am_ = rng.standard_normal((64, 4)), rng.standard_normal((4, 64))
dW = Bm_ @ Am_
assert dW.shape == (64, 64) and np.linalg.matrix_rank(dW) == 4
assert 64 * 64 == 4096 and Bm_.size + Am_.size == 512

# ---- softmax 瓶颈 ----
rng = np.random.default_rng(0)
n, V, dd = 200, 1000, 16
H = rng.standard_normal((n, dd))
W = rng.standard_normal((V, dd))
Z = H @ W.T
assert Z.shape == (200, 1000) and np.linalg.matrix_rank(Z) == 16
zmax = Z.max(axis=1, keepdims=True)
logp = Z - (zmax + np.log(np.exp(Z - zmax).sum(axis=1, keepdims=True)))
assert np.allclose(np.exp(logp).sum(axis=1), 1)
assert np.linalg.matrix_rank(logp) == 17

# ---- 例：行空间分量与零空间分量 ----
Wm = sp.Matrix([[1, 0, 1], [0, 1, 1]])
nv = col(1, 1, -1)
assert Wm * nv == sp.zeros(2, 1) and Wm.nullspace()[0].cross(nv) == sp.zeros(3, 1)
x = col(2, 1, 0)
assert Wm * x == col(2, 1) and Wm * (x + 2 * nv) == col(2, 1) and x + 2 * nv == col(4, 3, -2)
xn = R(nv.dot(x), nv.dot(nv)) * nv
xr = x - xn
assert nv.dot(x) == 3 and xn == nv and xr == col(1, 0, 1)
assert Wm * xr == col(2, 1) and xr.dot(xn) == 0

# ---- 例：最小范数解 ----
X = sp.Matrix([[1, 0, 1], [0, 1, 1]])
y = col(2, 3)
G = X * X.T
assert G == sp.Matrix([[2, 1], [1, 2]]) and G.inv() == sp.Matrix([[2, -1], [-1, 2]]) / 3
alpha = G.inv() * y
assert alpha == col(R(1, 3), R(4, 3))
ws = X.T * alpha
assert ws == col(R(1, 3), R(4, 3), R(5, 3)) and X * ws == y
assert ws.dot(ws) == R(14, 3) and nv.dot(ws) == 0
w_other = col(2, 3, 0)
assert X * w_other == y and w_other.dot(w_other) == 13
t = sp.symbols("t")
wt = w_other + t * nv
assert X * wt == y
assert sp.solve(sp.diff(wt.dot(wt), t), t) == [R(-5, 3)]
assert sp.simplify(wt.subs(t, R(-5, 3)) - ws) == sp.zeros(3, 1)

Xn, yn = np.array(X, dtype=float), np.array([2.0, 3.0])
w = np.zeros(3)
for _ in range(500):
    w = w - 0.1 * Xn.T @ (Xn @ w - yn)
assert np.allclose(w, [1 / 3, 4 / 3, 5 / 3]) and np.allclose(w, np.linalg.pinv(Xn) @ yn)
w = np.array([1.0, 1.0, -1.0])
for _ in range(500):
    w = w - 0.1 * Xn.T @ (Xn @ w - yn)
assert np.allclose(w, [4 / 3, 7 / 3, 2 / 3]) and np.allclose(Xn @ w, yn)
assert np.isclose(w @ w, 23 / 3) and np.isclose(w @ [1, 1, -1], 3)

# ---- 插图里的二维例子：X=[1 2]，y=4 ----
X1 = sp.Matrix([[1, 2]])
w_min = X1.T * (X1 * X1.T).inv() * col(4)
assert w_min == col(R(4, 5), R(8, 5))
w0 = col(2, R(-1, 2))
w_lim = w0 + X1.T * (4 - (X1 * w0)[0]) / 5
assert w_lim == col(R(13, 5), R(7, 10)) and (X1 * w_lim)[0] == 4

print("subspaces: all checks passed")
