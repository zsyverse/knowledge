"""模电·频率响应 插图（前缀 fr-）。数值与 verify_freq.py 一致。"""
import numpy as np
from acommon import (elm, new_drawing, save, save_fig, dot, text, wire, gnd, ac_src, axes, plt,
                     C1, C2, C3, MUTED, INK, GRID)


def R(d, p, q, lab=None, loc="top", **kw):
    e = elm.Resistor().endpoints(p, q)
    if lab:
        e.label(lab, loc=loc, **kw)
    d.add(e)


def Cap(d, p, q, lab=None, loc="top", **kw):
    e = elm.Capacitor().endpoints(p, q)
    if lab:
        e.label(lab, loc=loc, **kw)
    d.add(e)


def term(d, xy, name, dx=-0.5, dy=0.0):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1] + dy), name)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(True, which="major", color=GRID, lw=0.6)


# ---------------------------------------------------------------- 电路
def rc_circuits():
    d = new_drawing()
    for x0, hp in ((0, False), (7.0, True)):
        y, gy = 2.2, 0.0
        term(d, (x0, y), "$v_i$")
        term(d, (x0, gy), "")
        if hp:
            Cap(d, (x0, y), (x0 + 2.6, y), "$C$")
            R(d, (x0 + 2.6, y), (x0 + 2.6, gy), "$R$", loc="bot")
        else:
            R(d, (x0, y), (x0 + 2.6, y), "$R$")
            Cap(d, (x0 + 2.6, y), (x0 + 2.6, gy), "$C$", loc="bot")
        dot(d, (x0 + 2.6, y)); dot(d, (x0 + 2.6, gy))
        wire(d, (x0 + 2.6, y), (x0 + 4.0, y))
        wire(d, (x0, gy), (x0 + 4.0, gy))
        term(d, (x0 + 4.0, y), "$v_o$", dx=0.5)
        term(d, (x0 + 4.0, gy), "")
        text(d, (x0 + 2.0, -0.8), "高通" if hp else "低通", color=MUTED, fontsize=13)
    save(d, "fr-rc")


def hybrid_pi(miller=False):
    """共射高频小信号等效电路（r_bb'=0）；miller=True 时把 C_μ 换成两端的米勒等效电容。"""
    d = new_drawing()
    yt, gy = 3.0, 0.0
    ac_src(d, (0, gy), (0, yt - 1.2), "$v_s$", loc="bot")
    wire(d, (0, yt - 1.2), (0, yt))
    R(d, (0, yt), (2.0, yt), "$R_s$")
    R(d, (2.8, yt), (2.8, gy), "$R_B$", loc="bot")
    xb = 4.6
    R(d, (xb, yt), (xb, gy), "$r_\\pi$", loc="bot")
    Cap(d, (xb + 1.3, yt), (xb + 1.3, gy), "$C_\\pi$", loc="bot")
    text(d, (xb + 0.45, yt + 0.45), "$b$")
    xc = 11.0 if miller else 9.0
    xs = xc - 1.2 if miller else xc
    if miller:
        xm = xb + 2.8
        Cap(d, (xm, yt), (xm, gy), "$C_M$", loc="bot")
        wire(d, (2.0, yt), (xm, yt))
        for x in (2.8, xb, xb + 1.3):
            dot(d, (x, yt)); dot(d, (x, gy))
        wire(d, (xs, yt), (xc + 3.0, yt))
        Cap(d, (xc + 1.0, yt), (xc + 1.0, gy), "$\\approx C_\\mu$", loc="bot")
        dot(d, (xc + 1.0, yt)); dot(d, (xc + 1.0, gy))
        xl = xc + 3.0
    else:
        wire(d, (2.0, yt), (xb + 1.3, yt))
        for x in (2.8, xb):
            dot(d, (x, yt)); dot(d, (x, gy))
        wire(d, (xb + 1.3, yt), (xb + 1.3, yt + 1.2))
        Cap(d, (xb + 1.3, yt + 1.2), (xc, yt + 1.2), "$C_\\mu$")
        wire(d, (xc, yt + 1.2), (xc, yt))
        dot(d, (xb + 1.3, yt))
        wire(d, (xc, yt), (xc + 2.2, yt))
        xl = xc + 2.2
    d.add(elm.SourceControlledI().endpoints((xs, yt), (xs, gy)).label("$g_m v_\\pi$", loc="bot"))
    text(d, (xs, yt + 0.45) if miller else (xc + 0.4, yt + 0.4), "$c$")
    R(d, (xl, yt), (xl, gy), "$R_C\\parallel R_L$", loc="bot")
    dot(d, (xs, yt)); dot(d, (xs, gy))
    wire(d, (xl, yt), (xl + 0.8, yt))
    term(d, (xl + 0.8, yt), "$v_o$", dx=0.5)
    text(d, (xb - 0.45, yt - 0.5), "+", fontsize=12)
    text(d, (xb - 0.5, yt / 2 + 0.55), "$v_\\pi$")
    text(d, (xb - 0.45, gy + 0.5), "−", fontsize=12)
    wire(d, (0, gy), (xl, gy))
    gnd(d, (xb + 0.65, gy))
    save(d, "fr-miller" if miller else "fr-hybrid-pi")


