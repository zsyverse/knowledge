"""习题·互感与理想变压器 解析插图（images/ex/sol/m-*）。数值见 verify_coupled.py。"""
from solcommon import (elm, new_drawing, ssave, dot, text, note, cur, arrow, wire, ac_src, OHM, MUTED)


def m_tdec_eq():
    """题4：异名端相连 → 臂 j(4+2)、j(8+2)、-j2（通向 n）。"""
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$50\\angle0^\\circ\\,\\mathrm{V}$")
    cur(d, (0, 4), (1.2, 4), "$\\dot I$")
    dot(d, (1.2, 4)); text(d, (1.2, 4.5), "$a$")
    d.add(elm.Inductor2(loops=3).endpoints((1.2, 4), (4.5, 4)).label(f"$j(4+2)=j6{OHM}$"))
    dot(d, (4.5, 4)); dot(d, (4.5, 0))
    d.add(elm.Inductor2(loops=3).endpoints((4.5, 4), (4.5, 0)).label(f"$j(8+2)=j10{OHM}$", loc="bot"))
    d.add(elm.Inductor2(loops=3).endpoints((4.5, 4), (8.5, 4)).label(f"$-j2{OHM}$"))
    note(d, (6.5, 3.3), "（$-M$ 臂）")
    dot(d, (8.5, 4)); text(d, (8.5, 4.5), "$n$")
    d.add(elm.Resistor().endpoints((8.5, 4), (8.5, 0)).label(f"$6{OHM}$", loc="bot"))
    wire(d, (0, 0), (8.5, 0))
    ssave(d, "m-tdec-eq")


def m_mesh_tdec():
    """题5：L1、L2 的同名端都接在公共节点 → 同名端相连：臂 j(4-2)、j(4-2)，公共臂 +j2。"""
    d = new_drawing()
    ac_src(d, (0, 0), (0, 6), "$20\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.Inductor2(loops=3).endpoints((0, 6), (3.6, 6)).label(f"$j\\omega M=j2{OHM}$"))
    arrow(d, (0.9, 7.5), (2.7, 7.5), None); text(d, (1.8, 8.0), "$\\dot I_1-\\dot I_S$")
    dot(d, (3.6, 6)); dot(d, (3.6, 0))
    d.add(elm.Inductor2(loops=3).endpoints((3.6, 6), (3.6, 3)).label(f"$j(4-2){OHM}$", loc="top"))
    d.add(elm.Resistor().endpoints((3.6, 3), (3.6, 0)).label(f"$5{OHM}$", loc="top"))
    arrow(d, (4.3, 2.2), (4.3, 0.9), "$\\dot I_1$", loc="bot")
    d.add(elm.Inductor2(loops=3).endpoints((3.6, 6), (8.2, 6)).label(f"$j(4-2){OHM}$"))
    d.add(elm.SourceI().endpoints((8.2, 0), (8.2, 6)).label("$\\dot I_S=j2\\,\\mathrm{A}$", loc="bot"))
    wire(d, (0, 0), (8.2, 0))
    ssave(d, "m-mesh-tdec")


def m_reflect_pri():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$100\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3, 4)).label(f"$10{OHM}$"))
    cur(d, (3, 4), (4.2, 4), "$\\dot I_1$")
    d.add(elm.Inductor2(loops=3).endpoints((4.2, 4), (7.2, 4)).label(f"$j20{OHM}$"))
    d.add(elm.RBox().endpoints((7.2, 4), (7.2, 0)).label(f"$Z_r=5-j5{OHM}$", loc="bot"))
    note(d, (8.6, 0.6), "（反映阻抗）")
    wire(d, (0, 0), (7.2, 0))
    ssave(d, "m-reflect-pri")


def m_reflect_sec():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$j\\omega M\\dot I_1=47.14\\angle45^\\circ\\,\\mathrm{V}$")
    cur(d, (0, 4), (1.4, 4), "$\\dot I_2$")
    d.add(elm.Inductor2(loops=3).endpoints((1.4, 4), (4.4, 4)).label(f"$j10{OHM}$"))
    d.add(elm.Resistor().endpoints((4.4, 4), (4.4, 0)).label(f"$R_L=10{OHM}$", loc="bot"))
    wire(d, (0, 0), (4.4, 0))
    ssave(d, "m-reflect-sec")


def _ref(d, us, rs, rin, name, i1=None, u1=None):
    ac_src(d, (0, 0), (0, 4), us)
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(rs))
    if i1:
        cur(d, (3.5, 4), (5.5, 4), i1)
    else:
        wire(d, (3.5, 4), (5.5, 4))
    d.add(elm.Resistor().endpoints((5.5, 4), (5.5, 0)).label(rin, loc="bot")
          .label(("+", u1 or "", "−"), loc="top"))
    wire(d, (0, 0), (5.5, 0))
    ssave(d, name)


def m_match_ref():
    d = new_drawing()
    _ref(d, "$12\\angle0^\\circ\\,\\mathrm{V}$", f"$R_S=800{OHM}$", f"$n^2R_L=10^2\\times8=800{OHM}$",
         "m-match-ref", u1="$\\dot U_1$")


def m_trap_ref():
    d = new_drawing()
    _ref(d, "$20\\angle0^\\circ\\,\\mathrm{V}$", f"$4{OHM}$", f"$n^2R_L=2^2\\times2=8{OHM}$",
         "m-trap-ref", i1="$\\dot I_1=\\frac{5}{3}\\,\\mathrm{A}$", u1="$\\dot U_1$")


if __name__ == "__main__":
    m_tdec_eq(); m_mesh_tdec(); m_reflect_pri(); m_reflect_sec(); m_match_ref(); m_trap_ref()
