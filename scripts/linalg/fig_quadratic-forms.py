"""第 8 章「对称矩阵、二次型与正定性」的插图。"""
from common import *


def _grid(xlim, ylim, n=401):
    xs = np.linspace(*xlim, n)
    ys = np.linspace(*ylim, n)
    return np.meshgrid(xs, ys)


def ellipse():
    """q(x)=5x1^2+6x1x2+5x2^2 的等高线：主轴沿特征向量，半轴长 sqrt(c/lambda)。"""
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    lim = (-2.7, 2.7)
    plane(ax, lim, lim)
    X, Y = _grid(lim, lim)
    Z = 5 * X**2 + 6 * X * Y + 5 * Y**2
    ax.contour(X, Y, Z, levels=[2], colors=MUTED, linewidths=0.9, linestyles="--")
    ax.contour(X, Y, Z, levels=[8], colors=C1, linewidths=2.0)
    r = 1 / np.sqrt(2)
    vec(ax, (r, r), C2, None)
    vec(ax, (2 * r, -2 * r), C3, None)
    ax.text(0.95, 1.25, "$q_1$ 方向：$\\lambda_1=8$\n半轴 $\\sqrt{8/8}=1$", color=C2, fontsize=11, va="bottom")
    ax.text(1.0, -1.95, "$q_2$ 方向：$\\lambda_2=2$\n半轴 $\\sqrt{8/2}=2$", color=C3, fontsize=11, va="top", ha="center")
    ax.text(-2.6, 1.75, "$x^{\\mathsf{T}}Ax=8$", color=C1, fontsize=12)
    ax.text(-0.2, -0.62, "$=2$", color=MUTED, fontsize=10, ha="right")
    save_fig(fig, "quadratic-forms-ellipse")


def three_types():
    """正定、半正定、不定三种二次型的等高线。"""
    fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.7))
    lim = (-2.2, 2.2)
    X, Y = _grid(lim, lim)
    cases = [
        ("正定：$2x_1^2+x_2^2$\n原点是唯一的最低点", 2 * X**2 + Y**2),
        ("半正定：$(x_1+x_2)^2$\n直线 $x_1+x_2=0$ 上处处最低", (X + Y) ** 2),
        ("不定：$x_1^2-x_2^2$\n原点是鞍点（橙线上 $q<0$）", X**2 - Y**2),
    ]
    for ax, (title, Z) in zip(axs, cases):
        plane(ax, lim, lim, ticks=False)
        ax.contour(X, Y, Z, levels=[0.5, 1.5, 3, 5, 8], colors=C1, linewidths=1.2)
        ax.contour(X, Y, Z, levels=[-3, -1.5, -0.5], colors=C2, linewidths=1.2, linestyles="-")
        ax.set_title(title, fontsize=11, color=INK, pad=8)
    axs[1].plot([-2.2, 2.2], [2.2, -2.2], color=C3, lw=2.0)
    for s in (1, -1):
        axs[2].plot([-2.2, 2.2], [-2.2 * s, 2.2 * s], color=MUTED, lw=0.9, ls="--")
    axs[0].plot([0], [0], "o", color=C3, ms=6)
    axs[2].plot([0], [0], "o", color=C3, ms=6)
    save_fig(fig, "quadratic-forms-three-types")


def gd_zigzag():
    """f = (x1^2 + kappa*x2^2)/2 上的梯度下降，步长取 2/(lambda_max+lambda_min)。"""
    fig, axs = plt.subplots(2, 1, figsize=(7.0, 5.0))
    xlim, ylim = (-1.5, 11.0), (-2.4, 2.4)
    X, Y = _grid(xlim, ylim)
    for ax, kappa in zip(axs, (1.0, 20.0)):
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        style(ax)
        ax.grid(False)
        Z = 0.5 * (X**2 + kappa * Y**2)
        ax.contour(X, Y, Z, levels=[0.5, 2, 6, 12, 20, 32, 50], colors=MUTED, linewidths=0.7)
        H = np.diag([1.0, kappa])
        eta = 2 / (1 + kappa)
        x = np.array([10.0, 1.0])
        path = [x.copy()]
        for _ in range(40):
            x = x - eta * (H @ x)
            path.append(x.copy())
        path = np.array(path)
        ax.plot(path[:, 0], path[:, 1], color=C2, lw=1.4, marker="o", ms=3.5)
        ax.plot([0], [0], "*", color=C3, ms=12)
        steps = "1 步到达最低点" if kappa == 1 else "每步只收缩到 19/21，来回振荡"
        ax.set_title(f"$\\kappa={kappa:g}$，$\\eta={'1' if kappa == 1 else '2/21'}$：{steps}", fontsize=11, color=INK, pad=6)
        ax.set_ylabel("$x_2$", color=INK)
    axs[1].set_xlabel("$x_1$", color=INK)
    fig.tight_layout()
    save_fig(fig, "quadratic-forms-gd-zigzag")


def main():
    ellipse()
    three_types()
    gd_zigzag()


if __name__ == "__main__":
    main()
