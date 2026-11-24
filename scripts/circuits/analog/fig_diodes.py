"""模电·半导体与二极管 插图（前缀 di-）。

二极管用 elm.Diode / elm.Zener，.endpoints(阳极, 阴极)。
"""
import os
from pathlib import Path

import numpy as np
from matplotlib.patches import Rectangle
from acommon import (elm, new_drawing, save, save_fig, dot, text, cur, wire, gnd, vsrc, ac_src,
                     axes, plt, C1, C2, C3, MUTED, INK, GRID)

K = "\\,\\mathrm{k}\\Omega"
VT = 0.026


def fsave(fig, name):
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    save_fig(fig, name)


# ---------------------------------------------------------------- PN 结示意 + 电位分布
def pn():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.2), gridspec_kw=dict(height_ratios=[1.3, 1]), sharex=True)
    a1.add_patch(Rectangle((0, 0), 4, 2, color="#f6d5d5", lw=0))
    a1.add_patch(Rectangle((4, 0), 4, 2, color="#d6e4f5", lw=0))
    a1.add_patch(Rectangle((3, 0), 2, 2, fill=False, ls="--", ec=MUTED, lw=1))
    for y in (0.5, 1.5):
        for x in (3.35, 3.75):
            a1.plot(x, y, "o", ms=13, mfc="white", mec=INK, mew=1)
            a1.text(x, y, "−", ha="center", va="center", fontsize=11, color=INK)
        for x in (4.25, 4.65):
            a1.plot(x, y, "o", ms=13, mfc="white", mec=INK, mew=1)
            a1.text(x, y, "+", ha="center", va="center", fontsize=11, color=INK)
    rng = np.random.default_rng(3)
    a1.plot(rng.uniform(0.2, 2.8, 14), rng.uniform(0.2, 1.8, 14), "o", ms=6, mfc="none", mec=C2, mew=1.4)
    a1.plot(rng.uniform(5.2, 7.8, 14), rng.uniform(0.2, 1.8, 14), "o", ms=5, color=C1)
    a1.text(1.5, 2.25, "P 区：多子为空穴（空心圈）", ha="center", fontsize=10, color=INK)
    a1.text(6.5, 2.25, "N 区：多子为电子（实心点）", ha="center", fontsize=10, color=INK)
    a1.text(4, 2.25, "耗尽层", ha="center", fontsize=10, color=INK)
    a1.text(4, -0.05, "负离子 | 正离子", ha="center", va="top", fontsize=8.5, color=MUTED)
    a1.annotate("", xy=(3.1, -0.55), xytext=(4.9, -0.55), arrowprops=dict(arrowstyle="->", color=C3, lw=1.6))
    a1.text(4, -0.95, "内电场 $E$（N → P）", ha="center", fontsize=10, color=INK)
    a1.set_xlim(-0.2, 8.2); a1.set_ylim(-1.2, 2.6); a1.axis("off")
    x = np.linspace(0, 8, 400)
    phi = np.where(x < 3, 0, np.where(x > 5, 1, np.where(x < 4, 0.5 * (x - 3) ** 2, 1 - 0.5 * (5 - x) ** 2)))
    a2.plot(x, phi, color=C1, lw=2)
    a2.annotate("", xy=(7.2, 1), xytext=(7.2, 0), arrowprops=dict(arrowstyle="<->", color=MUTED))
    a2.text(7.35, 0.5, "$V_{ho}$（内建电位差）", fontsize=10, color=INK, va="center")
    a2.set_ylabel("电位 $\\varphi$", color=INK)
    a2.set_yticks([]); a2.set_xticks([])
    for s in ("top", "right"):
        a2.spines[s].set_visible(False)
    a2.spines["left"].set_color(MUTED); a2.spines["bottom"].set_color(MUTED)
    a2.set_ylim(-0.15, 1.3)
    fig.tight_layout()
    fsave(fig, "di-pn")


