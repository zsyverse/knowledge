"""习题·互感与理想变压器 插图（前缀 m-）。"""
from excommon import (elm, new_drawing, save, dot, text, cur, arrow, wire, ac_src, pdot, m_arrow, OHM)


def m_eq():
    """L1 同名端在上，L2 同名端在下；i1、i2 均从上端流入，u1、u2 均上正下负。"""
    d = new_drawing()
    dot(d, (0, 4), True); dot(d, (0, 0), True)
    cur(d, (0, 4), (2, 4), "$i_1$")
    wire(d, (0, 0), (2, 0))
    d.add(elm.Gap().endpoints((0, 4), (0, 0)).label(("+", "$u_1$", "−"), loc="top"))
    d.add(elm.Inductor2(loops=4).endpoints((2, 4), (2, 0)).label("$L_1$", loc="top"))
    dot(d, (7, 4), True); dot(d, (7, 0), True)
    cur(d, (7, 4), (5, 4), "$i_2$")
    wire(d, (7, 0), (5, 0))
    d.add(elm.Gap().endpoints((7, 4), (7, 0)).label(("+", "$u_2$", "−"), loc="bot"))
    d.add(elm.Inductor2(loops=4).endpoints((5, 4), (5, 0)).label("$L_2$", loc="bot"))
    pdot(d, (2.5, 3.0)); pdot(d, (4.5, 1.0))
    m_arrow(d, (2.8, 2.0), (4.2, 2.0))
    save(d, "m-eq")


def m_series():
    """两种串联接法：(a) 1′ 接 2，从 1、2′ 测量；(b) 1′ 接 2′，从 1、2 测量。"""
    d = new_drawing()
    for x0, tag, mode in ((0, "(a)", "a"), (9, "(b)", "b")):
        xa, xb = x0 + 1.5, x0 + 4.5
        d.add(elm.Inductor2(loops=4).endpoints((xa, 4), (xa, 0)).label("A", loc="bot"))
        d.add(elm.Inductor2(loops=4).endpoints((xb, 4), (xb, 0)).label("B", loc="bot"))
        text(d, (xa - 0.45, 3.55), "$1$"); text(d, (xa - 0.45, 0.45), "$1'$")
        text(d, (xb + 0.45, 3.55), "$2$"); text(d, (xb + 0.45, 0.45), "$2'$")
        wire(d, (x0, 4.6), (xa, 4.6), (xa, 4)); dot(d, (x0, 4.6), True)
        if mode == "a":
            wire(d, (xa, 0), (xa, -0.6), (x0 + 3, -0.6), (x0 + 3, 4.6), (xb, 4.6), (xb, 4))
            wire(d, (xb, 0), (xb, -0.6), (x0 + 6, -0.6)); dot(d, (x0 + 6, -0.6), True)
        else:
            wire(d, (xa, 0), (xa, -0.6), (xb, -0.6), (xb, 0))
            wire(d, (xb, 4), (xb, 4.6), (x0 + 6, 4.6)); dot(d, (x0 + 6, 4.6), True)
        text(d, (x0 + 3, -1.6), tag, fontsize=13)
    save(d, "m-series")


def m_tdec():
    """L1：a→n，同名端在 a 端；L2：n→地，同名端在 n 端（上）；R 与 L2 并联。"""
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U$")
    cur(d, (0, 4), (1.2, 4), "$\\dot I$")
    dot(d, (1.2, 4)); text(d, (1.2, 4.5), "$a$")
    d.add(elm.Inductor2(loops=3).endpoints((1.2, 4), (4.5, 4)).label(f"$j4{OHM}$"))
    dot(d, (4.5, 4)); text(d, (4.5, 4.5), "$n$")
    d.add(elm.Inductor2(loops=3).endpoints((4.5, 4), (4.5, 0)).label(f"$j8{OHM}$", loc="bot"))
    pdot(d, (1.75, 3.55)); pdot(d, (5.0, 3.35))
    m_arrow(d, (2.4, 3.2), (3.9, 2.0), "$j2\\,\\Omega$")
    wire(d, (4.5, 4), (7.5, 4))
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$6{OHM}$", loc="bot"))
    wire(d, (0, 0), (7.5, 0))
    dot(d, (4.5, 0))
    save(d, "m-tdec")


