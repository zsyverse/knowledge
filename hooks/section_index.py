"""
1. 把模块首页里的 <!-- articles --> 替换成该目录下所有文章的列表（按日期倒序）。
2. front matter 带 draft: true 的文章：mkdocs serve 时可见，mkdocs build 时排除。
"""
import datetime, os, re
from mkdocs.utils.meta import get_data

PLACEHOLDER = "<!-- articles -->"
_serving = False


def on_startup(command, dirty):
    global _serving
    _serving = command == "serve"


def _meta(path):
    with open(path, encoding="utf-8") as f:
        return get_data(f.read())


def on_files(files, config):
    if _serving:
        return files
    for f in list(files.documentation_pages()):
        if _meta(f.abs_src_path)[1].get("draft"):
            files.remove(f)
    return files


def _article(path):
    body, meta = _meta(path)
    if meta.get("draft") and not _serving:
        return None
    title = meta.get("title")
    if not title:
        m = re.search(r"^#\s+(.+)$", body, re.M)
        title = m.group(1).strip() if m else os.path.basename(path)[:-3]
    date = meta.get("date")
    if isinstance(date, (datetime.date, datetime.datetime)):
        date = date.strftime("%Y-%m-%d")
    return {
        "file": os.path.basename(path),
        "title": title,
        "date": str(date or ""),
        "desc": meta.get("description", ""),
        "tags": meta.get("tags") or [],
        "draft": bool(meta.get("draft")),
    }


def on_page_markdown(markdown, page, config, files):
    if PLACEHOLDER not in markdown or not page.file.src_uri.endswith("index.md"):
        return markdown
    folder = os.path.dirname(page.file.abs_src_path)
    arts = [
        _article(os.path.join(folder, n))
        for n in os.listdir(folder)
        if n.endswith(".md") and n != "index.md"
    ]
    arts = [a for a in arts if a]
    # 日期新的在前；同一天的按该目录 .nav.yml 中的顺序
    order = {}
    nav_file = os.path.join(folder, ".nav.yml")
    if os.path.exists(nav_file):
        names = re.findall(r"^\s*-\s*(?:[^:\n]+:\s*)?([\w./-]+\.md)\s*$", open(nav_file, encoding="utf-8").read(), re.M)
        order = {n: i for i, n in enumerate(names)}
    arts.sort(key=lambda a: (order.get(a["file"], len(order)), a["title"]))
    arts.sort(key=lambda a: a["date"], reverse=True)
    if not arts:
        return markdown.replace(PLACEHOLDER, "*还没有文章。*")
    items = []
    for a in arts:
        info = " · ".join(x for x in [a["date"], " ".join(f"`{t}`" for t in a["tags"])] if x)
        if a["draft"]:
            info = "草稿 · " + info
        item = f"-   **[{a['title']}]({a['file']})**\n\n    <small>{info}</small>"
        if a["desc"]:
            item += f"\n\n    {a['desc']}"
        items.append(item)
    block = '<div class="grid cards" markdown>\n\n' + "\n\n".join(items) + "\n\n</div>"
    return markdown.replace(PLACEHOLDER, block)


# ---------------------------------------------------------------------------
# 3. 首页：<!-- recent --> 最近更新列表；<!-- count:目录 --> 该目录下文章数
# 4. 全站 <img> 默认懒加载
# ---------------------------------------------------------------------------
SKIP_TOP = {"index.md", "tags.md", "guide.md"}


def _all_articles(docs_dir):
    out = []
    for root, dirs, names in os.walk(docs_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("assets", "images")]
        for n in names:
            if not n.endswith(".md") or n == "index.md":
                continue
            rel = os.path.relpath(os.path.join(root, n), docs_dir).replace(os.sep, "/")
            if rel in SKIP_TOP:
                continue
            a = _article(os.path.join(root, n))
            if a:
                a["rel"] = rel
                out.append(a)
    return out


def _dir_titles(docs_dir):
    """从各级 .nav.yml 读出 目录 -> 显示名，如 ai/rl -> 强化学习"""
    titles = {}
    for root, dirs, names in os.walk(docs_dir):
        if ".nav.yml" not in names:
            continue
        base = os.path.relpath(root, docs_dir).replace(os.sep, "/")
        text = open(os.path.join(root, ".nav.yml"), encoding="utf-8").read()
        for title, d in re.findall(r"^\s*-\s*([^:\n]+?):\s*([\w-]+)\s*$", text, re.M):
            titles[(d if base == "." else f"{base}/{d}")] = title.strip()
    return titles


