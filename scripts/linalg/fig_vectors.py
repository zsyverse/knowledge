"""第 1 章「向量、内积与范数」的插图。"""
from common import *


def combination():
    """左：向量加法的平行四边形；右：b = 2 v1 + v2。"""
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 4.1))

    plane(a, (-0.6, 5.2), (-0.6, 4.2))
    x, y = np.array([3, 1]), np.array([1, 2])
    vec(a, y, MUTED, origin=x, lw=1.1, ls="--")
    vec(a, x, MUTED, origin=y, lw=1.1, ls="--")
    vec(a, x, C1, "$x$", label_ofs=(0.05, -0.38))
    vec(a, y, C2, "$y$", label_ofs=(-0.32, 0.08))
    vec(a, x + y, C3, "$x+y$", label_ofs=(0.08, 0.1))
    a.set_title("加法：把 $y$ 平移到 $x$ 的终点", fontsize=11, color=INK, pad=10)

    plane(b, (-0.6, 6.4), (-0.6, 5.9))
    v1, v2 = np.array([1, 2]), np.array([3, 1])
    vec(b, 2 * v1, C1, "$2v_1$", lw=1.3, ls="--", label_ofs=(-0.72, 0.05))
    vec(b, v2, MUTED, origin=2 * v1, lw=1.1, ls="--")
    b.text(3.2, 4.72, "$v_2$", color=C2, fontsize=13)
    vec(b, v1, C1, "$v_1$", label_ofs=(-0.5, -0.05))
    vec(b, v2, C2, "$v_2$", label_ofs=(0.08, -0.35))
    vec(b, (5, 5), C3, "$b=2v_1+v_2$", label_ofs=(-1.1, 0.25))
    b.set_title("线性组合：沿 $v_1$ 走 2 步，再沿 $v_2$ 走 1 步", fontsize=11, color=INK, pad=10)

    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "vectors-combination")


def unit_balls():
    """三种范数的单位球（二维）。"""
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    plane(ax, (-1.55, 1.55), (-1.55, 1.55), ticks=False)
    for xy, s in (((1.07, -0.2), "1"), ((-1.3, -0.2), "−1"), ((0.07, 1.08), "1"), ((0.07, -1.22), "−1")):
        ax.text(*xy, s, color=MUTED, fontsize=10)
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=C2, lw=2, label=r"$\|x\|_1=1$：菱形")
    ax.plot(np.cos(t), np.sin(t), color=C1, lw=2, label=r"$\|x\|_2=1$：圆")
    ax.plot([1, -1, -1, 1, 1], [1, 1, -1, -1, 1], color=C3, lw=2, label=r"$\|x\|_\infty=1$：正方形")
    ax.legend(frameon=False, fontsize=11, loc="center left", bbox_to_anchor=(1.02, 0.5), labelcolor=INK)
    save_fig(fig, "vectors-unit-balls")


def projection():
    """x 向 u 所在直线的投影 p 与残差 e。"""
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    plane(ax, (-0.7, 4.3), (-0.9, 3.7), ticks=False)
    u, x = np.array([3.0, 1.0]), np.array([1.0, 3.0])
    c = (u @ x) / (u @ u)
    p = c * u
    ax.plot([-0.6 * 3, 1.4 * 3], [-0.6, 1.4], color=MUTED, lw=0.9, ls=":")
    vec(ax, u, INK, "$u$", lw=1.6, label_ofs=(0.08, -0.36))
    vec(ax, x, C1, "$x$", label_ofs=(-0.05, 0.12))
    vec(ax, x - p, C2, None, origin=p, lw=1.6, ls="--")
    ax.text(1.55, 1.95, "$e=x-p$", color=C2, fontsize=13)
    vec(ax, p, C3, None, lw=2.6)
    ax.text(0.75, -0.55, r"$p=\frac{u^{\mathsf{T}}x}{u^{\mathsf{T}}u}\,u$", color=C3, fontsize=17)
    # 直角标记
    d1 = u / np.linalg.norm(u) * 0.22
    d2 = (x - p) / np.linalg.norm(x - p) * 0.22
    sq = np.array([p - d1, p - d1 + d2, p + d2])
    ax.plot(sq[:, 0], sq[:, 1], color=MUTED, lw=1.0)
    save_fig(fig, "vectors-projection")


def main():
    combination()
    unit_balls()
    projection()


if __name__ == "__main__":
    main()
