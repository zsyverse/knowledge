"""模电·功率放大与直流电源 插图（前缀 pw-）。

    cd scripts/circuits/analog && ../../../.venv/bin/python fig_power.py
"""
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig as _save_fig, dot, text, wire, gnd, opamp, axes, plt,
                     note, C1, C2, C3, C4, INK, MUTED)


def save_fig(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    _save_fig(fig, name)


def rail(d, xy, name, up=True):
    """电源端子：空心圆 + 名称。"""
    dot(d, xy, True)
    text(d, (xy[0], xy[1] + (0.4 if up else -0.4)), name)


def npn(d, base_xy, label=None, pnp=False):
    e = (elm.BjtPnp if pnp else elm.BjtNpn)(circle=True).anchor("base").at(base_xy)
    if label:
        e.label(label, loc="right", ofst=0.1)
    d.add(e)
    return e


# ---------------------------------------------------------------- 功率放大
def ocl(name="pw-ocl", otl=False):
    """甲乙类互补推挽：OCL（±V_CC）或 OTL（单电源 + 输出电容）。"""
    d = new_drawing()
    xb = 3.0                      # 偏置链所在竖线
    xt = 5.0                      # 晶体管基极横坐标
    t1 = npn(d, (xt, 1.6), "$T_1$")
    t2 = npn(d, (xt, -1.6), "$T_2$", pnp=True)
    xo = t1.emitter[0]
    # 集电极接电源
    top, bot = 4.4, -4.4
    wire(d, t1.collector, (xo, top))
    rail(d, (xo, top), "$+V_{CC}$")
    if otl:
        wire(d, t2.collector, (xo, bot - 0.0)); gnd(d, (xo, bot))
    else:
        wire(d, t2.collector, (xo, bot))
        rail(d, (xo, bot), "$-V_{CC}$", up=False)
    # 发射极汇合为输出点
    wire(d, t1.emitter, (xo, 0)); wire(d, t2.emitter, (xo, 0)); dot(d, (xo, 0))
    # 偏置链 +V_CC — R1 — D1 — D2 — R2 — −V_CC
    wire(d, (xb, top), (xo, top))
    d.add(elm.Resistor().endpoints((xb, top), (xb, 1.6)).label("$R_1$", loc="bot"))
    d.add(elm.Diode().endpoints((xb, 1.6), (xb, 0)).label("$D_1$", loc="bot"))
    d.add(elm.Diode().endpoints((xb, 0), (xb, -1.6)).label("$D_2$", loc="bot"))
    if otl:
        d.add(elm.Resistor().endpoints((xb, -1.6), (xb, bot)).label("$R_2$", loc="bot"))
        wire(d, (xb, bot), (xo, bot))
    else:
        d.add(elm.Resistor().endpoints((xb, -1.6), (xb, bot)).label("$R_2$", loc="bot"))
        wire(d, (xb, bot), (xo, bot))
    dot(d, (xb, top)); dot(d, (xb, bot))
    wire(d, (xb, 1.6), t1.base); dot(d, (xb, 1.6))
    wire(d, (xb, -1.6), t2.base); dot(d, (xb, -1.6))
    # 输入
    dot(d, (xb, 0))
    if otl:
        d.add(elm.Capacitor().endpoints((0.6, 0), (xb, 0)).label("$C_1$"))
    else:
        wire(d, (0.6, 0), (xb, 0))
    dot(d, (0.6, 0), True); text(d, (0.1, 0), "$v_i$")
    # 输出与负载
    xr = xo + 2.6
    if otl:
        d.add(elm.Capacitor(polar=True).endpoints((xo, 0), (xr, 0)).label("$C$"))
        text(d, (xo + 0.55, 0.45), "$A$")
    else:
        wire(d, (xo, 0), (xr, 0))
    d.add(elm.Resistor().endpoints((xr, 0), (xr, -2.2)).label("$R_L$", loc="bot"))
    gnd(d, (xr, -2.2))
    dot(d, (xr, 0))
    wire(d, (xr, 0), (xr + 1.0, 0)); dot(d, (xr + 1.0, 0), True); text(d, (xr + 1.5, 0), "$v_o$")
    save(d, name)


def crossover():
    """乙类的交越失真：传输特性与输出波形。"""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 2.9), gridspec_kw=dict(width_ratios=[1, 1.6]))
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.spines["left"].set_position(("data", 0)); ax.spines["bottom"].set_position(("data", 0))
    vth = 0.5
    vi = np.linspace(-2, 2, 400)
    b = np.sign(vi) * np.clip(np.abs(vi) - vth, 0, None)
    a1.plot(vi, vi, color=C1, lw=1.6, ls="--", label="理想 / 甲乙类")
    a1.plot(vi, b, color=C2, lw=2, label="乙类")
    a1.axvspan(-vth, vth, color=C2, alpha=0.10)
    a1.set_xlabel("$v_i$", color=INK, loc="right"); a1.text(0.1, 1.55, "$v_o$", color=INK)
    a1.set_xticks([-vth, vth], ["$-V_{th}$", "$V_{th}$"]); a1.set_yticks([])
    a1.xaxis.set_label_coords(1.0, 0.42)
    a1.legend(frameon=False, fontsize=9, loc="lower right")
    a1.set_title("传输特性（死区 $|v_i|<V_{th}\\approx0.5$ V）", fontsize=10, color=INK)
    t = np.linspace(0, 2, 600)
    v = 2 * np.sin(2 * np.pi * t)
    o = np.sign(v) * np.clip(np.abs(v) - vth, 0, None)
    a2.plot(t, v, color=C1, lw=1.3, ls="--", label="$v_i$")
    a2.plot(t, o, color=C2, lw=2, label="$v_o$（乙类）")
    a2.axhline(0, color=MUTED, lw=0.8)
    a2.set_xticks([]); a2.set_yticks([]); a2.text(0.03, 2.0, "$v$", color=INK)
    a2.set_xlabel("$t$", color=INK, loc="right")
    a2.annotate("交越失真", xy=(1.0, 0.0), xytext=(1.08, -1.9), color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    a2.legend(frameon=False, fontsize=9, loc="lower left", ncol=2, bbox_to_anchor=(0.0, -0.08))
    fig.tight_layout()
    save_fig(fig, "pw-crossover")


def dissipation():
    """乙类 OCL：P_o、P_V、单管 P_T 与效率随 U_om/V_CC 的变化（以 V_CC^2/R_L 为单位）。"""
    fig, ax = axes(6.0, 3.2)
    x = np.linspace(0, 1, 300)
    po = x**2 / 2
    pv = 2 * x / np.pi
    pt1 = (pv - po) / 2
    ax.plot(x, pv, color=C1, lw=2, label="$P_V$（电源）")
    ax.plot(x, po, color=C3, lw=2, label="$P_o$（负载）")
    ax.plot(x, pt1, color=C2, lw=2, label="$P_{T1}$（每管）")
    xm = 2 / np.pi
    ax.plot([xm, xm], [0, 1 / np.pi**2], color=MUTED, lw=0.8, ls=":")
    ax.plot([xm], [1 / np.pi**2], "o", color=C2, ms=4)
    ax.annotate("$U_{om}=2V_{CC}/\\pi$ 时\n$P_{T1max}=V_{CC}^2/(\\pi^2R_L)\\approx0.2P_{om}$",
                xy=(xm, 1 / np.pi**2), xytext=(0.06, 0.36), color=INK, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.set_xlabel("$U_{om}/V_{CC}$", color=INK, loc="right")
    ax.set_ylabel("功率 / $(V_{CC}^2/R_L)$", color=INK, fontsize=10)
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 0.68)
    a2 = ax.twinx()
    a2.plot(x, np.pi * x / 4 * 100, color=C4, lw=1.4, ls="--", label="$\\eta$（右轴）")
    a2.set_ylim(0, 0.68 / 0.64 * 85); a2.set_ylabel("$\\eta$ / %", color=C4, fontsize=10)
    a2.tick_params(colors=MUTED, labelsize=9)
    for s in ("top",):
        a2.spines[s].set_visible(False)
    a2.spines["right"].set_color(MUTED)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=9, loc="upper left")
    save_fig(fig, "pw-dissipation")


