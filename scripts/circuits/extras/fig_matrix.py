"""拓展·矩阵形式与状态方程 插图（前缀 mx-）。"""
import numpy as np
from matplotlib.patches import FancyArrowPatch
from xcommon import (elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, isrc, wire, plt,
                     OHM, C1, C2, MUTED, INK, GRID)
from common import vsrc_h

NODES = {1: (0, 1.5), 2: (2, 3), 3: (4, 1.5), 4: (2, 0)}
BR = {1: (1, 2), 2: (2, 3), 3: (1, 4), 4: (2, 4), 5: (3, 4), 6: (3, 1)}


def graph(name, tree=()):
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    ax.set_aspect("equal"); ax.axis("off")
    for k, (a, b) in BR.items():
        p, q = np.array(NODES[a], float), np.array(NODES[b], float)
        thick = k in tree
        col = C1 if thick else INK
        lw = 3.2 if thick else 1.4
        if k == 6:       # ③→① 绕到 ④ 下方
            c = np.array([2, -2.4])
            u = np.linspace(0, 1, 200)
            pts = ((1 - u) ** 2)[:, None] * p + (2 * u * (1 - u))[:, None] * c + (u ** 2)[:, None] * q
            ax.plot(pts[:, 0], pts[:, 1], color=col, lw=lw, zorder=1)
            m = pts[100]; d = pts[104] - pts[96]
            lab = m + np.array([0, -0.32])
        else:
            ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=lw, zorder=1)
            m = (p + q) / 2; d = q - p
            nrm = np.array([-d[1], d[0]]) / np.hypot(*d)
            lab = m + 0.3 * nrm
            if k == 4:
                lab = m + np.array([0.28, 0])
        d = d / np.hypot(*d)
        ax.add_patch(FancyArrowPatch(m - 0.18 * d, m + 0.2 * d, arrowstyle="-|>", mutation_scale=16,
                                     color=col, lw=0, zorder=3))
        ax.text(*lab, f"{k}", fontsize=13, color=col, ha="center", va="center")
    for n, (x, y) in NODES.items():
        ax.plot([x], [y], "o", ms=7, color=INK, zorder=4)
        off = {1: (-0.38, 0), 2: (0, 0.35), 3: (0.38, 0), 4: (0.42, 0.2)}[n]
        ax.text(x + off[0], y + off[1], "①②③④"[n - 1], fontsize=14, ha="center", va="center", color=INK)
    ax.set_xlim(-0.7, 4.7); ax.set_ylim(-1.55, 3.6)
    save_fig(fig, name)


def mx_branch():
    d = new_drawing()
    a, b = (0, 2), (9.0, 2)
    dot(d, a, True); dot(d, b, True)
    text(d, (-0.45, 2), "$a$"); text(d, (9.45, 2), "$b$")
    cur(d, a, (1.4, 2), "$\\dot I_k$", loc="top")
    wire(d, (1.4, 2), (1.4, 3.3)); wire(d, (1.4, 2), (1.4, 0.7))
    d.add(elm.ResistorIEC().endpoints((1.4, 3.3), (4.6, 3.3)).label("$Z_k$"))
    vsrc_h(d, (7.4, 3.3), (4.6, 3.3), "$\\dot U_{sk}$")
    wire(d, (7.4, 3.3), (7.6, 3.3), (7.6, 2)); wire(d, (7.6, 2), b); wire(d, (7.6, 2), (7.6, 0.7))
    d.add(elm.SourceI().endpoints((7.6, 0.7), (1.4, 0.7)).label("$\\dot I_{sk}$", loc="bot"))
    dot(d, (1.4, 2)); dot(d, (7.6, 2))
    text(d, (0.2, 1.1), "$+$"); text(d, (4.5, -0.6), "$\\dot U_k$（$a$ 为 $+$，$b$ 为 $-$）", fontsize=13)
    text(d, (8.8, 1.1), "$−$")
    save(d, "mx-branch")


def mx_state():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$u_s$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3.2, 3.5)).label(f"$R_1=1{OHM}$"))
    dot(d, (3.2, 3.5)); dot(d, (3.2, 0)); text(d, (3.2, 3.95), "$a$")
    d.add(elm.Capacitor().endpoints((3.2, 3.5), (3.2, 0)).label("$1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    wire(d, (3.2, 3.5), (6.4, 3.5))
    d.add(elm.Inductor2(loops=3).endpoints((6.4, 3.5), (6.4, 1.6)).label("$1\\,\\mathrm{H}$", loc="bot"))
    arrow(d, (5.8, 3.1), (5.8, 2.0), "$i_L$", loc="top")
    d.add(elm.Resistor().endpoints((6.4, 1.6), (6.4, 0)).label(f"$R_2=1{OHM}$", loc="bot"))
    wire(d, (0, 0), (6.4, 0))
    save(d, "mx-state")


def mx_x4():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$u_s$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3.0, 3.5)).label(f"$1{OHM}$"))
    dot(d, (3.0, 3.5)); dot(d, (3.0, 0)); text(d, (3.0, 3.95), "$a$")
    d.add(elm.Capacitor().endpoints((3.0, 3.5), (3.0, 0)).label("$C_1=1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_1$", "−"), loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((3.0, 3.5), (6.6, 3.5)).label("$L=1\\,\\mathrm{H}$"))
    arrow(d, (4.0, 2.9), (5.6, 2.9), "$i_L$", loc="bot")
    dot(d, (6.6, 3.5)); dot(d, (6.6, 0)); text(d, (6.6, 3.95), "$b$")
    d.add(elm.Capacitor().endpoints((6.6, 3.5), (6.6, 0)).label("$C_2=1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_2$", "−"), loc="bot"))
    wire(d, (6.6, 3.5), (9.0, 3.5))
    d.add(elm.Resistor().endpoints((9.0, 3.5), (9.0, 0)).label(f"$1{OHM}$", loc="bot"))
    wire(d, (0, 0), (9.0, 0))
    save(d, "mx-x4")


if __name__ == "__main__":
    graph("mx-graph", tree=(3, 4, 5))
    graph("mx-graph-plain")
    mx_branch(); mx_state(); mx_x4()
