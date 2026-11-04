"""构建后检查习题页与拓展补充页：公式外不应残留 $，所有 <img> 的 src 都应存在，列表项没有被打乱。
各栏目首页（index）没有题目，不统计答案数。

    NO_MKDOCS_2_WARNING=1 .venv/bin/mkdocs build && .venv/bin/python scripts/circuits/exercises/check_site.py [SITE_DIR]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = (Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site") / "basics" / "circuits"
bad = 0
pages = []
for sec in ("exercises", "extras"):
    SITE = BASE / sec
    pages += sorted(SITE.glob("*/index.html")) + [SITE / "index.html"]
for page in pages:
    s = page.read_text()
    main = s.split('<article', 1)[-1].split('</article>', 1)[0]
    body = re.sub(r'<(span|div) class="arithmatex">.*?</\1>', '', main, flags=re.S)
    body = re.sub(r'<(script|code|pre)\b.*?</\1>', '', body, flags=re.S)
    txt = re.sub(r'<[^>]+>', '', body)
    for line in txt.splitlines():
        if '$' in line:
            print(f"[stray $] {page.parent.name}: {line.strip()[:100]}"); bad += 1
    for src in re.findall(r'<img[^>]*src="([^"]+)"', main):
        if src.startswith("http") or src.startswith("data:"):
            continue
        if not (page.parent / src).resolve().exists():
            print(f"[missing img] {page.parent.name}: {src}"); bad += 1
    # Python-Markdown 的坑：列表项"文字 + 紧跟的子列表"后面再接段落/图片时，文字会被挪到子列表之后
    for _ in re.findall(r'<li>\s*<(?:ul|ol)>', main):
        print(f"[list reordered] {page.parent.name}"); bad += 1
    if page.parent.name in ("exercises", "extras"):
        print(f"{page.parent.name:24s} (栏目首页)")
        continue
    n = len(re.findall(r'<details class="success"', main))
    m = len(re.findall(r'<details class="note"', main))
    print(f"{page.parent.name:24s} answers={n} solutions={m}")
print("problems:", bad)
