"""验算第 12 章（用线性代数读 Transformer）例题与正文中的数字。

    .venv/bin/python scripts/linalg/verify_transformer-linalg.py
"""
import numpy as np
import sympy as sp

R = sp.Rational

# ---------- 例：权重绑定下的 logits ----------
E = sp.Matrix([[1, 0], [0, 1], [1, 1], [-1, 0]])
h = sp.Matrix([[2, 1]])
z = h * E.T
assert z == sp.Matrix([[2, 1, 3, -2]])
ez = [sp.exp(v) for v in z]
p = [float(e / sum(ez)) for e in ez]
assert [round(v, 3) for v in p] == [0.244, 0.090, 0.662, 0.004]
assert p.index(max(p)) == 2
cos1 = (h * E.row(0).T)[0] / (h.norm() * E.row(0).norm())
cos3 = (h * E.row(2).T)[0] / (h.norm() * E.row(2).norm())
assert sp.simplify(cos1 - 2 / sp.sqrt(5)) == 0 and abs(float(cos1) - 0.894) < 5e-4
assert sp.simplify(cos3 - 3 / sp.sqrt(10)) == 0 and abs(float(cos3) - 0.949) < 5e-4
assert E.row(2).norm() == sp.sqrt(2) and E.row(3) == -E.row(0) and z[3] == -z[0]
ids = np.array([2, 0, 3])
En = np.array(E.tolist(), dtype=float)
assert np.array_equal(np.eye(4)[ids] @ En, En[ids])
rng = np.random.default_rng(0)
H, E_big = rng.standard_normal((200, 64)), rng.standard_normal((1000, 64))
assert np.linalg.matrix_rank(H @ E_big.T) == 64

# ---------- 例：手算 3 个 token 的因果注意力 ----------
X = sp.Matrix([[1, 0], [0, 1], [1, 1]])
WQ = sp.log(2) * sp.Matrix([1, 1])
WK = sp.Matrix([1, 0])
WV = sp.Matrix([[0, 3], [3, 0]])
Q, K, V = X * WQ, X * WK, X * WV
assert Q == sp.log(2) * sp.Matrix([1, 1, 2]) and K == sp.Matrix([1, 0, 1])
assert V == sp.Matrix([[0, 3], [3, 0], [3, 3]])
S = Q * K.T
assert S == sp.log(2) * sp.Matrix([[1, 0, 1], [1, 0, 1], [2, 0, 2]])
WQK = WQ * WK.T
assert WQK == sp.log(2) * sp.Matrix([[1, 0], [1, 0]]) and WQK.rank() == 1
# 双线性型与 QK' 一致
assert sp.simplify(X * WQK * X.T - S) == sp.zeros(3, 3)
expS = sp.Matrix(3, 3, lambda i, j: sp.simplify(sp.exp(S[i, j])) if j <= i else 0)
assert expS == sp.Matrix([[2, 0, 0], [2, 1, 0], [4, 1, 4]])
A = sp.Matrix(3, 3, lambda i, j: expS[i, j] / sum(expS.row(i)))
assert A == sp.Matrix([[1, 0, 0], [R(2, 3), R(1, 3), 0], [R(4, 9), R(1, 9), R(4, 9)]])
assert A.is_lower and all(sum(A.row(i)) == 1 for i in range(3))
O = A * V
assert O == sp.Matrix([[0, 3], [1, 2], [R(5, 3), R(8, 3)]])

def softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    P = np.exp(S)
    return P / P.sum(axis=-1, keepdims=True)

def attention(X, WQ, WK, WV, causal=True):
    n, dk = len(X), WQ.shape[1]
    S = (X @ WQ) @ (X @ WK).T / np.sqrt(dk)
    if causal:
        S = np.where(np.tril(np.ones((n, n), dtype=bool)), S, -np.inf)
    A = softmax(S)
    return A @ (X @ WV), A

On, An = attention(np.array(X.tolist(), dtype=float), np.log(2) * np.array([[1.0], [1]]), np.array([[1.0], [0]]),
                   np.array(WV.tolist(), dtype=float))
assert np.allclose(An, np.array(A.tolist(), dtype=float)) and np.allclose(On, np.array(O.tolist(), dtype=float))

# ---------- 正文：多头 = 各头之和 ----------
rng = np.random.default_rng(0)
n, d, h_ = 5, 8, 2
dk = d // h_
X5 = rng.standard_normal((n, d))
WQ8, WK8, WV8, WO8 = (rng.standard_normal((d, d)) for _ in range(4))
heads = [attention(X5, WQ8[:, t * dk:(t + 1) * dk], WK8[:, t * dk:(t + 1) * dk], WV8[:, t * dk:(t + 1) * dk])[0] for t in range(h_)]
out = np.concatenate(heads, axis=1) @ WO8
total = np.zeros((n, d))
for t in range(h_):
    sl = slice(t * dk, (t + 1) * dk)
    _, At = attention(X5, WQ8[:, sl], WK8[:, sl], WV8[:, sl])
    OV = WV8[:, sl] @ WO8[sl, :]
    assert np.linalg.matrix_rank(OV) == 4 and np.linalg.matrix_rank(WQ8[:, sl] @ WK8[:, sl].T) == 4
    total += At @ X5 @ OV
