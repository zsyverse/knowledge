"""模电·信号运算与处理 插图（前缀 sp-）。

    cd scripts/circuits/analog && ../../../.venv/bin/python fig_sigproc.py
"""
import math
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig as _save_fig, dot, text, wire, gnd, axes, plt,
                     note, C1, C2, C3, C4, INK, MUTED)

K = "\\,\\mathrm{k}\\Omega"


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


def term(d, xy, name, dx=-0.6):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1]), name)


def out_term(d, xy, name="$u_o$", length=1.0):
    p = (xy[0] + length, xy[1])
    wire(d, xy, p)
    term(d, p, name, dx=0.55)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(True, color="#dddddd", lw=0.6)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- 对数 / 指数
def log_amp():
    d = new_drawing()
    op = opamp(d, (4.0, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    term(d, (0, 0), "$u_i$", dx=-0.5)
    d.add(elm.Resistor().endpoints((0, 0), (nx, 0)).label("$R$"))
    wire(d, (nx, 0), n1); dot(d, (nx, 0))
    yt = 2.4
    q = elm.BjtNpn(circle=True).theta(90).anchor("base").at(((nx + ox) / 2, yt - 0.75))
    d.add(q)
    wire(d, (nx, 0), (nx, yt), (q.collector[0], yt), q.collector) if False else None
    wire(d, (nx, 0), (nx, q.collector[1]), q.collector)
    wire(d, q.emitter, (ox, q.emitter[1]), (ox, o[1]))
    wire(d, q.base, (q.base[0], q.base[1] - 0.5)); gnd(d, (q.base[0], q.base[1] - 0.5))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    out_term(d, (ox, o[1]))
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    text(d, (q.base[0] + 0.0, q.collector[1] + 0.95), "$T$")
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((nx + 0.0 - 0.45, 0.4), (nx - 0.45, 1.2)))
    text(d, (nx - 0.95, 0.8), "$i_C$")
    save(d, "sp-log")


def exp_amp():
    d = new_drawing()
    op = opamp(d, (4.0, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    term(d, (0, 0), "$u_i$", dx=-0.5)
    d.add(elm.Diode().endpoints((0, 0), (nx, 0)).label("$D$"))
    wire(d, (nx, 0), n1); dot(d, (nx, 0))
    yt = 1.8
    wire(d, (nx, 0), (nx, yt))
    d.add(elm.Resistor().endpoints((nx, yt), (ox, yt)).label("$R$"))
    wire(d, (ox, yt), (ox, o[1]))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    out_term(d, (ox, o[1]))
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    save(d, "sp-exp")


# ---------------------------------------------------------------- 精密全波整流
def rectifier():
    d = new_drawing()
    a1 = opamp(d, (3.2, 0), label="$A_1$")
    n1, p1, o1 = a1.in1, a1.in2, a1.out
    nx = n1[0] - 0.6
    term(d, (0, 0), "$u_i$", dx=-0.5)
    wire(d, (0, 0), (0.4, 0)); dot(d, (0.4, 0))
    d.add(elm.Resistor().endpoints((0.4, 0), (nx, 0)).label(f"$R$"))
    wire(d, (nx, 0), n1); dot(d, (nx, 0))
    wire(d, p1, (nx, p1[1]), (nx, p1[1] - 0.5)); gnd(d, (nx, p1[1] - 0.5))
    oa = o1[0] + 0.5
    wire(d, o1, (oa, o1[1])); dot(d, (oa, o1[1]))
    # D1：A1 输出 → 反相端（ui<0 时导通）
    y1 = 1.4
    wire(d, (nx, 0), (nx, y1))
    d.add(elm.Diode().endpoints((oa, y1), (nx, y1)).label("$D_1$"))
    wire(d, (oa, o1[1]), (oa, y1))
    # D2 + R：经 D2 取输出 u_o1（ui>0 时 D2 导通）
    y2 = 2.9
    xo1 = oa + 1.6
    wire(d, (nx, y1), (nx, y2)); dot(d, (nx, y1))
    d.add(elm.Resistor().endpoints((nx, y2), (xo1, y2)).label("$R$"))
    d.add(elm.Diode().endpoints((xo1, y2), (xo1, o1[1])).label("$D_2$", loc="bot"))
    wire(d, (oa, o1[1]), (xo1, o1[1]))
    dot(d, (xo1, y2)); text(d, (xo1 + 0.15, y2 + 0.45), "$u_{o1}$")
    # A2：反相加法
    a2 = opamp(d, (xo1 + 3.6, y2 - 2.6), label="$A_2$")
    n2_, p2, o2 = a2.in1, a2.in2, a2.out
    nx2 = n2_[0] - 0.6
    wire(d, (xo1, y2), (xo1 + 0.6, y2))
    d.add(elm.Resistor().endpoints((xo1 + 0.6, y2), (nx2, y2)).label("$R/2$"))
    wire(d, (nx2, y2), (nx2, n2_[1]), n2_); dot(d, (nx2, n2_[1]))
    # ui 经 R 到 A2 反相端（底部走线）
    yb = -2.6
    wire(d, (0.4, 0), (0.4, yb))
    d.add(elm.Resistor().endpoints((0.4, yb), (nx2 - 1.4, yb)).label("$R$", loc="bot"))
    wire(d, (nx2 - 1.4, yb), (nx2 - 1.4, n2_[1]), (nx2, n2_[1])); dot(d, (nx2 - 1.4, n2_[1])) if False else None
    ox2 = o2[0] + 0.5
    yf = y2 + 1.2
    wire(d, (nx2, y2), (nx2, yf)); dot(d, (nx2, y2))
    d.add(elm.Resistor().endpoints((nx2, yf), (ox2, yf)).label("$R$"))
    wire(d, (ox2, yf), (ox2, o2[1])); wire(d, o2, (ox2, o2[1])); dot(d, (ox2, o2[1]))
    out_term(d, (ox2, o2[1]), length=0.9)
    wire(d, p2, (nx2 - 0.0, p2[1]), (nx2, p2[1] - 0.5)); gnd(d, (nx2, p2[1] - 0.5))
    save(d, "sp-rect")


def rect_wave():
    t = np.linspace(0, 2, 800)
    ui = 0.5 * np.sin(2 * np.pi * t)
    uo1 = np.where(ui > 0, -ui, 0)
    uo = np.abs(ui)
    fig, axs = plt.subplots(3, 1, figsize=(5.4, 4.0), sharex=True)
    for ax, y, lab, c in zip(axs, (ui, uo1, uo), ("$u_i$/V", "$u_{o1}$/V", "$u_o$/V"), (C2, C3, C1)):
        style(ax)
        ax.plot(t, y, color=c, lw=2)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_ylim(-0.65, 0.65)
        ax.set_yticks([-0.5, 0, 0.5])
        ax.set_ylabel(lab, color=INK)
    axs[-1].set_xlabel("$t/T$", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "sp-rect-wave")


# ---------------------------------------------------------------- Howland 电流源
def howland():
    d = new_drawing()
    op = opamp(d, (4.2, 0), flip=True)        # + 在上
    n1, n2, o = op.in1, op.in2, op.out        # n1=− 在下，n2=+ 在上
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    # + 端：R3 接 ui，R4 接输出，RL 对地
    xl = nx - 0.9
    term(d, (xl - 3.0, n2[1]), "$u_i$", dx=-0.5)
    d.add(elm.Resistor().endpoints((xl - 3.0, n2[1]), (xl, n2[1])).label("$R_3$"))
    wire(d, (xl, n2[1]), n2); dot(d, (nx, n2[1]))
    yt = n2[1] + 1.8
    wire(d, (nx, n2[1]), (nx, yt))
    d.add(elm.Resistor().endpoints((nx, yt), (ox, yt)).label("$R_4$"))
    wire(d, (ox, yt), (ox, o[1]))
    d.add(elm.Resistor().endpoints((xl, n2[1]), (xl, n2[1] - 2.2)).label("$R_L$", loc="top"))
    gnd(d, (xl, n2[1] - 2.2)); dot(d, (xl, n2[1]))
    d.add(elm.Arrow(headwidth=0.3, headlength=0.38).endpoints((xl - 1.1, n2[1] - 0.5), (xl - 1.1, n2[1] - 1.5)))
    text(d, (xl - 1.45, n2[1] - 1.0), "$i_L$")
    # − 端：R1 对地，R2 接输出
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    yb = n1[1] - 1.5
    wire(d, (nx, n1[1]), (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (ox, yb)).label("$R_2$", loc="bot"))
    wire(d, (ox, yb), (ox, o[1])); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.0)).label("$R_1$", loc="bot"))
    gnd(d, (nx, yb - 2.0))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    out_term(d, (ox, o[1]), length=0.8)
    save(d, "sp-howland")


