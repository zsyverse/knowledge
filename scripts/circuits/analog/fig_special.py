"""模电·集成功能电路 插图（前缀 ic-）。

    cd scripts/circuits/analog && ../../../.venv/bin/python fig_special.py
"""
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig as _save_fig, dot, text, wire, gnd, axes, plt,
                     note, C1, C2, C3, C4, INK, MUTED)

ARW = dict(headwidth=0.25, headlength=0.32)


def save_fig(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    _save_fig(fig, name)


def op(d, in1, flip=False):
    e = elm.Opamp(leads=True, flip=flip).right().anchor("in1").at(in1)
    d.add(e)
    return e


def box(d, c, w, h, s, fontsize=14):
    """方框（中心 c，宽 w，高 h），返回左右上下边中点。"""
    x, y = c
    pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)]
    wire(d, *pts, pts[0])
    text(d, c, s, fontsize=fontsize)
    return dict(W=(x - w / 2, y), E=(x + w / 2, y), N=(x, y + h / 2), S=(x, y - h / 2))


def harrow(d, p, q, label=None, loc="top"):
    a = elm.Arrow(**ARW).endpoints(p, q)
    if label:
        a.label(label, loc=loc)
    d.add(a)


def term(d, xy, s, dx=-0.55):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1]), s)


# ---------------------------------------------------------------- 仪用放大器
def ina():
    d = new_drawing()
    a1 = op(d, (2.0, 2.0), flip=True)        # + 在上
    a2 = op(d, (2.0, -2.0))                  # − 在上
    xn, xr = 1.4, 6.0
    # A1 / A2 输入
    term(d, (0, a1.in2[1]), "$v_{I1}$"); wire(d, (0, a1.in2[1]), a1.in2)
    term(d, (0, a2.in2[1]), "$v_{I2}$"); wire(d, (0, a2.in2[1]), a2.in2)
    # 反馈 R 与 R_G
    wire(d, a1.in1, (xn, a1.in1[1]), (xn, 0.9))
    wire(d, a2.in1, (xn, a2.in1[1]), (xn, -0.9))
    d.add(elm.Resistor().endpoints((xn, 0.9), (xr, 0.9)).label("$R$", loc="bot"))
    d.add(elm.Resistor().endpoints((xn, -0.9), (xr, -0.9)).label("$R$", loc="top"))
    d.add(elm.Resistor().endpoints((xn, 0.9), (xn, -0.9)).label("$R_G$", loc="top"))
    dot(d, (xn, 0.9)); dot(d, (xn, -0.9))
    wire(d, a1.out, (xr, a1.out[1]), (xr, 0.9)); dot(d, (xr, a1.out[1]))
    wire(d, a2.out, (xr, a2.out[1]), (xr, -0.9)); dot(d, (xr, a2.out[1]))
    text(d, (xr + 0.1, a1.out[1] + 0.45), "$v_{O1}$", fontsize=13)
    text(d, (xr + 0.1, a2.out[1] - 0.45), "$v_{O2}$", fontsize=13)
    text(d, (3.6, a1.out[1] + 0.05), "$A_1$", fontsize=13)
    text(d, (3.6, a2.out[1] - 0.05), "$A_2$", fontsize=13)
    # 差分级 A3（− 在上）
    a3 = op(d, (9.6, 0.625))
    xj = 8.9
    d.add(elm.Resistor().endpoints((xr, a1.out[1]), (xj, a1.out[1])).label("$R_3$"))
    d.add(elm.Resistor().endpoints((xr, a2.out[1]), (xj, a2.out[1])).label("$R_3$", loc="bot"))
    wire(d, (xj, a1.out[1]), (xj, a3.in1[1]), a3.in1)
    wire(d, (xj, a2.out[1]), (xj, a3.in2[1]), a3.in2)
    xo = a3.out[0] + 0.6
    d.add(elm.Resistor().endpoints((xj, a1.out[1]), (xo, a1.out[1])).label("$R_4$"))
    wire(d, (xo, a1.out[1]), (xo, a3.out[1]), a3.out)
    dot(d, (xj, a1.out[1])); dot(d, (xj, a2.out[1])); dot(d, (xo, a3.out[1]))
    d.add(elm.Resistor().endpoints((xj, a2.out[1]), (xj, -5.2)).label("$R_4$", loc="bot"))
    dot(d, (xj, -5.2), True); text(d, (xj + 1.0, -5.2), "REF（接地）", fontsize=12)
    wire(d, (xo, 0), (xo + 0.8, 0)); term(d, (xo + 0.8, 0), "$v_O$", dx=0.55)
    text(d, (11.2, 0.0), "$A_3$", fontsize=13)
    save(d, "ic-ina")


