"""第 4 章 线性无关、秩与四个基本子空间 的插图。

    .venv/bin/python scripts/linalg/fig_subspaces.py
"""
from matplotlib.patches import Polygon

from common import *


def _dir(deg):
    t = np.deg2rad(deg)
    return np.array([np.cos(t), np.sin(t)])


def _rect(ax, o, a, b, color):
    """以 o 为一个顶点、沿向量 a 和 b 张开的矩形。"""
    pts = [o, o + a, o + a + b, o + b]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, alpha=0.16, edgecolor=color, lw=1.6))
    ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor=color, lw=1.6))
    return o + (a + b) / 2


def _arrow(ax, p, q, color=INK, ls="-", lw=1.4, rad=0.0):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=3, shrinkB=3,
                                mutation_scale=13, connectionstyle=f"arc3,rad={rad}"))


def four_subspaces():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_aspect("equal")
    ax.axis("off")

    OL, OR = np.array([0.0, 0.0]), np.array([8.2, 0.0])
    # 左边 R^n：行空间在上，零空间在下，在原点垂直相接
    p, q = _dir(120), _dir(210)
    c_row = _rect(ax, OL, 2.9 * p, 1.9 * (-q), C1)
    c_null = _rect(ax, OL, 2.3 * q, 1.5 * (-p), C2)
    # 右边 R^m：列空间在上，左零空间在下
    p2, q2 = _dir(60), _dir(-30)
    c_col = _rect(ax, OR, 2.9 * p2, 1.9 * (-q2), C1)
    c_lnull = _rect(ax, OR, 1.7 * q2, 1.1 * (-p2), C2)

    kw = dict(va="center", fontsize=12, color=INK, linespacing=1.5)
    ax.text(-1.85, 2.75, "行空间 $C(A^{\\mathsf{T}})$\n维数 $r$", ha="right", **kw)
    ax.text(-2.25, -1.75, "零空间 $N(A)$\n维数 $n-r$", ha="right", **kw)
    ax.text(OR[0] + 1.85, 2.75, "列空间 $C(A)$\n维数 $r$", ha="left", **kw)
    ax.text(OR[0] + 1.75, -1.55, "左零空间 $N(A^{\\mathsf{T}})$\n维数 $m-r$", ha="left", **kw)
    ax.text(OL[0] + 0.1, 3.9, "$\\mathbb{R}^n$", ha="center", fontsize=16, color=INK)
    ax.text(OR[0] - 0.1, 3.9, "$\\mathbb{R}^m$", ha="center", fontsize=16, color=INK)

    # 直角记号
    for o, a, b in ((OL, p, q), (OR, p2, q2)):
        s = 0.22
        ax.plot(*np.array([o + s * a, o + s * a + s * b, o + s * b]).T, color=MUTED, lw=0.9)

    # 点与箭头
    xr = OL + 1.15 * p + 0.75 * (-q)
    xn = OL + 1.25 * q + 0.55 * (-p)
    x = xr + xn - OL
    b = OR + 1.15 * p2 + 0.75 * (-q2)
    for pt in (xr, xn, x, b, OL, OR):
        ax.plot(*pt, "o", color=INK, ms=4.5, zorder=5)
    ax.plot(*np.array([xr, x, xn]).T, color=MUTED, lw=0.9, ls="--")
    ax.text(xr[0] - 0.5, xr[1] + 0.12, "$x_r$", fontsize=13, color=INK)
    ax.text(xn[0] - 0.12, xn[1] - 0.48, "$x_n$", fontsize=13, color=INK)
    ax.text(x[0] - 0.2, x[1], "$x=x_r+x_n$", fontsize=13, color=INK, ha="right", va="center")
    ax.text(b[0] + 0.16, b[1] + 0.1, "$b$", fontsize=13, color=INK)
    ax.text(OL[0] + 0.4, OL[1] - 0.32, "$0$", fontsize=12, color=MUTED)
    ax.text(OR[0] - 0.66, OR[1] - 0.34, "$0$", fontsize=12, color=MUTED)

    _arrow(ax, xr, b, rad=-0.1)
    _arrow(ax, xn, OR, rad=0.14)
    _arrow(ax, x, b, color=MUTED, ls="--", lw=1.1, rad=-0.5)
    ax.text(4.3, 1.98, "$Ax_r=b$", ha="center", fontsize=12.5, color=INK)
    ax.text(4.3, -1.5, "$Ax_n=0$", ha="center", fontsize=12.5, color=INK)
    ax.text(4.0, 4.12, "$Ax=b$", ha="center", fontsize=12.5, color=MUTED)

    ax.set_xlim(-5.4, 13.4)
    ax.set_ylim(-2.9, 4.7)
    save_fig(fig, "subspaces-four")


