"""习题·电路的一般分析方法 解析插图（images/ex/sol/a-*）。数值见 verify_analysis.py。"""
from solcommon import (elm, new_drawing, ssave, dot, text, note, cur, arrow, vsrc, isrc, wire,
                       OHM, C1, C2, MUTED)


def val(d, xy, s, **kw):
    text(d, xy, s, color=C1, **kw)


def dashed(d, pts, color=C2):
    for p, q in zip(pts, pts[1:]):
        d.add(elm.Line().endpoints(p, q).color(color).linestyle("--").linewidth(1.3))


# ------------------------------------------------------------------ 题3 超网孔
def a_supermesh_super():
    d = new_drawing()
    v = vsrc(d, (0, 0), (0, 4), "$28\\,\\mathrm{V}$", loc="bot")
    r1 = d.add(elm.Resistor().endpoints((0, 4), (4.5, 4)).label(f"$4{OHM}$", loc="bot"))
    s = isrc(d, (4.5, 0), (4.5, 4), "$2\\,\\mathrm{A}$", loc="top")
    r2 = d.add(elm.Resistor().endpoints((4.5, 4), (9, 4)).label(f"$2{OHM}$", loc="bot"))
    r3 = d.add(elm.Resistor().endpoints((9, 4), (9, 0)).label(f"$6{OHM}$", loc="top"))
    wire(d, (0, 0), (9, 0))
    dot(d, (4.5, 4)); dot(d, (4.5, 0))
    text(d, (5.15, 3.2), "$+$"); text(d, (5.95, 2.0), "$U=24\\,\\mathrm{V}$", halign="left"); text(d, (5.15, 0.8), "$-$")
    val(d, (2.2, 0.9), "$I_1=1\\,\\mathrm{A}$")
    val(d, (7.2, 0.9), "$I_2=3\\,\\mathrm{A}$")
    # 超网孔：沿外圈顺时针（绕开电流源）
    dashed(d, [(-0.6, -0.6), (-0.6, 4.6), (9.6, 4.6), (9.6, -0.6), (-0.6, -0.6)])
    arrow(d, (3.0, 5.0), (5.5, 5.0), None)
    text(d, (4.25, 5.55), "超网孔（顺时针）", color=C2, fontsize=12)
    note(d, (4.5, -1.3), "$28=4I_1+2I_2+6I_2$，再加约束 $I_2-I_1=2$")
    ssave(d, "a-supermesh-super")


