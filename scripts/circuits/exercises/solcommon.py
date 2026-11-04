"""解析插图（images/ex/sol/）的公共工具：在 excommon 的基础上增加
- ssave / sfig：保存到 images/ex/sol/；
- first_order_wave：一阶电路三要素波形（标出 f(0_-)、f(0_+)、f(∞)、τ 和 t=0 处切线）；
- 相量图工具 phasor_axes / phasor / angle_arc。

各 sol_*.py 只依赖这里和 excommon，生成方式与题图相同（make_all.py 一并运行）。
"""
from __future__ import annotations

import numpy as np
from matplotlib.ticker import FormatStrFormatter

from excommon import (SOL, elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, isrc,  # noqa: F401
                      ac_src, pdot, m_arrow, wire, plt, OHM, ARW)

C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#9b59b6"
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"


def ssave(d, name):
    save(d, name, out=SOL)


def sfig(fig, name):
    save_fig(fig, name, out=SOL)


def note(d, xy, s, **kw):
    """图中说明文字（灰色小字）。"""
    kw.setdefault("halign", "center")
    kw.setdefault("valign", "center")
    d.add(elm.Label().at(xy).label(s, color=MUTED, fontsize=12, **kw))


def open_end(d, xy):
    dot(d, xy, True)


# ---------------------------------------------------------------- 波形
def axes(w=5.6, h=3.0):
    fig, ax = plt.subplots(figsize=(w, h))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%g"))
    return fig, ax


def first_order_wave(name, f0p, finf, tau, ylab, unit, f0m=None, tmax=None, fmt="{:g}",
                     extra=None, tunit="s", w=5.6, h=3.0, zero=True):
    """f(t)=f(∞)+[f(0+)-f(∞)]e^{-t/τ}。f0m 给出时画出 t<0 的水平段（换路前稳态值）。
    extra(ax) 可追加内容。"""
    fig, ax = axes(w, h)
    tmax = tmax or 5 * tau
    t = np.linspace(0, tmax, 400)
    f = finf + (f0p - finf) * np.exp(-t / tau)
    tl = -0.18 * tmax
    vals = [f0p, finf] + ([f0m] if f0m is not None else []) + ([0] if zero else [])
    lo, hi = min(vals), max(vals)
    pad = 0.12 * (hi - lo or 1)
    ax.set_xlim(tl, tmax); ax.set_ylim(lo - pad, hi + pad)
    if zero:
        ax.axhline(0, color=MUTED, lw=0.8)
    ax.axvline(0, color=MUTED, lw=0.8)
    if f0m is not None:
        ax.plot([tl, 0], [f0m, f0m], color=C1, lw=2)
        if abs(f0m - f0p) > 1e-9:
            ax.plot([0, 0], [f0m, f0p], color=C1, lw=1, ls=":")
            ax.plot([0], [f0m], "o", ms=5, mfc="white", mec=C1)
    ax.plot(t, f, color=C1, lw=2)
    ax.plot([0], [f0p], "o", ms=5, color=C1)
    ax.axhline(finf, color=C2, lw=1, ls="--")
    # 切线：从 (0,f0p) 指向 (τ, f∞)
    ax.plot([0, tau], [f0p, finf], color=MUTED, lw=1, ls="--")
    ax.plot([tau, tau], [finf, finf + (f0p - finf) * np.exp(-1)], color=MUTED, lw=0.8, ls=":")
    ax.plot([tau], [finf + (f0p - finf) * np.exp(-1)], "o", ms=4, color=MUTED)
    ax.set_xticks([0, tau] + [k * tau for k in range(2, int(tmax / tau) + 1)],
                  ["0", "$\\tau$"] + [f"${k}\\tau$" for k in range(2, int(tmax / tau) + 1)])
    yt = sorted({round(v, 9) for v in vals})
    ax.set_yticks(yt, [fmt.format(v) for v in yt])
    ax.set_xlabel(f"$t$", color=INK, loc="right")
    ax.set_ylabel(f"{ylab}/{unit}" if unit else ylab, color=INK)
    if extra:
        extra(ax)
    sfig(fig, name)


# ---------------------------------------------------------------- 相量图
def phasor_axes(xlim, ylim, size=4.4):
    w = size
    h = size * (ylim[1] - ylim[0]) / (xlim[1] - xlim[0])
    fig, ax = plt.subplots(figsize=(w, max(h, 1.6)))
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


def phasor(ax, z, color, label=None, xy=None, start=0j, lw=2, ls="-", fs=12):
    z = complex(z); start = complex(start)
    ax.annotate("", xy=((z + start).real, (z + start).imag), xytext=(start.real, start.imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, mutation_scale=15,
                                shrinkA=0, shrinkB=0))
    if label:
        if xy is None:
            e = z + start
            xy = (e.real, e.imag)
        ax.text(xy[0], xy[1], label, color=INK, fontsize=fs, ha="center", va="center")


def angle_arc(ax, a1, a2, r, label=None, xy=None, color=MUTED, center=0j, fs=11):
    """从角度 a1 到 a2（度）的圆弧。"""
    th = np.radians(np.linspace(a1, a2, 60))
    ax.plot(center.real + r * np.cos(th), center.imag + r * np.sin(th), color=color, lw=1)
    if label:
        if xy is None:
            m = np.radians((a1 + a2) / 2)
            xy = (center.real + 1.35 * r * np.cos(m), center.imag + 1.35 * r * np.sin(m))
        ax.text(*xy, label, color=INK, fontsize=fs, ha="center", va="center")
