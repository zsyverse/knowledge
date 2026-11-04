"""拓展补充插图的公共设置：沿用习题插图的 excommon / solcommon 工具，输出到 images/extras/。

    .venv/bin/python scripts/circuits/extras/make_all.py        # 生成全部拓展补充插图
    .venv/bin/python scripts/circuits/extras/preview.py OUT a b  # 渲染成 PNG 检查

约定与习题插图相同：
- 二端元件一律 .endpoints(起点, 终点) 定位；
- SourceV 的 + 端在终点一侧；SourceI 的箭头由起点指向终点；
- 运放用 elm.Opamp：in1 为反相输入（−，上方），in2 为同相输入（+，下方）。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "exercises"))
sys.path.insert(0, str(HERE.parent))

from excommon import (elm, new_drawing, save as _save, save_fig as _save_fig, dot, text, cur, arrow,  # noqa: E402,F401
                      vsrc, isrc, ac_src, pdot, wire, plt, ROOT, OHM, ARW)
from solcommon import axes, note, C1, C2, C3, C4, INK, MUTED, GRID  # noqa: E402,F401

OUT = ROOT / "docs" / "basics" / "circuits" / "images" / "extras"
OUT.mkdir(parents=True, exist_ok=True)


def save(d, name):
    _save(d, name, out=OUT)


def save_fig(fig, name):
    _save_fig(fig, name, out=OUT)


def opamp(d, at_in1, flip=False):
    """放置理想运放，使反相输入端 in1 位于 at_in1。返回元件（可用 .in1/.in2/.out）。
    flip=True 时 + 端在上、− 端在下（in1 仍为 −）。"""
    e = elm.Opamp(leads=True, flip=flip).anchor("in1").at(at_in1)
    d.add(e)
    return e


def gnd(d, xy):
    d.add(elm.Ground().at(xy))


def port(d, xy, name=None, side="left", **kw):
    """端子（空心圆）并可标名称。"""
    dot(d, xy, True)
    if name:
        dx = -0.45 if side == "left" else 0.45
        text(d, (xy[0] + dx, xy[1]), name, **kw)


def vlabel(d, top, bot, name, x_off=0.0, plus="+", minus="−"):
    """在 top、bot 两点之间（竖直）标注 + name −（不画元件）。"""
    x = top[0] + x_off
    text(d, (x, top[1] - 0.35), plus)
    text(d, (x, (top[1] + bot[1]) / 2), name)
    text(d, (x, bot[1] + 0.35), minus)
