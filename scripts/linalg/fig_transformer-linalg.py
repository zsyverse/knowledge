"""第 12 章 用线性代数读 Transformer 的插图。"""
from matplotlib.patches import Arc, FancyBboxPatch, Polygon, Rectangle

from common import *


def attention():
    """手算例：注意力矩阵（下三角）与输出在值向量凸包中的位置。"""
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.2, 4.3), gridspec_kw=dict(width_ratios=[1, 1.15]))

    A = np.array([[1, 0, 0], [2 / 3, 1 / 3, 0], [4 / 9, 1 / 9, 4 / 9]])
    txt = [["1", "", ""], ["2/3", "1/3", ""], ["4/9", "1/9", "4/9"]]
    ax.set_xlim(0, 3)
    ax.set_ylim(3, 0)
    ax.set_aspect("equal")
    for i in range(3):
        for j in range(3):
            if j > i:
                ax.add_patch(Rectangle((j, i), 1, 1, fc="none", ec=MUTED, lw=0.8, hatch="///", alpha=0.5))
                ax.text(j + 0.5, i + 0.5, "0", ha="center", va="center", fontsize=13, color=MUTED,
                        bbox=dict(boxstyle="circle,pad=0.25", fc="#f2f2f2", ec="none"))
            else:
                ax.add_patch(Rectangle((j, i), 1, 1, fc=C1, ec=INK, lw=0.8, alpha=0.12 + 0.6 * A[i, j]))
                ax.add_patch(Rectangle((j, i), 1, 1, fc="none", ec=INK, lw=0.8))
                ax.text(j + 0.5, i + 0.5, txt[i][j], ha="center", va="center", fontsize=14, color=INK)
    ax.set_xticks([0.5, 1.5, 2.5], ["$j=1$", "$j=2$", "$j=3$"])
    ax.set_yticks([0.5, 1.5, 2.5], ["$i=1$", "$i=2$", "$i=3$"])
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelsize=11, colors=INK)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("注意力矩阵 $A$：第 $i$ 行是位置 $i$ 对各位置的权重\n阴影为被掩码的位置", fontsize=10.5, color=INK, labelpad=10)

    V = np.array([[0, 3], [3, 0], [3, 3]], dtype=float)
    O = A @ V
    plane(bx, (-0.6, 4.3), (-0.6, 4.0))
    bx.add_patch(Polygon(V, closed=True, fc=C1, ec=C1, alpha=0.10, lw=0))
    bx.add_patch(Polygon(V, closed=True, fc="none", ec=C1, lw=1.3))
    bx.plot(V[:, 0], V[:, 1], "o", color=INK, ms=7, zorder=5)
    bx.plot(O[1:, 0], O[1:, 1], "o", color=C2, ms=8, zorder=6)
    bx.plot(O[0, 0], O[0, 1], "o", mfc="none", mec=C2, mew=2, ms=14, zorder=6)
    bx.text(0.18, 3.3, "$v_1$", fontsize=13, color=INK, ha="left")
    bx.text(-0.15, 3.48, "$o_1$", fontsize=13, color=C2, ha="right")
    bx.text(3.12, 0.15, "$v_2$", fontsize=13, color=INK)
    bx.text(3.12, 3.15, "$v_3$", fontsize=13, color=INK)
    bx.text(0.62, 1.72, "$o_2$", fontsize=13, color=C2)
    bx.text(1.8, 2.3, "$o_3$", fontsize=13, color=C2)
    bx.set_xlabel("值向量 $v_j$ 与输出 $o_i$：输出落在值向量的凸包内", fontsize=10.5, color=INK, labelpad=10)
    fig.tight_layout(w_pad=3)
    save_fig(fig, "transformer-linalg-attention")


def rope():
    """RoPE：向量随位置旋转；内积只依赖相对位置。"""
    th = np.deg2rad(30)
    Rm = lambda a: np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.2, 4.4))
    circle = np.linspace(0, 2 * np.pi, 300)

    r = 2.2
    plane(ax, (-1.6, 3.0), (-0.6, 3.0), ticks=False)
    ax.plot(r * np.cos(circle), r * np.sin(circle), color=MUTED, lw=0.9, ls="--")
    x0 = r * np.array([np.cos(np.deg2rad(10)), np.sin(np.deg2rad(10))])
    for m, col in zip(range(4), (C1, C1, C1, C1)):
        v = Rm(m * th) @ x0
        vec(ax, v, col, lw=2.0 if m == 0 else 1.6)
        ax.text(*(v * 1.13), f"位置 {m}", fontsize=10.5, color=C1, ha="center", va="center")
    for m in range(3):
        a0 = 10 + 30 * m
        ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=a0, theta2=a0 + 30, color=MUTED, lw=1.0))
        mid = np.deg2rad(a0 + 15)
        ax.text(0.95 * np.cos(mid), 0.95 * np.sin(mid), "$\\theta$", fontsize=10.5, color=MUTED, ha="center", va="center")
    ax.set_title("每往后一个位置，多转一个 $\\theta$", fontsize=12, color=INK, pad=8)

    q0 = 2.0 * np.array([1.0, 0.0])
    k0 = 2.4 * np.array([np.cos(np.deg2rad(20)), np.sin(np.deg2rad(20))])
    plane(bx, (-3.0, 2.6), (-0.6, 3.0), ticks=False)
    for (m, n), ls, lw, alpha in (((1, 3), "-", 2.2, 1.0), ((3, 5), "--", 1.8, 1.0)):
        qm, kn = Rm(m * th) @ q0, Rm(n * th) @ k0
        vec(bx, qm, C1, lw=lw, ls=ls)
        vec(bx, kn, C2, lw=lw, ls=ls)
        bx.text(*(qm * 1.16), f"$q_{m}$", fontsize=13, color=C1, ha="center", va="center")
        bx.text(*(kn * 1.14), f"$k_{n}$", fontsize=13, color=C2, ha="center", va="center")
        a_q, a_k = 30 * m, 20 + 30 * n
        rad = 1.3 if m == 1 else 1.9
        bx.add_patch(Arc((0, 0), rad, rad, theta1=a_q, theta2=a_k, color=INK, lw=1.0))
        mid = np.deg2rad((a_q + a_k) / 2)
        bx.text((rad / 2 + 0.24) * np.cos(mid), (rad / 2 + 0.24) * np.sin(mid), "80°", fontsize=10, color=INK,
                ha="center", va="center")
    bx.set_title("位置对 (1, 3) 与 (3, 5)：夹角相同，内积相同", fontsize=12, color=INK, pad=8)
    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "transformer-linalg-rope")


