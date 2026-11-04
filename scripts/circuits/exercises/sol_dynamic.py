"""习题·动态电路 解析插图（images/ex/sol/d-*）。数值见 verify_dynamic.py。"""
import numpy as np

from solcommon import (elm, new_drawing, ssave, sfig, dot, text, note, cur, arrow, vsrc, isrc, wire,
                       first_order_wave, axes, OHM, C1, C2, C3, INK, MUTED)


def short(d, p, q, lab, loc="top"):
    """储能元件在直流稳态下的短路线（标注原元件）。"""
    d.add(elm.Line().endpoints(p, q).label(lab, loc=loc, color=MUTED, fontsize=12))


def opened(d, p, q, lab, val=None, side="right"):
    """电容开路（竖直，p 在上）：两端子之间留空，右侧标出电压极性（p 为 +）与数值，左侧注明元件。"""
    dot(d, p, True); dot(d, q, True)
    x, ym = p[0], (p[1] + q[1]) / 2
    text(d, (x + 0.25, p[1] - 0.4), "+"); text(d, (x + 0.25, q[1] + 0.4), "−")
    if val:
        text(d, (x + 0.2, ym), val, halign="left")
    note(d, (x + 0.1, ym), lab, halign="right")


# ------------------------------------------------------------------ 题2 作业 7-3
def d73_0m():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$24\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3, 4)).label(f"$R_1=1{OHM}$"))
    cur(d, (3, 4), (4.2, 4), "$i(0_-)=4\\,\\mathrm{A}$", loc="top")
    short(d, (4.2, 4), (7, 4), "$L$ 短路", loc="bot")
    dot(d, (7, 4)); dot(d, (7, 0))
    d.add(elm.Resistor().endpoints((7, 4), (7, 0)).label(f"$R_2=5{OHM}$", loc="top"))
    wire(d, (7, 4), (9.5, 4), (9.5, 3.0))
    wire(d, (9.5, 1.0), (9.5, 0), (0, 0))
    opened(d, (9.5, 3.0), (9.5, 1.0), "$C$ 开路", "$u_C(0_-)=20\\,\\mathrm{V}$")
    note(d, (2.0, 5.2), "$S$ 在位置 1")
    ssave(d, "d-73-0m")


def d73_0p():
    d = new_drawing()
    wire(d, (0, 0), (0, 4))
    note(d, (-1.0, 2.0), "经触点 2\n接下边线")
    e = elm.SourceI().endpoints((0, 4), (3.6, 4)).label("$i(0_+)=4\\,\\mathrm{A}$", loc="top") \
        .label(("+", "$u_L$", "−"), loc="bot")
    d.add(e)
    dot(d, (3.6, 4)); dot(d, (3.6, 0))
    d.add(elm.Resistor().endpoints((3.6, 4), (3.6, 0)).label(f"$5{OHM}$", loc="bot"))
    note(d, (2.4, 2.0), "$4\\,\\mathrm{A}\\downarrow$")
    wire(d, (3.6, 4), (6.6, 4))
    vsrc(d, (6.6, 0), (6.6, 4), "$u_C(0_+)=20\\,\\mathrm{V}$", loc="bot")
    arrow(d, (5.6, 3.6), (5.6, 2.4), "$i_C$", loc="top")
    wire(d, (0, 0), (6.6, 0))
    ssave(d, "d-73-0p")


# ------------------------------------------------------------------ 题3 RC
def drc_0m():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$18\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4.5), (3.5, 4.5)).label(f"$6{OHM}$"))
    dot(d, (3.5, 4.5)); text(d, (3.5, 5.0), "$a$")
    d.add(elm.Resistor().endpoints((3.5, 4.5), (3.5, 0)).label(f"$3{OHM}$", loc="bot"))
    note(d, (2.4, 2.25), "$S$ 闭合")
    d.add(elm.Resistor().endpoints((3.5, 4.5), (7, 4.5)).label(f"$2{OHM}$").label("无电流", loc="bot", color=MUTED, fontsize=12))
    wire(d, (7, 4.5), (7, 3.3))
    wire(d, (7, 1.2), (7, 0), (0, 0))
    opened(d, (7, 3.3), (7, 1.2), "$C$ 开路", "$u_C=u_a=6\\,\\mathrm{V}$")
    dot(d, (3.5, 0))
    ssave(d, "d-rc-0m")


