"""动态电路页插图。"""
from common import elm, new_drawing, save, dot, text, cur

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def rc_example():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 4)).label("$12\\,\\mathrm{V}$", loc="top"))
    d.add(elm.Resistor().endpoints((0, 4), (3.5, 4)).label(f"$6{OHM}$"))
    dot(d, (3.5, 4))
    d.add(elm.Capacitor().endpoints((3.5, 4), (3.5, 0)).label("$1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    d.add(elm.Line().endpoints((3.5, 4), (6.5, 4)))
    dot(d, (6.5, 4))
    d.add(elm.Resistor().endpoints((6.5, 4), (6.5, 0)).label(f"$3{OHM}$", loc="bot"))
    d.add(elm.Switch(action="close").endpoints((6.5, 4), (9.5, 4)).label("$S\\ (t=0)$"))
    d.add(elm.Resistor().endpoints((9.5, 4), (9.5, 0)).label(f"$2{OHM}$", loc="top")
          .label(("+", "$u$", "−"), loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (9.5, 0)))
    dot(d, (3.5, 0)); dot(d, (6.5, 0))
    save(d, "rc-example")


def rl_example():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 5)).label("$12\\,\\mathrm{V}$", loc="top"))
    d.add(elm.Resistor().endpoints((0, 5), (4, 5)).label(f"$R_1=2{OHM}$"))
    dot(d, (4, 5)); text(d, (4, 5.5), "$a$")
    d.add(elm.Switch(action="open").endpoints((4, 5), (4, 2.6)).label("$S\\ (t=0)$", loc="top"))
    d.add(elm.Resistor().endpoints((4, 2.6), (4, 0)).label(f"$R_2=6{OHM}$", loc="top"))
    d.add(elm.Line().endpoints((4, 5), (7.5, 5)))
    d.add(elm.Resistor().endpoints((7.5, 5), (7.5, 2.6)).label(f"$R_3=3{OHM}$", loc="top"))
    d.add(elm.Inductor2(loops=3).endpoints((7.5, 2.6), (7.5, 0)).label("$1\\,\\mathrm{H}$", loc="top")
          .label(("+", "$u_L$", "−"), loc="bot"))
    d.add(elm.Arrow(**ARW).endpoints((8.9, 4.4), (8.9, 3.0)).label("$i_L$", loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (7.5, 0)))
    dot(d, (4, 0))
    save(d, "rl-example")


def cap_jump():
    d = new_drawing()
    d.add(elm.Capacitor().endpoints((0, 3.5), (0, 0)).label("$C_1=1\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_1$", "−"), loc="bot"))
    d.add(elm.Switch(action="close").endpoints((0, 3.5), (3.5, 3.5)).label("$S\\ (t=0)$"))
    d.add(elm.Capacitor().endpoints((3.5, 3.5), (3.5, 0)).label("$C_2=2\\,\\mathrm{F}$", loc="bot")
          .label(("+", "$u_2$", "−"), loc="top"))
    d.add(elm.Line().endpoints((0, 0), (3.5, 0)))
    save(d, "cap-jump")


def rc_controlled():
    d = new_drawing()
    d.add(elm.SourceV().endpoints((0, 0), (0, 4)).label("$10\\,\\mathrm{V}$", loc="top"))
    d.add(elm.Switch(action="close").endpoints((0, 4), (2.8, 4)).label("$S\\ (t=0)$"))
    d.add(elm.Resistor().endpoints((2.8, 4), (5.8, 4)).label(f"$R_1=2{OHM}$"))
    d.add(elm.Arrow(**ARW).endpoints((3.6, 3.35), (5.0, 3.35)).label("$i_1$", loc="bot"))
    dot(d, (5.8, 4)); text(d, (5.8, 4.5), "$a$")
    d.add(elm.SourceControlledI().endpoints((5.8, 0), (5.8, 4)).label("$0.5\\,i_1$", loc="bot"))
    d.add(elm.Line().endpoints((5.8, 4), (13, 4)))
    d.add(elm.Resistor().endpoints((9, 4), (9, 0)).label(f"$R_2=2{OHM}$", loc="bot"))
    dot(d, (9, 4)); dot(d, (9, 0))
    d.add(elm.Capacitor().endpoints((13, 4), (13, 0)).label("$0.5\\,\\mathrm{F}$", loc="top")
          .label(("+", "$u_C$", "−"), loc="bot"))
    d.add(elm.Line().endpoints((0, 0), (13, 0)))
    dot(d, (5.8, 0))
    save(d, "rc-controlled")


if __name__ == "__main__":
    rc_example()
    rl_example()
    cap_jump()
    rc_controlled()
