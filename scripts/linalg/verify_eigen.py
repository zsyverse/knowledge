"""验算第 7 章「特征值与特征向量」里的例题和正文中的数。

    .venv/bin/python scripts/linalg/verify_eigen.py
"""
import numpy as np
import sympy as sp

R = sp.Rational
lam = sp.symbols("lambda")


def main():
    # ---- 第 1 节 / 例：二阶矩阵 ----
    A = sp.Matrix([[1, 2], [1, 0]])
    assert A.eigenvals() == {2: 1, -1: 1}
    v1, v2, x = sp.Matrix([2, 1]), sp.Matrix([1, -1]), sp.Matrix([0, 1])
    assert A * v1 == 2 * v1 and A * v2 == -v2
    assert A * x == sp.Matrix([2, 0])
    assert x == R(1, 3) * v1 - R(2, 3) * v2
    assert A.trace() == 1 and A.det() == -2
    assert sp.expand((lam * sp.eye(2) - A).det() - (lam - 2) * (lam + 1)) == 0
    assert 2 * sp.eye(2) - A == sp.Matrix([[1, -2], [-1, 2]])
    assert -sp.eye(2) - A == sp.Matrix([[-2, -2], [-1, -1]])

    # ---- 例：三阶矩阵，重根 ----
    B = sp.Matrix([[4, 1, -1], [2, 5, -2], [1, 1, 2]])
    assert sp.expand((lam * sp.eye(3) - B).det() - (lam - 3) ** 2 * (lam - 5)) == 0
    assert 3 * sp.eye(3) - B == sp.Matrix([[-1, -1, 1], [-2, -2, 2], [-1, -1, 1]])
    assert 5 * sp.eye(3) - B == sp.Matrix([[1, -1, 1], [-2, 0, 2], [-1, -1, 3]])
    b1, b2, b3 = sp.Matrix([-1, 1, 0]), sp.Matrix([1, 0, 1]), sp.Matrix([1, 2, 1])
    assert B * b1 == 3 * b1 and B * b2 == 3 * b2 and B * b3 == 5 * b3
    assert B * b3 == sp.Matrix([5, 10, 5])
    assert B.trace() == 11 and B.det() == 45
    assert (3 * sp.eye(3) - B).rank() == 1

    # ---- 例：对角化与 A^k，递推数列 ----
    P = sp.Matrix([[2, 1], [1, -1]])
    assert P.inv() == R(1, 3) * sp.Matrix([[1, 1], [1, -2]])
    assert P.inv() * A * P == sp.diag(2, -1)
    k = sp.symbols("k", integer=True, nonnegative=True)
    Ak = R(1, 3) * sp.Matrix([[2 ** (k + 1) + (-1) ** k, 2 ** (k + 1) - 2 * (-1) ** k],
                              [2**k - (-1) ** k, 2**k + 2 * (-1) ** k]])
    for kk in range(0, 9):
        assert Ak.subs(k, kk) == A**kk
    assert R(1, 3) * sp.Matrix([[3, 6], [3, 0]]) == A
    seq = [0, 1]
    for _ in range(10):
        seq.append(seq[-1] + 2 * seq[-2])
    assert seq[:7] == [0, 1, 1, 3, 5, 11, 21]
    assert all(seq[i] == (2**i - (-1) ** i) // 3 for i in range(len(seq)))

    # ---- 例：能否对角化 ----
    PB = sp.Matrix.hstack(b1, b2, b3)
    assert PB == sp.Matrix([[-1, 1, 1], [1, 0, 2], [0, 1, 1]])
    assert PB.inv() * B * PB == sp.diag(3, 3, 5)
    Bj = sp.Matrix([[3, 1, 0], [0, 3, 0], [0, 0, 5]])
    assert sp.expand((lam * sp.eye(3) - Bj).det() - (lam - 3) ** 2 * (lam - 5)) == 0
    assert 3 * sp.eye(3) - Bj == sp.Matrix([[0, -1, 0], [0, 0, 0], [0, 0, -2]])
    assert (3 * sp.eye(3) - Bj).rank() == 2 and not Bj.is_diagonalizable()
    assert B.is_diagonalizable()
    J = sp.Matrix([[1, 1], [0, 1]])
    assert (sp.eye(2) - J).rank() == 1 and not J.is_diagonalizable() and J.det() != 0
    assert sp.Matrix([[1, 0], [0, 0]]).is_diagonalizable()

    # ---- 例：旋转加缩放 ----
    C = sp.Matrix([[1, -1], [1, 1]])
    assert set(C.eigenvals()) == {1 + sp.I, 1 - sp.I}
    assert sp.Abs(1 + sp.I) == sp.sqrt(2) and sp.arg(1 + sp.I) == sp.pi / 4
    assert C**2 == sp.Matrix([[0, -2], [2, 0]]) and C**4 == -4 * sp.eye(2) and C**8 == 16 * sp.eye(2)
    th = sp.symbols("theta", real=True)
    Rm = sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
    assert sp.simplify((lam * sp.eye(2) - Rm).det() - (lam**2 - 2 * sp.cos(th) * lam + 1)) == 0

    # ---- 例：对称矩阵正交对角化 ----
    S = sp.Matrix([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    assert S.eigenvals() == {4: 1, 1: 2}
    q1 = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    q2 = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
    q3 = sp.Matrix([1, 1, -2]) / sp.sqrt(6)
    Q = sp.Matrix.hstack(q1, q2, q3)
    assert sp.simplify(Q.T * Q) == sp.eye(3)
    assert sp.simplify(Q.T * S * Q) == sp.diag(4, 1, 1)
    assert sp.simplify(4 * q1 * q1.T + q2 * q2.T + q3 * q3.T) == S
    assert sp.Matrix([1, -1, 0]).dot(sp.Matrix([1, 0, -1])) != 0
    a, b, d = sp.symbols("a b d", real=True)
    assert sp.expand((a + d) ** 2 - 4 * (a * d - b**2) - ((a - d) ** 2 + 4 * b**2)) == 0

    # ---- 第 6 节：eig / eigh / 幂迭代 ----
    An = np.array([[1.0, 2.0], [1.0, 0.0]])
    w, Pn = np.linalg.eig(An)
    assert np.allclose(w.real, [2, -1]) and np.allclose(An @ Pn, Pn * w)
    assert np.allclose(Pn.real.round(4), [[0.8944, -0.7071], [0.4472, 0.7071]])
    Sn = np.array(S.tolist(), dtype=float)
    ws, Qs = np.linalg.eigh(Sn)
    assert np.allclose(ws, [1, 1, 4]) and np.allclose(Qs.T @ Qs, np.eye(3))
    assert np.allclose(np.linalg.eigvals(np.array([[0.0, -1.0], [1.0, 0.0]])), [1j, -1j])

    def power_iteration(M, iters=50, seed=0):
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(M.shape[0])
        for _ in range(iters):
            v = M @ v
            v /= np.linalg.norm(v)
        return v @ M @ v, v

    assert np.isclose(power_iteration(An, 10)[0], 2.032285261462978)
    assert np.isclose(power_iteration(An, 20)[0], 2.0000349987644572)
    assert abs(power_iteration(An, 40)[0] - 2) < 1e-10

    # ---- 例：梯度下降的稳定学习率 ----
    H = sp.Matrix([[3, 1], [1, 3]])
    assert H.eigenvals() == {4: 1, 2: 1} and H.trace() == 6 and H.det() == 8
    x0 = sp.Matrix([1, 0])
    assert x0 == R(1, 2) * sp.Matrix([1, 1]) + R(1, 2) * sp.Matrix([1, -1])
    eta = R(2, 5)
    xk = x0
    for kk in range(1, 6):
        xk = xk - eta * H * xk
        closed = R(1, 2) * R(-3, 5) ** kk * sp.Matrix([1, 1]) + R(1, 2) * R(1, 5) ** kk * sp.Matrix([1, -1])
        assert xk == closed
        if kk == 1:
            assert xk == sp.Matrix([R(-1, 5), R(-2, 5)])
        if kk == 2:
            assert xk == sp.Matrix([R(1, 5), R(4, 25)])
    assert 1 - R(3, 5) * 4 == R(-7, 5) and 1 - R(3, 5) * 2 == R(-1, 5)
    Hn = np.array([[3.0, 1.0], [1.0, 3.0]])
    out = {}
    for e in (0.1, 0.4, 0.5, 0.6):
        xv = np.array([1.0, 0.0])
        for _ in range(50):
            xv = xv - e * (Hn @ xv)
        out[e] = np.linalg.norm(xv)
    assert np.isclose(out[0.1], 1.0092165219453994e-05)
    assert np.isclose(out[0.4], 5.7154117240146445e-12)
    assert np.isclose(out[0.5], np.sqrt(2) / 2)
    assert np.isclose(out[0.6], 14318145.984815756)
    assert np.isclose(np.sqrt(2) / 2 * 1.4**50, out[0.6], rtol=1e-6) and 1.3e7 < out[0.6] < 1.5e7

    # ---- 第 8 节：RNN ----
    assert abs(0.9**100 - 2.7e-5) < 0.1e-5 and abs(1.1**100 - 1.4e4) < 0.03e4
    rng = np.random.default_rng(0)
    n = 64
    W0 = rng.standard_normal((n, n)) / np.sqrt(n)
    rho0 = np.abs(np.linalg.eigvals(W0)).max()
    g = rng.standard_normal(n)
    g /= np.linalg.norm(g)
    expect = {0.9: ["0.267", "0.00228", "1.13e-05"], 1.0: ["0.764", "0.443", "0.426"], 1.1: ["1.98", "52", "5.87e+03"]}
    for rho in (0.9, 1.0, 1.1):
        W = W0 * (rho / rho0)
        v, res = g.copy(), []
        for kk in range(1, 101):
            v = W.T @ v
            if kk in (10, 50, 100):
                res.append(f"{np.linalg.norm(v):.3g}")
        assert res == expect[rho], (rho, res)

    Wt = sp.Matrix([[R(9, 10), 0], [R(3, 10), R(1, 2)]]).T
    assert Wt == sp.Matrix([[R(9, 10), R(3, 10)], [0, R(1, 2)]])
    assert Wt * sp.Matrix([1, 0]) == R(9, 10) * sp.Matrix([1, 0])
    assert Wt * sp.Matrix([3, -4]) == R(1, 2) * sp.Matrix([3, -4])
    gg = sp.Matrix([1, 1])
    assert gg == R(7, 4) * sp.Matrix([1, 0]) - R(1, 4) * sp.Matrix([3, -4])
    for kk in (1, 5, 10):
        assert Wt**kk * gg == R(7, 4) * R(9, 10) ** kk * sp.Matrix([1, 0]) - R(1, 4) * R(1, 2) ** kk * sp.Matrix([3, -4])
    g10 = np.array((Wt**10 * gg).evalf().tolist(), dtype=float).ravel()
    assert np.allclose(g10.round(4), [0.6095, 0.0010])
    norm = lambda kk: float((Wt**kk * gg).norm())
    assert norm(45) > 0.01 * np.sqrt(2) > norm(46)
    assert abs(np.log(0.01 * np.sqrt(2) / 1.75) / np.log(0.9) - 45.7) < 0.05
    assert abs(0.01 * np.sqrt(2) / 1.75 - 0.00808) < 5e-6

    # ---- 例：两状态马尔可夫链 ----
    T = sp.Matrix([[R(9, 10), R(1, 2)], [R(1, 10), R(1, 2)]])
    assert T.eigenvals() == {1: 1, R(2, 5): 1} and T.trace() == R(7, 5) and T.det() == R(2, 5)
    pi = sp.Matrix([R(5, 6), R(1, 6)])
    assert T * pi == pi and T * sp.Matrix([1, -1]) == R(2, 5) * sp.Matrix([1, -1])
    p = sp.Matrix([0, 1])
    assert p == pi - R(5, 6) * sp.Matrix([1, -1])
    seqp = []
    for kk in range(1, 4):
        p = T * p
        assert p == pi - R(5, 6) * R(2, 5) ** kk * sp.Matrix([1, -1])
        seqp.append(p)
    assert seqp[0] == sp.Matrix([R(1, 2), R(1, 2)])
    assert seqp[1] == sp.Matrix([R(7, 10), R(3, 10)])
    assert seqp[2] == sp.Matrix([R(39, 50), R(11, 50)])

    # ---- 例：PageRank ----
    M = sp.Matrix([[0, 0, 1], [R(1, 2), 0, 0], [R(1, 2), 1, 0]])
    pi3 = sp.Matrix([R(2, 5), R(1, 5), R(2, 5)])
    assert M * pi3 == pi3
    Mn = np.array([[0, 0, 1], [0.5, 0, 0], [0.5, 1, 0]])
    dd, nn = 0.85, 3
    G = dd * Mn + (1 - dd) / nn * np.ones((nn, nn))
    assert (G > 0).all() and np.allclose(G.sum(axis=0), 1)
    pv = np.ones(nn) / nn
    for _ in range(100):
        pv = G @ pv
    assert np.allclose(pv.round(4), [0.3878, 0.2148, 0.3974]) and np.isclose(pv.sum(), 1)
    assert np.allclose(G @ pv, pv)
    assert pv[2] > pv[0] > pv[1]

    print("verify_eigen: all checks passed")


if __name__ == "__main__":
    main()