# ---------------------------------------------------------------- 乘法器：除法电路
def divider():
    d = new_drawing()
    a = op(d, (3.0, 0.0))                    # − 在上
    term(d, (0, 0), "$v_X$")
    d.add(elm.Resistor().endpoints((0, 0), (2.3, 0)).label("$R_1$"))
    wire(d, (2.3, 0), a.in1); dot(d, (2.3, 0))
    wire(d, a.in2, (2.3, a.in2[1]), (2.3, -1.9)); gnd(d, (2.3, -1.9))
    xo = a.out[0] + 0.8
    wire(d, a.out, (xo + 0.9, a.out[1])); dot(d, (xo, a.out[1]))
    term(d, (xo + 0.9, a.out[1]), "$v_O$", dx=0.55)
    # 乘法器在反馈支路
    m = box(d, (5.6, 2.6), 1.4, 1.4, "$\\times$", fontsize=20)
    text(d, (5.6, 3.6), "乘法器 $k$", fontsize=12)
    wire(d, (xo, a.out[1]), (xo, m["E"][1] - 0.35), (m["E"][0], m["E"][1] - 0.35))
    wire(d, (m["E"][0], m["E"][1] + 0.35), (xo + 0.9, m["E"][1] + 0.35))
    term(d, (xo + 0.9, m["E"][1] + 0.35), "$v_Y$", dx=0.55)
    d.add(elm.Resistor().endpoints(m["W"], (2.3, m["W"][1])).label("$R_2$"))
    wire(d, (2.3, m["W"][1]), (2.3, 0))
    text(d, (3.4, m["W"][1] - 0.55), "$kv_Ov_Y$", fontsize=13, color=C1)
    save(d, "ic-divider")


def am_wave():
    """调幅波与同步检波。"""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 3.8), sharex=True)
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.set_yticks([])
    t = np.linspace(0, 2, 4000)
    m = 1 + 0.6 * np.cos(2 * np.pi * t)
    vam = m * np.cos(2 * np.pi * 20 * t)
    a1.plot(t, vam, color=C1, lw=0.9, label="$v_{AM}=k(V_0+v_m)v_c$")
    a1.plot(t, m, color=C2, lw=1.4, ls="--", label="包络 $\\propto V_0+v_m$")
    a1.plot(t, -m, color=C2, lw=1.4, ls="--")
    a1.legend(frameon=False, fontsize=9, loc="upper right", ncol=2, bbox_to_anchor=(1.0, 1.25))
    prod = vam * np.cos(2 * np.pi * 20 * t)
    a2.plot(t, prod, color=C3, lw=0.8, label="$v_{AM}\\cdot v_c$（含 $2\\omega_c$ 分量）")
    a2.plot(t, m / 2, color=C2, lw=1.8, label="低通滤波后 $\\propto V_0+v_m$")
    a2.legend(frameon=False, fontsize=9, loc="upper right", ncol=2, bbox_to_anchor=(1.0, 1.22))
    a2.set_xticks([]); a2.set_xlabel("$t$", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "ic-am")


