"""习题·电阻电路的等效变换 插图（前缀 e-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, vsrc_h, arrow, vsrc, isrc, wire, OHM


def term(d, xy, name, dx=-0.45, dy=0.0):
    dot(d, xy, True)
    text(d, (xy[0] + dx, xy[1] + dy), f"${name}$")


def e_series():
    """串并联：底边 5Ω 被下方导线短接。"""
    d = new_drawing()
    term(d, (0, 5), "a"); term(d, (0, 0), "b")
    d.add(elm.Resistor().endpoints((0, 5), (4, 5)).label(f"$4{OHM}$"))
    d.add(elm.Resistor().endpoints((4, 5), (7.5, 5)).label(f"$2{OHM}$"))
    wire(d, (7.5, 5), (10.5, 5))
    d.add(elm.Resistor().endpoints((4, 5), (4, 0)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7.5, 5), (7.5, 0)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((10.5, 5), (10.5, 0)).label(f"$6{OHM}$", loc="bot"))
    wire(d, (0, 0), (4, 0))
    d.add(elm.Resistor().endpoints((4, 0), (7.5, 0)).label(f"$5{OHM}$", loc="top"))
    wire(d, (7.5, 0), (10.5, 0))
    wire(d, (4, 0), (4, -1.3), (7.5, -1.3), (7.5, 0))
    for p in ((4, 5), (7.5, 5), (4, 0), (7.5, 0)):
        dot(d, p)
    text(d, (4, 5.55), "$c$"); text(d, (7.5, 5.55), "$d$")
    save(d, "e-series")


def _bridge(d, vals, cd_loc="bot"):
    """矩形画法的桥：a 左、b 右，上 c、下 d。vals=(ac, cb, ad, db, cd)。"""
    ac, cb, ad, db, cd = vals
    wire(d, (0, 0), (0, 5)); wire(d, (9, 0), (9, 5))
    d.add(elm.Resistor().endpoints((0, 5), (4.5, 5)).label(f"${ac}{OHM}$"))
    d.add(elm.Resistor().endpoints((4.5, 5), (9, 5)).label(f"${cb}{OHM}$"))
    d.add(elm.Resistor().endpoints((0, 0), (4.5, 0)).label(f"${ad}{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((4.5, 0), (9, 0)).label(f"${db}{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 0)).label(f"${cd}{OHM}$", loc=cd_loc))
    dot(d, (4.5, 5)); dot(d, (4.5, 0))
    text(d, (4.5, 5.6), "$c$"); text(d, (4.5, -0.65), "$d$")
    wire(d, (-1.6, 2.5), (0, 2.5)); wire(d, (9, 2.5), (10.6, 2.5))
    dot(d, (0, 2.5)); dot(d, (9, 2.5))
    term(d, (-1.6, 2.5), "a"); term(d, (10.6, 2.5), "b", dx=0.45)


def e_bridge():
    d = new_drawing()
    _bridge(d, (3, 6, 4, 8, 10))
    save(d, "e-bridge")


def e_ydelta():
    d = new_drawing()
    _bridge(d, (6, 4, 6, 10, 6), cd_loc="top")
    arrow(d, (5.3, 3.2), (5.3, 1.8), "$I_{cd}$", loc="bot")
    save(d, "e-ydelta")


def e_sym():
    """作业 4-47：左右对称。"""
    d = new_drawing()
    L, M, Rt = (2, 5), (5.5, 5), (9, 5)
    wire(d, (0, 5), L)
    wire(d, Rt, (11, 5))
    d.add(elm.Resistor().endpoints(L, M).label(f"$1{OHM}$"))
    d.add(elm.Resistor().endpoints(M, Rt).label(f"$1{OHM}$"))
    wire(d, L, (2, 7.2))
    d.add(elm.Resistor().endpoints((2, 7.2), (9, 7.2)).label(f"$7{OHM}$"))
    wire(d, (9, 7.2), Rt)
    d.add(elm.Resistor().endpoints((0, 5), (0, 0)).label(f"$3{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints(L, (2, 0)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints(Rt, (9, 0)).label(f"$6{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((11, 5), (11, 0)).label(f"$3{OHM}$", loc="bot"))
    wire(d, (0, 0), (2, 0))
    d.add(elm.Resistor().endpoints((2, 0), (5.5, 0)).label(f"$1{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((5.5, 0), (9, 0)).label(f"$1{OHM}$", loc="bot"))
    wire(d, (9, 0), (11, 0))
    d.add(elm.Resistor().endpoints(M, (5.5, 2.6)).label(f"$1{OHM}$", loc="bot"))
    vsrc(d, (5.5, 0), (5.5, 2.6), "$6\\,\\mathrm{V}$", loc="bot")
    arrow(d, (4.8, 3.3), (4.8, 4.5), "$I$", loc="top")
    for p in (L, M, Rt, (2, 0), (5.5, 0), (9, 0)):
        dot(d, p)
    save(d, "e-sym")


def e_bridge_is():
    """作业 4-5。"""
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$5\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4), (2.5, 4)); wire(d, (0, 0), (12, 0))
    term(d, (1.2, 4), "a", dx=0, dy=0.45); term(d, (1.2, 0), "b", dx=0, dy=-0.45)
    d.add(elm.Gap().endpoints((1.2, 3.6), (1.2, 0.4)).label(("+", "$U_{ab}$", "−"), loc="bot"))
    wire(d, (2.5, 2.5), (2.5, 5.5)); wire(d, (10, 2.5), (10, 5.5))
    dot(d, (2.5, 4)); dot(d, (10, 4))
    d.add(elm.Resistor().endpoints((2.5, 5.5), (6.2, 5.5)).label(f"$4{OHM}$"))
    d.add(elm.Resistor().endpoints((6.2, 5.5), (10, 5.5)).label(f"$10{OHM}$"))
    d.add(elm.Resistor().endpoints((2.5, 2.5), (6.2, 2.5)).label(f"$6{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((6.2, 2.5), (10, 2.5)).label(f"$5{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((6.2, 5.5), (6.2, 2.5)).label(f"$10{OHM}$", loc="top")
          .label(("+", "$U$", "−"), loc="bot"))
    dot(d, (6.2, 5.5)); dot(d, (6.2, 2.5))
    wire(d, (10, 4), (12, 4))
    d.add(elm.Resistor().endpoints((12, 4), (12, 0)).label(f"$24{OHM}$", loc="bot"))
    save(d, "e-bridge-is")


def e_source():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 2.5), "$12\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 2.5), (0, 5)).label(f"$6{OHM}$", loc="top"))
    isrc(d, (3.2, 0), (3.2, 2.5), "$3\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((3.2, 2.5), (3.2, 5)).label(f"$4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((6.2, 5), (6.2, 0)).label(f"$3{OHM}$", loc="bot"))
    wire(d, (0, 5), (6.2, 5))
    d.add(elm.Resistor().endpoints((6.2, 5), (9.5, 5)).label(f"$2{OHM}$"))
    wire(d, (9.5, 5), (10.5, 5))
    wire(d, (0, 0), (10.5, 0))
    for p in ((3.2, 5), (6.2, 5), (3.2, 0), (6.2, 0)):
        dot(d, p)
    text(d, (6.2, 5.55), "$t$")
    term(d, (10.5, 5), "a", dx=0.45); term(d, (10.5, 0), "b", dx=0.45)
    save(d, "e-source")


def e_rin():
    d = new_drawing()
    term(d, (0, 4), "a"); term(d, (0, 0), "b")
    cur(d, (0, 4), (1.2, 4), "$i$")
    wire(d, (1.2, 4), (2.5, 4))
    d.add(elm.Gap().endpoints((0, 3.6), (0, 0.4)).label(("+", "$u$", "−"), loc="bot", ofst=0.2))
    d.add(elm.Resistor().endpoints((2.5, 4), (2.5, 0)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((2.5, 4), (6, 4)).label(f"$1{OHM}$"))
    d.add(elm.Resistor().endpoints((6, 4), (6, 0)).label(f"$4{OHM}$", loc="top"))
    arrow(d, (6.7, 2.9), (6.7, 1.3), "$i_1$", loc="bot")
    wire(d, (6, 4), (9.5, 4))
    isrc(d, (9.5, 0), (9.5, 4), "$3i_1$", loc="bot", ctrl=True)
    wire(d, (0, 0), (9.5, 0))
    for p in ((2.5, 4), (2.5, 0), (6, 4), (6, 0)):
        dot(d, p)
    text(d, (6, 4.55), "$x$")
    save(d, "e-rin")


if __name__ == "__main__":
    e_series()
    e_bridge()
    e_ydelta()
    e_sym()
    e_bridge_is()
    e_source()
    e_rin()
