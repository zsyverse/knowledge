"""拓展·二端口网络 插图（前缀 tp-）。端口电流 I1、I2 一律从上端子流入网络。"""
from xcommon import (elm, new_drawing, save, dot, text, cur, arrow, vsrc, isrc, wire, gnd, OHM, MUTED)
from common import vsrc_h

U1, U2, I1, I2 = "$\\dot U_1$", "$\\dot U_2$", "$\\dot I_1$", "$\\dot I_2$"


def box(d, x0, y0, x1, y1, label=None, fs=16):
    wire(d, (x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
    if label:
        text(d, ((x0 + x1) / 2, (y0 + y1) / 2), label, fontsize=fs)


def ports(d, xl, xr, yt, yb, il=I1, ir=I2, ul=U1, ur=U2, names=True, ext=1.6):
    """在 x=xl（左）与 x=xr（右）处画端口引线、端子、电流箭头和电压极性。"""
    L, R = xl - ext, xr + ext
    cur(d, (L, yt), (xl, yt), il, loc="top")
    cur(d, (R, yt), (xr, yt), ir, loc="top")
    wire(d, (L, yb), (xl, yb)); wire(d, (R, yb), (xr, yb))
    for x in (L, R):
        dot(d, (x, yt), True); dot(d, (x, yb), True)
    ym = (yt + yb) / 2
    for x, u in ((L - 0.0, ul), (R, ur)):
        text(d, (x, yt - 0.55), "$+$"); text(d, (x, ym), u); text(d, (x, yb + 0.55), "$−$")
    if names:
        text(d, (L - 0.45, yt), "$1$"); text(d, (L - 0.45, yb), "$1'$")
        text(d, (R + 0.45, yt), "$2$"); text(d, (R + 0.45, yb), "$2'$")
    return L, R


def tp_port():
    d = new_drawing()
    box(d, 0, -0.4, 3.2, 3.4, "$N$", fs=20)
    ports(d, 0, 3.2, 3.0, 0.0)
    arrow(d, (-0.9, -0.45), (-2.0, -0.45), I1, loc="bot")
    arrow(d, (4.1, -0.45), (5.2, -0.45), I2, loc="bot")
    save(d, "tp-port")


def t_shape(d, za, zb, zc, x0=0, yt=3, yb=0, ccvs=None, terms=True):
    """T 形：上边 za、zc 串臂，中间 zb 并臂。返回两端 x。"""
    m = x0 + 3.4
    d.add(elm.Resistor().endpoints((x0, yt), (m, yt)).label(za))
    d.add(elm.Resistor().endpoints((m, yt), (m, yb)).label(zb, loc="bot"))
    dot(d, (m, yt)); dot(d, (m, yb))
    x = m
    if ccvs:
        vsrc_h(d, (m + 2.6, yt), (m, yt), ccvs, ctrl=True)
        x = m + 2.6
    d.add(elm.Resistor().endpoints((x, yt), (x + 3.4, yt)).label(zc))
    wire(d, (x0, yb), (x + 3.4, yb))
    return x0, x + 3.4


def tp_ex1():
    d = new_drawing()
    xl, xr = t_shape(d, f"$2{OHM}$", f"$4{OHM}$", f"$3{OHM}$", ccvs="$2\\dot I_1$")
    ports(d, xl, xr, 3, 0, ext=1.2)
    save(d, "tp-ex1")


def tp_teq():
    d = new_drawing()
    xl, xr = t_shape(d, "$Z_{11}-Z_{12}$", "$Z_{12}$", "$Z_{22}-Z_{12}$")
    ports(d, xl, xr, 3, 0, ext=1.2, names=False)
    save(d, "tp-teq")


def pi_shape(d, ya, yb, yc, x0=0, w=5.0, yt=3, yb_=0, res=False):
    a, b = x0 + 1.0, x0 + 1.0 + w
    wire(d, (x0, yt), (a, yt)); wire(d, (b, yt), (b + 1.0, yt))
    d.add(elm.Resistor().endpoints((a, yt), (b, yt)).label(yb))
    d.add(elm.Resistor().endpoints((a, yt), (a, yb_)).label(ya, loc="top"))
    d.add(elm.Resistor().endpoints((b, yt), (b, yb_)).label(yc, loc="top"))
    for p in ((a, yt), (b, yt), (a, yb_), (b, yb_)):
        dot(d, p)
    wire(d, (x0, yb_), (b + 1.0, yb_))
    return x0, b + 1.0


def tp_pieq():
    d = new_drawing()
    xl, xr = pi_shape(d, "$Y_{11}+Y_{12}$", "$-Y_{12}$", "$Y_{22}+Y_{12}$")
    ports(d, xl, xr, 3, 0, ext=1.2, names=False)
    save(d, "tp-pieq")


def tp_term():
    d = new_drawing()
    box(d, 0, -0.3, 3.2, 3.6, "$N$", fs=20)
    yt, yb = 3.0, 0.3
    # 左：电源
    cur(d, (-1.6, yt), (0, yt), I1, loc="top")
    d.add(elm.Resistor().endpoints((-4.8, yt), (-1.6, yt)).label("$Z_s$"))
    vsrc(d, (-4.8, yb), (-4.8, yt), "$\\dot U_s$", loc="top")
    wire(d, (-4.8, yb), (0, yb))
    dot(d, (-1.6, yt), True); dot(d, (-1.6, yb), True)
    text(d, (-1.1, yt - 0.5), "$+$"); text(d, (-1.1, 1.65), U1); text(d, (-1.1, yb + 0.5), "$−$")
    # 右：负载
    cur(d, (4.8, yt), (3.2, yt), I2, loc="top")
    wire(d, (4.8, yt), (6.6, yt)); wire(d, (3.2, yb), (6.6, yb))
    d.add(elm.Resistor().endpoints((6.6, yt), (6.6, yb)).label("$Z_L$", loc="bot"))
    dot(d, (4.8, yt), True); dot(d, (4.8, yb), True)
    text(d, (4.3, yt - 0.5), "$+$"); text(d, (4.3, 1.65), U2); text(d, (4.3, yb + 0.5), "$−$")
    arrow(d, (-1.4, -0.7), (-0.1, -0.7)); text(d, (-0.75, -1.15), "$Z_{in}$")
    arrow(d, (4.6, -0.7), (3.3, -0.7)); text(d, (3.95, -1.15), "$Z_{out}$")
    save(d, "tp-term")


def _lead(d, p, q, term=True):
    wire(d, p, q)
    if term:
        dot(d, q, True)


def tp_cascade():
    d = new_drawing()
    box(d, 0, 0, 2.4, 2.4, "$N_1$"); box(d, 4.0, 0, 6.4, 2.4, "$N_2$")
    for y in (2.0, 0.4):
        _lead(d, (0, y), (-1.2, y)); wire(d, (2.4, y), (4.0, y)); _lead(d, (6.4, y), (7.6, y))
    text(d, (3.2, -0.9), "级联：$\\mathbf{T}=\\mathbf{T}_1\\mathbf{T}_2$", fontsize=14)
    save(d, "tp-cascade")


def tp_series():
    d = new_drawing()
    box(d, 0, 1.8, 2.4, 4.2, "$N_1$"); box(d, 0, -1.4, 2.4, 1.0, "$N_2$")
    for x, xo, xm in ((0, -1.4, -0.6), (2.4, 3.8, 3.0)):
        _lead(d, (x, 3.8), (xo, 3.8)); _lead(d, (x, -1.0), (xo, -1.0))
        wire(d, (x, 2.2), (xm, 2.2), (xm, 0.6), (x, 0.6))
    text(d, (1.2, -2.3), "串联：$\\mathbf{Z}=\\mathbf{Z}_1+\\mathbf{Z}_2$", fontsize=14)
    save(d, "tp-series")


def tp_parallel():
    d = new_drawing()
    box(d, 0, 1.8, 2.4, 4.2, "$N_1$"); box(d, 0, -1.4, 2.4, 1.0, "$N_2$")
    for x, s_ in ((0, -1), (2.4, 1)):
        xa, xb, xo = x + 0.6 * s_, x + 1.2 * s_, x + 1.9 * s_
        _lead(d, (x, 3.8), (xo, 3.8)); dot(d, (xa, 3.8))
        wire(d, (xa, 3.8), (xa, 0.6), (x, 0.6))
        _lead(d, (x, -1.0), (xo, -1.0)); dot(d, (xb, -1.0))
        wire(d, (x, 2.2), (xb, 2.2), (xb, -1.0))
    text(d, (1.2, -2.3), "并联：$\\mathbf{Y}=\\mathbf{Y}_1+\\mathbf{Y}_2$", fontsize=14)
    save(d, "tp-parallel")


def tp_gyrator():
    d = new_drawing()
    box(d, 0, -0.3, 3.0, 3.6, None)
    text(d, (1.5, 2.05), "$r$", fontsize=16)
    d.add(elm.Arrow(headwidth=0.25, headlength=0.3).endpoints((0.9, 1.35), (2.1, 1.35)))
    yt, yb = 3.0, 0.3
    cur(d, (-1.4, yt), (0, yt), I1, loc="top")
    wire(d, (-1.4, yb), (0, yb))
    dot(d, (-1.4, yt), True); dot(d, (-1.4, yb), True)
    text(d, (-1.4, yt - 0.55), "$+$"); text(d, (-1.4, 1.65), U1); text(d, (-1.4, yb + 0.55), "$−$")
    cur(d, (4.4, yt), (3.0, yt), I2, loc="top")
    wire(d, (4.4, yt), (5.8, yt)); wire(d, (3.0, yb), (5.8, yb))
    dot(d, (4.4, yt), True); dot(d, (4.4, yb), True)
    text(d, (4.4, yt - 0.55), "$+$"); text(d, (4.4, 1.65), U2); text(d, (4.4, yb + 0.55), "$−$")
    d.add(elm.Capacitor().endpoints((5.8, yt), (5.8, yb)).label("$C$", loc="bot"))
    save(d, "tp-gyrator")


def tp_pi():
    d = new_drawing()
    xl, xr = pi_shape(d, f"$2{OHM}$", f"$1{OHM}$", f"$2{OHM}$", w=4.0)
    ports(d, xl, xr, 3, 0, ext=1.2)
    save(d, "tp-pi")


def tp_hfe():
    d = new_drawing()
    yt, yb = 3, 0
    d.add(elm.Resistor().endpoints((0, yt), (0, yb)).label("$r_{be}=1\\,\\mathrm{k}\\Omega$", loc="bot"))
    cur(d, (-1.6, yt), (0, yt), I1, loc="top"); wire(d, (-1.6, yb), (0, yb))
    xs, xr = 4.4, 7.8
    isrc(d, (xs, yt), (xs, yb), "$50\\dot I_1$", loc="top", ctrl=True)
    d.add(elm.Resistor().endpoints((xr, yt), (xr, yb)).label("$r_{ce}=10\\,\\mathrm{k}\\Omega$", loc="top"))
    wire(d, (xs, yt), (xr, yt)); wire(d, (xs, yb), (xr, yb))
    dot(d, (xr, yt)); dot(d, (xr, yb))
    wire(d, (xr, yt), (xr + 0.4, yt)); wire(d, (xr, yb), (xr + 1.8, yb))
    cur(d, (xr + 1.8, yt), (xr + 0.4, yt), I2, loc="top")
    for x in (-1.6, xr + 1.8):
        dot(d, (x, yt), True); dot(d, (x, yb), True)
        text(d, (x, yt - 0.55), "$+$"); text(d, (x, 1.5), U1 if x < 0 else U2); text(d, (x, yb + 0.55), "$−$")
    save(d, "tp-hfe")


def tp_ladder():
    d = new_drawing()
    yt, yb = 3, 0
    x = 0
    for k in range(2):
        d.add(elm.Resistor().endpoints((x, yt), (x + 3, yt)).label(f"$1{OHM}$"))
        d.add(elm.Resistor().endpoints((x + 3, yt), (x + 3, yb)).label(f"$2{OHM}$", loc="top"))
        dot(d, (x + 3, yt)); dot(d, (x + 3, yb))
        x += 3
    wire(d, (x, yt), (x + 2.2, yt))
    d.add(elm.Resistor().endpoints((x + 2.2, yt), (x + 2.2, yb)).label(f"$R_L=2{OHM}$", loc="bot"))
    wire(d, (-1.2, yb), (x + 2.2, yb)); wire(d, (-1.2, yt), (0, yt))
    dot(d, (-1.2, yt), True); dot(d, (-1.2, yb), True)
    text(d, (-1.2, yt - 0.55), "$+$"); text(d, (-1.2, 1.5), U1); text(d, (-1.2, yb + 0.55), "$−$")
    dot(d, (x + 1.1, yt), True); dot(d, (x + 1.1, yb), True)
    text(d, (x + 1.1, yt - 0.55), "$+$"); text(d, (x + 1.1, 1.5), U2); text(d, (x + 1.1, yb + 0.55), "$−$")
    text(d, (1.5, -0.8), "第 1 节", fontsize=12, color=MUTED); text(d, (4.5, -0.8), "第 2 节", fontsize=12, color=MUTED)
    save(d, "tp-ladder")


if __name__ == "__main__":
    tp_port(); tp_ex1(); tp_teq(); tp_pieq(); tp_term(); tp_cascade(); tp_series(); tp_parallel(); tp_gyrator(); tp_pi(); tp_hfe(); tp_ladder()
