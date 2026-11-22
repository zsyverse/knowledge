"""验算 docs/basics/math/linalg/exercises.md 里 20 道题的每个数。"""
import numpy as np
import sympy as sp

R = sp.Rational
M = sp.Matrix


def close(a, b, tol=1e-9):
    assert np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol), (a, b)


# 1. 点积排序与余弦排序
q = M([3, 4, 0])
docs = [M([4, 3, 0]), M([0, 8, 6]), M([1, 0, 2])]
dots = [q.dot(d) for d in docs]
coss = [q.dot(d) / (q.norm() * d.norm()) for d in docs]
assert dots == [24, 32, 3]
assert coss[0] == R(24, 25) and coss[1] == R(16, 25) and sp.simplify(coss[2] - 3 / (5 * sp.sqrt(5))) == 0
assert abs(float(coss[2]) - 0.268) < 1e-3
assert 2 - 2 * coss[0] == R(2, 25)

# 2. 点积的方差（蒙特卡洛只看量级）
rng = np.random.default_rng(0)
for d in (16, 64, 256):
    s = (rng.standard_normal((100_000, d)) * rng.standard_normal((100_000, d))).sum(1)
    assert abs(s.std() / np.sqrt(d) - 1) < 0.02
assert abs(np.exp(8) - 2981) < 1
sig = 64 ** -0.25
assert abs(sig - 1 / (2 * np.sqrt(2))) < 1e-12 and abs(sig - 0.354) < 1e-3
s = (sig * rng.standard_normal((100_000, 64)) * sig * rng.standard_normal((100_000, 64))).sum(1)
assert abs(s.std() - 1) < 0.02

# 3. MLP 参数量
dims = [3072, 512, 128, 10]
per = [dims[i] * dims[i + 1] + dims[i + 1] for i in range(3)]
assert per == [1573376, 65664, 1290] and sum(per) == 1640330
assert 3072 * 10 + 10 == 30730
W1, W2, W3 = (rng.standard_normal((dims[i + 1], dims[i])) for i in range(3))
b1, b2, b3 = (rng.standard_normal(dims[i + 1]) for i in range(3))
X = rng.standard_normal((64, 3072))
H1 = X @ W1.T + b1
H2 = H1 @ W2.T + b2
Y = H2 @ W3.T + b3
assert H1.shape == (64, 512) and H2.shape == (64, 128) and Y.shape == (64, 10)
W, b = W3 @ W2 @ W1, W3 @ W2 @ b1 + W3 @ b2 + b3
close(Y, X @ W.T + b, 1e-5)
assert W.shape == (10, 3072) and np.linalg.matrix_rank(W) == 10

# 4. 含参数的方程组
a, bb, t = sp.symbols("a b t")
A4 = M([[1, 1, 1], [1, 2, 3], [1, 3, a]])
assert sp.simplify(A4.det() - (a - 5)) == 0
assert A4.subs(a, 6).solve(M([1, 2, 4])) == M([1, -1, 1])
A5 = A4.subs(a, 5)
xg = M([0, 1, 0]) + t * M([1, -2, 1])
assert sp.simplify(A5 * xg - M([1, 2, 3])) == sp.zeros(3, 1)
assert A5.rank() == 2 and A5.row_join(M([1, 2, 4])).rank() == 3

# 5. LU 分解
A = M([[2, 1, 1], [4, 3, 3], [8, 7, 9]])
L = M([[1, 0, 0], [2, 1, 0], [4, 3, 1]])
U = M([[2, 1, 1], [0, 1, 1], [0, 0, 2]])
assert L * U == A and A.det() == 4
assert L.solve(M([4, 10, 24])) == M([4, 2, 2]) and A.solve(M([4, 10, 24])) == M([1, 1, 1])
assert L.solve(M([1, 2, 3])) == M([1, 0, -1]) and A.solve(M([1, 2, 3])) == M([R(1, 2), R(1, 2), R(-1, 2)])

# 6. 四个基本子空间
A = M([[1, 3, 1, 2], [2, 6, 4, 8], [0, 0, 2, 4]])
rref, piv = A.rref()
assert rref == M([[1, 3, 0, 0], [0, 0, 1, 2], [0, 0, 0, 0]]) and piv == (0, 2) and A.rank() == 2
for n in (M([-3, 1, 0, 0]), M([0, 0, -2, 1])):
    assert A * n == sp.zeros(3, 1)
    assert M([1, 3, 0, 0]).dot(n) == 0 and M([0, 0, 1, 2]).dot(n) == 0
