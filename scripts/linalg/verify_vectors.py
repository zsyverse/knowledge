"""验算第 1 章「向量、内积与范数」例题里的每个数。

    .venv/bin/python scripts/linalg/verify_vectors.py
"""
import itertools

import numpy as np
import sympy as sp

R = sp.Rational


def close(a, b, tol=1e-9):
    return np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol, rtol=0)


def main():
    # 例：把一个向量写成线性组合  b = 2 v1 + v2
    v1, v2, b = sp.Matrix([1, 2]), sp.Matrix([3, 1]), sp.Matrix([5, 5])
    c = sp.Matrix.hstack(v1, v2).solve(b)
    assert c == sp.Matrix([2, 1])
    assert 2 * v1 + v2 == b

    # 例：求两个向量的夹角
    x, y = sp.Matrix([1, 2, 2]), sp.Matrix([3, 0, 4])
    assert x.dot(y) == 11 and x.norm() == 3 and y.norm() == 5
    cos = x.dot(y) / (x.norm() * y.norm())
    assert cos == R(11, 15)
    assert abs(float(sp.deg(sp.acos(cos))) - 42.83) < 0.005
    assert abs(float(cos) - 0.733) < 5e-4

    # 例：Cauchy–Schwarz 求最大值
    a = sp.Matrix([1, 2, 3])
    xs = a / a.norm()
    assert sp.simplify(a.dot(xs) - sp.sqrt(14)) == 0 and xs.norm() == 1
    assert abs(float(sp.sqrt(14)) - 3.742) < 5e-4
    rng = np.random.default_rng(0)
    U = rng.standard_normal((20000, 3))
    U /= np.linalg.norm(U, axis=1, keepdims=True)
    assert (U @ np.array([1.0, 2.0, 3.0])).max() <= np.sqrt(14) + 1e-12

    # 例：三种范数与归一化
    x = sp.Matrix([3, -4, 0, 12])
    n1, n2, ninf = sum(abs(t) for t in x), x.norm(), max(abs(t) for t in x)
    assert (n1, n2, ninf) == (19, 13, 12)
    assert ninf <= n2 <= n1 <= sp.sqrt(4) * n2 == 26
    assert (x / n2).norm() == 1
    # 范数之间的不等式链（随机检验）
    for _ in range(200):
        n = int(rng.integers(1, 9))
        v = rng.standard_normal(n)
        l1, l2, li = np.abs(v).sum(), np.linalg.norm(v), np.abs(v).max()
        assert li <= l2 + 1e-12 and l2 <= l1 + 1e-12 and l1 <= np.sqrt(n) * l2 + 1e-12 and np.sqrt(n) * l2 <= n * li + 1e-12

    # 例：向全 1 向量投影
    x, one = sp.Matrix([1, 2, 3]), sp.ones(3, 1)
    c = one.dot(x) / one.dot(one)
    p = c * one
    e = x - p
    assert c == 2 and p == sp.Matrix([2, 2, 2]) and e == sp.Matrix([-1, 0, 1]) and one.dot(e) == 0
    assert x.dot(x) == p.dot(p) + e.dot(e)          # 勾股定理
    # 插图用的数：x=(1,3), u=(3,1)
    u, x2 = sp.Matrix([3, 1]), sp.Matrix([1, 3])
    p2 = u.dot(x2) / u.dot(u) * u
    assert p2 == sp.Matrix([R(9, 5), R(3, 5)]) and u.dot(x2 - p2) == 0

    # 例：三种标准下的检索排序
    q = sp.Matrix([2, 1, 2])
    D = [sp.Matrix(d) for d in ([2, 2, 1], [4, 0, 3], [0, 3, 4], [6, 6, 3])]
    assert q.norm() == 3 and [d.norm() for d in D] == [3, 5, 5, 9]
    dots = [q.dot(d) for d in D]
    coss = [q.dot(d) / (q.norm() * d.norm()) for d in D]
    dist2 = [(q - d).dot(q - d) for d in D]
    assert dots == [8, 14, 11, 24]
    assert coss == [R(8, 9), R(14, 15), R(11, 15), R(8, 9)]
    assert dist2 == [2, 6, 12, 42]
    assert close([float(c) for c in coss], [0.889, 0.933, 0.733, 0.889], 5e-4)
    assert close([float(sp.sqrt(d)) for d in dist2], [1.41, 2.45, 3.46, 6.48], 5e-3)
    assert sorted(range(4), key=lambda i: -dots[i]) == [3, 1, 2, 0]           # d4 > d2 > d3 > d1
    assert coss[1] > coss[0] == coss[3] > coss[2]                             # d2 > d1 = d4 > d3
    assert sorted(range(4), key=lambda i: dist2[i]) == [0, 1, 2, 3]           # d1, d2, d3, d4
    assert D[3] == 3 * D[0]
    # 归一化后：‖a-b‖² = 2 - 2cos，三种排序一致
    qn = q / q.norm()
    for d, c in zip(D, coss):
        dn = d / d.norm()
        assert sp.simplify((qn - dn).dot(qn - dn) - (2 - 2 * c)) == 0 and qn.dot(dn) == c

    # 点积的方差：各分量独立、均值 0、方差 1 时 Var(q·k) = d_k
    # 精确检验：分量取 ±1（均值 0、方差 1），枚举 d=3 的全部 2^6 种情形
    vals = [sum(qi * ki for qi, ki in zip(s[:3], s[3:])) for s in itertools.product((-1, 1), repeat=6)]
    assert R(sum(vals), len(vals)) == 0 and R(sum(v * v for v in vals), len(vals)) == 3
    # 蒙特卡洛：标准正态
    for d in (16, 64, 256):
        s = np.sum(rng.standard_normal((20000, d)) * rng.standard_normal((20000, d)), axis=1)
        assert abs(s.std() / np.sqrt(d) - 1) < 0.03 and abs(s.mean()) < 0.05 * np.sqrt(d)

    # 例：缩放前后的 softmax
    def softmax(z):
        e = np.exp(np.asarray(z, dtype=float) - np.max(z))
        return e / e.sum()

    p_raw, p_scaled = softmax([8, 0, -8]), softmax([1, 0, -1])
    assert close(p_raw, [0.99966, 0.00034, 0.0000001], 5e-6)
    assert close(p_scaled, [0.665, 0.245, 0.090], 5e-4)
    assert np.sqrt(64) == 8

    # 高维随机向量近似正交：Var(cos) = 1/d
    for d in (10, 100, 1000):
        a, b_ = rng.standard_normal((20000, d)), rng.standard_normal((20000, d))
        cs = np.sum(a * b_, axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b_, axis=1))
        assert abs(cs.std() * np.sqrt(d) - 1) < 0.03

    # 例：余弦 0.3 算不算相似
    assert abs(0.3 * np.sqrt(768) - 8.3) < 0.05
    assert abs(1 / np.sqrt(768) - 0.036) < 5e-4
    assert abs(np.degrees(np.arccos(0.3)) - 72.5) < 0.05

    # 例：按全局范数裁剪
    g = sp.Matrix([3, 4, 12])
    assert g.norm() == 13
    gc = g / 13
    assert gc.norm() == 1 and close([float(t) for t in gc], [0.231, 0.308, 0.923], 5e-4)
    assert [min(max(t, -5), 5) for t in g] == [3, 4, 5]          # 按值裁剪，方向改变

    print("verify_vectors: all checks passed")


if __name__ == "__main__":
    main()
