"""互感、变压器、三相单相等效、非正弦页插图。"""
from common import elm, new_drawing, save, dot, text, cur
from fig_ac import ac_src

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def pdot(d, xy):
    """同名端标记（实心大圆点）。"""
    d.add(elm.Dot(radius=0.13).at(xy))


def m_arrow(d, p, q, label="$M$"):
    d.add(elm.Arrow(double=True, headwidth=0.25, headlength=0.3).endpoints(p, q).label(label))


def coupled_dots():
    d = new_drawing()
    dot(d, (0, 4), True); dot(d, (0, 0), True)
    cur(d, (0, 4), (2, 4), "$i_1$")
    d.add(elm.Line().endpoints((0, 0), (2, 0)))
    d.add(elm.Gap().endpoints((0, 4), (0, 0)).label(("+", "$u_1$", "−"), loc="top"))
    d.add(elm.Inductor2(loops=4).endpoints((2, 4), (2, 0)).label("$L_1$", loc="top"))
    dot(d, (7, 4), True); dot(d, (7, 0), True)
    cur(d, (7, 4), (5, 4), "$i_2$")
    d.add(elm.Line().endpoints((7, 0), (5, 0)))
    d.add(elm.Gap().endpoints((7, 4), (7, 0)).label(("+", "$u_2$", "−"), loc="bot"))
    d.add(elm.Inductor2(loops=4).endpoints((5, 4), (5, 0)).label("$L_2$", loc="bot"))
    pdot(d, (2.5, 2.85)); pdot(d, (4.5, 2.85))
    m_arrow(d, (2.8, 2.0), (4.2, 2.0))
    save(d, "coupled-dots")


def t_decoupling():
    d = new_drawing()
    # 原电路：1 —L1— 3 —L2— 2，3 端引出；同名端都在公共节点 3 一侧
    dot(d, (0, 4), True); text(d, (-0.4, 4), "$1$")
    d.add(elm.Inductor2(loops=3).endpoints((0, 4), (3, 4)).label("$L_1$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((3, 4), (6, 4)).label("$L_2$", loc="bot"))
    dot(d, (6, 4), True); text(d, (6.4, 4), "$2$")
    dot(d, (3, 4))
    d.add(elm.Line().endpoints((3, 4), (3, 1.5)))
    dot(d, (3, 1.5), True); text(d, (3, 1.05), "$3$")
    pdot(d, (2.2, 4.55)); pdot(d, (3.8, 4.55))
    m_arrow(d, (1.2, 5.3), (4.8, 5.3))
    text(d, (8.1, 3.4), "$\\Longleftrightarrow$", fontsize=22)
    # T 形等效
    x = 10
    dot(d, (x, 4), True); text(d, (x - 0.4, 4), "$1$")
    d.add(elm.Inductor2(loops=3).endpoints((x, 4), (x + 3, 4)).label("$L_1-M$"))
    d.add(elm.Inductor2(loops=3).endpoints((x + 3, 4), (x + 6, 4)).label("$L_2-M$"))
    dot(d, (x + 6, 4), True); text(d, (x + 6.4, 4), "$2$")
    dot(d, (x + 3, 4))
    d.add(elm.Inductor2(loops=3).endpoints((x + 3, 4), (x + 3, 1.0)).label("$M$", loc="bot"))
    dot(d, (x + 3, 1.0), True); text(d, (x + 3, 0.55), "$3$")
    save(d, "t-decoupling")


def coupled_5_35():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 6), "$\\dot U$", loc="bot")
    d.add(elm.Line().endpoints((0, 6), (7.5, 6)))
    d.add(elm.Line().endpoints((0, 0), (7.5, 0)))
    d.add(elm.Resistor().endpoints((3.5, 6), (3.5, 3)).label(f"$R_1=10{OHM}$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 3), (3.5, 0)).label("$L_1$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((2.8, 5.3), (2.8, 4.1)).label("$\\dot I_1$", loc="top"))
    d.add(elm.Resistor().endpoints((7.5, 6), (7.5, 3)).label(f"$R_2=5{OHM}$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((7.5, 3), (7.5, 0)).label("$L_2$", loc="bot"))
    d.add(elm.Arrow(**ARW).endpoints((6.8, 5.3), (6.8, 4.1)).label("$\\dot I_2$", loc="top"))
    dot(d, (3.5, 6)); dot(d, (3.5, 0))
    pdot(d, (3.95, 2.35)); pdot(d, (7.05, 0.65))
    m_arrow(d, (4.4, 1.5), (6.6, 1.5))
    save(d, "coupled-5-35")


def ideal_transformer():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 3.2)).label("$U_S$", loc="top"))
    d.add(elm.Resistor().endpoints((0, 3.2), (3.5, 3.2)).label(f"$270{OHM}$"))
    d.add(elm.Line().endpoints((3.5, 3.2), (5, 3.2)))
    d.add(elm.Line().endpoints((0, 0), (5, 0)))
    d.add(elm.Transformer(t1=4, t2=4).scale(2).at((5, 0)))
    d.add(elm.Line().endpoints((7, 3.2), (9, 3.2)))
    d.add(elm.Line().endpoints((7, 0), (9, 0)))
    d.add(elm.Resistor().endpoints((9, 3.2), (9, 0)).label(f"$30{OHM}$", loc="bot"))
    pdot(d, (5.25, 3.0)); pdot(d, (6.75, 3.0))
    text(d, (6, 4.0), "$n:1$")
    save(d, "ideal-transformer")


