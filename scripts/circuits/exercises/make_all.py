"""一次性生成 docs/basics/circuits/images/ex/ 下的全部习题插图（运行本目录所有 fig_*.py）。

    .venv/bin/python scripts/circuits/exercises/make_all.py
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

for f in sorted(HERE.glob("fig_*.py")):
    runpy.run_path(str(f), run_name="__main__")
