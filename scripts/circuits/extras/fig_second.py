"""拓展·二阶电路与卷积积分 插图（前缀 so-）。"""
import numpy as np
from xcommon import (elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, isrc, wire, axes, plt,
                     OHM, C1, C2, C3, MUTED, INK, GRID)


def so_series():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$U_s$", loc="top")
    d.add(elm.Switch(action="close").endpoints((0, 3.5), (2.4, 3.5)).label("$S\\ (t=0)$"))
    d.add(elm.Resistor().endpoints((2.4, 3.5), (5.0, 3.5)).label("$R$"))
    d.add(elm.Inductor2(loops=3).endpoints((5.0, 3.5), (8.0, 3.5)).label("$L$"))
    arrow(d, (5.6, 2.85), (7.4, 2.85), "$i$", loc="bot")
    d.add(elm.Capacitor().endpoints((8.0, 3.5), (8.0, 0)).label("$C$", loc="top").label(("+", "$u_C$", "−"), loc="bot"))
    wire(d, (0, 0), (8.0, 0))
    save(d, "so-series")


def so_parallel():
    d = new_drawing()
    isrc(d, (0, 0), (0, 3.5), "$I_s\\,\\varepsilon(t)$", loc="top")
    xs = [2.6, 5.0, 7.6]
    wire(d, (0, 3.5), (xs[-1], 3.5)); wire(d, (0, 0), (xs[-1], 0))
    d.add(elm.Resistor().endpoints((xs[0], 3.5), (xs[0], 0)).label("$R$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((xs[1], 3.5), (xs[1], 0)).label("$L$", loc="bot"))
    arrow(d, (xs[1] - 0.6, 2.8), (xs[1] - 0.6, 1.4), "$i_L$", loc="top")
    d.add(elm.Capacitor().endpoints((xs[2], 3.5), (xs[2], 0)).label("$C$", loc="top"))
    for x in xs[:2]:
        dot(d, (x, 3.5)); dot(d, (x, 0))
    text(d, (xs[2] + 1.0, 3.0), "$+$"); text(d, (xs[2] + 1.0, 1.75), "$u$"); text(d, (xs[2] + 1.0, 0.5), "$−$")
    save(d, "so-parallel")


def so_conv():
    fig, axs = plt.subplots(3, 1, figsize=(5.4, 6.6))
    for ax in axs:
        for sp_ in ("top", "right"):
            ax.spines[sp_].set_visible(False)
        for sp_ in ("left", "bottom"):
            ax.spines[sp_].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    tau = np.linspace(-0.5, 3.5, 800)
    # (a) e(τ) 与 h(τ)
    ax = axs[0]
    ax.plot(tau, ((tau >= 0) & (tau < 1)).astype(float), color=C2, lw=2, label="$e(\\tau)$")
    ax.plot(tau[tau >= 0], np.exp(-tau[tau >= 0]), color=C1, lw=2, label="$h(\\tau)$")
    ax.set_xlabel("$\\tau$", color=INK, loc="right"); ax.legend(fontsize=9, frameon=False)
    ax.set_title("① 激励与冲激响应", fontsize=10, color=INK)
    ax.set_ylim(-0.1, 1.25)
    # (b) 翻转平移 h(t−τ)，t = 1.6
    ax = axs[1]
    t0 = 1.6
    e = ((tau >= 0) & (tau < 1)).astype(float)
    hf = np.where(tau <= t0, np.exp(-(t0 - tau)), 0)
    ax.plot(tau, e, color=C2, lw=2)
    ax.plot(tau, hf, color=C1, lw=2, label="$h(t-\\tau)$")
    ax.fill_between(tau, 0, e * hf, color=C3, alpha=0.35, lw=0, label="乘积的面积 $=r(t)$")
    ax.axvline(t0, color=MUTED, lw=0.8, ls="--"); ax.text(t0 + 0.05, 1.12, "$\\tau=t=1.6$", fontsize=9, color=INK)
    ax.set_xlabel("$\\tau$", color=INK, loc="right"); ax.legend(fontsize=9, frameon=False, loc="upper right")
    ax.set_title("② 翻转、平移到 $t$、相乘", fontsize=10, color=INK)
    ax.set_ylim(-0.1, 1.25)
    # (c) r(t)
    ax = axs[2]
    tt = np.linspace(0, 3.5, 500)
    r = np.where(tt < 1, 1 - np.exp(-tt), (np.e - 1) * np.exp(-tt))
    ax.plot(tt, r, color=C3, lw=2)
    ax.plot([t0], [(np.e - 1) * np.exp(-t0)], "o", ms=5, color=C3)
    ax.plot([1], [1 - np.exp(-1)], "o", ms=4, color=MUTED)
    ax.text(1.08, 0.64, "$1-e^{-1}\\approx0.632$", fontsize=9, color=INK)
    ax.set_xlabel("$t$", color=INK, loc="right")
    ax.set_title("③ 对每个 $t$ 求面积得 $r(t)$", fontsize=10, color=INK)
    ax.set_ylim(-0.05, 0.8)
    fig.tight_layout()
    save_fig(fig, "so-conv")


def so_x2_wave():
    fig, ax = axes(5.4, 2.8)
    tt = np.linspace(0, 2, 600)
    u = 10 - 10 * np.exp(-3 * tt) * (np.cos(4 * tt) + 0.75 * np.sin(4 * tt))
    ax.plot(tt, u, color=C1, lw=2)
    ax.axhline(10, color=C2, lw=1, ls="--")
    tp = np.pi / 4; up = 10 + 10 * np.exp(-3 * tp)
    ax.plot([tp], [up], "o", ms=5, color=C1)
    ax.text(tp + 0.05, up + 0.25, "$t=\\pi/4$，$u_C\\approx10.95\\,\\mathrm{V}$", fontsize=10, color=INK)
    ax.set_ylim(0, 12.2); ax.set_xlim(0, 2)
    ax.set_xlabel("$t$/s", color=INK, loc="right"); ax.set_ylabel("$u_C$/V", color=INK)
    save_fig(fig, "so-x2-wave")


if __name__ == "__main__":
    so_series(); so_parallel(); so_conv(); so_x2_wave()
