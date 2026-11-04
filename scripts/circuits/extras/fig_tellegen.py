"""拓展·特勒根定理、互易与对偶 插图（前缀 td-）。"""
from xcommon import (elm, new_drawing, save, dot, text, cur, arrow, vsrc, isrc, wire, OHM, MUTED)


def box(d, x0, y0, x1, y1, label):
    wire(d, (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
    text(d, ((x0 + x1) / 2, (y0 + y1) / 2), label, fontsize=18)


def one_case(name, lt, rt, lab, tag):
    """lt/rt: ('V', 值) 电压源 | ('R', 值) 电阻 | ('S',) 短路 | ('O',) 开路 | ('I', 值) 电流源（箭头向上）。"""
    d = new_drawing()
    bx0, bx1 = 3.4, 7.0
    box(d, bx0, -0.4, bx1, 3.4, "$N_R$")
    yt, yb = 3.0, 0.0
    il, ir, ul, ur = lab
    xl, xr = 1.4, 9.0
    cur(d, (xl, yt), (bx0, yt), il, loc="top")
    cur(d, (xr, yt), (bx1, yt), ir, loc="top")
    wire(d, (xl, yb), (bx0, yb)); wire(d, (bx1, yb), (xr, yb))
    for x in (xl, xr):
        dot(d, (x, yt)); dot(d, (x, yb))
    for x, u in ((2.4, ul), (8.0, ur)):
        text(d, (x, yt - 0.55), "$+$"); text(d, (x, 1.5), u); text(d, (x, yb + 0.55), "$−$")
    for xx, (kind, *v), loc in ((xl, lt, "top"), (xr, rt, "bot")):
        if kind == "V":
            vsrc(d, (xx, yb), (xx, yt), v[0], loc=loc)
        elif kind == "R":
            d.add(elm.Resistor().endpoints((xx, yt), (xx, yb)).label(v[0], loc=loc))
        elif kind == "S":
            wire(d, (xx, yt), (xx, yb))
        elif kind == "I":
            isrc(d, (xx, yb), (xx, yt), v[0], loc=loc)
    text(d, (5.2, -1.2), tag, fontsize=14)
    save(d, name)


HAT = ("$\\hat I_1$", "$\\hat I_2$", "$\\hat U_1$", "$\\hat U_2$")
PLAIN = ("$I_1$", "$I_2$", "$U_1$", "$U_2$")


def mesh_node():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 3.5), "$10\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 3.5), (3.5, 3.5)).label(f"$R_1=2{OHM}$"))
    d.add(elm.Resistor().endpoints((3.5, 3.5), (3.5, 0)).label(f"$R_3=4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((3.5, 3.5), (8.5, 3.5)).label(f"$R_2=1{OHM}$"))
    d.add(elm.Resistor().endpoints((8.5, 3.5), (8.5, 0)).label(f"$R_4=3{OHM}$", loc="bot"))
    wire(d, (0, 0), (8.5, 0)); dot(d, (3.5, 3.5)); dot(d, (3.5, 0))
    d.add(elm.LoopArrow(direction="cw", width=1.4, height=1.4).at((1.75, 1.75)).label("$I_a$", loc="center")) \
        if hasattr(elm, "LoopArrow") else None
    d.add(elm.LoopArrow(direction="cw", width=1.4, height=1.4).at((6.9, 1.75)).label("$I_b$", loc="center")) \
        if hasattr(elm, "LoopArrow") else None
    save(d, "td-mesh")

    d = new_drawing()
    isrc(d, (0, 0), (0, 3.5), "$10\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 3.5), (2.5, 3.5))
    d.add(elm.Resistor().endpoints((2.5, 3.5), (2.5, 0)).label("$G_1=2\\,\\mathrm{S}$", loc="bot"))
    d.add(elm.Resistor().endpoints((2.5, 3.5), (6.5, 3.5)).label("$G_3=4\\,\\mathrm{S}$"))
    d.add(elm.Resistor().endpoints((6.5, 3.5), (6.5, 0)).label("$G_2=1\\,\\mathrm{S}$", loc="bot"))
    wire(d, (6.5, 3.5), (9.5, 3.5))
    d.add(elm.Resistor().endpoints((9.5, 3.5), (9.5, 0)).label("$G_4=3\\,\\mathrm{S}$", loc="bot"))
    wire(d, (0, 0), (9.5, 0))
    for p in ((2.5, 3.5), (6.5, 3.5), (2.5, 0), (6.5, 0)):
        dot(d, p)
    text(d, (2.5, 4.0), "$a$"); text(d, (6.5, 4.0), "$b$")
    d.add(elm.Ground().at((4.5, 0)))
    save(d, "td-node")


if __name__ == "__main__":
    one_case("td-tel-a", ("V", "$10\\,\\mathrm{V}$"), ("S",), PLAIN, "(a)")
    one_case("td-tel-b", ("R", f"$2{OHM}$"), ("V", "$20\\,\\mathrm{V}$"), HAT, "(b)")
    one_case("td-x2-a", ("V", "$10\\,\\mathrm{V}$"), ("O",), PLAIN, "(a)")
    one_case("td-x2-b", ("S",), ("I", "$3\\,\\mathrm{A}$"), HAT, "(b)")
    mesh_node()
