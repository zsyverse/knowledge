"""习题·电路定理 解析插图（images/ex/sol/t-*）。数值见 verify_theorems.py 与页面解析。"""
from solcommon import (elm, new_drawing, ssave, dot, text, note, cur, arrow, vsrc, isrc, wire, OHM, MUTED, C2)
from excommon import vsrc_h


def zeroed_v(d, p, q, side_xy):
    """电压源置零 → 短路线。"""
    wire(d, p, q)
    note(d, side_xy, "电压源\n短路", halign="right")


# ------------------------------------------------------------------ 题2 叠加
def _super_body(d):
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$6{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$3{OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$2{OHM}$"))
    dot(d, (7.5, 4)); text(d, (7.5, 4.5), "$b$")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$4{OHM}$", loc="top"))
    dot(d, (3.5, 0)); dot(d, (7.5, 0))


def t_super_1():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$")
    _super_body(d)
    arrow(d, (4.2, 2.8), (4.2, 1.4), "$I'=1\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (7.5, 0))
    note(d, (9.3, 2.0), "$3\\,\\mathrm{A}$ 开路\n（支路去掉）")
    text(d, (4.5, -0.9), "$U_a'=12\\times\\frac{2}{6+2}=3\\,\\mathrm{V}$")
    ssave(d, "t-super-1")


def t_super_2():
    d = new_drawing()
    zeroed_v(d, (0, 0), (0, 4), (-0.3, 2.0))
    _super_body(d)
    arrow(d, (4.2, 2.8), (4.2, 1.4), "$I''=1\\,\\mathrm{A}$", loc="bot")
    arrow(d, (6.4, 3.3), (4.8, 3.3), "$1.5\\,\\mathrm{A}$", loc="bot")
    arrow(d, (8.2, 2.8), (8.2, 1.4), "$1.5\\,\\mathrm{A}$", loc="bot")
    wire(d, (7.5, 4), (10.8, 4))
    isrc(d, (10.8, 0), (10.8, 4), "$3\\,\\mathrm{A}$", loc="bot")
    wire(d, (0, 0), (10.8, 0))
    ssave(d, "t-super-2")


# ------------------------------------------------------------------ 题3 含 CCVS 的叠加
def _ccvs_body(d, lab_i, ctrl):
    d.add(elm.Resistor().endpoints((0, 5), (3.2, 5)).label(f"$2{OHM}$"))
    cur(d, (3.2, 5), (4.5, 5), lab_i)
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$a$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 2.5)).label(f"$4{OHM}$", loc="top"))
    vsrc(d, (4.5, 0), (4.5, 2.5), ctrl, loc="top", ctrl=True)
    dot(d, (4.5, 0))


def t_super_ccvs_1():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 5), "$10\\,\\mathrm{V}$")
    _ccvs_body(d, "$i'$", "$2i'$")
    d.add(elm.Gap().endpoints((5.6, 4.6), (5.6, 0.4)).label(("+", "$U'$", "−"), loc="bot"))
    wire(d, (4.5, 5), (6.6, 5), (6.6, 4.4)); wire(d, (6.6, 0.6), (6.6, 0), (0, 0))
    dot(d, (6.6, 4.4), True); dot(d, (6.6, 0.6), True)
    note(d, (8.0, 2.5), "$3\\,\\mathrm{A}$\n开路")
    text(d, (3.3, -1.0), "$i'=1.25\\,\\mathrm{A},\\ U'=6i'=7.5\\,\\mathrm{V}$")
    ssave(d, "t-super-ccvs-1")


def t_super_ccvs_2():
    d = new_drawing()
    zeroed_v(d, (0, 0), (0, 5), (-0.3, 2.5))
    _ccvs_body(d, "$i''$", "$2i''$")
    d.add(elm.Gap().endpoints((7.0, 4.6), (7.0, 0.4)).label(("+", "$U''$", "−"), loc="bot"))
    wire(d, (4.5, 5), (9.2, 5))
    isrc(d, (9.2, 0), (9.2, 5), "$3\\,\\mathrm{A}$", loc="bot")
    arrow(d, (5.2, 4.3), (5.2, 3.0), "$i''+3$", loc="bot")
    wire(d, (0, 0), (9.2, 0))
    text(d, (4.2, -1.0), "$i''=-1.5\\,\\mathrm{A},\\ 2i''=-3\\,\\mathrm{V},\\ U''=3\\,\\mathrm{V}$")
    ssave(d, "t-super-ccvs-2")


