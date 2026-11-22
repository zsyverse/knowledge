"""验算第 11 章（矩阵求导与反向传播）例题与正文中的数字。

    .venv/bin/python scripts/linalg/verify_matrix-calculus.py
"""
import numpy as np
import sympy as sp

R = sp.Rational

# ---------- 例：按定义求梯度、Hessian 和 Jacobian ----------
x1, x2 = sp.symbols("x1 x2")
f = x1**2 * x2 + 2 * x2**2
at = {x1: 1, x2: 2}
grad = sp.Matrix([f.diff(x1), f.diff(x2)])
assert grad == sp.Matrix([2 * x1 * x2, x1**2 + 4 * x2]) and grad.subs(at) == sp.Matrix([4, 9])
H = sp.hessian(f, (x1, x2))
assert H == sp.Matrix([[2 * x2, 2 * x1], [2 * x1, 4]]) and H.subs(at) == sp.Matrix([[4, 2], [2, 4]])
g = sp.Matrix([x1 * x2, x1**2 + x2, 3 * x2])
J = g.jacobian([x1, x2])
assert J == sp.Matrix([[x2, x1], [2 * x1, 1], [0, 3]]) and J.subs(at) == sp.Matrix([[2, 1], [2, 1], [0, 3]])

# ---------- 例：x'Ax 的梯度 ----------
A = sp.Matrix([[1, 2], [0, 3]])
xv = sp.Matrix([x1, x2])
q = (xv.T * A * xv)[0]
assert sp.expand(q) == x1**2 + 2 * x1 * x2 + 3 * x2**2
gq = sp.Matrix([q.diff(x1), q.diff(x2)])
assert sp.simplify(gq - (A + A.T) * xv) == sp.zeros(2, 1)
assert A + A.T == sp.Matrix([[2, 2], [2, 6]]) and gq.subs(at) == sp.Matrix([6, 14])

# ---------- 例：a'Wb 与平方损失 ----------
a, b = sp.Matrix([1, 2]), sp.Matrix([3, 0, -1])
Wsym = sp.Matrix(2, 3, sp.symbols("w0:6"))
L = (a.T * Wsym * b)[0]
assert sp.Matrix(2, 3, lambda i, j: L.diff(Wsym[i, j])) == a * b.T == sp.Matrix([[3, 0, -1], [6, 0, -2]])
Xs = sp.Matrix(2, 3, sp.symbols("p0:6"))
Ts = sp.Matrix(2, 2, sp.symbols("t0:4"))
Rm = Xs * Wsym.T - Ts
L2 = sum(e**2 for e in Rm) / 2
assert sp.simplify(sp.Matrix(2, 3, lambda i, j: L2.diff(Wsym[i, j])) - Rm.T * Xs) == sp.zeros(2, 3)

# ---------- 例：最小二乘的梯度、Hessian 与牛顿步 ----------
A = sp.Matrix([[1, 1], [1, 2], [1, 3]])
bb = sp.Matrix([1, 2, 2])
assert A.T * A == sp.Matrix([[3, 6], [6, 14]]) and A.T * bb == sp.Matrix([5, 11])
assert 2 * A.T * (A * sp.zeros(2, 1) - bb) == sp.Matrix([-10, -22])
assert 2 * A.T * A == sp.Matrix([[6, 12], [12, 28]])
assert (A.T * A).det() == 6
assert (A.T * A).inv() == sp.Matrix([[14, -6], [-6, 3]]) / 6
xh = (A.T * A).inv() * A.T * bb
assert xh == sp.Matrix([R(2, 3), R(1, 2)])
assert A * xh - bb == sp.Matrix([R(1, 6), -R(1, 3), R(1, 6)])
assert A.T * (A * xh - bb) == sp.zeros(2, 1)
assert sp.zeros(2, 1) - (2 * A.T * A).inv() * sp.Matrix([-10, -22]) == xh

# ---------- 例：用 VJP 逐步回传 ----------
A = sp.Matrix([[1, 2], [0, 1], [1, 0]])
x0 = sp.Matrix([1, 1])
y = A * x0
z = y.multiply_elementwise(y)
assert y == sp.Matrix([3, 1, 1]) and z == sp.Matrix([9, 1, 1]) and sum(z) == 11
gz = sp.ones(3, 1)
gy = (2 * y).multiply_elementwise(gz)
assert gy == sp.Matrix([6, 2, 2])
gx = A.T * gy
assert gx == sp.Matrix([8, 14])
assert A.T * A == sp.Matrix([[2, 2], [2, 5]]) and 2 * A.T * A * x0 == gx

