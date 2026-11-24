"""模拟电子技术笔记插图的公共设置：沿用拓展补充的 xcommon 工具，输出到 images/analog/。

    .venv/bin/python scripts/circuits/analog/make_all.py          # 生成全部模电插图
    CIRCUIT_PREVIEW=<目录> .venv/bin/python scripts/circuits/analog/fig_xxx.py   # 同时输出 PNG 预览

约定与拓展补充相同：
- 二端元件一律 .endpoints(起点, 终点) 定位；
- SourceV 的 + 端在终点一侧；SourceI 的箭头由起点指向终点；
- 运放用 opamp()：in1 为反相输入（−），in2 为同相输入（+）；
- 晶体管用 schemdraw 的 elm.BjtNpn / BjtPnp / NFet / PFet / JFetN 等，用 .anchor(...).at(...) 定位。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "extras"))
sys.path.insert(0, str(HERE.parent / "exercises"))

import xcommon as _x  # noqa: E402
from xcommon import (elm, new_drawing, dot, text, cur, arrow, vsrc, isrc, ac_src, pdot, wire, plt,  # noqa: E402,F401
                     ROOT, OHM, ARW, axes, note, C1, C2, C3, C4, INK, MUTED, GRID, opamp, gnd, port, vlabel)
from excommon import save as _save, save_fig as _save_fig  # noqa: E402

OUT = ROOT / "docs" / "basics" / "circuits" / "images" / "analog"
OUT.mkdir(parents=True, exist_ok=True)


def save(d, name):
    _save(d, name, out=OUT)


def save_fig(fig, name):
    _save_fig(fig, name, out=OUT)
