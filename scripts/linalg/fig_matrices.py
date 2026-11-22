"""第 2 章「矩阵与线性变换」的插图。"""
from common import *

SQUARE = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float).T   # 2 x 5，单位方格的顶点


def _draw(ax, A, title, lim=((-1.6, 2.6), (-1.1, 2.3)), ghost=None):
    """画出单位方格（虚线）及其在 A 下的像（填色），以及 Ae1（蓝）、Ae2（橙）。"""
    A = np.asarray(A, dtype=float)
    plane(ax, *lim, ticks=False)
    ax.plot(SQUARE[0], SQUARE[1], color=MUTED, lw=1.0, ls="--")
    if ghost is not None:                      # 中间结果，细点线
        g = np.asarray(ghost, dtype=float) @ SQUARE
        ax.plot(g[0], g[1], color=MUTED, lw=1.0, ls=":")
    img = A @ SQUARE
    ax.fill(img[0], img[1], color=C3, alpha=0.22, lw=0)
    ax.plot(img[0], img[1], color=C3, lw=1.4)
    vec(ax, A[:, 0], C1, lw=2.0)
    vec(ax, A[:, 1], C2, lw=2.0)
    ax.set_title(title, fontsize=11, color=INK, pad=8)


def transforms():
    t = np.pi / 6
    items = [
        ("旋转 $30^\\circ$", [[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]),
        ("伸缩：横向 ×2，纵向 ×0.5", [[2, 0], [0, 0.5]]),
        ("剪切：$e_2$ 被推到 $(1,1)$", [[1, 1], [0, 1]]),
        ("向横轴投影：方格被压成线段", [[1, 0], [0, 0]]),
        ("关于直线 $y=x$ 反射", [[0, 1], [1, 0]]),
        ("一般矩阵：列为 $(2,1)$、$(-1,1)$", [[2, -1], [1, 1]]),
    ]
    fig, axs = plt.subplots(2, 3, figsize=(10.2, 6.0))
    for ax, (title, A) in zip(axs.ravel(), items):
        _draw(ax, A, title)
        if title.startswith("关于"):
            ax.plot([-1.0, 2.2], [-1.0, 2.2], color=MUTED, lw=0.8, ls=":")
    axs[0, 0].text(0.99, 0.37, "$Ae_1$", color=C1, fontsize=12)
    axs[0, 0].text(-1.05, 0.95, "$Ae_2$", color=C2, fontsize=12)
    fig.tight_layout(w_pad=1.5, h_pad=2.0)
    save_fig(fig, "matrices-transforms")


def composition():
    S = np.array([[1, 1], [0, 1]])     # 剪切
    R = np.array([[0, -1], [1, 0]])    # 逆时针旋转 90°
    fig, (a, b) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    lim = ((-2.3, 2.3), (-0.7, 2.7))
    _draw(a, S @ R, "先旋转 $90^\\circ$ 再剪切：$SR$", lim, ghost=R)
    _draw(b, R @ S, "先剪切再旋转 $90^\\circ$：$RS$", lim, ghost=S)
    a.text(1.08, 1.05, "$SRe_1$", color=C1, fontsize=12)
    a.text(-1.75, 0.15, "$SRe_2$", color=C2, fontsize=12)
    b.text(0.1, 1.05, "$RSe_1$", color=C1, fontsize=12)
    b.text(-1.95, 1.0, "$RSe_2$", color=C2, fontsize=12)
    fig.tight_layout(w_pad=2.5)
    save_fig(fig, "matrices-composition")


def main():
    transforms()
    composition()


if __name__ == "__main__":
    main()
