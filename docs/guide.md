# 写作指南

## 新增一篇文章

1. 在 `docs/` 对应模块的文件夹下新建 `xxx.md`（如 `docs/ai/rl/dapo.md`），**不用改任何配置**
2. 它会自动出现在左侧导航，以及该模块首页的「全部文章」列表里（按日期倒序）
3. `git add . && git commit -m "add xxx" && git push`，约 1 分钟后网站自动更新

短的速查笔记和长文都这样写，没有区别；长文可以参考 [从 PPO 到 GRPO](ai/rl/ppo-to-grpo.md) 的结构。

想调整导航里的顺序：编辑该文件夹下的 `.nav.yml`。新建一个小类：建文件夹，放一个带 `<!-- articles -->` 的 `index.md` 和一个 `.nav.yml`（照抄已有的），再在上一级的 `.nav.yml` 里加一行。

## 目录对照

| 大类 | 文件夹 |
| --- | --- |
| LLM/VLM | `docs/ai/llm/` |
| 强化学习 | `docs/ai/rl/` |
| Robot | `docs/ai/robot/` |
| AI4AI | `docs/ai4ai/` |
| 数学基础 | `docs/basics/math/` |
| 控制理论 | `docs/basics/control/` |
| 电路 | `docs/basics/circuits/` |
| 工程实践 | `docs/engineering/` |
| 前沿视野 | `docs/frontier/` |
| 科研体悟 | `docs/essays/research/` |
| 人生感悟 | `docs/essays/life/` |

## 草稿

文章开头加 `draft: true`：`mkdocs serve` 本地预览时可见，推送后**不会**发布到网站（但文件本身仍在公开仓库里，真正私密的内容不要提交）。

## 网站功能

- **图片点击放大**：所有图片都可以点开查看大图；不想被放大的图片加 `{ .no-zoom }`
- **首页自动统计**：各分类文章数和「最近更新」由 front matter 的 `date` 自动生成，所以记得写日期
- **国内访问**：字体用系统字体、公式库 KaTeX 放在本站，不依赖 Google Fonts / jsDelivr
- **电路图**：用 `{ .circuit }` 类，暗色模式下会自动反色

## 本地预览

```bash
pip install -r requirements.txt
mkdocs serve        # 打开 http://127.0.0.1:8000
```

## 笔记模板

````markdown
---
date: 2026-11-02
description: 一句话摘要，显示在模块首页的列表里
tags:
  - 强化学习
---

# 标题

!!! abstract "TL;DR"
    一段话总结。

## 核心公式 / 方法

## 我的理解与疑问

## 参考
````

## 前沿视野模板

````markdown
---
date: 2026-11-02
description: 一句话说清它是什么
tags: [论文, Robot]      # 来源类型 + 领域
---

# 标题

!!! info "来源"
    **类型**：论文 / 开源项目 / 产品 / 博客 / 演讲　**出处**：…　**链接**：[原文](https://...)

## 它是什么

## 为什么值得关注

## 核心思路

## 对我的启发
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
