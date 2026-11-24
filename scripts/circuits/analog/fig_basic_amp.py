"""模电·基本放大电路 插图（前缀 ba-）。

例题参数（与 verify_basic_amp.py 一致）：V_CC=12 V，R_B1=40 kΩ，R_B2=10 kΩ，R_C=3 kΩ，R_E=1 kΩ，
R_L=6 kΩ，β=100 → Q(I_CQ≈1.56 mA，V_CEQ≈5.75 V)。
"""
import numpy as np
from acommon import (elm, new_drawing, save, save_fig, dot, text, cur, wire, gnd, ac_src, axes, plt,
                     C1, C2, C3, MUTED, INK, GRID, isrc)

K = "\\,\\mathrm{k}\\Omega"


def R(d, p, q, lab=None, loc="top", **kw):
    e = elm.Resistor().endpoints(p, q)
    if lab:
        e.label(lab, loc=loc, **kw)
    d.add(e)
    return e


def Cap(d, p, q, lab=None, loc="top", **kw):
    e = elm.Capacitor().endpoints(p, q)
    if lab:
        e.label(lab, loc=loc, **kw)
    d.add(e)
    return e


def term(d, xy, name, dx=0.0, dy=0.45):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1] + dy), name)


def rail(d, x1, x2, y, name="$+V_{CC}$"):
    wire(d, (x1, y), (x2, y))
    dot(d, (x2, y), True)
    text(d, (x2 + 0.75, y), name)


def source_in(d, x0, y_top, y_bot, x_node):
    """信号源 v_s（内阻 R_s），输出端在 (x_node, y_top)。"""
    ac_src(d, (x0, y_bot), (x0, y_top - 1.0), "$v_s$", loc="bot")
    wire(d, (x0, y_top - 1.0), (x0, y_top))
    R(d, (x0, y_top), (x_node, y_top), "$R_s$")


# ---------------------------------------------------------------- 电路
def ce_full():
    """分压式偏置共射放大电路（带 R_E、C_E、负载）。"""
    d = new_drawing()
    yb, yt, gy = 2.5, 6.6, -1.0
    xb = 3.4                                   # 基极节点
    q = elm.BjtNpn().anchor("base").at((xb + 1.0, yb))
    d.add(q)
    xc = q.collector[0]
    source_in(d, -2.4, yb, gy, -0.4)
    term(d, (-0.4, yb), "$v_i$", dy=0.5)
    Cap(d, (-0.4, yb), (xb, yb), "$C_1$")
    wire(d, (xb, yb), q.base)
    dot(d, (xb, yb))
    R(d, (xb, yt), (xb, yb), "$R_{B1}$", loc="bot")
    R(d, (xb, yb), (xb, gy), "$R_{B2}$", loc="bot")
    yc = yb + 1.5
    R(d, (xc, yt), (xc, yc), "$R_C$")
    wire(d, (xc, yc), q.collector)
    dot(d, (xc, yc))
    rail(d, xb, xc + 1.6, yt)
    dot(d, (xc, yt))
    ye = yb - 1.4
    wire(d, q.emitter, (xc, ye))
    dot(d, (xc, ye))
    R(d, (xc, ye), (xc, gy), "$R_E$")
    wire(d, (xc, ye), (xc + 1.4, ye))
    Cap(d, (xc + 1.4, ye), (xc + 1.4, gy), "$C_E$", loc="bot")
    xl = xc + 3.6
    Cap(d, (xc, yc), (xl, yc), "$C_2$")
    dot(d, (xl, yc))
    R(d, (xl, yc), (xl, gy), "$R_L$")
    wire(d, (xl, yc), (xl + 1.0, yc))
    term(d, (xl + 1.0, yc), "$v_o$", dx=0.5, dy=0)
    wire(d, (-2.4, gy), (xl, gy))
    for x in (xb, xc, xc + 1.4):
        dot(d, (x, gy))
    gnd(d, (xc + 0.7, gy))
    save(d, "ba-ce-full")


