# 写作指南

## 新增一篇笔记

1. 在 `docs/` 对应目录下新建 `xxx.md`
2. 在 `mkdocs.yml` 的 `nav` 中加一行
3. `git add . && git commit -m "add xxx" && git push`，约 1 分钟后网站自动更新

## 写一篇博客长文

在 `docs/blog/posts/` 下新建 `.md` 文件，**不用改 nav**，会自动按日期排列，并生成归档和分类页面：

````markdown
---
date: 2026-11-02
slug: my-post          # 网址里显示的英文名
authors: [zsyverse]
categories: [强化学习]
draft: true            # 写完前先设为草稿，不会发布到网站；写完删掉这一行
---

# 标题

!!! abstract "TL;DR"
    一段话总结。

<!-- more -->

正文……（`<!-- more -->` 之前的内容会显示在博客列表页作为摘要）
````

**笔记 vs 博客**：笔记是按分类整理的速查手册，会持续修改；博客是有日期的完整长文。

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
