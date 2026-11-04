"""等效变换页插图。"""
from common import elm, new_drawing, save, dot, text, cur

OHM = "\\,\\Omega"


def bridge_switch():
    d = new_drawing()
    dot(d, (0, 6), True)
    dot(d, (0, 0), True)
    text(d, (-0.5, 6), "$a$")
    text(d, (-0.5, 0), "$b$")
    d.add(elm.Line().endpoints((0, 6), (10, 6)))
    d.add(elm.Line().endpoints((0, 0), (10, 0)))
    # a-b 直接相连的 10 Ω
    d.add(elm.Resistor().endpoints((2.5, 6), (2.5, 0)).label(f"$10{OHM}$", loc="bot"))
    dot(d, (2.5, 6)); dot(d, (2.5, 0))
    # 左桥臂 a-c-b
    d.add(elm.Resistor().endpoints((5, 6), (5, 3)).label(f"$10{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((5, 3), (5, 0)).label(f"$10{OHM}$", loc="top"))
    dot(d, (5, 6)); dot(d, (5, 0)); dot(d, (5, 3))
    text(d, (5.35, 2.6), "$c$")
    # 右桥臂 a-d-b
    d.add(elm.Resistor().endpoints((10, 6), (10, 3)).label(f"$20{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((10, 3), (10, 0)).label(f"$60{OHM}$", loc="bot"))
    dot(d, (10, 3))
    text(d, (9.65, 2.6), "$d$")
    # 桥 c-d：10 Ω 与开关 S 并联
    d.add(elm.Line().endpoints((5, 3), (6, 3)))
    d.add(elm.Resistor().endpoints((6, 3), (9, 3)).label(f"$10{OHM}$", loc="bot"))
    d.add(elm.Line().endpoints((9, 3), (10, 3)))
    d.add(elm.Line().endpoints((6, 3), (6, 4.4)))
    d.add(elm.Switch().endpoints((6, 4.4), (9, 4.4)).label("$S$"))
    d.add(elm.Line().endpoints((9, 4.4), (9, 3)))
    dot(d, (6, 3)); dot(d, (9, 3))
    save(d, "bridge-switch")


def y_delta():
    d = new_drawing()
    # Y（星形）
    o = (2.2, 2.2)
    a, b, c = (2.2, 5.6), (-0.6, 0.0), (5.0, 0.0)
    d.add(elm.Resistor().endpoints(a, o).label("$R_a$", loc="bot"))
    d.add(elm.Resistor().endpoints(b, o).label("$R_b$", loc="top"))
    d.add(elm.Resistor().endpoints(c, o).label("$R_c$", loc="bot"))
    dot(d, o)
    for p, s, off in ((a, "$a$", (0, 0.45)), (b, "$b$", (-0.4, -0.3)), (c, "$c$", (0.4, -0.3))):
        dot(d, p, True)
        text(d, (p[0] + off[0], p[1] + off[1]), s)
    text(d, (7.3, 2.4), "$\\Longleftrightarrow$", fontsize=22)
    # Δ（三角形）
    A, B, C = (12.4, 5.6), (9.6, 0.0), (15.2, 0.0)
    d.add(elm.Resistor().endpoints(A, B).label("$R_{ab}$", loc="top"))
    d.add(elm.Resistor().endpoints(B, C).label("$R_{bc}$", loc="bot"))
    d.add(elm.Resistor().endpoints(C, A).label("$R_{ca}$", loc="top"))
    for p, s, off in ((A, "$a$", (0, 0.45)), (B, "$b$", (-0.4, -0.3)), (C, "$c$", (0.4, -0.3))):
        dot(d, p, True)
        text(d, (p[0] + off[0], p[1] + off[1]), s)
    save(d, "y-delta")


def source_transform():
    d = new_drawing()
    # 戴维南形式：U_s 串 R
    d.add(elm.SourceV().endpoints((0, 0), (0, 3)).label("$U_s$", loc="bot"))
    d.add(elm.Resistor().endpoints((0, 3), (3, 3)).label("$R$"))
    d.add(elm.Line().endpoints((0, 0), (3, 0)))
    dot(d, (3, 3), True); dot(d, (3, 0), True)
    text(d, (3.4, 3), "$a$"); text(d, (3.4, 0), "$b$")
    text(d, (5.2, 1.5), "$\\Longleftrightarrow$", fontsize=22)
    # 诺顿形式：I_s 并 R
    d.add(elm.SourceI().endpoints((7, 0), (7, 3)).label("$I_s=\\dfrac{U_s}{R}$", loc="bot"))
    d.add(elm.Line().endpoints((7, 3), (12, 3)))
    d.add(elm.Line().endpoints((7, 0), (12, 0)))
    d.add(elm.Resistor().endpoints((10, 3), (10, 0)).label("$R$", loc="bot"))
    dot(d, (10, 3)); dot(d, (10, 0))
    dot(d, (12, 3), True); dot(d, (12, 0), True)
    text(d, (12.4, 3), "$a$"); text(d, (12.4, 0), "$b$")
    save(d, "source-transform")


def source_simplify():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 3)).label("$10\\,\\mathrm{V}$", loc="bot"))
    d.add(elm.Resistor().endpoints((0, 3), (0, 6)).label(f"$5{OHM}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 6), (5, 6)))
    d.add(elm.Line().endpoints((0, 0), (5, 0)))
    d.add(elm.SourceI().endpoints((3, 0), (3, 6)).label("$6\\,\\mathrm{A}$", loc="bot"))
    dot(d, (3, 6)); dot(d, (3, 0))
    dot(d, (5, 6), True); dot(d, (5, 0), True)
    text(d, (5.4, 6), "$a$"); text(d, (5.4, 0), "$b$")
    save(d, "source-simplify")


def input_resistance():
    d = new_drawing()
    dot(d, (0, 4), True); dot(d, (0, 0), True)
    text(d, (-0.45, 4), "$a$"); text(d, (-0.45, 0), "$b$")
    d.add(elm.Gap().endpoints((0, 4), (0, 0)).label(("+", "$u$", "−"), loc="bot"))
    cur(d, (0, 4), (2, 4), "$i$")
    d.add(elm.Line().endpoints((2, 4), (5, 4)))
    d.add(elm.Line().endpoints((0, 0), (5, 0)))
    cur(d, (2, 4), (2, 3), None)
    text(d, (1.55, 3.35), "$i_1$")
    d.add(elm.Resistor().endpoints((2, 3), (2, 0)).label(f"$6{OHM}$", loc="bot"))
    dot(d, (2, 4)); dot(d, (2, 0))
    d.add(elm.Resistor().endpoints((5, 4), (5, 2)).label(f"$3{OHM}$", loc="top"))
    d.add(elm.SourceControlledV().endpoints((5, 0), (5, 2)).label("$2i_1$", loc="top"))
    save(d, "input-resistance")


if __name__ == "__main__":
    bridge_switch()
    y_delta()
    source_transform()
    source_simplify()
    input_resistance()
