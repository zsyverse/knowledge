"""习题·电路的一般分析方法 插图（前缀 a-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, vsrc_h, arrow, vsrc, isrc, wire, OHM


def a_branch():
    """作业 4-12。"""
    d = new_drawing()
    vsrc(d, (0, 0), (0, 2.6), "$U_{S1}=10\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 2.6), (0, 5)).label(f"$R_1=10{OHM}$", loc="top"))
    cur(d, (0, 5), (4, 5), "$I_1$")
    dot(d, (4, 5)); dot(d, (4, 0))
    isrc(d, (4, 5), (4, 0), "$I_{S2}=3\\,\\mathrm{A}$", loc="bot")
    cur(d, (8, 5), (4, 5), "$I_3$")
    vsrc(d, (8, 5), (8, 2.6), "$U_{S3}=20\\,\\mathrm{V}$", loc="bot")
    d.add(elm.Resistor().endpoints((8, 2.6), (8, 0)).label(f"$R_3=20{OHM}$", loc="bot"))
    wire(d, (0, 0), (8, 0))
    save(d, "a-branch")


def a_supermesh():
    d = new_drawing()
    v = vsrc(d, (0, 0), (0, 4), "$28\\,\\mathrm{V}$", loc="top")
    r1 = d.add(elm.Resistor().endpoints((0, 4), (4.5, 4)).label(f"$4{OHM}$"))
    s = isrc(d, (4.5, 0), (4.5, 4), "$2\\,\\mathrm{A}$", loc="top")
    r2 = d.add(elm.Resistor().endpoints((4.5, 4), (9, 4)).label(f"$2{OHM}$"))
    r3 = d.add(elm.Resistor().endpoints((9, 4), (9, 0)).label(f"$6{OHM}$", loc="bot"))
    g1 = d.add(elm.Line().endpoints((4.5, 0), (0, 0)))
    g2 = d.add(elm.Line().endpoints((9, 0), (4.5, 0)))
    dot(d, (4.5, 4)); dot(d, (4.5, 0))
    text(d, (5.15, 3.2), "$+$"); text(d, (5.3, 2.0), "$U$"); text(d, (5.15, 0.8), "$-$")
    d.add(elm.LoopCurrent([r1, s, g1, v], pad=1.1).label("$I_1$"))
    d.add(elm.LoopCurrent([r2, r3, g2, s], pad=1.1).label("$I_2$"))
    save(d, "a-supermesh")


def a_node():
    d = new_drawing()
    isrc(d, (0, 0), (0, 2.5), "$2\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 2.5), (0, 5)).label(f"$5{OHM}$", loc="top"))
    wire(d, (0, 5), (3, 5))
    dot(d, (3, 5)); text(d, (3, 5.55), "①")
    d.add(elm.Resistor().endpoints((3, 5), (3, 0)).label(f"$2{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((3, 5), (7, 5)).label(f"$4{OHM}$"))
    dot(d, (7, 5)); text(d, (7, 5.55), "②")
    d.add(elm.Resistor().endpoints((7, 5), (7, 0)).label(f"$4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7, 5), (10.5, 5)).label(f"$4{OHM}$"))
    vsrc(d, (10.5, 0), (10.5, 5), "$24\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (10.5, 0))
    dot(d, (3, 0)); dot(d, (7, 0))
    d.add(elm.Ground().at((5, 0)))
    save(d, "a-node")


def a_supernode():
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$6\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4), (2.5, 4))
    dot(d, (2.5, 4)); text(d, (2.5, 4.55), "$a$")
    d.add(elm.Resistor().endpoints((2.5, 4), (2.5, 0)).label(f"$4{OHM}$", loc="bot"))
    wire(d, (2.5, 4), (3.5, 4))
    e = elm.Source().endpoints((3.5, 4), (6, 4))
    e.label("$8\\,\\mathrm{V}$", loc="top")
    e.label(("−", "", "+"), loc="bot", ofst=0.15)
    d.add(e)
    wire(d, (6, 4), (7, 4))
    dot(d, (7, 4)); text(d, (7, 4.55), "$b$")
    d.add(elm.Resistor().endpoints((7, 4), (7, 0)).label(f"$4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7, 4), (10.5, 4)).label(f"$2{OHM}$"))
    text(d, (10.5, 4.55), "$c$")
    vsrc(d, (10.5, 0), (10.5, 4), "$24\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (10.5, 0))
    dot(d, (2.5, 0)); dot(d, (7, 0))
    d.add(elm.Ground().at((5, 0)))
    save(d, "a-supernode")


def a_vccs():
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$3\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4), (2.5, 4))
    dot(d, (2.5, 4)); text(d, (2.5, 4.55), "①")
    d.add(elm.Resistor().endpoints((2.5, 4), (2.5, 0)).label(f"$4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((2.5, 4), (6.5, 4)).label(f"$2{OHM}$")
          .label(("+", "$u_x$", "−"), loc="bot"))
    dot(d, (6.5, 4)); text(d, (6.5, 4.55), "②")
    d.add(elm.Resistor().endpoints((6.5, 4), (6.5, 0)).label(f"$2{OHM}$", loc="bot"))
    wire(d, (6.5, 4), (9.5, 4))
    isrc(d, (9.5, 0), (9.5, 4), "$gu_x$", loc="bot", ctrl=True)
    wire(d, (0, 0), (9.5, 0))
    dot(d, (2.5, 0)); dot(d, (6.5, 0))
    d.add(elm.Ground().at((4.5, 0)))
    save(d, "a-vccs")


def a_diode():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$6\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (2.8, 4)).label("$1\\,\\mathrm{k}\\Omega$"))
    d.add(elm.Diode().endpoints((2.8, 4), (5, 4)))
    text(d, (3.9, 3.35), "$D_1$")
    arrow(d, (3.3, 4.6), (4.5, 4.6))
    text(d, (3.9, 5.15), "$I_{D1}$")
    dot(d, (5, 4)); text(d, (5.0, 4.6), "$o$")
    d.add(elm.Diode().endpoints((7.2, 4), (5, 4)))
    text(d, (6.1, 3.35), "$D_2$")
    arrow(d, (6.7, 4.6), (5.5, 4.6))
    text(d, (6.1, 5.15), "$I_{D2}$")
    d.add(elm.Resistor().endpoints((10, 4), (7.2, 4)).label("$1\\,\\mathrm{k}\\Omega$"))
    vsrc(d, (10, 0), (10, 4), "$U_2$", loc="bot")
    d.add(elm.Resistor().endpoints((5, 4), (5, 0)).label("$2\\,\\mathrm{k}\\Omega$", loc="bot")
          .label(("+", "$U_o$", "−"), loc="top"))
    wire(d, (0, 0), (10, 0))
    dot(d, (5, 0))
    d.add(elm.Ground().at((5, 0)))
    save(d, "a-diode")


def a_tree():
    """作业 4-17。"""
    d = new_drawing()
    yt, ym, yb = 6, 2.5, 0
    wire(d, (0, yb), (0, yt))
    d.add(elm.Resistor().endpoints((0, yt), (4, yt)).label("$R_4$"))
    d.add(elm.Resistor().endpoints((4, yt), (7.5, yt)).label("$R_6$"))
    arrow(d, (7.6, yt + 0.55), (8.8, yt + 0.55), "$I_6$", loc="top")
    d.add(elm.Resistor().endpoints((8.5, yt), (12, yt)).label("$R_5$"))
    wire(d, (7.5, yt), (8.5, yt))
    d.add(elm.Resistor().endpoints((0, ym), (4, ym)).label("$R_1$", loc="bot"))
    d.add(elm.Resistor().endpoints((4, ym), (8.5, ym)).label("$R_3$", loc="bot"))
    d.add(elm.Resistor().endpoints((8.5, ym), (12, ym)).label("$R_2$", loc="bot"))
    isrc(d, (4, ym), (4, yt), "$I_{S4}$", loc="top")
    isrc(d, (8.5, ym), (8.5, yt), "$I_{S5}$", loc="top")
    wire(d, (12, yt), (12, ym))
    cur(d, (12, yb), (12, ym), "$I_7$", loc="bot")
    d.add(elm.Resistor().endpoints((0, yb), (12, yb)).label("$R_7$", loc="bot"))
    for p in ((0, ym), (4, yt), (8.5, yt), (4, ym), (8.5, ym), (12, ym)):
        dot(d, p)
    save(d, "a-tree")


if __name__ == "__main__":
    a_branch()
    a_supermesh()
    a_node()
    a_supernode()
    a_vccs()
    a_diode()
    a_tree()
