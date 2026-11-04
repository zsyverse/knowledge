"""拓展·运算法 插图（前缀 lp-）。运算电路中的阻抗一律画成方框（ResistorIEC）。"""
import numpy as np
from xcommon import (elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, isrc, wire, plt,
                     OHM, C1, C2, C3, MUTED, INK, GRID)
from common import vsrc_h

Z = elm.ResistorIEC


def sw(d, p, q, action, label="$S\\ (t=0)$", loc="top"):
    d.add(elm.Switch(action=action).endpoints(p, q).label(label, loc=loc))


def _head(d, x, yt, yb, title):
    dot(d, (x, yt), True); dot(d, (x, yb), True)
    cur(d, (x, yt + 1.2), (x, yt), "$I(s)$", loc="bot")
    dot(d, (x, yt + 1.2), True)
    text(d, (x - 1.0, yt + 1.0), "$+$"); text(d, (x - 1.0, (yt + yb) / 2), "$U(s)$"); text(d, (x - 1.0, yb + 0.1), "$−$")
    text(d, (x + 1.0, yb - 1.0), title, fontsize=14)


def lp_model_L():
    d = new_drawing()
    yt, yb = 5.0, 0.0
    x = 0
    d.add(Z().endpoints((x, yt), (x, 2.5)).label("$sL$", loc="bot"))
    vsrc(d, (x, 2.5), (x, yb), "", loc="bot")
    text(d, (x + 1.3, 1.25), "$Li(0_-)$")
    _head(d, x, yt, yb, "串联形式")
    x = 6.0
    wire(d, (x, yt), (x + 2.2, yt)); wire(d, (x, yb), (x + 2.2, yb))
    d.add(Z().endpoints((x, yt), (x, yb)).label("$sL$", loc="bot"))
    isrc(d, (x + 2.2, yt), (x + 2.2, yb), "", loc="bot")
    text(d, (x + 3.3, 2.5), "$\\dfrac{i(0_-)}{s}$")
    dot(d, (x, yt)); dot(d, (x, yb))
    _head(d, x, yt, yb, "并联形式")
    save(d, "lp-model-L")


def lp_model_C():
    d = new_drawing()
    yt, yb = 5.0, 0.0
    x = 0
    d.add(Z().endpoints((x, yt), (x, 2.5)).label("$\\dfrac{1}{sC}$", loc="bot"))
    vsrc(d, (x, yb), (x, 2.5), "", loc="bot")
    text(d, (x + 1.35, 1.25), "$\\dfrac{u(0_-)}{s}$")
    _head(d, x, yt, yb, "串联形式")
    x = 6.0
    wire(d, (x, yt), (x + 2.2, yt)); wire(d, (x, yb), (x + 2.2, yb))
    d.add(Z().endpoints((x, yt), (x, yb)).label("$\\dfrac{1}{sC}$", loc="bot"))
    isrc(d, (x + 2.2, yb), (x + 2.2, yt), "", loc="bot")
    text(d, (x + 3.6, 2.5), "$Cu(0_-)$")
    dot(d, (x, yt)); dot(d, (x, yb))
    _head(d, x, yt, yb, "并联形式")
    save(d, "lp-model-C")