# ---------------------------------------------------------------- 伏安特性
def iv():
    fig, ax = axes(6.4, 3.4)
    v = np.linspace(0, 0.78, 300)
    Is = 1e-14
    i = Is * (np.exp(v / VT) - 1) * 1e3      # mA
    ax.plot(v, i, color=C1, lw=2)
    # 反向段：为了看得见，横轴用不同比例（标注说明）
    xr = np.linspace(-1.0, -0.02, 50)
    ax.plot(xr, -0.15 * np.ones_like(xr), color=C1, lw=2)
    xb = np.linspace(-1.16, -1.0, 40)
    ax.plot(xb, -0.15 - 60 * (-1.0 - xb) ** 1.4 * 10, color=C1, lw=2)
    ax.plot([-0.02, 0], [-0.15, 0], color=C1, lw=2)
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlim(-1.25, 0.95); ax.set_ylim(-8, 10)
    ax.set_xticks([-1.0, 0, 0.5, 0.7], ["$-V_{BR}$", "0", "$V_{th}$\n≈0.5", "≈0.7"])
    ax.set_yticks([])
    ax.set_xlabel("$v_D$ / V（反向段未按比例）", color=INK)
    ax.set_ylabel("$i_D$", color=INK)
    ax.annotate("正向导通：\n$i_D\\approx I_Se^{v_D/V_T}$", xy=(0.68, 4), xytext=(0.05, 6.5), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate("死区", xy=(0.3, 0.1), xytext=(0.2, 2.2), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate("反向饱和电流 $-I_S$\n（硅管 nA 级）", xy=(-0.5, -0.15), xytext=(-0.75, 3.2), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate("反向击穿", xy=(-1.08, -4), xytext=(-0.8, -6), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    fsave(fig, "di-iv")


# ---------------------------------------------------------------- 三种模型
def models():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 2.6), sharey=True)
    v = np.linspace(0, 0.8, 200)
    real = 1e-14 * np.exp(v / VT) * 1e3
    specs = [
        ("理想模型：$V_D=0$", [(-0.4, 0), (0, 0), (0, 12)]),
        ("恒压降模型：$V_D=V_{D(on)}\\approx0.7\\,$V", [(-0.4, 0), (0.7, 0), (0.7, 12)]),
        ("折线模型：$V_{th}$ 串 $r_D$", [(-0.4, 0), (0.6, 0), (0.6 + 12 * 0.012, 12)]),
    ]
    for ax, (title, pts) in zip(axs, specs):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.spines["left"].set_color(MUTED); ax.spines["bottom"].set_color(MUTED)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.plot(v, real, color=GRID, lw=2, label="实际特性")
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=C1, lw=2.2)
        ax.set_title(title, fontsize=10.5, color=INK)
        ax.set_xlim(-0.4, 0.95); ax.set_ylim(-1, 12)
        ax.set_xticks([0, 0.7], ["0", "0.7"]); ax.set_xlabel("$v_D$ / V", color=INK, loc="right")
    axs[0].set_ylabel("$i_D$ / mA", color=INK)
    axs[2].annotate("斜率 $1/r_D$", xy=(0.66, 5), xytext=(0.05, 8), fontsize=10, color=INK,
                    arrowprops=dict(arrowstyle="->", color=MUTED))
    axs[2].set_xticks([0, 0.6], ["0", "$V_{th}$"])
    fig.tight_layout()
    fsave(fig, "di-models")


# ---------------------------------------------------------------- 负载线
def loadline():
    fig, ax = axes(5.6, 3.2)
    v = np.linspace(0, 0.76, 300)
    i = 1e-14 * np.exp(v / VT) * 1e3
    ax.plot(v, i, color=C1, lw=2, label="二极管 $i_D=I_Se^{v_D/V_T}$")
    vv = np.linspace(0, 2, 10)
    ax.plot(vv, (2 - vv) / 100 * 1e3, color=C2, lw=2, label="负载线 $i_D=(2-v_D)/100\\,\\Omega$")
    vq, iq = 0.7247, 12.75
    ax.plot([vq], [iq], "o", color=INK)
    ax.annotate(f"$Q$（{vq:.2f} V, {iq:.1f} mA）", xy=(vq, iq), xytext=(0.95, 15), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.set_xlim(0, 2.1); ax.set_ylim(0, 22)
    ax.set_xlabel("$v_D$ / V", color=INK); ax.set_ylabel("$i_D$ / mA", color=INK)
    ax.legend(loc="upper right", fontsize=9, frameon=False)
    fsave(fig, "di-loadline")


# ---------------------------------------------------------------- 两个二极管（优先导通）
def and_gate():
    d = new_drawing()
    # 输出节点 O 在 (4, 3)；R 接 +10 V
    O = (4.0, 3.0)
    d.add(elm.Resistor().endpoints((4.0, 6.0), O).label(f"$R=2{K}$", loc="bot"))
    dot(d, (4.0, 6.0), True); text(d, (4.0, 6.45), "$+10\\,\\mathrm{V}$")
    # D1：阳极在 O 侧，阴极接 V1
    wire(d, O, (2.0, 3.0))
    d.add(elm.Diode().endpoints((2.0, 3.0), (2.0, 0.6)).label("$D_1$", loc="bot"))
    vsrc(d, (2.0, -1.8), (2.0, 0.6), "$V_1$", loc="bot")
    gnd(d, (2.0, -1.8))
    wire(d, O, (6.0, 3.0))
    d.add(elm.Diode().endpoints((6.0, 3.0), (6.0, 0.6)).label("$D_2$", loc="bot"))
    vsrc(d, (6.0, -1.8), (6.0, 0.6), "$V_2$", loc="bot")
    gnd(d, (6.0, -1.8))
    dot(d, O)
    wire(d, O, (4.0, 1.6)); dot(d, (4.0, 1.6), True); text(d, (4.0, 1.1), "$V_O$")
    save(d, "di-and")


# ---------------------------------------------------------------- 限幅电路
def clip():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 3), "$v_i$", loc="bot")
    d.add(elm.Resistor().endpoints((0, 3), (3, 3)).label(f"$R=1{K}$"))
    dot(d, (3, 3))
    d.add(elm.Diode().endpoints((3, 3), (3, 1.5)).label("$D$", loc="bot"))
    vsrc(d, (3, 0), (3, 1.5), "$V_{REF}=2\\,\\mathrm{V}$", loc="bot")
    wire(d, (3, 3), (6.0, 3)); dot(d, (6.0, 3), True)
    wire(d, (0, 0), (6.0, 0)); dot(d, (6.0, 0), True); dot(d, (3, 0))
    text(d, (6.0, 2.6), "+"); text(d, (6.0, 1.5), "$v_o$"); text(d, (6.0, 0.4), "−")
    save(d, "di-clip")


