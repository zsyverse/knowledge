"""一次性生成 docs/basics/circuits/images/ 下的全部插图。

    .venv/bin/python scripts/circuits/make_all.py
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for name in ("fig_basics", "fig_equiv", "fig_analysis", "fig_theorems", "fig_dynamic",
             "fig_ac", "fig_coupled", "plots"):
    runpy.run_path(str(HERE / f"{name}.py"), run_name="__main__")
