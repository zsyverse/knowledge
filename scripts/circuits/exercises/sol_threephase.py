"""习题·三相电路 解析插图（images/ex/sol/s-*）。正序，sin 约定、有效值相量。数值见 verify_threephase.py。"""
import numpy as np

from solcommon import (elm, new_drawing, ssave, sfig, dot, text, note, cur, arrow, wire, ac_src, OHM,
                       phasor_axes, phasor, angle_arc, C1, C2, C3, C4, INK, MUTED)


def P(mag, deg):
    return mag * np.exp(1j * np.radians(deg))


# ------------------------------------------------------------------ 题2
def s_2_phasor():
    fig, ax = phasor_axes((-1.75, 1.75), (-0.85, 1.25))
    A, B, C = P(1, 90), P(1, -30), P(1, -150)
    for z, col, lab, off in ((A, C1, "$\\dot U_A=219.4\\angle90^\\circ$", (0.0, 0.12)),
                             (B, C2, "$\\dot U_B$\n$219.4\\angle(-30^\\circ)$", (0.48, 0.12)),
                             (C, C3, "$\\dot U_C$\n$219.4\\angle(-150^\\circ)$", (-0.48, 0.12))):
        phasor(ax, z, col, lab, (z.real + off[0], z.imag + off[1]), fs=10.5)
    # 线电压：连接相电压端点（U_XY = U_X - U_Y：由 Y 端指向 X 端）
    phasor(ax, A - B, INK, "$\\dot U_{AB}=380\\angle120^\\circ$", (0.95, 0.42), start=B, lw=1.4, fs=10.5)
    phasor(ax, B - C, INK, "$\\dot U_{BC}=380\\angle0^\\circ$（已知）", (0, -0.66), start=C, lw=1.4, fs=10.5)
    phasor(ax, C - A, INK, "$\\dot U_{CA}=380\\angle(-120^\\circ)$", (-0.98, 0.42), start=A, lw=1.4, fs=10.5)
    ax.plot([0, 0.55], [0, 0], color=MUTED, lw=0.9, ls="--")
    angle_arc(ax, -30, 0, 0.42, "$30^\\circ$", (0.56, -0.13))
    sfig(fig, "s-2-phasor")


# ------------------------------------------------------------------ 题3
def s_delta_phasor():
    fig, ax = phasor_axes((-0.7, 1.5), (-1.25, 1.05))
    k = 1 / 13.16
    IAB, ICA = P(7.6 * k, -23.13), P(7.6 * k, 96.87)
    IA = IAB - ICA
    ax.plot([0, 1.35 * np.cos(np.radians(30))], [0, 1.35 * np.sin(np.radians(30))], color=MUTED, lw=1.2, ls="--")
    ax.text(1.2, 0.78, "$\\dot U_{AB}=380\\angle30^\\circ$\n（方向）", fontsize=10, color=MUTED, ha="center")
    phasor(ax, IAB, C1, "$\\dot I_{AB}=7.6\\angle(-23.13^\\circ)$", (0.98, -0.12), fs=10.5)
    phasor(ax, ICA, C3, "$\\dot I_{CA}=7.6\\angle96.87^\\circ$", (-0.05, 0.66), fs=10.5)
    phasor(ax, -ICA, C3, "$-\\dot I_{CA}$", (0.98, -0.45), start=IAB, lw=1.2, ls="--", fs=10.5)
    phasor(ax, IA, C2, "$\\dot I_A=13.16\\angle(-53.13^\\circ)$", (0.75, -1.1), lw=2.4, fs=10.5)
    angle_arc(ax, -23.13, 30, 0.32, "$53.13^\\circ$", (0.5, 0.06), fs=10)
    angle_arc(ax, -53.13, -23.13, 0.5, "$30^\\circ$", (0.45, -0.58), fs=10)
    ax.text(-0.65, 0.95, "电流按比例；电压只示方向", fontsize=9, color=MUTED)
    sfig(fig, "s-delta-phasor")


