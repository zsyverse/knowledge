"""习题·电阻电路的等效变换 解析插图（images/ex/sol/e-*）。数值见 verify_equiv.py。"""
from solcommon import (elm, new_drawing, ssave, dot, text, note, cur, arrow, vsrc, isrc, wire,
                       OHM, C1, C2, MUTED)


def term(d, xy, name, dx=-0.45, dy=0.0):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1] + dy), f"${name}$")


def val(d, xy, s, **kw):
    """计算结果（蓝色）。"""
    text(d, xy, s, color=C1, **kw)


# ------------------------------------------------------------------ 题2 被短接的电阻
def e_series_s1():
    d = new_drawing()
    term(d, (0, 5), "a"); term(d, (0, 0), "b")
    d.add(elm.Resistor().endpoints((0, 5), (4, 5)).label(f"$4{OHM}$"))
    d.add(elm.Resistor().endpoints((4, 5), (7.5, 5)).label(f"$2{OHM}$"))
    wire(d, (7.5, 5), (10.5, 5))
    d.add(elm.Resistor().endpoints((4, 5), (4, 0)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7.5, 5), (7.5, 0)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((10.5, 5), (10.5, 0)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (10.5, 0)).color(C2).linewidth(2.4))
    for p in ((4, 5), (7.5, 5), (4, 0), (7.5, 0), (10.5, 5), (10.5, 0)):
        dot(d, p)
    text(d, (4, 5.55), "$c$"); text(d, (7.5, 5.55), "$d$")
    text(d, (5.75, -0.55), "整条下边线都是节点 $b$（$5\\,\\Omega$ 被短接，已删去）", color=C2, fontsize=12)
    val(d, (9.0, 5.55), "$3\\parallel6=2\\,\\Omega$")
    ssave(d, "e-series-s1")