def clip_wave():
    fig, ax = axes(6.0, 2.6)
    th = np.linspace(0, 4 * np.pi, 800)
    vi = 5 * np.sin(th)
    vo = np.minimum(vi, 2.7)
    ax.plot(th / (2 * np.pi), vi, color=GRID, lw=1.6, ls="--", label="$v_i=5\\sin\\omega t$")
    ax.plot(th / (2 * np.pi), vo, color=C1, lw=2, label="$v_o$")
    ax.axhline(2.7, color=MUTED, lw=0.8, ls=":")
    ax.set_yticks([-5, 0, 2.7, 5])
    ax.set_xticks([0, 0.5, 1, 1.5, 2], ["0", "$T/2$", "$T$", "$3T/2$", "$2T$"])
    ax.set_ylabel("V", color=INK); ax.set_ylim(-6, 7.5)
    ax.legend(loc="upper center", ncol=2, fontsize=9, frameon=False)
    fsave(fig, "di-clip-wave")


# ---------------------------------------------------------------- 稳压管稳压电路
def zener():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3), "$V_I$", loc="bot")
    d.add(elm.Resistor().endpoints((0, 3), (3, 3)).label("$R$", loc="bot"))
    dot(d, (3, 3)); dot(d, (3, 0))
    d.add(elm.Zener().endpoints((3, 0), (3, 3)).label("$D_Z$", loc="bot"))
    wire(d, (3, 3), (5.5, 3))
    d.add(elm.Resistor().endpoints((5.5, 3), (5.5, 0)).label("$R_L$", loc="bot"))
    wire(d, (0, 0), (5.5, 0))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((1.0, 3.55), (2.0, 3.55)).label("$I_R$", loc="top"))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((2.3, 2.3), (2.3, 1.3)).label("$I_Z$", loc="top"))
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((4.0, 3.55), (5.0, 3.55)).label("$I_L$", loc="top"))
    text(d, (7.0, 2.6), "+"); text(d, (7.0, 1.5), "$V_O$"); text(d, (7.0, 0.4), "−")
    save(d, "di-zener")


if __name__ == "__main__":
    pn()
    iv()
    models()
    loadline()
    and_gate()
    clip()
    clip_wave()
    zener()
