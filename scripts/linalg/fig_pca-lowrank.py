"""第 10 章 PCA、低秩近似与 LoRA 的插图。"""
from matplotlib.patches import FancyBboxPatch, Rectangle

from common import *


def _pca(X, k):
    mu = X.mean(axis=0)
    Xc = X - mu
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = s**2 / (len(X) - 1)
    return mu, Vt[:k], Xc @ Vt[:k].T, var / var.sum()


def pca_axes():
    """手算例：5 个点、两个主方向；右图为白化后的点。"""
    X = np.array([[5.0, 3], [4, 4], [1, 1], [2, 0], [3, 2]])
    mu = X.mean(0)
    v1 = np.array([1, 1]) / np.sqrt(2)
    v2 = np.array([1, -1]) / np.sqrt(2)
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.2, 4.4), gridspec_kw=dict(width_ratios=[1.25, 1]))

    plane(ax, (-0.6, 7.6), (-1.2, 5.2))
    t = np.array([-3.4, 2.9])
    ax.plot(mu[0] + t * v1[0], mu[1] + t * v1[1], color=C1, lw=1.0, alpha=0.45)
    ax.plot(mu[0] + t * 0.5 * v2[0], mu[1] + t * 0.5 * v2[1], color=C2, lw=1.0, alpha=0.45)
    for p in X:
        foot = mu + ((p - mu) @ v1) * v1
        ax.plot([p[0], foot[0]], [p[1], foot[1]], color=MUTED, lw=1.0, ls="--")
    ax.plot(X[:, 0], X[:, 1], "o", color=INK, ms=7, zorder=5)
    vec(ax, v1 * np.sqrt(4.5), C1, origin=mu, lw=2.4)
    vec(ax, v2 * np.sqrt(0.5), C2, origin=mu, lw=2.4)
    ax.text(5.25, 4.45, "第一主方向 $v_1$\n方差 $\\lambda_1=4.5$", color=C1, fontsize=11, ha="left", va="center")
    ax.text(4.25, 0.85, "第二主方向 $v_2$\n方差 $\\lambda_2=0.5$", color=C2, fontsize=11, ha="left", va="center")
    ax.text(mu[0] - 0.12, mu[1] + 0.22, "均值 $\\mu$", color=INK, fontsize=10, ha="right")
    ax.set_title("原始数据与主方向", fontsize=12, color=INK, pad=10)

    Z = np.array([[1.0, 1], [1, -1], [-1, -1], [-1, 1], [0, 0]])
    plane(bx, (-2.2, 2.2), (-2.2, 2.2))
    bx.set_xticklabels(["-2", "", "", "2"])
    bx.set_yticklabels(["-2", "", "", "2"])
    th = np.linspace(0, 2 * np.pi, 200)
    bx.plot(np.cos(th), np.sin(th), color=MUTED, lw=1.0, ls="--")
    bx.plot(Z[:, 0], Z[:, 1], "o", color=INK, ms=7, zorder=5)
    vec(bx, (1, 0), C1, lw=2.4)
    vec(bx, (0, -1), C2, lw=2.4)
    bx.text(1.15, 0.15, "$z_1$，方差 1", color=C1, fontsize=11)
    bx.text(0.12, -1.55, "$z_2$，方差 1", color=C2, fontsize=11)
    bx.set_title("白化之后", fontsize=12, color=INK, pad=10)
    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "pca-lowrank-axes")


