"""模电·波形发生电路 插图（前缀 wg-）。

    cd scripts/circuits/analog && ../../../.venv/bin/python fig_wavegen.py
"""
import math
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig as _save_fig, dot, text, wire, gnd, axes, plt,
                     note, C1, C2, C3, INK, MUTED)


def opamp(d, at_in1, flip=False, label=None):
    """in1 为反相输入（−）；flip=True 时 + 在上。显式向右，避免继承方向。"""
    e = elm.Opamp(leads=True, flip=flip).right().anchor("in1").at(at_in1)
    d.add(e)
    if label:
        text(d, (e.in1[0] + 1.55, e.out[1]), label)
    return e


def save_fig(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    _save_fig(fig, name)


def term(d, xy, name, dx=0.55):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1]), name)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)


def zener_out(d, o, drop=2.4, name="$u_o$", out_len=1.0):
    p = (o[0] + 0.4, o[1])
    q = (p[0] + 2.0, o[1])
    wire(d, o, p)
    d.add(elm.Resistor().endpoints(p, q).label("$R_O$"))
    dot(d, q)
    mid = (q[0], q[1] - drop / 2)
    d.add(elm.Zener().endpoints(mid, q))
    d.add(elm.Zener().endpoints(mid, (q[0], q[1] - drop)))
    text(d, (q[0] + 0.75, mid[1]), "$\\pm U_Z$")
    gnd(d, (q[0], q[1] - drop))
    if out_len:
        wire(d, q, (q[0] + out_len, q[1]))
        term(d, (q[0] + out_len, q[1]), name)
    return q


# ---------------------------------------------------------------- 文氏桥振荡器
def wien():
    d = new_drawing()
    op = opamp(d, (6.0, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.7
    yp = n2[1]
    xp = nx - 1.4
    wire(d, n2, (xp, yp)); dot(d, (xp, yp))
    # 并联 RC 对地
    xr, xc = xp - 1.6, xp
    yg = yp - 3.2
    wire(d, (xr, yp), (xp, yp)); dot(d, (xp, yp))
    d.add(elm.Resistor().endpoints((xr, yp), (xr, yg)).label("$R$", loc="top"))
    d.add(elm.Capacitor().endpoints((xc, yp - 0.0), (xc, yg)).label("$C$", loc="bot"))
    wire(d, (xr, yg), (xc, yg)); gnd(d, ((xr + xc) / 2, yg))
    dot(d, (xr, yp))
    # 串联 RC：输出 → C → R → 同相端
    yt = yp + 2.0
    wire(d, (xr, yp), (xr, yt))
    xm = (xr + ox) / 2
    d.add(elm.Resistor().endpoints((xr, yt), (xm, yt)).label("$R$"))
    d.add(elm.Capacitor().endpoints((xm, yt), (ox, yt)).label("$C$"))
    wire(d, (ox, yt), (ox, o[1])); wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    wire(d, (ox, o[1]), (ox + 1.0, o[1])); term(d, (ox + 1.0, o[1]), "$u_o$")
    # 负反馈：Rg 对地，Rf1 + Rf2（并反向二极管）接输出
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    yb = n1[1] - 1.4
    wire(d, (nx, n1[1]), (nx, yb)); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.0)).label("$R_g$", loc="bot"))
    gnd(d, (nx, yb - 2.0))
    x1 = nx + 2.0
    d.add(elm.Resistor().endpoints((nx, yb), (x1, yb)).label("$R_{f1}$"))
    d.add(elm.Resistor().endpoints((x1, yb), (ox, yb)).label("$R_{f2}$"))
    wire(d, (ox, yb), (ox, o[1]))
    dot(d, (x1, yb)); dot(d, (ox, yb))
    yd1, yd2 = yb - 1.0, yb - 2.0
    wire(d, (x1, yb), (x1, yd2)); wire(d, (ox, yb), (ox, yd2))
    d.add(elm.Diode().endpoints((x1, yd1), (ox, yd1)).label("$D_1$", loc="bot", ofst=0.05))
    d.add(elm.Diode().endpoints((ox, yd2), (x1, yd2)).label("$D_2$", loc="bot", ofst=0.05))
    dot(d, (x1, yd1)); dot(d, (ox, yd1))
    text(d, (xp + 0.1, yp + 0.45), "$u_f$")
    save(d, "wg-wien")


