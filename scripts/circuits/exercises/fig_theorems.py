"""习题·电路定理 插图（前缀 t-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, vsrc_h, arrow, vsrc, isrc, wire, OHM


def box(d, x0, y0, x1, y1, label):
    wire(d, (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
    text(d, ((x0 + x1) / 2, (y0 + y1) / 2), label, fontsize=18)


def t_super():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$6{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$3{OHM}$", loc="top"))
    arrow(d, (4.2, 2.8), (4.2, 1.4), "$I$", loc="bot")
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$2{OHM}$"))
    dot(d, (7.5, 4)); text(d, (7.5, 4.5), "$b$")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$4{OHM}$", loc="top"))
    wire(d, (7.5, 4), (10.5, 4))
    isrc(d, (10.5, 0), (10.5, 4), "$3\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (10.5, 0))
    dot(d, (3.5, 0)); dot(d, (7.5, 0))
    save(d, "t-super")


def t_super_ccvs():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 5), "$10\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 5), (3.2, 5)).label(f"$2{OHM}$"))
    cur(d, (3.2, 5), (4.5, 5), "$i$")
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$a$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 2.5)).label(f"$4{OHM}$", loc="top"))
    vsrc(d, (4.5, 0), (4.5, 2.5), "$2i$", loc="top", ctrl=True)
    d.add(elm.Gap().endpoints((6.2, 4.6), (6.2, 0.4)).label(("+", "$U$", "−"), loc="bot"))
    wire(d, (4.5, 5), (8.5, 5))
    isrc(d, (8.5, 0), (8.5, 5), "$3\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (8.5, 0))
    dot(d, (4.5, 0))
    save(d, "t-super-ccvs")


def t_linear():
    d = new_drawing()
    box(d, 2.5, -0.4, 6.5, 3.4, "$N$")
    vsrc(d, (0, 0), (0, 3), "$U_S$")
    wire(d, (0, 3), (2.5, 3)); wire(d, (0, 0), (2.5, 0))
    wire(d, (6.5, 3), (9, 3)); wire(d, (6.5, 0), (9, 0))
    isrc(d, (9, 0), (9, 3), "$I_S$", loc="top")
    d.add(elm.Gap().endpoints((10.2, 0.2), (10.2, 2.8)).label(("−", "$U$", "+"), loc="bot"))
    dot(d, (9, 3)); dot(d, (9, 0))
    save(d, "t-linear")


def t_thevenin():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$24\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$4{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$12{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$6{OHM}$"))
    isrc(d, (7.5, 0), (7.5, 4), "$2\\,\\mathrm{A}$", loc="top")
    wire(d, (7.5, 4), (9.5, 4)); wire(d, (0, 0), (9.5, 0))
    dot(d, (3.5, 0)); dot(d, (7.5, 4)); dot(d, (7.5, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    text(d, (9.5, 4.5), "$a$"); text(d, (9.5, -0.5), "$b$")
    wire(d, (9.5, 4), (11.5, 4)); wire(d, (9.5, 0), (11.5, 0))
    d.add(elm.Resistor().endpoints((11.5, 4), (11.5, 0)).label("$R_L$", loc="bot"))
    save(d, "t-thevenin")


def t_norton():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$18\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$3{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$6{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$2{OHM}$"))
    isrc(d, (7.5, 4), (7.5, 0), "$1\\,\\mathrm{A}$", loc="top")
    wire(d, (7.5, 4), (9.5, 4)); wire(d, (0, 0), (9.5, 0))
    dot(d, (3.5, 0)); dot(d, (7.5, 4)); dot(d, (7.5, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    text(d, (9.95, 4), "$a$"); text(d, (9.95, 0), "$b$")
    save(d, "t-norton")


def t_ccvs_thevenin():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.2, 4)).label(f"$4{OHM}$"))
    cur(d, (3.2, 4), (4.5, 4), "$i_1$")
    dot(d, (4.5, 4)); text(d, (4.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((4.5, 4), (4.5, 0)).label(f"$4{OHM}$", loc="top"))
    wire(d, (4.5, 4), (5.5, 4))
    vsrc_h(d, (8.5, 4), (5.5, 4), "$2i_1$", ctrl=True)
    wire(d, (8.5, 4), (9.5, 4)); wire(d, (0, 0), (9.5, 0))
    dot(d, (4.5, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    text(d, (9.95, 4), "$a$"); text(d, (9.95, 0), "$b$")
    save(d, "t-ccvs-thevenin")


def t_4_36():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$U_{S1}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label("$R_1$"))
    dot(d, (3.5, 4))
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label("$R_2$", loc="top"))
    cur(d, (3.5, 4), (6, 4), "$I_2$")
    dot(d, (6, 4)); text(d, (6, 4.5), "$a$")
    d.add(elm.Switch().endpoints((6, 4), (6, 0)).label("$S$", loc="top"))
    arrow(d, (6.7, 1.6), (6.7, 0.4), "$I_3$", loc="bot")
    wire(d, (6, 4), (8.5, 4)); wire(d, (0, 0), (8.5, 0))
    dot(d, (3.5, 0)); dot(d, (6, 0)); text(d, (6, -0.5), "$b$")
    box(d, 8.5, -0.6, 11, 4.6, "A")
    save(d, "t-4-36")


if __name__ == "__main__":
    t_super()
    t_super_ccvs()
    t_linear()
    t_thevenin()
    t_norton()
    t_ccvs_thevenin()
    t_4_36()
