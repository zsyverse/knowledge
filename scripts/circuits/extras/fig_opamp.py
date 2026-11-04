"""拓展·含理想运放的电路 插图（前缀 oa-）。

运放一律用 xcommon.opamp：in1 为反相输入（−），in2 为同相输入（+）；flip=True 时 + 在上。
"""
import numpy as np
from xcommon import (elm, new_drawing, save, save_fig, dot, text, cur, arrow, vsrc, wire, opamp, gnd,
                     axes, plt, C1, C2, MUTED, INK, GRID)

K = "\\,\\mathrm{k}\\Omega"


def term_in(d, xy, name, dx=-0.6):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1]), name)


def term_out(d, out, name="$u_o$", length=1.4):
    p = (out[0] + length, out[1])
    wire(d, out, p)
    dot(d, p, True)
    text(d, (p[0] + 0.55, p[1]), name)


def loop(d, a, b, h, el, label=None, loc="top", **kw):
    """从 a 竖直走 h，经元件 el 横跨到 b 的正上/下方，再竖直回到 b。"""
    (x1, y1), (x2, y2) = a, b
    y = y1 + h
    wire(d, a, (x1, y))
    e = el.endpoints((x1, y), (x2, y))
    if label:
        e.label(label, loc=loc, **kw)
    d.add(e)
    wire(d, (x2, y), b)


def oa_model():
    d = new_drawing()
    op = opamp(d, (0, 0))
    for pin, nm, lab, loc in ((op.in1, "$u_-$", "$i_-$", "top"), (op.in2, "$u_+$", "$i_+$", "bot")):
        t = (pin[0] - 1.6, pin[1])
        term_in(d, t, nm)
        cur(d, t, pin, lab, loc=loc, frac=0.45)
    term_out(d, op.out, "$u_o$", length=1.2)
    text(d, (op.in1[0] + 1.75, op.in1[1] - 0.62), "$A$")
    save(d, "oa-model")


