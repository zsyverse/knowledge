"""习题·正弦稳态功率与谐振 解析插图（images/ex/sol/w-*）。数值见 verify_acpower.py。"""
import math

import numpy as np

from solcommon import (elm, new_drawing, ssave, sfig, dot, text, note, cur, arrow, ac_src, wire, plt,
                       phasor, phasor_axes, angle_arc, OHM, C1, C2, C3, C4, INK, MUTED)


def P(m, deg):
    return m * np.exp(1j * math.radians(deg))


# ------------------------------------------------------------------ 题2 功率三角形
def w_s_tri():
    Pw, Q = 250 * math.sqrt(3), 250
    fig, ax = plt.subplots(figsize=(4.6, 2.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.plot([0, Pw], [0, 0], color=C1, lw=2.2)
    ax.plot([Pw, Pw], [0, Q], color=C2, lw=2.2)
    ax.plot([0, Pw], [0, Q], color=INK, lw=2.2)
    ax.plot([Pw - 18, Pw - 18, Pw], [0, 18, 18], color=MUTED, lw=0.8)
    th = np.radians(np.linspace(0, 30, 40))
    ax.plot(90 * np.cos(th), 90 * np.sin(th), color=MUTED, lw=1)
    ax.text(110, 26, "$\\varphi=30^\\circ$", fontsize=11, color=INK)
    ax.text(Pw / 2, -22, "$P=433.0\\,\\mathrm{W}$", ha="center", va="top", fontsize=11, color=INK)
    ax.text(Pw + 14, Q / 2, "$Q=250\\,\\mathrm{var}$", ha="left", va="center", fontsize=11, color=INK)
    ax.text(Pw / 2 - 30, Q / 2 + 18, "$S=500\\,\\mathrm{VA}$", ha="right", va="bottom", fontsize=11, color=INK)
    ax.text(Pw / 2 + 20, Q * 0.95, "$\\bar S=500\\angle30^\\circ$", fontsize=10, color=MUTED, ha="right")
    ax.set_xlim(-20, Pw + 160); ax.set_ylim(-70, Q + 30)
    sfig(fig, "w-s-tri")


# ------------------------------------------------------------------ 题3 各支路电流相量
def w_branch_phasor():
    I1, I2, I3 = 12.5 + 0j, 6.25 - 6.25j, 6.25 + 6.25j
    Uab = 87.5 + 12.5j
    fig, ax = phasor_axes((-1.5, 15.5), (-8.5, 8.5), size=4.2)
    ax.plot([I2.real, I1.real], [I2.imag, I1.imag], color=MUTED, ls="--", lw=1)
    ax.plot([I3.real, I1.real], [I3.imag, I1.imag], color=MUTED, ls="--", lw=1)
    phasor(ax, I2, C2, "$\\dot I_2=8.84\\angle-45^\\circ$", (5.0, -7.6))
    phasor(ax, I3, C3, "$\\dot I_3=8.84\\angle45^\\circ$", (5.0, 7.6))
    phasor(ax, I1, INK, "$\\dot I_1=12.5\\angle0^\\circ$", (12.0, -0.8), lw=2.4)
    phasor(ax, Uab / 8, MUTED, "$\\dot U_{ab}$", (Uab.real / 8 + 1.1, Uab.imag / 8 + 0.6), lw=1.2)
    angle_arc(ax, 0, 45, 2.6, "$45^\\circ$", (3.4, 1.3), fs=10)
    angle_arc(ax, -45, 0, 2.6, "$45^\\circ$", (3.4, -1.3), fs=10)
    ax.text(14.0, 4.6, "$\\dot I_2\\perp\\dot I_3$\n$\\dot I_1$ 与 $\\dot U_S$ 同相", fontsize=10, color=INK, ha="center")
    sfig(fig, "w-branch-phasor")


# ------------------------------------------------------------------ 题5 补偿前后的功率三角形
def w_pfc_tri():
    Pw = 10.0
    Q1, Q2 = Pw * 4 / 3, Pw * math.sqrt(1 - 0.81) / 0.9
    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    ax.set_aspect("equal"); ax.axis("off")
    ax.plot([0, Pw], [0, 0], color=INK, lw=2.2)
    ax.plot([0, Pw], [0, Q1], color=C2, lw=2.2)
    ax.plot([0, Pw], [0, Q2], color=C1, lw=2.2)
    ax.plot([Pw, Pw], [0, Q1], color=C2, lw=1.2, ls=":")
    ax.plot([Pw, Pw], [0, Q2], color=C1, lw=2.2)
    ax.annotate("", xy=(Pw + 0.5, Q2), xytext=(Pw + 0.5, Q1),
                arrowprops=dict(arrowstyle="-|>", color=C3, lw=1.6, mutation_scale=14))
    ax.text(Pw / 2, -0.45, "$P=10\\,\\mathrm{kW}$（不变）", ha="center", va="top", fontsize=11, color=INK)
    ax.text(Pw + 0.25, Q1 + 0.25, "$Q_1=13.33\\,\\mathrm{kvar}$", ha="center", va="bottom", fontsize=11, color=INK)
    ax.text(Pw + 0.9, (Q1 + Q2) / 2, "电容提供\n$|Q_C|=8.49\\,\\mathrm{kvar}$", ha="left", va="center", fontsize=11, color=INK)
    ax.text(Pw + 0.9, Q2 / 2, "$Q_2=4.84\\,\\mathrm{kvar}$", ha="left", va="center", fontsize=11, color=INK)
    ax.text(3.0, 6.6, "$S_1=16.67\\,\\mathrm{kVA}$\n$\\lambda_1=0.6$", fontsize=11, color=C2, ha="right")
    ax.text(5.2, 4.1, "$S_2=11.11\\,\\mathrm{kVA}$\n$\\lambda_2=0.9$", fontsize=11, color=C1, ha="center", va="center")
    th1, th2 = math.degrees(math.atan(Q1 / Pw)), math.degrees(math.atan(Q2 / Pw))
    for r, a, lab, xy in ((3.2, th1, "$\\varphi_1=53.1^\\circ$", (3.6, 2.75)), (5.0, th2, "$\\varphi_2=25.8^\\circ$", (6.9, 1.05))):
        t = np.radians(np.linspace(0, a, 40))
        ax.plot(r * np.cos(t), r * np.sin(t), color=MUTED, lw=1)
        ax.text(*xy, lab, fontsize=10, color=INK, ha="center")
    ax.set_xlim(-0.5, 16); ax.set_ylim(-1.4, Q1 + 1.2)
    sfig(fig, "w-pfc-tri")


# ------------------------------------------------------------------ 题6 戴维南等效 + 共轭匹配
def w_maxp_eq():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_{oc}=10\\sqrt{2}\\angle45^\\circ\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (2.6, 4)).label(f"$2{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((2.6, 4), (5.2, 4)).label(f"$j2{OHM}$"))
    note(d, (2.6, 5.1), "$Z_{eq}=2+j2\\,\\Omega$")
    dot(d, (5.6, 4), True); dot(d, (5.6, 0), True)
    wire(d, (5.2, 4), (5.6, 4))
    text(d, (5.6, 4.5), "$a$"); text(d, (5.6, -0.5), "$b$")
    wire(d, (5.6, 4), (8, 4)); wire(d, (0, 0), (8, 0))
    d.add(elm.Resistor().endpoints((8, 4), (8, 2)).label(f"$2{OHM}$", loc="bot"))
    d.add(elm.Capacitor().endpoints((8, 2), (8, 0)).label(f"$-j2{OHM}$", loc="bot"))
    note(d, (8.0, 5.1), "$Z_L=Z_{eq}^*=2-j2\\,\\Omega$")
    text(d, (4.0, -1.0), "$I=\\frac{10\\sqrt{2}}{2+2}\\,\\mathrm{A},\\ P_{\\max}=I^2\\times2=25\\,\\mathrm{W}$")
    ssave(d, "w-maxp-eq")


# ------------------------------------------------------------------ 题7 瓦特表相量图
def w_watt_phasor():
    UA, UB = 10 + 0j, -10j            # 电压按 1/10 缩放（单位 10 V）
    I = 10 - 10j
    fig, ax = phasor_axes((-13, 14), (-13.5, 12), size=4.4)
    phasor(ax, UA, C1, "$\\dot U_A=100\\angle0^\\circ$", (10.5, 1.1))
    phasor(ax, UB, C2, "$\\dot U_B=100\\angle-90^\\circ$", (-4.5, -11.0))
    phasor(ax, I, INK, "$\\dot I=10\\sqrt{2}\\angle-45^\\circ$", (10.6, -11.0), lw=2.2)
    phasor(ax, -I, C3, "$\\dot I_W=-\\dot I=10\\sqrt{2}\\angle135^\\circ$", (-7.0, 11.0), lw=2.2)
    angle_arc(ax, -45, 0, 4.0, "$45^\\circ$", (5.3, -1.8), fs=10)
    angle_arc(ax, 135, 270, 2.6, "$135^\\circ$", (-4.4, -2.0), fs=10)
    ax.text(5.5, 7.5, "$P_A=UI\\cos45^\\circ=1000\\,\\mathrm{W}$\n$W=UI\\cos135^\\circ=-1000\\,\\mathrm{W}$",
            fontsize=10, color=INK, ha="center")
    ax.text(0.5, -13.3, "（电压、电流比例尺不同）", fontsize=9, color=MUTED, ha="center")
    sfig(fig, "w-watt-phasor")


# ------------------------------------------------------------------ 题9 右支路谐振 → 短路
def w_multi_eq():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    text(d, (-0.45, 5), "$a$"); text(d, (-0.45, 0), "$b$")
    d.add(elm.Gap().endpoints((0, 5), (0, 0)).label(("+", "$200\\angle30^\\circ\\,\\mathrm{V}$", "−"), loc="bot"))
    d.add(elm.Resistor().endpoints((0, 5), (3, 5)).label(f"$R_1=100{OHM}$"))
    cur(d, (3, 5), (4.5, 5), "$\\dot I_1=2\\angle30^\\circ\\,\\mathrm{A}$", loc="bot")
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$c$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 0)).label(f"$R_2=50{OHM}$", loc="top"))
    arrow(d, (5.2, 3.2), (5.2, 1.8), "$\\dot I_2=0$")
    wire(d, (4.5, 5), (8, 5))
    d.add(elm.Line().endpoints((8, 5), (8, 0)).color(C2))
    note(d, (8.3, 2.9), "右支路串联谐振", halign="left")
    note(d, (8.3, 2.1), "$Z=j200-j100-j100=0$", halign="left")
    note(d, (8.3, 1.3), "相当于短路", halign="left")
    wire(d, (0, 0), (8, 0))
    dot(d, (4.5, 0))
    ssave(d, "w-multi-eq")


if __name__ == "__main__":
    w_s_tri(); w_branch_phasor(); w_pfc_tri(); w_maxp_eq(); w_watt_phasor(); w_multi_eq()