assert M([[2, -1, 1]]) * A == sp.zeros(1, 4)
assert M([2, -1, 1]).dot(M([1, 2, 0])) == 0 and M([2, -1, 1]).dot(M([1, 4, 2])) == 0
assert A * M([1, 0, 1, 0]) == M([2, 6, 2]) and M([2, -1, 1]).dot(M([2, 6, 2])) == 0
assert A.row_join(M([2, 6, 2])).rref()[0][:, 4] == M([1, 1, 0])
assert len(A.nullspace()) == 2 and len(A.T.nullspace()) == 1

# 7. LoRA 参数量
d, r = 768, 4
assert d * d == 589824 and 2 * d * r == 6144 and round(2 * d * r / (d * d) * 100, 2) == 1.04
assert 12 * 2 * 2 * d * r == 147456
B1, A1 = rng.standard_normal((d, 4)), rng.standard_normal((4, d))
B2, A2 = rng.standard_normal((d, 8)), rng.standard_normal((8, d))
assert np.linalg.matrix_rank(B1 @ A1) == 4 and np.linalg.matrix_rank(B1 @ A1 + B2 @ A2) == 12

# 8. 线性流的对数密度
A = M([[2, 0], [1, 3]])
z = A.solve(M([3, 3]) - M([1, -1]))
assert z == M([1, 1]) and A.det() == 6
logp = -sp.log(2 * sp.pi) - R(1, 2) * z.dot(z) - sp.log(6)
assert abs(float(logp) - (-4.6296)) < 1e-4
An = np.array([[2.0, 0], [1, 3]])
S = An @ An.T                        # x ~ N(b, A A^T)
dx = np.array([2.0, 4.0])
ref = -0.5 * dx @ np.linalg.solve(S, dx) - 0.5 * np.linalg.slogdet(2 * np.pi * S)[1]
close(ref, float(logp))

# 9. 最小二乘直线
A = M([[1, -1], [1, 0], [1, 1], [1, 2]])
y = M([0, 1, 3, 4])
assert A.T * A == M([[4, 2], [2, 6]]) and A.T * y == M([8, 11])
xh = (A.T * A).solve(A.T * y)
assert xh == M([R(13, 10), R(7, 5)])
assert A * xh == M([R(-1, 10), R(13, 10), R(27, 10), R(41, 10)])
e = y - A * xh
assert e == M([R(1, 10), R(-3, 10), R(3, 10), R(-1, 10)]) and A.T * e == sp.zeros(2, 1) and e.dot(e) == R(1, 5)
xc = M([R(-3, 2), R(-1, 2), R(1, 2), R(3, 2)])
Ac = sp.ones(4, 1).row_join(xc)
assert Ac.T * Ac == M([[4, 0], [0, 5]])
assert sp.ones(4, 1).dot(y) / 4 == 2 and xc.dot(y) / xc.dot(xc) == R(7, 5)
assert 2 - R(7, 5) * R(1, 2) == R(13, 10)

# 10. 去掉方向
u = M([2, 1, 2]) / 3
h = M([3, 3, 0])
hp = h - u.dot(h) * u
assert u.dot(h) == 3 and hp == M([1, 2, -2]) and u.dot(hp) == 0
P = sp.eye(3) - u * u.T
assert P == M([[5, -2, -4], [-2, 8, -2], [-4, -2, 5]]) / 9
assert P * P == P and P.rank() == 2 and P.det() == 0 and P * h == hp
assert sorted(P.eigenvals(multiple=True)) == [0, 1, 1]
v = M([1, 0, 0])
naive = hp - v.dot(hp) * v
assert naive == M([0, 2, -2]) and u.dot(naive) == R(-2, 3)
w = v - u.dot(v) * u
assert w == M([5, -2, -4]) / 9
q2 = w / w.norm()
assert sp.simplify(q2 - M([5, -2, -4]) / (3 * sp.sqrt(5))) == sp.zeros(3, 1)
assert sp.simplify(q2.dot(hp) - 3 / sp.sqrt(5)) == 0
h2 = sp.simplify(hp - q2.dot(hp) * q2)
assert h2 == M([0, R(12, 5), R(-6, 5)]) and u.dot(h2) == 0 and v.dot(h2) == 0
Q = u.row_join(q2)
assert sp.simplify(h - Q * Q.T * h - h2) == sp.zeros(3, 1)

# 11. 梯度下降与特征值
H = M([[5, 2], [2, 2]])
assert H.eigenvals() == {1: 1, 6: 1}
assert H * M([1, -2]) == M([1, -2]) and H * M([2, 1]) == 6 * M([2, 1]) and M([1, -2]).dot(M([2, 1])) == 0
x0 = M([3, -1])
assert x0 == M([1, -2]) + M([2, 1]) and H * x0 == M([13, 4])
x = x0
for k in range(1, 3):
    x = x - R(2, 7) * H * x
    assert x == R(5, 7) ** k * M([1, -2]) + R(-5, 7) ** k * M([2, 1])
    assert sp.simplify(x.norm() - R(5, 7) ** k * x0.norm()) == 0
