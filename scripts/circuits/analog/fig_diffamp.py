"""模电·差分放大与集成运放 插图（前缀 dp-）。数值与 verify_diffamp.py 一致。"""
import numpy as np
import schemdraw.flow as flow
from acommon import (elm, new_drawing, save, save_fig, dot, text, cur, wire, gnd, opamp, axes, plt,
                     C1, C2, C3, MUTED, INK, GRID)


def R(d, p, q, lab=None, loc="top", **kw):
    e = elm.Resistor().endpoints(p, q)
    if lab:
        e.label(lab, loc=loc, **kw)
    d.add(e)


def term(d, xy, name, dx=-0.5, dy=0.0):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1] + dy), name)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)


# ---------------------------------------------------------------- 电路
def pair():
    """长尾式差分放大电路（尾电阻 R_EE，可换成电流源 I_T）。"""
    d = new_drawing()
    t1 = elm.BjtNpn().anchor("base").at((0, 0))
    t2 = elm.BjtNpn().reverse().anchor("base").at((4.4, 0))
    d.add(t1); d.add(t2)
    x1, x2 = t1.collector[0], t2.collector[0]
    yt, yc, ye = 4.4, 1.8, -1.5
    R(d, (x1, yt), (x1, yc), "$R_C$")
    R(d, (x2, yt), (x2, yc), "$R_C$", loc="bot")
    wire(d, (x1, yc), t1.collector); wire(d, (x2, yc), t2.collector)
    wire(d, (x1, yt), (x2, yt))
    xm = (x1 + x2) / 2
    dot(d, (xm, yt))
    wire(d, (xm, yt), (xm, yt + 0.6))
    term(d, (xm, yt + 0.6), "$+V_{CC}$", dx=0.0, dy=0.45)
    for x, nm, dx in ((x1, "$v_{o1}$", -0.55), (x2, "$v_{o2}$", 0.55)):
        dot(d, (x, yc))
        xo = x - 1.1 if dx < 0 else x + 1.1
        wire(d, (x, yc), (xo, yc))
        term(d, (xo, yc), nm, dx=dx)
    wire(d, t1.emitter, (x1, ye), (x2, ye), t2.emitter)
    dot(d, (xm, ye))
    cur(d, (xm, ye), (xm, ye - 1.0), "$I_{EE}$", loc="bot", frac=0.5)
    R(d, (xm, ye - 1.0), (xm, ye - 3.4), "$R_{EE}$", loc="bot")
    term(d, (xm, ye - 3.4), "$-V_{EE}$", dx=0.0, dy=-0.45)
    term(d, (-1.2, 0), "$v_1$")
    wire(d, (-1.2, 0), t1.base)
    term(d, (5.6, 0), "$v_2$", dx=0.5)
    wire(d, t2.base, (5.6, 0))
    text(d, (x1 + 0.6, 0.0), "$T_1$")
    text(d, (x2 - 0.6, 0.0), "$T_2$")
    cur(d, (x1, yc), t1.collector, None)
    text(d, (x1 + 0.55, 1.25), "$i_{C1}$", fontsize=13)
    cur(d, (x2, yc), t2.collector, None)
    text(d, (x2 - 0.55, 1.25), "$i_{C2}$", fontsize=13)
    save(d, "dp-pair")


def half_circuits():
    """(a) 差模半电路：射极为交流地；(b) 共模半电路：射极接 2R_EE。"""
    d = new_drawing()
    for x0, cm in ((0.0, False), (6.0, True)):
        t = elm.BjtNpn().anchor("base").at((x0 + 1.6, 0))
        d.add(t)
        xc = t.collector[0]
        R(d, (xc, 3.0), (xc, 1.4), "$R_C$")
        wire(d, (xc, 1.4), t.collector)
        dot(d, (xc, 1.4))
        wire(d, (xc, 1.4), (xc + 1.2, 1.4))
        term(d, (xc + 1.2, 1.4), "$v_{c1}$" if cm else "$v_{o1}$", dx=0.55)
        wire(d, (xc, 3.0), (xc - 0.6, 3.0)); wire(d, (xc, 3.0), (xc + 0.6, 3.0))
        text(d, (xc, 3.45), "交流地", color=MUTED, fontsize=12)
        gy = -2.6
        d.add(elm.SourceSin().endpoints((x0, gy), (x0, 0)).label("$v_c$" if cm else "$v_d/2$", loc="top"))
        wire(d, (x0, 0), t.base)
        if cm:
            R(d, t.emitter, (xc, gy), "$2R_{EE}$", loc="bot")
        else:
            wire(d, t.emitter, (xc, gy))
        wire(d, (x0, gy), (xc, gy))
        gnd(d, ((x0 + xc) / 2, gy))
        text(d, ((x0 + xc) / 2 + 0.3, gy - 1.0), "（b）共模" if cm else "（a）差模", color=MUTED, fontsize=13)
    save(d, "dp-half")