# ---------------------------------------------------------------- 曲线
def rc_bode():
    x = np.logspace(-2, 2, 400)
    HL, HH = 1 / (1 + 1j * x), 1j * x / (1 + 1j * x)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.8, 4.4), sharex=True)
    for a in (a1, a2):
        style(a); a.set_xscale("log")
    a1.plot(x, 20 * np.log10(abs(HL)), color=C1, lw=1.8, label="低通")
    a1.plot(x, 20 * np.log10(abs(HH)), color=C2, lw=1.8, label="高通")
    a1.plot([1e-2, 1, 1e2], [0, 0, -40], color=C1, lw=0.9, ls="--")
    a1.plot([1e-2, 1, 1e2], [-40, 0, 0], color=C2, lw=0.9, ls="--")
    a1.plot([1], [-3], "o", color=INK, ms=4)
    a1.annotate("$f=f_c$：$-3$ dB", xy=(1, -3), xytext=(1.4, 6), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    a1.text(8, -27, "$-20$ dB/十倍频", color=C1, fontsize=9)
    a1.text(0.012, -27, "$+20$ dB/十倍频", color=C2, fontsize=9)
    a1.set_ylim(-42, 11); a1.set_yticks([0, -20, -40])
    a1.set_ylabel("$20\\lg|H|$ / dB", color=INK)
    a1.legend(frameon=False, fontsize=9, loc="lower center")
    a2.plot(x, np.degrees(np.angle(HL)), color=C1, lw=1.8)
    a2.plot(x, np.degrees(np.angle(HH)), color=C2, lw=1.8)
    a2.plot([1e-2, 0.1, 10, 1e2], [0, 0, -90, -90], color=C1, lw=0.9, ls="--")
    a2.plot([1e-2, 0.1, 10, 1e2], [90, 90, 0, 0], color=C2, lw=0.9, ls="--")
    a2.set_yticks([-90, -45, 0, 45, 90]); a2.set_ylabel("$\\varphi$ / (°)", color=INK)
    a2.set_xticks([0.01, 0.1, 1, 10, 100], ["$0.01f_c$", "$0.1f_c$", "$f_c$", "$10f_c$", "$100f_c$"])
    a2.set_xlabel("$f$（对数刻度）", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "fr-rc-bode")


def amp_bode():
    f = np.logspace(0, 8, 600)
    A = -100 / ((1 - 1j * 20 / f) * (1 + 1j * f / 1e6))
    ph = -180 + np.degrees(np.arctan(20 / f)) - np.degrees(np.arctan(f / 1e6))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.8, 4.2), sharex=True)
    for a in (a1, a2):
        style(a); a.set_xscale("log")
    a1.plot(f, 20 * np.log10(abs(A)), color=C1, lw=1.8)
    a1.plot([1, 20, 1e6, 1e8], [40 - 20 * np.log10(20), 40, 40, 0], color=MUTED, lw=0.9, ls="--")
    a1.axhline(37, color=C3, lw=0.8, ls=":")
    for fc, lab in ((20, "$f_L$"), (1e6, "$f_H$")):
        a1.plot([fc], [37], "o", color=C2, ms=4)
        a1.text(fc, 30, lab, color=C2, ha="center", fontsize=10)
    a1.annotate("", xy=(20, 44), xytext=(1e6, 44), arrowprops=dict(arrowstyle="<->", color=C3))
    a1.text(4.5e3, 46, "通频带 $BW=f_H-f_L\\approx f_H$", color=C3, ha="center", fontsize=9)
    a1.text(1.2, 41, "中频 40 dB", color=INK, fontsize=9)
    a1.set_ylim(0, 52); a1.set_yticks([0, 20, 40])
    a1.text(2e7, 34.2, "37 dB", color=C3, fontsize=8, ha="center")
    a1.set_ylabel("$20\\lg|A_v|$ / dB", color=INK)
    a2.plot(f, ph, color=C1, lw=1.8)
    a2.set_yticks([-270, -225, -180, -135, -90])
    a2.set_ylabel("$\\varphi$ / (°)", color=INK)
    a2.set_xticks([1, 1e2, 1e4, 1e6, 1e8], ["1", "100", "10k", "1M", "100M"])
    a2.set_xlabel("$f$ / Hz", color=INK, loc="right")
    fig.tight_layout()
    save_fig(fig, "fr-amp-bode")