assert x == M([R(75, 49), R(-25, 49)])
assert x0 - R(2, 7) * H * x0 == M([R(-5, 7), R(-15, 7)])
assert 1 - R(3, 10) * 6 == R(-4, 5) and 1 - R(2, 5) * 6 == R(-7, 5)
assert int(np.ceil(np.log(100) / np.log(1.4))) == 14 and abs(np.log(100) / np.log(1.4) - 13.7) < 0.05
assert int(np.ceil(np.log(100) / np.log(3))) == 5

# 12. bigram 转移矩阵
P = M([[R(4, 5), R(1, 5)], [R(3, 5), R(2, 5)]])
pi = M([[R(3, 4), R(1, 4)]])
assert pi * P == pi and P.eigenvals() == {1: 1, R(1, 5): 1}
Pk = lambda k: M([[R(3, 4), R(1, 4)], [R(3, 4), R(1, 4)]]) + R(1, 5) ** k * M([[R(1, 4), R(-1, 4)], [R(-3, 4), R(3, 4)]])
for k in range(5):
    assert P ** k == Pk(k)
assert (M([[0, 1]]) * P ** 2) == M([[R(18, 25), R(7, 25)]])
assert pi[0] * P[0, 1] == R(3, 20) and pi[1] * P[1, 0] == R(3, 20)

# 13. 正定与 Cholesky
A = M([[4, 2, 0], [2, 5, 4], [0, 4, 13]])
assert [A[:k, :k].det() for k in (1, 2, 3)] == [4, 16, 144]
L = M([[2, 0, 0], [1, 2, 0], [0, 2, 3]])
assert L * L.T == A and A.cholesky() == L
assert L * M([1, -1, 1]) == M([2, -1, 1])
tt = sp.symbols("t", real=True)
assert M([[1, tt], [tt, 4]]).det() == 4 - tt**2

# 14. 两层线性网络的鞍点
w1, w2 = sp.symbols("w1 w2", real=True)
Lf = R(1, 2) * (w1 * w2 - 1) ** 2
Hs = sp.hessian(Lf, (w1, w2))
assert sp.simplify(Hs - M([[w2**2, 2 * w1 * w2 - 1], [2 * w1 * w2 - 1, w1**2]])) == sp.zeros(2, 2)
assert Hs.subs({w1: 0, w2: 0}).eigenvals() == {1: 1, -1: 1}
assert Hs.subs({w1: 1, w2: 1}).eigenvals() == {0: 1, 2: 1}
assert Hs.subs({w1: 1, w2: 1}) * M([1, -1]) == sp.zeros(2, 1)
assert Hs.subs({w1: 2, w2: R(1, 2)}).eigenvals() == {0: 1, R(17, 4): 1}

# 15. 对称矩阵的 SVD 与谱归一化
A = M([[1, 2], [2, -2]])
assert A.eigenvals() == {2: 1, -3: 1}
v1, v2 = M([1, -2]) / sp.sqrt(5), M([2, 1]) / sp.sqrt(5)
assert A * v1 == -3 * v1 and A * v2 == 2 * v2
u1, u2 = -v1, v2
assert sp.simplify(3 * u1 * v1.T + 2 * u2 * v2.T - A) == sp.zeros(2, 2)
close(np.linalg.svd(np.array(A, dtype=float), compute_uv=False), [3, 2])
assert A.norm() == sp.sqrt(13)
A1 = sp.simplify(3 * u1 * v1.T)
assert A1 == M([[R(-3, 5), R(6, 5)], [R(6, 5), R(-12, 5)]])
assert A - A1 == M([[R(8, 5), R(4, 5)], [R(4, 5), R(2, 5)]]) and (A - A1).norm() == 2
close(np.linalg.svd(np.array(A, dtype=float) / 3, compute_uv=False), [1, 2 / 3])

