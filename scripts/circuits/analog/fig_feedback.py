"""模电·负反馈放大电路 插图（前缀 fb-）。

    cd scripts/circuits/analog && ../../../.venv/bin/python fig_feedback.py
"""
import math
import os
from pathlib import Path

import numpy as np
import schemdraw.dsp as dsp
from acommon import (elm, new_drawing, save, save_fig as _save_fig, dot, text, cur, wire, gnd, opamp, axes, plt,
                     note, C1, C2, C3, INK, MUTED)

K = "\\,\\mathrm{k}\\Omega"
PLUS, MINUS = "$\\oplus$", "$\\ominus$"


def opamp(d, at_in1, flip=False):
    """同 acommon.opamp，但显式指定方向向右（避免继承上一元件的方向）。"""
    e = elm.Opamp(leads=True, flip=flip).right().anchor("in1").at(at_in1)
    d.add(e)
    return e


def save_fig(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    _save_fig(fig, name)


def term(d, xy, name, dx=-0.6):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1]), name)


def pol(d, xy, s, color=C2):
    text(d, xy, s, color=color, fontsize=17)


# ---------------------------------------------------------------- 框图
def block():
    d = new_drawing()
    term(d, (0, 0), "$x_i$", dx=-0.5)
    d.add(dsp.Arrow().endpoints((0, 0), (1.6, 0)))
    s = dsp.SumSigma().anchor("W").at((1.6, 0))
    d.add(s)
    text(d, (1.35, 0.4), "$+$")
    text(d, (2.6, -0.95), "$-$")
    d.add(dsp.Arrow().endpoints(s.E, (s.E[0] + 2.0, 0)).label("$x_{id}$", loc="top"))
    a = dsp.Box(w=2.4, h=1.4).anchor("W").at((s.E[0] + 2.0, 0)).label("基本放大电路\n$A$")
    d.add(a)
    xo = a.E[0] + 1.4
    wire(d, a.E, (xo, 0)); dot(d, (xo, 0))
    d.add(dsp.Arrow().endpoints((xo, 0), (xo + 1.4, 0)))
    text(d, (xo + 1.8, 0), "$x_o$")
    yb = -2.6
    fbx = (a.W[0] + a.E[0]) / 2
    wire(d, (xo, 0), (xo, yb))
    d.add(dsp.Arrow().endpoints((xo, yb), (fbx + 1.2, yb)))
    f = dsp.Box(w=2.4, h=1.4).anchor("E").at((fbx + 1.2, yb)).label("反馈网络\n$F$")
    d.add(f)
    wire(d, f.W, (s.S[0], yb))
    d.add(dsp.Arrow().endpoints((s.S[0], yb), s.S).label("$x_f$", loc="bot", ofst=0.15))
    save(d, "fb-block")


# ---------------------------------------------------------------- 共射 + R_E（瞬时极性）
def ce_re():
    d = new_drawing()
    t = elm.BjtNpn(circle=True).anchor("base").at((3.0, 0)).label("$T$", loc="right", ofst=0.15)
    d.add(t)
    b, c, e = t.base, t.collector, t.emitter
    top, bot = 4.2, -3.6
    xb = 2.0
    # 偏置分压
    wire(d, b, (xb, 0)); dot(d, (xb, 0))
    d.add(elm.Resistor().endpoints((xb, top), (xb, 0)).label("$R_{B1}$", loc="bot"))
    d.add(elm.Resistor().endpoints((xb, 0), (xb, bot)).label("$R_{B2}$", loc="bot"))
    # 集电极
    d.add(elm.Resistor().endpoints((c[0], top), (c[0], 1.8)).label("$R_C$", loc="bot"))
    wire(d, (c[0], 1.8), c)
    # 发射极电阻（不旁路）
    d.add(elm.Resistor().endpoints(e, (e[0], bot)).label("$R_E$", loc="bot"))
    wire(d, (xb, top), (c[0], top))
    dot(d, (c[0], top), True); text(d, (c[0] + 0.7, top), "$+V_{CC}$")
    wire(d, (xb, bot), (c[0] + 3.4, bot)); gnd(d, (c[0], bot))
    # 输入耦合
    d.add(elm.Capacitor().endpoints((0, 0), (xb, 0)).label("$C_1$"))
    term(d, (0, 0), "$u_i$", dx=-0.5)
    # 输出耦合 + 负载
    yc = 1.8
    dot(d, (c[0], yc))
    d.add(elm.Capacitor().endpoints((c[0], yc), (c[0] + 2.0, yc)).label("$C_2$"))
    wire(d, (c[0] + 2.0, yc), (c[0] + 3.4, yc))
    d.add(elm.Resistor().endpoints((c[0] + 3.4, yc), (c[0] + 3.4, bot)).label("$R_L$", loc="bot"))
    dot(d, (c[0] + 3.4, yc)); text(d, (c[0] + 3.85, yc + 0.35), "$u_o$")
    # 瞬时极性
    pol(d, (b[0] - 0.35, 0.45), PLUS)
    pol(d, (e[0] + 0.45, e[1] - 0.6), PLUS)
    pol(d, (c[0] + 0.45, yc - 0.55), MINUS)
    note(d, (e[0] + 1.75, -1.35), "$u_e$ 随 $u_b$ 升高\n$u_{be}$ 被削弱", halign="center")
    save(d, "fb-ce-re")


