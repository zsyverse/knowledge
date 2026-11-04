"""基本概念页插图。"""
from common import elm, new_drawing, save, dot, text, cur


def ref_direction():
    d = new_drawing()
    # (a) 关联参考方向：i 从 + 端流入
    dot(d, (0, 0), True)
    cur(d, (0, 0), (1.2, 0), "$i$")
    d.add(elm.RBox().endpoints((1.2, 0), (4.2, 0)).label(("+", "$u$", "−"), loc="bot", ofst=0.05))
    d.add(elm.Line().endpoints((4.2, 0), (5.4, 0)))
    dot(d, (5.4, 0), True)
    text(d, (2.7, 1.2), "(a) 关联：$p=ui$ 为吸收功率", fontsize=13)
    # (b) 非关联：i 从 − 端流入
    x0 = 7.5
    dot(d, (x0, 0), True)
    d.add(elm.Line().endpoints((x0, 0), (x0 + 1.2, 0)))
    d.add(elm.RBox().endpoints((x0 + 1.2, 0), (x0 + 4.2, 0)).label(("+", "$u$", "−"), loc="bot", ofst=0.05))
    cur(d, (x0 + 5.4, 0), (x0 + 4.2, 0), "$i$")
    dot(d, (x0 + 5.4, 0), True)
    text(d, (x0 + 2.7, 1.2), "(b) 非关联：$p=-ui$ 为吸收功率", fontsize=13)
    save(d, "ref-direction")


def power_example():
    d = new_drawing()
    # 左：2 A 电流源（箭头向上）；上：5 Ω；右：15 V 电压源（+ 在上）
    d.add(elm.SourceI().endpoints((0, 0), (0, 3.5)).label("$2\\,\\mathrm{A}$", loc="bot")
          .label(("−", "$U_I$", "+"), loc="top", ofst=0.25))
    d.add(elm.Line().endpoints((0, 3.5), (1, 3.5)))
    d.add(elm.Resistor().endpoints((1, 3.5), (4, 3.5)).label("$5\\,\\Omega$")
          .label(("+", "$U_R$", "−"), loc="bot"))
    cur(d, (4, 3.5), (5, 3.5), "$I=2\\,\\mathrm{A}$")
    d.add(elm.SourceV().endpoints((5, 0), (5, 3.5)).label("$15\\,\\mathrm{V}$", loc="bot"))
    d.add(elm.Line().endpoints((5, 0), (0, 0)))
    save(d, "power-example")


def potential_example():
    d = new_drawing()
    dot(d, (0, 9), True)
    text(d, (-1.1, 9), "$+12\\,\\mathrm{V}$")
    d.add(elm.Resistor().endpoints((0, 9), (0, 6)).label("$4\\,\\Omega$", loc="bot"))
    dot(d, (0, 6))
    text(d, (-0.5, 6), "$C$")
    d.add(elm.Resistor().endpoints((0, 6), (0, 3)).label("$2\\,\\Omega$", loc="bot"))
    dot(d, (0, 3))
    text(d, (-0.5, 3), "$A$")
    d.add(elm.Resistor().endpoints((0, 3), (0, 0)).label("$4\\,\\Omega$", loc="bot"))
    dot(d, (0, 0), True)
    text(d, (-1.1, 0), "$-12\\,\\mathrm{V}$")
    d.add(elm.Line().endpoints((0, 6), (1, 6)))
    d.add(elm.Switch().endpoints((1, 6), (3.5, 6)).label("$S$"))
    d.add(elm.Line().endpoints((3.5, 6), (3.5, 5)))
    d.add(elm.Ground().at((3.5, 5)))
    save(d, "potential-example")


if __name__ == "__main__":
    ref_direction()
    power_example()
    potential_example()