# ---------------------------------------------------------------- 函数发生器
def icl8038():
    fig, axs = plt.subplots(3, 1, figsize=(6.0, 3.9), sharex=True)
    t = np.linspace(0, 3, 3000)
    ph = (t % 1.0)
    tri = np.where(ph < 0.5, 1 / 3 + ph * 2 / 3, 2 / 3 - (ph - 0.5) * 2 / 3)
    sq = np.where(ph < 0.5, 1.0, 0.0)
    sine = np.sin(2 * np.pi * (ph - 0.25))
    for ax in axs:
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
    axs[0].plot(t, tri, color=C1, lw=1.8)
    axs[0].set_yticks([1 / 3, 2 / 3], ["$V_{CC}/3$", "$2V_{CC}/3$"]); axs[0].set_ylim(0.2, 0.8)
    axs[0].set_ylabel("$v_C$", color=INK, rotation=0, labelpad=12)
    axs[0].text(0.08, 0.68, "$+I$ 充电", fontsize=9, color=MUTED)
    axs[0].text(0.58, 0.68, "$-I$ 放电", fontsize=9, color=MUTED)
    axs[1].plot(t, sq, color=C2, lw=1.8)
    axs[1].set_yticks([0, 1], ["低", "高"]); axs[1].set_ylim(-0.2, 1.2)
    axs[1].set_ylabel("方波", color=INK, rotation=0, labelpad=14)
    axs[2].plot(t, sine, color=C3, lw=1.8)
    axs[2].set_yticks([]); axs[2].set_ylabel("正弦", color=INK, rotation=0, labelpad=14)
    axs[2].set_xticks([0, 0.5, 1.0], ["0", "$T/2$", "$T$"])
    axs[2].set_xlabel("$t$", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "ic-8038")


# ---------------------------------------------------------------- 开关电容
def sc_res():
    d = new_drawing()
    term(d, (0, 0), "$v_1$")
    d.add(elm.Switch().endpoints((0, 0), (2.2, 0)).label("$S_1\\ (\\varphi_1)$"))
    d.add(elm.Switch().endpoints((2.2, 0), (4.4, 0)).label("$S_2\\ (\\varphi_2)$"))
    term(d, (4.4, 0), "$v_2$", dx=0.55)
    dot(d, (2.2, 0))
    d.add(elm.Capacitor().endpoints((2.2, 0), (2.2, -1.8)).label("$C$", loc="bot"))
    gnd(d, (2.2, -1.8))
    text(d, (6.0, -0.4), "$\\Longleftrightarrow$", fontsize=18)
    term(d, (7.4, 0), "$v_1$")
    d.add(elm.Resistor().endpoints((7.4, 0), (10.4, 0)))
    text(d, (8.9, -0.9), "$R_{eq}=1/(Cf_s)$")
    term(d, (10.4, 0), "$v_2$", dx=0.55)
    save(d, "ic-sc")


def sc_int():
    d = new_drawing()
    a = op(d, (5.2, 0.0))
    term(d, (0, 0), "$v_I$")
    d.add(elm.Switch().endpoints((0, 0), (2.0, 0)).label("$\\varphi_1$"))
    d.add(elm.Switch().endpoints((2.0, 0), (4.2, 0)).label("$\\varphi_2$"))
    dot(d, (2.0, 0))
    d.add(elm.Capacitor().endpoints((2.0, 0), (2.0, -1.8)).label("$C_1$", loc="bot"))
    gnd(d, (2.0, -1.8))
    wire(d, (4.2, 0), a.in1); dot(d, (4.6, 0))
    wire(d, a.in2, (4.6, a.in2[1]), (4.6, -1.9)); gnd(d, (4.6, -1.9))
    xo = a.out[0] + 0.6
    wire(d, (4.6, 0), (4.6, 1.6))
    d.add(elm.Capacitor().endpoints((4.6, 1.6), (xo, 1.6)).label("$C_2$"))
    wire(d, (xo, 1.6), (xo, a.out[1])); wire(d, a.out, (xo + 0.8, a.out[1])); dot(d, (xo, a.out[1]))
    term(d, (xo + 0.8, a.out[1]), "$v_O$", dx=0.55)
    save(d, "ic-sc-int")