def dc_thevenin():
    """直流通路：基极分压网络用戴维南等效 V_BB、R_BB 代替。"""
    d = new_drawing()
    gy, yb = -1.2, 1.6
    q = elm.BjtNpn().anchor("base").at((3.2, yb))
    d.add(q)
    xc = q.collector[0]
    d.add(elm.SourceV().endpoints((0, gy), (0, yb)).label("$V_{BB}$", loc="bot"))
    R(d, (0, yb), (2.2, yb), "$R_{BB}$")
    cur(d, (2.2, yb), q.base, "$I_B$", frac=0.5)
    yt = yb + 3.2
    R(d, (xc, yt), (xc, yb + 1.5), "$R_C$")
    cur(d, (xc, yb + 1.5), q.collector, "$I_C$", loc="bot", frac=0.45)
    dot(d, (xc, yt), True)
    text(d, (xc + 0.9, yt), "$+V_{CC}$")
    cur(d, q.emitter, (xc, yb - 1.3), "$I_E$", loc="bot", frac=0.55)
    R(d, (xc, yb - 1.3), (xc, gy), "$R_E$", loc="bot")
    wire(d, (0, gy), (xc, gy))
    gnd(d, (xc / 2 + 0.6, gy))
    text(d, (xc + 1.25, yb), "$V_{CE}$")
    text(d, (xc + 1.25, yb + 0.6), "+", fontsize=13)
    text(d, (xc + 1.25, yb - 0.6), "−", fontsize=13)
    save(d, "ba-dc-thevenin")


def ce_ss(re=False):
    """共射电路的小信号等效电路（hybrid-π，忽略 r_o）。re=True 时射极电阻未旁路。"""
    d = new_drawing()
    yt = 3.0
    ye = 0.9 if re else 0.0
    gy = -0.9 if re else 0.0
    ac_src(d, (0, gy), (0, yt - 1.2), "$v_s$", loc="bot")
    wire(d, (0, yt - 1.2), (0, yt))
    R(d, (0, yt), (2.0, yt), "$R_s$")
    term(d, (2.0, yt), "$v_i$", dy=0.5)
    R(d, (2.8, yt), (2.8, gy), "$R_B$", loc="bot")
    wire(d, (2.0, yt), (4.8, yt))
    dot(d, (2.8, yt))
    text(d, (4.8, yt + 0.45), "$b$")
    R(d, (4.8, yt), (4.8, ye), "$r_\\pi$")
    text(d, (5.35, yt - 0.45), "+", fontsize=13)
    text(d, (5.4, (yt + ye) / 2), "$v_\\pi$")
    text(d, (5.35, ye + 0.45), "−", fontsize=13)
    xs = 7.0
    d.add(elm.SourceControlledI().endpoints((xs, yt), (xs, ye)).label("$g_m v_\\pi$", loc="bot"))
    text(d, (xs, yt + 0.45), "$c$")
    wire(d, (xs, yt), (10.6, yt))
    R(d, (9.0, yt), (9.0, gy), "$R_C$", loc="bot")
    R(d, (10.6, yt), (10.6, gy), "$R_L$", loc="bot")
    dot(d, (9.0, yt))
    wire(d, (10.6, yt), (11.4, yt))
    term(d, (11.4, yt), "$v_o$", dx=0.5, dy=0)
    if re:
        wire(d, (4.8, ye), (xs, ye))
        xm = (4.8 + xs) / 2
        dot(d, (xm, ye))
        text(d, (xm, ye + 0.4), "$e$")
        R(d, (xm, ye), (xm, gy), "$R_E$", loc="bot")
        wire(d, (0, gy), (10.6, gy))
        gnd(d, (xm, gy))
    else:
        wire(d, (0, gy), (10.6, gy))
        text(d, (5.9, gy + 0.4), "$e$")
        gnd(d, (5.9, gy))
    for x in (2.8, 9.0) + ((4.8, xs) if not re else ()):
        dot(d, (x, gy))
    if re:
        dot(d, (2.8, gy)); dot(d, (9.0, gy))
    save(d, "ba-ce-ss-re" if re else "ba-ce-ss")