# ---------- 例：手算一个线性层的反向传播 ----------
X = sp.Matrix([[1, 2, 0], [0, 1, -1]])
W = sp.Matrix([[1, 0, 2], [-1, 1, 0]])
bv = sp.Matrix([[0, 1]])
T = sp.Matrix([[0, 2], [-1, 0]])
assert X * W.T == sp.Matrix([[1, 1], [-2, 1]])
Y = X * W.T + sp.ones(2, 1) * bv
assert Y == sp.Matrix([[1, 2], [-2, 2]])
delta = Y - T
assert delta == sp.Matrix([[1, 0], [-1, 2]])
assert sum(e**2 for e in delta) / 2 == 3
assert delta.T * X == sp.Matrix([[1, 1, 1], [0, 2, -2]])
assert delta.T * sp.ones(2, 1) == sp.Matrix([0, 2])
assert delta * W == sp.Matrix([[1, 0, 2], [-3, 2, -2]])
o1 = delta.row(0).T * X.row(0)
o2 = delta.row(1).T * X.row(1)
assert o1 == sp.Matrix([[1, 2, 0], [0, 0, 0]]) and o2 == sp.Matrix([[0, -1, 1], [0, 2, -2]])
assert o1 + o2 == delta.T * X
# 与逐元素求导的结果一致
Ws = sp.Matrix(2, 3, sp.symbols("w0:6"))
bs = sp.Matrix(1, 2, sp.symbols("c0:2"))
Xsym = sp.Matrix(2, 3, sp.symbols("p0:6"))
Ls = sum(e**2 for e in (Xsym * Ws.T + sp.ones(2, 1) * bs - T)) / 2
sub = {**dict(zip(Ws, W)), **dict(zip(bs, bv)), **dict(zip(Xsym, X))}
assert sp.Matrix(2, 3, lambda i, j: Ls.diff(Ws[i, j])).subs(sub) == delta.T * X
assert sp.Matrix(2, 3, lambda i, j: Ls.diff(Xsym[i, j])).subs(sub) == delta * W
assert sp.Matrix(2, 1, lambda i, j: Ls.diff(bs[i])).subs(sub) == sp.Matrix([0, 2])

# ---------- 例：手算 softmax 交叉熵的梯度 ----------
zs = sp.symbols("z0:3")
ez = [sp.exp(v) for v in zs]
p_sym = sp.Matrix([e / sum(ez) for e in ez])
zval = dict(zip(zs, [0, sp.log(2), sp.log(5)]))
p = sp.simplify(p_sym.subs(zval))
assert p == sp.Matrix([R(1, 8), R(1, 4), R(5, 8)])
assert abs(float(-sp.log(R(5, 8))) - 0.470) < 5e-4
Jsm = sp.simplify(p_sym.jacobian(zs).subs(zval))
assert Jsm == sp.diag(*p) - p * p.T == sp.Matrix([[7, -2, -5], [-2, 12, -10], [-5, -10, 15]]) / 64
assert Jsm * sp.ones(3, 1) == sp.zeros(3, 1) and Jsm.rank() == 2 and Jsm == Jsm.T
yv = sp.Matrix([0, 0, 1])
Lce = -sp.log(p_sym[2])
gce = sp.simplify(sp.Matrix([Lce.diff(v) for v in zs]).subs(zval))
assert gce == p - yv == sp.Matrix([R(1, 8), R(1, 4), -R(3, 8)])
dLdp = sp.Matrix([0, 0, -R(8, 5)])
assert Jsm.T * dLdp == gce

# ---------- 正文：ReLU 掩码 ----------
assert (np.array([4, 5, 6]) * (np.array([1.5, -2, 0.3]) > 0)).tolist() == [4, 0, 6]

# ---------- 例：B=0 时 LoRA 的第一步梯度 ----------
G = sp.Matrix([[1, 2, 0], [0, 1, -1]])
A = sp.Matrix([[1, 0, -1]])
B = sp.zeros(2, 1)
s = 2
gB, gA = s * G * A.T, s * B.T * G
assert gB == sp.Matrix([2, 2]) and gA == sp.zeros(1, 3)
B = B - R(1, 10) * gB
assert B == sp.Matrix([-R(1, 5), -R(1, 5)])
assert s * B.T * G == sp.Matrix([[-R(2, 5), -R(6, 5), R(2, 5)]])
# 公式本身：对符号变量逐元素求导
As = sp.Matrix(1, 3, sp.symbols("a0:3"))
Bs = sp.Matrix(2, 1, sp.symbols("b0:2"))
W0 = sp.Matrix(2, 3, sp.symbols("w0:6"))
Xs = sp.Matrix([[1, 2, 0], [0, 1, -1], [2, 0, 1]])
Ts = sp.Matrix([[0, 2], [-1, 0], [1, 1]])
Wp = W0 + s * Bs * As
Rm = Xs * Wp.T - Ts
Ll = sum(e**2 for e in Rm) / 2
Gs = Rm.T * Xs
assert sp.simplify(sp.Matrix(2, 1, lambda i, j: Ll.diff(Bs[i])) - s * Gs * As.T) == sp.zeros(2, 1)
assert sp.simplify(sp.Matrix(1, 3, lambda i, j: Ll.diff(As[j])) - s * Bs.T * Gs) == sp.zeros(1, 3)

