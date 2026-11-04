"""习题·基本概念与定律 解析插图（images/ex/sol/b-*）。数值见 verify_basics.py。
电路结构与 fig_basics.py 中的题图完全相同，只把求得的量（蓝色）标上去。"""
from solcommon import (elm, new_drawing, ssave, dot, text, note, cur, arrow, vsrc, isrc, wire,
                       OHM, C1, MUTED)
from excommon import vsrc_h


def val(d, xy, s, **kw):
    text(d, xy, s, color=C1, **kw)


def ground(d, xy):
    d.add(elm.Ground().at(xy))


# ------------------------------------------------------------------ 题3 并联电源
def b_sources_sol():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 5), "$10\\,\\mathrm{V}$", loc="top")
    wire(d, (0, 5), (8, 5))
    d.add(elm.Resistor().endpoints((4, 5), (4, 0)).label(f"$2{OHM}$", loc="bot"))
    isrc(d, (8, 0), (8, 2.5), "$3\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((8, 2.5), (8, 5)).label(f"$4{OHM}$", loc="bot"))
    dot(d, (8, 2.5)); text(d, (7.5, 2.5), "$m$")
    wire(d, (0, 0), (8, 0))
    dot(d, (4, 5)); dot(d, (4, 0))
    arrow(d, (0.8, 3.0), (0.8, 4.4), None); val(d, (1.75, 3.7), "$I=2\\,\\mathrm{A}$")
    arrow(d, (3.3, 3.2), (3.3, 1.8), None); val(d, (2.7, 2.5), "$5\\,\\mathrm{A}$")
    arrow(d, (7.2, 3.3), (7.2, 4.5), None); val(d, (6.6, 4.3), "$3\\,\\mathrm{A}$")
    val(d, (6.75, 1.9), "$V_m=22\\,\\mathrm{V}$")
    note(d, (2.0, 5.5), "$V=10\\,\\mathrm{V}$")
    ground(d, (2.0, 0))
    ssave(d, "b-sources-sol")


# ------------------------------------------------------------------ 题4 直流稳态
def b_lc_dc_dc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$2{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$a$")
    wire(d, (3.5, 4), (3.5, 3.1)); wire(d, (3.5, 0.9), (3.5, 0))
    dot(d, (3.5, 3.1), True); dot(d, (3.5, 0.9), True)
    text(d, (3.75, 2.7), "+"); text(d, (3.75, 1.3), "−")
    text(d, (4.0, 2.0), "$u_C=8\\,\\mathrm{V}$", halign="left")
    note(d, (3.6, 2.0), "$C$ 开路", halign="right")
    d.add(elm.Line().endpoints((3.5, 4), (7.5, 4)).label("$L$ 短路", loc="top", color=MUTED, fontsize=12))
    arrow(d, (4.6, 3.35), (6.4, 3.35), "$i_L=2\\,\\mathrm{A}$", loc="bot")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$4{OHM}$", loc="bot"))
    wire(d, (0, 0), (7.5, 0))
    dot(d, (3.5, 0))
    ssave(d, "b-lc-dc-dc")


# ------------------------------------------------------------------ 题5 KCL（作业 2-4）
def b_kcl_sol():
    d = new_drawing()
    n3, n4, n1, n2, n5, n6 = (0, 4), (4, 4), (8, 4), (8, 8), (4, 0), (8, 0)
    wire(d, n3, (0, 8), (1.5, 8))
    d.add(elm.Resistor().endpoints((1.5, 8), (5.5, 8)))
    wire(d, (5.5, 8), n2, (11, 8))
    arrow(d, (2.6, 8.7), (4.4, 8.7), None); val(d, (3.5, 9.25), "$I_2=4\\,\\mathrm{A}$")
    d.add(elm.Resistor().endpoints(n2, n1))
    arrow(d, (8.7, 5.4), (8.7, 6.8), None); val(d, (9.9, 6.1), "$I_1=-3\\,\\mathrm{A}$")
    d.add(elm.Resistor().endpoints((11, 8), (11, 0)))
    arrow(d, (11.7, 4.7), (11.7, 3.3), "$1\\,\\mathrm{A}$", loc="bot")
    wire(d, (11, 0), n6)
    d.add(elm.Resistor().endpoints(n3, n4))
    arrow(d, (2.7, 4.7), (1.3, 4.7), "$1\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints(n4, n1))
    arrow(d, (5.3, 4.7), (6.7, 4.7), "$2\\,\\mathrm{A}$", loc="top")
    d.add(elm.Resistor().endpoints(n4, n5))
    arrow(d, (4.7, 2.7), (4.7, 1.3), None); val(d, (3.55, 2.0), "$I_5=-3\\,\\mathrm{A}$", halign="right")
    d.add(elm.Resistor().endpoints((0, 0), n3))
    arrow(d, (-0.7, 1.3), (-0.7, 2.7), "$3\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 0), n5)
    d.add(elm.Resistor().endpoints(n5, n6))
    arrow(d, (5.3, -0.7), (6.7, -0.7), None); val(d, (6.0, -1.25), "$I_6=-6\\,\\mathrm{A}$")
    vsrc(d, n1, n6, "$U_S$", loc="bot")
    arrow(d, (7.3, 1.3), (7.3, 2.7), None); val(d, (7.1, 2.0), "$I_7=-5\\,\\mathrm{A}$", halign="right")
    for p in (n3, n4, n1, n2, n5, n6):
        dot(d, p)
    text(d, (-0.55, 4.45), "③"); text(d, (4, 4.6), "④"); text(d, (8.55, 4.45), "①")
    text(d, (8, 8.6), "②"); text(d, (4, -0.6), "⑤"); text(d, (8.55, -0.45), "⑥")
    note(d, (5.5, -2.1), "求解顺序：③ → ④ → ⑤ → ⑥ → ①，节点 ② 用来校验")
    ssave(d, "b-kcl-sol")


# ------------------------------------------------------------------ 题6 KVL（作业 2-5）
def b_kvl_pot():
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
    for p in (n3, n4, n1, n2, n5, (8, 0)):
        dot(d, p)
    text(d, (-0.55, 4.45), "③"); text(d, (4, 4.6), "④"); text(d, (8.55, 4.45), "①")
    text(d, (8, 8.6), "②"); text(d, (4, -0.6), "⑤")
    val(d, (-0.9, 3.55), "$V_3=11$")
    val(d, (3.15, 3.45), "$V_4=8$")
    val(d, (9.0, 3.45), "$V_1=-6$")
    val(d, (9.4, 8.6), "$V_2=-8$")
    val(d, (5.6, -0.6), "$V_5=0$")
    ground(d, (2.0, 0))
    note(d, (5.5, -1.8), "以节点 ⑤（整条下边线）为参考，电位单位 V")
    ssave(d, "b-kvl-pot")


# ------------------------------------------------------------------ 题7 电位（作业 2-9）
def b_potential_sol():
    d = new_drawing()
    L, b, a = (0, 4), (5, 4), (5, 7.5)
    wire(d, L, (0, 7.5), (0.5, 7.5))
    d.add(elm.Resistor().endpoints((0.5, 7.5), (4, 7.5)).label(f"$2{OHM}$"))
    wire(d, (4, 7.5), a, (5.5, 7.5))
    d.add(elm.Resistor().endpoints((5.5, 7.5), (9, 7.5)).label(f"$6{OHM}$"))
    wire(d, (9, 7.5), (9, 4))
    dot(d, a); text(d, (5, 8.05), "$a$")
    arrow(d, (6.4, 8.5), (8.0, 8.5), None); val(d, (7.2, 9.0), "$I_t=-2\\,\\mathrm{A}$")
    wire(d, L, (1.6, 4))
    cur(d, (3.0, 4), (1.6, 4), "$I_2$")
    vsrc_h(d, (3.0, 4), (4.6, 4), "$3\\,\\mathrm{V}$")
    wire(d, (4.6, 4), b, (5.6, 4))
    d.add(elm.Resistor().endpoints((5.6, 4), (8.6, 4)).label(f"$5{OHM}$"))
    wire(d, (8.6, 4), (9, 4))
    dot(d, b); text(d, (5.45, 3.55), "$b$")
    d.add(elm.Resistor().endpoints(L, (0, 0)).label(f"$2{OHM}$", loc="top"))
    arrow(d, (-0.7, 3.5), (-0.7, 2.3), "$I_1$", loc="top")
    isrc(d, (1.6, 0), (1.6, 4), "$1\\,\\mathrm{A}$", loc="bot")
    vsrc(d, b, (5, 0), "$5\\,\\mathrm{V}$", loc="bot")
    vsrc(d, (9, 0), (9, 4), "$14\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (9, 0))
    for p in (L, (1.6, 4), (1.6, 0), (5, 0), (9, 4)):
        dot(d, p)
    ground(d, (3.3, 0))
    val(d, (-1.2, 4.45), "$V_L=-2$")
    val(d, (6.6, 3.1), "$V_b=-5$")
    val(d, (10.2, 4.45), "$V_R=14$")
    val(d, (5.0, 6.85), "$V_a=2$")
    note(d, (4.5, -1.2), "以下边线为参考点，电位单位 V")
    ssave(d, "b-potential-sol")


if __name__ == "__main__":
    b_sources_sol(); b_lc_dc_dc(); b_kcl_sol(); b_kvl_pot(); b_potential_sol()
