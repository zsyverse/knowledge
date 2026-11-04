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
