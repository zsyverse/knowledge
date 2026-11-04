"""习题·动态电路 插图（前缀 d-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, arrow, vsrc, isrc, wire, OHM


def sw(d, p, q, action, label="$S\\ (t=0)$", loc="top", pol=None, **kw):
    e = elm.Switch(action=action).endpoints(p, q)
    if label:
        e.label(label, loc=loc, **kw)
    if pol:
        e.label(("+", pol, "−"), loc="bot")
    d.add(e)
    return e


def d_73():
    """作业 7-3：S 由 1 扳向 2。"""
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$24\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (2.6, 4)).label(f"$R_1=1{OHM}$"))
    # 单刀双掷：触点 1 在 (3.1,4)，触点 2 在 (3.1,2.9)，动端在 (4.6,4)
    c1, c2, pv = (3.1, 4), (3.1, 2.9), (4.6, 4)
    wire(d, (2.6, 4), c1)
    dot(d, c1, True); dot(d, c2, True); dot(d, pv, True)
    d.add(elm.Line().endpoints(pv, (3.25, 4.25)))
    d.add(elm.Arc2(arrow="->", k=-0.4).at((3.65, 4.55)).to((3.45, 3.25)))
    text(d, (3.0, 4.5), "$1$"); text(d, (2.7, 2.9), "$2$")
    text(d, (4.3, 5.1), "$S\\ (t=0)$")
    wire(d, c2, (3.1, 0))
    dot(d, (3.1, 0))
    cur(d, pv, (5.6, 4), "$i$")
    d.add(elm.Inductor2(loops=3).endpoints((5.6, 4), (8.6, 4)).label("$2\\,\\mathrm{H}$")
          .label(("+", "$u_L$", "−"), loc="bot"))
    dot(d, (8.6, 4))
    d.add(elm.Resistor().endpoints((8.6, 4), (8.6, 0)).label(f"$R_2=5{OHM}$", loc="top"))
    wire(d, (8.6, 4), (11.5, 4))
    d.add(elm.Capacitor().endpoints((11.5, 4), (11.5, 0)).label("$0.2\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    arrow(d, (12.6, 3.4), (12.6, 2.0), "$i_C$", loc="bot")
    wire(d, (0, 0), (11.5, 0))
    dot(d, (8.6, 0))
    save(d, "d-73")


def d_rc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$18\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4.5), (3.5, 4.5)).label(f"$R_1=6{OHM}$"))
    dot(d, (3.5, 4.5)); text(d, (3.5, 5.0), "$a$")
    sw(d, (3.5, 4.5), (3.5, 2.3), "open", loc="top")
    d.add(elm.Resistor().endpoints((3.5, 2.3), (3.5, 0)).label(f"$R_2=3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((3.5, 4.5), (7.5, 4.5)).label(f"$R_3=2{OHM}$"))
    d.add(elm.Capacitor().endpoints((7.5, 4.5), (7.5, 0)).label("$0.5\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    arrow(d, (8.7, 3.6), (8.7, 2.2), "$i_C$", loc="bot")
    wire(d, (0, 0), (7.5, 0))
    dot(d, (3.5, 0))
    save(d, "d-rc")


def d_rl():
    d = new_drawing()
    isrc(d, (0, 0), (0, 4.5), "$6\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4.5), (10.5, 4.5))
    dot(d, (3, 4.5)); text(d, (3, 5.0), "$a$")
    d.add(elm.Resistor().endpoints((3, 4.5), (3, 0)).label(f"$R_1=3{OHM}$", loc="bot"))
    dot(d, (7, 4.5))
    sw(d, (7, 4.5), (7, 2.3), "close", loc="top")
    d.add(elm.Resistor().endpoints((7, 2.3), (7, 0)).label(f"$R_3=6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((10.5, 4.5), (10.5, 2.3)).label(f"$R_2=1{OHM}$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((10.5, 2.3), (10.5, 0)).label("$2\\,\\mathrm{H}$", loc="bot"))
    arrow(d, (9.8, 3.9), (9.8, 2.7), "$i_L$", loc="top")
    wire(d, (0, 0), (10.5, 0))
    dot(d, (3, 0)); dot(d, (7, 0))
    d.add(elm.Ground().at((1.5, 0)))
    save(d, "d-rl")


def d_74():
    """作业 7-4：两电感并联。"""
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$I_S$", loc="top")
    sw(d, (0, 4), (3, 4), "close")
    wire(d, (3, 4), (9, 4))
    d.add(elm.Inductor2(loops=4).endpoints((4.5, 4), (4.5, 0)).label("$L_1$", loc="bot"))
    d.add(elm.Inductor2(loops=4).endpoints((6.8, 4), (6.8, 0)).label("$L_2$", loc="bot"))
    d.add(elm.Resistor().endpoints((9, 4), (9, 0)).label("$R$", loc="bot"))
    arrow(d, (4.0, 3.8), (4.0, 2.7), "$i_1$", loc="top")
    arrow(d, (6.3, 3.8), (6.3, 2.7), "$i_2$", loc="top")
    wire(d, (0, 0), (9, 0))
    for x in (4.5, 6.8):
        dot(d, (x, 4)); dot(d, (x, 0))
    save(d, "d-74")


def d_75():
    """作业 7-5：S 闭合使两电容中点相连。"""
    d = new_drawing()
    vsrc(d, (0, 0), (0, 6), "$U_S$", loc="top")
    wire(d, (0, 6), (7, 6))
    wire(d, (0, 0), (7, 0))
    d.add(elm.Resistor().endpoints((3.5, 6), (3.5, 3)).label("$R_1$", loc="top"))
    d.add(elm.Capacitor().endpoints((3.5, 3), (3.5, 0)).label("$C_2$", loc="top")
          .label(("+", "$u_{C2}$", "−"), loc="bot"))
    d.add(elm.Capacitor().endpoints((7, 6), (7, 3)).label("$C_1$", loc="bot")
          .label(("+", "$u_{C1}$", "−"), loc="top"))
    d.add(elm.Resistor().endpoints((7, 3), (7, 0)).label("$R_2$", loc="bot"))
    sw(d, (3.5, 3), (7, 3), "close", loc="top")
    for p in ((3.5, 6), (3.5, 0), (3.5, 3), (7, 3)):
        dot(d, p)
    save(d, "d-75")


def d_710():
    """作业 7-10：受控源参数突变。"""
    d = new_drawing()
    isrc(d, (0, 0), (0, 4.5), "$I_S$", loc="top")
    wire(d, (0, 4.5), (3, 4.5))
    dot(d, (3, 4.5)); dot(d, (3, 0))
    d.add(elm.Resistor().endpoints((3, 4.5), (3, 2.25)).label(f"$1{OHM}$", loc="bot"))
    d.add(elm.SourceControlledV().endpoints((3, 0), (3, 2.25)).label("$\\beta i$", loc="bot"))
    d.add(elm.Resistor().endpoints((3, 4.5), (7, 4.5)).label(f"$1{OHM}$"))
    arrow(d, (4.2, 5.4), (5.8, 5.4), None)
    text(d, (5.0, 5.85), "$i$")
    dot(d, (7, 4.5)); dot(d, (7, 0))
    d.add(elm.Resistor().endpoints((7, 4.5), (7, 0)).label(f"$1{OHM}$", loc="bot"))
    wire(d, (7, 4.5), (10, 4.5))
    d.add(elm.Capacitor().endpoints((10, 4.5), (10, 0)).label("$1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u$", "−"), loc="bot"))
    wire(d, (0, 0), (10, 0))
    save(d, "d-710")


def d_712():
    """作业 7-12：S 打开后 CCVS 驱动右侧 RC。"""
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$u_S$", loc="top")
    arrow(d, (0.8, 2.0), (0.8, 3.4), "$i_1$", loc="bot")
    d.add(elm.Resistor().endpoints((0, 4.5), (3.5, 4.5)).label("$R_1$"))
    dot(d, (3.5, 4.5)); dot(d, (3.5, 0))
    d.add(elm.Capacitor().endpoints((3.5, 4.5), (3.5, 0)).label("$C_1$", loc="bot"))
    sw(d, (3.5, 4.5), (6.8, 4.5), "open", pol="$u_0$")
    dot(d, (6.8, 4.5)); dot(d, (6.8, 0))
    d.add(elm.SourceControlledV().endpoints((6.8, 0), (6.8, 4.5)).label("$ri_1$", loc="bot"))
    d.add(elm.Resistor().endpoints((6.8, 4.5), (10.3, 4.5)).label("$R_2$"))
    d.add(elm.Capacitor().endpoints((10.3, 4.5), (10.3, 0)).label("$C_2$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    wire(d, (0, 0), (10.3, 0))
    save(d, "d-712")


def d_728():
    """作业 7-28：S 打开后 CCCS 驱动右侧 RL。"""
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4.5), "$U_S$", loc="top")
    cur(d, (0, 4.5), (1.0, 4.5), "$i$")
    d.add(elm.Resistor().endpoints((1.0, 4.5), (3.8, 4.5)).label("$R$"))
    dot(d, (3.8, 4.5)); dot(d, (3.8, 0))
    d.add(elm.Capacitor().endpoints((3.8, 4.5), (3.8, 0)).label("$C$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    sw(d, (3.8, 4.5), (7, 4.5), "open", pol="$u_k$")
    dot(d, (7, 4.5)); dot(d, (7, 0))
    isrc(d, (7, 4.5), (7, 0), "$\\beta i$", loc="top", ctrl=True)
    d.add(elm.Resistor().endpoints((7, 4.5), (10.2, 4.5)).label("$R$"))
    dot(d, (10.2, 4.5)); dot(d, (10.2, 0))
    d.add(elm.Resistor().endpoints((10.2, 4.5), (10.2, 0)).label("$R$", loc="bot"))
    wire(d, (10.2, 4.5), (12.8, 4.5))
    d.add(elm.Inductor2(loops=4).endpoints((12.8, 4.5), (12.8, 0)).label("$L$", loc="bot"))
    arrow(d, (12.2, 4.0), (12.2, 2.8), "$i_L$", loc="top")
    wire(d, (0, 0), (12.8, 0))
    save(d, "d-728")


def d_rlc():
    d = new_drawing()
    d.add(elm.Capacitor().endpoints((0, 4), (0, 0)).label("$C=0.02\\,\\mathrm{F}$", loc="bot")
          .label(("+", "$u_C$", "−"), loc="top"))
    sw(d, (0, 4), (3, 4), "close")
    cur(d, (3, 4), (4, 4), "$i$")
    d.add(elm.Resistor().endpoints((4, 4), (7.5, 4)).label(f"$R=6{OHM}$"))
    d.add(elm.Inductor2(loops=4).endpoints((7.5, 4), (7.5, 0)).label("$L=0.5\\,\\mathrm{H}$", loc="bot"))
    wire(d, (0, 0), (7.5, 0))
    save(d, "d-rlc")


if __name__ == "__main__":
    d_73(); d_rc(); d_rl(); d_74(); d_75(); d_710(); d_712(); d_728(); d_rlc()