def transformer_5_42():
    d = new_drawing()
    d.add(elm.Transformer(t1=4, t2=4).scale(2).at((3, 0)))
    pdot(d, (3.25, 3.0)); pdot(d, (4.75, 3.0))
    text(d, (2.4, 1.6), "$N_1$"); text(d, (5.6, 1.6), "$N_2$")
    # 下端相连为 o
    d.add(elm.Line().endpoints((3, 0), (3, -0.8)))
    d.add(elm.Line().endpoints((3, -0.8), (7, -0.8)))
    d.add(elm.Line().endpoints((5, 0), (5, -0.8)))
    dot(d, (5, -0.8)); text(d, (5, -1.25), "$o$")
    # b 端（N1 同名端）
    cur(d, (3, 3.2), (1, 3.2), "$I$")
    dot(d, (1, 3.2), True); text(d, (0.6, 3.2), "$b$")
    # a 端（N2 同名端）与电阻 R（a—o）
    d.add(elm.Line().endpoints((5, 3.2), (7, 3.2)))
    dot(d, (7, 3.2))
    d.add(elm.Resistor().endpoints((7, 3.2), (7, -0.8)).label("$R$", loc="bot"))
    cur(d, (9, 3.2), (7, 3.2), "$I$")
    dot(d, (9, 3.2), True); text(d, (9.4, 3.2), "$a$")
    save(d, "transformer-5-42")


def single_phase_equiv():
    d = new_drawing()
    d.add(elm.SourceSin().endpoints((0, 0), (0, 4)).label("$\\dot U_{A}$", loc="top")
          .label(("−", "", "+"), loc="bot", ofst=0.1))
    text(d, (0, -0.5), "$N$")
    cur(d, (0, 4), (1.2, 4), "$\\dot I_A$")
    d.add(elm.RBox().endpoints((1.2, 4), (4.5, 4)).label("$Z_l$"))
    d.add(elm.Line().endpoints((4.5, 4), (6, 4)))
    d.add(elm.RBox().endpoints((6, 4), (6, 0)).label("$Z_Y$", loc="bot"))
    d.add(elm.Line().endpoints((6, 0), (0, 0)))
    text(d, (6, -0.5), "$N'$")
    text(d, (3, -1.1), "（中线：对称时 $\\dot U_{N'N}=0$，可视为短接）", fontsize=11)
    save(d, "single-phase-equiv")


def freq_response_6_11():
    d = new_drawing()
    d.add(elm.SourceSin().endpoints((0, 0), (0, 5)).label("$u_S$", loc="top")
          .label(("−", "", "+"), loc="bot", ofst=0.1))
    d.add(elm.Resistor().endpoints((0, 5), (3.5, 5)).label("$R$"))
    dot(d, (3.5, 5)); text(d, (3.5, 5.5), "$c$")
    d.add(elm.Line().endpoints((3.5, 5), (8, 5)))
    d.add(elm.Resistor().endpoints((5, 5), (5, 0)).label("$R$", loc="top"))
    dot(d, (5, 5)); dot(d, (5, 0))
    d.add(elm.Inductor2(loops=3).endpoints((8, 5), (8, 2.6)).label("$L_1$", loc="bot"))
    d.add(elm.Line().endpoints((7, 2.6), (9.4, 2.6)))
    dot(d, (8, 2.6))
    d.add(elm.Inductor2(loops=3).endpoints((7, 2.6), (7, 0)).label("$L_2$", loc="top"))
    d.add(elm.Capacitor().endpoints((9.4, 2.6), (9.4, 0)).label("$C=0.25\\,\\mathrm{F}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (9.4, 0)))
    dot(d, (7, 0)); dot(d, (3.5, 0)); text(d, (3.5, -0.5), "$d$")
    d.add(elm.Gap().endpoints((3.5, 4.4), (3.5, 0.6)).label(("+", "$u_{CD}$", "−"), loc="top"))
    save(d, "freq-response-6-11")


if __name__ == "__main__":
    coupled_dots()
    t_decoupling()
    coupled_5_35()
    ideal_transformer()
    transformer_5_42()
    single_phase_equiv()
    freq_response_6_11()
