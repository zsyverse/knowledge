"""第 9 章「奇异值分解」的插图。"""
from common import *


def circle_to_ellipse():
    """A=[[2,0.4],[1,2.2]] = U Sigma V^T：单位圆依次经过 V^T、Sigma、U。"""
    r = 1 / np.sqrt(2)
    V = np.array([[r, -r], [r, r]])
    U = np.array([[0.6, -0.8], [0.8, 0.6]])
    S = np.diag([2 * np.sqrt(2), np.sqrt(2)])
    t = np.linspace(0, 2 * np.pi, 400)
    circle = np.vstack([np.cos(t), np.sin(t)])
    stages = [
        ("单位圆上的 $v_1,\\ v_2$", np.eye(2), ("$v_1$", "$v_2$")),
        ("乘 $V^{\\mathsf{T}}$：旋转，$v_i$ 转到坐标轴", V.T, ("$e_1$", "$e_2$")),
        ("乘 $\\Sigma$：沿坐标轴伸缩", S @ V.T, ("$\\sigma_1e_1$", "$\\sigma_2e_2$")),
        ("乘 $U$：再旋转，得到 $Av_i=\\sigma_iu_i$", U @ S @ V.T, ("$\\sigma_1u_1$", "$\\sigma_2u_2$")),
    ]
    ofs = [((0.1, 0.1), (-0.5, 0.12)), ((0.05, 0.15), (0.12, 0.05)),
           ((-0.75, 0.22), (0.15, 0.05)), ((0.12, 0.05), (-1.25, 0.12))]
    fig, axs = plt.subplots(2, 2, figsize=(7.4, 7.4))
    for ax, (title, M, labels), (o1, o2) in zip(axs.ravel(), stages, ofs):
        plane(ax, (-3.3, 3.3), (-3.3, 3.3))
        P = M @ circle
        ax.plot(P[0], P[1], color=INK, lw=1.3)
        vec(ax, M @ V[:, 0], C1, labels[0], label_ofs=o1)
        vec(ax, M @ V[:, 1], C2, labels[1], label_ofs=o2)
        ax.set_title(title, fontsize=11, color=INK, pad=8)
    fig.tight_layout()
    save_fig(fig, "svd-circle-to-ellipse")


def deep_product():
    """20 个 128x128 随机矩阵连乘后的奇异值（从大到小）。"""
    rng = np.random.default_rng(0)
    n, L = 128, 20

    def product(make):
        P = np.eye(n)
        for _ in range(L):
            P = make() @ P
        return np.linalg.svd(P, compute_uv=False)

    fig, ax = axes(6.4, 4.0)
    idx = np.arange(1, n + 1)
    for gain, c in zip((1.2, 1.0, 0.8), (C2, C1, C4)):
        s = product(lambda: gain * rng.standard_normal((n, n)) / np.sqrt(n))
        ax.semilogy(idx, s, color=c, lw=1.8, label=f"高斯初始化，方差 ${gain}^2/n$")

    def orth():
        Q, _ = np.linalg.qr(rng.standard_normal((n, n)))
        return Q

    ax.semilogy(idx, product(orth), color=C3, lw=2.2, label="正交初始化")
    ax.set_xlabel("奇异值序号 $i$", color=INK)
    ax.set_ylabel("连乘矩阵的奇异值 $\\sigma_i$", color=INK)
    ax.set_xlim(1, n)
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    save_fig(fig, "svd-deep-product")


def main():
    circle_to_ellipse()
    deep_product()


if __name__ == "__main__":
    main()
