"""第 7 章「特征值与特征向量」的插图。"""
from common import *


def directions():
    """A=[[1,2],[1,0]]：一般向量被转了方向，特征向量仍落在原来的直线上。"""
    A = np.array([[1.0, 2.0], [1.0, 0.0]])
    x, v1, v2 = np.array([0.0, 1.0]), np.array([2.0, 1.0]), np.array([1.0, -1.0])
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 3.9))
    for ax, title in zip(axs, ("变换前", "变换后（乘 $A$）")):
        plane(ax, (-2.3, 4.9), (-1.9, 2.9))
        t = np.array([-5.0, 5.0])
        ax.plot(t * v1[0], t * v1[1], color=C1, lw=0.9, ls=":")
        ax.plot(t * v2[0], t * v2[1], color=C2, lw=0.9, ls=":")
        ax.set_title(title, fontsize=12, color=INK, pad=8)
    ax = axs[0]
    vec(ax, v1, C1, "$v_1$", label_ofs=(0.05, 0.15))
    vec(ax, v2, C2, "$v_2$", label_ofs=(0.2, 0.02))
    vec(ax, x, C3, "$x$", label_ofs=(0.12, -0.05))
    ax = axs[1]
    vec(ax, A @ v1, C1, "$Av_1=2v_1$", label_ofs=(-1.45, 0.3))
    vec(ax, A @ v2, C2, "$Av_2=-v_2$", label_ofs=(-1.25, -0.75))
    vec(ax, A @ x, C3, "$Ax$", label_ofs=(-0.15, 0.15))
    vec(ax, x, C3, None, lw=1.0, ls="--")
    save_fig(fig, "eigen-directions")


def gd_stability():
    """f = x^T H x / 2，H=[[3,1],[1,3]]（特征值 4 和 2）：学习率超过 2/4 就发散。"""
    H = np.array([[3.0, 1.0], [1.0, 3.0]])
    fig, ax = axes(5.6, 3.8)
    labels = {
        0.1: r"$\eta=0.1$",
        0.4: r"$\eta=0.4$",
        0.5: r"$\eta=0.5=2/\lambda_{\max}$（临界）",
        0.6: r"$\eta=0.6$（发散）",
    }
    for (eta, lab), c in zip(labels.items(), (C1, C3, C4, C2)):
        x = np.array([1.0, 0.0])
        norms = [np.linalg.norm(x)]
        for _ in range(30):
            x = x - eta * (H @ x)
            norms.append(np.linalg.norm(x))
        ax.semilogy(norms, color=c, lw=1.8, marker="o", ms=3, label=lab)
    ax.set_xlabel("迭代步数 $k$", color=INK)
    ax.set_ylabel(r"$\Vert x_k\Vert$", color=INK)
    ax.set_xlim(0, 30)
    ax.set_ylim(1e-8, 1e5)
    ax.legend(frameon=False, fontsize=10, loc="center left", bbox_to_anchor=(1.0, 0.5))
    save_fig(fig, "eigen-gd-stability")


def rnn_gradient():
    """线性 RNN 反传 k 步后的梯度范数：谱半径 0.9 / 1.0 / 1.1。"""
    rng = np.random.default_rng(0)
    n = 64
    W0 = rng.standard_normal((n, n)) / np.sqrt(n)
    rho0 = np.abs(np.linalg.eigvals(W0)).max()
    g = rng.standard_normal(n)
    g /= np.linalg.norm(g)
    ks = np.arange(0, 101)
    fig, ax = axes(6.4, 3.8)
    for rho, c in zip((1.1, 1.0, 0.9), (C2, C4, C1)):
        W = W0 * (rho / rho0)
        v, norms = g.copy(), [1.0]
        for _ in ks[1:]:
            v = W.T @ v
            norms.append(np.linalg.norm(v))
        ax.semilogy(ks, norms, color=c, lw=1.9, label=rf"$\rho(W)={rho}$")
        ax.semilogy(ks, rho ** ks, color=c, lw=0.9, ls="--")
    ax.plot([], [], color=MUTED, lw=0.9, ls="--", label=r"参考线 $\rho^k$")
    ax.set_xlabel("反向传播经过的时间步数 $k$", color=INK)
    ax.set_ylabel("梯度范数", color=INK)
    ax.set_xlim(0, 100)
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    save_fig(fig, "eigen-rnn-gradient")


def main():
    directions()
    gd_stability()
    rnn_gradient()


if __name__ == "__main__":
    main()
