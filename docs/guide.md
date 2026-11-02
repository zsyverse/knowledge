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
| 数学基础 | `docs/basics/math/` |
| 控制理论 | `docs/basics/control/` |
| 工程实践 | `docs/engineering/` |
| 论文精读 | `docs/papers/` |
| 科研体悟 | `docs/essays/research/` |
| 人生感悟 | `docs/essays/life/` |

## 草稿

文章开头加 `draft: true`：`mkdocs serve` 本地预览时可见，推送后**不会**发布到网站（但文件本身仍在公开仓库里，真正私密的内容不要提交）。

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

## 论文笔记模板

````markdown
---
date: 2026-11-02
description: 一句话说清这篇论文做了什么
tags: [论文, 强化学习]
---

# 论文标题

!!! info "信息"
    **作者**：… **机构**：… **会议/年份**：… **链接**：[arXiv](https://arxiv.org/abs/xxxx)

## 解决什么问题

## 核心方法

## 关键结果

## 我的思考（亮点 / 局限 / 能借鉴什么）
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
