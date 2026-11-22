"""验算第 10 章（PCA、低秩近似与 LoRA）例题与正文中的数字。

    .venv/bin/python scripts/linalg/verify_pca-lowrank.py
"""
import numpy as np
import sympy as sp

# ---------- 例：手算 5 个二维点的 PCA ----------
X = sp.Matrix([[5, 3], [4, 4], [1, 1], [2, 0], [3, 2]])
n = X.rows
mu = sp.Matrix([[sum(X[:, j]) / n for j in range(2)]])
assert mu == sp.Matrix([[3, 2]])
Xc = X - sp.ones(n, 1) * mu
assert Xc == sp.Matrix([[2, 1], [1, 2], [-2, -1], [-1, -2], [0, 0]])
G = Xc.T * Xc
assert G == sp.Matrix([[10, 8], [8, 10]])
S = G / (n - 1)
assert S == sp.Matrix([[sp.Rational(5, 2), 2], [2, sp.Rational(5, 2)]])
assert S.eigenvals() == {sp.Rational(9, 2): 1, sp.Rational(1, 2): 1}
v1 = sp.Matrix([1, 1]) / sp.sqrt(2)
v2 = sp.Matrix([1, -1]) / sp.sqrt(2)
assert sp.simplify(S * v1 - sp.Rational(9, 2) * v1) == sp.zeros(2, 1)
assert sp.simplify(S * v2 - sp.Rational(1, 2) * v2) == sp.zeros(2, 1)
# 奇异值 sigma_i^2 = (n-1) lambda_i
assert (n - 1) * sp.Rational(9, 2) == 18 and (n - 1) * sp.Rational(1, 2) == 2
V = sp.Matrix.hstack(v1, v2)
T = sp.simplify(Xc * V)
assert sp.simplify(T * sp.sqrt(2)) == sp.Matrix([[3, 1], [3, -1], [-3, -1], [-3, 1], [0, 0]])
assert sp.simplify((T[:, 0].T * T[:, 0])[0] / (n - 1)) == sp.Rational(9, 2)
assert sp.simplify((T[:, 1].T * T[:, 1])[0] / (n - 1)) == sp.Rational(1, 2)
assert sp.simplify((T[:, 0].T * T[:, 1])[0]) == 0
assert sp.Rational(9, 2) / 5 == sp.Rational(9, 10)
# 只保留 v1 的重构与误差
R1 = sp.simplify(Xc * v1 * v1.T)
assert R1.row(0) == sp.Matrix([[sp.Rational(3, 2), sp.Rational(3, 2)]])
assert R1.row(0) + mu == sp.Matrix([[sp.Rational(9, 2), sp.Rational(7, 2)]])
E = Xc - R1
assert E.row(0) == sp.Matrix([[sp.Rational(1, 2), -sp.Rational(1, 2)]])
errs = [sp.simplify((E.row(i) * E.row(i).T)[0]) for i in range(n)]
assert errs == [sp.Rational(1, 2)] * 4 + [0] and sum(errs) == 2

# ---------- 例：白化 ----------
Z = sp.simplify(T * sp.diag(1 / sp.sqrt(sp.Rational(9, 2)), 1 / sp.sqrt(sp.Rational(1, 2))))
assert Z == sp.Matrix([[1, 1], [1, -1], [-1, -1], [-1, 1], [0, 0]])
assert Z.T * Z / (n - 1) == sp.eye(2)

# NumPy 实现与手算一致
Xn = np.array(X.tolist(), dtype=float)
Xcn = Xn - Xn.mean(0)
U, s, Vt = np.linalg.svd(Xcn, full_matrices=False)
assert np.allclose(s**2, [18, 2])
assert np.allclose(s**2 / (s**2).sum(), [0.9, 0.1])
assert np.allclose(np.abs(Vt), 1 / np.sqrt(2))
assert np.allclose(np.cov(Xcn @ Vt.T / s * 2, rowvar=False), np.eye(2))
assert np.allclose(np.linalg.eigvalsh(np.cov(Xn, rowvar=False)), [0.5, 4.5])

