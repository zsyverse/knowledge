"""智能控制页面插图。

    .venv/bin/python scripts/control/fig_intelligent.py

输出到 docs/basics/control/images/intelligent/；INTELLIGENT_PREVIEW=<目录> 另存 PNG 预览。
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "linalg"))
import common as lc  # noqa: E402  复用线性代数模块的配色与样式
from common import C1, C2, C3, C4, INK, MUTED, GRID, plt, np, style  # noqa: E402
from intelligent_common import *  # noqa: E402,F403

OUT_DIR = lc.ROOT / "docs" / "basics" / "control" / "images" / "intelligent"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = OUT_DIR / f"{name}.svg"
    fig.savefig(p, transparent=True, bbox_inches="tight")
    prev = os.environ.get("INTELLIGENT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", p.relative_to(lc.ROOT))


def fuzzy_example():
    """左：输入 e 的隶属函数与 e=1 的模糊化；中：ec；右：输出削顶合成与重心。"""
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.3))
    x = np.linspace(-3, 3, 601)
    cols = {"N": C1, "Z": C3, "P": C2}
    for ax, val, name in ((axs[0], 1.0, "e"), (axs[1], -0.5, "ec")):
        style(ax)
        for k, p in IN.items():
            ax.plot(x, tri(x, *p), color=cols[k], lw=1.8, label=k)
            m = float(tri(val, *p))
            if m > 0:
                ax.plot([-3, val], [m, m], color=cols[k], lw=0.8, ls=":")
                ax.text(-2.95, m + 0.03, f"{m:.3g}" if m not in (2/3, 1/3, 1/6, 5/6) else
                        {2/3: "2/3", 1/3: "1/3", 1/6: "1/6", 5/6: "5/6"}[m], color=cols[k], fontsize=9)
        ax.axvline(val, color=INK, lw=1, ls="--")
        ax.set_title(f"输入 ${name}$ = {val:g} 的模糊化", fontsize=11, color=INK)
        ax.set_ylim(0, 1.12)
        ax.legend(frameon=False, fontsize=9, loc="upper center", ncol=3)
    ax = axs[2]
    style(ax)
    for k, p in OUT.items():
        ax.plot(U, tri(U, *p), color=MUTED, lw=0.8)
        ax.text(CENTER[k], 1.04, k, ha="center", color=MUTED, fontsize=9)
    cog, mu = mamdani(1.0, -0.5)
    ax.fill_between(U, mu, color=C4, alpha=0.35, lw=0)
    ax.plot(U, mu, color=C4, lw=1.6)
    ax.axvline(cog, color=C2, lw=1.4)
    ax.text(cog + 0.1, 0.8, f"重心 u≈{cog:.3f}", color=C2, fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_title("输出：各规则削顶后取并，再求重心", fontsize=11, color=INK)
    fig.tight_layout(w_pad=1.5)
    save(fig, "fuzzy-example")


def fuzzy_surface():
    """控制面 u(e, ec)：非线性，但关于原点对称。"""
    g = np.linspace(-3, 3, 61)
    Z = np.array([[mamdani(e, c)[0] for e in g] for c in g])
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    cs = ax.contourf(g, g, Z, levels=np.linspace(-3, 3, 25), cmap="RdBu_r")
    ax.contour(g, g, Z, levels=[-2, -1, 0, 1, 2], colors="white", linewidths=0.7)
    cb = fig.colorbar(cs, ax=ax, ticks=[-3, -1.5, 0, 1.5, 3])
    cb.set_label("控制量 u", color=MUTED)
    ax.plot(1, -0.5, "o", color="black", ms=5)
    ax.text(1.12, -0.75, "e=1, ec=−0.5", fontsize=9)
    ax.set_xlabel("误差 e", color=MUTED)
    ax.set_ylabel("误差变化率 ec", color=MUTED)
    ax.set_title("3×3 条规则得到的控制面", fontsize=11, color=INK)
    save(fig, "fuzzy-surface")


def ilc_fig():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.6))
    style(a)
    _, ys = ilc(0.5, 10)
    a.plot(T, REF, color=INK, lw=2.2, label="期望轨迹")
    for i, c in zip((0, 1, 3), (C2, C4, C1)):
        a.plot(T, ys[i], color=c, lw=1.4, ls="--" if i < 3 else "-", label=f"第 {i+1} 次运行")
    a.set_xlabel("时刻 t", color=MUTED)
    a.set_title("Γ=0.5：每次运行都比上次跟得更准", fontsize=11, color=INK)
    a.legend(frameon=False, fontsize=9)
    style(b)
    for g, c in zip((0.5, 1.0, 1.5, 2.2), (C1, C3, C4, C2)):
        errs, _ = ilc(g, 30)
        b.semilogy(np.arange(1, 31), errs, "o-", ms=3, color=c, lw=1.4,
                   label=f"Γ={g}, |1−ΓCB|={abs(1-g):.1f}")
    b.set_xlabel("迭代次数 k", color=MUTED)
    b.set_ylabel("最大跟踪误差", color=MUTED)
    b.set_title("收敛与否看 |1−ΓCB| 是否小于 1", fontsize=11, color=INK)
    b.legend(frameon=False, fontsize=9)
    fig.tight_layout(w_pad=2)
    save(fig, "ilc")


if __name__ == "__main__":
    fuzzy_example()
    fuzzy_surface()
    ilc_fig()