# ---------- 正文代码：公式表、两层 MLP、LoRA 的数值检查 ----------
def num_grad(f, x, h=1e-5):
    g = np.zeros_like(x)
    for i in np.ndindex(x.shape):
        old = x[i]
        x[i] = old + h; fp = f(x)
        x[i] = old - h; fm = f(x)
        x[i] = old
        g[i] = (fp - fm) / (2 * h)
    return g

rng = np.random.default_rng(0)
A = rng.standard_normal((3, 3)); a = rng.standard_normal(3); b = rng.standard_normal(4)
x = rng.standard_normal(3); W = rng.standard_normal((3, 4))
M = rng.standard_normal((5, 3)); c = rng.standard_normal(5)
Xn = rng.standard_normal((6, 4)); Tn = rng.standard_normal((6, 3))
for f, var, formula in [
    (lambda x: a @ x, x, a),
    (lambda x: x @ x, x, 2 * x),
    (lambda x: x @ A @ x, x, (A + A.T) @ x),
    (lambda x: ((M @ x - c) ** 2).sum(), x, 2 * M.T @ (M @ x - c)),
    (lambda W: a @ W @ b, W, np.outer(a, b)),
    (lambda W: np.trace(W.T @ np.ones((3, 4))), W, np.ones((3, 4))),
    (lambda W: (W**2).sum(), W, 2 * W),
    (lambda W: ((Xn @ W.T - Tn) ** 2).sum(), W, 2 * (Xn @ W.T - Tn).T @ Xn),
]:
    assert np.abs(num_grad(f, var) - formula).max() < 1e-7

def forward(params, X, Y):
    W1, b1, W2, b2 = params
    Z1 = X @ W1.T + b1
    H = np.maximum(Z1, 0)
    Z2 = H @ W2.T + b2
    Z2 = Z2 - Z2.max(axis=1, keepdims=True)
    logP = Z2 - np.log(np.exp(Z2).sum(axis=1, keepdims=True))
    return -(Y * logP).sum() / len(X), (Z1, H, np.exp(logP))

def backward(params, X, Y, cache):
    W1, b1, W2, b2 = params
    Z1, H, P = cache
    d2 = (P - Y) / len(X)
    gW2, gb2 = d2.T @ H, d2.sum(axis=0)
    d1 = (d2 @ W2) * (Z1 > 0)
    return d1.T @ X, d1.sum(axis=0), gW2, gb2

rng = np.random.default_rng(0)
n, d, h, c = 8, 5, 16, 3
X = rng.standard_normal((n, d))
Y = np.eye(c)[rng.integers(0, c, size=n)]
params = [rng.standard_normal((h, d)) * 0.5, np.zeros(h), rng.standard_normal((c, h)) * 0.5, np.zeros(c)]
loss, cache = forward(params, X, Y)
assert abs(loss - 1.4417) < 5e-5
for p_, g_ in zip(params, backward(params, X, Y, cache)):
    gn = num_grad(lambda _: forward(params, X, Y)[0], p_)
    assert g_.shape == p_.shape
    assert np.linalg.norm(g_ - gn) / (np.linalg.norm(g_) + np.linalg.norm(gn)) < 1e-9
# 线性层权重梯度的秩不超过 batch 大小
assert np.linalg.matrix_rank(backward(params, X[:3], Y[:3], forward(params, X[:3], Y[:3])[1])[0]) <= 3

rng = np.random.default_rng(0)
d_out, d_in, r, s = 4, 5, 2, 2.0
W = rng.standard_normal((d_out, d_in))
A = rng.standard_normal((r, d_in))
B = np.zeros((d_out, r))
X = rng.standard_normal((6, d_in)); T = rng.standard_normal((6, d_out))
loss_fn = lambda A, B: 0.5 * ((X @ (W + s * B @ A).T - T) ** 2).sum()
G = (X @ (W + s * B @ A).T - T).T @ X
gB, gA = s * G @ A.T, s * B.T @ G
assert np.allclose(gB, num_grad(lambda B: loss_fn(A, B), B))
assert np.allclose(gA, num_grad(lambda A: loss_fn(A, B), A))
assert np.abs(gA).max() == 0 and np.abs(gB).max() > 0
B = B - 0.01 * gB
G = (X @ (W + s * B @ A).T - T).T @ X
assert np.allclose(s * B.T @ G, num_grad(lambda A: loss_fn(A, B), A)) and np.abs(s * B.T @ G).max() > 0

print("verify_matrix-calculus: all checks passed")
