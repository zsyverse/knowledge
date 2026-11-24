"""运行本目录全部 verify_*.py（任何断言失败即退出非零）。

    .venv/bin/python scripts/circuits/analog/verify_all.py
"""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for f in sorted(p for p in HERE.glob("verify_*.py") if p.name != "verify_all.py"):
    print(f"== {f.name}")
    runpy.run_path(str(f), run_name="__main__")
print("all analog checks passed")
