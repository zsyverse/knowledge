"""正弦稳态、功率与谐振页插图。交流源用 SourceSin，并在圆外标出参考极性。"""
from common import elm, new_drawing, save, dot, text, cur

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def ac_src(d, p, q, label, loc="top"):
    """竖直交流电压源：p 在下，q 在上，+ 端在 q（上）。"""
    d.add(elm.SourceSin().endpoints(p, q).label(label, loc=loc).label(("−", "", "+"), loc="bot" if loc == "top" else "top", ofst=0.1))


def ac_5_22():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 5), "$\\dot U$")
    cur(d, (0, 5), (1.2, 5), "$\\dot I_1$")
    d.add(elm.Resistor().endpoints((1.2, 5), (4.5, 5)).label("$R_1$"))
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$a$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 2.5)).label("$R_2$", loc="top"))
    d.add(elm.Inductor2(loops=3).endpoints((4.5, 2.5), (4.5, 0)).label("$jX_2$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((5.2, 4.3), (5.2, 3.1)).label("$\\dot I_2$", loc="bot"))
    d.add(elm.Line().endpoints((4.5, 5), (8.5, 5)))
    d.add(elm.Resistor().endpoints((8.5, 5), (8.5, 2.5)).label("$R_3$", loc="top"))
    d.add(elm.Capacitor().endpoints((8.5, 2.5), (8.5, 0)).label("$-jX_3$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((9.2, 4.3), (9.2, 3.1)).label("$\\dot I_3$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (8.5, 0)))
    dot(d, (4.5, 0)); text(d, (4.5, -0.5), "$b$")
    save(d, "ac-5-22")


def ac_5_16():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    d.add(elm.Gap().endpoints((0, 5), (0, 0)).label(("+", "$u$", "−"), loc="bot"))
    cur(d, (0, 5), (1.0, 5), "$i$")
    d.add(elm.Capacitor().endpoints((1.0, 5), (4.0, 5)).label(f"$-j10{OHM}$"))
    d.add(elm.Line().endpoints((4.0, 5), (8.5, 5)))
    dot(d, (5, 5))
    d.add(elm.Resistor().endpoints((5, 5), (5, 2.5)).label("$R$", loc="top"))
    d.add(elm.Capacitor().endpoints((5, 2.5), (5, 0)).label("$-jX_C$", loc="top"))
    d.add(elm.Inductor2(loops=4).endpoints((8.5, 5), (8.5, 0)).label(f"$j10{OHM}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (8.5, 0)))
    dot(d, (5, 0))
    save(d, "ac-5-16")


def ac_5_21():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 5), "$\\dot U_S=20\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.Capacitor().endpoints((0, 5), (3, 5)).label(f"$Z_1=-j1{OHM}$"))
    cur(d, (3, 5), (4.5, 5), "$\\dot I_1$")
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$a$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 2.5)).label(f"$6{OHM}$", loc="top"))
    d.add(elm.Inductor2(loops=3).endpoints((4.5, 2.5), (4.5, 0)).label(f"$j8{OHM}$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((5.2, 4.3), (5.2, 3.1)).label("$\\dot I_2$", loc="bot"))
    d.add(elm.Line().endpoints((4.5, 5), (8.5, 5)))
    d.add(elm.Resistor().endpoints((8.5, 5), (8.5, 2.5)).label(f"$3{OHM}$", loc="top"))
    d.add(elm.Capacitor().endpoints((8.5, 2.5), (8.5, 0)).label(f"$-j4{OHM}$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((9.2, 4.3), (9.2, 3.1)).label("$\\dot I_3$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (8.5, 0)))
    dot(d, (4.5, 0)); text(d, (4.5, -0.5), "$b$")
    save(d, "ac-5-21")


def pf_correction():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_S$\n$100\\,\\mathrm{V},\\ 50\\,\\mathrm{Hz}$")
    cur(d, (0, 4), (3, 4), "$\\dot I$")
    d.add(elm.Line().endpoints((3, 4), (9, 4)))
    d.add(elm.RBox().endpoints((3, 4), (3, 0)).label("$Z_1$", loc="top").label("感性", loc="bot", fontsize=12))
    d.add(elm.Resistor().endpoints((6, 4), (6, 0)).label(f"$R=20{OHM}$", loc="bot"))
    d.add(elm.Capacitor().endpoints((9, 4), (9, 0)).label("$C$", loc="bot").color("#2a78d6"))
    d.add(elm.Line().endpoints((0, 0), (9, 0)))
    for x in (3, 6):
        dot(d, (x, 4)); dot(d, (x, 0))
    text(d, (10.2, 3.3), "补偿电容", fontsize=12, color="#2a78d6")
    save(d, "pf-correction")


def series_rlc():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U$", loc="bot")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label("$R$").label(("+", "$\\dot U_R$", "−"), loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4), (7, 4)).label("$L$").label(("+", "$\\dot U_L$", "−"), loc="bot"))
    cur(d, (7, 4), (8.5, 4), "$\\dot I$")
    d.add(elm.Capacitor().endpoints((8.5, 4), (8.5, 0)).label("$C$", loc="bot").label(("+", "$\\dot U_C$", "−"), loc="top"))
    d.add(elm.Line().endpoints((0, 0), (8.5, 0)))
    save(d, "series-rlc")


def resonance_5_27():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    text(d, (-0.45, 5), "$a$"); text(d, (-0.45, 0), "$b$")
    d.add(elm.Line().endpoints((0, 5), (6, 5)))
    d.add(elm.Line().endpoints((0, 0), (6, 0)))
    d.add(elm.Inductor2(loops=4).endpoints((2.5, 5), (2.5, 0)).label("$L_1=0.4\\,\\mathrm{H}$", loc="bot"))
    dot(d, (2.5, 5)); dot(d, (2.5, 0))
    d.add(elm.Inductor2(loops=3).endpoints((6, 5), (6, 2.5)).label("$L_2=0.6\\,\\mathrm{H}$", loc="bot"))
    d.add(elm.Capacitor().endpoints((6, 2.5), (6, 0)).label("$C=1\\,\\mu\\mathrm{F}$", loc="bot"))
    save(d, "resonance-5-27")


if __name__ == "__main__":
    ac_5_22()
    ac_5_16()
    ac_5_21()
    pf_correction()
    series_rlc()
    resonance_5_27()
