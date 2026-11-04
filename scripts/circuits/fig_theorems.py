"""电路定理页插图。"""
from common import elm, new_drawing, save, dot, text, cur

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def superposition():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 4)).label("$U_s=12\\,\\mathrm{V}$", loc="top"))
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label(f"$R_1=4{OHM}$"))
    dot(d, (4, 4)); text(d, (4, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((4, 4), (4, 0)).label(f"$R_2=6{OHM}$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((4.7, 3.0), (4.7, 1.0)).label("$i$", loc="bot"))
    d.add(elm.Line().endpoints((4, 4), (7.5, 4)))
    d.add(elm.SourceI().endpoints((7.5, 0), (7.5, 4)).label("$I_s=3\\,\\mathrm{A}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (7.5, 0)))
    dot(d, (4, 0))
    save(d, "superposition")


def thevenin_norton():
    d = new_drawing()
    # 黑箱
    for p, q in (((0, 0), (3, 0)), ((3, 0), (3, 4)), ((3, 4), (0, 4)), ((0, 4), (0, 0))):
        d.add(elm.Line().endpoints(p, q).color("#3b5bdb"))
    text(d, (1.5, 2.3), "含源线性", fontsize=13)
    text(d, (1.5, 1.6), "网络 $N$", fontsize=13)
    d.add(elm.Line().endpoints((3, 3.4), (4.3, 3.4)))
    d.add(elm.Line().endpoints((3, 0.6), (4.3, 0.6)))
    dot(d, (4.3, 3.4), True); dot(d, (4.3, 0.6), True)
    text(d, (4.65, 3.4), "$a$"); text(d, (4.65, 0.6), "$b$")
    text(d, (5.9, 2.0), "$\\Longleftrightarrow$", fontsize=22)
    # 戴维南
    x = 7.3
    d.add(elm.SourceV().endpoints((x, 0.6), (x, 3.4)).label("$U_{oc}$", loc="bot"))
    d.add(elm.Resistor().endpoints((x, 3.4), (x + 3, 3.4)).label("$R_{eq}$"))
    d.add(elm.Line().endpoints((x, 0.6), (x + 3, 0.6)))
    dot(d, (x + 3, 3.4), True); dot(d, (x + 3, 0.6), True)
    text(d, (x + 3.35, 3.4), "$a$"); text(d, (x + 3.35, 0.6), "$b$")
    text(d, (x + 4.6, 2.0), "$\\Longleftrightarrow$", fontsize=22)
    # 诺顿
    x = 13.4
    d.add(elm.SourceI().endpoints((x, 0.6), (x, 3.4)).label("$I_{sc}$", loc="bot"))
    d.add(elm.Line().endpoints((x, 3.4), (x + 3.6, 3.4)))
    d.add(elm.Line().endpoints((x, 0.6), (x + 3.6, 0.6)))
    d.add(elm.Resistor().endpoints((x + 2, 3.4), (x + 2, 0.6)).label("$R_{eq}$", loc="bot"))
    dot(d, (x + 2, 3.4)); dot(d, (x + 2, 0.6))
    dot(d, (x + 3.6, 3.4), True); dot(d, (x + 3.6, 0.6), True)
    text(d, (x + 3.95, 3.4), "$a$"); text(d, (x + 3.95, 0.6), "$b$")
    save(d, "thevenin-norton")


def thevenin_example():
    d = new_drawing()
    d.add(elm.SourceI().endpoints((0, 0), (0, 4)).label("$I_S=1\\,\\mathrm{A}$", loc="top"))
    dot(d, (0, 4)); text(d, (-0.45, 4.35), "$A$")
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label(f"$R_1=40{OHM}$", loc="bot"))
    dot(d, (4, 4)); text(d, (4, 4.5), "$B$")
    d.add(elm.Resistor().endpoints((4, 4), (4, 0)).label(f"$R_3=3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((4, 4), (8, 4)).label(f"$R_2=8{OHM}$", loc="bot"))
    dot(d, (8, 4)); text(d, (8.4, 4.35), "$C$")
    d.add(elm.Line().endpoints((0, 4), (0, 6.5)))
    d.add(elm.Resistor().endpoints((0, 6.5), (8, 6.5)).label(f"$R_4=16{OHM}$"))
    d.add(elm.Line().endpoints((8, 6.5), (8, 4)))
    d.add(elm.Line().endpoints((8, 4), (11, 4)))
    d.add(elm.ResistorVar().endpoints((11, 4), (11, 0)).label("$R$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (11, 0)))
    dot(d, (4, 0))
    d.add(elm.Ground().at((6, 0)))
    save(d, "thevenin-example")


def negative_resistance():
    d = new_drawing()
    d.add(elm.SourceI().endpoints((0, 0), (0, 4)).label("$1\\,\\mathrm{A}$", loc="top"))
    d.add(elm.Line().endpoints((0, 4), (3, 4)))
    dot(d, (3, 4)); text(d, (3, 4.5), "$x$")
    d.add(elm.Resistor().endpoints((3, 4), (3, 0)).label(f"$2{OHM}$", loc="top")
          .label(("+", "$U_2$", "−"), loc="bot"))
    d.add(elm.Resistor().endpoints((3, 4), (7, 4)).label(f"$3{OHM}$"))
    dot(d, (7, 4))
    d.add(elm.SourceControlledI().endpoints((7, 0), (7, 4)).label("$gU_2$", loc="bot"))
    d.add(elm.Line().endpoints((7, 4), (9.5, 4)))
    d.add(elm.Line().endpoints((0, 0), (9.5, 0)))
    dot(d, (3, 0)); dot(d, (7, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    text(d, (9.9, 4), "$a$"); text(d, (9.9, 0), "$b$")
    save(d, "negative-resistance")


if __name__ == "__main__":
    superposition()
    thevenin_norton()
    thevenin_example()
    negative_resistance()