# ---------------------------------------------------------------- Buck
def buck():
    d = new_drawing()
    yt, yb = 2.4, 0.0
    d.add(elm.SourceV().endpoints((0, yb), (0, yt)).label("$V_I$", loc="top"))
    d.add(elm.Switch().endpoints((0, yt), (2.4, yt)).label("$S$"))
    dot(d, (2.4, yt)); text(d, (2.4, yt + 0.45), "$v_X$", fontsize=13)
    d.add(elm.Diode().endpoints((2.4, yb), (2.4, yt)).label("$D$", loc="bot"))
    d.add(elm.Inductor().endpoints((2.4, yt), (5.2, yt)).label("$L$"))
    harrow(d, (3.3, yt - 0.55), (4.3, yt - 0.55), "$i_L$", loc="bot")
    d.add(elm.Capacitor().endpoints((5.2, yt), (5.2, yb)).label("$C$", loc="bot"))
    d.add(elm.Resistor().endpoints((6.6, yt), (6.6, yb)).label("$R_L$", loc="bot"))
    wire(d, (5.2, yt), (7.8, yt)); wire(d, (0, yb), (7.8, yb))
    for p in ((5.2, yt), (6.6, yt), (2.4, yb), (5.2, yb), (6.6, yb)):
        dot(d, p)
    dot(d, (7.8, yt), True); dot(d, (7.8, yb), True)
    text(d, (8.25, yt - 0.35), "+"); text(d, (8.25, (yt + yb) / 2), "$V_O$"); text(d, (8.25, yb + 0.35), "−")
    gnd(d, (4.0, yb))
    save(d, "ic-buck")


def buck_wave():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.0, 3.4), sharex=True)
    D, T = 0.4, 1.0
    t = np.linspace(0, 3, 3000)
    ph = t % T
    on = ph < D * T
    vi, vo = 1.0, D
    vx = np.where(on, vi, 0.0)
    IL, dI = 0.55, 0.3
    il = np.where(on, IL - dI / 2 + dI * ph / (D * T), IL + dI / 2 - dI * (ph - D * T) / ((1 - D) * T))
    for ax in (a1, a2):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
    a1.plot(t, vx, color=C1, lw=1.8)
    a1.axhline(vo, color=C2, lw=1.2, ls="--")
    a1.text(1.45, vo + 0.06, "$V_O=DV_I$", color=C2, fontsize=10)
    a1.set_yticks([0, vi], ["0", "$V_I$"]); a1.set_ylabel("$v_X$", color=INK, rotation=0, labelpad=10)
    a1.set_ylim(-0.1, 1.25)
    a2.plot(t, il, color=C3, lw=1.8)
    a2.axhline(IL, color=MUTED, lw=0.8, ls=":")
    a2.text(2.62, IL - 0.12, "$I_O$", color=INK, fontsize=10)
    a2.annotate("", xy=(0.4, IL + dI / 2), xytext=(0.4, IL - dI / 2), arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8))
    a2.text(0.45, IL - 0.05, "$\\Delta I_L$", fontsize=10, color=INK)
    a2.set_yticks([0]); a2.set_ylim(0, 0.85)
    a2.set_ylabel("$i_L$", color=INK, rotation=0, labelpad=10)
    a2.set_xticks([0, D, 1.0], ["0", "$DT_s$", "$T_s$"])
    a2.set_xlabel("$t$", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "ic-buck-wave")


# ---------------------------------------------------------------- PLL
def pll():
    d = new_drawing()
    y = 0
    pd = box(d, (2.6, y), 2.2, 1.2, "鉴相器 PD", 13)
    lp = box(d, (5.8, y), 2.6, 1.2, "环路滤波 LF", 13)
    vco = box(d, (9.0, y), 2.0, 1.2, "VCO", 13)
    dv = box(d, (5.8, -2.4), 2.0, 1.2, "$\\div N$", 15)
    harrow(d, (0, y), pd["W"]); text(d, (0.5, y + 0.45), "$f_r$", fontsize=14)
    harrow(d, pd["E"], lp["W"]); text(d, (4.2, y + 0.45), "$u_d$", fontsize=13)
    harrow(d, lp["E"], vco["W"]); text(d, (7.4, y + 0.45), "$u_c$", fontsize=13)
    harrow(d, vco["E"], (12.0, y)); text(d, (11.5, y + 0.45), "$f_o$", fontsize=14)
    dot(d, (10.8, y))
    wire(d, (10.8, y), (10.8, -2.4))
    harrow(d, (10.8, -2.4), dv["E"])
    wire(d, dv["W"], (2.6, -2.4))
    harrow(d, (2.6, -2.4), pd["S"])
    text(d, (3.6, -2.0), "$f_o/N$", fontsize=13)
    save(d, "ic-pll")


if __name__ == "__main__":
    ina()
    divider()
    am_wave()
    icl8038()
    sc_res()
    sc_int()
    buck()
    buck_wave()
    pll()
