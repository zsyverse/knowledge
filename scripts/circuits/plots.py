"""波形 / 曲线 / 相量图（matplotlib，透明背景）。"""
import numpy as np

from common import plt, save_fig

C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"


def _axes(w=6.0, h=3.4):
    fig, ax = plt.subplots(figsize=(w, h))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=10)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    return fig, ax


def max_power_curve():
    fig, ax = _axes()
    x = np.linspace(0, 6, 400)
    y = 4 * x / (1 + x) ** 2
    ax.plot(x, y, color=C1, lw=2)
    ax.plot([1], [1], "o", color=C1, ms=8, mec="white", mew=1.5)
    ax.annotate("$R_L=R_{eq}$ 时最大\n$P_{\\max}=U_{oc}^2/(4R_{eq})$", (1, 1), (2.2, 0.98),
                color=INK, fontsize=11, arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.set_xlabel("$R_L/R_{eq}$", color=INK)
    ax.set_ylabel("$P_L/P_{\\max}$", color=INK)
    ax.set_xlim(0, 6); ax.set_ylim(0, 1.2)
    save_fig(fig, "max-power-curve")


def first_order_curves():
    fig, ax = _axes()
    t = np.linspace(0, 5, 400)
    ax.plot(t, 1 - np.exp(-t), color=C1, lw=2, label="零状态（充电）$1-e^{-t/\\tau}$")
    ax.plot(t, np.exp(-t), color=C2, lw=2, label="零输入（放电）$e^{-t/\\tau}$")
    for k, v in ((1, 1 - np.exp(-1)), (1, np.exp(-1))):
        ax.plot([k], [v], "o", color=INK, ms=5)
    ax.annotate("$t=\\tau$：63.2%", (1, 1 - np.exp(-1)), (1.35, 0.5), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate("$t=\\tau$：36.8%", (1, np.exp(-1)), (1.6, 0.28), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.axvline(1, color=MUTED, lw=0.8, ls="--")
    ax.set_xticks([0, 1, 2, 3, 4, 5], ["0", "$\\tau$", "$2\\tau$", "$3\\tau$", "$4\\tau$", "$5\\tau$"])
    ax.set_xlabel("$t$", color=INK)
    ax.set_ylabel("归一化响应", color=INK)
    ax.set_xlim(0, 5); ax.set_ylim(0, 1.08)
    ax.legend(frameon=False, fontsize=10, loc="center right")
    save_fig(fig, "first-order-curves")


def second_order_cases():
    """串联 RLC 零输入：L=1 H，C=0.25 F，u_C(0)=1 V，i(0)=0。"""
    fig, ax = _axes()
    t = np.linspace(0, 6, 600)
    # 过阻尼 R=5：s=-1,-4  u=A e^{-t}+B e^{-4t}, A+B=1, -A-4B=0 -> A=4/3,B=-1/3
    u_over = 4 / 3 * np.exp(-t) - 1 / 3 * np.exp(-4 * t)
    # 临界 R=4：s=-2 重根  u=(1+2t)e^{-2t}
    u_crit = (1 + 2 * t) * np.exp(-2 * t)
    # 欠阻尼 R=2：s=-1±j√3  u=e^{-t}(cos√3t + sin√3t/√3)
    wd = np.sqrt(3)
    u_under = np.exp(-t) * (np.cos(wd * t) + np.sin(wd * t) / wd)
    ax.plot(t, u_over, color=C1, lw=2, label="过阻尼 $R=5\\,\\Omega$")
    ax.plot(t, u_crit, color=C3, lw=2, label="临界阻尼 $R=4\\,\\Omega$")
    ax.plot(t, u_under, color=C2, lw=2, label="欠阻尼 $R=2\\,\\Omega$")
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel("$t$ / s", color=INK)
    ax.set_ylabel("$u_C(t)$ / V", color=INK)
    ax.set_xlim(0, 6)
    ax.legend(frameon=False, fontsize=10)
    save_fig(fig, "second-order-cases")


def _phasor(ax, z, color, label, xy_text, start=0j, lw=2):
    ax.annotate("", xy=((z + start).real, (z + start).imag),
                xytext=(start.real, start.imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=16, shrinkA=0, shrinkB=0))
    ax.text(*xy_text, label, color=INK, fontsize=12, ha="center", va="center")


def _phasor_axes(lim):
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1])
    ax.axis("off")
    return fig, ax


def phasor_5_22():
    fig, ax = _phasor_axes(((-0.3, 3.4), (-1.3, 1.3)))
    c = np.cos(np.pi / 3); s = np.sin(np.pi / 3)
    _phasor(ax, complex(c, -s), C1, "$\\dot I_2$", (0.62, -1.0))
    _phasor(ax, complex(c, s), C2, "$\\dot I_3$", (0.62, 1.0))
    _phasor(ax, 1 + 0j, INK, "$\\dot I_1$", (0.86, 0.13), lw=2.4)
    ax.plot([c, 1], [-s, 0], ls="--", color=C2, lw=1)
    ax.plot([c, 1], [s, 0], ls="--", color=C1, lw=1)
    _phasor(ax, 2 + 0j, "#555555", "", (0, 0), start=1 + 0j, lw=1.4)
    ax.text(2.0, 0.2, "$\\dot U_{ab}$ 方向（参考）", fontsize=11, color=INK, ha="center")
    ax.text(0.2, -0.2, "$60^\\circ$", fontsize=11, color=INK)
    ax.text(0.2, 0.1, "$60^\\circ$", fontsize=11, color=INK)
    save_fig(fig, "phasor-5-22")


def resonance_curve():
    fig, ax = _axes()
    x = np.linspace(0.05, 3, 600)
    for Q, col in ((1, C3), (2, C1), (5, C2)):
        y = 1 / np.sqrt(1 + Q ** 2 * (x - 1 / x) ** 2)
        ax.plot(x, y, color=col, lw=2, label=f"$Q={Q}$")
    ax.axhline(1 / np.sqrt(2), color=MUTED, ls="--", lw=0.8)
    ax.text(2.35, 0.73, "$1/\\sqrt{2}$（通频带边界）", fontsize=10, color=INK)
    ax.set_xlabel("$\\omega/\\omega_0$", color=INK)
    ax.set_ylabel("$I/I_0$", color=INK)
    ax.set_xlim(0, 3); ax.set_ylim(0, 1.08)
    ax.legend(frameon=False, fontsize=10, loc="center right", bbox_to_anchor=(1.0, 0.4))
    save_fig(fig, "resonance-curve")


def power_triangle():
    """以 5-24 为例：P=1000 W，Q 由 866 var 补偿到 458 var。"""
    fig, ax = plt.subplots(figsize=(5.4, 3.6))
    ax.set_aspect("equal"); ax.axis("off")
    P, Q1, Q2 = 1000, 500 * np.sqrt(3), 100 * np.sqrt(21)
    ax.plot([0, P], [0, 0], color=INK, lw=2)
    ax.plot([P, P], [0, Q1], color=C2, lw=2)
    ax.plot([0, P], [0, Q1], color=C2, lw=2)
    ax.plot([0, P], [0, Q2], color=C1, lw=2)
    ax.annotate("", xy=(P + 60, Q2), xytext=(P + 60, Q1),
                arrowprops=dict(arrowstyle="-|>", color=C3, lw=1.6))
    ax.text(P / 2, -60, "$P=1000\\,\\mathrm{W}$（不变）", ha="center", va="top", fontsize=11, color=INK)
    ax.text(P - 30, Q1 + 20, "$Q_1=866\\,\\mathrm{var}$", ha="right", va="bottom", fontsize=11, color=INK)
    ax.text(P + 90, (Q1 + Q2) / 2, "电容提供\n$Q_C=-408\\,\\mathrm{var}$", ha="left", va="center", fontsize=11, color=INK)
    ax.text(P + 90, Q2 * 0.55, "$Q_2=458\\,\\mathrm{var}$", ha="left", va="center", fontsize=11, color=INK)
    ax.text(380, 520, "$S_1=1323\\,\\mathrm{VA}$", fontsize=11, color=C2, rotation=0)
    ax.text(560, 130, "$S_2=1100\\,\\mathrm{VA}$", fontsize=11, color=C1)
    ax.set_xlim(-50, 1500); ax.set_ylim(-150, 1000)
    save_fig(fig, "power-triangle")


def three_phase_phasors():
    fig, ax = _phasor_axes(((-1.25, 1.75), (-1.25, 1.25)))
    A = 1 + 0j
    B = np.exp(-2j * np.pi / 3)
    C = np.exp(2j * np.pi / 3)
    for z, col, lab, off in ((A, C1, "$\\dot U_A$", (0.12, -0.12)), (B, C2, "$\\dot U_B$", (-0.18, -0.08)),
                             (C, C3, "$\\dot U_C$", (-0.18, 0.08))):
        _phasor(ax, z, col, lab, (z.real + off[0], z.imag + off[1]))
    # U_AB = U_A - U_B ：从 B 端点指向 A 端点画（平移后的相量），并画从原点出发的 U_AB
    _phasor(ax, -B, "#999999", "$-\\dot U_B$", (1.0 + 0.25, 0.52), start=A, lw=1.3)
    uab = A - B
    _phasor(ax, uab, INK, "$\\dot U_{AB}$", (uab.real + 0.05, uab.imag + 0.15), lw=2.4)
    ax.text(0.42, 0.07, "$30^\\circ$", fontsize=11, color=INK)
    ax.text(1.05, -0.5, "$|\\dot U_{AB}|=\\sqrt{3}\\,U_p$", fontsize=11, color=INK)
    save_fig(fig, "three-phase-phasors")


def harmonic_synthesis():
    fig, ax = _axes(6.4, 3.4)
    wt = np.linspace(0, 2 * np.pi, 800)
    u0 = 0.5 * np.ones_like(wt)
    u1 = 1.0 * np.sin(wt)
    u3 = 0.35 * np.sin(3 * wt)
    ax.plot(wt, u0, color=C3, lw=1.4, ls="--", label="直流 $U_0$")
    ax.plot(wt, u1, color=C1, lw=1.4, ls="--", label="基波 $\\omega$")
    ax.plot(wt, u3, color=C2, lw=1.4, ls="--", label="三次谐波 $3\\omega$")
    ax.plot(wt, u0 + u1 + u3, color=INK, lw=2.2, label="合成 $u(t)$")
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi], ["0", "$T/4$", "$T/2$", "$3T/4$", "$T$"])
    ax.set_xlabel("$t$", color=INK)
    ax.set_xlim(0, 2 * np.pi)
    ax.legend(frameon=False, fontsize=10, ncol=2, loc="lower left")
    save_fig(fig, "harmonic-synthesis")


if __name__ == "__main__":
    max_power_curve()
    first_order_curves()
    second_order_cases()
    phasor_5_22()
    resonance_curve()
    power_triangle()
    three_phase_phasors()
    harmonic_synthesis()
