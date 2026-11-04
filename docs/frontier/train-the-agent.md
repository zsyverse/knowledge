---
date: 2026-11-04
description: Hugging Face 的 Sergio Paniego 讲 2026 年怎么训练 Agent：SFT、蒸馏、GRPO、环境中 RL、跨 harness RL 五种方法，以及 TRL + OpenEnv 的实现。
tags:
  - 演讲
  - Agent
  - 强化学习
  - 大模型
---

# Train the agent, not just the model

!!! info "来源"
    **类型**：演讲幻灯片（20 页）　**作者**：Sergio Paniego（[@sergiopaniego](https://huggingface.co/sergiopaniego)，Hugging Face）　**时间**：2026 年 10 月

    **原网址**：<https://huggingface.co/spaces/sergiopaniego/train-the-agent-slides>

    **在线幻灯片**：<https://sergiopaniego-train-the-agent-slides.static.hf.space/>

    **下载**：[train-the-agent-slides.pptx](assets/train-the-agent/train-the-agent-slides.pptx)（本站存档，版权归原作者）

!!! abstract "TL;DR"
    **Agent = 模型 + harness**（负责循环调用、管理工具、拼上下文、解析回复的外壳）。同一个模型换 harness，表现可以差一倍，所以要训练的是 Agent 整体，而不只是模型。后训练有五种手段：**模仿（SFT）、压缩（蒸馏）、奖励（GRPO）、在环境里行动（RL + 环境）、通过 harness 训练（跨 harness RL）**，可以组合使用；Hugging Face 用 TRL（训练）+ OpenEnv（环境）把它们统一起来。

## 核心观点

### 1. Agent 是模型加 harness

harness（如 Claude Code、Codex、OpenCode、Mini-SWE-Agent）做四件事：**跑循环**（反复调用模型、决定何时停）、**管工具**（决定有哪些工具并执行调用）、**写上下文**（系统提示、历史、压缩）、**读回复**（按自己的格式解析，不合格就拒绝）。

同样的权重、不同的 harness：LFM2.5-2.6B 在 Mini-SWE-Agent 里解决 62% 的任务，在 Claude Code 里只有 33%。

### 2. 五种训练方法

| 方法 | 学习信号 | 一句话 | TRL 中的实现 |
| --- | --- | --- | --- |
| 模仿 | SFT on agent traces | 模仿演示者过去的 Agent 会话轨迹 | `SFTTrainer` |
| 压缩 | 蒸馏 | 教师模型给每个 token 的概率分布 | `DistillationTrainer` |
| 奖励 | 可验证奖励的 RL | 能运行的检查：测试是否通过 | `GRPOTrainer` |
| 行动 | 环境中的 RL | 带工具的沙箱，循环由 trainer 驱动 | `GRPOTrainer` + OpenEnv |
| harness | 通过 harness 的 RL | 真实 Agent 跑自己的循环 | `AsyncGRPOTrainer` + OpenEnv |

前三种改变**训练信号**，后两种把训练搬进模型**真正行动的循环**里。

=== "SFT"

    把整段 Agent 会话（用户 → 模型调用工具 → 工具结果 → ……）存成聊天格式数据，用 `assistant_only_loss=True` **只在模型自己的回合上算 loss**，工具结果只作为上下文（参见 [SFT 笔记](../ai/llm/sft.md)）。

    局限：模型最多学到轨迹的水平，而好的轨迹很少展示「如何从错误中恢复」。

=== "蒸馏"

    SFT 只告诉模型「正确的那一个 token」，教师则给出**每个候选 token 的概率**。默认 **on-policy**：学生自己生成，教师给每个 token 打分，学生在自己犯错的位置被纠正。

    教师可以是更大的模型、合并多个 RL 专家（MOPD），或带提示的模型自身（自蒸馏）。限制：师生要**同一个 tokenizer**，学生上限受教师约束。

=== "GRPO"

    同一任务采样一组回答（如 8 个），奖励 = 通过的隐藏测试比例；**组内平均作为基线**，高于平均的回答概率上调、低于的下调，因此不需要单独训练价值模型（详见 [RLHF / DPO / GRPO](../ai/rl/rlhf.md) 和 [从 PPO 到 GRPO](../ai/rl/ppo-to-grpo.md)）。

    奖励可以是测试、编译器或已知答案；没有演示者，所以不受演示者水平限制。

=== "环境中 RL"

    OpenEnv 给每个环境统一的 `reset` / `step` 接口，以 Hub Space 的形式提供服务。模型在沙箱里多轮调用工具（如运行 Python、看报错、修改、再运行），最后由 `get_reward()` 跑隐藏测试给分——奖励在多轮工具使用之后才出现。

=== "跨 harness RL"

    真实的编码 Agent 自己驱动循环，trainer 不在环里。解决办法是 **capture proxy**：Agent 以为在调用普通的模型 API，代理把请求转发给 vLLM，同时记录每一轮的 token id 和 logprob，这正是 GRPO 训练所需的数据；`AsyncGRPOTrainer` 边生成边训练。

    前沿实验室已经在多个真实 harness 上训练编码模型：Kimi K3、Qwen3-Coder-Next、MiMo-V2.6、Poolside Laguna、Liquid LFM2.5。

### 3. 实验：跨 harness RL 的效果

| 项目 | 设置 |
| --- | --- |
| 模型 | LFM2.5-2.6B（Liquid AI） |
| harness | OpenCode、Claude Code、Codex、Mini-SWE-Agent，均未修改 |
| 任务 | SmolDataEnvs：来自真实 Kaggle notebook 的数据分析问题，1000 训练 / 250 留出 |
| 奖励 | 答对得 1，工具调用越少额外加分（最多 0.1） |
| 训练 | `AsyncGRPOTrainer`，1000 步，2 张 H100，每次 rollout 一个 E2B 沙箱 |

结果（250 道留出任务，4 个 harness 平均）：**42% → 54%**；在都能解出的任务上**工具调用减少 31%**；**4 个 harness 全部提升**。只在 OpenCode 里训练的对照组，在 OpenCode 中达到 58%，但在其他 harness 上提升小得多。

### 4. 怎么选

| 你手里有什么 | 用什么 |
| --- | --- |
| 想要的 Agent 的轨迹 | SFT |
| 同 tokenizer 的更强模型 | 蒸馏 |
| 能验证答案 | GRPO |
| 任务需要多步工具调用 | GRPO + OpenEnv |
| 用户在某个 harness 里使用它 | 通过 harness 训练 |

这些方法可以组合：例如 DeepSeek-V4 按领域先 SFT 再 GRPO，最后用 on-policy 蒸馏合并各专家。

## 我的思考

<!-- 在这里写下你的想法 -->

## 幻灯片

![第 1 页](assets/train-the-agent/slide-01.jpg){ loading=lazy }

![第 2 页](assets/train-the-agent/slide-02.jpg){ loading=lazy }

![第 3 页](assets/train-the-agent/slide-03.jpg){ loading=lazy }

![第 4 页](assets/train-the-agent/slide-04.jpg){ loading=lazy }

![第 5 页](assets/train-the-agent/slide-05.jpg){ loading=lazy }

![第 6 页](assets/train-the-agent/slide-06.jpg){ loading=lazy }

![第 7 页](assets/train-the-agent/slide-07.jpg){ loading=lazy }

![第 8 页](assets/train-the-agent/slide-08.jpg){ loading=lazy }

![第 9 页](assets/train-the-agent/slide-09.jpg){ loading=lazy }

![第 10 页](assets/train-the-agent/slide-10.jpg){ loading=lazy }

![第 11 页](assets/train-the-agent/slide-11.jpg){ loading=lazy }

![第 12 页](assets/train-the-agent/slide-12.jpg){ loading=lazy }

![第 13 页](assets/train-the-agent/slide-13.jpg){ loading=lazy }

![第 14 页](assets/train-the-agent/slide-14.jpg){ loading=lazy }

![第 15 页](assets/train-the-agent/slide-15.jpg){ loading=lazy }

![第 16 页](assets/train-the-agent/slide-16.jpg){ loading=lazy }

![第 17 页](assets/train-the-agent/slide-17.jpg){ loading=lazy }

![第 18 页](assets/train-the-agent/slide-18.jpg){ loading=lazy }

![第 19 页](assets/train-the-agent/slide-19.jpg){ loading=lazy }

![第 20 页](assets/train-the-agent/slide-20.jpg){ loading=lazy }

