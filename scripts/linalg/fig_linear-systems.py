"""第 3 章「线性方程组、消元与逆矩阵」的插图。"""
from common import *


def row_column():
    """2x - y = 1, x + y = 5 的行图像与列图像。"""
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.8, 4.3))

    plane(a, (-1.2, 5.6), (-1.6, 6.2))
    t = np.linspace(-1.2, 5.6, 2)
    a.plot(t, 2 * t - 1, color=C1, lw=2)
    a.plot(t, 5 - t, color=C2, lw=2)
    a.plot([2], [3], "o", color=INK, ms=6, zorder=5)
    a.text(2.25, 2.85, "$(2,\\,3)$", color=INK, fontsize=12)
    a.text(3.15, 4.3, "$2x-y=1$", color=C1, fontsize=12)
    a.text(3.6, 1.65, "$x+y=5$", color=C2, fontsize=12)
    a.set_title("行图像：两条直线的交点", fontsize=11, color=INK, pad=10)

    plane(b, (-3.6, 5.2), (-0.8, 5.9))
    a1, a2 = np.array([2, 1]), np.array([-1, 1])
    vec(b, 2 * a1, C1, "$2a_1$", lw=1.3, ls="--", label_ofs=(0.1, -0.35))
    vec(b, 3 * a2, MUTED, origin=2 * a1, lw=1.1, ls="--")
    b.text(2.75, 3.75, "$3a_2$", color=C2, fontsize=13)
    vec(b, a1, C1, "$a_1$", label_ofs=(-0.1, -0.5))
    vec(b, a2, C2, "$a_2$", label_ofs=(-0.6, 0.0))
    vec(b, (1, 5), C3, "$b=2a_1+3a_2$", label_ofs=(-2.9, 0.25))
    b.set_title("列图像：用两列凑出 $b$", fontsize=11, color=INK, pad=10)

    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "linear-systems-row-column")


def three_cases():
    """两个方程两个未知数的三种情形。"""
    fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.5))
    t = np.linspace(-1, 4.5, 2)
    lim = ((-0.8, 4.3), (-0.8, 4.3))

    ax = axs[0]
    plane(ax, *lim, ticks=False)
    ax.plot(t, 3 - t, color=C1, lw=2)
    ax.plot(t, t - 1, color=C2, lw=2)
    ax.plot([2], [1], "o", color=INK, ms=6, zorder=5)
    ax.text(2.25, 0.85, "$(2,\\,1)$", color=INK, fontsize=11)
    ax.set_title("相交：唯一解\n$x+y=3,\\ x-y=1$", fontsize=11, color=INK, pad=8)

    ax = axs[1]
    plane(ax, *lim, ticks=False)
    ax.plot(t, 3 - t, color=C1, lw=2)
    ax.plot(t, 1 - t, color=C2, lw=2)
    ax.set_title("平行：无解\n$x+y=3,\\ x+y=1$", fontsize=11, color=INK, pad=8)

    ax = axs[2]
    plane(ax, *lim, ticks=False)
    ax.plot(t, 3 - t, color=C1, lw=4.5, alpha=0.55)
    ax.plot(t, 3 - t, color=C2, lw=1.6, ls="--")
    ax.set_title("重合：无穷多解\n$x+y=3,\\ 2x+2y=6$", fontsize=11, color=INK, pad=8)

    fig.tight_layout(w_pad=1.8)
    save_fig(fig, "linear-systems-three-cases")


def main():
    row_column()
    three_cases()


if __name__ == "__main__":
    main()
