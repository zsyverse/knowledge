"""验算第 3 章「线性方程组、消元与逆矩阵」例题里的每个数。

    .venv/bin/python scripts/linalg/verify_linear-systems.py
"""
import numpy as np
import sympy as sp

M = sp.Matrix
R = sp.Rational


def main():
    # 第 1 节：2x - y = 1, x + y = 5
    A, b = M([[2, -1], [1, 1]]), M([1, 5])
    assert A.solve(b) == M([2, 3])
    assert 2 * A[:, 0] + 3 * A[:, 1] == b

    # 例：三元方程组的消元与回代
    Ab = M([[1, 2, -1, 3], [2, 5, 1, 14], [-1, 1, 3, 7]])
    s1 = Ab.copy()
    s1[1, :] = s1[1, :] - 2 * s1[0, :]
    s1[2, :] = s1[2, :] + s1[0, :]
    assert s1 == M([[1, 2, -1, 3], [0, 1, 3, 8], [0, 3, 2, 10]])
    s2 = s1.copy()
    s2[2, :] = s2[2, :] - 3 * s2[1, :]
    assert s2 == M([[1, 2, -1, 3], [0, 1, 3, 8], [0, 0, -7, -14]])
    assert [s2[i, i] for i in range(3)] == [1, 1, -7]                  # 主元
    A3, b3 = Ab[:, :3], Ab[:, 3]
    assert A3.solve(b3) == M([1, 2, 2])
    # 行最简形的中间步骤
    r1 = s2.copy()
    r1[2, :] = r1[2, :] / -7
    assert r1 == M([[1, 2, -1, 3], [0, 1, 3, 8], [0, 0, 1, 2]])
    r2 = r1.copy()
    r2[1, :] = r2[1, :] - 3 * r2[2, :]
    r2[0, :] = r2[0, :] + r2[2, :]
    assert r2 == M([[1, 2, 0, 5], [0, 1, 0, 2], [0, 0, 1, 2]])
    r3 = r2.copy()
    r3[0, :] = r3[0, :] - 2 * r3[1, :]
    assert r3 == M([[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 2]])
    assert Ab.rref() == (r3, (0, 1, 2))

    # 第 3 节插图的三种情形
    assert M([[1, 1], [1, -1]]).solve(M([3, 1])) == M([2, 1])
    assert M([[1, 1, 3], [1, 1, 1]]).rref()[1] == (0, 2)               # 出现 0 = c，无解
    assert M([[1, 1, 3], [2, 2, 6]]).rank() == 1                       # 两个方程重合

    # 例：含参数的方程组
    a, bb, t = sp.symbols("a b t")
    P = M([[1, 2, 1, 1], [2, 5, 3, 3], [3, 7, a, bb]])
    p1 = P.copy()
    p1[1, :] = p1[1, :] - 2 * p1[0, :]
    p1[2, :] = p1[2, :] - 3 * p1[0, :]
    assert p1 == M([[1, 2, 1, 1], [0, 1, 1, 1], [0, 1, a - 3, bb - 3]])
    p2 = p1.copy()
    p2[2, :] = p2[2, :] - p2[1, :]
    assert p2 == M([[1, 2, 1, 1], [0, 1, 1, 1], [0, 0, a - 4, bb - 4]])
    x, y, z = sp.symbols("x y z")
    sol = sp.solve([x + 2 * y + z - 1, 2 * x + 5 * y + 3 * z - 3, 3 * x + 7 * y + a * z - bb], [x, y, z], dict=True)[0]
    zf = (bb - 4) / (a - 4)
    assert sp.simplify(sol[z] - zf) == 0 and sp.simplify(sol[y] - (1 - zf)) == 0 and sp.simplify(sol[x] - (-1 + zf)) == 0
    # a = 4, b != 4：无解（系数矩阵秩 2，增广矩阵秩 3）
    assert P.subs({a: 4, bb: 7})[:, :3].rank() == 2 and P.subs({a: 4, bb: 7}).rank() == 3
    # a = 4, b = 4：无穷多解
    P44 = P.subs({a: 4, bb: 4})
    assert P44.rank() == 2
    xs = M([-1, 1, 0]) + t * M([1, -1, 1])
    assert sp.simplify(P44[:, :3] * xs - P44[:, 3]) == sp.zeros(3, 1)
    assert sp.expand(3 * (-1 + t) + 7 * (1 - t) + 4 * t) == 4

    # 逆矩阵：二阶公式
    assert M([[2, 1], [5, 3]]).inv() == M([[3, -1], [-5, 2]]) and M([[2, 1], [5, 3]]).det() == 1
    aa, b_, c_, d_ = sp.symbols("a b c d")
    G = M([[aa, b_], [c_, d_]])
    assert sp.simplify(G.inv() - M([[d_, -b_], [-c_, aa]]) / (aa * d_ - b_ * c_)) == sp.zeros(2, 2)

    # 例：Gauss–Jordan 消元求逆
    A = M([[1, 1, 0], [1, 2, 1], [0, 1, 2]])
    g = sp.Matrix.hstack(A, sp.eye(3))
    g[1, :] = g[1, :] - g[0, :]
    g[2, :] = g[2, :] - g[1, :]
    assert g == M([[1, 1, 0, 1, 0, 0], [0, 1, 1, -1, 1, 0], [0, 0, 1, 1, -1, 1]])
    g[1, :] = g[1, :] - g[2, :]
    assert g == M([[1, 1, 0, 1, 0, 0], [0, 1, 0, -2, 2, -1], [0, 0, 1, 1, -1, 1]])
    g[0, :] = g[0, :] - g[1, :]
    Ainv = M([[3, -2, 1], [-2, 2, -1], [1, -1, 1]])
    assert g == sp.Matrix.hstack(sp.eye(3), Ainv)
    assert A.inv() == Ainv and A * Ainv == sp.eye(3)
    assert list(A[0, :] * Ainv) == [1, 0, 0]

    # 逆的性质
    B = M([[2, 1, 0], [0, 1, 3], [1, 0, 1]])
    assert (A * B).inv() == B.inv() * A.inv() and (A.T).inv() == A.inv().T
    assert sp.diag(2, 4, 5).inv() == sp.diag(R(1, 2), R(1, 4), R(1, 5))
    assert (A + B).inv() != A.inv() + B.inv()

    # 例：LU 分解并解两个右端
    A = M([[1, 2, -1], [2, 5, 1], [-1, 1, 3]])
    L = M([[1, 0, 0], [2, 1, 0], [-1, 3, 1]])
    U = M([[1, 2, -1], [0, 1, 3], [0, 0, -7]])
    assert L * U == A
    assert -M([[1, 2, -1]]) + 3 * M([[0, 1, 3]]) + M([[0, 0, -7]]) == A[2, :]
    Ls, Us, _ = A.LUdecomposition()
    assert Ls == L and Us == U
    # 初等矩阵：E32 E31 E21 A = U，L = E21^{-1} E31^{-1} E32^{-1}
    E21, E31, E32 = sp.eye(3), sp.eye(3), sp.eye(3)
    E21[1, 0], E31[2, 0], E32[2, 1] = -2, 1, -3
    assert E32 * E31 * E21 * A == U and E21.inv() * E31.inv() * E32.inv() == L
    for rhs, yy, xx in ((M([3, 14, 7]), M([3, 8, -14]), M([1, 2, 2])), (M([-1, 0, 0]), M([-1, 2, -7]), M([2, -1, 1]))):
        assert L.solve(rhs) == yy and U.solve(yy) == xx and A * xx == rhs
    assert A.det() == 1 * 1 * (-7)                                     # 行列式 = 主元之积
    # 小主元：精确解约为 (1, 1)
    eps = R(1, 10**20)
    sol = M([[eps, 1], [1, 1]]).solve(M([1, 2]))
    assert abs(float(sol[0]) - 1) < 1e-15 and abs(float(sol[1]) - 1) < 1e-15

    # 运算量：求逆约为一次 LU 分解的 3 倍（2n^3 对 2n^3/3）
    assert R(2) / R(2, 3) == 3

    # 例：解正规方程拟合直线
    X = M([[1, 0], [1, 1], [1, 2], [1, 3]])
    yv = M([1, 2, 2, 4])
    assert X.T * X == M([[4, 6], [6, 14]]) and X.T * yv == M([9, 18])
    N = sp.Matrix.hstack(X.T * X, X.T * yv)
    N[1, :] = N[1, :] - R(3, 2) * N[0, :]
    assert N == M([[4, 6, 9], [0, 5, R(9, 2)]])
    w = (X.T * X).solve(X.T * yv)
    assert w == M([R(9, 10), R(9, 10)])
    pred = X * w
    assert pred == M([R(9, 10), R(18, 10), R(27, 10), R(36, 10)])
    res = yv - pred
    assert res == M([R(1, 10), R(2, 10), R(-7, 10), R(4, 10)]) and sum(res) == 0 and X.T * res == sp.zeros(2, 1)

    # 例：两个完全相同的特征（岭回归）
    X = M([[1, 1], [2, 2]])
    yv = M([2, 4])
    assert X.T * X == M([[5, 5], [5, 5]]) and X.T * yv == M([10, 10]) and (X.T * X).det() == 0
    lam = sp.symbols("lambda", positive=True)
    wr = (X.T * X + lam * sp.eye(2)).solve(X.T * yv)
    assert sp.simplify(wr[0] - 10 / (10 + lam)) == 0 and sp.simplify(wr[1] - 10 / (10 + lam)) == 0
    assert X.T * X + sp.eye(2) == M([[6, 5], [5, 6]]) and wr.subs(lam, 1) == M([R(10, 11), R(10, 11)])
    assert abs(float(R(10, 11)) - 0.909) < 5e-4
    assert sp.limit(wr[0], lam, 0) == 1
    # w1 + w2 = 2 上范数最小的是 (1, 1)
    s = sp.symbols("s", real=True)
    assert sp.solve(sp.diff(s**2 + (2 - s) ** 2, s), s) == [1]
    # 一般情形：d > n 时 X^T X 奇异，加 λI 后可逆
    rng = np.random.default_rng(0)
    Xr = rng.standard_normal((3, 6))
    assert np.linalg.matrix_rank(Xr.T @ Xr) == 3
    assert np.linalg.eigvalsh(Xr.T @ Xr + 0.1 * np.eye(6)).min() >= 0.1 - 1e-9

    # 例：一步牛顿法
    w1, w2 = sp.symbols("w1 w2")
    f = w1**2 + w1 * w2 + 2 * w2**2 - 4 * w1 - 9 * w2
    grad = M([sp.diff(f, w1), sp.diff(f, w2)])
    H = sp.hessian(f, (w1, w2))
    assert grad == M([2 * w1 + w2 - 4, w1 + 4 * w2 - 9]) and H == M([[2, 1], [1, 4]])
    g0 = grad.subs({w1: 0, w2: 0})
    assert g0 == M([-4, -9])
    Nw = sp.Matrix.hstack(H, -g0)
    Nw[1, :] = Nw[1, :] - R(1, 2) * Nw[0, :]
    assert Nw == M([[2, 1, 4], [0, R(7, 2), 7]])
    step = H.solve(-g0)
    assert step == M([1, 2]) and grad.subs({w1: 1, w2: 2}) == sp.zeros(2, 1)
    wk = np.zeros(2)
    gnum = lambda v: np.array([2 * v[0] + v[1] - 4, v[0] + 4 * v[1] - 9])
    hist = {}
    for k in range(1, 11):
        wk = wk - 0.2 * gnum(wk)
        hist[k] = wk.copy()
    assert np.allclose(hist[1], [0.8, 1.8]) and np.allclose(hist[10].round(4), [0.9968, 2.0013])

    # 规模估算
    for N, n2, nbytes, ops in ((1e3, 1e6, 4e6, 3.3e8), (1e6, 1e12, 4e12, 3.3e17), (7e9, 4.9e19, 1.96e20, 1.1e29)):
        assert np.isclose(N * N, n2) and np.isclose(N * N * 4, nbytes) and np.isclose(N**3 / 3, ops, rtol=0.05)
    assert 4e6 / 1e6 == 4 and 4e12 / 1e12 == 4 and np.isclose(1.96e20 / 1e18, 196)    # MB、TB、EB
    assert np.isclose(1e18 / 3 / 1e13, 3.3e4, rtol=0.02) and 9 < 1e18 / 3 / 1e13 / 3600 < 10
    secs = (7e9) ** 3 / 3 / 1e18
    assert np.isclose(secs, 1.1e11, rtol=0.05) and abs(secs / (365 * 24 * 3600) - 3600) < 50

    print("verify_linear-systems: all checks passed")


if __name__ == "__main__":
    main()