def wien_F():
    x = np.logspace(-1.3, 1.3, 600)
    F = 1 / (3 + 1j * (x - 1 / x))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.4, 3.9), sharex=True)
    for ax in (a1, a2):
        style(ax)
        ax.set_xscale("log")
        ax.axvline(1, color=MUTED, lw=0.9, ls="--")
        ax.grid(True, which="both", color="#dddddd", lw=0.6)
    a1.plot(x, abs(F), color=C1, lw=2)
    a1.set_yticks([0, 1 / 6, 1 / 3], ["0", "1/6", "1/3"])
    a1.set_ylabel("$|F|$", color=INK)
    a2.plot(x, np.degrees(np.angle(F)), color=C2, lw=2)
    a2.set_yticks([-90, -45, 0, 45, 90])
    a2.set_ylabel("$\\varphi_F$/(°)", color=INK)
    a2.set_xlabel("$\\omega/\\omega_0$", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "wg-wien-F")


# ---------------------------------------------------------------- 电容三点式（交流通路）
def colpitts():
    d = new_drawing()
    t = elm.BjtNpn(circle=True).anchor("base").at((2.0, 0)).label("$T$", loc="right", ofst=0.15)
    d.add(t)
    b, c, e = t.base, t.collector, t.emitter
    yg = -2.6
    wire(d, e, (e[0], yg))
    xb = 0.4
    xc = c[0] + 1.6
    yt = 2.4
    wire(d, b, (xb, 0)); dot(d, (xb, 0))
    wire(d, c, (c[0], 1.2), (xc, 1.2)); dot(d, (xc, 1.2))
    d.add(elm.Capacitor().endpoints((xb, 0), (xb, yg)).label("$C_2$", loc="bot"))
    d.add(elm.Capacitor().endpoints((xc, 1.2), (xc, yg)).label("$C_1$", loc="bot"))
    wire(d, (xb, 0), (xb, yt))
    d.add(elm.Inductor().endpoints((xb, yt), (xc, yt)).label("$L$"))
    wire(d, (xc, yt), (xc, 1.2))
    wire(d, (xb, yg), (xc, yg)); dot(d, (e[0], yg)); gnd(d, (e[0], yg))
    note(d, (xc + 2.1, 0.0), "交流通路\n（偏置电路省略）\n$e$ 交流接地")
    text(d, (b[0] - 0.25, 0.4), "$b$"); text(d, (c[0] + 0.35, 1.55), "$c$"); text(d, (e[0] + 0.35, e[1] - 0.3), "$e$")
    save(d, "wg-colpitts")


# ---------------------------------------------------------------- 石英晶体
def xtal_eq():
    d = new_drawing()
    top, bot = 0.0, -6.0
    xa, xb = 0.0, 2.6
    dot(d, (xa + 1.3, top + 0.8), True); dot(d, (xa + 1.3, bot - 0.8), True)
    wire(d, (xa + 1.3, top + 0.8), (xa + 1.3, top)); wire(d, (xa + 1.3, bot - 0.8), (xa + 1.3, bot))
    wire(d, (xa, top), (xb, top)); wire(d, (xa, bot), (xb, bot))
    d.add(elm.Resistor().endpoints((xa, top), (xa, -2.0)).label("$R_q$", loc="top"))
    d.add(elm.Inductor().endpoints((xa, -2.0), (xa, -4.0)).label("$L_q$", loc="top"))
    d.add(elm.Capacitor().endpoints((xa, -4.0), (xa, bot)).label("$C_q$", loc="top"))
    d.add(elm.Capacitor().endpoints((xb, top), (xb, bot)).label("$C_0$", loc="bot"))
    # 晶体符号
    d.add(elm.Crystal().endpoints((-3.6, -2.0), (-3.6, -4.0)).label("石英晶体", loc="top", ofst=0.3))
    wire(d, (-3.6, -2.0), (-3.6, -1.2)); wire(d, (-3.6, -4.0), (-3.6, -4.8))
    dot(d, (-3.6, -1.2), True); dot(d, (-3.6, -4.8), True)
    text(d, (-1.5, -3.0), "$\\Leftrightarrow$", fontsize=20)
    save(d, "wg-xtal-eq")


