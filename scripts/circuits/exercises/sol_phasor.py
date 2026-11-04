"""习题·相量法 解析插图（images/ex/sol/p-*）。sin 约定 + 有效值相量，数值见 verify_phasor.py。"""
import math

import numpy as np

from solcommon import (elm, new_drawing, ssave, sfig, dot, text, note, cur, arrow, ac_src, wire, plt,
                       phasor, angle_arc, OHM, C1, C2, C3, C4, INK, MUTED, GRID)


def P(m, deg):
    return m * np.exp(1j * math.radians(deg))


def panels(n, lims, w=4.0, ratios=None):
    """n 个相量图并排（各自等比例）；lims=[(xlim, ylim), ...]。"""
    ratios = ratios or [1] * n
    hs = [(l[1][1] - l[1][0]) / (l[0][1] - l[0][0]) for l in lims]
    fig, axs = plt.subplots(1, n, figsize=(w * n, w * max(hs)), gridspec_kw=dict(width_ratios=ratios))
    axs = np.atleast_1d(axs)
    for ax, (xl, yl) in zip(axs, lims):
        ax.set_aspect("equal"); ax.axis("off")
        ax.axhline(0, color=GRID, lw=0.8, zorder=0); ax.axvline(0, color=GRID, lw=0.8, zorder=0)
        ax.set_xlim(*xl); ax.set_ylim(*yl)
    return fig, axs


def dashed(ax, a, b, color=MUTED):
    ax.plot([a.real, b.real], [a.imag, b.imag], color=color, ls="--", lw=1)


# ------------------------------------------------------------------ 题2 相量加法
def p_sum():
    I1, I2 = P(6, 30), P(8, 120)
    I = I1 + I2
    fig, (ax,) = panels(1, [((-9.5, 7.5), (-1.0, 11.0))], w=4.4)
    dashed(ax, I1, I); dashed(ax, I2, I)
    phasor(ax, I1, C1, "$\\dot I_1=6\\angle30^\\circ$", (I1.real + 1.0, I1.imag + 0.8))
    phasor(ax, I2, C2, "$\\dot I_2=8\\angle120^\\circ$", (I2.real - 0.2, I2.imag + 0.7))
    phasor(ax, I, INK, "$\\dot I=10\\angle83.13^\\circ$", (I.real + 2.0, I.imag + 0.6), lw=2.4)
    angle_arc(ax, 0, 30, 2.2, "$30^\\circ$", (2.9, 0.65))
    angle_arc(ax, 0, 83.13, 3.4, "$83.13^\\circ$", (2.2, 3.6))
    # I1 与 I2 之间的直角标记
    u1, u2 = I1 / abs(I1), I2 / abs(I2)
    k = 0.7
    sq = [k * u1, k * (u1 + u2), k * u2]
    ax.plot([z.real for z in sq], [z.imag for z in sq], color=MUTED, lw=1)
    ax.text(-6.0, 1.0, "$\\dot I_1\\perp\\dot I_2$\n$I=\\sqrt{6^2+8^2}=10$", fontsize=11, color=INK, ha="center")
    sfig(fig, "p-sum")


# ------------------------------------------------------------------ 题4 电表读数
def p_meters():
    fig, (a, b) = panels(2, [((-1.5, 6.5), (-9.5, 5.5)), ((-1.5, 6.5), (-5.5, 9.5))], w=3.0)
    # (a) 并联，以电压为参考；单位 A
    phasor(a, 5.8 + 0j, MUTED, "$\\dot U$（参考）", (5.4, 0.75), lw=1.2)
    phasor(a, 3 + 0j, C1, "$\\dot I_R=3$", (1.5, 0.75))
    phasor(a, -8j, C2, "$\\dot I_L=8\\angle-90^\\circ$", (1.5, -8.6))
    phasor(a, 4j, C3, "$\\dot I_C=4\\angle90^\\circ$", (1.6, 4.4))
    phasor(a, -4j, MUTED, None, start=3 + 0j, lw=1.2, ls="--")
    a.text(4.5, -2.0, "$\\dot I_L+\\dot I_C$\n$=-j4$", fontsize=10, color=INK, ha="center")
    phasor(a, 3 - 4j, INK, "$\\dot I=3-j4$", (4.2, -4.6), lw=2.4)
    angle_arc(a, -53.13, 0, 1.4, "$53.1^\\circ$", (2.0, -0.95), fs=10)
    a.set_title("(a) 并联：$I_0=5\\,\\mathrm{A}$，滞后（感性）", fontsize=11, color=INK)
    # (b) 串联，以电流为参考；单位 10 V
    phasor(b, 5.8 + 0j, MUTED, "$\\dot I$（参考）", (5.2, -0.6), lw=1.2)
    phasor(b, 3 + 0j, C1, "$\\dot U_R=30$", (1.5, -0.7))
    phasor(b, 8j, C2, "$\\dot U_L=j80$", (-0.9, 8.0))
    phasor(b, -4j, C3, "$\\dot U_C=-j40$", (1.5, -4.6))
    phasor(b, 4j, MUTED, None, start=3 + 0j, lw=1.2, ls="--")
    b.text(4.6, 2.0, "$\\dot U_L+\\dot U_C$\n$=j40$", fontsize=10, color=INK, ha="center")
    phasor(b, 3 + 4j, INK, "$\\dot U=30+j40$", (4.4, 4.6), lw=2.4)
    angle_arc(b, 0, 53.13, 1.4, "$53.1^\\circ$", (2.0, 0.95), fs=10)
    b.set_title("(b) 串联：$U=50\\,\\mathrm{V}$，超前（感性）", fontsize=11, color=INK)
    sfig(fig, "p-meters-phasor")