assert np.allclose(out, total)

# ---------- 例：LayerNorm 与 RMSNorm 的几何 ----------
x = sp.Matrix([4, 2, 0, -2])
dd = 4
P = sp.eye(dd) - sp.ones(dd, dd) / dd
assert P * P == P and P.T == P and P.rank() == dd - 1 and P * sp.ones(dd, 1) == sp.zeros(dd, 1)
xt = P * x
assert xt == sp.Matrix([3, 1, -1, -3]) and sum(xt) == 0
assert xt.norm() == sp.sqrt(20) and sp.sqrt(R(20, 4)) == sp.sqrt(5)
ln = xt / sp.sqrt(5)
assert sp.simplify(ln.norm() - 2) == 0
assert [round(float(v), 3) for v in ln] == [1.342, 0.447, -0.447, -1.342]
rms = sp.sqrt(sum(v**2 for v in x) / dd)
assert rms == sp.sqrt(6)
rn = x / rms
assert sp.simplify(rn.norm() - 2) == 0
assert [round(float(v), 3) for v in rn] == [1.633, 0.816, 0.0, -0.816]
xn = np.array([4.0, 2, 0, -2])
ln_f = lambda v: (v - v.mean()) / v.std()
rms_f = lambda v: v / np.sqrt((v**2).mean())
Pn = np.eye(4) - np.ones((4, 4)) / 4
assert np.allclose(ln_f(xn), rms_f(Pn @ xn)) and np.allclose(ln_f(3 * xn + 5), ln_f(xn)) and np.allclose(rms_f(3 * xn), rms_f(xn))

# ---------- 例：RoPE 的内积只依赖相对位置 ----------
phi, al, be = sp.symbols("phi alpha beta", real=True)
Rot = lambda a: sp.Matrix([[sp.cos(a), -sp.sin(a)], [sp.sin(a), sp.cos(a)]])
assert sp.simplify(Rot(phi).T * Rot(phi)) == sp.eye(2)
assert sp.simplify(Rot(al) * Rot(be) - Rot(al + be)) == sp.zeros(2, 2)
assert sp.simplify(Rot(al).T * Rot(be) - Rot(be - al)) == sp.zeros(2, 2)
th = sp.pi / 2
assert Rot(th) == sp.Matrix([[0, -1], [1, 0]])
q, k = sp.Matrix([1, 0]), sp.Matrix([2, 1])
qm = lambda m: Rot(m * th) * q
kn = lambda n: Rot(n * th) * k
assert qm(1) == sp.Matrix([0, 1]) and kn(2) == sp.Matrix([-2, -1]) and (qm(1).T * kn(2))[0] == -1
assert qm(2) == sp.Matrix([-1, 0]) and kn(3) == sp.Matrix([1, -2]) and (qm(2).T * kn(3))[0] == -1
assert Rot(th) * k == sp.Matrix([-1, 2]) and (q.T * Rot(th) * k)[0] == -1
assert [(q.T * Rot(j * th) * k)[0] for j in (0, 2, 3)] == [2, -2, 1]
assert kn(3).norm() == k.norm() == sp.sqrt(5)

def rope(x, pos, base=10000.0):
    d = x.shape[-1]
    theta = base ** (-np.arange(0, d, 2) / d)
    ang = pos[:, None] * theta
    cos, sin = np.cos(ang), np.sin(ang)
    out = np.empty_like(x)
    out[:, 0::2] = x[:, 0::2] * cos - x[:, 1::2] * sin
    out[:, 1::2] = x[:, 0::2] * sin + x[:, 1::2] * cos
    return out

rng = np.random.default_rng(0)
qv, kv = rng.standard_normal((1, 8)), rng.standard_normal((1, 8))
score = lambda m, n: (rope(qv, np.array([m])) @ rope(kv, np.array([n])).T).item()
assert abs(score(3, 7) - score(103, 107)) < 1e-9 and abs(score(3, 7) + 1.833596) < 5e-7 and abs(score(3, 8) + 1.812200) < 5e-7
assert np.isclose(np.linalg.norm(rope(qv, np.array([50]))), np.linalg.norm(qv))
# rope 与显式的分块旋转矩阵一致
m_ = 5
thetas = 10000.0 ** (-np.arange(0, 8, 2) / 8)
Rb = np.zeros((8, 8))
for i, t in enumerate(thetas):
    c, s = np.cos(m_ * t), np.sin(m_ * t)
    Rb[2 * i:2 * i + 2, 2 * i:2 * i + 2] = [[c, -s], [s, c]]
