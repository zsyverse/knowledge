"""习题·基本概念与基尔霍夫定律 插图。"""
from excommon import elm, new_drawing, save, dot, text, cur, vsrc_h, arrow, vsrc, isrc, wire, OHM


def ex_b_elements():
    """四个元件的参考方向：A、C 关联，B、D 非关联。"""
    d = new_drawing()
    specs = [
        ("A", True, "$u=5\\,\\mathrm{V}$", "$i=-2\\,\\mathrm{A}$", (0, 3.2)),
        ("B", False, "$u=-3\\,\\mathrm{V}$", "$i=4\\,\\mathrm{A}$", (7.5, 3.2)),
        ("C", True, "$u=-6\\,\\mathrm{V}$", "$i=-1.5\\,\\mathrm{A}$", (0, 0)),
        ("D", False, "$u=5.5\\,\\mathrm{V}$", "$i=2\\,\\mathrm{A}$", (7.5, 0)),
    ]
    for name, assoc, us, is_, (x, y) in specs:
        dot(d, (x, y), True)
        dot(d, (x + 5.4, y), True)
        if assoc:
            cur(d, (x, y), (x + 1.2, y), is_)
            d.add(elm.Line().endpoints((x + 4.2, y), (x + 5.4, y)))
        else:
            d.add(elm.Line().endpoints((x, y), (x + 1.2, y)))
            cur(d, (x + 5.4, y), (x + 4.2, y), is_)
        d.add(elm.RBox().endpoints((x + 1.2, y), (x + 4.2, y)).label(name, loc="center"))
        text(d, (x + 0.35, y - 0.55), "$+$")
        text(d, (x + 5.05, y - 0.55), "$-$")
        text(d, (x + 2.7, y - 0.8), us)
    save(d, "b-elements")


