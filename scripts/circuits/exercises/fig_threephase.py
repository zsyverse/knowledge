"""习题·三相电路 插图（前缀 s-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, arrow, wire, ac_src, OHM

YA, YB, YC = 6.0, 3.5, 1.0


def terminals(d, x=0.0, labels=("A", "B", "C")):
    for y, s in zip((YA, YB, YC), labels):
        dot(d, (x, y), True)
        text(d, (x - 0.45, y), f"${s}$")


def ladder_delta(d, x1, x2, x3, zl="$Z$", arrow_ab=True):
    """Δ 负载画成梯形：Z_AB 在 x1（A→B），Z_BC 在 x2（B→C），Z_CA 在 x3（A→C）。"""
    d.add(elm.RBox().endpoints((x1, YA), (x1, YB)).label(zl, loc="bot"))
    d.add(elm.RBox().endpoints((x2, YB), (x2, YC)).label(zl, loc="bot"))
    d.add(elm.RBox().endpoints((x3, YA), (x3, YC)).label(zl, loc="bot"))
    dot(d, (x1, YA)); dot(d, (x1, YB)); dot(d, (x2, YB)); dot(d, (x2, YC))
    if arrow_ab:
        arrow(d, (x1 - 0.65, YA - 0.45), (x1 - 0.65, YB + 0.45), "$\\dot I_{AB}$", loc="top")


def s_delta():
    d = new_drawing()
    terminals(d)
    cur(d, (0, YA), (2.5, YA), "$\\dot I_A$")
    wire(d, (2.5, YA), (9, YA))
    wire(d, (0, YB), (6.5, YB))
    wire(d, (0, YC), (9, YC))
    ladder_delta(d, 4, 6.5, 9, "$Z$")
    save(d, "s-delta")


def s_delta_line():
    d = new_drawing()
    terminals(d)
    for y in (YA, YB, YC):
        d.add(elm.RBox().endpoints((0.6, y), (3.4, y)).label("$Z_l$"))
        d.add(elm.Line().endpoints((0, y), (0.6, y)))
    cur(d, (3.4, YA), (4.8, YA), "$\\dot I_A$")
    wire(d, (4.8, YA), (11, YA))
    wire(d, (3.4, YB), (8.5, YB))
    wire(d, (3.4, YC), (11, YC))
    for y, s in ((YA, "A'"), (YB, "B'"), (YC, "C'")):
        text(d, (4.0, y - 0.45), f"${s}$")
    ladder_delta(d, 6, 8.5, 11, "$Z_\\Delta$")
    save(d, "s-delta-line")


def s_5_51():
    """作业 5-51：Y 形电源；Y 形电容负载与 Δ 形电阻负载并接。"""
    d = new_drawing()
    xs = 0.0
    for y, s in ((YA, "A"), (YB, "B"), (YC, "C")):
        d.add(elm.SourceSin().endpoints((xs, y), (xs + 2.6, y)).label(f"$\\dot U_{s}$", loc="top")
              .label(("−", "", "+"), loc="bot", ofst=0.1))
    wire(d, (xs, YA), (xs, YC))
    dot(d, (xs, YB)); text(d, (xs - 0.45, YB), "$N$")
    cur(d, (xs + 2.6, YA), (xs + 3.8, YA), "$\\dot I_A$")
    wire(d, (xs + 3.8, YA), (13, YA))
    wire(d, (xs + 2.6, YB), (10.5, YB))
    wire(d, (xs + 2.6, YC), (13, YC))
    text(d, (9.3, YA + 0.45), "$A$"); text(d, (9.3, YB + 0.45), "$B$"); text(d, (9.3, YC - 0.45), "$C$")
    # Y 形电容：从各端线向下到星点母线（交叉处无圆点＝不相连）
    yb = -2.0
    for x, y in ((5, YA), (6.3, YB), (7.6, YC)):
        dot(d, (x, y))
        wire(d, (x, y), (x, -0.4))
        d.add(elm.Capacitor().endpoints((x, -0.4), (x, yb)).label("$C$", loc="bot"))
    wire(d, (5, yb), (7.6, yb))
    text(d, (6.3, yb - 0.5), "$N'$")
    arrow(d, (4.35, YA - 0.6), (4.35, YB + 0.6), "$\\dot I_{A1}$", loc="top")
    # Δ 形电阻
    d.add(elm.Resistor().endpoints((9, YA), (9, YB)).label(f"$300{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((10.5, YB), (10.5, YC)).label(f"$300{OHM}$", loc="bot"))
    d.add(elm.Resistor().endpoints((13, YA), (13, YC)).label(f"$300{OHM}$", loc="bot"))
    for p in ((9, YA), (9, YB), (10.5, YB), (10.5, YC)):
        dot(d, p)
    arrow(d, (8.35, YA - 0.45), (8.35, YB + 0.45), "$\\dot I_{AB}$", loc="top")
    save(d, "s-5-51")


def wattmeter(d, x, y, yv, name):
    """功率表：电流线圈串在 y 线上（圆），两线圈的 * 端相连于左侧；电压线圈另一端接 yv 线。"""
    d.add(elm.Source().endpoints((x - 1.2, y), (x + 1.2, y)))
    text(d, (x, y), name, fontsize=13)
    s = 1 if yv < y else -1          # 电压线圈引线方向：yv 在下方时从圆底引出
    wire(d, (x - 0.9, y), (x - 0.9, y + s * 1.0), (x, y + s * 1.0), (x, y + s * 0.5))
    text(d, (x - 1.15, y + s * 0.35), "$*$"); text(d, (x + 0.3, y + s * 0.85), "$*$")
    wire(d, (x, y - s * 0.5), (x, yv))
    dot(d, (x - 0.9, y)); dot(d, (x, yv))


def s_two_watt():
    d = new_drawing()
    terminals(d)
    wire(d, (0, YA), (2.8, YA)); wire(d, (5.2, YA), (12, YA))
    wire(d, (0, YB), (12, YB))
    wire(d, (0, YC), (2.8, YC)); wire(d, (5.2, YC), (12, YC))
    wattmeter(d, 4, YA, YB, "$W_1$")
    wattmeter(d, 4, YC, YB, "$W_2$")
    arrow(d, (6.2, YA + 0.5), (7.6, YA + 0.5), "$\\dot I_A$", loc="top")
    arrow(d, (6.2, YC + 0.5), (7.6, YC + 0.5), "$\\dot I_C$", loc="top")
    for y in (YA, YB, YC):
        d.add(elm.RBox().endpoints((12, y), (15, y)).label("$Z$"))
    wire(d, (15, YA), (15, YC))
    dot(d, (15, YB)); text(d, (15.5, YB), "$N'$")
    text(d, (13.5, YC - 1.0), "对称 Y 形负载", fontsize=12)
    save(d, "s-two-watt")


def s_ystar(name, elems):
    d = new_drawing()
    terminals(d)
    for y, (kind, lab) in zip((YA, YB, YC), elems):
        wire(d, (0, y), (3, y))
        e = {"C": elm.Capacitor, "R": elm.Resistor, "Z": elm.RBox, "L": elm.Lamp}[kind]
        d.add(e().endpoints((3, y), (6.5, y)).label(lab))
    wire(d, (6.5, YA), (6.5, YC))
    dot(d, (6.5, YB)); text(d, (7.0, YB), "$N'$")
    for y, s in ((YA, "A"), (YB, "B"), (YC, "C")):
        arrow(d, (0.8, y + 0.5), (2.2, y + 0.5), f"$\\dot I_{s}$", loc="top")
    save(d, name)


def s_5_58():
    d = new_drawing()
    dot(d, (0, 6), True); dot(d, (0, 0), True)
    text(d, (-0.4, 6.1), "$+$"); text(d, (-0.4, -0.1), "$-$")
    d.add(elm.Gap().endpoints((0, 6), (0, 0)).label("$\\dot U$", loc="bot", ofst=0.4))
    wire(d, (0, 6), (2, 6)); wire(d, (0, 0), (2, 0))
    d.add(elm.Inductor2(loops=3).endpoints((2, 6), (2, 3)).label("$L$", loc="bot"))
    d.add(elm.Capacitor().endpoints((2, 3), (2, 0)).label("$C$", loc="bot"))
    dot(d, (2, 6)); dot(d, (2, 3)); dot(d, (2, 0))
    for y, s in ((6, "A"), (3, "B"), (0, "C")):
        d.add(elm.Resistor().endpoints((2, y), (7, y)).label("$R$")
              .label(("+", f"$\\dot U_{s}$", "−"), loc="bot"))
    wire(d, (7, 6), (7, 0))
    dot(d, (7, 3)); text(d, (7.45, 3), "$O$")
    save(d, "s-5-58")


if __name__ == "__main__":
    s_delta()
    s_delta_line()
    s_5_51()
    s_two_watt()
    s_ystar("s-ystar", [("Z", "$Z$"), ("Z", "$Z$"), ("Z", "$Z$")])
    s_ystar("s-phase-seq", [("C", "$C$"), ("L", "$R$"), ("L", "$R$")])
    s_5_58()
