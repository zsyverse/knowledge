"""习题·非正弦周期电路 解析插图（images/ex/sol/n-*）。数值见 verify_nonsin.py。"""
import numpy as np

from solcommon import (elm, new_drawing, ssave, sfig, dot, text, note, cur, arrow, wire, ac_src, vsrc, isrc,
                       axes, OHM, C1, C2, INK, MUTED)


# ------------------------------------------------------------------ 题3 叠加
def n_multisrc_dc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label(f"$4{OHM}$"))
    arrow(d, (1.3, 3.3), (2.7, 3.3), "$1.5\\,\\mathrm{A}$", loc="bot")
    dot(d, (4, 4)); text(d, (4, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((4, 4), (4, 0)).label(f"$4{OHM}$", loc="top")
          .label(("+", "$U_{a0}=6\\,\\mathrm{V}$", "−"), loc="bot"))
    wire(d, (0, 0), (4, 0))
    note(d, (2.0, -0.7), "（电流源开路）")
    ssave(d, "n-multisrc-dc")


def n_multisrc_ac():
    d = new_drawing()
    wire(d, (0, 0), (0, 4))
    note(d, (-0.3, 2), "电压源\n短路", halign="right")
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label(f"$4{OHM}$"))
    dot(d, (4, 4)); text(d, (4, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((4, 4), (4, 0)).label(f"$4{OHM}$", loc="top")
          .label(("+", "$\\dot U_{a1}=4\\angle0^\\circ\\,\\mathrm{V}$", "−"), loc="bot"))
    wire(d, (4, 4), (9, 4))
    isrc(d, (9, 0), (9, 4), "$\\dot I_S=2\\angle0^\\circ\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (9, 0))
    dot(d, (4, 0))
    ssave(d, "n-multisrc-ac")


# ------------------------------------------------------------------ 题5 RC 低通
def n_rc_h():
    fig, ax = axes(5.6, 3.0)
    w = np.logspace(1.5, 5, 400)
    H = 1 / np.sqrt(1 + (w / 1000) ** 2)
    ax.semilogx(w, H, color=C1, lw=2)
    ax.axvline(1000, color=MUTED, lw=0.8, ls="--")
    for wk, hk, lab, xy in ((1000, 1 / np.sqrt(2), "$\\omega=1000$：$|H|=0.707$", (1700, 0.82)),
                            (1e4, 1 / np.sqrt(101), "$\\omega=10^4$：$|H|=0.0995$", (1.4e4, 0.25))):
        ax.plot([wk], [hk], "o", color=C2, ms=6)
        ax.annotate(lab, (wk, hk), xy, fontsize=10, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(1000, 1.06, "$\\omega_c=1/RC$", fontsize=10, color=INK, ha="center")
    ax.set_xlim(10 ** 1.5, 1e5); ax.set_ylim(0, 1.12)
    ax.set_xticks([1e2, 1e3, 1e4, 1e5], ["$10^2$", "$10^3$", "$10^4$", "$10^5$"])
    ax.set_xlabel("$\\omega$/(rad/s)", color=INK, loc="right"); ax.set_ylabel("$|H(j\\omega)|$", color=INK)
    sfig(fig, "n-rc-h")


# ------------------------------------------------------------------ 题6 各次谐波单独作用
def _rlc_panel(d, x, y, title, src, kind):
    text(d, (x + 2.4, y + 4.7), title, fontsize=14)
    if kind == "dc":
        vsrc(d, (x, y), (x, y + 3.6), src, loc="top")
    else:
        ac_src(d, (x, y), (x, y + 3.6), src, loc="top")
    d.add(elm.Resistor().endpoints((x, y + 3.6), (x + 2.4, y + 3.6)).label(f"$10{OHM}$"))
    if kind == "dc":
        d.add(elm.Line().endpoints((x + 2.4, y + 3.6), (x + 4.8, y + 3.6)).label("$L$ 短路", color=MUTED, fontsize=12))
        wire(d, (x + 4.8, y + 3.6), (x + 4.8, y + 2.7)); wire(d, (x + 4.8, y + 0.9), (x + 4.8, y))
        dot(d, (x + 4.8, y + 2.7), True); dot(d, (x + 4.8, y + 0.9), True)
        text(d, (x + 5.1, y + 2.4), "+"); text(d, (x + 5.1, y + 1.2), "−")
        text(d, (x + 5.3, y + 1.8), "$U_{C0}=10\\,\\mathrm{V}$", halign="left")
        note(d, (x + 4.5, y + 1.8), "$C$ 开路", halign="right")
        res = "$I_0=0$"
    else:
        xl = "$j3\\,\\Omega$" if kind == "h1" else "$j9\\,\\Omega$"
        xc = "$-j27\\,\\Omega$" if kind == "h1" else "$-j9\\,\\Omega$"
        d.add(elm.Inductor2(loops=3).endpoints((x + 2.4, y + 3.6), (x + 4.8, y + 3.6)).label(xl))
        d.add(elm.Capacitor().endpoints((x + 4.8, y + 3.6), (x + 4.8, y)).label(xc, loc="bot"))
        res = "$\\dot I_1=3.846\\angle67.38^\\circ\\,\\mathrm{A}$" if kind == "h1" else \
            "$\\dot I_3=3\\angle0^\\circ\\,\\mathrm{A}$（串联谐振）"
    wire(d, (x, y), (x + 4.8, y))
    text(d, (x + 2.4, y - 0.7), res, fontsize=13)


def n_rlc_h():
    d = new_drawing()
    _rlc_panel(d, 0, 7.0, "直流", "$10\\,\\mathrm{V}$", "dc")
    _rlc_panel(d, 10.5, 7.0, "基波 $\\omega$", "$100\\angle0^\\circ\\,\\mathrm{V}$", "h1")
    _rlc_panel(d, 5.2, 0, "3 次谐波 $3\\omega$", "$30\\angle0^\\circ\\,\\mathrm{V}$", "h3")
    ssave(d, "n-rlc-h")


# ------------------------------------------------------------------ 题7 滤波网络在两个频率下
def _filter_row(d, y, title, src, xl, xc1, xc2, tank, out):
    text(d, (-2.0, y + 4.4), title, fontsize=14, halign="left")
    ac_src(d, (0, y), (0, y + 2.4), src, loc="top")
    wire(d, (0, y + 2.4), (1.0, y + 2.4))
    wire(d, (1.0, y + 2.4), (1.0, y + 3.3)); wire(d, (1.0, y + 2.4), (1.0, y + 1.5))
    d.add(elm.Inductor2(loops=3).endpoints((1.0, y + 3.3), (4.0, y + 3.3)).label(xl))
    d.add(elm.Capacitor().endpoints((1.0, y + 1.5), (4.0, y + 1.5)).label(xc1, loc="bot"))
    wire(d, (4.0, y + 3.3), (4.0, y + 1.5))
    dot(d, (1.0, y + 2.4)); dot(d, (4.0, y + 2.4))
    wire(d, (4.0, y + 2.4), (4.8, y + 2.4))
    d.add(elm.Capacitor().endpoints((4.8, y + 2.4), (7.6, y + 2.4)).label(xc2))
    wire(d, (7.6, y + 2.4), (8.6, y + 2.4))
    d.add(elm.Resistor().endpoints((8.6, y + 2.4), (8.6, y)).label(f"$50{OHM}$", loc="bot"))
    wire(d, (0, y), (8.6, y))
    note(d, (4.3, y - 0.6), tank)
    text(d, (11.2, y + 1.2), out, halign="left")


def n_filter_h():
    d = new_drawing()
    _filter_row(d, 6.6, "基波 $\\omega=1000$", "$100\\angle0^\\circ\\,\\mathrm{V}$", "$j11.11\\,\\Omega$", "$-j100\\,\\Omega$",
                "$-j12.5\\,\\Omega$", "槽路 $=j12.5\\,\\Omega$，与 $C_2$ 串联后 $=0$", "$\\dot U_{R1}=100\\angle0^\\circ$")
    _filter_row(d, 0, "3 次谐波 $3\\omega=3000$", "$20\\angle0^\\circ\\,\\mathrm{V}$", "$j33.3\\,\\Omega$", "$-j33.3\\,\\Omega$",
                "$-j4.17\\,\\Omega$", "槽路并联谐振 → 开路", "$\\dot U_{R3}=0$")
    ssave(d, "n-filter-h")


if __name__ == "__main__":
    n_multisrc_dc(); n_multisrc_ac(); n_rc_h(); n_rlc_h(); n_filter_h()
