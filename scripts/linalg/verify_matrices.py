"""验算第 2 章「矩阵与线性变换」例题里的每个数。

    .venv/bin/python scripts/linalg/verify_matrices.py
"""
import numpy as np
import sympy as sp

M = sp.Matrix


def main():
    # 二维基本变换：矩阵的列是 e1、e2 的像
    th, a, b, k = sp.symbols("theta a b k", real=True)
    e1, e2 = M([1, 0]), M([0, 1])
    table = [
        (M([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]]), M([sp.cos(th), sp.sin(th)]), M([-sp.sin(th), sp.cos(th)])),
        (M([[a, 0], [0, b]]), M([a, 0]), M([0, b])),
        (M([[1, k], [0, 1]]), M([1, 0]), M([k, 1])),
        (M([[1, 0], [0, 0]]), M([1, 0]), M([0, 0])),
        (M([[0, 1], [1, 0]]), M([0, 1]), M([1, 0])),
    ]
    for A, i1, i2 in table:
        assert A * e1 == i1 and A * e2 == i2

    # 例：由两个向量的像求矩阵
    A = M([[2, 1], [2, -1]])
    assert A * M([1, 1]) == M([3, 1]) and A * M([1, -1]) == M([1, 3])
    assert A[:, 0] == (M([3, 1]) + M([1, 3])) / 2 and A[:, 1] == (M([3, 1]) - M([1, 3])) / 2
    assert A * M([3, 2]) == M([8, 4])
    assert M([[3, 1], [1, 3]]) * M([[1, 1], [1, -1]]).inv() == A       # A [v1 v2] = [w1 w2]

    # 矩阵乘向量的两种看法
    A = M([[1, 2], [3, 4], [5, 6]])
    x = M([2, -1])
    assert A * x == M([0, 2, 4])
    assert M([A[i, :].dot(x) for i in range(3)]) == M([0, 2, 4])
    assert 2 * A[:, 0] - A[:, 1] == M([0, 2, 4])

    # 例：用四种看法算同一个乘积
    A, B = M([[1, 2], [3, 4]]), M([[0, 1], [2, 3]])
    C = M([[4, 7], [8, 15]])
    assert A * B == C
    assert sp.Matrix.hstack(A * B[:, 0], A * B[:, 1]) == C
    assert A * B[:, 0] == M([4, 8]) and A * B[:, 1] == M([7, 15])
    assert sp.Matrix.vstack(A[0, :] * B, A[1, :] * B) == C
    assert A[:, 0] * B[0, :] == M([[0, 1], [0, 3]]) and A[:, 1] * B[1, :] == M([[4, 6], [8, 12]])
    assert A[:, 0] * B[0, :] + A[:, 1] * B[1, :] == C
    assert B * A == M([[3, 4], [11, 16]]) and A * B != B * A

    # 例：复合变换的顺序
    Rm, S = M([[0, -1], [1, 0]]), M([[1, 1], [0, 1]])
    assert S * Rm == M([[1, -1], [1, 0]]) and Rm * S == M([[0, -1], [1, 1]])
    assert S * Rm * e1 == M([1, 1]) and Rm * S * e1 == M([0, 1])
    assert Rm * e1 == M([0, 1]) and S * M([0, 1]) == M([1, 1])

    # 易错点里的反例
    A0, B0 = M([[1, 0], [0, 0]]), M([[0, 0], [0, 1]])
    assert A0 * B0 == sp.zeros(2, 2) and A0 != sp.zeros(2, 2) and B0 != sp.zeros(2, 2)

    # 转置：(AB)^T = B^T A^T，(Ax)^T y = x^T (A^T y)
    A = M(2, 3, sp.symbols("a0:6"))
    B = M(3, 2, sp.symbols("b0:6"))
    assert (A * B).T == B.T * A.T
    x, y = M(sp.symbols("x0:3")), M(sp.symbols("y0:2"))
    assert sp.expand(((A * x).T * y)[0] - (x.T * (A.T * y))[0]) == 0
    assert (A.T * A).T == A.T * A                                       # A^T A 对称
    # 置换阵 P^T P = I；上三角之积仍为上三角
    P = M([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    assert P.T * P == sp.eye(3)
    U1, U2 = M([[1, 2], [0, 3]]), M([[4, 5], [0, 6]])
    assert (U1 * U2).is_upper

    # 例：内积与外积
    u, v = M([1, 2, 3]), M([4, 5])
    O = u * v.T
    assert O == M([[4, 5], [8, 10], [12, 15]]) and O.rank() == 1
    assert v.dot(M([1, 1])) == 9 and O * M([1, 1]) == M([9, 18, 27]) == 9 * u
    assert u.dot(u) == 14 and (u * u.T).shape == (3, 3) and (u * u.T).is_symmetric()

    # 例：手算一层全连接层
    W, b_ = M([[1, 0, -1], [2, 1, 0]]), M([1, -1])
    X = M([[1, 2, 3], [0, 1, 0]])
    assert W * X[0, :].T + b_ == M([-1, 3]) and W * X[1, :].T + b_ == M([1, 0])
    Y = X * W.T + sp.ones(2, 1) * b_.T
    assert Y == M([[-1, 3], [1, 0]])
    assert Y.applyfunc(lambda t: sp.Max(t, 0)) == M([[0, 3], [1, 0]])

    # 例：追踪 shape 并计算参数量
    assert 784 * 256 + 256 == 200960 and 256 * 10 + 10 == 2570 and 200960 + 2570 == 203530
    assert 4096 * 16384 == 67108864
    total = 2 * 67108864 + 16384 + 4096
    assert total == 134238208 and abs(total / 1e8 - 1.34) < 0.005
    assert abs((16384 + 4096) / total * 100 - 0.015) < 5e-4            # 偏置占比（百分数）

    # 例：把两层合并成一层
    W1, b1, W2, b2 = M([[1, 2], [0, 1]]), M([1, 0]), M([[1, -1]]), M([2])
    assert W2 * W1 == M([[1, 1]]) and W2 * b1 + b2 == M([3])
    x = M([1, 1])
    assert W1 * x + b1 == M([4, 1]) and W2 * (W1 * x + b1) + b2 == M([5])
    assert (W2 * W1) * x + (W2 * b1 + b2) == M([5])
    relu = lambda t: max(t, 0)
    assert relu(1) + relu(-1) == 1 and relu(1 + (-1)) == 0
    assert (64 * 16 + 64) + (64 * 64 + 64) + (4 * 64 + 4) == 5508 and 4 * 16 + 4 == 68
    # 一般情形：W2 (W1 x + b1) + b2 = (W2 W1) x + (W2 b1 + b2)
    rng = np.random.default_rng(0)
    A1, c1, A2, c2 = rng.standard_normal((7, 5)), rng.standard_normal(7), rng.standard_normal((3, 7)), rng.standard_normal(3)
    xx = rng.standard_normal(5)
    assert np.allclose(A2 @ (A1 @ xx + c1) + c2, (A2 @ A1) @ xx + (A2 @ c1 + c2))

    # 例：三个 token 的查表
    E = M([[1, 0], [0, 1], [2, 2], [-1, 3]])
    ids = [2, 0, 2]
    O = sp.zeros(3, 4)
    for r, i in enumerate(ids):
        O[r, i] = 1
    assert O == M([[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]])
    assert O * E == M([[2, 2], [1, 0], [2, 2]]) == sp.Matrix.vstack(*[E[i, :] for i in ids])

    # 例：3 个 token 的注意力分数矩阵
    Q, K = M([[1, 0], [1, 1], [0, 2]]), M([[1, 2], [0, 1], [2, 0]])
    S = Q * K.T
    assert S == M([[1, 0, 2], [3, 1, 2], [4, 2, 0]])
    assert all(S[i, j] == Q[i, :].dot(K[j, :]) for i in range(3) for j in range(3))
    assert [max(range(3), key=lambda j: S[i, j]) for i in range(3)] == [2, 0, 0]   # 第 3、1、1 个键
    # Gram 矩阵：对称，对角元为范数平方
    G = Q * Q.T
    assert G.is_symmetric() and [G[i, i] for i in range(3)] == [Q[i, :].dot(Q[i, :]) for i in range(3)]

    print("verify_matrices: all checks passed")


if __name__ == "__main__":
    main()