def cc_amp():
    """共集电极放大电路（射极跟随器）。"""
    d = new_drawing()
    yb, yt, gy = 2.5, 5.8, -1.0
    xb = 3.4
    q = elm.BjtNpn().anchor("base").at((xb + 1.0, yb))
    d.add(q)
    xc = q.collector[0]
    source_in(d, -2.4, yb, gy, -0.4)
    term(d, (-0.4, yb), "$v_i$", dy=0.5)
    Cap(d, (-0.4, yb), (xb, yb), "$C_1$")
    wire(d, (xb, yb), q.base)
    dot(d, (xb, yb))
    R(d, (xb, yt), (xb, yb), "$R_{B1}$", loc="bot")
    R(d, (xb, yb), (xb, gy), "$R_{B2}$", loc="bot")
    wire(d, q.collector, (xc, yt))
    rail(d, xb, xc + 1.6, yt)
    dot(d, (xc, yt))
    ye = yb - 1.4
    wire(d, q.emitter, (xc, ye))
    dot(d, (xc, ye))
    R(d, (xc, ye), (xc, gy), "$R_E$", loc="bot")
    xl = xc + 3.0
    Cap(d, (xc, ye), (xl, ye), "$C_2$")
    dot(d, (xl, ye))
    R(d, (xl, ye), (xl, gy), "$R_L$")
    wire(d, (xl, ye), (xl + 1.0, ye))
    term(d, (xl + 1.0, ye), "$v_o$", dx=0.5, dy=0)
    wire(d, (-2.4, gy), (xl, gy))
    for x in (xb, xc):
        dot(d, (x, gy))
    gnd(d, ((xb + xc) / 2, gy))
    save(d, "ba-cc")


def cb_amp():
    """共基极放大电路：基极经 C_B 交流接地，信号从射极输入、集电极输出。"""
    d = new_drawing()
    yb, yt, gy = 2.5, 6.6, -1.0
    xb = 2.6
    q = elm.BjtNpn().anchor("base").at((xb + 1.0, yb))
    d.add(q)
    xc = q.collector[0]
    R(d, (xb, yt), (xb, yb), "$R_{B1}$", loc="bot")
    R(d, (xb, yb), (xb, gy), "$R_{B2}$", loc="bot")
    wire(d, (xb, yb), q.base)
    dot(d, (xb, yb))
    wire(d, (xb, yb), (xb - 1.5, yb))
    Cap(d, (xb - 1.5, yb), (xb - 1.5, gy), "$C_B$", loc="bot")
    yc = yb + 1.5
    R(d, (xc, yt), (xc, yc), "$R_C$")
    wire(d, (xc, yc), q.collector)
    dot(d, (xc, yc))
    rail(d, xb, xc + 1.6, yt)
    dot(d, (xc, yt))
    ye = yb - 1.4
    wire(d, q.emitter, (xc, ye))
    dot(d, (xc, ye))
    R(d, (xc, ye), (xc, gy), "$R_E$")
    # 射极输入：从右下方经 C_1 进入，避免与基极支路交叉
    xi = xc + 2.6
    Cap(d, (xi, ye), (xc, ye), "$C_1$", loc="bot")
    d.add(elm.Resistor().endpoints((xi + 2.2, ye), (xi, ye)).label("$R_s$", loc="bot"))
    term(d, (xi, ye), "$v_i$", dy=-0.5)
    ac_src(d, (xi + 2.2, gy), (xi + 2.2, ye), "$v_s$")
    xl = xc + 3.6
    Cap(d, (xc, yc), (xl, yc), "$C_2$")
    dot(d, (xl, yc))
    R(d, (xl, yc), (xl, ye + 0.9), "$R_L$")
    wire(d, (xl, ye + 0.9), (xl + 1.6, ye + 0.9))
    gnd(d, (xl + 1.6, ye + 0.9))
    wire(d, (xl, yc), (xl + 1.0, yc))
    term(d, (xl + 1.0, yc), "$v_o$", dx=0.5, dy=0)
    wire(d, (xb - 1.5, gy), (xi + 2.2, gy))
    for x in (xb, xc):
        dot(d, (x, gy))
    gnd(d, ((xb + xc) / 2 - 0.4, gy))
    save(d, "ba-cb")