# ---------------------------------------------------------------- 直流电源
def bridge():
    """单相桥式整流 + 电容滤波。"""
    d = new_drawing()
    tr = elm.Transformer(t1=4, t2=4).anchor("p1").at((0, 1.5))
    d.add(tr)
    p1, p2, s1, s2 = tr.p1, tr.p2, tr.s1, tr.s2
    wire(d, p1, (p1[0] - 0.8, p1[1])); wire(d, p2, (p2[0] - 0.8, p2[1]))
    dot(d, (p1[0] - 0.8, p1[1]), True); dot(d, (p2[0] - 0.8, p2[1]), True)
    text(d, (p1[0] - 1.25, (p1[1] + p2[1]) / 2), "$v_1$")
    text(d, (s1[0] + 0.45, (s1[1] + s2[1]) / 2), "$v_2$")
    # 菱形四个顶点：T、B 接交流，R 为 + 输出端，L 为 − 输出端
    cy, r = (s1[1] + s2[1]) / 2, 1.5
    cx = s1[0] + 2.6 + r
    L, R, T, B = (cx - r, cy), (cx + r, cy), (cx, cy + r), (cx, cy - r)
    d.add(elm.Diode().endpoints(T, R).label("$D_1$", loc="top"))
    d.add(elm.Diode().endpoints(L, B).label("$D_3$", loc="bot"))
    d.add(elm.Diode().endpoints(B, R).label("$D_2$", loc="bot"))
    d.add(elm.Diode().endpoints(L, T).label("$D_4$", loc="top"))
    for p in (L, R, T, B):
        dot(d, p)
    wire(d, s1, (s1[0] + 0.7, s1[1]), (s1[0] + 0.7, T[1] + 0.8), (T[0], T[1] + 0.8), T)
    wire(d, s2, (s2[0] + 0.7, s2[1]), (s2[0] + 0.7, B[1] - 0.8), (B[0], B[1] - 0.8), B)
    xc, xl = R[0] + 1.6, R[0] + 3.4
    ybot = B[1] - 1.6
    wire(d, R, (xl, cy))
    wire(d, L, (L[0] - 0.6, cy), (L[0] - 0.6, ybot), (xl, ybot))
    d.add(elm.Capacitor(polar=True).endpoints((xc, cy), (xc, ybot)).label("$C$", loc="bot"))
    d.add(elm.Resistor().endpoints((xl, cy), (xl, ybot)).label("$R_L$", loc="bot"))
    dot(d, (xc, cy)); dot(d, (xc, ybot))
    xv = xl + 1.4
    text(d, (xv, cy - 0.3), "+"); text(d, (xv, (cy + ybot) / 2), "$V_O$")
    text(d, (xv, ybot + 0.3), "−")
    save(d, "pw-bridge")