# ------------------------------------------------------------------ 题4 Y–Δ
def e_ydelta_y():
    d = new_drawing()
    term(d, (-1.6, 2.5), "a")
    cur(d, (-1.6, 2.5), (-0.6, 2.5), "$2\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints((-0.6, 2.5), (2.5, 2.5)).label(f"$2{OHM}$"))
    dot(d, (2.5, 2.5)); text(d, (2.0, 3.0), "$o$")
    val(d, (1.5, 1.95), "$V_o=8\\,\\mathrm{V}$")
    wire(d, (2.5, 2.5), (2.5, 5)); wire(d, (2.5, 2.5), (2.5, 0))
    d.add(elm.Resistor().endpoints((2.5, 5), (5.8, 5)).label(f"$2{OHM}$"))
    d.add(elm.Resistor().endpoints((5.8, 5), (9, 5)).label(f"$4{OHM}$"))
    d.add(elm.Resistor().endpoints((2.5, 0), (5.8, 0)).label(f"$2{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((5.8, 0), (9, 0)).label(f"$10{OHM}$", loc="bot"))
    dot(d, (5.8, 5)); dot(d, (5.8, 0))
    text(d, (5.8, 5.6), "$c$"); text(d, (5.8, -0.65), "$d$")
    val(d, (5.8, 4.3), "$V_c=\\frac{16}{3}\\,\\mathrm{V}$")
    val(d, (5.8, 0.7), "$V_d=\\frac{20}{3}\\,\\mathrm{V}$")
    arrow(d, (3.2, 5.9), (4.6, 5.9), "$\\frac{4}{3}\\,\\mathrm{A}$", loc="top")
    arrow(d, (3.2, -0.9), (4.6, -0.9), "$\\frac{2}{3}\\,\\mathrm{A}$", loc="bot")
    wire(d, (9, 0), (9, 5)); wire(d, (9, 2.5), (10.6, 2.5))
    dot(d, (9, 2.5))
    term(d, (10.6, 2.5), "b", dx=0.45)
    note(d, (10.6, 1.8), "（参考点）")
    ssave(d, "e-ydelta-y")


# ------------------------------------------------------------------ 题5 对称
def e_sym_half():
    d = new_drawing()
    M, B = (5.5, 5), (5.5, 0)
    d.add(elm.Resistor().endpoints((2, 5), M).label(f"$1{OHM}$"))
    d.add(elm.Resistor().endpoints(M, (9, 5)).label(f"$1{OHM}$"))
    d.add(elm.Resistor().endpoints((2, 5), (2, 0)).label(f"$3\\parallel6=2{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((9, 5), (9, 0)).label(f"$3\\parallel6=2{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((2, 0), B).label(f"$1{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints(B, (9, 0)).label(f"$1{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints(M, (5.5, 2.6)).label(f"$1{OHM}$", loc="bot"))
    vsrc(d, B, (5.5, 2.6), "$6\\,\\mathrm{V}$", loc="bot")
    arrow(d, (4.8, 3.3), (4.8, 4.5), "$I=2\\,\\mathrm{A}$", loc="top")
    arrow(d, (4.6, 6.1), (3.0, 6.1), "$1\\,\\mathrm{A}$", loc="top")
    arrow(d, (6.4, 6.1), (8.0, 6.1), "$1\\,\\mathrm{A}$", loc="top")
    for p in ((2, 5), M, (9, 5), (2, 0), B, (9, 0)):
        dot(d, p)
    note(d, (5.5, -1.4), "$7\\,\\Omega$ 两端等电位、无电流，已断开")
    ssave(d, "e-sym-half")


# ------------------------------------------------------------------ 题6 Δ→Y
def e_bridge_is_y():
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$5\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4), (2.5, 4)); wire(d, (0, 0), (12.5, 0))
    term(d, (1.2, 4), "a", dx=0, dy=0.45); term(d, (1.2, 0), "b", dx=0, dy=-0.45)
    dot(d, (2.5, 4)); text(d, (2.5, 4.55), "$l$")
    d.add(elm.Resistor().endpoints((2.5, 4), (5, 4)).label(f"$1.2{OHM}$"))
    dot(d, (5, 4)); text(d, (4.6, 4.55), "$o$")
    wire(d, (5, 4), (5, 5.8)); wire(d, (5, 4), (5, 2.2))
    d.add(elm.Resistor().endpoints((5, 5.8), (7.6, 5.8)).label(f"$2{OHM}$"))
    d.add(elm.Resistor().endpoints((7.6, 5.8), (10.5, 5.8)).label(f"$10{OHM}$"))
    d.add(elm.Resistor().endpoints((5, 2.2), (7.6, 2.2)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7.6, 2.2), (10.5, 2.2)).label(f"$5{OHM}$", loc="bot"))
    dot(d, (7.6, 5.8)); dot(d, (7.6, 2.2))
    text(d, (7.6, 6.4), "$p$"); text(d, (7.6, 1.55), "$q$")
    val(d, (7.6, 5.15), "$V_p=20\\,\\mathrm{V}$")
    val(d, (7.6, 2.85), "$V_q=15\\,\\mathrm{V}$")
    arrow(d, (8.4, 6.95), (9.7, 6.95), "$2\\,\\mathrm{A}$", loc="top")
    arrow(d, (8.4, 1.25), (9.7, 1.25), "$3\\,\\mathrm{A}$", loc="bot")
    wire(d, (10.5, 2.2), (10.5, 5.8))
    dot(d, (10.5, 4)); text(d, (10.9, 4.45), "$r$")
    wire(d, (10.5, 4), (12.5, 4))
    d.add(elm.Resistor().endpoints((12.5, 4), (12.5, 0)).label(f"$24{OHM}$", loc="bot"))
    note(d, (7.6, -0.6), "电位以 $r$ 为参考；$U=V_p-V_q=5\\,\\mathrm{V}$")
    ssave(d, "e-bridge-is-y")


# ------------------------------------------------------------------ 题7 电源等效变换
def _out(d, x, y=5):
    d.add(elm.Resistor().endpoints((x, y), (x + 3, y)).label(f"$2{OHM}$"))
    wire(d, (x + 3, y), (x + 3.8, y))
    term(d, (x + 3.8, y), "a", dx=0.45); term(d, (x + 3.8, 0), "b", dx=0.45)


def e_source_s1():
    d = new_drawing()
    isrc(d, (0, 0), (0, 5), "$\\frac{12}{6}=2\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints((2.2, 5), (2.2, 0)).label(f"$6{OHM}$", loc="bot"))
    isrc(d, (4.4, 0), (4.4, 5), "$3\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((6.6, 5), (6.6, 0)).label(f"$3{OHM}$", loc="bot"))
    wire(d, (0, 5), (6.6, 5)); wire(d, (0, 0), (10.4, 0))
    for x in (2.2, 4.4, 6.6):
        dot(d, (x, 5)); dot(d, (x, 0))
    text(d, (6.6, 5.55), "$t$")
    _out(d, 6.6)
    ssave(d, "e-source-s1")


def e_source_s23():
    """左：5 A 并 2 Ω 再串 2 Ω；右：化为 10 V 串 4 Ω，接 6 Ω 负载。"""
    d = new_drawing()
    isrc(d, (0, 0), (0, 5), "$2+3=5\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints((2.6, 5), (2.6, 0)).label(f"$6\\parallel3=2{OHM}$", loc="bot"))
    wire(d, (0, 5), (2.6, 5)); wire(d, (0, 0), (6.4, 0))
    dot(d, (2.6, 5)); dot(d, (2.6, 0))
    text(d, (2.6, 5.55), "$t$")
    _out(d, 2.6)
    text(d, (8.6, 2.5), "$\\Longrightarrow$", fontsize=22)
    x = 11.4
    vsrc(d, (x, 0), (x, 5), "$10\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((x, 5), (x + 3.2, 5)).label(f"$2+2=4{OHM}$"))
    wire(d, (x + 3.2, 5), (x + 3.8, 5))
    term(d, (x + 3.8, 5), "a", dx=0, dy=0.5); term(d, (x + 3.8, 0), "b", dx=0, dy=-0.5)
    cur(d, (x + 3.8, 5), (x + 6.2, 5), "$I_L=1\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints((x + 6.2, 5), (x + 6.2, 0)).label(f"$R_L=6{OHM}$", loc="bot"))
    wire(d, (x, 0), (x + 6.2, 0))
    note(d, (x - 0.2, -0.9), "$5\\,\\mathrm{A}\\times2\\,\\Omega=10\\,\\mathrm{V}$")
    ssave(d, "e-source-s23")


if __name__ == "__main__":
    e_series_s1(); e_ydelta_y(); e_sym_half(); e_bridge_is_y()
    e_source_s1(); e_source_s23()