def lp_ex():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$10\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (3, 4)).label(f"$R_1=2{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((3, 4), (6.5, 4)).label("$1\\,\\mathrm{H}$"))
    arrow(d, (3.8, 3.35), (5.6, 3.35), "$i$", loc="bot")
    dot(d, (6.5, 4)); dot(d, (6.5, 0))
    d.add(elm.Capacitor().endpoints((6.5, 4), (6.5, 0)).label("$0.2\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    wire(d, (6.5, 4), (9.8, 4))
    sw(d, (9.8, 4), (9.8, 2.2), "open", loc="bot")
    d.add(elm.Resistor().endpoints((9.8, 2.2), (9.8, 0)).label(f"$R_2=3{OHM}$", loc="bot"))
    wire(d, (0, 0), (9.8, 0))
    save(d, "lp-ex")


def lp_ex_s():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$\\dfrac{10}{s}$", loc="top")
    d.add(Z().endpoints((0, 4), (2.8, 4)).label("$2$"))
    d.add(Z().endpoints((2.8, 4), (5.4, 4)).label("$s$"))
    vsrc_h(d, (8.2, 4), (5.4, 4), "$2$")
    cur(d, (8.2, 4), (10, 4), "$I(s)$", loc="top")
    d.add(Z().endpoints((10, 4), (10, 2.0)).label("$\\dfrac{5}{s}$", loc="bot"))
    vsrc(d, (10, 0), (10, 2.0), "", loc="bot")
    text(d, (11.2, 1.0), "$\\dfrac{6}{s}$")
    wire(d, (0, 0), (10, 0))
    text(d, (11.6, 3.3), "$+$"); text(d, (11.6, 2.0), "$U_C(s)$"); text(d, (11.6, 0.4), "$−$")
    save(d, "lp-ex-s")


def lp_poles():
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.axhline(0, color=MUTED, lw=1); ax.axvline(0, color=MUTED, lw=1)
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-2.4, 3.2)
    ax.axis("off")
    ax.fill_between([-3.4, 0], -2.4, 3.2, color=C3, alpha=0.06, lw=0)
    ax.fill_between([0, 3.4], -2.4, 3.2, color=C2, alpha=0.06, lw=0)
    ax.text(3.3, -0.12, "$\\sigma$", fontsize=13, ha="right", va="top", color=INK)
    ax.text(0.12, 3.15, "$j\\omega$", fontsize=13, va="top", color=INK)
    ax.text(-3.3, -2.3, "左半平面：稳定", fontsize=10, color=INK, va="bottom")
    ax.text(3.3, -2.3, "右半平面：不稳定", fontsize=10, color=INK, va="bottom", ha="right")
    tt = np.linspace(0, 1, 200)
    cases = [((-2.2, 0), lambda u: np.exp(-4 * u)),
             ((0, 0), lambda u: np.ones_like(u)),
             ((2.2, 0), lambda u: np.exp(3 * u) / np.exp(3)),
             ((-1.6, 1.4), lambda u: np.exp(-3 * u) * np.cos(25 * u)),
             ((0, 1.4), lambda u: np.cos(25 * u)),
             ((1.6, 1.4), lambda u: np.exp(3 * (u - 1)) * np.cos(25 * u))]
    for (x, y), f in cases:
        ax.plot([x], [y], "x", ms=9, mew=2, color=C1)
        if y:
            ax.plot([x], [-y], "x", ms=9, mew=2, color=C1)
        ins = ax.inset_axes([x - 0.55, y + 0.25 if y else -1.15, 1.1, 0.75], transform=ax.transData)
        ins.plot(tt, f(tt), color=C2, lw=1.4)
        ins.axhline(0, color=GRID, lw=0.6)
        ins.set_xticks([]); ins.set_yticks([])
        for sp_ in ins.spines.values():
            sp_.set_color(GRID)
        ins.set_ylim(-1.15, 1.15)
    save_fig(fig, "lp-poles")


def lp_x2():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$u_s$", loc="top")
    sw(d, (0, 3.5), (2.6, 3.5), "close")
    d.add(elm.Resistor().endpoints((2.6, 3.5), (5.4, 3.5)).label(f"$2{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((5.4, 3.5), (5.4, 0)).label("$1\\,\\mathrm{H}$", loc="bot"))
    arrow(d, (4.6, 2.8), (4.6, 1.2), "$i$", loc="top")
    wire(d, (0, 0), (5.4, 0))
    save(d, "lp-x2")


def lp_x3():
    d = new_drawing()
    d.add(elm.Capacitor().endpoints((0, 3.5), (0, 0)).label("$0.5\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    cur(d, (0, 3.5), (3.8, 3.5), "$i$", loc="top")
    d.add(elm.Resistor().endpoints((3.8, 3.5), (6.6, 3.5)).label(f"$3{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((6.6, 3.5), (6.6, 0)).label("$1\\,\\mathrm{H}$", loc="top")
          .label(("+", "$u_L$", "−"), loc="bot"))
    wire(d, (0, 0), (6.6, 0))
    save(d, "lp-x3")


def lp_x4():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$u_s$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3, 3.5)).label("$R$"))
    d.add(elm.Inductor2(loops=3).endpoints((3, 3.5), (6, 3.5)).label("$1\\,\\mathrm{H}$"))
    d.add(elm.Capacitor().endpoints((6, 3.5), (6, 0)).label("$0.5\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    wire(d, (0, 0), (6, 0))
    save(d, "lp-x4")


if __name__ == "__main__":
    lp_model_L(); lp_model_C(); lp_ex(); lp_ex_s(); lp_poles(); lp_x2(); lp_x3(); lp_x4()
