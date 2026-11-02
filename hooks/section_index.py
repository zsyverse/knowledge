"""把模块首页里的 <!-- articles --> 替换成该目录下所有文章的列表（按日期倒序）。"""
import datetime, os, re
from mkdocs.utils.meta import get_data

PLACEHOLDER = "<!-- articles -->"


def _article(path):
    with open(path, encoding="utf-8") as f:
        body, meta = get_data(f.read())
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
    arts.sort(key=lambda a: (a["date"], a["title"]), reverse=True)
    if not arts:
        return markdown.replace(PLACEHOLDER, "*还没有文章。*")
    items = []
    for a in arts:
        info = " · ".join(x for x in [a["date"], " ".join(f"`{t}`" for t in a["tags"])] if x)
        item = f"-   **[{a['title']}]({a['file']})**\n\n    <small>{info}</small>"
        if a["desc"]:
            item += f"\n\n    {a['desc']}"
        items.append(item)
    block = '<div class="grid cards" markdown>\n\n' + "\n\n".join(items) + "\n\n</div>"
    return markdown.replace(PLACEHOLDER, block)
