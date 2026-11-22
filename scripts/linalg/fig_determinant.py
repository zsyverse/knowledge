"""第 5 章 行列式 的插图。

    .venv/bin/python scripts/linalg/fig_determinant.py
"""
from matplotlib.patches import FancyArrowPatch, Polygon

from common import *


def _para(ax, a, b, color, alpha=0.16, ls="-", lw=1.2, fill=True):
    a, b = np.asarray(a, float), np.asarray(b, float)
    pts = [(0, 0), a, a + b, b]
    if fill:
        ax.add_patch(Polygon(pts, closed=True, facecolor=color, alpha=alpha, edgecolor="none"))
    ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor=color, lw=lw, ls=ls))


def _turn(ax, a, b, r=0.75):
    """从 a 的方向转到 b 的方向的弧形箭头，表示定向。"""
    ta, tb = np.arctan2(a[1], a[0]), np.arctan2(b[1], b[0])
    p, q = r * np.array([np.cos(ta), np.sin(ta)]), r * np.array([np.cos(tb), np.sin(tb)])
    rad = 0.45 if tb > ta else -0.45
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=11, color=INK, lw=1.1, zorder=6))


def area():
    fig, axs = plt.subplots(1, 3, figsize=(11.4, 4.0))
    cases = [
        ((3, 1), (1, 2), "$\\det=5$：面积放大 5 倍，定向不变"),
        ((1, 2), (3, 1), "$\\det=-5$：面积放大 5 倍，定向翻转"),
        ((2, 1), (4, 2), "$\\det=0$：压成一条线段"),
    ]
    for ax, (a1, a2, title) in zip(axs, cases):
        plane(ax, (-0.7, 4.7), (-0.7, 3.7))
        ax.add_patch(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True, facecolor=MUTED, alpha=0.18,
                             edgecolor=MUTED, lw=1.0, ls="--"))
        degenerate = a1[0] * a2[1] - a1[1] * a2[0] == 0
        if not degenerate:
            _para(ax, a1, a2, C3)
            _turn(ax, a1, a2)
        upper, lower = (-0.15, 0.18), (0.1, -0.38)
        if degenerate:
            ofs1, ofs2 = (-0.1, 0.28), (0.05, -0.5)
        else:
            ofs1, ofs2 = (lower, upper) if a1[1] < a2[1] else (upper, lower)
        vec(ax, a2, C2, "$a_2$", label_ofs=ofs2, lw=2.2)
        vec(ax, a1, C1, "$a_1$", label_ofs=ofs1, lw=2.2)
        ax.set_title(title, fontsize=11.5, color=INK, pad=10)
    axs[0].text(1.75, 1.42, "面积 5", color=C3, fontsize=11.5)
    axs[1].text(1.75, 1.42, "面积 5", color=C3, fontsize=11.5)
    axs[2].annotate("单位方格", (0.5, 0.92), (0.2, 1.75), fontsize=10, color=MUTED,
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    fig.subplots_adjust(wspace=0.12)
    save_fig(fig, "determinant-area")


def shear():
    fig, axs = plt.subplots(1, 3, figsize=(11.4, 3.4))
    f = 5 / 3
    steps = [
        ((3, 1), (1, 2), None, "两行为 $(3,1)$、$(1,2)$"),
        ((3, 1), (0, f), ((3, 1), (1, 2)), "$r_2-\\frac{1}{3}r_1$：两行为 $(3,1)$、$(0,\\frac{5}{3})$"),
        ((3, 0), (0, f), ((3, 1), (0, f)), "$r_1-\\frac{3}{5}r_2$：两行为 $(3,0)$、$(0,\\frac{5}{3})$"),
    ]
    for ax, (r1, r2, ghost, title) in zip(axs, steps):
        plane(ax, (-0.7, 4.7), (-0.7, 3.7))
        if ghost:
            _para(ax, *ghost, MUTED, fill=False, ls="--", lw=1.0)
        _para(ax, r1, r2, C3)
        vec(ax, r2, C2, "$r_2$", label_ofs=(-0.42, 0.12) if r2[0] else (0.14, -0.42), lw=2.2)
        vec(ax, r1, C1, "$r_1$", label_ofs=(0.1, -0.38) if r1[1] else (0.1, 0.14), lw=2.2)
        ax.set_title(title, fontsize=11.5, color=INK, pad=10)
        c = (np.asarray(r1, float) + np.asarray(r2, float)) / 2
        ax.text(c[0], c[1], "面积 5", color=C3, fontsize=11.5, ha="center", va="center")
    fig.subplots_adjust(wspace=0.12)
    save_fig(fig, "determinant-shear")


def change_of_variables():
    fig, ax = axes(6.6, 3.5)
    pdf = lambda t, mu, sd: np.exp(-0.5 * ((t - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    t = np.linspace(-4, 7, 600)
    ax.plot(t, pdf(t, 0, 1), color=C1, lw=2)
    ax.plot(t, pdf(t, 1, 2), color=C2, lw=2)
    zz = np.linspace(0.5, 1.0, 50)
    xx = np.linspace(2.0, 3.0, 50)
    ax.fill_between(zz, pdf(zz, 0, 1), color=C1, alpha=0.35, lw=0)
    ax.fill_between(xx, pdf(xx, 1, 2), color=C2, alpha=0.35, lw=0)
    ax.text(0.7, 0.39, "$p_Z(z)$，$Z\\sim N(0,1)$", color=C1, fontsize=11.5)
    ax.text(4.2, 0.1, "$p_X(x)$，$X=2Z+1$", color=C2, fontsize=11.5)
    ax.annotate("$z\\in[0.5,\\,1]$：宽 0.5", (0.8, 0.24), (1.55, 0.315), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate("$x\\in[2,\\,3]$：宽 1，高度减半\n两块阴影面积相等", (2.5, 0.08), (3.3, 0.2), fontsize=10.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED), linespacing=1.4)
    ax.set_xlim(-4, 7)
    ax.set_ylim(0, 0.44)
    ax.set_xlabel("$z$ 或 $x$", color=INK)
    ax.set_ylabel("概率密度", color=INK)
    save_fig(fig, "determinant-change-of-variables")


def main():
    area()
    shear()
    change_of_variables()


if __name__ == "__main__":
    main()