assert np.allclose(rope(qv, np.array([m_]))[0], Rb @ qv[0]) and np.allclose(Rb.T @ Rb, np.eye(8))

# ---------- 例：参数量 ----------
def count_params(V, d, L, d_ff, ffn_mats=2, tie=True):
    parts = {
        "embedding": V * d,
        "attention": L * 4 * d * d,
        "ffn": L * ffn_mats * d * d_ff,
        "norm": (2 * L + 1) * d,
        "unembedding": 0 if tie else V * d,
    }
    return sum(parts.values()), parts

total, parts = count_params(V=1000, d=64, L=2, d_ff=256)
assert parts == {"embedding": 64000, "attention": 32768, "ffn": 65536, "norm": 320, "unembedding": 0}
assert total == 162624 and count_params(1000, 64, 2, 256, tie=False)[0] == 226624
assert [round(v / total * 100, 1) for v in parts.values()] == [39.4, 20.1, 40.3, 0.2, 0.0]
total, parts = count_params(V=32000, d=4096, L=32, d_ff=11008, ffn_mats=3, tie=False)
assert parts == {"embedding": 131072000, "attention": 2147483648, "ffn": 4328521728, "norm": 266240, "unembedding": 131072000}
assert total == 6738415616 and 65 * 4096 == 266240
assert [round(v / total * 100, 1) for v in parts.values()] == [1.9, 31.9, 64.2, 0.0, 1.9]

# ---------- 正文：完整的前向计算 ----------
def rmsnorm(X, g):
    return X / np.sqrt((X**2).mean(axis=-1, keepdims=True)) * g

def block(X, p, h, pos):
    n, d = X.shape
    dk = d // h
    Xn = rmsnorm(X, p["g1"])
    d_attn = np.zeros_like(X)
    mask = np.tril(np.ones((n, n), dtype=bool))
    for t in range(h):
        sl = slice(t * dk, (t + 1) * dk)
        Q, K, V = rope(Xn @ p["WQ"][:, sl], pos), rope(Xn @ p["WK"][:, sl], pos), Xn @ p["WV"][:, sl]
        A = softmax(np.where(mask, Q @ K.T / np.sqrt(dk), -np.inf))
        assert np.allclose(A, np.tril(A)) and np.allclose(A.sum(1), 1) and (A >= 0).all()
        d_attn += A @ V @ p["WO"][sl, :]
    X = X + d_attn
    d_ffn = np.maximum(rmsnorm(X, p["g2"]) @ p["W1"], 0) @ p["W2"]
    return X + d_ffn, [d_attn, d_ffn]

V, d, h, d_ff, L = 1000, 64, 4, 256, 2
rng = np.random.default_rng(0)
init = lambda *shape: rng.standard_normal(shape) * 0.1
E = init(V, d)
layers = [dict(WQ=init(d, d), WK=init(d, d), WV=init(d, d), WO=init(d, d),
               W1=init(d, d_ff), W2=init(d_ff, d), g1=np.ones(d), g2=np.ones(d)) for _ in range(L)]
g_final = np.ones(d)

def forward(ids):
    X0 = E[ids]
    X, deltas = X0, []
    for p in layers:
        X, ds = block(X, p, h, np.arange(len(ids)))
        deltas += ds
    return rmsnorm(X, g_final) @ E.T, X0, X, deltas

ids = rng.integers(0, V, size=100)
logits, X0, XL, deltas = forward(ids)
assert X0.shape == (100, 64) and logits.shape == (100, 1000)
assert np.allclose(XL, X0 + sum(deltas)) and np.linalg.matrix_rank(logits) == 64
ids2 = ids.copy()
ids2[-1] = (ids2[-1] + 1) % V
assert np.allclose(forward(ids2)[0][:-1], logits[:-1]) and not np.allclose(forward(ids2)[0][-1], logits[-1])
n_params = E.size + g_final.size + sum(v.size for p in layers for v in p.values())
assert n_params == 162624 == count_params(V, d, L, d_ff)[0]
# 平移不变：所有位置同时加一个偏移，输出不变（RoPE 只依赖相对位置）
def forward_pos(ids, offset):
    X = E[ids]
    for p in layers:
        X, _ = block(X, p, h, np.arange(len(ids)) + offset)
    return rmsnorm(X, g_final) @ E.T
assert np.allclose(forward_pos(ids, 0), forward_pos(ids, 37))

print("verify_transformer-linalg: all checks passed")