def cs_amp():
    """分压式偏置共源放大电路（增强型 NMOS）。"""
    d = new_drawing()
    yg, yt, gy = 2.5, 6.6, -1.0
    xg = 3.4
    m = elm.NFet().reverse().anchor("gate").at((xg + 1.0, yg))
    d.add(m)
    xd = m.drain[0]
    source_in(d, -2.4, yg, gy, -0.4)
    term(d, (-0.4, yg), "$v_i$", dy=0.5)
    Cap(d, (-0.4, yg), (xg, yg), "$C_1$")
    wire(d, (xg, yg), m.gate)
    dot(d, (xg, yg))
    R(d, (xg, yt), (xg, yg), "$R_{G1}$", loc="bot")
    R(d, (xg, yg), (xg, gy), "$R_{G2}$", loc="bot")
    yd = yg + 1.6
    R(d, (xd, yt), (xd, yd), "$R_D$")
    wire(d, (xd, yd), m.drain)
    dot(d, (xd, yd))
    rail(d, xg, xd + 1.6, yt, "$+V_{DD}$")
    dot(d, (xd, yt))
    ys = yg - 1.5
    wire(d, m.source, (xd, ys))
    dot(d, (xd, ys))
    R(d, (xd, ys), (xd, gy), "$R_S$")
    wire(d, (xd, ys), (xd + 1.4, ys))
    Cap(d, (xd + 1.4, ys), (xd + 1.4, gy), "$C_S$", loc="bot")
    xl = xd + 3.6
    Cap(d, (xd, yd), (xl, yd), "$C_2$")
    dot(d, (xl, yd))
    R(d, (xl, yd), (xl, gy), "$R_L$")
    wire(d, (xl, yd), (xl + 1.0, yd))
    term(d, (xl + 1.0, yd), "$v_o$", dx=0.5, dy=0)
    wire(d, (-2.4, gy), (xl, gy))
    for x in (xg, xd, xd + 1.4):
        dot(d, (x, gy))
    gnd(d, (xd + 0.7, gy))
    save(d, "ba-cs")


def mirror(widlar=False):
    """基本 BJT 电流镜（widlar=True：T2 射极串 R_E 的微电流源）。"""
    d = new_drawing()
    gy, yb, yt = (-3.0 if widlar else -1.6), 0.0, 5.0
    q1 = elm.BjtNpn().reverse().anchor("base").at((2.2, yb))
    q2 = elm.BjtNpn().anchor("base").at((3.6, yb))
    d.add(q1); d.add(q2)
    x1, x2 = q1.collector[0], q2.collector[0]
    wire(d, q1.base, q2.base)
    xm = 2.9
    dot(d, (xm, yb))
    yk = yb + 1.5
    cur(d, (x1, yk), q1.collector, "$I_{C1}$", loc="top", frac=0.55)
    wire(d, (x1, yk), (xm, yk))
    cur(d, (xm, yk), (xm, yb), "$2I_B$", loc="bot", frac=0.5)
    dot(d, (x1, yk))
    R(d, (x1, yt), (x1, yk + 1.2), "$R$")
    cur(d, (x1, yk + 1.2), (x1, yk), "$I_{REF}$", loc="top", frac=0.5)
    d.add(elm.Resistor().endpoints((x2, yt), (x2, yb + 2.3)).label("负载", loc="bot"))
    cur(d, (x2, yb + 2.3), q2.collector, "$I_O$", loc="bot", frac=0.5)
    wire(d, (x1, yt), (x2, yt))
    dot(d, (x2, yt))
    wire(d, (x2, yt), (x2 + 1.0, yt))
    dot(d, (x2 + 1.0, yt), True)
    text(d, (x2 + 1.8, yt), "$+V_{CC}$")
    wire(d, q1.emitter, (x1, gy))
    if widlar:
        R(d, q2.emitter, (x2, gy), "$R_E$", loc="bot")
    else:
        wire(d, q2.emitter, (x2, gy))
    wire(d, (x1, gy), (x2, gy))
    gnd(d, (xm, gy))
    text(d, (x1 - 0.6, yb - 0.05), "$T_1$")
    text(d, (x2 + 0.6, yb - 0.05), "$T_2$")
    save(d, "ba-widlar" if widlar else "ba-mirror")