def m_mesh():
    """作业 5-34 改编：L1 同名端在上，L2 同名端在左。"""
    d = new_drawing()
    ac_src(d, (0, 0), (0, 6), "$\\dot U_S$")
    wire(d, (0, 6), (4, 6))
    dot(d, (4, 6))
    d.add(elm.Inductor2(loops=3).endpoints((4, 6), (4, 3)).label(f"$j4{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((4, 3), (4, 0)).label(f"$5{OHM}$", loc="top"))
    arrow(d, (4.7, 2.2), (4.7, 0.9), "$\\dot I_1$")
    d.add(elm.Inductor2(loops=3).endpoints((4, 6), (8.5, 6)).label(f"$j4{OHM}$"))
    pdot(d, (4.5, 5.45)); pdot(d, (4.9, 6.5))
    m_arrow(d, (5.0, 4.3), (6.4, 5.4), "$j2\\,\\Omega$")
    d.add(elm.SourceI().endpoints((8.5, 0), (8.5, 6)).label("$\\dot I_S$", loc="bot"))
    wire(d, (0, 0), (8.5, 0))
    dot(d, (4, 0))
    save(d, "m-mesh")


def m_reflect():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_S$")
    d.add(elm.Resistor().endpoints((0, 4), (3, 4)).label(f"$R_1=10{OHM}$"))
    cur(d, (3, 4), (4.5, 4), "$\\dot I_1$")
    d.add(elm.Inductor2(loops=4).endpoints((4.5, 4), (4.5, 0)).label(f"$j20{OHM}$", loc="top"))
    d.add(elm.Inductor2(loops=4).endpoints((7, 4), (7, 0)).label(f"$j10{OHM}$", loc="bot"))
    pdot(d, (5.0, 3.0)); pdot(d, (6.5, 3.0))
    m_arrow(d, (5.15, 2.0), (6.35, 2.0), "$j10\\,\\Omega$")
    cur(d, (7, 4), (8.5, 4), "$\\dot I_2$")
    wire(d, (8.5, 4), (10, 4))
    d.add(elm.Resistor().endpoints((10, 4), (10, 0)).label(f"$R_L=10{OHM}$", loc="bot"))
    wire(d, (0, 0), (4.5, 0)); wire(d, (7, 0), (10, 0))
    save(d, "m-reflect")


def _xfmr(d, x, dots=("top", "top")):
    d.add(elm.Transformer(t1=4, t2=4).scale(2).at((x, 0)))
    pdot(d, (x + 0.25, 3.0) if dots[0] == "top" else (x + 0.25, 0.2))
    pdot(d, (x + 1.75, 3.0) if dots[1] == "top" else (x + 1.75, 0.2))


def m_match():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 3.2), "$\\dot U_S$")
    d.add(elm.Resistor().endpoints((0, 3.2), (3.5, 3.2)).label(f"$R_S=800{OHM}$"))
    wire(d, (3.5, 3.2), (5, 3.2)); wire(d, (0, 0), (5, 0))
    _xfmr(d, 5)
    text(d, (6, 4.0), "$n:1$")
    wire(d, (7, 3.2), (9, 3.2)); wire(d, (7, 0), (9, 0))
    d.add(elm.Resistor().endpoints((9, 3.2), (9, 0)).label(f"$R_L=8{OHM}$", loc="bot"))
    save(d, "m-match")


def m_trap():
    """n=2，一次同名端在上，二次同名端在下；U2 上正，I2 从负载流入二次上端。"""
    d = new_drawing()
    ac_src(d, (0, 0), (0, 3.2), "$\\dot U_S$")
    d.add(elm.Resistor().endpoints((0, 3.2), (3, 3.2)).label(f"$4{OHM}$"))
    cur(d, (3, 3.2), (5, 3.2), "$\\dot I_1$")
    wire(d, (0, 0), (5, 0))
    _xfmr(d, 5, dots=("top", "bot"))
    text(d, (6, 4.0), "$2:1$")
    cur(d, (9, 3.2), (7, 3.2), "$\\dot I_2$")
    wire(d, (7, 0), (9, 0))
    d.add(elm.Gap().endpoints((7.7, 2.8), (7.7, 0.4)).label(("+", "$\\dot U_2$", "−"), loc="bot"))
    d.add(elm.Resistor().endpoints((9, 3.2), (9, 0)).label(f"$2{OHM}$", loc="bot"))
    save(d, "m-trap")


if __name__ == "__main__":
    m_eq(); m_series(); m_tdec(); m_mesh(); m_reflect(); m_match(); m_trap()