def active_load():
    """有源负载（PNP 电流镜）差分对，单端输出。"""
    d = new_drawing()
    t1 = elm.BjtNpn().anchor("base").at((0, 0))
    t2 = elm.BjtNpn().reverse().anchor("base").at((4.4, 0))
    d.add(t1); d.add(t2)
    x1, x2 = t1.collector[0], t2.collector[0]
    yb3 = 3.4
    t3 = elm.BjtPnp().reverse().anchor("base").at((x1 + 0.75, yb3))
    t4 = elm.BjtPnp().anchor("base").at((x2 - 0.75, yb3))
    d.add(t3); d.add(t4)
    assert abs(t3.collector[0] - x1) < 0.01 and abs(t4.collector[0] - x2) < 0.01
    wire(d, t3.base, t4.base)
    xm = (x1 + x2) / 2
    dot(d, (xm, yb3))
    yk = 1.6
    wire(d, t3.collector, (x1, yk), t1.collector)
    wire(d, (x1, yk), (xm, yk), (xm, yb3))
    dot(d, (x1, yk))
    wire(d, t4.collector, (x2, yk), t2.collector)
    dot(d, (x2, yk))
    wire(d, (x2, yk), (x2 + 1.4, yk))
    term(d, (x2 + 1.4, yk), "$v_o$", dx=0.5)
    ytop = 5.0
    wire(d, t3.emitter, (x1, ytop), (x2, ytop), t4.emitter)
    dot(d, (xm, ytop))
    wire(d, (xm, ytop), (xm, ytop + 0.5))
    term(d, (xm, ytop + 0.5), "$+V_{CC}$", dx=0.0, dy=0.45)
    ye = -1.5
    wire(d, t1.emitter, (x1, ye), (x2, ye), t2.emitter)
    dot(d, (xm, ye))
    d.add(elm.SourceI().endpoints((xm, ye), (xm, ye - 2.2)).label("$I_T$", loc="bot"))
    term(d, (xm, ye - 2.2), "$-V_{EE}$", dx=0.0, dy=-0.45)
    term(d, (-1.2, 0), "$v_1$"); wire(d, (-1.2, 0), t1.base)
    term(d, (5.6, 0), "$v_2$", dx=0.5); wire(d, t2.base, (5.6, 0))
    text(d, (x1 + 0.6, 0.0), "$T_1$"); text(d, (x2 - 0.6, 0.0), "$T_2$")
    text(d, (x1 - 0.6, yb3), "$T_3$"); text(d, (x2 + 0.6, yb3), "$T_4$")
    save(d, "dp-active-load")


def opamp_blocks():
    d = new_drawing()
    names = [("差分输入级", "高 $R_i$、高 CMRR\n抑制零漂"), ("中间增益级", "共射 + 有源负载\n补偿电容 $C_c$"),
             ("输出级", "互补推挽（OCL）\n低 $R_o$、大电流")]
    w, h, gap = 3.2, 1.6, 1.4
    x = 0.0
    xs = []
    for nm, sub in names:
        b = flow.Box(w=w, h=h).at((x, 0)).anchor("W").label(nm, fontsize=14)
        d.add(b)
        text(d, (x + w / 2, -1.5), sub, color=MUTED, fontsize=11)
        xs.append(x)
        x += w + gap
    for x0 in xs[:-1]:
        d.add(elm.Arrow().endpoints((x0 + w, 0), (x0 + w + gap, 0)))
    d.add(elm.Arrow().endpoints((-1.4, 0.4), (0, 0.4)))
    d.add(elm.Arrow().endpoints((-1.4, -0.4), (0, -0.4)))
    text(d, (-1.8, 0.4), "$u_+$"); text(d, (-1.8, -0.4), "$u_-$")
    d.add(elm.Arrow().endpoints((x - gap, 0), (x - gap + 1.4, 0)))
    text(d, (x - gap + 1.85, 0), "$u_o$")
    bx = flow.Box(w=x - gap, h=1.0).at((0, 2.3)).anchor("W").label("偏置电路：电流镜、微电流源", fontsize=13)
    d.add(bx)
    for x0 in xs:
        d.add(elm.Arrow().endpoints((x0 + w / 2, 1.8), (x0 + w / 2, h / 2)))
    save(d, "dp-opamp-blocks")