# ------------------------------------------------------------------ 题5 超节点
def a_supernode_sn():
    d = new_drawing()
    isrc(d, (0, 0), (0, 4), "$6\\,\\mathrm{A}$", loc="top")
    wire(d, (0, 4), (2.5, 4))
    dot(d, (2.5, 4)); text(d, (2.5, 4.55), "$a$")
    d.add(elm.Resistor().endpoints((2.5, 4), (2.5, 0)).label(f"$4{OHM}$", loc="bot"))
    wire(d, (2.5, 4), (3.5, 4))
    e = elm.Source().endpoints((3.5, 4), (6, 4))
    e.label("$8\\,\\mathrm{V}$", loc="top")
    e.label(("−", "", "+"), loc="bot", ofst=0.15)
    d.add(e)
    wire(d, (6, 4), (7, 4))
    dot(d, (7, 4)); text(d, (7, 4.55), "$b$")
    d.add(elm.Resistor().endpoints((7, 4), (7, 0)).label(f"$4{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((7, 4), (10.5, 4)).label(f"$2{OHM}$"))
    text(d, (10.5, 4.55), "$c$")
    vsrc(d, (10.5, 0), (10.5, 4), "$24\\,\\mathrm{V}$", loc="bot")
    wire(d, (0, 0), (10.5, 0))
    dot(d, (2.5, 0)); dot(d, (7, 0))
    d.add(elm.Ground().at((5, 0)))
    dashed(d, [(1.9, 3.0), (1.9, 5.4), (7.6, 5.4), (7.6, 3.0), (1.9, 3.0)])
    text(d, (4.75, 5.8), "超节点", color=C2, fontsize=12)
    val(d, (1.1, 4.55), "$U_a=12$")
    val(d, (8.6, 3.4), "$U_b=20$")
    val(d, (11.6, 4.55), "$U_c=24$")
    arrow(d, (3.9, 2.5), (5.6, 2.5), None); val(d, (4.75, 1.95), "$i_{ab}=3\\,\\mathrm{A}$")
    note(d, (5.25, -1.0), "电位单位 V，接地点为参考")
    ssave(d, "a-supernode-sn")


# ------------------------------------------------------------------ 题7 二极管
def _diode_case(d, U2, d2_on, Uo, I1, I2):
    o = 6
    vsrc(d, (0, 0), (0, 4), "$6\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (2.8, 4)).label("$1\\,\\mathrm{k}\\Omega$"))
    wire(d, (2.8, 4), (o, 4))
    note(d, (4.4, 3.45), "$D_1$ 导通→短路")
    arrow(d, (3.6, 4.6), (5.2, 4.6)); val(d, (4.4, 5.15), f"$I_{{D1}}={I1}$")
    dot(d, (o, 4)); text(d, (o, 4.6), "$o$")
    if d2_on:
        wire(d, (9.2, 4), (o, 4))
        note(d, (7.6, 3.45), "$D_2$ 导通→短路")
        arrow(d, (8.4, 4.6), (6.8, 4.6)); val(d, (7.6, 5.15), f"$I_{{D2}}={I2}$")
    else:
        wire(d, (o, 4), (7.0, 4)); wire(d, (8.2, 4), (9.2, 4))
        dot(d, (7.0, 4), True); dot(d, (8.2, 4), True)
        note(d, (7.6, 3.45), "$D_2$ 截止→开路")
        val(d, (7.6, 5.15), "$I_{D2}=0$")
    d.add(elm.Resistor().endpoints((12, 4), (9.2, 4)).label("$1\\,\\mathrm{k}\\Omega$"))
    vsrc(d, (12, 0), (12, 4), f"$U_2={U2}\\,\\mathrm{{V}}$", loc="bot")
    d.add(elm.Resistor().endpoints((o, 4), (o, 0)).label("$2\\,\\mathrm{k}\\Omega$", loc="bot")
          .label(("+", "", "−"), loc="top"))
    val(d, (4.9, 1.9), f"$U_o={Uo}\\,\\mathrm{{V}}$", halign="right")
    wire(d, (0, 0), (12, 0))
    dot(d, (o, 0))
    d.add(elm.Ground().at((o, 0)))


def a_diode_1():
    d = new_drawing()
    _diode_case(d, 2, False, 4, "2\\,\\mathrm{mA}", None)
    note(d, (6, -1.2), "$u_{D2}=U_2-U_o=2-4=-2\\,\\mathrm{V}\\leq0$，截止成立")
    ssave(d, "a-diode-1")


def a_diode_2():
    d = new_drawing()
    _diode_case(d, 5, True, 4.4, "1.6\\,\\mathrm{mA}", "0.6\\,\\mathrm{mA}")
    note(d, (6, -1.2), "两管电流都为正，假设成立")
    ssave(d, "a-diode-2")


# ------------------------------------------------------------------ 题8 指定的树
def a_tree_tree():
    d = new_drawing()
    yt, ym, yb = 6, 2.5, 0
    TREE = dict(color=C1, lw=2.6)

    def R(p, q, lab, tree, loc="top"):
        e = elm.Resistor().endpoints(p, q).label(lab, loc=loc)
        if tree:
            e.color(C1).linewidth(2.6)
        else:
            e.color(MUTED).linestyle("--")
        d.add(e)

    def W(p, q, tree=None):
        e = elm.Line().endpoints(p, q)
        if tree is True:
            e.color(C1).linewidth(2.6)
        elif tree is False:
            e.color(MUTED).linestyle("--")
        d.add(e)

    W((0, yb), (0, yt))                                     # 节点 L（竖线）
    R((0, yt), (4, yt), "$R_4$", True)
    R((4, yt), (7.5, yt), "$R_6$", False); W((7.5, yt), (8.5, yt), False)
    R((8.5, yt), (12, yt), "$R_5$", True); W((12, yt), (12, ym), True)
    R((0, ym), (4, ym), "$R_1$", True, loc="bot")
    R((4, ym), (8.5, ym), "$R_3$", True, loc="bot")
    R((8.5, ym), (12, ym), "$R_2$", True, loc="bot")
    for x, lab in ((4, "$I_{S4}$"), (8.5, "$I_{S5}$")):
        d.add(elm.SourceI().endpoints((x, ym), (x, yt)).label(lab, loc="top").color(MUTED).linestyle("--"))
    W((12, yb), (12, ym), False)
    R((0, yb), (12, yb), "$R_7$", False, loc="bot")
    arrow(d, (12.7, 0.6), (12.7, 1.9), "$I_7$", loc="bot")
    arrow(d, (7.6, yt + 0.55), (8.8, yt + 0.55), "$I_6$", loc="top")
    for p in ((0, ym), (4, yt), (8.5, yt), (4, ym), (8.5, ym), (12, ym)):
        dot(d, p)
    text(d, (-0.55, ym + 0.45), "$L$"); text(d, (12.5, ym + 0.45), "$Q$")
    text(d, (6, -1.6), "实线（蓝）：树支 $R_1\\sim R_5$　虚线（灰）：连支 $R_6$、$R_7$、$I_{S4}$、$I_{S5}$",
         color=MUTED, fontsize=12)
    ssave(d, "a-tree-tree")


if __name__ == "__main__":
    a_supermesh_super(); a_supernode_sn(); a_diode_1(); a_diode_2(); a_tree_tree()
