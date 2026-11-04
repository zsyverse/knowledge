"""习题·正弦稳态功率与谐振 插图（前缀 w-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, arrow, wire, ac_src, OHM


def w_branch():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 5), "$\\dot U_S=100\\angle0^\\circ\\,\\mathrm{V}$")
    cur(d, (0, 5), (1.0, 5), "$\\dot I_1$")
    d.add(elm.Resistor().endpoints((1.0, 5), (3.6, 5)).label(f"$1{OHM}$"))
    d.add(elm.Capacitor().endpoints((3.6, 5), (6, 5)).label(f"$-j1{OHM}$"))
    dot(d, (6, 5)); text(d, (6, 5.5), "$a$")
    d.add(elm.Resistor().endpoints((6, 5), (6, 2.5)).label(f"$6{OHM}$", loc="top"))
    d.add(elm.Inductor2(loops=3).endpoints((6, 2.5), (6, 0)).label(f"$j8{OHM}$", loc="top"))
    arrow(d, (6.7, 4.3), (6.7, 3.1), "$\\dot I_2$")
    wire(d, (6, 5), (10, 5))
    d.add(elm.Resistor().endpoints((10, 5), (10, 2.5)).label(f"$8{OHM}$", loc="top"))
    d.add(elm.Capacitor().endpoints((10, 2.5), (10, 0)).label(f"$-j6{OHM}$", loc="top"))
    arrow(d, (10.7, 4.3), (10.7, 3.1), "$\\dot I_3$")
    wire(d, (0, 0), (10, 0))
    dot(d, (6, 0)); text(d, (6, -0.5), "$b$")
    save(d, "w-branch")


def w_line():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_1$")
    cur(d, (0, 4), (1.2, 4), "$\\dot I$")
    d.add(elm.RBox().endpoints((1.2, 4), (4.8, 4)).label(f"$Z_l=0.1+j0.1{OHM}$"))
    wire(d, (4.8, 4), (7, 4))
    d.add(elm.RBox().endpoints((7, 4), (7, 0)).label("负载", loc="bot", fontsize=12))
    text(d, (8.9, 2.3), "$P_2=10\\,\\mathrm{kW}$", fontsize=13)
    text(d, (8.9, 1.5), "$\\lambda_2=0.8$（感性）", fontsize=12)
    d.add(elm.Gap().endpoints((5.8, 3.5), (5.8, 0.5)).label(("+", "$\\dot U_2$", "−"), loc="top"))
    wire(d, (0, 0), (7, 0))
    save(d, "w-line")


def w_pfc():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$220\\,\\mathrm{V}$\n$50\\,\\mathrm{Hz}$")
    cur(d, (0, 4), (2, 4), "$\\dot I$")
    wire(d, (2, 4), (7, 4))
    d.add(elm.RBox().endpoints((3.5, 4), (3.5, 0)).label("$Z$", loc="top")
          .label("$10\\,\\mathrm{kW}$\n$\\lambda=0.6$\n（感性）", loc="bot", fontsize=12))
    d.add(elm.Capacitor().endpoints((7, 4), (7, 0)).label("$C$", loc="bot").color("#2a78d6"))
    wire(d, (0, 0), (7, 0))
    for x in (3.5,):
        dot(d, (x, 4)); dot(d, (x, 0))
    save(d, "w-pfc")


def w_maxp():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$20\\angle0^\\circ\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$4{OHM}$"))
    dot(d, (3.5, 4))
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4), (3.5, 0)).label(f"$j4{OHM}$", loc="top"))
    wire(d, (3.5, 4), (6, 4)); wire(d, (0, 0), (6, 0))
    dot(d, (3.5, 0))
    dot(d, (6, 4), True); dot(d, (6, 0), True)
    text(d, (6, 4.5), "$a$"); text(d, (6, -0.5), "$b$")
    wire(d, (6, 4), (8, 4)); wire(d, (6, 0), (8, 0))
    d.add(elm.RBox().endpoints((8, 4), (8, 0)).label("$Z_L$", loc="bot"))
    save(d, "w-maxp")


def w_watt():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U_A$")
    cur(d, (0, 4), (1.4, 4), "$\\dot I$")
    d.add(elm.Inductor2(loops=3).endpoints((1.4, 4), (4.4, 4)).label(f"$j10{OHM}$"))
    wire(d, (4.4, 4), (5.0, 4))
    # 瓦特表：电流线圈（水平方框）串在上方导线中，* 端在右；电压线圈（竖直方框）* 端接同一点，另一端接下方导线
    d.add(elm.RBox().endpoints((5.0, 4), (7.6, 4)).label("$W$", loc="top", ofst=0.25))
    text(d, (7.3, 4.6), "$*$", fontsize=16)
    dot(d, (7.6, 4))
    d.add(elm.RBox().endpoints((7.6, 4), (7.6, 0)))
    text(d, (7.15, 3.3), "$*$", fontsize=16)
    dot(d, (7.6, 0))
    wire(d, (7.6, 4), (10, 4))
    ac_src(d, (10, 0), (10, 4), "$\\dot U_B$", loc="bot")
    wire(d, (0, 0), (10, 0))
    save(d, "w-watt")


def w_series():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$\\dot U$")
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$R=12.5{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((3.5, 4), (7, 4)).label("$L=250\\,\\mu\\mathrm{H}$"))
    cur(d, (7, 4), (8.5, 4), "$\\dot I$")
    d.add(elm.Capacitor().endpoints((8.5, 4), (8.5, 0)).label("$C$", loc="bot")
          .label(("+", "$\\dot U_C$", "−"), loc="top"))
    wire(d, (0, 0), (8.5, 0))
    save(d, "w-series")


def w_multi():
    d = new_drawing()
    dot(d, (0, 5), True); dot(d, (0, 0), True)
    text(d, (-0.45, 5), "$a$"); text(d, (-0.45, 0), "$b$")
    d.add(elm.Gap().endpoints((0, 5), (0, 0)).label(("+", "$\\dot U$", "−"), loc="bot"))
    d.add(elm.Resistor().endpoints((0, 5), (3, 5)).label(f"$R_1=100{OHM}$"))
    cur(d, (3, 5), (4.5, 5), "$\\dot I_1$")
    dot(d, (4.5, 5)); text(d, (4.5, 5.5), "$c$")
    d.add(elm.Resistor().endpoints((4.5, 5), (4.5, 0)).label(f"$R_2=50{OHM}$", loc="top"))
    arrow(d, (5.2, 3.2), (5.2, 1.8), "$\\dot I_2$")
    d.add(elm.Capacitor().endpoints((4.5, 5), (8, 5)).label("$C_1=20\\,\\mu\\mathrm{F}$"))
    d.add(elm.Inductor2(loops=3).endpoints((8, 5), (8, 2.5)).label("$L=0.4\\,\\mathrm{H}$", loc="bot"))
    d.add(elm.Capacitor().endpoints((8, 2.5), (8, 0)).label("$C_2=20\\,\\mu\\mathrm{F}$", loc="bot"))
    wire(d, (0, 0), (8, 0))
    dot(d, (4.5, 0))
    save(d, "w-multi")


if __name__ == "__main__":
    w_branch(); w_line(); w_pfc(); w_maxp(); w_watt(); w_series(); w_multi()