def ex_b_kcl():
    """作业 2-4：只给部分支路电流，求其余。"""
    d = new_drawing()
    n3, n4, n1, n2, n5, n6 = (0, 4), (4, 4), (8, 4), (8, 8), (4, 0), (8, 0)
    wire(d, n3, (0, 8), (1.5, 8))
    d.add(elm.Resistor().endpoints((1.5, 8), (5.5, 8)))
    wire(d, (5.5, 8), n2, (11, 8))
    arrow(d, (2.6, 8.7), (4.4, 8.7), "$I_2$", loc="top")
    d.add(elm.Resistor().endpoints(n2, n1))
    arrow(d, (8.7, 5.4), (8.7, 6.8), "$I_1$", loc="bot")
    d.add(elm.Resistor().endpoints((11, 8), (11, 0)))
    arrow(d, (11.7, 4.7), (11.7, 3.3), "$1\\,\\mathrm{A}$", loc="bot")
    wire(d, (11, 0), n6)
    d.add(elm.Resistor().endpoints(n3, n4))
    arrow(d, (2.7, 4.7), (1.3, 4.7), "$1\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints(n4, n1))
    arrow(d, (5.3, 4.7), (6.7, 4.7), "$2\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints(n4, n5))
    arrow(d, (4.7, 2.7), (4.7, 1.3), "$I_5$", loc="bot")
    d.add(elm.Resistor().endpoints((0, 0), n3))
    arrow(d, (-0.7, 1.3), (-0.7, 2.7), "$3\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 0), n5)
    d.add(elm.Resistor().endpoints(n5, n6))
    arrow(d, (5.3, -0.7), (6.7, -0.7), "$I_6$", loc="bot")
    vsrc(d, n1, n6, "$U_S$", loc="bot")
    arrow(d, (7.3, 1.3), (7.3, 2.7), "$I_7$", loc="top")
    for p in (n3, n4, n1, n2, n5, n6):
        dot(d, p)
    text(d, (-0.55, 4.45), "③"); text(d, (4, 4.6), "④"); text(d, (8.55, 4.45), "①")
    text(d, (8, 8.6), "②"); text(d, (4, -0.6), "⑤"); text(d, (8.55, -0.45), "⑥")
    save(d, "b-kcl")


def ex_b_kvl():
    """作业 2-5：同一结构，已知部分元件电压，求其余。"""
    d = new_drawing()
    n3, n4, n1, n2, n5 = (0, 4), (4, 4), (8, 4), (8, 8), (4, 0)
    wire(d, n3, (0, 8), (1.5, 8))
    d.add(elm.RBox().endpoints((1.5, 8), (5.5, 8)).label(("−", "$U_2$", "+"), loc="top"))
    wire(d, (5.5, 8), n2, (11, 8))
    d.add(elm.RBox().endpoints(n2, n1).label(("−", "$2\\,\\mathrm{V}$", "+"), loc="bot"))
    d.add(elm.RBox().endpoints((11, 8), (11, 0)).label(("−", "$8\\,\\mathrm{V}$", "+"), loc="bot"))
    wire(d, (11, 0), (0, 0))
    d.add(elm.RBox().endpoints(n3, n4).label(("+", "$3\\,\\mathrm{V}$", "−"), loc="top"))
    d.add(elm.RBox().endpoints(n4, n1).label(("+", "$U_3$", "−"), loc="top"))
    d.add(elm.RBox().endpoints(n4, n5).label(("+", "$8\\,\\mathrm{V}$", "−"), loc="bot"))
    d.add(elm.RBox().endpoints(n3, (0, 0)).label(("+", "$U_5$", "−"), loc="top"))
    isrc(d, (8, 0), n1, "$I_S$", loc="bot")
    d.add(elm.Gap().endpoints((7.0, 3.6), (7.0, 0.4)).label(("+", "$U_7$", "−"), loc="bot"))
    for p in (n3, n4, n1, n2, n5, (8, 0)):
        dot(d, p)
    text(d, (-0.55, 4.45), "③"); text(d, (4, 4.6), "④"); text(d, (8.55, 4.45), "①")
    text(d, (8, 8.6), "②"); text(d, (4, -0.6), "⑤")
    save(d, "b-kvl")


def ex_b_potential():
    """作业 2-9。"""
    d = new_drawing()
    L, b, a = (0, 4), (5, 4), (5, 7.5)
    wire(d, L, (0, 7.5), (0.5, 7.5))
    d.add(elm.Resistor().endpoints((0.5, 7.5), (4, 7.5)).label(f"$2{OHM}$"))
    wire(d, (4, 7.5), a, (5.5, 7.5))
    d.add(elm.Resistor().endpoints((5.5, 7.5), (9, 7.5)).label(f"$6{OHM}$"))
    wire(d, (9, 7.5), (9, 4))
    dot(d, a); text(d, (5, 8.05), "$a$")
    wire(d, L, (1.6, 4))
    cur(d, (3.0, 4), (1.6, 4), "$I_2$")
    vsrc_h(d, (3.0, 4), (4.6, 4), "$3\\,\\mathrm{V}$")
    wire(d, (4.6, 4), b, (5.6, 4))
    d.add(elm.Resistor().endpoints((5.6, 4), (8.6, 4)).label(f"$5{OHM}$"))
    wire(d, (8.6, 4), (9, 4))
    dot(d, b); text(d, (5.45, 3.55), "$b$")
    d.add(elm.Gap().endpoints((5.4, 7.1), (5.4, 4.4)).label(("+", "$U_{ab}$", "−"), loc="bot", ofst=0.1))
    d.add(elm.Resistor().endpoints(L, (0, 0)).label(f"$2{OHM}$", loc="top"))
    arrow(d, (-0.7, 3.5), (-0.7, 2.3), "$I_1$", loc="top")
    isrc(d, (1.6, 0), (1.6, 4), "$1\\,\\mathrm{A}$", loc="bot")
    vsrc(d, b, (5, 0), "$5\\,\\mathrm{V}$", loc="bot")
    vsrc(d, (9, 0), (9, 4), "$14\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (9, 0))
    for p in (L, (1.6, 4), (1.6, 0), (5, 0), (9, 4)):
        dot(d, p)
    save(d, "b-potential")


def ex_b_vccs():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$10\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$2{OHM}$"))
    cur(d, (3.5, 4), (4.5, 4), "$I$")
    wire(d, (4.5, 4), (8, 4))
    dot(d, (4.5, 4)); text(d, (4.5, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((4.5, 4), (4.5, 0)).label(f"$3{OHM}$", loc="top")
          .label(("+", "$u$", "−"), loc="bot"))
    isrc(d, (8, 0), (8, 4), "$0.5u$", loc="bot", ctrl=True)
    wire(d, (0, 0), (8, 0))
    dot(d, (4.5, 0))
    save(d, "b-vccs")


def ex_b_sources():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 5), "$10\\,\\mathrm{V}$", loc="top")
    wire(d, (0, 5), (8, 5))
    d.add(elm.Resistor().endpoints((4, 5), (4, 0)).label(f"$2{OHM}$", loc="bot"))
    isrc(d, (8, 0), (8, 2.5), "$3\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((8, 2.5), (8, 5)).label(f"$4{OHM}$", loc="bot"))
    dot(d, (8, 2.5)); text(d, (7.5, 2.5), "$m$")
    wire(d, (0, 0), (8, 0))
    dot(d, (4, 5)); dot(d, (4, 0))
    save(d, "b-sources")


def ex_b_lc_dc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$2{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$a$")
    d.add(elm.Capacitor().endpoints((3.5, 4), (3.5, 0)).label("$2\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4), (7.5, 4)).label("$1\\,\\mathrm{H}$"))
    arrow(d, (4.6, 3.35), (6.4, 3.35), "$i_L$", loc="bot")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$4{OHM}$", loc="bot"))
    wire(d, (0, 0), (7.5, 0))
    dot(d, (3.5, 0))
    save(d, "b-lc-dc")


if __name__ == "__main__":
    ex_b_elements()
    ex_b_kcl()
    ex_b_kvl()
    ex_b_potential()
    ex_b_vccs()
    ex_b_sources()
    ex_b_lc_dc()
