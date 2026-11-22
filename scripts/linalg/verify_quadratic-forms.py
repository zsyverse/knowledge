"""验算第 8 章「对称矩阵、二次型与正定性」里的例题和正文中的数。

    .venv/bin/python scripts/linalg/verify_quadratic-forms.py
"""
import numpy as np
import sympy as sp

R = sp.Rational
lam = sp.symbols("lambda")
x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)


def is_pd(A):
    try:
        np.linalg.cholesky(A)
        return True
    except np.linalg.LinAlgError:
        return False


def quad(A, v):
    return sp.expand((v.T * A * v)[0])


def main():
    v2, v3 = sp.Matrix([x1, x2]), sp.Matrix([x1, x2, x3])

    # ---- 第 1 节：二次型与矩阵 ----
    assert quad(sp.Matrix([[1, 4], [0, 2]]), v2) == quad(sp.Matrix([[1, 2], [2, 2]]), v2) == x1**2 + 4 * x1 * x2 + 2 * x2**2
    A1 = sp.Matrix([[1, 2, 0], [2, 2, -1], [0, -1, 3]])
    assert quad(A1, v3) == x1**2 + 2 * x2**2 + 3 * x3**2 + 4 * x1 * x2 - 2 * x2 * x3
    E = sp.Matrix([[5, 3], [3, 5]])
    assert quad(E, v2) == 5 * x1**2 + 6 * x1 * x2 + 5 * x2**2
    assert E.eigenvals() == {8: 1, 2: 1} and E.trace() == 10 and E.det() == 16
    q1, q2 = sp.Matrix([1, 1]) / sp.sqrt(2), sp.Matrix([1, -1]) / sp.sqrt(2)
    assert E * q1 == 8 * q1 and E * q2 == 2 * q2
    # 半轴端点落在椭圆上
    assert quad(E, 1 * q1) == 8 and quad(E, 2 * q2) == 8

    # ---- 第 2 节：判断正定 ----
    assert sp.Matrix([[1, 2], [2, 1]]).eigenvals() == {3: 1, -1: 1}
    Z = sp.Matrix([[0, 0], [0, -1]])
    assert Z[0, 0] == 0 and Z.det() == 0 and Z.is_negative_semidefinite and not Z.is_positive_semidefinite
    T = sp.Matrix([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])
    assert [T[:k, :k].det() for k in (1, 2, 3)] == [2, 3, 4]
    r2 = T[1, :] + R(1, 2) * T[0, :]
    assert r2 == sp.Matrix([[0, R(3, 2), -1]])
    r3 = T[2, :] + R(2, 3) * r2
    assert r3 == sp.Matrix([[0, 0, R(4, 3)]])
    assert sp.expand((lam * sp.eye(3) - T).det() - (lam - 2) * ((lam - 2) ** 2 - 2)) == 0
    assert set(T.eigenvals()) == {2 - sp.sqrt(2), 2, 2 + sp.sqrt(2)}
    assert quad(T, v3) == sp.expand(x1**2 + (x1 - x2) ** 2 + (x2 - x3) ** 2 + x3**2)
    Bm = sp.Matrix([[1, 0, 0], [-1, 1, 0], [0, -1, 1], [0, 0, 1]])
    assert Bm.T * Bm == T and Bm.rank() == 3

    t = sp.symbols("t", real=True)
    At = sp.Matrix([[1, t, 0], [t, 2, 1], [0, 1, 1]])
    assert At[:2, :2].det() == 2 - t**2 and sp.expand(At.det()) == 1 - t**2
    assert At.subs(t, R(1, 2)).is_positive_definite
    assert At.subs(t, 1).is_positive_semidefinite and not At.subs(t, 1).is_positive_definite
    assert At.subs(t, R(3, 2)).is_indefinite and At.subs(t, R(6, 5)).is_indefinite

    # ---- 第 3 节：Cholesky ----
    C = sp.Matrix([[4, 2, 2], [2, 5, 3], [2, 3, 6]])
    L = sp.Matrix([[2, 0, 0], [1, 2, 0], [1, 1, 2]])
    assert L * L.T == C and C.cholesky() == L and C.det() == 64
    b = sp.Matrix([2, 5, 7])
    y = L.solve(b)
    x = L.T.solve(y)
    assert y == sp.Matrix([1, 2, 2]) and x == sp.Matrix([R(-1, 4), R(1, 2), 1]) and C * x == b
    Cn = np.array(C.tolist(), dtype=float)
    Ln = np.linalg.cholesky(Cn)
    assert np.allclose(Ln, np.array(L.tolist(), dtype=float))
    assert np.isclose(2 * np.log(np.diag(Ln)).sum(), 4.1588830833596715) and np.isclose(np.linalg.slogdet(Cn)[1], np.log(64))
    assert is_pd(Cn) and not is_pd(np.array([[1.0, 2.0], [2.0, 1.0]])) and not is_pd(np.array([[1.0, 1.0], [1.0, 1.0]]))

    # ---- 第 4 节：标准形与 Rayleigh 商 ----
    S = sp.Matrix([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
    assert quad(S, v3) == 2 * x1**2 + 2 * x2**2 + 2 * x3**2 + 2 * x1 * x2 + 2 * x1 * x3 + 2 * x2 * x3
    assert quad(S, v3) == sp.expand((x1 + x2 + x3) ** 2 + x1**2 + x2**2 + x3**2)
    Q = sp.Matrix.hstack(sp.Matrix([1, 1, 1]) / sp.sqrt(3), sp.Matrix([1, -1, 0]) / sp.sqrt(2), sp.Matrix([1, 1, -2]) / sp.sqrt(6))
    assert sp.simplify(Q.T * Q) == sp.eye(3) and sp.simplify(Q.T * S * Q) == sp.diag(4, 1, 1)
    ray = lambda v: R((sp.Matrix(v).T * E * sp.Matrix(v))[0], sp.Matrix(v).dot(sp.Matrix(v)))
    assert ray([1, 0]) == 5 and ray([2, 1]) == R(37, 5) and ray([1, 1]) == 8 and ray([1, -1]) == 2
    assert float(R(37, 5)) == 7.4

    # ---- 第 5 节：Hessian ----
    f = x1**3 + x2**3 - 3 * x1 * x2
    grad = [sp.diff(f, s) for s in (x1, x2)]
    assert grad == [3 * x1**2 - 3 * x2, 3 * x2**2 - 3 * x1]
    sols = sp.solve(grad, [x1, x2], dict=True)
    assert {(s[x1], s[x2]) for s in sols} == {(0, 0), (1, 1)}
    Hf = sp.hessian(f, (x1, x2))
    assert Hf == sp.Matrix([[6 * x1, -3], [-3, 6 * x2]])
    H0, H1 = Hf.subs({x1: 0, x2: 0}), Hf.subs({x1: 1, x2: 1})
    assert H0.eigenvals() == {3: 1, -3: 1} and H1.eigenvals() == {3: 1, 9: 1}
    assert H0 * sp.Matrix([1, -1]) == 3 * sp.Matrix([1, -1]) and H0 * sp.Matrix([1, 1]) == -3 * sp.Matrix([1, 1])
    assert H1[0, 0] == 6 and H1.det() == 27 and f.subs({x1: 1, x2: 1}) == -1

    # ---- 第 6 节：条件数与收敛速度 ----
    def gd_steps(H, x0, eta, tol=1e-3):
        xv, k = x0.copy(), 0
        while np.linalg.norm(xv) > tol * np.linalg.norm(x0):
            xv = xv - eta * (H @ xv)
            k += 1
        return k

    got = [gd_steps(np.diag([m, 1.0]), np.array([1.0, 1.0]), 2 / (m + 1)) for m in (1.0, 20.0, 100.0, 1000.0)]
    assert got == [1, 70, 346, 3454]
    for kap, st in zip((20, 100, 1000), got[1:]):
        assert abs(st - kap / 2 * np.log(1e3)) / st < 0.02
    assert abs(np.log(1e3) / 2 - 3.45) < 0.005
    assert R(2, 20) == R(1, 10) and abs(2 / 21 - 0.095) < 5e-4 and abs(19 / 21 - 0.905) < 5e-4
    k3 = np.log(1e-3) / np.log(19 / 21)
    assert abs(k3 - 69.02) < 0.005 and int(np.ceil(k3)) == 70
    k4 = np.log(1e-3) / np.log(0.95)
    assert abs(k4 - 134.7) < 0.05 and int(np.ceil(k4)) == 135
    assert abs(1 - 0.05 * 20) < 1e-12

    # ---- 第 7 节：协方差与 Gram 矩阵 ----
    X = sp.Matrix([[2, 0], [0, 1], [-2, -1]])
    assert sum(X[:, 0]) == 0 and sum(X[:, 1]) == 0
    assert X.T * X == sp.Matrix([[8, 2], [2, 2]])
    Sig = X.T * X / 3
    assert Sig[0, 0] == R(8, 3) and Sig.det() == R(4, 3) and Sig.is_positive_definite
    v = sp.Matrix([1, -1]) / sp.sqrt(2)
    assert sp.simplify((v.T * Sig * v)[0]) == 1
    assert sp.simplify(X * v - sp.Matrix([2, -1, -1]) / sp.sqrt(2)) == sp.zeros(3, 1)
    assert sp.simplify((X * v).dot(X * v) / 3) == 1
    Xp = sp.Matrix([[1, 2], [0, 0], [-1, -2]])
    assert Xp.T * Xp == sp.Matrix([[2, 4], [4, 8]]) and (Xp.T * Xp).eigenvals() == {10: 1, 0: 1}
    assert Xp * sp.Matrix([2, -1]) == sp.zeros(3, 1)

    rng = np.random.default_rng(0)
    Xn = rng.standard_normal((3, 5))
    Xn = Xn - Xn.mean(axis=0)
    Sn = Xn.T @ Xn / len(Xn)
    ev = np.linalg.eigvalsh(Sn)
    assert np.allclose(ev.round(4), [0, 0, 0, 0.5068, 2.482])
    assert np.linalg.matrix_rank(Sn) == 2
    assert not is_pd(Sn) and is_pd(Sn + 1e-6 * np.eye(5))
    evK = np.linalg.eigvalsh(Xn @ Xn.T)
    assert np.allclose(evK.round(4), [0, 1.5204, 7.4461]) and np.allclose(evK[1:], 3 * ev[3:])

    # ---- 第 8 节：高斯采样 ----
    Sg = sp.Matrix([[4, 2], [2, 3]])
    Lg = sp.Matrix([[2, 0], [1, sp.sqrt(2)]])
    assert Sg.cholesky() == Lg and Lg * Lg.T == Sg
    rng = np.random.default_rng(0)
    mu = np.array([1.0, -1.0])
    Lg_n = np.linalg.cholesky(np.array([[4.0, 2.0], [2.0, 3.0]]))
    z = rng.standard_normal((100_000, 2))
    xs = mu + z @ Lg_n.T
    assert np.allclose(xs.mean(axis=0).round(2), [1, -1])
    assert np.allclose(np.cov(xs, rowvar=False).round(2), [[4.02, 1.99], [1.99, 2.99]])

    # ---- 第 9 节：鞍点实验、预条件 ----
    rng = np.random.default_rng(0)
    frac = {}
    for n in (1, 2, 3, 4, 6):
        hits = 0
        for _ in range(20000):
            G = rng.standard_normal((n, n))
            hits += np.linalg.eigvalsh((G + G.T) / 2).min() > 0
        frac[n] = hits / 20000
    assert frac == {1: 0.498, 2: 0.145, 3: 0.02715, 4: 0.0024, 6: 0.0}, frac

    H = sp.Matrix([[100, 5], [5, 1]])
    assert H.trace() == 101 and H.det() == 75 and 101**2 - 300 == 9901
    lmax, lmin = (101 + sp.sqrt(9901)) / 2, (101 - sp.sqrt(9901)) / 2
    assert set(H.eigenvals()) == {lmax, lmin}
    assert abs(float(lmax) - 100.25) < 0.005 and abs(float(lmin) - 0.748) < 0.0005 and abs(float(lmax / lmin) - 134) < 0.05
    D = sp.diag(R(1, 10), 1)
    Hs = D * H * D
    assert Hs == sp.Matrix([[1, R(1, 2)], [R(1, 2), 1]]) and Hs.eigenvals() == {R(3, 2): 1, R(1, 2): 1}
    assert H.inv() == R(1, 75) * sp.Matrix([[1, -5], [-5, 100]])
    xN = H.inv() * sp.Matrix([1, 1])
    assert xN == sp.Matrix([R(-4, 75), R(95, 75)])
    assert abs(float(xN[0]) + 0.053) < 5e-4 and abs(float(xN[1]) - 1.267) < 5e-4

    Hn = np.array([[100.0, 5.0], [5.0, 1.0]])
    bn = np.array([1.0, 1.0])
    x_star = np.linalg.solve(Hn, bn)

    def run(P_inv, tol=1e-6):
        w = np.linalg.eigvals(P_inv @ Hn).real
        eta = 2 / (w.max() + w.min())
        xv, k = np.zeros(2), 0
        while np.linalg.norm(xv - x_star) > tol * np.linalg.norm(x_star):
            xv = xv - eta * P_inv @ (Hn @ xv - bn)
            k += 1
        return f"kappa={w.max() / w.min():.1f}, steps={k}"

    assert run(np.eye(2)) == "kappa=134.0, steps=926"
    assert run(np.diag(1 / np.diag(Hn))) == "kappa=3.0, steps=19"
    assert run(np.linalg.inv(Hn)) == "kappa=1.0, steps=1"

    print("verify_quadratic-forms: all checks passed")


if __name__ == "__main__":
    main()
