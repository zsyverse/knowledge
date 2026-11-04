"""习题·非正弦周期电路与频率响应 插图（前缀 n-）。"""
from excommon import elm, new_drawing, save, dot, text, cur, arrow, wire, ac_src, vsrc, isrc, OHM


def n_multisrc():
    d = new_drawing()
    vsrc(d, (0, 0), (0, 4), "$12\\,\\mathrm{V}$", loc="top")
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label(f"$R_1=4{OHM}$"))
    dot(d, (4, 4)); text(d, (4, 4.5), "$a$")
    d.add(elm.Resistor().endpoints((4, 4), (4, 0)).label(f"$R_2=4{OHM}$", loc="top")
          .label(("+", "$u_a$", "−"), loc="bot"))
    wire(d, (4, 4), (8, 4))
    isrc(d, (8, 0), (8, 4), "$i_S$", loc="bot")
    wire(d, (0, 0), (8, 0))
    dot(d, (4, 0))
    save(d, "n-multisrc")


def n_rl_meter():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$u$")
    d.add(elm.MeterA().endpoints((0, 4), (3, 4)))
    d.add(elm.Resistor().endpoints((3, 4), (6.5, 4)).label("$R$"))
    d.add(elm.Inductor2(loops=3).endpoints((6.5, 4), (6.5, 0)).label("$L$", loc="bot"))
    wire(d, (0, 0), (6.5, 0))
    save(d, "n-rl-meter")


def n_rc():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4), "$u_i$")
    d.add(elm.Resistor().endpoints((0, 4), (4, 4)).label("$R=1\\,\\mathrm{k\\Omega}$"))
    dot(d, (4, 4))
    d.add(elm.Capacitor().endpoints((4, 4), (4, 0)).label("$C=1\\,\\mu\\mathrm{F}$", loc="top"))
    wire(d, (4, 4), (6.5, 4)); wire(d, (0, 0), (6.5, 0))
    dot(d, (4, 0))
    dot(d, (6.5, 4), True); dot(d, (6.5, 0), True)
    d.add(elm.Gap().endpoints((6.5, 4), (6.5, 0)).label(("+", "$u_o$", "−"), loc="bot"))
    save(d, "n-rc")


def n_rlc_meter():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 4.5), "$u$")
    d.add(elm.MeterA().endpoints((0, 4.5), (2.6, 4.5)))
    d.add(elm.Resistor().endpoints((2.6, 4.5), (5.6, 4.5)).label(f"$R=10{OHM}$"))
    d.add(elm.Inductor2(loops=3).endpoints((5.6, 4.5), (8.6, 4.5)).label(f"$\\omega L=3{OHM}$"))
    dot(d, (8.6, 4.5)); dot(d, (8.6, 0))
    d.add(elm.Capacitor().endpoints((8.6, 4.5), (8.6, 0)).label("$\\dfrac{1}{\\omega C}=27\\,\\Omega$", loc="top"))
    wire(d, (8.6, 4.5), (11, 4.5)); wire(d, (8.6, 0), (11, 0))
    d.add(elm.MeterV().endpoints((11, 4.5), (11, 0)))
    wire(d, (0, 0), (8.6, 0))
    save(d, "n-rlc-meter")


def n_filter():
    d = new_drawing()
    ac_src(d, (0, 0), (0, 5), "$u_S$")
    wire(d, (0, 5), (1.2, 5))
    # 并联谐振槽路 L1 ∥ C1
    wire(d, (1.2, 5), (1.2, 6.2)); wire(d, (1.2, 5), (1.2, 3.8))
    d.add(elm.Inductor2(loops=3).endpoints((1.2, 6.2), (4.6, 6.2)).label("$L_1$"))
    d.add(elm.Capacitor().endpoints((1.2, 3.8), (4.6, 3.8)).label("$C_1=10\\,\\mu\\mathrm{F}$", loc="bot"))
    wire(d, (4.6, 6.2), (4.6, 3.8))
    dot(d, (1.2, 5)); dot(d, (4.6, 5))
    wire(d, (4.6, 5), (5.4, 5))
    d.add(elm.Capacitor().endpoints((5.4, 5), (8.4, 5)).label("$C_2$"))
    wire(d, (8.4, 5), (9.4, 5))
    d.add(elm.Resistor().endpoints((9.4, 5), (9.4, 0)).label(f"$R=50{OHM}$", loc="bot")
          .label(("+", "$u_R$", "−"), loc="top"))
    wire(d, (0, 0), (9.4, 0))
    save(d, "n-filter")


if __name__ == "__main__":
    n_multisrc()
    n_rl_meter()
    n_rc()
    n_rlc_meter()
    n_filter()
