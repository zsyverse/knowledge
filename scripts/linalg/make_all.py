"""一次性生成 docs/basics/math/linalg/images/ 下的全部插图，并跑完所有验算脚本。

    .venv/bin/python scripts/linalg/make_all.py            # 画图 + 验算
    .venv/bin/python scripts/linalg/make_all.py verify     # 只验算
    .venv/bin/python scripts/linalg/make_all.py fig        # 只画图

fig_<章>.py 负责画图，verify_<章>.py 用 SymPy / NumPy 断言该章例题里的每个数。
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

what = sys.argv[1] if len(sys.argv) > 1 else "all"
patterns = {"fig": ["fig_*.py"], "verify": ["verify_*.py"], "all": ["fig_*.py", "verify_*.py"]}[what]
for pat in patterns:
    for script in sorted(HERE.glob(pat)):
        print(f"== {script.name}")
        runpy.run_path(str(script), run_name="__main__")