# ---------------------------------------------------------------- 两级运放 + 级间反馈
def two_stage():
    d = new_drawing()
    a1 = opamp(d, (3.0, 0))
    m1, p1, o1 = a1.in1, a1.in2, a1.out
    text(d, (m1[0] + 1.55, o1[1]), "$A_1$")
    nx = m1[0] - 0.6
    term(d, (0, 0), "$u_i$", dx=-0.5)
    d.add(elm.Resistor().endpoints((0, 0), (nx, 0)).label("$R_1$"))
    wire(d, (nx, 0), m1); dot(d, (nx, 0))
    ox1 = o1[0] + 0.5
    wire(d, o1, (ox1, o1[1])); dot(d, (ox1, o1[1]))
    wire(d, p1, (nx, p1[1]), (nx, p1[1] - 0.5)); gnd(d, (nx, p1[1] - 0.5))
    # A2：同相放大
    a2 = opamp(d, (ox1 + 2.2, o1[1] - 1.25), flip=True)     # + 在上，与 A1 输出同高
    m2, p2, o2 = a2.in1, a2.in2, a2.out
    text(d, (m2[0] + 1.55, o2[1]), "$A_2$")
    wire(d, (ox1, o1[1]), p2)
    nx2 = m2[0] - 0.6
    ox2 = o2[0] + 0.5
    yj = m2[1] - 1.0
    wire(d, m2, (nx2, m2[1]), (nx2, yj)); dot(d, (nx2, yj))
    d.add(elm.Resistor().endpoints((nx2, yj), (nx2, yj - 2.0)).label("$R_3$", loc="bot"))
    gnd(d, (nx2, yj - 2.0))
    d.add(elm.Resistor().endpoints((nx2, yj), (ox2, yj)).label("$R_4$", loc="bot"))
    wire(d, (ox2, yj), (ox2, o2[1])); wire(d, o2, (ox2, o2[1])); dot(d, (ox2, o2[1]))
    wire(d, (ox2, o2[1]), (ox2 + 1.2, o2[1])); term(d, (ox2 + 1.2, o2[1]), "$u_o$", dx=0.55)
    # 级间反馈 RF：u_o → A1 反相端
    ytop = 2.2
    wire(d, (ox2, o2[1]), (ox2, ytop))
    d.add(elm.Resistor().endpoints((ox2, ytop), (nx - 0.0, ytop)).label("$R_F$", loc="top"))
    wire(d, (nx, ytop), (nx, 0))
    # 极性
    pol(d, (0, 0.55), PLUS)
    pol(d, (nx + 0.35, -0.5), PLUS)
    pol(d, (ox1 + 0.35, o1[1] - 0.55), MINUS)
    pol(d, (ox2 + 0.45, o2[1] - 0.5), MINUS)
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((nx - 0.35, 0.6), (nx - 0.35, 1.5)))
    text(d, (nx - 0.75, 1.05), "$i_f$")
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((0.6, -0.45), (1.4, -0.45)))
    text(d, (1.0, -0.85), "$i_i$")
    save(d, "fb-two-stage")


