# 写作指南

## 新增一篇笔记

1. 在 `docs/` 对应目录下新建 `xxx.md`
2. 在 `mkdocs.yml` 的 `nav` 中加一行
3. `git add . && git commit -m "add xxx" && git push`，约 1 分钟后网站自动更新

## 本地预览

```bash
pip install -r requirements.txt
mkdocs serve        # 打开 http://127.0.0.1:8000
```

## 笔记模板

````markdown
---
tags:
  - 强化学习
---

# 标题

## 一句话总结

## 核心公式 / 方法

## 我的理解与疑问

## 参考
````

## 常用语法

| 效果 | 写法 |
| --- | --- |
| 行内公式 | `$E=mc^2$` |
| 块公式 | `$$ ... $$` |
| 提示框 | `!!! note "标题"` |
| 折叠框 | `??? tip "标题"` |
| 流程图 | ` ```mermaid ` 代码块 |
| 待办 | `- [ ] 事项` |
