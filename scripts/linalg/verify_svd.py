"""验算第 9 章「奇异值分解」里的例题和正文中的数。

    .venv/bin/python scripts/linalg/verify_svd.py
"""
import numpy as np
import sympy as sp

R = sp.Rational
sq = sp.sqrt


def simp_eq(a, b):
    return sp.simplify(a - b) == sp.zeros(*a.shape)


def main():
    # ---- 例：二阶矩阵的 SVD ----
    A0 = sp.Matrix([[2, R(2, 5)], [1, R(11, 5)]])
    assert A0.T * A0 == sp.Matrix([[5, 3], [3, 5]]) and (A0.T * A0).eigenvals() == {8: 1, 2: 1}
    s1, s2 = 2 * sq(2), sq(2)
    v1, v2 = sp.Matrix([1, 1]) / sq(2), sp.Matrix([-1, 1]) / sq(2)
    assert simp_eq(A0 * v1, sp.Matrix([R(12, 5), R(16, 5)]) / sq(2))
    assert simp_eq(A0 * v2, sp.Matrix([R(-8, 5), R(6, 5)]) / sq(2))
    u1, u2 = sp.simplify(A0 * v1 / s1), sp.simplify(A0 * v2 / s2)
    assert u1 == sp.Matrix([R(3, 5), R(4, 5)]) and u2 == sp.Matrix([R(-4, 5), R(3, 5)])
    U, S, V = sp.Matrix.hstack(u1, u2), sp.diag(s1, s2), sp.Matrix.hstack(v1, v2)
    assert simp_eq(U * S * V.T, A0) and simp_eq(U.T * U, sp.eye(2)) and simp_eq(V.T * V, sp.eye(2))
    assert simp_eq(S * V.T, sp.Matrix([[2, 2], [-1, 1]]))
    assert U.det() == 1 and sp.simplify(V.det()) == 1  # 都是旋转
    assert abs(float(sp.atan2(R(4, 5), R(3, 5))) * 180 / np.pi - 53.1) < 0.05
    assert A0.trace() == R(21, 5) and A0.det() == 4 and sp.simplify(s1 * s2) == 4
    assert R(21, 5) ** 2 - 16 == R(164, 100)
    ev = sorted(float(e) for e in A0.eigenvals())
    assert abs(ev[1] - 2.74) < 0.005 and abs(ev[0] - 1.46) < 0.005
    assert abs(float(s1) - 2.83) < 0.005 and abs(float(s2) - 1.41) < 0.005

    # ---- 例：2x3 矩阵的 SVD ----
    A = sp.Matrix([[3, 2, 2], [2, 3, -2]])
    assert A * A.T == sp.Matrix([[17, 8], [8, 17]]) and (A * A.T).eigenvals() == {25: 1, 9: 1}
    ua, ub = sp.Matrix([1, 1]) / sq(2), sp.Matrix([1, -1]) / sq(2)
    va, vb = sp.simplify(A.T * ua / 5), sp.simplify(A.T * ub / 3)
    assert simp_eq(va, sp.Matrix([1, 1, 0]) / sq(2)) and simp_eq(vb, sp.Matrix([1, -1, 4]) / (3 * sq(2)))
    vc = sp.Matrix([2, -2, -1]) / 3
    assert A * vc == sp.zeros(2, 1)
    Ua, Va = sp.Matrix.hstack(ua, ub), sp.Matrix.hstack(va, vb, vc)
    Sa = sp.Matrix([[5, 0, 0], [0, 3, 0]])
    assert simp_eq(Ua * Sa * Va.T, A) and simp_eq(Va.T * Va, sp.eye(3)) and simp_eq(Ua.T * Ua, sp.eye(2))
    Vt_doc = sp.Matrix([[1 / sq(2), 1 / sq(2), 0], [1 / (3 * sq(2)), -1 / (3 * sq(2)), 4 / (3 * sq(2))], [R(2, 3), R(-2, 3), R(-1, 3)]])
    assert simp_eq(Va.T, Vt_doc)

    # ---- 例：外积展开、秩、子空间 ----
    T1, T2 = sp.simplify(5 * ua * va.T), sp.simplify(3 * ub * vb.T)
    assert T1 == R(5, 2) * sp.Matrix([[1, 1, 0], [1, 1, 0]])
    assert T2 == R(1, 2) * sp.Matrix([[1, -1, 4], [-1, 1, -4]])
    assert T1 + T2 == A and A.rank() == 2

    # ---- 第 3 节：NumPy ----
    An = np.array(A.tolist(), dtype=float)
    Un, sn, Vtn = np.linalg.svd(An)
    assert Un.shape == (2, 2) and sn.shape == (2,) and Vtn.shape == (3, 3) and np.allclose(sn, [5, 3])
    assert np.allclose(Vtn.round(4), [[-0.7071, -0.7071, 0], [-0.2357, 0.2357, -0.9428], [-0.6667, 0.6667, 0.3333]])
    Ur, sr, Vtr = np.linalg.svd(An, full_matrices=False)
    assert Vtr.shape == (2, 3) and np.allclose(Ur * sr @ Vtr, An)
    rng = np.random.default_rng(0)
    B = rng.standard_normal((6, 2)) @ rng.standard_normal((2, 5))
    Bn = B + 1e-6 * rng.standard_normal(B.shape)
    assert np.allclose(np.linalg.svd(B, compute_uv=False).round(4), [4.9601, 2.1812, 0, 0, 0])
    sb = np.linalg.svd(Bn, compute_uv=False)
    assert np.allclose(sb, [4.96005421, 2.18118080, 2.35571410e-06, 1.54865298e-06, 4.90474675e-07], rtol=1e-6)
    assert 5 < np.log10(sb[1] / sb[2]) < 6.5
    assert (np.linalg.matrix_rank(B), np.linalg.matrix_rank(Bn), np.linalg.matrix_rank(Bn, tol=1e-4)) == (2, 5, 2)

    # ---- 例：三种范数 ----
    assert np.isclose(np.linalg.norm(An, 2), 5) and np.isclose(np.linalg.norm(An, "fro"), np.sqrt(34)) and np.isclose(np.linalg.norm(An, "nuc"), 8)
    assert sum(e**2 for e in A) == 34 and abs(np.sqrt(34) - 5.83) < 0.005

    # ---- 例：病态方程组 ----
    C = sp.Matrix([[1, 1], [1, R(10001, 10000)]])
    assert C.solve(sp.Matrix([2, R(20001, 10000)])) == sp.Matrix([1, 1])
    assert C.solve(sp.Matrix([2, R(20002, 10000)])) == sp.Matrix([0, 2])
    assert C.det() == R(1, 10000)
    Cn = np.array([[1.0, 1.0], [1.0, 1.0001]])
    sc = np.linalg.svd(Cn, compute_uv=False)
    assert abs(sc[0] - 2.00005) < 1e-6 and abs(sc[1] - 5.0e-5) < 1e-8 and np.isclose(sc[0] * sc[1], 1e-4)
    kappa = np.linalg.cond(Cn)
    assert abs(kappa - 4.0e4) < 0.01e4
    rb = 1e-4 / np.linalg.norm([2, 2.0001])
    rx = np.linalg.norm([-1, 1]) / np.linalg.norm([1, 1])
    assert abs(rb - 3.5e-5) < 0.05e-5 and rx == 1 and abs(rx / rb - 2.8e4) < 0.05e4 and rx / rb <= kappa

    # ---- 例：超定方程组，伪逆 ----
    A3 = sp.Matrix([[1, 1], [0, 1], [1, 0]])
    assert A3.T * A3 == sp.Matrix([[2, 1], [1, 2]]) and (A3.T * A3).eigenvals() == {3: 1, 1: 1}
    w1, w2 = sp.Matrix([1, 1]) / sq(2), sp.Matrix([1, -1]) / sq(2)
    y1, y2 = sp.simplify(A3 * w1 / sq(3)), sp.simplify(A3 * w2)
    assert simp_eq(y1, sp.Matrix([2, 1, 1]) / sq(6)) and simp_eq(y2, sp.Matrix([0, -1, 1]) / sq(2))
    P1, P2 = sp.simplify(w1 * y1.T / sq(3)), sp.simplify(w2 * y2.T)
    assert P1 == R(1, 6) * sp.Matrix([[2, 1, 1], [2, 1, 1]]) and P2 == R(1, 2) * sp.Matrix([[0, -1, 1], [0, 1, -1]])
    A3p = R(1, 3) * sp.Matrix([[1, -1, 2], [1, 2, -1]])
    assert P1 + P2 == A3p and A3.pinv() == A3p and (A3.T * A3).inv() * A3.T == A3p
    b3 = sp.Matrix([3, 0, 0])
    x3 = A3p * b3
    res = b3 - A3 * x3
    assert x3 == sp.Matrix([1, 1]) and res == sp.Matrix([1, -1, -1]) and res.norm() == sq(3) and A3.T * res == sp.zeros(2, 1)

    # ---- 例：欠定方程组，最小范数解 ----
    Q1, Q2 = sp.simplify(va * ua.T / 5), sp.simplify(vb * ub.T / 3)
    assert Q1 == R(1, 10) * sp.Matrix([[1, 1], [1, 1], [0, 0]]) and Q2 == R(1, 18) * sp.Matrix([[1, -1], [-1, 1], [4, -4]])
    Ap = R(1, 45) * sp.Matrix([[7, 2], [2, 7], [10, -10]])
    assert Q1 + Q2 == Ap and A.pinv() == Ap and A.T * (A * A.T).inv() == Ap
    bb = sp.Matrix([5, 5])
    xp = Ap * bb
    assert xp == sp.Matrix([1, 1, 0]) and A * xp == bb
    t = sp.symbols("t", real=True)
    xt = xp + t * sp.Matrix([2, -2, -1])
    assert sp.expand(xt.dot(xt)) == 2 + 9 * t**2 and A * xt == bb
    assert xt.subs(t, 1) == sp.Matrix([3, -1, -1]) and xt.subs(t, 1).norm() == sq(11)
    assert np.allclose(np.linalg.pinv(np.array(A3.tolist(), dtype=float)) @ [3, 0, 0], [1, 1])
    assert np.allclose(np.linalg.lstsq(np.array(A3.tolist(), dtype=float), np.array([3.0, 0, 0]), rcond=None)[0], [1, 1])
    assert np.allclose(np.linalg.pinv(An) @ [5, 5], [1, 1, 0])
    # 岭回归的滤波因子 sigma/(sigma^2+lambda)
    lam = 0.3
    Af, bf = np.array(A3.tolist(), dtype=float), np.array([3.0, 0.0, 0.0])
    Uf, sf, Vtf = np.linalg.svd(Af, full_matrices=False)
    ridge = np.linalg.solve(Af.T @ Af + lam * np.eye(2), Af.T @ bf)
    assert np.allclose(ridge, Vtf.T @ (sf / (sf**2 + lam) * (Uf.T @ bf)))

    # ---- 例：最佳秩一近似 ----
    A1 = T1
    assert A - A1 == T2 and (A - A1).rank() == 1
    assert np.isclose(np.linalg.norm(np.array(T2.tolist(), dtype=float), 2), 3) and np.isclose(np.linalg.norm(np.array(T2.tolist(), dtype=float), "fro"), 3)
    assert abs(25 / 34 - 0.735) < 0.0005
    Bc = sp.Matrix([[3, 2, 2], [0, 0, 0]])
    assert (A - Bc).norm() == sq(17) and abs(float(sq(17)) - 4.12) < 0.005 and float(sq(17)) > 3
    rng = np.random.default_rng(0)
    M = rng.standard_normal((50, 40))
    Um, sm, Vtm = np.linalg.svd(M, full_matrices=False)
    k = 10
    Mk = Um[:, :k] * sm[:k] @ Vtm[:k]
    assert np.isclose(np.linalg.norm(M - Mk, 2), sm[k]) and np.isclose(sm[k], 8.542357878185664)
    assert np.isclose(np.linalg.norm(M - Mk, "fro"), np.sqrt((sm[k:] ** 2).sum())) and np.isclose(np.linalg.norm(M - Mk, "fro"), 27.9716237951984)

    # ---- 第 7 节：谱归一化 ----
    def spectral_norm(W, iters=1, seed=0):
        rng = np.random.default_rng(seed)
        u = rng.standard_normal(W.shape[0])
        for _ in range(iters):
            v = W.T @ u
            v /= np.linalg.norm(v)
            u = W @ v
            u /= np.linalg.norm(u)
        return u @ W @ v

    rng = np.random.default_rng(0)
    W = rng.standard_normal((256, 128)) / np.sqrt(128)
    assert [round(float(spectral_norm(W, it)), 4) for it in (1, 5, 20, 100, 500)] == [1.7384, 2.2694, 2.3638, 2.4046, 2.4047]
    sw = np.linalg.svd(W, compute_uv=False)
    assert np.allclose(sw[:3].round(4), [2.4047, 2.3603, 2.2993]) and abs((sw[1] / sw[0]) ** 2 - 0.96) < 0.005
    W_sn = W / spectral_norm(W, 500)
    xx, yy = rng.standard_normal(128), rng.standard_normal(128)
    assert round(float(np.linalg.norm(W_sn @ xx - W_sn @ yy) / np.linalg.norm(xx - yy)), 4) == 0.5711
    assert round(float(np.linalg.norm(W_sn, 2)), 4) == 1.0

    W2 = sp.Matrix([[1, 2], [0, 1]])
    assert W2.T * W2 == sp.Matrix([[1, 2], [2, 5]])
    assert set((W2.T * W2).eigenvals()) == {3 + 2 * sq(2), 3 - 2 * sq(2)}
    assert sp.simplify(sq(3 + 2 * sq(2)) - (1 + sq(2))) == 0
    assert abs(float(s1) - 2.828) < 0.0005 and abs(1 + np.sqrt(2) - 2.414) < 0.0005
    assert abs(float(s1 * (1 + sq(2))) - 6.83) < 0.005
    W21 = W2 * A0
    assert W21 == sp.Matrix([[4, R(24, 5)], [1, R(11, 5)]])
    G = W21.T * W21
    assert G == sp.Matrix([[17, R(107, 5)], [R(107, 5), R(697, 25)]]) and G.trace() == R(1122, 25) and G.det() == 16
    assert float(G.trace()) == 44.88 and float(G[1, 1]) == 27.88
    lmax = (44.88 + np.sqrt(44.88**2 - 64)) / 2
    assert abs(lmax - 44.52) < 0.005 and abs(np.sqrt(lmax) - 6.67) < 0.005
    assert np.isclose(np.sqrt(lmax), np.linalg.norm(np.array(W21.tolist(), dtype=float), 2))
    assert np.sqrt(lmax) < float(s1 * (1 + sq(2)))

    # ---- 第 8 节：连乘矩阵的奇异值 ----
    rng = np.random.default_rng(0)
    n, depth = 128, 20

    def product_singular_values(make_layer):
        J = np.eye(n)
        for _ in range(depth):
            J = make_layer() @ J
        s = np.linalg.svd(J, compute_uv=False)
        return f"max {s[0]:.3g}, median {np.median(s):.3g}, min {s[-1]:.3g}"

    expect = {0.8: "max 0.0779, median 1.11e-05, min 2.5e-19", 1.0: "max 6.34, median 0.000761, min 6.53e-18",
              1.2: "max 224, median 0.0333, min 6.11e-16"}
    for gain in (0.8, 1.0, 1.2):
        got = product_singular_values(lambda: gain * rng.standard_normal((n, n)) / np.sqrt(n))
        assert got == expect[gain], got
    assert product_singular_values(lambda: np.linalg.qr(rng.standard_normal((n, n)))[0]) == "max 1, median 1, min 1"
    # E||Wx||^2 = g^2 ||x||^2
    rng = np.random.default_rng(1)
    xv = rng.standard_normal(64)
    est = np.mean([np.linalg.norm(1.3 * rng.standard_normal((64, 64)) / 8 @ xv) ** 2 for _ in range(4000)])
    assert abs(est / (1.69 * xv @ xv) - 1) < 0.02

    # ---- 第 9 节：稳定秩与有效秩 ----
    def stable_rank(s):
        return (s**2).sum() / s[0] ** 2

    def effective_rank(s):
        p = s[s > 0] / s.sum()
        return np.exp(-(p * np.log(p)).sum())

    sv = np.array([10.0, 1.0, 1.0, 1.0])
    assert np.isclose(stable_rank(sv), 1.03)
    t1, t2 = -(10 / 13) * np.log(10 / 13), -(3 / 13) * np.log(1 / 13)
    assert abs(t1 - 0.202) < 0.0005 and abs(t2 - 0.592) < 0.0005 and abs(t1 + t2 - 0.794) < 0.0005
    assert abs(effective_rank(sv) - 2.21) < 0.005 and np.isclose(effective_rank(sv), np.exp(t1 + t2))
    assert np.isclose(stable_rank(np.ones(7)), 7) and np.isclose(effective_rank(np.ones(7)), 7)
    rng = np.random.default_rng(0)
    low = rng.standard_normal((64, 4)) @ rng.standard_normal((4, 64))
    mats = {"low-rank": low, "low-rank + noise": low + 0.01 * rng.standard_normal((64, 64)),
            "gaussian": rng.standard_normal((64, 64))}
    expect = {"low-rank": (4, 2.14, 3.89), "low-rank + noise": (64, 2.14, 4.37), "gaussian": (64, 16.42, 51.31)}
    for name, Mx in mats.items():
        s = np.linalg.svd(Mx, compute_uv=False)
        got = (int(np.linalg.matrix_rank(Mx)), round(float(stable_rank(s)), 2), round(float(effective_rank(s)), 2))
        assert got == expect[name], (name, got)

    print("verify_svd: all checks passed")


if __name__ == "__main__":
    main()