# ---------------------------------------------------------------- 四种组态
def vs():
    """电压串联：同相放大。"""
    d = new_drawing()
    op = opamp(d, (3.0, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term(d, (0.6, n2[1]), "$u_i$", dx=-0.5)
    wire(d, (0.6, n2[1]), n2)
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    ox = o[0] + 0.6
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    yb = n1[1] - 1.6
    wire(d, (nx, n1[1]), (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (ox, yb)).label("$R_f$", loc="bot"))
    wire(d, (ox, yb), (ox, o[1])); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.2)).label("$R_1$", loc="bot"))
    gnd(d, (nx, yb - 2.2))
    wire(d, (ox, o[1]), (ox + 1.0, o[1])); term(d, (ox + 1.0, o[1]), "$u_o$", dx=0.55)
    text(d, (nx - 0.65, yb - 0.6), "$u_f$")
    save(d, "fb-vs")


def vp():
    """电压并联：反相放大。"""
    d = new_drawing()
    op = opamp(d, (3.6, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term(d, (0, 0), "$u_s$", dx=-0.5)
    d.add(elm.Resistor().endpoints((0, 0), (nx, 0)).label("$R_1$"))
    wire(d, (nx, 0), n1); dot(d, (nx, 0))
    ox = o[0] + 0.6
    wire(d, (nx, 0), (nx, 1.7))
    d.add(elm.Resistor().endpoints((nx, 1.7), (ox, 1.7)).label("$R_f$"))
    wire(d, (ox, 1.7), (ox, o[1])); wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    wire(d, (ox, o[1]), (ox + 1.0, o[1])); term(d, (ox + 1.0, o[1]), "$u_o$", dx=0.55)
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    cur(d, (0.25, 0), (0.95, 0), None)
    text(d, (0.6, -0.45), "$i_i$")
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((nx + 0.3, 2.1), (nx + 1.1, 2.1)))
    text(d, (nx + 0.7, 2.5), "$i_f$")
    save(d, "fb-vp")


def cs():
    """电流串联：负载浮地的 V–I 变换。"""
    d = new_drawing()
    op = opamp(d, (3.0, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term(d, (0.6, n2[1]), "$u_i$", dx=-0.5)
    wire(d, (0.6, n2[1]), n2)
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    ox = o[0] + 0.6
    wire(d, o, (ox, o[1]))
    yb = n1[1] - 1.6
    wire(d, (nx, n1[1]), (nx, yb))
    d.add(elm.Resistor().endpoints((ox, yb), (nx, yb)).label("$R_L$", loc="bot"))
    wire(d, (ox, yb), (ox, o[1])); dot(d, (nx, yb))
    cur(d, (ox, o[1] - 0.2), (ox, o[1] - 1.2), "$i_o$", loc="bot")
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.2)).label("$R$", loc="bot"))
    gnd(d, (nx, yb - 2.2))
    text(d, (nx - 0.65, yb - 0.6), "$u_f$")
    save(d, "fb-cs")


def cp():
    """电流并联：负载电流按 R、R_F 分流后送回反相端。"""
    d = new_drawing()
    op = opamp(d, (3.6, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term(d, (0, 0), "$u_s$", dx=-0.5)
    d.add(elm.Resistor().endpoints((0, 0), (nx, 0)).label("$R_1$"))
    wire(d, (nx, 0), n1); dot(d, (nx, 0))
    ox = o[0] + 0.6
    mx = ox
    ytop = 2.0
    wire(d, (nx, 0), (nx, ytop))
    d.add(elm.Resistor().endpoints((nx, ytop), (mx, ytop)).label("$R_F$"))
    dot(d, (mx, ytop)); text(d, (mx + 0.1, ytop + 0.4), "$M$")
    d.add(elm.Resistor().endpoints((mx, ytop), (mx + 2.4, ytop)).label("$R$"))
    wire(d, (mx + 2.4, ytop), (mx + 2.4, ytop - 0.6)); gnd(d, (mx + 2.4, ytop - 0.6))
    d.add(elm.Resistor().endpoints((ox, o[1]), (mx, ytop)).label("$R_L$", loc="bot"))
    wire(d, o, (ox, o[1]))
    dot(d, (ox, o[1]))
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((ox + 1.3, o[1] + 0.6), (ox + 1.3, o[1] + 1.6)))
    text(d, (ox + 1.7, o[1] + 1.1), "$i_o$")
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    cur(d, (0.25, 0), (0.95, 0), None)
    text(d, (0.6, -0.45), "$i_i$")
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((nx + 0.4, ytop + 0.35), (nx + 1.2, ytop + 0.35)))
    text(d, (nx + 0.8, ytop + 0.75), "$i_f$")
    save(d, "fb-cp")


