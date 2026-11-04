"""拓展·均匀传输线 插图（前缀 tl-）。"""
import numpy as np
from xcommon import (elm, new_drawing, save, save_fig, dot, text, wire, axes, plt, C1, C2, C3, MUTED, INK)


def tl_segment():
    d = new_drawing()
    yt, yb = 3.2, 0
    for x in (0, 10.4):
        dot(d, (x, yt), True); dot(d, (x, yb), True)
    d.add(elm.Resistor().endpoints((0, yt), (3.0, yt)).label("$R_0\\,\\mathrm{d}x$"))
    d.add(elm.Inductor2(loops=3).endpoints((3.0, yt), (6.2, yt)).label("$L_0\\,\\mathrm{d}x$"))
    wire(d, (6.2, yt), (10.4, yt)); wire(d, (0, yb), (10.4, yb))
    d.add(elm.Resistor().endpoints((7.2, yt), (7.2, yb)).label("$G_0\\,\\mathrm{d}x$", loc="top"))
    d.add(elm.Capacitor().endpoints((9.4, yt), (9.4, yb)).label("$C_0\\,\\mathrm{d}x$", loc="top"))
    for p in ((7.2, yt), (9.4, yt), (7.2, yb), (9.4, yb)):
        dot(d, p)
    text(d, (-0.45, yt), "$x$", fontsize=13); text(d, (10.95, yt), "$x+\\mathrm{d}x$", fontsize=13)
    text(d, (-0.6, 1.6), "$u$"); text(d, (11.4, 1.6), "$u+\\mathrm{d}u$")
    save(d, "tl-segment")


def tl_standing():
    fig, ax = axes(5.4, 2.9)
    x = np.linspace(0, 1, 500)          # x'/λ，从负载往回量
    for G, col, lab in ((0, C3, "匹配 $Z_L=Z_c$（$\\Gamma=0$）：行波"),
                        (1 / 3, C1, "$Z_L=2Z_c$（$\\Gamma=1/3$）：行驻波"),
                        (1, C2, "开路（$\\Gamma=1$）：驻波")):
        ax.plot(x, np.abs(1 + G * np.exp(-2j * 2 * np.pi * x)), color=col, lw=2, label=lab)
    ax.set_xlim(1, 0)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0\n(负载)", "$\\lambda/4$", "$\\lambda/2$", "$3\\lambda/4$", "$\\lambda$"])
    ax.set_yticks([0, 2 / 3, 1, 4 / 3, 2], ["0", "2/3", "1", "4/3", "2"])
    ax.set_ylim(0, 3.0)
    ax.set_xlabel("到负载的距离 $x'$", color=INK, loc="left")
    ax.set_ylabel("$|\\dot U|/|\\dot U^+|$", color=INK)
    ax.legend(fontsize=9, frameon=False, loc="upper center", ncol=1)
    save_fig(fig, "tl-standing")


if __name__ == "__main__":
    tl_segment(); tl_standing()