# ------------------------------------------------------------------ 题4
def s_delta_line_1ph():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_A=220\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.RBox().endpoints((0, 4), (3.2, 4)).label(f"$Z_l=1+j1{OHM}$"))
    cur(d, (3.2, 4), (5, 4), "$\\dot I_A$")
    text(d, (5, 4.5), "$A'$"); dot(d, (5, 4))
    d.add(elm.RBox().endpoints((5, 4), (5, 0)).label(f"$Z_Y=\\frac{{Z_\\Delta}}{{3}}=8+j11{OHM}$", loc="bot"))
    wire(d, (0, 0), (5, 0))
    text(d, (-0.45, -0.35), "$N$"); text(d, (5.45, -0.35), "$N'$")
    note(d, (2.5, -1.0), "（对称时 $N$、$N'$ 等电位，用短路线相连）")
    ssave(d, "s-delta-line-1ph")


# ------------------------------------------------------------------ 题5
def s_551_1ph():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_A=100\\angle0^\\circ\\,\\mathrm{V}$")
    cur(d, (0, 4), (1.8, 4), "$\\dot I_A=1+j3.14\\,\\mathrm{A}$")
    wire(d, (1.8, 4), (8.0, 4)); wire(d, (0, 0), (8.0, 0))
    dot(d, (3.5, 4)); dot(d, (3.5, 0))
    d.add(elm.Capacitor().endpoints((3.5, 4), (3.5, 0)).label(f"$-j31.85{OHM}$", loc="top"))
    arrow(d, (4.2, 3.2), (4.2, 1.8), "$j3.14\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((8.0, 4), (8.0, 0)).label(f"$\\frac{{300}}{{3}}=100{OHM}$", loc="bot"))
    note(d, (8.0, -0.6), "Δ 电阻化成 Y")
    arrow(d, (7.3, 3.2), (7.3, 1.8), "$1\\,\\mathrm{A}$", loc="top")
    text(d, (-0.45, -0.35), "$N$")
    ssave(d, "s-551-1ph")


# ------------------------------------------------------------------ 题7
def s_two_watt_phasor():
    fig, ax = phasor_axes((-1.2, 1.9), (-1.2, 2.2))
    r3 = np.sqrt(3)
    for deg, lab, xy in ((0, "$\\dot U_A$", (1.1, 0.1)), (-120, "$\\dot U_B$", (-0.62, -0.98)),
                         (120, "$\\dot U_C$", (-0.62, 0.98))):
        phasor(ax, P(1, deg), "#aaaaaa", lab, xy, lw=1.2, fs=10.5)
    phasor(ax, P(r3, 30), C1, "$\\dot U_{AB}$", (1.62, 0.98), fs=11)
    phasor(ax, P(r3, 90), C3, "$\\dot U_{CB}$", (0.0, 1.85), fs=11)
    IA, IC = P(1.1, -53.13), P(1.1, 66.87)
    phasor(ax, IA, C2, "$\\dot I_A$", (0.78, -1.0), lw=2.4)
    phasor(ax, IC, C2, "$\\dot I_C$", (0.54, 1.13), lw=2.4)
    angle_arc(ax, -53.13, 30, 0.45, "$\\varphi+30^\\circ=83.13^\\circ$", (0.95, -0.33), fs=10)
    angle_arc(ax, 66.87, 90, 0.75, "$23.13^\\circ$", (-0.3, 0.8), fs=10)
    ax.text(-1.15, 2.12, "$W_1=U_lI_l\\cos83.13^\\circ$,  $W_2=U_lI_l\\cos23.13^\\circ$", fontsize=10, color=INK)
    sfig(fig, "s-two-watt-phasor")


# ------------------------------------------------------------------ 题8
def s_phase_seq_phasor():
    fig, ax = phasor_axes((-1.25, 1.3), (-1.1, 1.05))
    A, B, C = P(1, 0), P(1, -120), P(1, 120)
    Np = complex(-0.2, 0.6)
    for z, lab, xy in ((A, "$\\dot U_A$", (1.1, 0.08)), (B, "$\\dot U_B$", (-0.62, -0.98)),
                       (C, "$\\dot U_C$", (-0.78, 0.98))):
        phasor(ax, z, "#aaaaaa", lab, xy, lw=1.2, fs=10.5)
    phasor(ax, Np, C2, "$\\dot U_{N'N}=139.1\\angle108.43^\\circ$", (0.6, 0.8), lw=2, fs=10)
    phasor(ax, B - Np, C1, "$U_{BN'}\\approx329.2\\,\\mathrm{V}$（亮）", (0.5, -0.55), start=Np, lw=2.2, fs=10)
    phasor(ax, C - Np, C3, "$U_{CN'}\\approx88.2$（暗）", (-0.88, 0.48), start=Np, lw=2.2, fs=10)
    phasor(ax, A - Np, C4, "$\\dot U_{AN'}$", (0.55, 0.42), start=Np, lw=1.2, ls="--", fs=10)
    ax.plot([Np.real], [Np.imag], "o", color=C2, ms=4)
    ax.text(Np.real + 0.13, Np.imag + 0.1, "$N'$", fontsize=11, color=INK, ha="right")
    ax.text(0.05, -0.1, "$N$", fontsize=11, color=INK)
    ax.text(0.55, 0.98, "单位：$220\\,\\mathrm{V}$", fontsize=9, color=MUTED)
    sfig(fig, "s-phase-seq-phasor")


# ------------------------------------------------------------------ 题9
def s_558_potential():
    """位形图：以 V_c=0 为原点，点 X→Y 的箭头表示 V_Y−V_X。"""
    fig, ax = phasor_axes((-0.45, 1.5), (-1.22, 0.38))
    a, b, c = 1 + 0j, P(1, -60), 0j
    O = (a + b + c) / 3
    for z, s, off in ((a, "$a$", (0.06, 0.07)), (b, "$b$", (-0.08, -0.07)), (c, "$c$", (-0.06, 0.07)),
                      (O, "$O$", (-0.1, -0.06))):
        ax.plot([z.real], [z.imag], "o", color=INK, ms=3.5)
        ax.text(z.real + off[0], z.imag + off[1], s, fontsize=12, color=INK, ha="center", va="center")
    phasor(ax, a - c, MUTED, "$\\dot U=U\\angle0^\\circ$", (0.5, 0.1), start=c, lw=1.2, ls="--", fs=10.5)
    phasor(ax, a - b, C4, "$\\dot U_{ab}$（$L$）", (1.0, -0.48), start=b, lw=1.2, ls="--", fs=10.5)
    phasor(ax, b - c, C4, "$\\dot U_{bc}$（$C$）", (0.03, -0.5), start=c, lw=1.2, ls="--", fs=10.5)
    phasor(ax, a - O, C1, "$\\dot U_A\\angle30^\\circ$", (0.9, -0.2), start=O, fs=10.5)
    phasor(ax, b - O, C2, "$\\dot U_B\\angle(-90^\\circ)$", (0.82, -0.95), start=O, fs=10.5)
    phasor(ax, c - O, C3, "$\\dot U_C\\angle150^\\circ$", (0.12, -0.24), start=O, fs=10.5)
    ax.text(-0.42, -1.18, "等边三角形边长 $U$，$O$ 为中心，$|\\dot U_A|=|\\dot U_B|=|\\dot U_C|=U/\\sqrt{3}$",
            fontsize=9.5, color=MUTED)
    sfig(fig, "s-558-potential")


if __name__ == "__main__":
    s_2_phasor(); s_delta_phasor(); s_delta_line_1ph(); s_551_1ph()
    s_two_watt_phasor(); s_phase_seq_phasor(); s_558_potential()
