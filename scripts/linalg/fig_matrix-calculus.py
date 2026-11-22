"""第 11 章 矩阵求导与反向传播的插图。"""
from matplotlib.patches import FancyBboxPatch

from common import *


def graph():
    """两层 MLP 的计算图：前向的中间量与反向的梯度。"""
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0.9, 5.3)
    ax.axis("off")

    yc, bw, bh = 3.0, 1.9, 1.3
    ops = [(2.6, "线性层\n$W_1,\\ b_1$"), (5.7, "ReLU"), (8.8, "线性层\n$W_2,\\ b_2$"), (11.9, "softmax\n交叉熵")]
    for xc, name in ops:
        ax.add_patch(FancyBboxPatch((xc - bw / 2, yc - bh / 2), bw, bh, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="none", ec=INK, lw=1.4))
        ax.text(xc, yc, name, ha="center", va="center", fontsize=11.5, color=INK, linespacing=1.4)

    def arrow(p, q, color):
        ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, mutation_scale=13,
                                                        shrinkA=0, shrinkB=0))

    # 前向（蓝）：箭头在上半，变量名写在箭头上方
    xs = [x for x, _ in ops]
    fwd = [((0.55, xs[0] - bw / 2), "$X$"), ((xs[0] + bw / 2, xs[1] - bw / 2), "$Z_1$"),
           ((xs[1] + bw / 2, xs[2] - bw / 2), "$H$"), ((xs[2] + bw / 2, xs[3] - bw / 2), "$Z_2$"),
           ((xs[3] + bw / 2, 13.75), "$L$")]
    for (x0, x1), name in fwd:
        arrow((x0, yc + 0.32), (x1, yc + 0.32), C1)
        ax.text((x0 + x1) / 2, yc + 0.5, name, ha="center", va="bottom", fontsize=13, color=C1)

    # 反向（橙）：箭头在下半，梯度写在箭头下方
    bwd = [((xs[3] - bw / 2, xs[2] + bw / 2), "$\\delta_2=(P-Y)/n$"),
           ((xs[2] - bw / 2, xs[1] + bw / 2), "$\\partial L/\\partial H=\\delta_2W_2$"),
           ((xs[1] - bw / 2, xs[0] + bw / 2), "$\\delta_1=\\partial L/\\partial H\\odot[Z_1>0]$")]
    for (x0, x1), name in bwd:
        arrow((x0, yc - 0.32), (x1, yc - 0.32), C2)
        ax.text((x0 + x1) / 2, yc - bh / 2 - 0.3, name, ha="center", va="top", fontsize=11.5, color=C2)

    # 参数的梯度：从线性层向上分出
    for xc, name in ((xs[0], "$\\partial L/\\partial W_1=\\delta_1^{\\top}X,\\ \\ \\partial L/\\partial b_1=\\delta_1^{\\top}\\mathbf{1}$"),
                     (xs[2], "$\\partial L/\\partial W_2=\\delta_2^{\\top}H,\\ \\ \\partial L/\\partial b_2=\\delta_2^{\\top}\\mathbf{1}$")):
        arrow((xc, yc + bh / 2), (xc, yc + bh / 2 + 0.62), C2)
        ax.text(xc, yc + bh / 2 + 0.75, name, ha="center", va="bottom", fontsize=12, color=C2)

    # 图例
    arrow((0.3, 1.25), (1.0, 1.25), C1)
    ax.text(1.12, 1.25, "前向：中间量", fontsize=10.5, color=C1, va="center")
    arrow((3.6, 1.25), (2.9, 1.25), C2)
    ax.text(3.72, 1.25, "反向：梯度", fontsize=10.5, color=C2, va="center")
    save_fig(fig, "matrix-calculus-graph")


def gradcheck():
    """梯度检查的相对误差随步长 h 的变化。"""
    def forward(params, X, Y):
        W1, b1, W2, b2 = params
        Z1 = X @ W1.T + b1
        H = np.maximum(Z1, 0)
        Z2 = H @ W2.T + b2
        Z2 = Z2 - Z2.max(axis=1, keepdims=True)
        logP = Z2 - np.log(np.exp(Z2).sum(axis=1, keepdims=True))
        return -(Y * logP).sum() / len(X), (Z1, H, np.exp(logP))

    def num_grad(f, x, h):
        g = np.zeros_like(x)
        for i in np.ndindex(x.shape):
            old = x[i]
            x[i] = old + h; fp = f(x)
            x[i] = old - h; fm = f(x)
            x[i] = old
            g[i] = (fp - fm) / (2 * h)
        return g

    rng = np.random.default_rng(0)
    n, d, h, c = 8, 5, 16, 3
    X = rng.standard_normal((n, d))
    Y = np.eye(c)[rng.integers(0, c, size=n)]
    params = [rng.standard_normal((h, d)) * 0.5, np.zeros(h), rng.standard_normal((c, h)) * 0.5, np.zeros(c)]
    _, (Z1, H, P) = forward(params, X, Y)
    d2 = (P - Y) / n
    gW1 = ((d2 @ params[2]) * (Z1 > 0)).T @ X

    hs = 10.0 ** np.linspace(-12, -1, 34)
    errs = []
    for hh in hs:
        g_num = num_grad(lambda _: forward(params, X, Y)[0], params[0], hh)
        errs.append(np.linalg.norm(gW1 - g_num) / (np.linalg.norm(gW1) + np.linalg.norm(g_num)))
    errs = np.array(errs)

    fig, ax = axes(6.6, 3.7)
    ax.loglog(hs, errs, "-o", color=C1, lw=1.6, ms=4)
    ax.text(3e-12, 8e-9, "舍入误差\n$\\propto 1/h$", color=INK, fontsize=11, ha="left")
    ax.text(1.5e-3, 5e-11, "截断误差\n$\\propto h^2$", color=INK, fontsize=11, ha="left")
    ax.annotate("跨过 ReLU 折点", (hs[-4], errs[-4]), (6e-10, 1.2e-2), color=C2, fontsize=11,
                arrowprops=dict(arrowstyle="->", color=C2))
    ax.axvline(1e-5, color=MUTED, lw=0.9, ls="--")
    ax.text(1.5e-5, 1.5e-5, "$h=10^{-5}$", color=MUTED, fontsize=10.5)
    ax.set_xlabel("步长 $h$", color=INK)
    ax.set_ylabel("相对误差", color=INK)
    ax.set_ylim(5e-12, 0.3)
    save_fig(fig, "matrix-calculus-gradcheck")
    return hs, errs


def main():
    graph()
    gradcheck()


if __name__ == "__main__":
    main()