def xtal_X():
    Lq, Cq, C0 = 50e-3, 0.02e-12, 5e-12
    fs = 1 / (2 * math.pi * math.sqrt(Lq * Cq))
    fp = fs * math.sqrt(1 + Cq / C0)
    f = np.linspace(fs - 12e3, fp + 12e3, 4000)
    w = 2 * np.pi * f
    Xs = w * Lq - 1 / (w * Cq)
    X0 = -1 / (w * C0)
    X = Xs * X0 / (Xs + X0)
    X[np.abs(X) > 2e5] = np.nan
    fig, ax = axes(5.6, 3.0)
    ax.plot((f - fs) / 1e3, X / 1e3, color=C1, lw=2)
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=MUTED, lw=0.9, ls="--")
    ax.axvline((fp - fs) / 1e3, color=MUTED, lw=0.9, ls="--")
    ax.axvspan(0, (fp - fs) / 1e3, color=C2, alpha=0.08)
    ax.text(0.4, 120, "感性区\n$f_s<f<f_p$", color=C2, fontsize=10)
    ax.text(-11, 120, "容性", color=INK, fontsize=10)
    ax.text(13, 120, "容性", color=INK, fontsize=10)
    ax.text(0.3, -185, "$f_s$", color=INK, fontsize=11)
    ax.text((fp - fs) / 1e3 + 1.2, -185, "$f_p$", color=INK, fontsize=11)
    ax.set_ylim(-200, 200)
    ax.set_xlabel("$(f-f_s)$/kHz", color=INK, loc="right")
    ax.set_ylabel("电抗 $X$/k$\\Omega$", color=INK)
    fig.tight_layout()
    save_fig(fig, "wg-xtal-X")


# ---------------------------------------------------------------- RC 方波发生器
def square():
    d = new_drawing()
    op = opamp(d, (3.6, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    q = zener_out(d, o, out_len=1.6)
    xr = q[0] + 0.7
    # 反相端：C 对地，R 接 u_o
    wire(d, n1, (nx, 0)); dot(d, (nx, 0))
    yt = 1.8
    wire(d, (nx, 0), (nx, yt))
    d.add(elm.Resistor().endpoints((nx, yt), (xr, yt)).label("$R$"))
    wire(d, (xr, yt), (xr, o[1])); dot(d, (xr, o[1]))
    xc = nx - 1.4
    wire(d, (nx, 0), (xc, 0))
    d.add(elm.Capacitor().endpoints((xc, 0), (xc, -2.4)).label("$C$", loc="bot").label(("+", "$u_C$", "−"), loc="top", ofst=0.1))
    gnd(d, (xc, -2.4))
    # 同相端：R2 对地、R1 接 u_o
    py = n2[1]
    yb = py - 2.4
    wire(d, n2, (nx, py), (nx, yb)); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.0)).label("$R_2$", loc="bot"))
    gnd(d, (nx, yb - 2.0))
    d.add(elm.Resistor().endpoints((nx, yb), (xr, yb)).label("$R_1$", loc="bot"))
    wire(d, (xr, yb), (xr, o[1]))
    save(d, "wg-square")


def square_wave():
    UZ, F, tau = 6.0, 0.5, 1.0
    t1 = tau * math.log((1 + F) / (1 - F))
    t = np.linspace(0, 3 * 2 * t1, 1500)
    uc, uo = [], []
    state = UZ
    v = -F * UZ
    dt = t[1] - t[0]
    # 起始时刻取在电容刚降到 −F·UZ、输出刚翻为 +UZ 的瞬间
    for _ in t:
        uc.append(v); uo.append(state)
        v += (state - v) / tau * dt
        if state > 0 and v >= F * UZ:
            state = -UZ
        elif state < 0 and v <= -F * UZ:
            state = UZ
    fig, ax = axes(5.8, 3.0)
    ax.plot(t, uo, color=C1, lw=2, label="$u_o$")
    ax.plot(t, uc, color=C2, lw=2, label="$u_C$")
    for y in (F * UZ, -F * UZ):
        ax.axhline(y, color=MUTED, lw=0.9, ls="--")
    ax.set_yticks([-UZ, -F * UZ, 0, F * UZ, UZ], ["$-U_Z$", "$-FU_Z$", "0", "$FU_Z$", "$U_Z$"])
    ax.set_xticks([0, t1, 2 * t1], ["0", "$T/2$", "$T$"])
    ax.set_xlabel("$t$", color=INK, loc="right")
    ax.set_ylim(-7.5, 10)
    ax.legend(fontsize=10, frameon=False, loc="upper right", ncol=2)
    fig.tight_layout()
    save_fig(fig, "wg-square-wave")


