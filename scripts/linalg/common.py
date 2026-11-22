"""线性代数笔记插图的公共设置。

所有插图用 matplotlib 绘制，输出为文字转路径、透明背景的 SVG，
放在 docs/basics/math/linalg/images/。运行方式：

    .venv/bin/python scripts/linalg/make_all.py          # 全部重画
    .venv/bin/python scripts/linalg/fig_vectors.py       # 只画某一章

环境变量 LINALG_PREVIEW=<目录> 时，额外输出白底 PNG 预览，方便检查。
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "basics" / "math" / "linalg" / "images"
OUT.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams.update(
    {
        "svg.fonttype": "path",
        "mathtext.fontset": "stix",
        "font.family": "sans-serif",
        "font.sans-serif": ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"],
        "axes.unicode_minus": False,
    }
)

# 与电路、控制两个模块的曲线图同一套颜色
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#8e5bd0"
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"


def axes(w=6.0, h=3.6):
    """普通曲线图：去掉上、右边框，浅色网格。"""
    fig, ax = plt.subplots(figsize=(w, h))
    style(ax)
    return fig, ax


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def plane(ax, xlim=(-3, 3), ylim=(-3, 3), ticks=True):
    """二维坐标平面：坐标轴过原点、等比例、整数网格。画向量和线性变换时用。"""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
        ax.spines[s].set_color(MUTED)
        ax.spines[s].set_linewidth(0.9)
    xs = [t for t in range(int(np.ceil(xlim[0])), int(np.floor(xlim[1])) + 1) if t != 0]
    ys = [t for t in range(int(np.ceil(ylim[0])), int(np.floor(ylim[1])) + 1) if t != 0]
    ax.set_xticks(xs if ticks else [])
    ax.set_yticks(ys if ticks else [])
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def vec(ax, v, color=C1, label=None, origin=(0, 0), lw=2.0, ls="-", label_ofs=(0.08, 0.08), fontsize=13, **kw):
    """从 origin 画到 origin+v 的箭头；label 写在箭头尖端旁（可用 $...$ 数学文本）。"""
    o = np.asarray(origin, dtype=float)
    p = o + np.asarray(v, dtype=float)
    ax.annotate(
        "", xy=p, xytext=o,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0, mutation_scale=14),
        **kw,
    )
    if label:
        ax.text(p[0] + label_ofs[0], p[1] + label_ofs[1], label, color=color, fontsize=fontsize)


def save_fig(fig, name: str) -> None:
    path = OUT / f"{name}.svg"
    fig.savefig(path, transparent=True, bbox_inches="tight")
    prev = os.environ.get("LINALG_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


__all__ = ["plt", "np", "axes", "style", "plane", "vec", "save_fig",
           "C1", "C2", "C3", "C4", "INK", "MUTED", "GRID", "OUT", "ROOT"]
