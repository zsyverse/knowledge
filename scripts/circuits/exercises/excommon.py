"""习题插图的公共设置：沿用 scripts/circuits/common.py 的绘图风格，输出到 images/ex/。

    .venv/bin/python scripts/circuits/exercises/make_all.py      # 生成全部习题插图
    .venv/bin/python scripts/circuits/exercises/preview.py a b   # 用 Chrome 把 SVG 渲染成 PNG 检查

约定（与笔记插图相同）：
- 二端元件一律 .endpoints(起点, 终点) 定位；
- SourceV / SourceSin 的 + 端在终点一侧（另用 label 标出 +、−）；
- SourceI / 受控电流源的箭头由起点指向终点。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from common import elm, new_drawing, dot, text, cur, vsrc_h, plt, ROOT  # noqa: E402,F401

OUT = ROOT / "docs" / "basics" / "circuits" / "images" / "ex"
OUT.mkdir(parents=True, exist_ok=True)

OHM = "\\,\\Omega"
ARW = dict(headwidth=0.3, headlength=0.38)


def save(d, name: str) -> None:
    path = OUT / f"{name}.svg"
    d.save(str(path), transparent=True)
    plt.close("all")
    prev = os.environ.get("CIRCUIT_PREVIEW")
    if prev:
        Path(prev).mkdir(parents=True, exist_ok=True)
        d.save(str(Path(prev) / f"{name}.png"), transparent=False, dpi=90)
        plt.close("all")
    print("wrote", path.relative_to(ROOT))


def save_fig(fig, name: str) -> None:
    path = OUT / f"{name}.svg"
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def arrow(d, p, q, label=None, loc="bot", **kw):
    """独立的电流参考箭头（不画导线），p→q。"""
    a = elm.Arrow(**ARW).endpoints(p, q)
    if label:
        a.label(label, loc=loc, **kw)
    d.add(a)
    return a


def vsrc(d, p, q, label, loc="top", ctrl=False):
    """直流电压源 p→q，+ 端在 q。圆内带 +/− 符号（schemdraw 默认），值标在一侧。"""
    e = (elm.SourceControlledV() if ctrl else elm.SourceV()).endpoints(p, q)
    if label:
        e.label(label, loc=loc)
    d.add(e)
    return e


def isrc(d, p, q, label, loc="top", ctrl=False):
    """电流源，箭头 p→q。"""
    e = (elm.SourceControlledI() if ctrl else elm.SourceI()).endpoints(p, q)
    if label:
        e.label(label, loc=loc)
    d.add(e)
    return e


def ac_src(d, p, q, label, loc="top"):
    """交流电压源 p→q，+ 端在 q，在圆外标出参考极性。"""
    sign_loc = "bot" if loc == "top" else "top"
    d.add(elm.SourceSin().endpoints(p, q).label(label, loc=loc).label(("−", "", "+"), loc=sign_loc, ofst=0.1))


def pdot(d, xy):
    """同名端标记。"""
    d.add(elm.Dot(radius=0.13).at(xy))


def m_arrow(d, p, q, label="$M$"):
    d.add(elm.Arrow(double=True, headwidth=0.25, headlength=0.3).endpoints(p, q).label(label))


def wire(d, *pts):
    for a, b in zip(pts, pts[1:]):
        d.add(elm.Line().endpoints(a, b))
