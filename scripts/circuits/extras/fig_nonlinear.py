"""拓展·非线性电阻电路 插图（前缀 nl-）。"""
import numpy as np
from xcommon import (elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, wire, axes, plt,
                     OHM, C1, C2, C3, MUTED, INK, GRID)


def nonlin(d, p, q, label=None, loc="bot"):
    """非线性电阻：方框 + 斜线（竖直放置时）。"""
    e = elm.ResistorIEC().endpoints(p, q)
    if label:
        e.label(label, loc=loc)
    d.add(e)
    (x1, y1), (x2, y2) = p, q
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if x1 == x2:
        wire(d, (mx - 0.55, my - 0.75), (mx - 0.2, my - 0.75), (mx + 0.45, my + 0.75))
    else:
        wire(d, (mx - 0.75, my - 0.55), (mx - 0.75, my - 0.2), (mx + 0.75, my + 0.45))


def nl_types():
    fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.3))
    for ax in axs:
        for sd in ("top", "right"):
            ax.spines[sd].set_visible(False)
        for sd in ("left", "bottom"):
            ax.spines[sd].set_position("zero"); ax.spines[sd].set_color(MUTED)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel("$u$", loc="right", color=INK, fontsize=12)
        ax.set_ylabel("$i$", loc="top", rotation=0, color=INK, fontsize=12)
    x = np.linspace(0, 1, 300)
    y = 6 * x**3 - 7.2 * x**2 + 2.4 * x
    axs[0].plot(x, y, color=C1, lw=2); axs[0].set_title("压控型：$i=g(u)$", fontsize=12, color=INK)
    axs[0].set_ylim(-0.05, 1.25); axs[0].set_xlim(-0.05, 1.05)
    axs[1].plot(y, x, color=C2, lw=2); axs[1].set_title("流控型：$u=f(i)$", fontsize=12, color=INK)
    axs[1].set_xlim(-0.05, 1.25); axs[1].set_ylim(-0.05, 1.05)
    uu = np.linspace(-1, 0.75, 300)
    axs[2].plot(uu, (np.exp(uu * 6) - 1) / np.exp(4.5), color=C3, lw=2)
    axs[2].set_title("单调型", fontsize=12, color=INK)
    axs[2].set_ylim(-0.1, 1.05)
    fig.tight_layout()
    save_fig(fig, "nl-types")


def nl_ex():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$u_s$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3.2, 3.5)).label(f"$R_1=2{OHM}$"))
    dot(d, (3.2, 3.5)); dot(d, (3.2, 0)); text(d, (3.2, 3.95), "$a$")
    d.add(elm.Resistor().endpoints((3.2, 3.5), (3.2, 0)).label(f"$R_2=2{OHM}$", loc="bot"))
    cur(d, (3.2, 3.5), (6.8, 3.5), "$i$", loc="top", frac=0.6)
    nonlin(d, (6.8, 3.5), (6.8, 0), "$i=u^2$", loc="top")
    text(d, (7.8, 2.9), "$+$"); text(d, (7.8, 1.75), "$u$"); text(d, (7.8, 0.6), "$−$")
    wire(d, (0, 0), (6.8, 0))
    save(d, "nl-ex")


def nl_loadline():
    fig, ax = axes(5.2, 3.4)
    u = np.linspace(0, 3.2, 300)
    ax.plot(u, u ** 2, color=C1, lw=2, label="非线性电阻 $i=u^2$")
    ax.plot(u, 6 - u, color=C2, lw=2, label="负载线 $i=6-u$")
    ax.plot(u, 4 + 4 * (u - 2), color=MUTED, lw=1.2, ls="--", label="切线：斜率 $1/r_d=4\\,\\mathrm{S}$")
    ax.plot([0, 2], [0, 4], color=C3, lw=1.2, ls=":", label="割线：斜率 $1/R=2\\,\\mathrm{S}$")
    ax.plot([2], [4], "o", ms=6, color=INK)
    ax.text(2.07, 3.5, "$Q(2\\,\\mathrm{V},\\,4\\,\\mathrm{A})$", fontsize=10, color=INK)
    ax.set_xlim(0, 3.2); ax.set_ylim(0, 7)
    ax.set_xlabel("$u$/V", color=INK, loc="right"); ax.set_ylabel("$i$/A", color=INK)
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    save_fig(fig, "nl-loadline")


def nl_pwl():
    fig, ax = axes(5.2, 3.2)
    u = np.linspace(-0.5, 4.2, 400)
    ax.plot(u, np.where(u < 1, 0, (u - 1) / 0.5), color=C1, lw=2.2, label="分段线性特性")
    ax.plot(u, 4 - u, color=C2, lw=1.6, label="$U_{oc}=4\\,\\mathrm{V}$ 的负载线")
    ax.plot(u, 0.5 - u, color=C3, lw=1.6, label="$U_{oc}=0.5\\,\\mathrm{V}$ 的负载线")
    ax.plot([2], [2], "o", ms=6, color=INK); ax.text(2.1, 2.2, "$(2,\\,2)$", fontsize=10, color=INK)
    ax.plot([0.5], [0], "o", ms=6, color=INK); ax.text(0.55, 0.25, "$(0.5,\\,0)$", fontsize=10, color=INK)
    ax.text(0.0, -0.75, "段①：$i=0$", fontsize=10, color=INK)
    ax.text(2.9, 2.5, "段②：$u=1+0.5i$", fontsize=10, color=INK)
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlim(-0.5, 4.2); ax.set_ylim(-1, 6.2)
    ax.set_xlabel("$u$/V", color=INK, loc="right"); ax.set_ylabel("$i$/A", color=INK)
    ax.legend(fontsize=9, frameon=False, loc="upper left")
    save_fig(fig, "nl-pwl")


def nl_small():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$\\Delta u_{oc}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3.4, 3.5)).label(f"$R_{{eq}}=1{OHM}$"))
    cur(d, (3.4, 3.5), (5.2, 3.5), "$\\Delta i$", loc="top")
    d.add(elm.Resistor().endpoints((5.2, 3.5), (5.2, 0)).label(f"$r_d=0.25{OHM}$", loc="top"))
    text(d, (6.0, 2.9), "$+$"); text(d, (6.0, 1.75), "$\\Delta u$"); text(d, (6.0, 0.6), "$−$")
    wire(d, (0, 0), (5.2, 0))
    save(d, "nl-small")


def nl_x5():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 2.2), "$3\\,\\mathrm{V}$", loc="top")
    d.add(elm.SourceSin().endpoints((0, 2.2), (0, 4.6)).label("$0.1\\sin\\omega t\\ \\mathrm{V}$", loc="top")
          .label(("−", "", "+"), loc="bot", ofst=0.1))
    d.add(elm.Resistor().endpoints((0, 4.6), (3.6, 4.6)).label(f"$R=1{OHM}$"))
    nonlin(d, (3.6, 4.6), (3.6, 0), "$i=2u^2$", loc="top")
    arrow(d, (4.4, 3.8), (4.4, 2.8), "$i$", loc="bot")
    text(d, (5.4, 3.9), "$+$"); text(d, (5.4, 2.3), "$u$"); text(d, (5.4, 0.7), "$−$")
    wire(d, (0, 0), (3.6, 0))
    save(d, "nl-x5")


if __name__ == "__main__":
    nl_types(); nl_ex(); nl_loadline(); nl_pwl(); nl_small(); nl_x5()