def drc_req():
    d = new_drawing()
    wire(d, (0, 0), (0, 2.5))
    note(d, (-0.3, 1.25), "电压源\n短路", halign="right")
    d.add(elm.Resistor().endpoints((0, 2.5), (3.5, 2.5)).label(f"$6{OHM}$"))
    dot(d, (3.5, 2.5)); text(d, (3.5, 3.0), "$a$")
    d.add(elm.Resistor().endpoints((3.5, 2.5), (7, 2.5)).label(f"$2{OHM}$"))
    wire(d, (0, 0), (7, 0))
    dot(d, (7, 2.5), True); dot(d, (7, 0), True)
    arrow(d, (8.6, 1.25), (7.3, 1.25), None)
    text(d, (8.8, 1.25), "$R_{eq}=6+2=8\\,\\Omega$", halign="left")
    note(d, (3.5, 1.0), "$S$ 断开，$3\\,\\Omega$ 支路不接入")
    ssave(d, "d-rc-req")


def drc_wave():
    def ex(ax):
        ax.text(6.0, 10.0, "$u_C=18-12e^{-t/4}$", color=INK, fontsize=11)
        ax.text(6.0, 7.4, "$\\tau=8\\times0.5=4\\,\\mathrm{s}$", color=INK, fontsize=10)
    first_order_wave("d-rc-wave", 6, 18, 4, "$u_C$", "V", f0m=6, extra=ex, zero=False)


# ------------------------------------------------------------------ 题4 RL
def _rl(d, closed, l_src):
    isrc(d, (0, 0), (0, 4.5), "$6\\,\\mathrm{A}$")
    wire(d, (0, 4.5), (9.5, 4.5))
    dot(d, (3, 4.5)); text(d, (3, 5.0), "$a$")
    d.add(elm.Resistor().endpoints((3, 4.5), (3, 0)).label(f"$3{OHM}$", loc="bot"))
    dot(d, (6.2, 4.5))
    if closed:
        d.add(elm.Resistor().endpoints((6.2, 4.5), (6.2, 0)).label(f"$6{OHM}$", loc="bot"))
        note(d, (5.2, 2.25), "$S$\n闭合")
        dot(d, (6.2, 0))
    else:
        d.add(elm.Switch().endpoints((6.2, 4.5), (6.2, 2.5)).label("$S$ 断开", loc="bot"))
        d.add(elm.Resistor().endpoints((6.2, 2.5), (6.2, 0)).label(f"$6{OHM}$", loc="bot"))
        dot(d, (6.2, 0))
    d.add(elm.Resistor().endpoints((9.5, 4.5), (9.5, 2.5)).label(f"$1{OHM}$", loc="bot"))
    l_src(d)
    wire(d, (0, 0), (9.5, 0))
    dot(d, (3, 0))


def drl_0m():
    d = new_drawing()
    _rl(d, False, lambda d: short(d, (9.5, 2.5), (9.5, 0), "$L$ 短路", loc="bot"))
    arrow(d, (10.4, 4.0), (10.4, 2.8), "$i_L(0_-)=4.5\\,\\mathrm{A}$", loc="bot")
    ssave(d, "d-rl-0m")


def drl_0p():
    d = new_drawing()
    _rl(d, True, lambda d: isrc(d, (9.5, 2.5), (9.5, 0), "$i_L(0_+)=4.5\\,\\mathrm{A}$", loc="bot"))
    note(d, (4.75, -0.8), "$a$ 点 KCL：$6=u_a/3+u_a/6+4.5\\ \\Rightarrow\\ u_a(0_+)=3\\,\\mathrm{V}$")
    ssave(d, "d-rl-0p")


