"""习题·正弦稳态与相量法 插图（前缀 p-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, arrow, wire, ac_src, OHM


def meter(d, kind, p, q, label):
    e = (elm.MeterA() if kind == "A" else elm.MeterV()).endpoints(p, q)
    d.add(e)
    if label:
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        vertical = abs(p[0] - q[0]) < 1e-9
        text(d, (mx + 0.95, my) if vertical else (mx, my + 0.95), label)


def p_meters_a():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 5.5), "$\\dot U$")
    meter(d, "A", (0, 5.5), (2.4, 5.5), "$A_0$")
    wire(d, (2.4, 5.5), (9.5, 5.5))
    for x, el, name, lab in ((3.5, elm.Resistor(), "$A_1$", "$R$"),
                             (6.5, elm.Inductor2(loops=3), "$A_2$", "$L$"),
                             (9.5, elm.Capacitor(), "$A_3$", "$C$")):
        meter(d, "A", (x, 5.5), (x, 3.3), name)
        d.add(el.endpoints((x, 3.3), (x, 0)).label(lab, loc="bot"))
    for x in (3.5, 6.5):
        dot(d, (x, 5.5)); dot(d, (x, 0))
    wire(d, (0, 0), (9.5, 0))
    save(d, "p-meters-a")


def p_meters_b():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U$")
    wire(d, (0, 4), (1.5, 4))
    xs = (1.5, 4.5, 7.5, 10.5)
    els = (elm.Resistor().label("$R$", loc="bot"), elm.Inductor2(loops=3).label("$L$", loc="bot"),
           elm.Capacitor().label("$C$", loc="bot"))
    for (x0, x1), el, name in zip(zip(xs, xs[1:]), els, ("$V_1$", "$V_2$", "$V_3$")):
        d.add(el.endpoints((x0, 4), (x1, 4)))
        wire(d, (x0, 4), (x0, 6.3)); wire(d, (x1, 4), (x1, 6.3))
        d.add(elm.MeterV().endpoints((x0 + 0.25, 6.3), (x1 - 0.25, 6.3)))
        wire(d, (x0, 6.3), (x0 + 0.25, 6.3)); wire(d, (x1 - 0.25, 6.3), (x1, 6.3))
        text(d, ((x0 + x1) / 2, 7.3), name)
    for x in xs:
        dot(d, (x, 4))
    wire(d, (10.5, 4), (10.5, 0), (0, 0))
    save(d, "p-meters-b")


def p_impedance():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    text(d, (-0.45, 5), "$a$"); text(d, (-0.45, 0), "$b$")
    d.add(elm.Resistor().endpoints((0, 5), (3.5, 5)).label(f"$4{OHM}$"))
    wire(d, (3.5, 5), (8, 5))
    d.add(elm.Inductor2(loops=4).endpoints((4.5, 5), (4.5, 0)).label(f"$j6{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((8, 5), (8, 2.5)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Capacitor().endpoints((8, 2.5), (8, 0)).label(f"$-j3{OHM}$", loc="bot"))
    wire(d, (0, 0), (8, 0))
    dot(d, (4.5, 5)); dot(d, (4.5, 0))
    save(d, "p-impedance")


def p_5_14():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    d.add(elm.Resistor().endpoints((0, 5), (3, 5)).label(f"$6{OHM}$"))
    d.add(elm.Capacitor().endpoints((3, 5), (5.5, 5)).label(f"$-j6{OHM}$")
          .label(("+", "$\\dot U_C$", "−"), loc="bot"))
    wire(d, (5.5, 5), (9, 5))
    dot(d, (6.5, 5)); dot(d, (6.5, 0))
    d.add(elm.SourceControlledI().endpoints((6.5, 0), (6.5, 5)).label("$0.5\\dot U_C$", loc="bot"))
    d.add(elm.Inductor2(loops=4).endpoints((9, 5), (9, 0)).label(f"$j12{OHM}$", loc="bot"))
    wire(d, (0, 0), (9, 0))
    arrow(d, (0.6, 2.5), (2.4, 2.5), "$Z$", loc="top")
    save(d, "p-5-14")


def p_lamp():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U$")
    text(d, (4.6, -0.7), "$U=220\\,\\mathrm{V},\\ f=50\\,\\mathrm{Hz}$")
    cur(d, (0, 4), (1.5, 4), "$\\dot I$")
    d.add(elm.Resistor().endpoints((1.5, 4), (5, 4)).label("灯管 $R$"))
    d.add(elm.Inductor2(loops=4).endpoints((5, 4), (8.5, 4)).label("镇流器 $L$"))
    wire(d, (8.5, 4), (8.5, 0), (0, 0))
    save(d, "p-lamp")


def p_5_12():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    d.add(elm.Gap().endpoints((0, 4.6), (0, 0.4)).label(("+", "$\\dot U$", "−"), loc="top"))
    cur(d, (0, 5), (1.3, 5), "$\\dot I$")
    d.add(elm.Resistor().endpoints((1.3, 5), (4.5, 5)).label("$R_1$", loc="bot")
          .label(("+", "$\\dot U_{R_1}$", "−"), loc="top"))
    dot(d, (4.5, 5))
    d.add(elm.Capacitor().endpoints((4.5, 5), (4.5, 0)).label("$-jX_C$", loc="bot")
          .label(("+", "$\\dot U_C$", "−"), loc="top"))
    arrow(d, (5.3, 2.0), (5.3, 0.8), "$\\dot I_1$", loc="bot")
    cur(d, (4.5, 5), (5.8, 5), "$\\dot I_2$")
    d.add(elm.Resistor().endpoints((5.8, 5), (9, 5)).label("$R_2$", loc="bot")
          .label(("+", "$\\dot U_{R_2}$", "−"), loc="top"))
    d.add(elm.Inductor2(loops=4).endpoints((9, 5), (9, 0)).label("$jX_L$", loc="bot")
          .label(("+", "$\\dot U_L$", "−"), loc="top"))
    wire(d, (0, 0), (9, 0))
    dot(d, (4.5, 0))
    save(d, "p-5-12")


def p_node():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4.5), "$u_{S1}$")
    d.add(elm.Resistor().endpoints((0, 4.5), (3.5, 4.5)).label(f"$R=5{OHM}$"))
    dot(d, (3.5, 4.5)); text(d, (3.5, 5.0), "$a$")
    d.add(elm.Capacitor().endpoints((3.5, 4.5), (3.5, 0)).label("$C=200\\,\\mu\\mathrm{F}$", loc="top"))
    arrow(d, (4.2, 2.9), (4.2, 1.6), "$i_C$", loc="bot")
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4.5), (7.5, 4.5)).label("$L=5\\,\\mathrm{mH}$"))
    ac_src(d, (7.5, 0), (7.5, 4.5), "$u_{S2}$", loc="bot")
    wire(d, (0, 0), (7.5, 0))
    dot(d, (3.5, 0))
    save(d, "p-node")


if __name__ == "__main__":
    p_meters_a()
    p_meters_b()
    p_impedance()
    p_5_14()
    p_lamp()
    p_5_12()
    p_node()