def ripple():
    """全波整流电容滤波的输出波形（数值仿真）。"""
    fig, ax = axes(6.2, 2.9)
    f, Vp, RL, C = 50.0, 9.2, 90.0, 1000e-6
    t = np.linspace(0, 0.06, 6000)
    vr = Vp * np.abs(np.sin(2 * np.pi * f * t))
    vo = np.empty_like(t); v = 0.0
    dt = t[1] - t[0]
    for i, x in enumerate(vr):
        if x >= v:
            v = x
        else:
            v -= v / (RL * C) * dt
        vo[i] = v
    ax.plot(t * 1e3, vr, color=C1, lw=1.0, ls="--", label="整流后 $|v_2|$（未滤波）")
    ax.plot(t * 1e3, vo, color=C2, lw=2, label="电容滤波后 $v_O$")
    m = t > 0.03
    vmax, vmin = vo[m].max(), vo[m].min()
    for v_ in (vmax, vmin):
        ax.plot([33, 46], [v_, v_], color=MUTED, lw=0.7, ls=":")
    ax.annotate("", xy=(35, vmax), xytext=(35, vmin), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
    ax.text(36.0, vmax + 0.45, "$V_{r(pp)}$", color=INK, fontsize=10)
    ax.set_xlabel("$t$ / ms", color=INK, loc="right"); ax.set_ylabel("$v$ / V", color=INK)
    ax.set_ylim(0, 11.5); ax.set_xlim(0, 60)
    ax.legend(frameon=False, fontsize=9, loc="lower left", ncol=2, bbox_to_anchor=(0.0, 1.0))
    save_fig(fig, "pw-ripple")


def zener():
    """稳压管稳压电路。"""
    d = new_drawing()
    y1, y0 = 2.2, 0
    dot(d, (0, y1), True); dot(d, (0, y0), True)
    text(d, (-0.45, y1 - 0.4), "+"); text(d, (-0.45, (y1 + y0) / 2), "$V_I$"); text(d, (-0.45, y0 + 0.4), "−")
    d.add(elm.Resistor().endpoints((0, y1), (3, y1)).label("$R$"))
    d.add(elm.Zener().endpoints((3, y0), (3, y1)).label("$D_Z$", loc="bot"))
    d.add(elm.Resistor().endpoints((5.2, y1), (5.2, y0)).label("$R_L$", loc="bot"))
    wire(d, (3, y1), (6.4, y1)); wire(d, (0, y0), (6.4, y0))
    dot(d, (3, y1)); dot(d, (5.2, y1)); dot(d, (3, y0)); dot(d, (5.2, y0))
    dot(d, (6.4, y1), True); dot(d, (6.4, y0), True)
    text(d, (6.85, y1 - 0.4), "+"); text(d, (6.85, (y1 + y0) / 2), "$V_O$"); text(d, (6.85, y0 + 0.4), "−")
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((1.0, y1 + 0.95), (2.0, y1 + 0.95)).label("$I_R$"))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((2.45, 1.75), (2.45, 0.85)).label("$I_Z$", loc="top"))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((4.6, 1.75), (4.6, 0.85)).label("$I_L$", loc="top"))
    save(d, "pw-zener")