# ---------------------------------------------------------------- 环路增益波特图
def bode():
    A0, fp, F = 1e4, 1e6, 2e-4
    f = np.logspace(4, 8, 600)
    T = A0 * F / (1 + 1j * f / fp) ** 3
    mag = 20 * np.log10(abs(T))
    ph = np.degrees(np.unwrap(np.angle(T)))
    fc = math.sqrt(2 ** (2 / 3) - 1) * fp
    f180 = math.sqrt(3) * fp
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.8, 4.6), sharex=True)
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=10)
        ax.grid(True, color="#dddddd", lw=0.6, which="both")
        ax.set_axisbelow(True)
        ax.set_xscale("log")
        ax.axvline(fc, color=MUTED, lw=0.9, ls="--")
        ax.axvline(f180, color=MUTED, lw=0.9, ls=":")
    a1.plot(f, mag, color=C1, lw=2)
    a1.axhline(0, color=INK, lw=0.9)
    Tm = 20 * math.log10(A0 * F / 8)
    a1.annotate("", xy=(f180, Tm), xytext=(f180, 0), arrowprops=dict(arrowstyle="<->", color=C2, lw=1.4))
    a1.text(f180 * 1.15, Tm / 2 - 1, "GM = 12 dB", color=C2, fontsize=10)
    a1.set_ylabel("$20\\lg|T|$/dB", color=INK)
    a1.set_ylim(-60, 12)
    a1.text(fc * 0.55, 3, "$f_c$", color=INK, fontsize=11)
    a2.plot(f, ph, color=C1, lw=2)
    a2.axhline(-180, color=INK, lw=0.9)
    phc = -3 * math.degrees(math.atan(fc / fp))
    a2.annotate("", xy=(fc, phc), xytext=(fc, -180), arrowprops=dict(arrowstyle="<->", color=C2, lw=1.4))
    a2.text(fc * 0.12, -140, "PM = 67.6°", color=C2, fontsize=10)
    a2.text(f180 * 1.1, -170, "$f_{180}$", color=INK, fontsize=11)
    a2.set_yticks([0, -90, -180, -270])
    a2.set_ylabel("$\\angle T$/(°)", color=INK)
    a2.set_xlabel("$f$/Hz", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "fb-bode")


def comp():
    A0 = 1e4
    f = np.logspace(1, 9, 800)

    def mag(ps):
        v = A0 * np.ones_like(f, dtype=complex)
        for p in ps:
            v = v / (1 + 1j * f / p)
        return 20 * np.log10(abs(v))

    fig, ax = axes(5.8, 3.2)
    ax.set_xscale("log")
    ax.plot(f, mag([1e6, 1e7, 1e8]), color=C2, lw=2, label="补偿前：极点 1、10、100 MHz")
    ax.plot(f, mag([1e3, 1e7, 1e8]), color=C1, lw=2, label="补偿后：主极点压到 1 kHz")
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(1e7, color=MUTED, lw=0.9, ls="--")
    ax.text(1.2e7, 30, "$f_{p2}=10$ MHz", color=INK, fontsize=10)
    ax.text(30, 66, "$20\\lg A_0=80$ dB", color=INK, fontsize=10)
    ax.set_ylim(-40, 90)
    ax.set_ylabel("$20\\lg|A|$/dB", color=INK)
    ax.set_xlabel("$f$/Hz", color=INK, loc="right")
    ax.legend(fontsize=9, frameon=False, loc="lower left")
    ax.grid(True, which="both", color="#dddddd", lw=0.6)
    fig.tight_layout()
    save_fig(fig, "fb-comp")


if __name__ == "__main__":
    block()
    ce_re()
    two_stage()
    vs()
    vp()
    cs()
    cp()
    bode()
    comp()