def offset_model():
    """输入失调与偏置电流的等效：输入接地的反相放大器。"""
    d = new_drawing()
    op = opamp(d, (5.0, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.7
    wire(d, n1, (nx, n1[1]))
    dot(d, (nx, n1[1]))
    R(d, (nx, n1[1]), (nx - 2.6, n1[1]), "$R_1$", loc="bot")
    wire(d, (nx - 2.6, n1[1]), (nx - 2.6, n1[1] - 0.5)); gnd(d, (nx - 2.6, n1[1] - 0.5))
    ox = o[0] + 0.6
    y = n1[1] + 1.6
    wire(d, (nx, n1[1]), (nx, y))
    R(d, (nx, y), (ox, y), "$R_f$")
    wire(d, (ox, y), (ox, o[1]))
    wire(d, o, (ox + 0.8, o[1])); dot(d, (ox, o[1]))
    term(d, (ox + 0.8, o[1]), "$U_O$", dx=0.55)
    px = nx - 1.2
    wire(d, n2, (px, n2[1]))
    d.add(elm.SourceV().endpoints((px, n2[1] - 1.8), (px, n2[1])).label("$U_{IO}$", loc="top"))
    R(d, (px, n2[1] - 1.8), (px, n2[1] - 4.0), "$R_p$")
    gnd(d, (px, n2[1] - 4.0))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((n1[0] - 0.55, n1[1] + 0.35), (n1[0] - 0.05, n1[1] + 0.35)))
    text(d, (n1[0] - 0.3, n1[1] + 0.75), "$I_{B-}$", fontsize=13)
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((n2[0] - 0.55, n2[1] - 0.35), (n2[0] - 0.05, n2[1] - 0.35)))
    text(d, (n2[0] - 0.3, n2[1] - 0.75), "$I_{B+}$", fontsize=13)
    save(d, "dp-offset")


# ---------------------------------------------------------------- 曲线
def transfer():
    x = np.linspace(-8, 8, 400)            # v_d / V_T
    i1 = 1 / (1 + np.exp(-x))
    fig, ax = axes(5.4, 2.9)
    ax.plot(x, i1, color=C1, lw=1.8, label="$i_{C1}/I_{EE}$")
    ax.plot(x, 1 - i1, color=C2, lw=1.8, label="$i_{C2}/I_{EE}$")
    xl = np.linspace(-2.6, 2.6, 10)
    ax.plot(xl, 0.5 + xl / 4, color=MUTED, lw=1.0, ls="--", label="小信号近似")
    ax.axvspan(-1, 1, color=GRID, alpha=0.6)
    ax.text(0, 1.04, "近似线性区\n$|v_d|\\lesssim V_T$", ha="center", fontsize=9, color=INK)
    ax.axhline(0.5, color=MUTED, lw=0.6)
    ax.set_xticks([-8, -4, -2, 0, 2, 4, 8]); ax.set_yticks([0, 0.5, 1])
    ax.set_ylim(-0.05, 1.25)
    ax.set_xlabel("$v_d/V_T$", color=INK, loc="right")
    ax.legend(frameon=False, fontsize=9, loc="center right", bbox_to_anchor=(1.0, 0.3))
    save_fig(fig, "dp-transfer")


def slew():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.5))
    for a in (a1, a2):
        style(a)
    t = np.linspace(0, 2, 400)
    a1.plot(t, np.sin(2 * np.pi * t), color=C1, lw=1.8)
    tt = np.linspace(-0.12, 0.12, 10)
    a1.plot(0.5 + tt, -2 * np.pi * tt, color=C2, lw=2.0)
    a1.annotate("斜率最大 $=\\omega U_{om}$\n（过零处）", xy=(0.5, 0), xytext=(0.0, -1.05), fontsize=9, color=C2,
                arrowprops=dict(arrowstyle="->", color=C2))
    a1.annotate("峰值处斜率为 0", xy=(0.25, 1), xytext=(0.9, 1.15), fontsize=9, color=MUTED,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    a1.axhline(0, color=MUTED, lw=0.6)
    a1.set_xticks([]); a1.set_yticks([-1, 0, 1], ["$-U_{om}$", "0", "$U_{om}$"])
    a1.set_ylim(-1.3, 1.45)
    a1.set_title("正弦输出的最大变化率", fontsize=10, color=INK)
    # 压摆率限制：dy/dt = clip(k (x − y), −SR, SR)
    n = 4000
    tt = np.linspace(0, 2, n)
    x = np.sin(2 * np.pi * tt)
    y = np.zeros(n)
    SR = 3.0                                  # < ω U_om = 2π
    dt = tt[1] - tt[0]
    for k in range(1, n):
        y[k] = y[k - 1] + np.clip(200 * (x[k - 1] - y[k - 1]), -SR, SR) * dt
    a2.plot(tt, x, color=GRID, lw=1.5, ls="--", label="理想输出")
    a2.plot(tt, y, color=C1, lw=1.8, label="受 SR 限制")
    a2.axhline(0, color=MUTED, lw=0.6)
    a2.set_xticks([]); a2.set_yticks([])
    a2.set_ylim(-1.3, 1.45)
    a2.set_title("$\\omega U_{om}>SR$：斜率失真", fontsize=10, color=INK)
    a2.legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    save_fig(fig, "dp-slew")


if __name__ == "__main__":
    pair()
    half_circuits()
    active_load()
    opamp_blocks()
    offset_model()
    transfer()
    slew()
