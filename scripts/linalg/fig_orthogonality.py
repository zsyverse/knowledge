"""第 6 章 正交、投影与最小二乘 的插图。

    .venv/bin/python scripts/linalg/fig_orthogonality.py
"""
from matplotlib.patches import Polygon

from common import *


def projection():
    """b 向平面（列空间）的投影，斜二测画法。"""
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    ax.set_aspect("equal")
    ax.axis("off")
    plane_pts = np.array([(0, 0), (6.2, 0), (8.0, 2.3), (1.8, 2.3)])
    ax.add_patch(Polygon(plane_pts, closed=True, facecolor=C1, alpha=0.13, edgecolor="none"))
    ax.add_patch(Polygon(plane_pts, closed=True, fill=False, edgecolor=C1, lw=1.3))
    O, P_, B = np.array([1.7, 0.75]), np.array([5.6, 1.45]), np.array([5.6, 4.1])

    vec(ax, np.array([2.3, 0.0]), MUTED, "$a_1$", origin=O, lw=1.3, label_ofs=(0.05, -0.38), fontsize=12)
    vec(ax, np.array([0.95, 1.2]), MUTED, "$a_2$", origin=O, lw=1.3, label_ofs=(-0.42, 0.05), fontsize=12)
    vec(ax, P_ - O, C1, origin=O, lw=2.2)
    vec(ax, B - O, INK, origin=O, lw=2.2)
    vec(ax, B - P_, C2, origin=P_, lw=2.0, ls="--")
    # 直角记号
    dvec = (O - P_) / np.linalg.norm(O - P_)
    s = 0.27
    ax.plot(*np.array([P_ + s * dvec, P_ + s * dvec + (0, s), P_ + (0, s)]).T, color=MUTED, lw=1.0)
    for pt in (O, P_):
        ax.plot(*pt, "o", color=INK, ms=4.5, zorder=6)

    ax.text(B[0] + 0.15, B[1] - 0.05, "$b$", fontsize=14, color=INK)
    ax.text(P_[0] + 0.15, P_[1] - 0.45, "$p=A\\hat{x}=Pb$", fontsize=13, color=INK)
    ax.text(P_[0] + 0.2, (P_[1] + B[1]) / 2, "$e=b-p$\n与平面垂直", fontsize=12.5, color=C2, va="center", linespacing=1.5)
    ax.text(O[0] - 0.12, O[1] - 0.42, "$0$", fontsize=12, color=MUTED)
    ax.text(6.3, 0.22, "列空间 $C(A)$", fontsize=12, color=C1, ha="right")
    ax.set_xlim(-0.3, 8.6)
    ax.set_ylim(-0.3, 4.5)
    save_fig(fig, "orthogonality-projection")


def least_squares():
    fig, ax = axes(5.8, 3.9)
    t = np.array([0.0, 1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 2.0, 4.0])
    A = np.column_stack([np.ones(4), t])
    c, d = np.linalg.lstsq(A, y, rcond=None)[0]
    tt = np.linspace(-0.4, 3.5, 2)
    ax.plot(tt, c + d * tt, color=C1, lw=2)
    fit = c + d * t
    for ti, yi, fi in zip(t, y, fit):
        ax.plot([ti, ti], [yi, fi], color=C2, lw=1.8)
    ax.plot(t, fit, "o", color=C1, ms=5)
    ax.plot(t, y, "o", color=INK, ms=7, zorder=5)
    for ti, yi, fi in zip(t, y, fit):
        left = yi > fi                       # 点在直线上方时标在左边，避开向右上升的直线
        ax.text(ti + (-0.1 if left else 0.1), (yi + fi) / 2 + (0.06 if left else 0), f"{yi - fi:+.1f}",
                color=C2, fontsize=11, va="center", ha="right" if left else "left")
    ax.text(1.42, 3.2, "$y=0.9+0.9\\,t$", color=C1, fontsize=12.5, ha="right")
    ax.annotate("", (2.62, 3.22), (1.5, 3.25), arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(2.25, 1.45, "残差 $e_i=y_i-(c+dt_i)$", color=C2, fontsize=11)
    ax.set_xlim(-0.5, 3.6)
    ax.set_ylim(0, 4.6)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xlabel("$t$", color=INK)
    ax.set_ylabel("$y$", color=INK)
    save_fig(fig, "orthogonality-least-squares")


def init():
    """与正文代码相同的随机数顺序：先取 x0，再依次跑 正交、c=1.0、c=0.9、c=1.1。"""
    rng = np.random.default_rng(0)
    d, depth = 64, 50
    x0 = rng.standard_normal(d)
    x0 /= np.linalg.norm(x0)

    def run(make):
        x, norms = x0.copy(), [1.0]
        for _ in range(depth):
            x = make() @ x
            norms.append(np.linalg.norm(x))
        return norms

    orth = lambda: np.linalg.qr(rng.standard_normal((d, d)))[0]
    gauss = lambda c: (lambda: c * rng.standard_normal((d, d)) / np.sqrt(d))
    curves = [("正交矩阵", orth, C3), ("高斯，$c=1.0$", gauss(1.0), C1),
              ("高斯，$c=0.9$", gauss(0.9), C2), ("高斯，$c=1.1$", gauss(1.1), C4)]
    fig, ax = axes(6.4, 3.8)
    for name, make, color in curves:
        norms = run(make)
        ax.plot(range(depth + 1), norms, color=color, lw=2)
        ax.text(depth + 1, norms[-1], name, color=color, fontsize=11, va="center")
    ax.set_yscale("log")
    ax.set_xlim(0, depth)
    ax.set_xlabel("层数", color=INK)
    ax.set_ylabel("信号范数 $\\Vert x_l\\Vert$（对数坐标）", color=INK)
    save_fig(fig, "orthogonality-init")


def main():
    projection()
    least_squares()
    init()


if __name__ == "__main__":
    main()
