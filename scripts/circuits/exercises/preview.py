"""用无头 Chrome 把 images/ex/*.svg 按网页显示尺寸（宽 ≤520 px）渲染成 PNG，便于逐张检查。

    .venv/bin/python scripts/circuits/exercises/preview.py OUTDIR [name ...]

不给 name 时渲染全部。
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "docs" / "basics" / "circuits" / "images" / "ex"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def size(svg: Path):
    head = svg.read_text()[:2000]
    w = float(re.search(r'width="([\d.]+)pt"', head).group(1))
    h = float(re.search(r'height="([\d.]+)pt"', head).group(1))
    return w, h


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[2:] or [p.stem for p in sorted(SRC.glob("*.svg"))]
    for n in names:
        svg = SRC / f"{n}.svg"
        w, h = size(svg)
        dw = min(520, w * 4 / 3)
        dh = dw * h / w
        html = Path(tempfile.mkdtemp()) / "p.html"
        html.write_text(f'<html><body style="margin:10px;background:#fff">'
                        f'<img src="{svg.as_uri()}" style="width:{dw:.0f}px"></body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--screenshot={out / (n + '.png')}", f"--window-size={int(dw)+20},{int(dh)+20}",
                        "--force-device-scale-factor=1.5", "--allow-file-access-from-files", html.as_uri()],
                       capture_output=True)
        print("rendered", n)


if __name__ == "__main__":
    main()