def series_reg():
    """串联型线性稳压电路：基准 + 误差放大 + 调整管 + 取样。"""
    d = new_drawing()
    yt, yo, yg = 5.3, 2.6, -2.2
    t = npn(d, (5.0, 4.3), "$T$")
    xe = t.collector[0]
    xin, xz = -1.6, -0.4
    dot(d, (xin, yt), True); text(d, (xin - 0.5, yt), "$V_I$")
    wire(d, (xin, yt), (xe, yt), t.collector)
    # 输出、取样、负载
    xs, xl, xo = 9.0, 10.3, 11.5
    wire(d, t.emitter, (xe, yo), (xo, yo))
    dot(d, (xo, yo), True); text(d, (xo + 0.5, yo), "$V_O$")
    d.add(elm.Resistor().endpoints((xs, yo), (xs, 0.2)).label("$R_1$", loc="bot"))
    d.add(elm.Resistor().endpoints((xs, 0.2), (xs, yg)).label("$R_2$", loc="bot"))
    d.add(elm.Resistor().endpoints((xl, yo), (xl, yg)).label("$R_L$", loc="bot"))
    for p in ((xs, yo), (xl, yo), (xs, 0.2), (xs, yg), (xl, yg)):
        dot(d, p)
    # 误差放大器（+ 在上）
    op = elm.Opamp(leads=True, flip=True).right().anchor("in1").at((1.2, 0.6))
    d.add(op)
    wire(d, op.out, (4.6, op.out[1]), (4.6, t.base[1]), t.base)
    wire(d, op.in1, (0.7, op.in1[1]), (0.7, -0.6), (8.2, -0.6), (8.2, 0.2), (xs, 0.2))
    # 基准
    yr = op.in2[1]
    d.add(elm.Resistor().endpoints((xz, yt), (xz, yr)).label("$R$", loc="bot"))
    d.add(elm.Zener().endpoints((xz, yg), (xz, yr)).label("$D_Z$", loc="bot"))
    wire(d, (xz, yr), op.in2)
    dot(d, (xz, yt)); dot(d, (xz, yr))
    text(d, (0.35, yr + 0.4), "$V_{REF}$", fontsize=13)
    wire(d, (xz, yg), (xo, yg)); dot(d, (xo, yg), True)
    gnd(d, (3.0, yg))
    note(d, (xe, yt + 0.55), "调整管")
    note(d, (2.9, 2.75), "误差放大")
    note(d, (7.8, -1.4), "取样")
    note(d, (-1.6, -0.6), "基准")
    save(d, "pw-series")