# ---------------------------------------------------------------- 有源滤波
def lp1():
    d = new_drawing()
    op = opamp(d, (4.4, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    term(d, (0, n2[1]), "$u_i$", dx=-0.5)
    xc = 2.4
    d.add(elm.Resistor().endpoints((0, n2[1]), (xc, n2[1])).label("$R$"))
    wire(d, (xc, n2[1]), n2); dot(d, (xc, n2[1]))
    d.add(elm.Capacitor().endpoints((xc, n2[1]), (xc, n2[1] - 2.6)).label("$C$", loc="bot"))
    gnd(d, (xc, n2[1] - 2.6))
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    yb = n1[1] - 1.5
    wire(d, (nx, n1[1]), (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (ox, yb)).label("$R_f$", loc="bot"))
    wire(d, (ox, yb), (ox, o[1])); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 2.0)).label("$R_1$", loc="top"))
    gnd(d, (nx, yb - 2.0))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    out_term(d, (ox, o[1]), length=0.8)
    save(d, "sp-lp1")


def sallen_key():
    d = new_drawing()
    op = opamp(d, (7.0, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    ox = o[0] + 0.6
    y = n2[1]
    term(d, (0, y), "$u_i$", dx=-0.5)
    xa, xp = 2.6, 5.2
    d.add(elm.Resistor().endpoints((0, y), (xa, y)).label("$R_1$"))
    d.add(elm.Resistor().endpoints((xa, y), (xp, y)).label("$R_2$"))
    wire(d, (xp, y), n2); dot(d, (xa, y)); dot(d, (xp, y))
    text(d, (xa, y - 0.45), "$a$")
    yt = y + 2.0
    wire(d, (xa, y), (xa, yt))
    d.add(elm.Capacitor().endpoints((xa, yt), (ox, yt)).label("$C_1$"))
    wire(d, (ox, yt), (ox, o[1]))
    d.add(elm.Capacitor().endpoints((xp, y), (xp, y - 3.0)).label("$C_2$", loc="bot"))
    gnd(d, (xp, y - 3.0))
    # 同相放大部分：K = 1 + Rb/Ra
    wire(d, n1, (nx, n1[1])); dot(d, (nx, n1[1]))
    yb = n1[1] - 1.5
    wire(d, (nx, n1[1]), (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (ox, yb)).label("$R_b$", loc="bot"))
    wire(d, (ox, yb), (ox, o[1])); dot(d, (nx, yb))
    d.add(elm.Resistor().endpoints((nx, yb), (nx, yb - 1.8)).label("$R_a$", loc="top"))
    gnd(d, (nx, yb - 1.8))
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    out_term(d, (ox, o[1]), length=0.8)
    note(d, (nx + 3.4, yb - 1.9), "$K=1+R_b/R_a$\n（单位增益：$R_b=0$, $R_a$ 开路）")
    save(d, "sp-sk")


def filter_bode():
    w = np.logspace(-1.3, 1.3, 600)
    fig, ax = axes(5.8, 3.4)
    ax.set_xscale("log")
    for q, c, lab in ((0.5, C3, "$Q=0.5$（单位增益、等 R 等 C）"), (1 / math.sqrt(2), C1, "$Q=0.707$（Butterworth）"),
                      (2.0, C2, "$Q=2$")):
        H = 1 / (1 - w ** 2 + 1j * w / q)
        ax.plot(w, 20 * np.log10(abs(H)), color=c, lw=2, label=lab)
    ax.plot(w, 20 * np.log10(abs(1 / (1 + 1j * w))), color=MUTED, lw=1.5, ls="--", label="一阶（$-20$ dB/dec）")
    ax.axhline(-3, color=MUTED, lw=0.8, ls=":")
    ax.text(6, -1.6, "$-3$ dB", color=MUTED, fontsize=9)
    ax.set_ylim(-45, 10)
    ax.set_xlabel("$f/f_0$", color=INK, loc="right")
    ax.set_ylabel("$20\\lg|A/A_p|$/dB", color=INK)
    ax.legend(fontsize=9, frameon=False, loc="lower left")
    ax.grid(True, which="both", color="#dddddd", lw=0.6)
    fig.tight_layout()
    save_fig(fig, "sp-filter-bode")


# ---------------------------------------------------------------- 比较器
def zener_out(d, o, x_out=1.2, drop=2.4):
    """运放输出 → R_O → u_o，u_o 与地之间接双向稳压管 ±U_Z。返回 u_o 点。"""
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
    out_term(d, q, length=x_out)
    return q


def schmitt_inv():
    d = new_drawing()
    op = opamp(d, (3.0, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    term(d, (0.6, 0), "$u_i$", dx=-0.5)
    wire(d, (0.6, 0), n1)
    q = zener_out(d, o)
    # + 端：R1 接 U_REF（向左），R_F 接 u_o（下方回绕）
    py = n2[1]
    wire(d, n2, (nx, py)); dot(d, (nx, py))
    d.add(elm.Resistor().endpoints((nx, py), (nx - 2.4, py)).label("$R_1$", loc="bot"))
    term(d, (nx - 2.4, py), "$U_{REF}$", dx=-0.85)
    yf = py - 2.9
    xr = q[0] + 0.6
    wire(d, (nx, py), (nx, yf))
    d.add(elm.Resistor().endpoints((xr, yf), (nx, yf)).label("$R_F$", loc="bot"))
    wire(d, (xr, yf), (xr, o[1])); dot(d, (xr, o[1]))
    save(d, "sp-schmitt-inv")


def schmitt_noninv():
    d = new_drawing()
    op = opamp(d, (4.0, 0), flip=True)
    n1, n2, o = op.in1, op.in2, op.out          # + 在上
    nx = n1[0] - 0.6
    term(d, (0, n2[1]), "$u_i$", dx=-0.5)
    d.add(elm.Resistor().endpoints((0, n2[1]), (nx, n2[1])).label("$R_1$"))
    wire(d, (nx, n2[1]), n2); dot(d, (nx, n2[1]))
    q = zener_out(d, o)
    yt = n2[1] + 1.8
    xr = q[0] + 0.6
    wire(d, (nx, n2[1]), (nx, yt))
    d.add(elm.Resistor().endpoints((nx, yt), (xr, yt)).label("$R_2$"))
    wire(d, (xr, yt), (xr, o[1])); dot(d, (xr, o[1]))
    wire(d, n1, (nx - 1.2, n1[1]))
    term(d, (nx - 1.2, n1[1]), "$U_{REF}$", dx=-0.85)
    save(d, "sp-schmitt-ni")


def window():
    d = new_drawing()
    a1 = opamp(d, (3.0, 2.0), flip=True, label="$A_1$")     # + 在上：接 ui
    a2 = opamp(d, (3.0, -1.5), label="$A_2$")               # − 在上：接 ui
    xi = 0.6
    term(d, (0, a1.in2[1]), "$u_i$", dx=-0.5)
    wire(d, (0, a1.in2[1]), a1.in2)
    dot(d, (xi, a1.in2[1]))
    wire(d, (xi, a1.in2[1]), (xi, a2.in1[1]), a2.in1)
    wire(d, a1.in1, (1.6, a1.in1[1])); term(d, (1.6, a1.in1[1]), "$U_{RH}$", dx=-0.75)
    wire(d, a2.in2, (1.6, a2.in2[1])); term(d, (1.6, a2.in2[1]), "$U_{RL}$", dx=-0.75)
    xo = a1.out[0] + 2.4
    ym = (a1.out[1] + a2.out[1]) / 2
    d.add(elm.Diode().endpoints(a1.out, (xo, a1.out[1])).label("$D_1$"))
    d.add(elm.Diode().endpoints(a2.out, (xo, a2.out[1])).label("$D_2$", loc="bot"))
    wire(d, (xo, a1.out[1]), (xo, a2.out[1])); dot(d, (xo, ym))
    wire(d, (xo, ym), (xo + 0.9, ym))
    d.add(elm.Resistor().endpoints((xo + 0.9, ym), (xo + 0.9, ym - 2.4)).label("$R$", loc="bot"))
    gnd(d, (xo + 0.9, ym - 2.4)); dot(d, (xo + 0.9, ym))
    out_term(d, (xo + 0.9, ym), length=1.0)
    save(d, "sp-window")


def transfer():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.9))
    for ax in axs:
        style(ax)
        ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
        ax.set_xlabel("$u_i$/V", color=INK, loc="right")
    kw = dict(color=C1, lw=2)
    ar = dict(arrowstyle="-|>", color=C2, lw=1.4, mutation_scale=14)
    # 反相滞回（图卡例）
    a = axs[0]
    a.plot([-4, 2, 2], [10, 10, -10], **kw)
    a.plot([4, -2, -2], [-10, -10, 10], **kw)
    a.annotate("", xy=(1.3, 10), xytext=(-0.5, 10), arrowprops=ar)
    a.annotate("", xy=(-1.3, -10), xytext=(0.5, -10), arrowprops=ar)
    a.annotate("", xy=(2, -6), xytext=(2, 6), arrowprops=ar)
    a.annotate("", xy=(-2, 6), xytext=(-2, -6), arrowprops=ar)
    a.set_xticks([-2, 2]); a.set_yticks([-10, 10]); a.set_ylim(-13, 13)
    a.set_ylabel("$u_o$/V", color=INK)
    a.set_title("反相滞回（$\\pm2$ V）", fontsize=11, color=INK)
    # 同相滞回（练习：+3.33 / −0.67）
    a = axs[1]
    hi, lo = 10 / 3, -2 / 3
    a.plot([-3, hi, hi], [-6, -6, 6], **kw)
    a.plot([6, lo, lo], [6, 6, -6], **kw)
    a.annotate("", xy=(2.6, -6), xytext=(0.6, -6), arrowprops=ar)
    a.annotate("", xy=(0.2, 6), xytext=(2.2, 6), arrowprops=ar)
    a.annotate("", xy=(hi, 3.5), xytext=(hi, -3.5), arrowprops=ar)
    a.annotate("", xy=(lo, -3.5), xytext=(lo, 3.5), arrowprops=ar)
    a.set_xticks([lo, 1, hi], ["$-0.67$", "1", "3.33"]); a.set_yticks([-6, 6]); a.set_ylim(-8, 8)
    a.set_title("同相滞回（$U_{REF}=1$ V）", fontsize=11, color=INK)
    # 窗口
    a = axs[2]
    a.plot([0, 2, 2, 4, 4, 6], [5, 5, 0, 0, 5, 5], **kw)
    a.set_xticks([2, 4], ["$U_{RL}$", "$U_{RH}$"]); a.set_yticks([0, 5], ["0", "$U_{OH}$"])
    a.set_ylim(-1.5, 7)
    a.set_title("窗口比较器", fontsize=11, color=INK)
    fig.tight_layout()
    save_fig(fig, "sp-transfer")


if __name__ == "__main__":
    log_amp()
    exp_amp()
    rectifier()
    rect_wave()
    howland()
    lp1()
    sallen_key()
    filter_bode()
    schmitt_inv()
    schmitt_noninv()
    window()
    transfer()