def truncation():
    """秩 5 加噪声矩阵：奇异值谱与截断误差。"""
    rng = np.random.default_rng(0)
    m, n = 200, 100
    M = rng.standard_normal((m, 5)) @ rng.standard_normal((5, n)) + 0.1 * rng.standard_normal((m, n))
    s = np.linalg.svd(M, compute_uv=False)
    ks = np.arange(0, 31)
    rel = np.array([np.sqrt((s[k:] ** 2).sum() / (s**2).sum()) for k in ks])

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(9.2, 3.5))
    style(ax)
    style(bx)
    idx = np.arange(1, 31)
    ax.semilogy(idx[:5], s[:5], "o", color=C1, ms=6)
    ax.semilogy(idx[5:], s[5:30], "o", color=MUTED, ms=4)
    ax.annotate("前 5 个：信号", (5, s[4]), (9, 110), color=C1, fontsize=11,
                arrowprops=dict(arrowstyle="->", color=C1))
    ax.annotate("其余：噪声", (14, s[13]), (15, 9), color=MUTED, fontsize=11,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.set_xlabel("序号 $i$", color=INK)
    ax.set_ylabel("奇异值 $\\sigma_i$", color=INK)
    ax.set_xlim(0, 31)
    ax.set_ylim(1, 400)

    bx.plot(ks, rel, "-o", color=C2, lw=1.8, ms=4)
    bx.axvline(5, color=MUTED, lw=0.9, ls="--")
    bx.annotate("$k=5$：误差 4.3%", (5, rel[5]), (9, 0.35), color=INK, fontsize=11,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    bx.set_xlabel("保留的秩 $k$", color=INK)
    bx.set_ylabel("相对误差", color=INK)
    bx.set_xlim(-0.5, 30.5)
    bx.set_ylim(0, 1.05)
    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "pca-lowrank-truncation")


def embedding():
    """64 维里的 3 个簇与 12 个簇，投影到前两个主成分。"""
    def clusters(n_cls, d=64, per=100, spread=8.0, seed=0):
        rng = np.random.default_rng(seed)
        centers = rng.standard_normal((n_cls, d)) * spread / np.sqrt(d)
        labels = np.repeat(np.arange(n_cls), per)
        return centers[labels] + rng.standard_normal((n_cls * per, d)), labels

    cmap = plt.get_cmap("tab20")
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.2))
    for ax, n_cls in zip(axs, (3, 12)):
        X, labels = clusters(n_cls)
        _, _, Z, ratio = _pca(X, 2)
        style(ax)
        colors = [C1, C2, C3] if n_cls == 3 else [cmap(i) for i in (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 1, 5)]
        for c in range(n_cls):
            pts = Z[labels == c]
            ax.plot(pts[:, 0], pts[:, 1], "o", color=colors[c], ms=3.2, alpha=0.75, mec="none")
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_xlabel(f"第一主成分（{ratio[0]:.1%}）", color=INK)
        ax.set_ylabel(f"第二主成分（{ratio[1]:.1%}）", color=INK)
        ax.set_title(f"{n_cls} 个簇：前两个主成分累计 {ratio[:2].sum():.1%}", fontsize=12, color=INK)
    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "pca-lowrank-embedding")


def lora():
    """LoRA 结构示意：冻结的 W 与旁路 A、B。"""
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")

    def box(x, y, w, h, color, text, sub=None, fill=0.10):
        ax.add_patch(Rectangle((x, y), w, h, fc=color, ec=color, lw=1.6, alpha=fill))
        ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=color, lw=1.6))
        ax.text(x + w / 2, y + h / 2 + (0.18 if sub else 0), text, ha="center", va="center", fontsize=13, color=color)
        if sub:
            ax.text(x + w / 2, y + h / 2 - 0.3, sub, ha="center", va="center", fontsize=9.5, color=color)

    def arrow(p, q, color=INK):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, mutation_scale=13))

    # 输入
    ax.text(0.45, 2.6, "$x$", fontsize=15, color=INK, ha="center", va="center")
    ax.text(0.45, 2.15, "$d_\\mathrm{in}$ 维", fontsize=9.5, color=MUTED, ha="center")
    ax.plot([0.8, 1.5], [2.6, 2.6], color=INK, lw=1.4)
    ax.plot([1.5, 1.5], [1.2, 4.0], color=INK, lw=1.4)
    # 主路：冻结的 W
    arrow((1.5, 4.0), (3.4, 4.0))
    box(3.4, 3.2, 2.6, 1.6, MUTED, "$W$", "冻结，$d_\\mathrm{out}\\times d_\\mathrm{in}$")
    ax.plot([6.0, 8.4], [4.0, 4.0], color=INK, lw=1.4)
    arrow((8.4, 4.0), (8.4, 2.95))
    # 旁路：A 降维，B 升维
    arrow((1.5, 1.2), (2.5, 1.2))
    box(2.5, 0.75, 2.0, 0.9, C1, "$A$")
    ax.text(3.5, 0.6, "$r\\times d_\\mathrm{in}$，随机初始化", fontsize=9.5, color=C1, ha="center", va="top")
    arrow((4.5, 1.2), (5.5, 1.2), C1)
    ax.text(5.0, 1.42, "$r$ 维", fontsize=9.5, color=C1, ha="center")
    box(5.5, 0.3, 0.9, 1.8, C2, "$B$")
    ax.text(5.95, 2.22, "$d_\\mathrm{out}\\times r$，零初始化", fontsize=9.5, color=C2, ha="center", va="bottom")
    ax.plot([6.4, 8.4], [1.2, 1.2], color=INK, lw=1.4)
    ax.text(7.4, 1.42, "$\\times\\ \\alpha/r$", fontsize=11, color=INK, ha="center")
    arrow((8.4, 1.2), (8.4, 2.25))
    # 相加
    ax.add_patch(plt.Circle((8.4, 2.6), 0.33, fc="none", ec=INK, lw=1.4))
    ax.text(8.4, 2.6, "+", fontsize=15, color=INK, ha="center", va="center")
    arrow((8.73, 2.6), (9.45, 2.6))
    ax.text(9.55, 2.6, "$W'x$", fontsize=14, color=INK, ha="left", va="center")
    save_fig(fig, "pca-lowrank-lora")


def main():
    pca_axes()
    truncation()
    embedding()
    lora()


if __name__ == "__main__":
    main()
