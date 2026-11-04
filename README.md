# 知识库

个人知识库：大模型、强化学习、机器人、电路与控制，以及前沿技术与随笔。

🌐 **https://zsyverse.github.io/knowledge/**

基于 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)，push 到 `main` 后由 GitHub Actions 自动构建部署。

## 目录结构

```
docs/
├── ai/              AI：llm/ rl/ robot/
├── ai4ai/           AI4AI
├── basics/          基础：math/ control/ circuits/（知识点 / 习题 / 拓展补充）
├── engineering/     工程实践
├── frontier/        前沿视野
├── essays/          随笔：research/ life/
├── assets/          样式、脚本、本地 KaTeX
├── index.md         首页（文章数、最近更新自动生成）
└── guide.md         写作指南
hooks/section_index.py   模块文章列表、首页统计、草稿、图片懒加载
scripts/                 电路图生成与习题验算脚本
```

## 写作

在对应目录新建 `.md`（带 `date` / `description` / `tags` front matter）即可，导航和列表自动更新。详见 [docs/guide.md](docs/guide.md)。

```bash
uv venv && uv pip install -r requirements.txt
.venv/bin/mkdocs serve      # http://127.0.0.1:8000
```