# ---------------------------------------------------------------- 方波–三角波发生器
def sqtri():
    d = new_drawing()
    a1 = opamp(d, (3.0, 0), flip=True, label="$A_1$")     # + 在上
    n1, p1, o1 = a1.in1, a1.in2, a1.out
    nx = n1[0] - 0.6
    wire(d, n1, (nx, n1[1]), (nx, n1[1] - 0.5)); gnd(d, (nx, n1[1] - 0.5))
    q = zener_out(d, o1, out_len=0)
    text(d, (q[0] + 0.2, q[1] + 0.45), "$u_{o1}$")
    # A2 积分器
    a2 = opamp(d, (q[0] + 3.0, q[1]), label="$A_2$")
    n2, p2, o2 = a2.in1, a2.in2, a2.out
    nx2 = n2[0] - 0.6
    d.add(elm.Resistor().endpoints(q, (nx2, q[1])).label("$R$"))
    wire(d, (nx2, q[1]), n2); dot(d, (nx2, q[1]))
    ox2 = o2[0] + 0.6
    yc = q[1] + 1.8
    wire(d, (nx2, q[1]), (nx2, yc))
    d.add(elm.Capacitor().endpoints((nx2, yc), (ox2, yc)).label("$C$"))
    wire(d, (ox2, yc), (ox2, o2[1])); wire(d, o2, (ox2, o2[1])); dot(d, (ox2, o2[1]))
    wire(d, p2, (nx2, p2[1]), (nx2, p2[1] - 0.5)); gnd(d, (nx2, p2[1] - 0.5))
    wire(d, (ox2, o2[1]), (ox2 + 1.0, o2[1])); term(d, (ox2 + 1.0, o2[1]), "$u_o$")
    # A1 同相端：R2 接 u_o1（上方），R1 接 u_o（经底部回线）
    py = p1[1]
    wire(d, p1, (nx, py)); dot(d, (nx, py))
    yt = py + 1.6
    xq = q[0] - 0.0
    wire(d, (nx, py), (nx, yt))
    d.add(elm.Resistor().endpoints((nx, yt), (q[0], yt)).label("$R_2$"))
    wire(d, (q[0], yt), q)
    xl = nx - 1.6
    d.add(elm.Resistor().endpoints((nx, py), (xl, py)).label("$R_1$", loc="top"))
    yb = -4.2
    wire(d, (xl, py), (xl, yb), (ox2, yb), (ox2, o2[1]))
    save(d, "wg-sqtri")


def sqtri_wave():
    UZ, UT, RC = 6.0, 3.0, 0.5    # ms
    t = np.linspace(0, 3, 3001)
    sq, tri = [], []
    s, v = UZ, UT                  # 从三角波峰值、方波刚翻为 +UZ 开始
    dt = t[1] - t[0]
    for _ in t:
        sq.append(s); tri.append(v)
        v += -s / RC * dt
        if s > 0 and v <= -UT:
            s = -UZ
        elif s < 0 and v >= UT:
            s = UZ
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.6, 3.8), sharex=True)
    for ax in (a1, a2):
        style(ax)
        ax.axhline(0, color=MUTED, lw=0.8)
        for k in (0.5, 1.0, 1.5, 2.0, 2.5):
            ax.axvline(k, color=MUTED, lw=0.6, ls=":")
    a1.plot(t, sq, color=C1, lw=2)
    a1.set_yticks([-6, 6], ["$-U_Z$", "$+U_Z$"]); a1.set_ylim(-8, 8)
    a1.set_ylabel("$u_{o1}$", color=INK)
    a2.plot(t, tri, color=C2, lw=2)
    a2.set_yticks([-3, 0, 3], ["$-U_T$", "0", "$+U_T$"]); a2.set_ylim(-4.2, 4.2)
    a2.set_ylabel("$u_o$", color=INK)
    a2.set_xticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
    a2.set_xlabel("$t$/ms", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "wg-sqtri-wave")


if __name__ == "__main__":
    wien()
    wien_F()
    colpitts()
    xtal_eq()
    xtal_X()
    square()
    square_wave()
    sqtri()
    sqtri_wave()