def _category(rel, titles):
    parts = rel.split("/")[:-1]
    names = [titles.get("/".join(parts[: i + 1])) for i in range(len(parts))]
    return " / ".join(n for n in names if n)


def _home_markdown(markdown, page, config):
    if page.file.src_uri != "index.md":
        return markdown
    docs_dir = config["docs_dir"]
    arts = _all_articles(docs_dir)

    def count(m):
        d = m.group(1).strip("/")
        if d == "all":
            return str(len(arts))
        if d == "tags":
            return str(len({t for a in arts for t in a["tags"]}))
        return str(sum(1 for a in arts if a["rel"].startswith(d + "/")))

    markdown = re.sub(r"<!--\s*count:([\w/-]+)\s*-->", count, markdown)
    latest = max((a["date"] for a in arts if a["date"]), default="")
    markdown = markdown.replace("<!-- updated -->", latest[5:].replace("-", "/") if latest else "—")
    if "<!-- recent -->" in markdown:
        titles = _dir_titles(docs_dir)
        arts.sort(key=lambda a: a["date"], reverse=True)
        rows = []
        per_dir, shown = {}, []
        for a in arts:  # 每个目录最多 3 篇，避免同一批文章刷屏
            d = a["rel"].rsplit("/", 1)[0]
            if per_dir.get(d, 0) < 3:
                per_dir[d] = per_dir.get(d, 0) + 1
                shown.append(a)
            if len(shown) == 10:
                break
        for a in shown:
            cat = _category(a["rel"], titles)
            rows.append(f'- <time>{a["date"]}</time> [{a["title"]}]({a["rel"]}) <span class="cat">{cat}</span>')
        markdown = markdown.replace("<!-- recent -->", "\n".join(rows))
    return markdown


_orig_on_page_markdown = on_page_markdown


def on_page_markdown(markdown, page, config, files):  # noqa: F811
    markdown = _home_markdown(markdown, page, config)
    return _orig_on_page_markdown(markdown, page, config, files)


_ICON_CAL = '<svg viewBox="0 0 24 24"><path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2m0 16H5V9h14zM5 7V6h14v1z"/></svg>'
_ICON_TXT = '<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zm4 18H6V4h7v5h5zM8 12h8v2H8zm0 4h8v2H8z"/></svg>'
_ICON_CLK = '<svg viewBox="0 0 24 24"><path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16m0-18a10 10 0 1 1 0 20 10 10 0 0 1 0-20m.5 5v5.25l4.5 2.67-.75 1.23L11 13V7z"/></svg>'


def _reading_stats(md):
    """中文按字、英文按词统计；忽略代码块、公式、HTML 注释与链接地址"""
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    md = re.sub(r"(```|~~~).*?\1", "", md, flags=re.S)
    md = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", "", md, flags=re.S)
    md = re.sub(r"<!--.*?-->|<[^>]+>|\]\([^)]*\)", "", md, flags=re.S)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", md))
    words = len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*", md))
    return cjk + words, max(1, round(cjk / 400 + words / 220))


def _page_meta(page):
    if page.file.src_uri.endswith("index.md") or page.file.src_uri in SKIP_TOP:
        return ""
    date = page.meta.get("date")
    if isinstance(date, (datetime.date, datetime.datetime)):
        date = date.strftime("%Y-%m-%d")
    n, mins = _reading_stats(page.markdown or "")
    if n < 80:
        return ""
    parts = []
    if date:
        parts.append(f"<span>{_ICON_CAL}{date}</span>")
    parts.append(f"<span>{_ICON_TXT}约 {n:,} 字</span>")
    parts.append(f"<span>{_ICON_CLK}{mins} 分钟读完</span>")
    return '<div class="page-meta">' + "".join(parts) + "</div>"


def on_page_content(html, page, config, files):
    meta = _page_meta(page)
    if meta:
        html, k = re.subn(r"</h1>", lambda m: m.group(0) + meta, html, count=1)
        if not k:
            html = meta + html
    return re.sub(r"<img(?![^>]*\sloading=)", '<img loading="lazy" decoding="async"', html)