def multistage():
    x = np.logspace(-1.5, 1, 400)
    fig, ax = axes(5.4, 2.8)
    ax.set_xscale("log")
    ax.grid(True, color=GRID, lw=0.6)
    for n, col in ((1, C1), (2, C2), (3, C3)):
        k = np.sqrt(2 ** (1 / n) - 1)
        ax.plot(x, -10 * n * np.log10(1 + x ** 2), color=col, lw=1.7, label=f"{n} 级：$f_H={k:.2f}f_{{H1}}$")
        ax.plot([k], [-3], "o", color=col, ms=4)
    ax.axhline(-3, color=MUTED, lw=0.8, ls="--")
    ax.set_ylim(-12, 1); ax.set_yticks([0, -3, -6, -9, -12])
    ax.set_xticks([0.1, 0.3, 1, 3, 10], ["0.1", "0.3", "1", "3", "10"])
    ax.set_xlabel("$f/f_{H1}$", color=INK, loc="right")
    ax.set_ylabel("相对中频 / dB", color=INK)
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    save_fig(fig, "fr-multistage")


def step():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.6))
    for a in (a1, a2):
        style(a); a.grid(False)
    t = np.linspace(0, 5, 400)
    v = 1 - np.exp(-t)
    a1.plot(t, v, color=C1, lw=1.8)
    t10, t90 = np.log(10 / 9), np.log(10)
    for tt, vv, lab in ((t10, 0.1, "$0.1V_\\infty$"), (t90, 0.9, "$0.9V_\\infty$"), (1, 1 - np.exp(-1), "$0.632V_\\infty$")):
        a1.plot([0, tt], [vv, vv], ls="--", color=MUTED, lw=0.8)
        a1.plot([tt, tt], [0, vv], ls="--", color=MUTED, lw=0.8)
    a1.annotate("", xy=(t10, 0.05), xytext=(t90, 0.05), arrowprops=dict(arrowstyle="<->", color=C2))
    a1.text((t10 + t90) / 2, 0.12, "$t_r=2.2\\tau$", color=C2, ha="center", fontsize=9)
    a1.set_yticks([0, 0.1, 0.632, 0.9, 1], ["0", "0.1", "0.632", "0.9", "1"])
    a1.set_xticks([0, 1, t90, 4], ["0", "$\\tau$", "$2.3\\tau$", "$4\\tau$"])
    a1.set_title("高频段决定上升时间（$f_H$）", fontsize=10, color=INK)
    a1.set_ylabel("$v_o/V_\\infty$", color=INK)
    tp = 1.0
    tt = np.linspace(-0.2, 1.6, 600)
    tauL = 4.0
    vin = np.where((tt >= 0) & (tt < tp), 1.0, 0.0)
    vo = np.where(tt < 0, 0, np.where(tt < tp, np.exp(-tt / tauL), (np.exp(-tp / tauL) - 1) * np.exp(-(tt - tp) / tauL)))
    a2.plot(tt, vin, color=GRID, lw=1.4, ls="--", label="输入")
    a2.plot(tt, vo, color=C1, lw=1.8, label="输出")
    a2.annotate("", xy=(tp + 0.05, 1.0), xytext=(tp + 0.05, np.exp(-tp / tauL)),
                arrowprops=dict(arrowstyle="<->", color=C2))
    a2.text(tp + 0.1, 0.88, "平顶降落 $\\delta$", color=C2, fontsize=9)
    a2.set_xticks([0, tp], ["0", "$t_p$"]); a2.set_yticks([0, 1])
    a2.set_title("低频段决定平顶降落（$f_L$）", fontsize=10, color=INK)
    a2.legend(frameon=False, fontsize=8, loc="center right")
    fig.tight_layout()
    save_fig(fig, "fr-step")


if __name__ == "__main__":
    rc_circuits()
    hybrid_pi()
    hybrid_pi(miller=True)
    rc_bode()
    amp_bode()
    multistage()
    step()