def residual():
    """残差流：各子层从同一个向量读、往里写。"""
    fig, ax = plt.subplots(figsize=(10.4, 3.5))
    ax.set_xlim(0, 14.6)
    ax.set_ylim(0.2, 4.4)
    ax.axis("off")
    ys, yb = 3.2, 1.2

    def arrow(p, q, color=INK, lw=1.4):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12,
                                                        shrinkA=0, shrinkB=0))

    ax.text(0.2, ys, "$x_0$", fontsize=14, color=INK, va="center")
    ax.text(0.05, ys - 0.5, "词嵌入", fontsize=9.5, color=MUTED, va="center")
    ax.plot([0.9, 11.6], [ys, ys], color=C1, lw=3.0, solid_capstyle="butt")
    arrow((11.6, ys), (12.0, ys), C1, lw=3.0)
    ax.text(6.2, ys + 0.62, "残差流：贯穿各层的同一个 $d$ 维向量", fontsize=11, color=C1, ha="center")

    names = ["注意力", "FFN", "注意力", "FFN"]
    for i, name in enumerate(names):
        xr = 1.5 + 2.6 * i          # 读出的位置
        xw = xr + 1.8               # 写回的位置
        bxc = (xr + xw) / 2
        ax.add_patch(FancyBboxPatch((bxc - 0.6, yb - 0.4), 1.2, 0.8, boxstyle="round,pad=0,rounding_size=0.1",
                                    fc="none", ec=INK, lw=1.3))
        ax.text(bxc, yb, name, ha="center", va="center", fontsize=11, color=INK)
        ax.plot([xr, xr], [ys, yb], color=INK, lw=1.3)
        arrow((xr, yb), (bxc - 0.6, yb))
        ax.plot([bxc + 0.6, xw], [yb, yb], color=C2, lw=1.3)
        arrow((xw, yb), (xw, ys - 0.24), C2)
        ax.add_patch(plt.Circle((xw, ys), 0.24, fc="white", ec=INK, lw=1.3, zorder=5))
        ax.text(xw, ys, "+", fontsize=13, color=INK, ha="center", va="center", zorder=6)
        ax.text(xw + 0.12, (ys + yb) / 2, f"$\\Delta_{i + 1}$", fontsize=12, color=C2, ha="left", va="center")
        if i == 0:
            ax.text(xr - 0.15, (ys + yb) / 2, "读出", fontsize=10.5, color=INK, ha="right", va="center")
            ax.text(xw - 0.15, (ys + yb) / 2, "写入", fontsize=10.5, color=C2, ha="right", va="center")
    for xc, lab in ((3.7, "第 1 层"), (8.9, "第 2 层")):
        ax.text(xc, 0.42, lab, fontsize=10.5, color=MUTED, ha="center")
    ax.plot([1.2, 6.2], [0.68, 0.68], color=MUTED, lw=0.8)
    ax.plot([6.4, 11.4], [0.68, 0.68], color=MUTED, lw=0.8)

    ax.add_patch(FancyBboxPatch((12.0, ys - 0.4), 1.0, 0.8, boxstyle="round,pad=0,rounding_size=0.1", fc="none", ec=INK, lw=1.3))
    ax.text(12.5, ys, "$W_U$", fontsize=12, color=INK, ha="center", va="center")
    arrow((13.0, ys), (13.5, ys))
    ax.text(13.58, ys, "logits", fontsize=11.5, color=INK, va="center")
    ax.text(13.1, ys - 1.15, "$x_L=x_0+\\sum_\\ell\\Delta_\\ell$", fontsize=11.5, color=INK, ha="center", va="center")
    save_fig(fig, "transformer-linalg-residual")


def main():
    attention()
    rope()
    residual()


if __name__ == "__main__":
    main()