# 16. PCA
X = M([[5, 4], [-3, 0], [2, 0], [0, 4]])
mu = sum((X[i, :] for i in range(4)), sp.zeros(1, 2)) / 4
assert mu == M([[1, 2]])
Xc = X - sp.ones(4, 1) * mu
assert Xc == M([[4, 2], [-4, -2], [1, -2], [-1, 2]]) and Xc.T * Xc == M([[34, 12], [12, 16]])
lam = sp.symbols("lam")
assert sp.expand((Xc.T * Xc).charpoly(lam).as_expr() - (lam**2 - 50 * lam + 400)) == 0
S = Xc.T * Xc / 3
assert S.eigenvals() == {R(40, 3): 1, R(10, 3): 1}
p1 = M([2, 1]) / sp.sqrt(5)
assert sp.simplify(S * p1 - R(40, 3) * p1) == sp.zeros(2, 1)
score = sp.simplify(Xc * p1)
assert score == M([2 * sp.sqrt(5), -2 * sp.sqrt(5), 0, 0])
rec = sp.simplify(score * p1.T + sp.ones(4, 1) * mu)
assert rec == M([[5, 4], [-3, 0], [1, 2], [1, 2]])
assert sum((X - rec)[i] ** 2 for i in range(8)) == 10
assert R(40, 3) / (R(40, 3) + R(10, 3)) == R(4, 5)
close(np.linalg.svd(np.array(Xc, dtype=float), compute_uv=False) ** 2, [40, 10])

# 17. 岭回归
X = M([[1, 0], [0, 2]])
y = M([1, 2])
assert (X.T * X).solve(X.T * y) == M([1, 1])
wr = (X.T * X + sp.eye(2)).solve(X.T * y)
assert wr == M([R(1, 2), R(4, 5)])
Xn, yn, w, eta, lam = np.array(X, dtype=float), np.array(y, dtype=float).ravel(), np.zeros(2), 0.1, 1.0
for _ in range(500):
    w = (1 - eta * lam) * w - eta * Xn.T @ (Xn @ w - yn)
close(w, [0.5, 0.8])

# 18. softmax 交叉熵与线性层梯度
z = np.log([2.0, 3.0, 5.0])
p = np.exp(z) / np.exp(z).sum()
close(p, [0.2, 0.3, 0.5])
close(-np.log(p[2]), np.log(2))
g = p - np.array([0, 0, 1.0])
close(g, [0.2, 0.3, -0.5])
x = np.array([1.0, 2.0])
G = np.outer(g, x)
close(G, [[0.2, 0.4], [0.3, 0.6], [-0.5, -1.0]])
assert np.linalg.matrix_rank(G) == 1
W0 = rng.standard_normal((3, 2))          # 有限差分核对 dL/dW = (p - y) x^T
def loss(Wm):
    zz = Wm @ x
    return -(zz[2] - np.log(np.exp(zz).sum()))
pz = np.exp(W0 @ x) / np.exp(W0 @ x).sum()
Gn = np.zeros_like(W0)
for i in range(3):
    for j in range(2):
        E = np.zeros_like(W0); E[i, j] = 1e-6
        Gn[i, j] = (loss(W0 + E) - loss(W0 - E)) / 2e-6
close(Gn, np.outer(pz - np.array([0, 0, 1.0]), x), 1e-6)

# 19. 注意力输出是凸组合
V = np.array([[1.0, 0], [0, 1], [-1, 0]])
S = np.array([[0.0, 0, 0], [0, np.log(3), 0], [0, np.log(2), 0]])
mask = np.triu(np.ones((3, 3), dtype=bool), 1)
S = np.where(mask, -np.inf, S)
Aw = np.exp(S) / np.exp(S).sum(1, keepdims=True)
close(Aw, [[1, 0, 0], [0.25, 0.75, 0], [0.25, 0.5, 0.25]])
O = Aw @ V
close(O, [[1, 0], [0.25, 0.75], [0, 0.5]])
close(Aw @ np.ones(3), np.ones(3))
assert np.all(np.linalg.norm(O, axis=1) <= np.linalg.norm(V, axis=1).max() + 1e-12)
close(np.linalg.norm(O, axis=1), [1, np.sqrt(10) / 4, 0.5])

# 20. RoPE
th = sp.pi / 6
Rm = lambda m: M([[sp.cos(m * th), -sp.sin(m * th)], [sp.sin(m * th), sp.cos(m * th)]])
qv = kv = M([1, 0])
vals = [sp.simplify((Rm(m) * qv).dot(Rm(0) * kv)) for m in range(4)]
assert vals == [1, sp.sqrt(3) / 2, R(1, 2), 0]
q2, k2 = M([1, 2]), M([3, -1])
assert sp.simplify((Rm(5) * q2).dot(Rm(3) * k2) - (Rm(12) * q2).dot(Rm(10) * k2)) == 0
assert sp.simplify((Rm(5) * q2).dot(Rm(3) * k2) - q2.dot(Rm(-2) * k2)) == 0
assert sp.simplify((Rm(5) * q2).dot(Rm(3) * k2) - (1 - 7 * sp.sqrt(3)) / 2) == 0
assert sp.simplify((Rm(7) * q2).norm() - q2.norm()) == 0
assert sp.simplify(Rm(2).T * Rm(2) - sp.eye(2)) == sp.zeros(2, 2)

print("exercises: all checks passed")