def oa_transfer():
    fig, ax = axes(4.6, 2.6)
    U = 12
    ax.plot([-3, -1, 1, 3], [-U, -U, U, U], color=C1, lw=2)
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xticks([]); ax.set_yticks([-U, U], ["$-U_{sat}$", "$U_{sat}$"])
    ax.set_xlim(-3, 3); ax.set_ylim(-15, 15)
    ax.set_xlabel("$u_d=u_+-u_-$", color=INK, loc="right")
    ax.set_ylabel("$u_o$", color=INK)
    ax.annotate("线性区：斜率 $A$ 极大，\n$u_d$ 只有微伏级", xy=(0.35, 4.2), xytext=(0.9, -8), color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(-2.8, -10.0, "负饱和", color=INK, fontsize=10)
    ax.text(1.7, 9.0, "正饱和", color=INK, fontsize=10)
    save_fig(fig, "oa-transfer")


def inv(name, r1="$R_1$", rf="$R_f$", cap=False, uc=False):
    """反相放大 / 积分器（cap=True 时反馈元件为电容）。"""
    d = new_drawing()
    op = opamp(d, (4.5, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term_in(d, (0, n1[1]), "$u_i$")
    d.add(elm.Resistor().endpoints((0, n1[1]), (nx, n1[1])).label(r1))
    wire(d, (nx, n1[1]), n1)
    fb = elm.Capacitor() if cap else elm.Resistor()
    if uc:
        fb.label(("+", "$u_C$", "−"), loc="bot", ofst=0.15)
    loop(d, (nx, n1[1]), (o[0] + 0.6, o[1]), 1.9 - o[1] + n1[1] - 0.6, fb, rf)
    dot(d, (nx, n1[1])); dot(d, (o[0] + 0.6, o[1]))
    wire(d, o, (o[0] + 0.6, o[1]))
    term_out(d, (o[0] + 0.6, o[1]), length=0.8)
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    save(d, name)


def noninv(name, follower=False):
    d = new_drawing()
    op = opamp(d, (4.5, 0), flip=True)          # + 在上
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term_in(d, (nx - 2.2, n2[1]), "$u_i$")
    wire(d, (nx - 2.2, n2[1]), n2)
    wire(d, n1, (nx, n1[1]))
    ox = o[0] + 0.6
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    if follower:
        wire(d, (nx, n1[1]), (nx, n1[1] - 1.0), (ox, n1[1] - 1.0), (ox, o[1]))
    else:
        loop(d, (nx, n1[1]), (ox, o[1]), -1.6 + (o[1] - n1[1]) * 0 , elm.Resistor(), "$R_f$", loc="bot")
        dot(d, (nx, n1[1]))
        d.add(elm.Resistor().endpoints((nx, n1[1]), (nx - 2.2, n1[1])).label("$R_1$", loc="bot"))
        wire(d, (nx - 2.2, n1[1]), (nx - 2.2, n1[1] - 0.5)); gnd(d, (nx - 2.2, n1[1] - 0.5))
    term_out(d, (ox, o[1]), length=0.8)
    save(d, name)


def summing(name, labels=("$R_1$", "$R_2$", "$R_3$", "$R_f$"), ins=("$u_1$", "$u_2$", "$u_3$")):
    d = new_drawing()
    op = opamp(d, (5.5, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    bx = nx - 0.9
    ys = [n1[1] + 2.8, n1[1] + 1.4, n1[1]]
    for y, r, u in zip(ys, labels[:3], ins):
        term_in(d, (0, y), u)
        d.add(elm.Resistor().endpoints((0, y), (bx, y)).label(r, loc="top", ofst=0.05))
        if y != n1[1]:
            dot(d, (bx, y)) if y != ys[0] else None
    wire(d, (bx, ys[0]), (bx, n1[1]), n1)
    dot(d, (bx, n1[1])); dot(d, (nx, n1[1]))
    ox = o[0] + 0.6
    loop(d, (nx, n1[1]), (ox, o[1]), 3.9, elm.Resistor(), labels[3])
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    term_out(d, (ox, o[1]), length=0.8)
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    save(d, name)


def diff(name):
    d = new_drawing()
    op = opamp(d, (5.0, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term_in(d, (0, n1[1]), "$u_1$")
    d.add(elm.Resistor().endpoints((0, n1[1]), (nx, n1[1])).label("$R_1$"))
    wire(d, (nx, n1[1]), n1)
    term_in(d, (0, n2[1]), "$u_2$")
    d.add(elm.Resistor().endpoints((0, n2[1]), (nx, n2[1])).label("$R_2$", loc="bot"))
    wire(d, (nx, n2[1]), n2)
    dot(d, (nx, n2[1]))
    d.add(elm.Resistor().endpoints((nx, n2[1]), (nx, n2[1] - 2.4)).label("$R_3$", loc="bot"))
    gnd(d, (nx, n2[1] - 2.4))
    ox = o[0] + 0.6
    loop(d, (nx, n1[1]), (ox, o[1]), 1.6, elm.Resistor(), "$R_f$")
    dot(d, (nx, n1[1]))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    term_out(d, (ox, o[1]), length=0.8)
    save(d, name)


def two_stage():
    d = new_drawing()
    a1 = opamp(d, (2.6, 0), flip=True)           # A1 同相放大，+ 在上
    m1, p1, o1 = a1.in1, a1.in2, a1.out
    text(d, (m1[0] + 1.6, o1[1]), "$A_1$")
    nx = m1[0] - 0.6
    term_in(d, (nx - 2.4, p1[1]), "$u_{i1}$", dx=-0.7)
    wire(d, (nx - 2.4, p1[1]), p1)
    wire(d, m1, (nx, m1[1])); dot(d, (nx, m1[1]))
    d.add(elm.Resistor().endpoints((nx, m1[1]), (nx - 2.4, m1[1])).label(f"$10{K}$", loc="bot"))
    wire(d, (nx - 2.4, m1[1]), (nx - 2.4, m1[1] - 0.5)); gnd(d, (nx - 2.4, m1[1] - 0.5))
    ox1 = o1[0] + 0.6
    loop(d, (nx, m1[1]), (ox1, o1[1]), -1.6, elm.Resistor(), f"$20{K}$", loc="bot")
    wire(d, o1, (ox1, o1[1])); dot(d, (ox1, o1[1]))
    text(d, (ox1, o1[1] + 0.45), "$u_{o1}$")
    # A2：差分
    a2 = opamp(d, (ox1 + 3.6, o1[1]))
    m2, p2, o2 = a2.in1, a2.in2, a2.out
    text(d, (m2[0] + 1.6, o2[1]), "$A_2$")
    nx2 = m2[0] - 0.6
    d.add(elm.Resistor().endpoints((ox1, o1[1]), (nx2, m2[1])).label(f"$10{K}$"))
    wire(d, (nx2, m2[1]), m2); dot(d, (nx2, m2[1]))
    ox2 = o2[0] + 0.6
    loop(d, (nx2, m2[1]), (ox2, o2[1]), 1.6, elm.Resistor(), f"$30{K}$")
    wire(d, o2, (ox2, o2[1])); dot(d, (ox2, o2[1]))
    term_out(d, (ox2, o2[1]), length=0.8)
    pt = (nx2, p2[1] - 1.8)
    wire(d, p2, (nx2, p2[1]), pt)
    dot(d, pt, True); text(d, (pt[0] - 0.65, pt[1]), "$u_{i2}$")
    save(d, "oa-two-stage")


def lossy():
    d = new_drawing()
    op = opamp(d, (4.5, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    term_in(d, (0, n1[1]), "$u_i$")
    d.add(elm.Resistor().endpoints((0, n1[1]), (nx, n1[1])).label(f"$R_1=10{K}$"))
    wire(d, (nx, n1[1]), n1); dot(d, (nx, n1[1]))
    loop(d, (nx, n1[1]), (ox, o[1]), 1.7, elm.Capacitor().label(("+", "$u_C$", "−"), loc="top", ofst=0.1),
         "$C=0.1\\,\\mu\\mathrm{F}$", loc="bot")
    loop(d, (nx, n1[1] + 1.7), (ox, n1[1] + 1.7), 1.9, elm.Resistor(), f"$R_f=20{K}$")
    dot(d, (nx, n1[1] + 1.7)); dot(d, (ox, n1[1] + 1.7))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    term_out(d, (ox, o[1]), length=0.8)
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    save(d, "oa-lossy")


def tfb():
    d = new_drawing()
    op = opamp(d, (4.5, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    term_in(d, (0, n1[1]), "$u_i$")
    d.add(elm.Resistor().endpoints((0, n1[1]), (nx, n1[1])).label(f"$R_1=10{K}$"))
    wire(d, (nx, n1[1]), n1); dot(d, (nx, n1[1]))
    top = n1[1] + 4.2
    mx = (nx + ox) / 2
    wire(d, (nx, n1[1]), (nx, top))
    d.add(elm.Resistor().endpoints((nx, top), (mx, top)).label(f"$R_2=100{K}$"))
    d.add(elm.Resistor().endpoints((mx, top), (ox, top)).label(f"$R_3=100{K}$"))
    wire(d, (ox, top), (ox, o[1]))
    dot(d, (mx, top)); text(d, (mx + 0.4, top - 0.4), "$m$")
    d.add(elm.Resistor().endpoints((mx, top), (mx, top - 2.2)).label(f"$R_4=10{K}$", loc="bot"))
    gnd(d, (mx, top - 2.2))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    term_out(d, (ox, o[1]), length=0.8)
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    save(d, "oa-tfb")


def nic():
    d = new_drawing()
    op = opamp(d, (6.5, 0), flip=True)            # + 在上
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    ax_ = nx - 4.0
    dot(d, (ax_, n2[1]), True); text(d, (ax_ - 0.45, n2[1]), "$a$")
    cur(d, (ax_, n2[1]), (ax_ + 1.2, n2[1]), "$i$", loc="top")
    wire(d, (ax_, n2[1]), n2)
    dot(d, (nx, n2[1]))
    loop(d, (nx, n2[1]), (ox, o[1]), 1.6, elm.Resistor(), f"$R=1{K}$")
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    loop(d, (nx, n1[1]), (ox, o[1]), -1.6, elm.Resistor(), f"$R_1=2{K}$", loc="bot")
    rx = nx - 1.1
    wire(d, (nx, n1[1]), (rx, n1[1]))
    d.add(elm.Resistor().endpoints((rx, n1[1]), (rx, n1[1] - 3.2)).label(f"$R_2=1{K}$", loc="top"))
    gb = (rx, n1[1] - 3.2)
    wire(d, (ax_, gb[1]), gb)
    dot(d, (ax_, gb[1]), True); text(d, (ax_ - 0.45, gb[1]), "$a'$")
    text(d, (ax_, (n2[1] + gb[1]) / 2 + 0.9), "$+$"); text(d, (ax_, (n2[1] + gb[1]) / 2), "$u$")
    text(d, (ax_, gb[1] + 0.5), "$−$")
    gnd(d, (ox, gb[1])); wire(d, gb, (ox, gb[1]))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    term_out(d, (ox, o[1]), length=0.8)
    save(d, "oa-nic")


def integ_wave():
    from xcommon import axes as ax_
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.4, 3.8), sharex=True, gridspec_kw=dict(height_ratios=[1, 2]))
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=10)
        ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.axhline(0, color=MUTED, lw=0.8)
    a1.plot([0, 1, 1, 3.2], [0.5, 0.5, -1, -1], color=C2, lw=2)
    a1.set_yticks([-1, 0, 0.5], ["−1", "0", "0.5"]); a1.set_ylabel("$u_i$/V", color=INK)
    t = np.array([0, 1, 2.7, 3.2]); u = np.array([0, -5, 12, 12])
    a2.plot(t, u, color=C1, lw=2)
    a2.axhline(12, color=MUTED, lw=1, ls="--"); a2.axhline(-12, color=MUTED, lw=1, ls="--")
    a2.plot([1.5], [0], "o", ms=5, color=C1); a2.plot([1], [-5], "o", ms=5, color=C1); a2.plot([2.7], [12], "o", ms=5, color=C1)
    a2.text(1.02, -6.6, "$(1,\\,-5)$", fontsize=10, color=INK)
    a2.text(1.55, -2.0, "$(1.5,\\,0)$", fontsize=10, color=INK)
    a2.text(2.0, 12.8, "$(2.7,\\,12)$ 起正饱和", fontsize=10, color=INK)
    a2.set_yticks([-12, -5, 0, 12]); a2.set_ylim(-14, 15)
    a2.set_ylabel("$u_o$/V", color=INK)
    a2.set_xticks([0, 1, 1.5, 2.7, 3]); a2.set_xticklabels(["0", "1", "1.5", "2.7", "3"])
    a2.set_xlabel("$t$/s", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "oa-integ-wave")


if __name__ == "__main__":
    oa_model()
    oa_transfer()
    inv("oa-inv")
    noninv("oa-noninv")
    noninv("oa-follower", follower=True)
    summing("oa-sum")
    diff("oa-diff")
    inv("oa-integ", r1="$R$", rf="$C$", cap=True, uc=True)
    two_stage()
    lossy()
    summing("oa-sum3", labels=(f"$20{K}$", f"$30{K}$", f"$60{K}$", f"$R_f=60{K}$"))
    tfb()
    nic()
    inv("oa-integ-ex", r1=f"$R=100{K}$", rf="$C=1\\,\\mu\\mathrm{F}$", cap=True, uc=True)
    integ_wave()
