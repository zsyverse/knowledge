"""模电·信号与放大器 插图（前缀 sa-）。

运放一律用 opamp()：in1 为反相输入（−），in2 为同相输入（+）；flip=True 时 + 在上。
"""
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig, dot, text, cur, wire, opamp, gnd, ac_src,
                     axes, plt, C1, C2, C3, MUTED, INK, GRID)

K = "\\,\\mathrm{k}\\Omega"


def fsave(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    save_fig(fig, name)


def dashed_box(d, x1, y1, x2, y2, label=None):
    for p, q in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        d.add(elm.Line().endpoints(p, q).linestyle("--").color(MUTED))
    if label:
        text(d, ((x1 + x2) / 2, y2 + 0.4), label, color=MUTED, fontsize=13)


def vpm(d, x, ytop, ybot, name):
    text(d, (x, ytop - 0.35), "+")
    text(d, (x, (ytop + ybot) / 2), name)
    text(d, (x, ybot + 0.35), "−")


# ---------------------------------------------------------------- 电压放大模型（含源与负载）
def vamp_model():
    d = new_drawing()
    H = 3.0
    ac_src(d, (0, 0), (0, H), "$v_s$", loc="bot")
    d.add(elm.Resistor().endpoints((0, H), (2.4, H)).label("$R_s$"))
    dot(d, (2.4, H), True); dot(d, (2.4, 0), True)
    wire(d, (2.4, H), (3.9, H))
    d.add(elm.Resistor().endpoints((3.9, H), (3.9, 0)).label("$R_i$", loc="bot"))
    vpm(d, 2.75, H, 0, "$v_i$")
    d.add(elm.SourceControlledV().endpoints((5.4, 0), (5.4, H)).label("$A_{vo}v_i$", loc="bot"))
    d.add(elm.Resistor().endpoints((5.4, H), (7.4, H)).label("$R_o$"))
    dot(d, (7.4, H), True); dot(d, (7.4, 0), True)
    wire(d, (7.4, H), (9.0, H))
    d.add(elm.Resistor().endpoints((9.0, H), (9.0, 0)).label("$R_L$", loc="bot"))
    vpm(d, 7.9, H, 0, "$v_o$")
    wire(d, (0, 0), (9.0, 0))
    dot(d, (3.9, 0)); dot(d, (5.4, 0))
    dashed_box(d, 3.2, -0.4, 7.05, H + 0.6, "放大器")
    text(d, (1.2, -0.75), "信号源", color=MUTED, fontsize=13)
    text(d, (9.0, -0.75), "负载", color=MUTED, fontsize=13)
    save(d, "sa-vamp-model")


# ---------------------------------------------------------------- 四种放大器模型
def panel(d, x0, y0, kind, title):
    H = 3.0
    xr, xs, xo = x0 + 1.3, x0 + 3.2, x0 + 6.2
    dot(d, (x0, y0 + H), True); dot(d, (x0, y0), True)
    if kind in ("v", "g"):
        wire(d, (x0, y0 + H), (xr, y0 + H))
        vpm(d, x0 - 0.45, y0 + H, y0, "$v_i$")
    else:
        cur(d, (x0, y0 + H), (xr, y0 + H), "$i_i$", frac=0.45)
    d.add(elm.Resistor().endpoints((xr, y0 + H), (xr, y0)).label("$R_i$", loc="bot"))
    if kind in ("v", "r"):     # 戴维南型输出：受控电压源串 R_o
        lab = "$A_{vo}v_i$" if kind == "v" else "$R_m i_i$"
        d.add(elm.SourceControlledV().endpoints((xs, y0), (xs, y0 + H)).label(lab, loc="bot"))
        d.add(elm.Resistor().endpoints((xs, y0 + H), (xo, y0 + H)).label("$R_o$"))
        dot(d, (xs, y0))
    else:                      # 诺顿型输出：受控电流源并 R_o
        lab = "$G_m v_i$" if kind == "g" else "$A_{is}i_i$"
        d.add(elm.SourceControlledI().endpoints((xs, y0), (xs, y0 + H)).label(lab, loc="bot"))
        xp = xs + 2.2
        wire(d, (xs, y0 + H), (xo, y0 + H))
        d.add(elm.Resistor().endpoints((xp, y0 + H), (xp, y0)).label("$R_o$", loc="bot"))
        dot(d, (xp, y0 + H)); dot(d, (xp, y0)); dot(d, (xs, y0))
    dot(d, (xo, y0 + H), True); dot(d, (xo, y0), True)
    wire(d, (x0, y0), (xo, y0))
    dot(d, (xr, y0))
    text(d, (x0 + 3.1, y0 - 0.8), title, fontsize=14)


def models4():
    d = new_drawing()
    panel(d, 0, 5.2, "v", "(a) 电压放大：$R_i\\to\\infty$，$R_o\\to0$")
    panel(d, 9.6, 5.2, "i", "(b) 电流放大：$R_i\\to0$，$R_o\\to\\infty$")
    panel(d, 0, 0, "g", "(c) 互导放大：$R_i\\to\\infty$，$R_o\\to\\infty$")
    panel(d, 9.6, 0, "r", "(d) 互阻放大：$R_i\\to0$，$R_o\\to0$")
    save(d, "sa-models4")


# ---------------------------------------------------------------- 运放的等效电路
def opamp_equiv():
    d = new_drawing()
    dot(d, (0, 2.6), True); text(d, (-0.55, 2.6), "$u_+$")
    dot(d, (0, 0), True); text(d, (-0.55, 0), "$u_-$")
    wire(d, (0, 2.6), (1.6, 2.6)); wire(d, (0, 0), (1.6, 0))
    d.add(elm.Resistor().endpoints((1.6, 2.6), (1.6, 0)).label("$R_{id}$", loc="bot"))
    vpm(d, 1.0, 2.6, 0, "$u_d$")
    d.add(elm.SourceControlledV().endpoints((4.2, -0.6), (4.2, 2.6)).label("$A\\,u_d$", loc="bot"))
    gnd(d, (4.2, -0.6))
    d.add(elm.Resistor().endpoints((4.2, 2.6), (6.4, 2.6)).label("$R_o$"))
    dot(d, (6.4, 2.6), True); text(d, (6.95, 2.6), "$u_o$")
    dashed_box(d, 0.5, -0.35, 6.0, 3.3)
    save(d, "sa-opamp-equiv")


# ---------------------------------------------------------------- 例题电路
def noninv():
    d = new_drawing()
    op = opamp(d, (4.5, 0), flip=True)          # + 在上
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    dot(d, (nx - 2.2, n2[1]), True); text(d, (nx - 2.8, n2[1]), "$v_i$")
    wire(d, (nx - 2.2, n2[1]), n2)
    wire(d, n1, (nx, n1[1]))
    ox = o[0] + 0.6
    wire(d, o, (ox, o[1])); dot(d, (ox, o[1]))
    y = n1[1] - 1.6
    wire(d, (nx, n1[1]), (nx, y))
    d.add(elm.Resistor().endpoints((nx, y), (ox, y)).label(f"$R_f=90{K}$", loc="bot"))
    wire(d, (ox, y), (ox, o[1]))
    dot(d, (nx, n1[1]))
    d.add(elm.Resistor().endpoints((nx, n1[1]), (nx - 2.2, n1[1])).label(f"$R_1=10{K}$", loc="top"))
    wire(d, (nx - 2.2, n1[1]), (nx - 2.2, n1[1] - 0.5)); gnd(d, (nx - 2.2, n1[1] - 0.5))
    wire(d, (ox, o[1]), (ox + 0.9, o[1])); dot(d, (ox + 0.9, o[1]), True)
    text(d, (ox + 1.45, o[1]), "$v_o$")
    text(d, (op.center[0] + 0.1, op.center[1] + 1.6), "$\\pm12\\,\\mathrm{V}$", color=MUTED, fontsize=13)
    save(d, "sa-noninv")


def inv():
    d = new_drawing()
    op = opamp(d, (4.5, 0))
    n1, n2, o = op.in1, op.in2, op.out
    nx = n1[0] - 0.6
    dot(d, (0, n1[1]), True); text(d, (-0.55, n1[1]), "$v_i$")
    d.add(elm.Resistor().endpoints((0, n1[1]), (nx, n1[1])).label(f"$R_1=10{K}$"))
    wire(d, (nx, n1[1]), n1)
    ox = o[0] + 0.6
    y = n1[1] + 1.4
    wire(d, (nx, n1[1]), (nx, y))
    d.add(elm.Resistor().endpoints((nx, y), (ox, y)).label(f"$R_f=30{K}$"))
    wire(d, (ox, y), (ox, o[1]))
    dot(d, (nx, n1[1])); dot(d, (ox, o[1]))
    wire(d, o, (ox, o[1]))
    wire(d, (ox, o[1]), (ox + 0.9, o[1])); dot(d, (ox + 0.9, o[1]), True)
    text(d, (ox + 1.45, o[1]), "$v_o$")
    wire(d, n2, (nx, n2[1]), (nx, n2[1] - 0.5)); gnd(d, (nx, n2[1] - 0.5))
    text(d, (op.center[0] + 0.2, op.center[1] - 1.5), "$\\pm15\\,\\mathrm{V}$", color=MUTED, fontsize=13)
    save(d, "sa-inv")


# ---------------------------------------------------------------- 采样与量化
def sampling():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.6))
    t = np.linspace(0, 1, 500)
    f = lambda x: 1.6 * np.sin(2 * np.pi * 1.3 * x) + 0.7 * np.sin(2 * np.pi * 2.9 * x + 0.5)
    n = np.arange(0, 13)
    Ts = 1 / 12
    xs = f(n * Ts)
    D = 0.5
    q = np.round(xs / D) * D
    for ax in axs:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(MUTED); ax.spines["bottom"].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.set_ylim(-2.7, 2.7)
        ax.axhline(0, color=MUTED, lw=0.6)
    axs[0].plot(t, f(t), color=C1, lw=2)
    axs[0].set_title("模拟量：时间、幅值都连续", fontsize=11, color=INK)
    axs[0].set_xlabel("$t$", color=INK, loc="right"); axs[0].set_yticks([]); axs[0].set_xticks([])
    axs[0].set_ylabel("$v(t)$", color=INK)
    axs[1].plot(t / Ts, f(t), color=GRID, lw=1.2)
    axs[1].stem(n, xs, linefmt=C1, markerfmt="o", basefmt=" ")
    axs[1].set_title("离散时间：采样 $v[n]=v(nT_s)$", fontsize=11, color=INK)
    axs[1].set_xlabel("$n$", color=INK, loc="right"); axs[1].set_yticks([])
    for lv in np.arange(-2.5, 2.6, D):
        axs[2].axhline(lv, color=GRID, lw=0.8, ls="--")
    axs[2].stem(n, q, linefmt=C2, markerfmt="o", basefmt=" ")
    axs[2].plot(n, xs, "x", color=MUTED, ms=5)
    axs[2].set_title("数字量：量化到 $\\Delta$ 的整数倍", fontsize=11, color=INK)
    axs[2].set_xlabel("$n$", color=INK, loc="right")
    axs[2].set_yticks([0, D], ["0", "$\\Delta$"])
    for ax in axs[1:]:
        ax.set_xlim(-0.5, 12.8)
    fig.tight_layout()
    fsave(fig, "sa-sampling")


