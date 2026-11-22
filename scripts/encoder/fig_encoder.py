"""「编码器」一文的插图：光电编码器结构、A/B 正交波形、二进制与格雷码码盘。

    .venv/bin/python scripts/encoder/fig_encoder.py

输出文字转路径、透明背景的 SVG 到 docs/basics/wiki/images/encoder/。
环境变量 ENCODER_PREVIEW=<目录> 时另存白底 PNG 预览。
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Wedge  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "basics" / "wiki" / "images" / "encoder"
OUT.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams.update({
    "svg.fonttype": "path",
    "mathtext.fontset": "stix",
    "font.family": "sans-serif",
    "font.sans-serif": ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
})
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#8e5bd0"
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"


def save_fig(fig, name):
    path = OUT / f"{name}.svg"
    fig.savefig(path, transparent=True, bbox_inches="tight")
    prev = os.environ.get("ENCODER_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def optical():
    """左：侧视结构（LED → 码盘 → 固定光栅 → 光电元件）；右：码盘正视。"""
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw={"width_ratios": [1.45, 1]})
    for ax in (a, b):
        ax.set_aspect("equal")
        ax.axis("off")

    # 侧视
    a.set_xlim(0, 10)
    a.set_ylim(-0.6, 4.6)
    a.add_patch(Rectangle((2.6, 1.75), 1.8, 0.3, color=MUTED))         # 转轴（从左侧电机伸入）
    a.text(3.5, 1.6, "转轴（接电机）", ha="center", va="top", color=MUTED, fontsize=10)
    # 码盘（侧视：竖直薄片，带透光缝）
    a.add_patch(Rectangle((4.4, 0.0), 0.5, 4.2, fc="none", ec=INK, lw=1.2))
    for y in np.arange(2.6, 4.2, 0.3):
        a.add_patch(Rectangle((4.4, y), 0.5, 0.15, color=C1, alpha=0.35))
    a.text(4.65, 4.35, "码盘（随轴转）", ha="center", color=C1, fontsize=10)
    # 固定光栅
    a.add_patch(Rectangle((5.6, 2.5), 0.25, 1.6, fc="none", ec=INK, lw=1.0))
    for y in np.arange(2.6, 4.1, 0.3):
        a.add_patch(Rectangle((5.6, y), 0.25, 0.15, color=C1, alpha=0.35))
    a.text(5.75, 2.3, "固定光栅", ha="center", va="top", color=MUTED, fontsize=10)
    # LED 与光电元件
    a.add_patch(Rectangle((1.2, 2.9), 0.9, 0.7, fc=C2, ec="none", alpha=0.85))
    a.text(1.65, 2.7, "LED", ha="center", va="top", color=C2, fontsize=11)
    a.add_patch(Rectangle((7.3, 2.9), 0.9, 0.7, fc=C3, ec="none", alpha=0.85))
    a.text(7.75, 2.7, "光电元件", ha="center", va="top", color=C3, fontsize=11)
    for dy in (-0.15, 0.0, 0.15):
        a.add_patch(FancyArrowPatch((2.2, 3.25 + dy), (7.2, 3.25 + dy), arrowstyle="-|>",
                                    mutation_scale=9, color=C2, lw=0.9, alpha=0.6))
    # 输出脉冲
    t = np.linspace(0, 1.8, 400)
    a.plot(7.3 + t, 0.6 + 0.5 * (np.sin(2 * np.pi * t / 0.45) > 0), color=C3, lw=1.6)
    a.text(8.2, 1.35, "明暗 → 方波", ha="center", color=C3, fontsize=10)
    a.set_title("侧视：缝对齐透光，错开遮光", fontsize=11, color=INK)

    # 正视码盘
    b.set_xlim(-1.3, 1.3)
    b.set_ylim(-1.3, 1.3)
    b.add_patch(Circle((0, 0), 1.15, fc="none", ec=INK, lw=1.2))
    n = 24
    for k in range(n):
        th = 360 / n * k
        b.add_patch(Wedge((0, 0), 1.08, th, th + 360 / n / 2, width=0.22, color=C1, alpha=0.75))
    b.add_patch(Wedge((0, 0), 0.75, 85, 95, width=0.14, color=C2, alpha=0.9))
    b.annotate("Z 相：每圈一个缝", (0.0, 0.62), (0.0, -0.4), ha="center", fontsize=9.5, color=C2,
               arrowprops=dict(arrowstyle="-", color=C2, lw=0.8))
    b.add_patch(Circle((0, 0), 0.12, color=MUTED))
    b.set_title(f"正视：{n} 线增量码盘", fontsize=11, color=INK)
    fig.tight_layout()
    save_fig(fig, "optical")


def quadrature():
    """A/B 相差 90°：正转 A 超前 B，反转 B 超前 A；Z 每圈一个脉冲。"""
    fig, axs = plt.subplots(3, 1, figsize=(8.6, 3.6), sharex=True)
    x = np.linspace(0, 8, 2000)
    sq = lambda ph: (np.mod(x - ph, 2) < 1).astype(float)
    # 前半正转（A 超前），后半反转（B 超前）
    A = np.where(x < 4, sq(0), sq(0.5))
    B = np.where(x < 4, sq(0.5), sq(0))
    Z = ((x > 1.0) & (x < 1.5)).astype(float)
    for ax, y, c, lab in zip(axs, (A, B, Z), (C1, C2, C3), ("A", "B", "Z")):
        ax.plot(x, y, color=c, lw=1.8, drawstyle="steps-post")
        ax.set_ylim(-0.25, 1.35)
        ax.set_yticks([])
        ax.set_ylabel(lab, rotation=0, labelpad=12, color=c, fontsize=12, va="center")
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.axvline(4, color=MUTED, lw=0.8, ls="--")
    axs[0].text(2, 1.2, "正转：A 先上升，B 晚 1/4 周期", ha="center", color=INK, fontsize=10)
    axs[0].text(6, 1.2, "反转：B 先上升，A 晚 1/4 周期", ha="center", color=INK, fontsize=10)
    axs[-1].set_xticks([])
    axs[-1].set_xlabel("时间", color=MUTED, fontsize=10)
    fig.tight_layout(h_pad=0.2)
    save_fig(fig, "quadrature")


def gray_disks():
    """3 位绝对式码盘：自然二进制 vs 格雷码。内圈为最高位。"""
    fig, axs = plt.subplots(1, 2, figsize=(8.2, 4.2))
    codes = {
        "自然二进制": [k for k in range(8)],
        "格雷码": [k ^ (k >> 1) for k in range(8)],
    }
    for ax, (name, seq) in zip(axs, codes.items()):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        for k, c in enumerate(seq):
            th0 = 90 - 45 * (k + 1)
            for bit in range(3):                       # bit 2 = 最高位，放内圈
                r_out = 0.5 + 0.3 * (3 - bit)
                on = (c >> bit) & 1
                ax.add_patch(Wedge((0, 0), r_out, th0, th0 + 45, width=0.3,
                                   fc=C1 if on else "white", ec=MUTED, lw=0.6, alpha=0.85 if on else 1))
            mid = np.deg2rad(th0 + 22.5)
            ax.text(1.3 * np.cos(mid), 1.3 * np.sin(mid), format(c, "03b"), ha="center", va="center",
                    fontsize=9.5, color=INK, family="monospace")
        ax.plot([0, 0], [0.45, 1.45], color=C2, lw=1.4)
        ax.text(0.06, 1.38, "读头", color=C2, fontsize=9.5)
        changed = sum(bin(seq[k] ^ seq[(k + 1) % 8]).count("1") for k in range(8))
        worst = max(bin(seq[k] ^ seq[(k + 1) % 8]).count("1") for k in range(8))
        ax.set_title(f"{name}：相邻扇区最多 {worst} 位同时翻转", fontsize=11, color=INK)
    fig.tight_layout()
    save_fig(fig, "gray-disks")


if __name__ == "__main__":
    optical()
    quadrature()
    gray_disks()