# ---------- 例：按累计解释方差选 k ----------
sig = sp.Matrix([10, 6, 3, 2, 1])
sq = [x**2 for x in sig]
assert sq == [100, 36, 9, 4, 1] and sum(sq) == 150
ratio = [sp.Rational(x, 150) for x in sq]
assert [round(float(x) * 100, 1) for x in ratio] == [66.7, 24.0, 6.0, 2.7, 0.7]
cum = [float(sum(ratio[: k + 1])) for k in range(5)]
assert [round(c * 100, 1) for c in cum] == [66.7, 90.7, 96.7, 99.3, 100.0]
pick = lambda th: next(k + 1 for k, c in enumerate(cum) if c >= th)
assert (pick(0.90), pick(0.95), pick(0.99)) == (2, 3, 4)

# ---------- 例：截断的压缩率与误差 ----------
m_, n_ = 60, 40
assert m_ * n_ == 2400
assert 2 * (m_ + n_ + 1) == 202 and round(202 / 2400 * 100, 1) == 8.4
assert 3 * (m_ + n_ + 1) == 303 and round(303 / 2400 * 100, 1) == 12.6
assert abs(float(sp.sqrt(sp.Rational(14, 150))) - 0.306) < 5e-4
assert abs(float(sp.sqrt(sp.Rational(5, 150))) - 0.183) < 5e-4
assert abs((1 - cum[1]) - 14 / 150) < 1e-12 and round(1 - cum[1], 3) == 0.093
rng = np.random.default_rng(1)
Uq, _ = np.linalg.qr(rng.standard_normal((m_, 5)))
Vq, _ = np.linalg.qr(rng.standard_normal((n_, 5)))
M = Uq @ np.diag([10.0, 6, 3, 2, 1]) @ Vq.T
Uu, ss, Vv = np.linalg.svd(M, full_matrices=False)
M2 = (Uu[:, :2] * ss[:2]) @ Vv[:2]
assert abs(np.linalg.norm(M - M2) / np.linalg.norm(M) - np.sqrt(14 / 150)) < 1e-12
assert abs(np.linalg.norm(M - M2, 2) - 3) < 1e-12

# 正文：秩 5 加噪声矩阵
rng = np.random.default_rng(0)
m, nn = 200, 100
M = rng.standard_normal((m, 5)) @ rng.standard_normal((5, nn)) + 0.1 * rng.standard_normal((m, nn))
U, s, Vt = np.linalg.svd(M, full_matrices=False)
assert s[4] > 100 and s[5] < 3
table = {1: (301, 0.8203), 3: (903, 0.5229), 5: (1505, 0.0431), 10: (3010, 0.0401), 20: (6020, 0.0347)}
for k, (store, rel) in table.items():
    Mk = (U[:, :k] * s[:k]) @ Vt[:k]
    assert k * (m + nn + 1) == store
    assert abs(np.linalg.norm(M - Mk) / np.linalg.norm(M) - rel) < 5e-5
    assert abs(np.sqrt((s[k:] ** 2).sum() / (s**2).sum()) - rel) < 5e-5

# ---------- 例：拆分 4096×4096 的线性层 ----------
assert 4096**2 == 16_777_216
assert 256 * (4096 + 4096) == 2_097_152 and 4096**2 // (256 * 8192) == 8
assert 4096 * 4096 // (4096 + 4096) == 2048
rng = np.random.default_rng(0)
d_out, d_in, k = 512, 1024, 32
W = rng.standard_normal((d_out, k)) @ rng.standard_normal((k, d_in)) / k + 0.01 * rng.standard_normal((d_out, d_in))
U, s, Vt = np.linalg.svd(W, full_matrices=False)
W1, W2 = s[:k, None] * Vt[:k], U[:, :k]
x = rng.standard_normal((4, d_in))
y, y2 = x @ W.T, x @ W1.T @ W2.T
assert (W.size, W1.size + W2.size) == (524288, 49152)
assert abs(np.linalg.norm(y - y2) / np.linalg.norm(y) - 0.0525) < 5e-5

# ---------- 例：LoRA 的可训练参数量 ----------
d, r, L = 4096, 8, 32
assert r * (d + d) == 65_536
assert r * (d + d) * 2 * L == 4_194_304
assert 2 * L * d * d == 1_073_741_824
assert sp.Rational(r * 2 * d, d * d) == sp.Rational(2 * r, d) == sp.Rational(16, 4096)
assert round(16 / 4096 * 100, 2) == 0.39
assert round(4_194_304 / 7e9 * 100, 2) == 0.06
assert 4_194_304 * 2 == 8 * 2**20