# ------------------------------------------------------------------ 题5 戴维南
def t_thev_uoc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$24\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$4{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$12{OHM}$", loc="top"))
    note(d, (2.0, 0.6), "$V_c=24\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$6{OHM}$"))
    arrow(d, (6.3, 3.4), (4.7, 3.4), "$2\\,\\mathrm{A}$", loc="bot")
    isrc(d, (7.5, 0), (7.5, 4), "$2\\,\\mathrm{A}$", loc="top")
    wire(d, (7.5, 4), (9.5, 4)); wire(d, (0, 0), (9.5, 0))
    dot(d, (3.5, 0)); dot(d, (7.5, 4)); dot(d, (7.5, 0))
    dot(d, (9.5, 4), True); dot(d, (9.5, 0), True)
    text(d, (9.5, 4.5), "$a$"); text(d, (9.5, -0.5), "$b$")
    d.add(elm.Gap().endpoints((9.5, 4), (9.5, 0)).label(("+", "$U_{oc}=36\\,\\mathrm{V}$", "−"), loc="bot"))
    ssave(d, "t-thevenin-uoc")


def t_thev_req():
    d = new_drawing()
    zeroed_v(d, (0, 0), (0, 4), (-0.3, 2.0))
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$4{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$12{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$6{OHM}$"))
    note(d, (6.0, 2.0), "电流源开路")
    wire(d, (0, 0), (7.5, 0)); dot(d, (3.5, 0))
    dot(d, (7.5, 4), True); dot(d, (7.5, 0), True)
    text(d, (7.5, 4.5), "$a$"); text(d, (7.5, -0.5), "$b$")
    arrow(d, (9.0, 2.0), (7.8, 2.0), None)
    text(d, (9.2, 2.0), "$R_{eq}=6+4\\parallel12=9\\,\\Omega$", halign="left")
    ssave(d, "t-thevenin-req")


def t_thev_eq():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$36\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$R_{{eq}}=9{OHM}$"))
    dot(d, (3.5, 4), True); dot(d, (3.5, 0), True)
    text(d, (3.5, 4.5), "$a$"); text(d, (3.5, -0.5), "$b$")
    cur(d, (3.5, 4), (6, 4), "$I=3\\,\\mathrm{A}$")
    d.add(elm.Resistor().endpoints((6, 4), (6, 0)).label(f"$R_L=3{OHM}$", loc="bot"))
    wire(d, (0, 0), (6, 0))
    ssave(d, "t-thevenin-eq")


# ------------------------------------------------------------------ 题6 诺顿
def t_norton_isc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$18\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$3{OHM}$"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$6{OHM}$", loc="top"))
    note(d, (2.0, 0.6), "$V_c=6\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$2{OHM}$"))
    arrow(d, (4.7, 3.4), (6.3, 3.4), "$3\\,\\mathrm{A}$", loc="bot")
    isrc(d, (7.5, 4), (7.5, 0), "$1\\,\\mathrm{A}$", loc="top")
    wire(d, (7.5, 4), (10, 4)); wire(d, (0, 0), (10, 0))
    dot(d, (3.5, 0)); dot(d, (7.5, 4)); dot(d, (7.5, 0))
    dot(d, (10, 4)); dot(d, (10, 0))
    text(d, (10.45, 4), "$a$"); text(d, (10.45, 0), "$b$")
    d.add(elm.Line().endpoints((10, 4), (10, 0)).color(C2))
    arrow(d, (10.6, 2.8), (10.6, 1.2), "$I_{sc}=3-1=2\\,\\mathrm{A}$", loc="bot")
    ssave(d, "t-norton-isc")


