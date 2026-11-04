"""电路笔记插图的公共设置。

所有电路图用 schemdraw（matplotlib 后端）绘制，输出为文字转路径的 SVG，
放在 docs/basics/circuits/images/。运行方式：

    .venv/bin/python scripts/circuits/make_all.py

环境变量 CIRCUIT_PREVIEW=<目录> 时，额外输出 PNG 预览，方便检查。
"""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "basics" / "circuits" / "images"
OUT.mkdir(parents=True, exist_ok=True)

matplotlib.rcParams.update(
    {
        "svg.fonttype": "path",
        "mathtext.fontset": "stix",
        "font.family": "sans-serif",
        "font.sans-serif": ["Heiti TC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"],
        "axes.unicode_minus": False,
    }
)
schemdraw.use("matplotlib")

FONTSIZE = 15
UNIT = 3.0


def new_drawing() -> schemdraw.Drawing:
    d = schemdraw.Drawing(show=False)
    d.config(unit=UNIT, fontsize=FONTSIZE, lw=1.4, font="sans-serif", mathfont="stix")
    return d


def save(d: schemdraw.Drawing, name: str) -> None:
    path = OUT / f"{name}.svg"
    d.save(str(path), transparent=True)
    plt.close("all")
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        d.save(str(Path(prev) / f"{name}.png"), transparent=False, dpi=90)
        plt.close("all")
    print("wrote", path.relative_to(ROOT))


def save_fig(fig: plt.Figure, name: str) -> None:
    path = OUT / f"{name}.svg"
    fig.savefig(path, transparent=True, bbox_inches="tight")
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(prev) / f"{name}.png", dpi=90, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def dot(d, xy, open_=False):
    """节点圆点；open_=True 为端子（空心）。"""
    d.add(elm.Dot(open=open_).at(xy))


def text(d, xy, s, **kw):
    """在指定坐标放置一段文字。"""
    kw.setdefault("halign", "center")
    kw.setdefault("valign", "center")
    d.add(elm.Label().at(xy).label(s, **kw))


__all__ = ["elm", "new_drawing", "save", "save_fig", "dot", "text", "cur", "vsrc_h", "plt"]


def cur(d, p, q, label=None, loc="top", frac=0.5, **kw):
    """画导线 p→q，并在其上（frac 位置）画指向 q 的电流箭头。"""
    import math

    d.add(elm.Line().endpoints(p, q))
    (x1, y1), (x2, y2) = p, q
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    mx, my = x1 + (x2 - x1) * frac, y1 + (y2 - y1) * frac
    a = elm.Arrow(headwidth=0.34, headlength=0.42).endpoints((mx - 0.3 * ux, my - 0.3 * uy), (mx + 0.21 * ux, my + 0.21 * uy))
    if label:
        a.label(label, loc=loc, **kw)
    d.add(a)
    return a


def vsrc_h(d, p, q, value, ctrl=False):
    """水平放置的电压源：p 端为 +，q 端为 −（圆内不画符号，极性标在圆外）。"""
    e = (elm.SourceControlled() if ctrl else elm.Source()).endpoints(p, q)
    e.label(value, loc="top")
    e.label(("+", "", "−"), loc="bot", ofst=0.15)
    d.add(e)
    return e
