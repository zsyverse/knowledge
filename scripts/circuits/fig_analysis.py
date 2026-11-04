"""分析方法页插图。

约定：所有二端元件都用 .endpoints(起点, 终点) 定位；
SourceV 的 + 端在终点一侧，SourceI / 受控电流源的箭头由起点指向终点。
"""
from common import elm, new_drawing, save, dot, text, cur, vsrc_h

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def mesh_example():
    d = new_drawing()
    # 左 10 V（+ 在上），R1=2 Ω，中间 R3=4 Ω，R2=4 Ω，右 4 V（+ 在上）
    vs1 = d.add(elm.SourceV().endpoints((0, 0), (0, 4)).label("$10\\,\\mathrm{V}$", loc="top"))
    r1 = d.add(elm.Resistor().endpoints((0, 4), (5, 4)).label(f"$R_1=2{OHM}$"))
    r2 = d.add(elm.Resistor().endpoints((5, 4), (10, 4)).label(f"$R_2=4{OHM}$"))
    r3 = d.add(elm.Resistor().endpoints((5, 4), (5, 0)).label(f"$R_3$\n$4{OHM}$", loc="bot"))
    vs2 = d.add(elm.SourceV().endpoints((10, 0), (10, 4)).label("$4\\,\\mathrm{V}$", loc="bot"))
    gnd = d.add(elm.Line().endpoints((0, 0), (10, 0)))
    dot(d, (5, 4)); dot(d, (5, 0))
    d.add(elm.LoopCurrent([r1, r3, gnd, vs1], pad=1.3).label("$I_1$"))
    d.add(elm.LoopCurrent([r2, vs2, gnd, r3], pad=1.3).label("$I_2$"))
    save(d, "mesh-example")


def node_ccvs():
    d = new_drawing()
    # 10 V（+ 在上）—1 Ω—A；A—8 Ω—地；A—2 Ω—B；B—3 Ω—地；B—受控源 3U1（+ 在上）—地
    d.add(elm.SourceV().endpoints((0, 0), (0, 4)).label("$10\\,\\mathrm{V}$", loc="top"))
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$1{OHM}$").label(("+", "$U_1$", "−"), loc="bot"))
    dot(d, (3.5, 4)); text(d, (3.5, 4.5), "$A$")
    d.add(elm.Resistor().endpoints((3.5, 4), (3.5, 0)).label(f"$8{OHM}$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((4.2, 3.0), (4.2, 1.0)).label("$I_1$", loc="bot"))
    d.add(elm.Resistor().endpoints((3.5, 4), (7.5, 4)).label(f"$2{OHM}$"))
    dot(d, (7.5, 4)); text(d, (7.5, 4.5), "$B$")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$3{OHM}$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((8.2, 3.0), (8.2, 1.0)).label("$I_3$", loc="bot"))
    d.add(elm.Line().endpoints((7.5, 4), (11, 4)))
    d.add(elm.SourceControlledV().endpoints((11, 0), (11, 4)).label("$3U_1$", loc="top"))
    d.add(elm.Arrow(**ARW).endpoints((11.8, 1.0), (11.8, 3.0)).label("$I_2$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (11, 0)))
    dot(d, (3.5, 0)); dot(d, (7.5, 0))
    d.add(elm.Arrow(**ARW).endpoints((2.6, -0.45), (0.9, -0.45)).label("$I_4$", loc="bot"))
    d.add(elm.Ground().at((5.5, 0)))
    save(d, "node-ccvs")


def supernode():
    d = new_drawing()
    # 1 A 由地注入 a；a—2 Ω—地；a、b 间 10 V（a 正 b 负）；b—3 Ω—地
    d.add(elm.SourceI().endpoints((0, 0), (0, 4)).label("$1\\,\\mathrm{A}$", loc="top"))
    d.add(elm.Line().endpoints((0, 4), (2.5, 4)))
    d.add(elm.Resistor().endpoints((2.5, 4), (2.5, 0)).label(f"$2{OHM}$", loc="bot"))
    dot(d, (2.5, 4)); text(d, (2.5, 4.5), "$a$")
    d.add(elm.Line().endpoints((2.5, 4), (3.5, 4)))
    vsrc_h(d, (3.5, 4), (6.5, 4), "$10\\,\\mathrm{V}$")
    d.add(elm.Line().endpoints((6.5, 4), (7.5, 4)))
    dot(d, (7.5, 4)); text(d, (7.5, 4.5), "$b$")
    d.add(elm.Resistor().endpoints((7.5, 4), (7.5, 0)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (7.5, 0)))
    dot(d, (2.5, 0))
    d.add(elm.Ground().at((5, 0)))
    # 超节点虚线框：圈住 a、电压源、b
    d.add(elm.Line().endpoints((2.0, 3.3), (8.0, 3.3)).linestyle("--").color("#e8590c"))
    d.add(elm.Line().endpoints((8.0, 3.3), (8.0, 5.3)).linestyle("--").color("#e8590c"))
    d.add(elm.Line().endpoints((8.0, 5.3), (2.0, 5.3)).linestyle("--").color("#e8590c"))
    d.add(elm.Line().endpoints((2.0, 5.3), (2.0, 3.3)).linestyle("--").color("#e8590c"))
    text(d, (5, 5.75), "超节点", fontsize=13, color="#e8590c")
    save(d, "supernode")


def diode_example():
    d = new_drawing()
    dot(d, (0, 4), True); text(d, (0, 4.5), "$a\\ (V_a)$")
    d.add(elm.Diode().endpoints((0, 4), (3, 4)).label("$D$"))
    d.add(elm.Arrow(**ARW).endpoints((0.9, 3.35), (2.1, 3.35)).label("$I_D$", loc="bot"))
    dot(d, (3, 4)); text(d, (3, 4.5), "$x$")
    d.add(elm.Resistor().endpoints((3, 4), (3, 1)).label("$4\\,\\mathrm{k\\Omega}$", loc="top"))
    dot(d, (3, 1), True); text(d, (3, 0.45), "$-24\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((3, 4), (7, 4)).label("$8\\,\\mathrm{k\\Omega}$"))
    dot(d, (7, 4)); text(d, (7, 3.45), "$b$")
    d.add(elm.Resistor().endpoints((7, 4), (7, 7)).label("$20\\,\\mathrm{k\\Omega}$", loc="top"))
    d.add(elm.Line().endpoints((7, 4), (9.5, 4)))
    d.add(elm.SourceI().endpoints((9.5, 7), (9.5, 4)).label("$3.5\\,\\mathrm{mA}$", loc="bot"))
    d.add(elm.Line().endpoints((7, 7), (9.5, 7)))
    dot(d, (7, 7)); d.add(elm.Line().endpoints((7, 7), (7, 8)))
    dot(d, (7, 8), True); text(d, (7, 8.5), "$+10\\,\\mathrm{V}$")
    save(d, "diode-example")


if __name__ == "__main__":
    mesh_example()
    node_ccvs()
    supernode()
    diode_example()