def drl_req():
    d = new_drawing()
    note(d, (2.4, 2), "电流源开路\n（支路去掉）", halign="right")
    dot(d, (3, 4)); dot(d, (3, 0))
    d.add(elm.Resistor().endpoints((3, 4), (3, 0)).label(f"$3{OHM}$", loc="bot"))
    wire(d, (3, 4), (6, 4)); wire(d, (3, 0), (6, 0))
    dot(d, (6, 4)); dot(d, (6, 0))
    d.add(elm.Resistor().endpoints((6, 4), (6, 0)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((6, 4), (9.5, 4)).label(f"$1{OHM}$"))
    wire(d, (6, 0), (9.5, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    arrow(d, (11.0, 2), (9.8, 2), None)
    text(d, (11.5, 1.2), "$R_{eq}=1+3\\parallel6=3\\,\\Omega$")
    ssave(d, "d-rl-req")


def drl_ua():
    def ex(ax):
        ax.annotate("$u_a$ 在 $t=0$ 由 $4.5$ 跳到 $3$", (0.02, 3.0), (0.9, 3.15), fontsize=10, color=INK,
                    arrowprops=dict(arrowstyle="->", color=MUTED))
        ax.text(1.6, 3.62, "$u_a=4-e^{-1.5t}$，$\\tau=\\frac{2}{3}\\,\\mathrm{s}$", color=INK, fontsize=10, va="top")
    first_order_wave("d-rl-ua", 3, 4, 2 / 3, "$u_a$", "V", f0m=4.5, extra=ex, zero=False)


# ------------------------------------------------------------------ 题5 作业 7-4
def d74_wave():
    fig, ax = axes()
    tau = 2 / 3
    t = np.linspace(0, 5 * tau, 300)
    tl = -0.6
    ax.axvline(0, color=MUTED, lw=0.8)
    i1 = 3 - 2 * np.exp(-t / tau); i2 = 3 - np.exp(-t / tau)
    ax.plot([tl, 0], [1, 1], color=C1, lw=2); ax.plot(t, i1, color=C1, lw=2, label="$i_1=3-2e^{-1.5t}$")
    ax.plot([tl, 0], [2, 2], color=C2, lw=2); ax.plot(t, i2, color=C2, lw=2, label="$i_2=3-e^{-1.5t}$")
    ax.axhline(3, color=MUTED, ls="--", lw=1)
    ax.text(3.0, 3.12, "$i_1(\\infty)=i_2(\\infty)=3\\,\\mathrm{A}$", fontsize=10, color=INK, ha="right", va="bottom")
    ax.set_xlim(tl, 5 * tau); ax.set_ylim(0, 3.6)
    ax.set_yticks([0, 1, 2, 3]); ax.set_xticks([0, 2 / 3, 4 / 3, 2, 8 / 3, 10 / 3],
                                               ["0", "$\\tau$", "$2\\tau$", "$3\\tau$", "$4\\tau$", "$5\\tau$"])
    ax.set_xlabel("$t$", color=INK, loc="right"); ax.set_ylabel("电流/A", color=INK)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    ax.text(-0.3, 1.12, "$i_1$", fontsize=10, color=C1, ha="center", va="bottom")
    ax.text(-0.3, 2.12, "$i_2$", fontsize=10, color=C2, ha="center", va="bottom")
    sfig(fig, "d-74-wave")


# ------------------------------------------------------------------ 题6 作业 7-5
def d75_charge():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 6), "$9\\,\\mathrm{V}$")
    wire(d, (0, 6), (7, 6)); wire(d, (0, 0), (7, 0))
    d.add(elm.Resistor().endpoints((3.5, 6), (3.5, 3)).label(f"$R_1=1{OHM}$", loc="top"))
    d.add(elm.Capacitor().endpoints((3.5, 3), (3.5, 0)).label("$C_2=2\\,\\mathrm{F}$", loc="top")
          .label(("+", "", "−"), loc="bot"))
    d.add(elm.Capacitor().endpoints((7, 6), (7, 3)).label("$C_1=1\\,\\mathrm{F}$", loc="bot")
          .label(("+", "", "−"), loc="top"))
    d.add(elm.Resistor().endpoints((7, 3), (7, 0)).label(f"$R_2=2{OHM}$", loc="bot"))
    wire(d, (3.5, 3), (7, 3))
    note(d, (5.4, 2.1), "$S$ 闭合")
    for p in ((3.5, 6), (3.5, 0), (3.5, 3), (7, 3), (7, 6), (7, 0)):
        dot(d, p)
    # 闭合面：穿过两电容介质，切断两电阻引线
    pts = [(2.9, 1.5), (2.9, 3.45), (6.55, 3.45), (6.55, 4.5), (7.55, 4.5), (7.55, 2.55), (4.0, 2.55),
           (4.0, 1.5), (2.9, 1.5)]
    for a, b in zip(pts, pts[1:]):
        d.add(elm.Line().endpoints(a, b).color(C2).linestyle("--").linewidth(1.2))
    text(d, (9.6, 4.1), "$-C_1u_{C1}$", color=C2)
    text(d, (1.3, 1.95), "$+C_2u_{C2}$", color=C2)
    ssave(d, "d-75-charge")


# ------------------------------------------------------------------ 题7 作业 7-10
def d710_req():
    d = new_drawing()
    dot(d, (0, 4.5), True); dot(d, (0, 0), True)
    note(d, (-0.9, 2.25), "$I_S$\n开路")
    wire(d, (0, 4.5), (3, 4.5)); wire(d, (0, 0), (3, 0))
    dot(d, (3, 4.5)); dot(d, (3, 0))
    d.add(elm.Resistor().endpoints((3, 4.5), (3, 2.25)).label(f"$1{OHM}$", loc="bot"))
    d.add(elm.SourceControlledV().endpoints((3, 0), (3, 2.25)).label("$1.5i$", loc="bot"))
    d.add(elm.Resistor().endpoints((3, 4.5), (7, 4.5)).label(f"$1{OHM}$"))
    arrow(d, (4.2, 5.4), (5.8, 5.4), None); text(d, (5.0, 5.85), "$i$")
    dot(d, (7, 4.5)); dot(d, (7, 0))
    d.add(elm.Resistor().endpoints((7, 4.5), (7, 0)).label(f"$1{OHM}$", loc="bot"))
    cur(d, (10, 4.5), (7, 4.5), "$i_t$", loc="top", frac=0.45)
    vsrc(d, (10, 0), (10, 4.5), "$u$", loc="bot")
    wire(d, (7, 0), (10, 0))
    text(d, (5.0, -1.0), "$R_{eq}=u/i_t=(2-\\beta)/(3-\\beta)=1/3\\,\\Omega$")
    ssave(d, "d-710-req")


# ------------------------------------------------------------------ 题8 作业 7-12
def d712_0m():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$12\\,\\mathrm{V}$")
    cur(d, (0, 4.5), (1.0, 4.5), "$i_1=0.3\\,\\mathrm{A}$", loc="top", frac=0.6)
    d.add(elm.Resistor().endpoints((1.0, 4.5), (3.8, 4.5)).label(f"$20{OHM}$", loc="bot"))
    dot(d, (3.8, 4.5))
    wire(d, (3.8, 4.5), (3.8, 3.4)); wire(d, (3.8, 1.1), (3.8, 0))
    opened(d, (3.8, 3.4), (3.8, 1.1), "$C_1$", "$6\\,\\mathrm{V}$", side="right")
    wire(d, (3.8, 4.5), (7, 4.5))
    note(d, (5.4, 5.0), "$S$ 闭合")
    dot(d, (7, 4.5)); dot(d, (7, 0))
    d.add(elm.SourceControlledV().endpoints((7, 0), (7, 4.5)).label("$ri_1=6\\,\\mathrm{V}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7, 4.5), (10.2, 4.5)).label(f"$10{OHM}$").label("无电流", loc="bot", color=MUTED, fontsize=12))
    wire(d, (10.2, 4.5), (10.2, 3.4)); wire(d, (10.2, 1.1), (10.2, 0))
    opened(d, (10.2, 3.4), (10.2, 1.1), "$C_2$", "$u_C=6\\,\\mathrm{V}$", side="right")
    wire(d, (0, 0), (10.2, 0))
    dot(d, (3.8, 0))
    ssave(d, "d-712-0m")


def d712_wave():
    fig, ax = axes(5.8, 3.2)
    t = np.linspace(0, 10, 400)
    ax.axvline(0, color=MUTED, lw=0.8); ax.axhline(0, color=MUTED, lw=0.8)
    ax.plot(t, 12 - 6 * np.exp(-t / 2), color=C1, lw=2, label="$u_{C1}=12-6e^{-t/2}$")
    ax.plot(t, 6 * np.exp(-t / 2), color=C3, lw=1.6, ls="--", label="$ri_1=6e^{-t/2}$")
    ax.plot(t, 12 - 12 * np.exp(-t / 2), color=INK, lw=2, label="$u_0=u_{C1}-ri_1$")
    ax.plot(t, 12 * np.exp(-t / 2) - 6 * np.exp(-t), color=C2, lw=2, label="$u_C=12e^{-t/2}-6e^{-t}$")
    ax.set_xlim(-0.3, 10); ax.set_ylim(-0.5, 13)
    ax.set_yticks([0, 6, 12]); ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xlabel("$t$/s", color=INK, loc="right"); ax.set_ylabel("电压/V", color=INK)
    ax.legend(frameon=False, fontsize=9.5, loc="center right")
    sfig(fig, "d-712-wave")


# ------------------------------------------------------------------ 题9 作业 7-28
def d728_0m():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$12\\,\\mathrm{V}$")
    cur(d, (0, 4.5), (1.0, 4.5), "$i=0.72\\,\\mathrm{A}$", loc="top", frac=0.6)
    d.add(elm.Resistor().endpoints((1.0, 4.5), (3.8, 4.5)).label(f"$10{OHM}$", loc="bot"))
    dot(d, (3.8, 4.5))
    wire(d, (3.8, 4.5), (3.8, 3.4)); wire(d, (3.8, 1.1), (3.8, 0))
    opened(d, (3.8, 3.4), (3.8, 1.1), "$C$", "$4.8\\,\\mathrm{V}$")
    wire(d, (3.8, 4.5), (7, 4.5))
    note(d, (5.4, 5.0), "$S$ 闭合")
    dot(d, (7, 4.5)); dot(d, (7, 0))
    isrc(d, (7, 4.5), (7, 0), "$\\beta i=0.24\\,\\mathrm{A}$", loc="bot", ctrl=True)
    d.add(elm.Resistor().endpoints((7, 4.5), (11.4, 4.5)).label(f"$10{OHM}$"))
    arrow(d, (9.0, 3.9), (10.6, 3.9), "$0.48\\,\\mathrm{A}$", loc="bot")
    dot(d, (11.4, 4.5)); dot(d, (11.4, 0))
    d.add(elm.Resistor().endpoints((11.4, 4.5), (11.4, 0)).label(f"$10{OHM}$", loc="bot"))
    note(d, (11.4, -0.5), "（被短路）")
    wire(d, (11.4, 4.5), (13.8, 4.5))
    short(d, (13.8, 4.5), (13.8, 0), "$L$ 短路", loc="bot")
    arrow(d, (14.6, 3.8), (14.6, 2.4), "$i_L=0.48\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (13.8, 0))
    dot(d, (3.8, 0))
    ssave(d, "d-728-0m")


def d728_wave():
    fig, (a1, a2) = plt_sub()
    t = np.linspace(0, 0.3, 600); tl = -0.03
    iL = 0.78 * np.exp(-50 * t) - 0.3 * np.exp(-10 * t)
    uk = 12 - 5.4 * np.exp(-10 * t) + 7.8 * np.exp(-50 * t)
    for ax in (a1, a2):
        ax.axvline(0, color=MUTED, lw=0.8); ax.axhline(0, color=MUTED, lw=0.8)
    a1.plot([tl, 0], [0.48, 0.48], color=C1, lw=2); a1.plot(t, iL, color=C1, lw=2)
    a1.set_ylabel("$i_L$/A", color=INK); a1.set_yticks([-0.2, 0, 0.2, 0.48])
    a1.text(0.12, 0.25, "$i_L=0.78e^{-50t}-0.3e^{-10t}$\n连续，$i_L(0_+)=0.48$", fontsize=10, color=INK)
    a2.plot([tl, 0], [0, 0], color=C2, lw=2); a2.plot([0, 0], [0, 14.4], color=C2, lw=1, ls=":")
    a2.plot([0], [0], "o", ms=5, mfc="white", mec=C2); a2.plot([0], [14.4], "o", ms=5, color=C2)
    a2.plot(t, uk, color=C2, lw=2); a2.axhline(12, color=MUTED, ls="--", lw=1)
    a2.set_ylabel("$u_k$/V", color=INK); a2.set_yticks([0, 12, 14.4])
    a2.text(0.12, 5.0, "$u_k$ 在 $t=0$ 由 $0$ 跳到 $14.4\\,\\mathrm{V}$", fontsize=10, color=INK)
    a2.set_xlim(tl, 0.3); a2.set_xlabel("$t$/s", color=INK, loc="right")
    sfig(fig, "d-728-wave")


def plt_sub():
    from solcommon import plt, GRID
    from matplotlib.ticker import FormatStrFormatter
    fig, axs = plt.subplots(2, 1, figsize=(5.6, 4.4), sharex=True)
    for ax in axs:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=10)
        ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    return fig, axs


# ------------------------------------------------------------------ 题10 RLC
def drlc_wave():
    fig, (a1, a2) = plt_sub()
    t = np.linspace(0, 0.8, 600)
    env = np.exp(-6 * t)
    uc = env * (10 * np.cos(8 * t) + 7.5 * np.sin(8 * t))
    i = 2.5 * env * np.sin(8 * t)
    for ax in (a1, a2):
        ax.axhline(0, color=MUTED, lw=0.8)
    a1.plot(t, 12.5 * env, color=MUTED, ls="--", lw=1); a1.plot(t, -12.5 * env, color=MUTED, ls="--", lw=1)
    a1.plot(t, uc, color=C1, lw=2)
    a1.set_ylabel("$u_C$/V", color=INK); a1.set_yticks([0, 5, 10]); a1.set_ylim(-3, 13.5)
    a1.text(0.3, 4.0, "包络 $\\pm12.5e^{-6t}$", fontsize=10, color=MUTED)
    a2.plot(t, 2.5 * env, color=MUTED, ls="--", lw=1); a2.plot(t, -2.5 * env, color=MUTED, ls="--", lw=1)
    a2.plot(t, i, color=C2, lw=2)
    a2.set_ylabel("$i$/A", color=INK); a2.set_yticks([0, 0.5, 1.0])
    a2.set_ylim(-0.3, 1.3)
    a2.text(0.35, 0.65, "$i=2.5e^{-6t}\\sin 8t$", fontsize=10, color=INK)
    a2.set_xticks([0, np.pi / 16, np.pi / 8, 3 * np.pi / 16, np.pi / 4],
                  ["0", "$\\frac{\\pi}{16}$", "$\\frac{\\pi}{8}$", "$\\frac{3\\pi}{16}$", "$\\frac{\\pi}{4}$"])
    a2.set_xlim(0, 0.8); a2.set_xlabel("$t$/s", color=INK, loc="right")
    a1.text(0.78, 11.0, "周期 $T_d=2\\pi/\\omega_d=\\pi/4\\,\\mathrm{s}$", fontsize=10, color=INK, ha="right")
    sfig(fig, "d-rlc-wave")


if __name__ == "__main__":
    d73_0m(); d73_0p()
    drc_0m(); drc_req(); drc_wave()
    drl_0m(); drl_0p(); drl_req(); drl_ua()
    d74_wave(); d75_charge(); d710_req()
    d712_0m(); d712_wave(); d728_0m(); d728_wave(); drlc_wave()