# ---------- 例：手算一次 LoRA 合并 ----------
W = sp.Matrix([[1, 2, 3], [0, 1, 0]])
B = sp.Matrix([1, 2])
A = sp.Matrix([[1, 0, -1]])
dW = 2 * B * A
assert dW == sp.Matrix([[2, 0, -2], [4, 0, -4]]) and dW.rank() == 1
Wm = W + dW
assert Wm == sp.Matrix([[3, 2, 1], [4, 1, -4]])
x1, x2 = sp.Matrix([1, 0, 0]), sp.Matrix([1, 1, 1])
assert A * x1 == sp.Matrix([1]) and W * x1 == sp.Matrix([1, 0])
assert W * x1 + 2 * B * (A * x1) == Wm * x1 == sp.Matrix([3, 4])
assert A * x2 == sp.Matrix([0]) and W * x2 == Wm * x2 == sp.Matrix([6, 1])

# 正文：LoRA 的 NumPy 代码
rng = np.random.default_rng(0)
d_out, d_in, r, alpha = 6, 4, 2, 4
W = rng.standard_normal((d_out, d_in))
A = rng.standard_normal((r, d_in)) * 0.1
B = np.zeros((d_out, r))
fwd = lambda x, W, A, B: x @ W.T + (alpha / r) * (x @ A.T) @ B.T
x = rng.standard_normal((3, d_in))
assert np.allclose(fwd(x, W, A, B), x @ W.T)
B = rng.standard_normal((d_out, r))
dW = (alpha / r) * B @ A
assert np.allclose(fwd(x, W, A, B), x @ (W + dW).T)
assert (np.linalg.matrix_rank(dW), np.linalg.matrix_rank(W + dW)) == (2, 4)

# 正文：W 本身不低秩
rng = np.random.default_rng(0)
d, r = 256, 8
W = rng.standard_normal((d, d)) / np.sqrt(d)
s = np.linalg.svd(W, compute_uv=False)
assert abs(np.sqrt((s[r:] ** 2).sum() / (s**2).sum()) - 0.942) < 5e-4
dW = rng.standard_normal((d, r)) @ rng.standard_normal((r, d)) * 0.01
assert (np.linalg.matrix_rank(dW), np.linalg.matrix_rank(W + dW)) == (8, 256)

# ---------- 正文：embedding 的 PCA 可视化 ----------
def pca(X, k):
    mu = X.mean(axis=0)
    Xc = X - mu
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = s**2 / (len(X) - 1)
    return mu, Vt[:k], Xc @ Vt[:k].T, var / var.sum()

def clusters(n_cls, d=64, per=100, spread=8.0, seed=0):
    rng = np.random.default_rng(seed)
    centers = rng.standard_normal((n_cls, d)) * spread / np.sqrt(d)
    labels = np.repeat(np.arange(n_cls), per)
    return centers[labels] + rng.standard_normal((n_cls * per, d)), labels

def centroid_acc(P, labels):
    C = np.stack([P[labels == c].mean(0) for c in np.unique(labels)])
    d2 = ((P[:, None, :] - C[None]) ** 2).sum(-1)
    return (d2.argmin(1) == labels).mean()

expect = {3: (0.435, 1.000, 1.000), 12: (0.157, 1.000, 0.630)}
for n_cls, (e_ratio, e_full, e_2d) in expect.items():
    Xs, labels = clusters(n_cls)
    _, _, Zs, ratio = pca(Xs, 2)
    assert abs(ratio[:2].sum() - e_ratio) < 5e-4
    assert abs(centroid_acc(Xs, labels) - e_full) < 5e-4
    assert abs(centroid_acc(Zs, labels) - e_2d) < 5e-4
    # 簇中心（去均值后）张成 n_cls-1 维
    C = np.stack([Xs[labels == c].mean(0) for c in range(n_cls)])
    assert np.linalg.matrix_rank(C - C.mean(0)) == n_cls - 1

print("verify_pca-lowrank: all checks passed")