# ------------------------------------------------------------------ 题7 日光灯电压三角形
def p_lamp():
    UR, UL = 0.36 * 40 / 0.36 ** 2, 0.36 * math.sqrt((220 / 0.36) ** 2 - (40 / 0.36 ** 2) ** 2)
    phi = math.degrees(math.atan2(UL, UR))
    fig, (ax,) = panels(1, [((-25, 290), (-40, 230))], w=4.2)
    phasor(ax, 250 + 0j, MUTED, "$\\dot I$（参考）", (232, -18), lw=1.2)
    phasor(ax, UR + 0j, C1, "$\\dot U_R\\approx111.1\\,\\mathrm{V}$", (UR / 2, -18))
    phasor(ax, 1j * UL, C2, "$\\dot U_L\\approx189.9\\,\\mathrm{V}$", (UR + 62, UL / 2), start=UR + 0j)
    phasor(ax, UR + 1j * UL, INK, "$\\dot U=220\\,\\mathrm{V}$", (UR / 2 - 38, UL / 2 + 10), lw=2.4)
    angle_arc(ax, 0, phi, 40, f"$\\varphi\\approx{phi:.1f}^\\circ$", (70, 30), fs=11)
    ax.text(150, 205, "$\\cos\\varphi=U_R/U\\approx0.505$", fontsize=11, color=INK, ha="center")
    sfig(fig, "p-lamp-tri")


# ------------------------------------------------------------------ 题8 作业 5-12
def p_512():
    fig, (a, b) = panels(2, [((-4, 17), (-13, 13)), ((-20, 225), (-85, 75))], w=3.0, ratios=[1, 1.5])
    I1, I2 = 10j, 10 - 10j
    phasor(a, I1, C3, "$\\dot I_1=j10$", (-2.2, 10.5))
    phasor(a, I2, C2, "$\\dot I_2=10\\sqrt{2}\\angle-45^\\circ$", (9.0, -11.6))
    dashed(a, I1, I1 + I2); dashed(a, I2, I1 + I2)
    phasor(a, I1 + I2, INK, "$\\dot I=10\\angle0^\\circ$", (6.0, 1.3), lw=2.4)
    angle_arc(a, -45, 0, 3.0, "$45^\\circ$", (4.4, -1.9), fs=10)
    a.set_title("电流（A），$\\dot U_C$ 为参考", fontsize=11, color=INK)
    UR2, UL = 5 * I2, 5j * I2
    phasor(b, UR2, C2, "$\\dot U_{R_2}=50-j50$", (20, -62))
    phasor(b, UL, C3, "$\\dot U_L=50+j50$", (125, -38), start=UR2)
    phasor(b, 100 + 0j, C1, None, lw=2.6)
    phasor(b, 100 + 0j, C4, None, start=100 + 0j, lw=2.0)
    b.text(50, 10, "$\\dot U_C=100$", fontsize=11, color=INK, ha="center")
    b.text(150, 10, "$\\dot U_{R_1}=100$", fontsize=11, color=INK, ha="center")
    b.annotate("", xy=(200, 45), xytext=(0, 45),
               arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0, mutation_scale=15, shrinkA=0, shrinkB=0))
    b.text(100, 58, "$\\dot U=\\dot U_C+\\dot U_{R_1}=200\\angle0^\\circ$", fontsize=11, color=INK, ha="center")
    angle_arc(b, 45, 135, 14, "$90^\\circ$", (50, -26), center=UR2, fs=10)
    b.set_title("电压（V）", fontsize=11, color=INK)
    sfig(fig, "p-512-phasor")


# ------------------------------------------------------------------ 题9 相量模型
def p_node_model():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4.5), "$10\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4.5), (3.5, 4.5)).label(f"$5{OHM}$", loc="bot"))
    arrow(d, (1.2, 5.3), (2.4, 5.3), "$\\dot I_R=-2\\,\\mathrm{A}$", loc="top")
    dot(d, (3.5, 4.5)); text(d, (3.5, 5.0), "$a$")
    d.add(elm.Capacitor().endpoints((3.5, 4.5), (3.5, 0)).label(f"$-j5{OHM}$", loc="top"))
    arrow(d, (4.2, 2.9), (4.2, 1.6), "$\\dot I_C=j4$", loc="bot")
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4.5), (7.5, 4.5)).label(f"$j5{OHM}$", loc="bot"))
    arrow(d, (4.9, 5.3), (6.1, 5.3), "$\\dot I_L=-2-j4$", loc="top")
    ac_src(d, (7.5, 0), (7.5, 4.5), "$j10\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (7.5, 0))
    dot(d, (3.5, 0))
    text(d, (3.75, -0.8), "$\\dot U_a=20\\angle0^\\circ\\,\\mathrm{V}$")
    ssave(d, "p-node-model")


if __name__ == "__main__":
    p_sum(); p_meters(); p_lamp(); p_512(); p_node_model()