def solution_set():
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    plane(ax, (-3.6, 5.6), (-1.6, 3.6))
    t = np.linspace(-4, 6, 2)
    ax.plot(t, -t / 2, color=C2, lw=2)
    ax.plot(t, (4 - t) / 2, color=C1, lw=2)
    ax.text(-3.5, 1.95, "零空间 $N(A)$\n$x_1+2x_2=0$", color=C2, fontsize=11, va="bottom", linespacing=1.4)
    ax.text(3.45, 1.55, "解集 $x_1+2x_2=4$\n（不过原点）", color=C1, fontsize=11, va="bottom", linespacing=1.4)

    xp, s = np.array([4.0, 0.0]), np.array([-2.0, 1.0])
    vec(ax, xp, INK, lw=1.8)
    ax.text(3.72, -0.52, "$x_p$", color=INK, fontsize=13)
    vec(ax, s, C2, "$x_n$", label_ofs=(-0.42, -0.5), lw=1.8)
    vec(ax, s, C2, origin=xp, lw=1.4, ls="--")
    vec(ax, xp + s, C1, "$x_p+x_n$", label_ofs=(0.02, 0.2), lw=1.8)
    for c in (-0.5, 1, 2):
        ax.plot(*(xp + c * s), "o", color=C1, ms=5, zorder=5)
    ax.plot(0, 0, "o", color=INK, ms=4, zorder=5)
    save_fig(fig, "subspaces-solution-set")


def min_norm():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    plane(ax, (-1.6, 5.2), (-1.6, 3.2))
    t = np.linspace(-2, 6, 2)
    ax.plot(t, (4 - t) / 2, color=C1, lw=2)
    ax.plot(t, 2 * t, color=MUTED, lw=1.1, ls="--")
    ax.plot(t, -t / 2, color=C2, lw=1.3)
    th = np.linspace(0, 2 * np.pi, 200)
    rad = 4 / np.sqrt(5)
    ax.plot(rad * np.cos(th), rad * np.sin(th), color=GRID, lw=1.2)

    X, y = np.array([[1.0, 2.0]]), np.array([4.0])

    def path(w, lr=0.06, steps=12):
        pts = [w]
        for _ in range(steps):
            w = w - lr * X.T @ (X @ w - y)
            pts.append(w)
        return np.array(pts)

    for w0, color in ((np.array([0.0, 0.0]), C3), (np.array([2.0, -0.5]), C4)):
        pts = path(w0)
        ax.plot(pts[:, 0], pts[:, 1], "-", color=color, lw=1.6)
        ax.plot(pts[:-1, 0], pts[:-1, 1], "o", color=color, ms=4)
        for i in (1, 3):
            vec(ax, 0.55 * (pts[i + 1] - pts[i]), color, origin=pts[i], lw=1.6)
    ax.plot(0.8, 1.6, "o", color=C3, ms=8, mec="white", mew=1.2, zorder=6)
    ax.plot(2.6, 0.7, "o", color=C4, ms=8, mec="white", mew=1.2, zorder=6)
    ax.plot(2.0, -0.5, "o", color=C4, ms=6, zorder=6)
    ax.plot(0, 0, "o", color=C3, ms=6, zorder=6)

    ax.text(0.95, 1.78, "最小范数解 $w^\\star$", color=C3, fontsize=11.5)
    ax.text(2.75, 0.88, "另一个解", color=C4, fontsize=11.5)
    ax.text(2.12, -0.95, "$w_0\\neq 0$", color=C4, fontsize=12)
    ax.text(-0.95, 0.18, "$w_0=0$", color=C3, fontsize=12)
    ax.text(3.45, -0.88, "解集 $w_1+2w_2=4$", color=C1, fontsize=11)
    ax.text(1.18, 2.72, "行空间 $C(X^{\\mathsf{T}})$", color=MUTED, fontsize=11)
    ax.text(2.9, -1.38, "零空间 $N(X)$", color=C2, fontsize=11)
    save_fig(fig, "subspaces-min-norm")


def main():
    four_subspaces()
    solution_set()
    min_norm()


if __name__ == "__main__":
    main()
