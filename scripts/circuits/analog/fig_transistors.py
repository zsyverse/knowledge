"""模电·双极型晶体管与场效应管 插图（前缀 tr-）。

晶体管用 schemdraw 的 elm.BjtNpn / BjtPnp / AnalogNFet / AnalogPFet / JFetN / JFetP，.anchor(...).at(...) 定位。
"""
import os
from pathlib import Path

import numpy as np
from acommon import (elm, new_drawing, save, save_fig, dot, text, cur, wire, gnd, vsrc,
                     axes, plt, C1, C2, C3, C4, MUTED, INK, GRID)

K = "\\,\\mathrm{k}\\Omega"
ARW = dict(headwidth=0.25, headlength=0.3)


def fsave(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    save_fig(fig, name)


def vdd(d, xy, name):
    dot(d, xy, True)
    text(d, (xy[0], xy[1] + 0.45), name)


# ---------------------------------------------------------------- BJT 符号与电流方向
def symbols():
    d = new_drawing()
    q = elm.BjtNpn(circle=True).right().anchor("base").at((0, 0))
    d.add(q)
    b, c, e = q.base, q.collector, q.emitter
    cur(d, (b[0] - 1.4, b[1]), b, "$I_B$", frac=0.45)
    cur(d, (c[0], c[1] + 1.2), c, "$I_C$", loc="bot", frac=0.45)
    cur(d, e, (e[0], e[1] - 1.2), "$I_E$", loc="bot", frac=0.55)
    text(d, (b[0] - 1.6, b[1] + 0.35), "B"); text(d, (c[0] + 0.35, c[1] + 1.2), "C"); text(d, (e[0] + 0.35, e[1] - 1.2), "E")
    text(d, (q.center[0] + 0.2, e[1] - 2.0), "NPN：$I_E=I_B+I_C$", fontsize=14)
    p = elm.BjtPnp(circle=True).right().anchor("base").at((6.0, 0))
    d.add(p)
    b, c, e = p.base, p.collector, p.emitter
    cur(d, b, (b[0] - 1.4, b[1]), "$I_B$", frac=0.55)
    cur(d, (e[0], e[1] + 1.2), e, "$I_E$", loc="bot", frac=0.45)
    cur(d, c, (c[0], c[1] - 1.2), "$I_C$", loc="bot", frac=0.55)
    text(d, (b[0] - 1.6, b[1] + 0.35), "B"); text(d, (e[0] + 0.35, e[1] + 1.2), "E"); text(d, (c[0] + 0.35, c[1] - 1.2), "C")
    text(d, (p.center[0] + 0.2, c[1] - 2.0), "PNP：箭头指向基极", fontsize=14)
    save(d, "tr-symbols")


# ---------------------------------------------------------------- 输入特性
def input_curve():
    fig, ax = axes(4.4, 3.0)
    v = np.linspace(0, 0.8, 300)
    VT = 0.026
    ib = lambda v: 1e-15 * (np.exp(v / VT) - 1) * 1e6 / 1.0   # µA
    ax.plot(v, np.minimum(ib(v + 0.04), 200), color=C2, lw=2, label="$V_{CE}=0$")
    ax.plot(v, np.minimum(ib(v), 200), color=C1, lw=2, label="$V_{CE}\\geq1\\,$V")
    ax.set_xlim(0, 0.8); ax.set_ylim(0, 100)
    ax.set_xlabel("$v_{BE}$ / V", color=INK); ax.set_ylabel("$i_B$ / µA", color=INK)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.annotate("$V_{CE}$ 增大，曲线右移；\n$\\geq1\\,$V 后基本重合", xy=(0.635, 35), xytext=(0.12, 55), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    fsave(fig, "tr-input")


# ---------------------------------------------------------------- 输出特性
def output_curve():
    fig, ax = axes(5.8, 3.4)
    VA = 60.0
    vce = np.linspace(0, 12, 400)
    for ib in (0, 10, 20, 30, 40):
        ic = 100 * ib * 1e-3 * (1 + vce / VA)          # mA
        ic = ic * (1 - np.exp(-vce / 0.12))            # 饱和区
        ax.plot(vce, ic + (0.02 if ib == 0 else 0), color=C1, lw=1.8)
        ax.text(12.15, ic[-1], f"$I_B={ib}\\,\\mu$A", fontsize=9, color=INK, va="center")
    x = np.linspace(0, 0.5, 50)
    ax.plot(x, 4.6 * x / 0.5, color=MUTED, ls="--", lw=1)
    ax.text(0.15, 5.0, "饱和区", fontsize=10, color=C2)
    ax.text(5.0, 5.0, "放大区：$i_C\\approx\\beta i_B$", fontsize=10, color=C2)
    ax.text(5.0, 0.25, "截止区（$i_B\\leq0$）", fontsize=10, color=C2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.6)
    ax.set_xlabel("$v_{CE}$ / V", color=INK); ax.set_ylabel("$i_C$ / mA", color=INK)
    fsave(fig, "tr-output")


# ---------------------------------------------------------------- 固定偏置 / 带 R_E 的偏置
def bias(name, RB, RC, RE=None):
    d = new_drawing()
    q = elm.BjtNpn(circle=True).right().anchor("base").at((3.0, 0))
    d.add(q)
    b, c, e = q.base, q.collector, q.emitter
    top = 4.0
    wire(d, (0, top), (c[0], top))
    vdd(d, (0, top), "$V_{CC}=12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((1.6, top), (1.6, b[1])).label(RB, loc="top"))
    wire(d, (1.6, b[1]), b)
    dot(d, (1.6, top))
    d.add(elm.Resistor().endpoints((c[0], top), (c[0], c[1] + 0.2)).label(RC, loc="bot"))
    wire(d, (c[0], c[1] + 0.2), c)
    if RE:
        d.add(elm.Resistor().endpoints(e, (e[0], e[1] - 2.0)).label(RE, loc="bot"))
        gnd(d, (e[0], e[1] - 2.0))
    else:
        wire(d, e, (e[0], e[1] - 0.6)); gnd(d, (e[0], e[1] - 0.6))
    text(d, (q.center[0] + 1.0, q.center[1] - 0.1), "$\\beta=100$", fontsize=13, color=MUTED, halign="left")
    save(d, name)


# ---------------------------------------------------------------- 混合 π 模型
def hybrid():
    d = new_drawing()
    H = 2.8
    dot(d, (0, H), True); text(d, (-0.45, H), "B")
    wire(d, (0, H), (1.5, H))
    d.add(elm.Resistor().endpoints((1.5, H), (1.5, 0)).label("$r_\\pi$", loc="bot"))
    text(d, (0.75, H - 0.4), "+"); text(d, (0.75, H / 2), "$v_{\\pi}$"); text(d, (0.75, 0.4), "−")
    d.add(elm.SourceControlledI().endpoints((4.0, H), (4.0, 0)).label("$g_mv_\\pi$", loc="bot"))
    d.add(elm.Resistor().endpoints((5.8, H), (5.8, 0)).label("$r_o$", loc="bot"))
    wire(d, (4.0, H), (7.0, H)); dot(d, (7.0, H), True); text(d, (7.45, H), "C")
    wire(d, (0, 0), (5.8, 0))
    dot(d, (0, 0), True); text(d, (-0.45, 0), "E")
    wire(d, (3.4, 0), (3.4, -0.6)); gnd(d, (3.4, -0.6))
    for x in (1.5, 4.0):
        dot(d, (x, 0))
    dot(d, (5.8, H))
    text(d, (3.4, -1.6), "$g_m=I_C/V_T$，$r_\\pi=\\beta/g_m$，$r_o=V_A/I_C$", fontsize=13)
    save(d, "tr-hybrid")


# ---------------------------------------------------------------- 场效应管符号（教材画法）
def _ln(d, p, q):
    d.add(elm.Line().endpoints(p, q))


def fet(d, x, y, kind="nmos", dep=False):
    """教材画法的场效应管：kind = nmos / pmos / njfet / pjfet。
    MOS：沟道线断开为增强型、连续为耗尽型，衬底箭头 N 沟道指向沟道、P 沟道背离沟道，衬底接源极。
    JFET：栅极箭头 N 沟道指向沟道、P 沟道背离沟道。返回 dict(gate, drain, source)。"""
    cx = x + 0.3                      # 沟道线
    if kind in ("nmos", "pmos"):
        _ln(d, (x, y - 0.6), (x, y + 0.6))                    # 栅极板
        _ln(d, (x - 1.0, y - 0.45), (x, y - 0.45))            # 栅极引线
        if dep:
            _ln(d, (cx, y - 0.65), (cx, y + 0.65))
        else:
            for a, b in ((0.35, 0.65), (-0.15, 0.15), (-0.65, -0.35)):
                _ln(d, (cx, y + a), (cx, y + b))
        _ln(d, (cx, y + 0.5), (x + 1.0, y + 0.5)); _ln(d, (x + 1.0, y + 0.5), (x + 1.0, y + 1.3))
        _ln(d, (cx, y - 0.5), (x + 1.0, y - 0.5)); _ln(d, (x + 1.0, y - 0.5), (x + 1.0, y - 1.3))
        _ln(d, (x + 1.0, y), (x + 1.0, y - 0.5))              # 衬底接源极
        if kind == "nmos":
            d.add(elm.Arrow(headwidth=0.22, headlength=0.28).endpoints((x + 1.0, y), (cx, y)))
        else:
            d.add(elm.Arrow(headwidth=0.22, headlength=0.28).endpoints((cx, y), (x + 1.0, y)))
        g = (x - 1.0, y - 0.45)
    else:
        _ln(d, (cx, y - 0.65), (cx, y + 0.65))
        _ln(d, (cx, y + 0.5), (x + 1.0, y + 0.5)); _ln(d, (x + 1.0, y + 0.5), (x + 1.0, y + 1.3))
        _ln(d, (cx, y - 0.5), (x + 1.0, y - 0.5)); _ln(d, (x + 1.0, y - 0.5), (x + 1.0, y - 1.3))
        if kind == "njfet":
            d.add(elm.Arrow(headwidth=0.22, headlength=0.28).endpoints((x - 1.0, y - 0.3), (cx, y - 0.3)))
        else:
            _ln(d, (x - 1.0, y - 0.3), (x - 0.4, y - 0.3))
            d.add(elm.Arrow(headwidth=0.22, headlength=0.28).endpoints((cx, y - 0.3), (x - 0.4, y - 0.3)))
        g = (x - 1.0, y - 0.3)
    return dict(gate=g, drain=(x + 1.0, y + 1.3), source=(x + 1.0, y - 1.3))


def fet_symbols():
    d = new_drawing()
    items = [("nmos", False, "N 沟道增强型"), ("nmos", True, "N 沟道耗尽型"), ("pmos", False, "P 沟道增强型"),
             ("pmos", True, "P 沟道耗尽型"), ("njfet", False, "N 沟道 JFET"), ("pjfet", False, "P 沟道 JFET")]
    for k, (kind, dep, name) in enumerate(items):
        x = k * 3.3
        a = fet(d, x, 0, kind, dep)
        text(d, (a["gate"][0] + 0.1, a["gate"][1] + 0.35), "G", fontsize=12)
        text(d, (a["drain"][0] + 0.35, a["drain"][1] - 0.2), "D", fontsize=12)
        text(d, (a["source"][0] + 0.35, a["source"][1] + 0.2), "S", fontsize=12)
        text(d, (x + 0.2, -2.0), name, fontsize=12)
    save(d, "tr-fet-symbols")


# ---------------------------------------------------------------- 转移特性
def fet_transfer():
    fig, ax = axes(6.0, 3.2)
    v = np.linspace(-5, 5, 500)
    Kn = 0.5
    enh = np.where(v > 1, Kn * (v - 1) ** 2, 0)
    dep = np.where(v > -2, Kn * (v + 2) ** 2, 0)
    jf = np.where((v > -4) & (v <= 0), 8 * (1 - v / -4) ** 2, np.nan)
    ax.plot(v, enh, color=C1, lw=2, label="N 沟道增强型 MOS（$V_{GS(th)}=1\\,$V）")
    ax.plot(v, dep, color=C3, lw=2, label="N 沟道耗尽型 MOS（$V_P=-2\\,$V）")
    ax.plot(v, jf, color=C2, lw=2, label="N 沟道 JFET（$V_P=-4\\,$V，$I_{DSS}=8\\,$mA）")
    ax.plot([0], [8], "o", color=C2)
    ax.annotate("$I_{DSS}$", xy=(0, 8), xytext=(0.3, 7.2), fontsize=10, color=INK)
    ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlim(-5, 5); ax.set_ylim(0, 14)
    ax.set_xlabel("$v_{GS}$ / V", color=INK); ax.set_ylabel("$i_D$ / mA", color=INK)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False)
    fsave(fig, "tr-fet-transfer")


# ---------------------------------------------------------------- MOS 输出特性
def mos_output():
    fig, ax = axes(5.8, 3.4)
    Kn, VT, lam = 0.5, 1.0, 0.02
    vds = np.linspace(0, 10, 400)
    for vgs in (2, 3, 4):
        vov = vgs - VT
        tri = Kn * (2 * vov * vds - vds ** 2)
        sat = Kn * vov ** 2 * (1 + lam * (vds - vov))
        idd = np.where(vds < vov, tri * (1 + 0 * vds), sat)
        ax.plot(vds, idd, color=C1, lw=1.8)
        ax.text(10.15, idd[-1], f"$V_{{GS}}={vgs}\\,$V", fontsize=9, color=INK, va="center")
    x = np.linspace(0, 3.2, 100)
    ax.plot(x, Kn * x ** 2, color=C2, ls="--", lw=1.2)
    ax.text(2.6, 5.4, "$v_{DS}=v_{GS}-V_{GS(th)}$", fontsize=10, color=C2)
    ax.text(0.15, 4.3, "可变电阻区", fontsize=10, color=INK)
    ax.text(5.2, 3.4, "饱和区（恒流区）", fontsize=10, color=INK)
    ax.text(5.2, 0.03, "截止区：$v_{GS}\\leq V_{GS(th)}$ 时 $i_D=0$", fontsize=9, color=INK, va="bottom")
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.set_xlabel("$v_{DS}$ / V", color=INK); ax.set_ylabel("$i_D$ / mA", color=INK)
    fsave(fig, "tr-mos-output")


# ---------------------------------------------------------------- 分压偏置 NMOS
def cs_bias():
    d = new_drawing()
    a = fet(d, 3.2, 0, "nmos")
    g, dr, s = a["gate"], a["drain"], a["source"]
    top, bot = 4.2, -3.6
    wire(d, (0.8, top), (dr[0], top))
    vdd(d, (0.8, top), "$V_{DD}=12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0.8, top), (0.8, -0.45)).label(f"$R_{{G1}}=200{K}$", loc="top"))
    d.add(elm.Resistor().endpoints((0.8, -0.45), (0.8, bot)).label(f"$R_{{G2}}=100{K}$", loc="top"))
    wire(d, (0.8, g[1]), g); dot(d, (0.8, g[1]))
    d.add(elm.Resistor().endpoints((dr[0], top), dr).label(f"$R_D=3{K}$", loc="bot"))
    d.add(elm.Resistor().endpoints(s, (s[0], bot)).label(f"$R_S=1{K}$", loc="bot"))
    wire(d, (0.8, bot), (s[0], bot)); dot(d, (s[0], bot))
    gnd(d, ((0.8 + s[0]) / 2, bot))
    dot(d, (dr[0], top))
    save(d, "tr-cs-bias")


if __name__ == "__main__":
    symbols()
    input_curve()
    output_curve()
    bias("tr-fixed-bias", f"$R_B=565{K}$", f"$R_C=3{K}$")
    bias("tr-bias-re", f"$R_B=430{K}$", f"$R_C=2{K}$", f"$R_E=1{K}$")
    hybrid()
    fet_symbols()
    fet_transfer()
    mos_output()
    cs_bias()