def lm317():
    d = new_drawing()
    # 稳压器方框
    x0, x1, y0, y1 = 2.0, 4.6, 0.0, 1.6
    wire(d, (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
    text(d, ((x0 + x1) / 2, (y0 + y1) / 2 + 0.15), "LM317")
    text(d, (x0 + 0.35, y1 - 0.35), "IN", fontsize=10)
    text(d, (x1 - 0.42, y1 - 0.35), "OUT", fontsize=10)
    text(d, ((x0 + x1) / 2, y0 + 0.28), "ADJ", fontsize=10)
    yin = y1 - 0.35
    dot(d, (-0.6, yin), True); text(d, (-1.1, yin), "$V_I$")
    wire(d, (-0.6, yin), (x0, yin))
    d.add(elm.Capacitor().endpoints((0.6, yin), (0.6, -3.6)).label("$0.33\\,\\mu$F", loc="bot"))
    dot(d, (0.6, yin))
    xr = 6.4
    wire(d, (x1, yin), (9.2, yin)); dot(d, (9.2, yin), True); text(d, (9.7, yin), "$V_O$")
    d.add(elm.Resistor().endpoints((xr, yin), (xr, -1.2)).label("$R_1=240\\,\\Omega$", loc="bot"))
    dot(d, (xr, yin))
    xm = (x0 + x1) / 2
    wire(d, (xm, y0), (xm, -1.2), (xr, -1.2)); dot(d, (xr, -1.2))
    d.add(elm.Resistor().endpoints((xr, -1.2), (xr, -3.6)).label("$R_2$", loc="bot"))
    xc = 8.4
    dot(d, (xc, yin))
    d.add(elm.Capacitor().endpoints((xc, yin), (xc, -3.6)).label("$1\\,\\mu$F", loc="bot"))
    wire(d, (-0.6, -3.6), (9.2, -3.6)); dot(d, (-0.6, -3.6), True); dot(d, (9.2, -3.6), True)
    dot(d, (0.6, -3.6)); dot(d, (xr, -3.6)); dot(d, (xc, -3.6))
    text(d, (xr - 0.95, (yin - 1.2) / 2), "$1.25$ V", fontsize=11, color=C1)
    d.add(elm.Arrow(headwidth=0.22, headlength=0.28).endpoints((xm - 0.35, -0.2), (xm - 0.35, -1.0)))
    text(d, (xm - 0.95, -0.6), "$I_{ADJ}$", fontsize=12)
    save(d, "pw-lm317")


if __name__ == "__main__":
    ocl()
    ocl("pw-otl", otl=True)
    crossover()
    dissipation()
    bridge()
    ripple()
    zener()
    series_reg()
    lm317()