# ------------------------------------------------------------------ 题7 含 CCVS 的戴维南
def _ccvs_left(d, src=True):
    if src:
        vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$")
    else:
        zeroed_v(d, (0, 0), (0, 4), (-0.3, 2.0))
    d.add(elm.Resistor().endpoints((0, 4), (3.2, 4)).label(f"$4{OHM}$"))
    cur(d, (3.2, 4), (4.5, 4), "$i_1$")
    dot(d, (4.5, 4)); text(d, (4.5, 4.5), "$c$")
    d.add(elm.Resistor().endpoints((4.5, 4), (4.5, 0)).label(f"$4{OHM}$", loc="top"))
    wire(d, (4.5, 4), (5.5, 4))
    vsrc_h(d, (8.5, 4), (5.5, 4), "$2i_1$", ctrl=True)
    dot(d, (4.5, 0))


def t_ccvs_isc():
    d = new_drawing()
    _ccvs_left(d)
    wire(d, (8.5, 4), (10, 4)); wire(d, (0, 0), (10, 0))
    dot(d, (10, 4)); dot(d, (10, 0))
    text(d, (10.45, 4), "$a$"); text(d, (10.45, 0), "$b$")
    d.add(elm.Line().endpoints((10, 4), (10, 0)).color(C2))
    arrow(d, (10.6, 2.8), (10.6, 1.2), "$I_{sc}=9\\,\\mathrm{A}$", loc="bot")
    note(d, (5.0, -0.9), "$V_a=0$：$V_c=-2i_1=-12\\,\\mathrm{V}$，$i_1=6\\,\\mathrm{A}$")
    ssave(d, "t-ccvs-isc")


def t_ccvs_test():
    d = new_drawing()
    _ccvs_left(d, src=False)
    wire(d, (8.5, 4), (9.5, 4)); wire(d, (0, 0), (11.5, 0))
    dot(d, (9.5, 4), True); text(d, (9.5, 4.5), "$a$")
    cur(d, (11.5, 4), (9.5, 4), "$i$", frac=0.5)
    vsrc(d, (11.5, 0), (11.5, 4), "$u$", loc="bot")
    note(d, (5.0, -0.9), "$V_c=2u,\\ i_1=-u/2\\ \\Rightarrow\\ i=u,\\ R_{eq}=1\\,\\Omega$")
    ssave(d, "t-ccvs-test")


# ------------------------------------------------------------------ 题8 作业 4-36（S 闭合）
def t_436_closed():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$10\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$R_1=2{OHM}$"))
    dot(d, (3.5, 4))
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$R_2=4{OHM}$", loc="top"))
    note(d, (2.4, 0.8), "被短路")
    cur(d, (3.5, 4), (6, 4), "$5\\,\\mathrm{A}$")
    dot(d, (6, 4)); text(d, (6, 4.5), "$a$")
    d.add(elm.Line().endpoints((6, 4), (6, 0)).color(C2))
    note(d, (5.4, 2.6), "$S$\n闭合")
    arrow(d, (6.6, 2.6), (6.6, 1.2), "$I_3=8\\,\\mathrm{A}$", loc="bot")
    cur(d, (8.5, 4), (6, 4), "$I_{sc}=3\\,\\mathrm{A}$", frac=0.5)
    wire(d, (0, 0), (8.5, 0))
    dot(d, (3.5, 0)); dot(d, (6, 0)); text(d, (6, -0.5), "$b$")
    wire(d, (8.5, -0.6), (11, -0.6), (11, 4.6), (8.5, 4.6), (8.5, -0.6))
    text(d, (9.75, 2.0), "A", fontsize=18)
    ssave(d, "t-436-closed")


if __name__ == "__main__":
    t_super_1(); t_super_2(); t_super_ccvs_1(); t_super_ccvs_2()
    t_thev_uoc(); t_thev_req(); t_thev_eq(); t_norton_isc()
    t_ccvs_isc(); t_ccvs_test(); t_436_closed()