# ---------------------------------------------------------------- 曲线
def loadlines():
    Vcc, Rc, Re, RL, beta, VT = 12.0, 3.0, 1.0, 6.0, 100, 0.026
    Vbb, Rbb = 12 * 10 / 50, 8.0
    IB = (Vbb - 0.7) / (Rbb + (1 + beta) * Re)
    IC = beta * IB
    VCE = Vcc - IC * Rc - (1 + beta) * IB * Re
    RLp = Rc * RL / (Rc + RL)
    fig, ax = axes(5.8, 3.6)
    v = np.linspace(0, 13, 400)
    for ib in (0.005, 0.010, IB, 0.020, 0.025):
        ic = beta * ib * (1 - np.exp(-v / 0.12)) * (1 + v / 150)
        ax.plot(v, ic, color=C1 if ib == IB else "#9db8dc", lw=1.4 if ib == IB else 1.0)
        ax.text(12.6, beta * ib * (1 + 12.6 / 150), f"{ib * 1000:.1f} µA" if ib == IB else f"{ib * 1000:.0f} µA",
                color=MUTED, fontsize=8, va="center")
    # 直流负载线：V_CE = V_CC − I_C (R_C + R_E)（I_E≈I_C）
    ax.plot([0, Vcc], [Vcc / (Rc + Re), 0], color=INK, lw=1.4)
    ax.text(1.0, Vcc / (Rc + Re) - 0.12, "直流负载线  斜率 $-1/(R_C+R_E)$", color=INK, fontsize=9)
    # 交流负载线：过 Q，斜率 −1/R_L'
    v0 = VCE + IC * RLp
    i0 = IC + VCE / RLp
    ax.plot([0, v0], [i0, 0], color=C2, lw=1.6)
    ax.text(2.4, 3.75, "交流负载线  斜率 $-1/R_L'$", color=C2, fontsize=9)
    ax.plot([VCE], [IC], "o", color=C2, ms=6, zorder=5)
    ax.annotate(f"Q({VCE:.2f} V, {IC:.2f} mA)", xy=(VCE, IC), xytext=(7.0, 2.27), color=INK, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.plot([VCE, VCE], [0, IC], ls="--", color=MUTED, lw=0.8)
    ax.plot([0, VCE], [IC, IC], ls="--", color=MUTED, lw=0.8)
    # 摆幅
    ax.annotate("", xy=(v0, -0.18), xytext=(VCE, -0.18), arrowprops=dict(arrowstyle="<->", color=C3))
    ax.text((VCE + v0) / 2, -0.42, "$I_{CQ}R_L'$", color=C3, fontsize=9, ha="center")
    ax.annotate("", xy=(0.2, -0.18), xytext=(VCE, -0.18), arrowprops=dict(arrowstyle="<->", color=C3))
    ax.text((0.2 + VCE) / 2, -0.42, "$V_{CEQ}-V_{CE(sat)}$", color=C3, fontsize=9, ha="center")
    ax.axvspan(0, 0.2, color=GRID, alpha=0.7)
    ax.text(0.28, 0.6, "饱和区", color=MUTED, fontsize=8, rotation=90)
    ax.text(9.6, 0.12, "截止区 $I_C\\approx0$", color=MUTED, fontsize=8)
    ax.set_xlim(0, 13.8); ax.set_ylim(-0.6, 4.7)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12]); ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_xlabel("$v_{CE}$ / V", color=INK, loc="right")
    ax.set_ylabel("$i_C$ / mA", color=INK)
    save_fig(fig, "ba-loadlines")


def distortion():
    """Q 点偏低/偏高时 NPN 共射输出 v_o 的削波。"""
    t = np.linspace(0, 2, 400)
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2))
    for ax, (title, top, bot) in zip(axs, (("Q 点偏低 → 截止失真", 0.6, -1.2), ("Q 点偏高 → 饱和失真", 1.2, -0.6))):
        s = np.sin(2 * np.pi * t)
        ax.plot(t, s, color=GRID, lw=1.0, ls="--")
        ax.plot(t, np.clip(s, bot, top), color=C1, lw=1.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(MUTED)
        ax.set_xticks([]); ax.set_yticks([0], ["0"])
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_ylabel("$v_o$", color=INK)
    axs[0].text(0.1, 0.75, "顶部削平", color=C2, fontsize=9)
    axs[1].text(0.55, -0.92, "底部削平", color=C2, fontsize=9)
    fig.tight_layout()
    save_fig(fig, "ba-distortion")


if __name__ == "__main__":
    ce_full()
    dc_thevenin()
    ce_ss()
    ce_ss(re=True)
    cc_amp()
    cb_amp()
    cs_amp()
    mirror()
    mirror(widlar=True)
    loadlines()
    distortion()