def aliasing():
    fig, ax = axes(6.4, 2.6)
    t = np.linspace(0, 2e-3, 2000)
    fs = 8e3
    n = np.arange(0, 17)
    ax.plot(t * 1e3, np.cos(2 * np.pi * 7e3 * t), color=C1, lw=1.2, label="7 kHz 原信号")
    ax.plot(t * 1e3, np.cos(2 * np.pi * 1e3 * t), color=C2, lw=1.8, ls="--", label="1 kHz 混叠信号")
    ax.plot(n / fs * 1e3, np.cos(2 * np.pi * 7e3 * n / fs), "o", color=INK, ms=5, label="$f_s=8$ kHz 的采样点")
    ax.set_xlabel("$t$ / ms", color=INK); ax.set_ylim(-1.3, 1.6); ax.set_xlim(0, 2)
    ax.legend(loc="upper center", ncol=3, fontsize=9, frameon=False)
    fsave(fig, "sa-aliasing")


def clipping():
    fig, ax = axes(6.4, 2.8)
    th = np.linspace(0, 4 * np.pi, 1000)
    vi = 1.5 * np.sin(th)
    vo = np.clip(-10 * vi, -12, 12)
    ax.plot(th / (2 * np.pi), vi, color=C1, lw=1.6, label="$v_i$（$1.5\\,$V 峰值）")
    ax.plot(th / (2 * np.pi), -10 * vi, color=GRID, lw=1.2, ls="--", label="理想 $-10v_i$")
    ax.plot(th / (2 * np.pi), vo, color=C2, lw=2, label="实际 $v_o$")
    ax.axhline(12, color=MUTED, lw=0.8, ls=":"); ax.axhline(-12, color=MUTED, lw=0.8, ls=":")
    ax.set_yticks([-15, -12, 0, 12, 15])
    ax.set_xticks([0, 0.5, 1, 1.5, 2], ["0", "$T/2$", "$T$", "$3T/2$", "$2T$"])
    ax.set_ylabel("电压 / V", color=INK)
    ax.set_ylim(-17, 21)
    ax.legend(loc="upper center", ncol=3, fontsize=9, frameon=False)
    fsave(fig, "sa-clipping")


if __name__ == "__main__":
    vamp_model()
    models4()
    opamp_equiv()
    noninv()
    inv()
    sampling()
    aliasing()
    clipping()
