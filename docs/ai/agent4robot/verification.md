---
date: 2026-11-19
description: agent 操控机器人时，怎么知道做对了、怎么防止做错？分五层：动作前审核、感知结果检查、动作后测量回执、官方任务判定、运行层面的护栏与审计。并对照 Inner Monologue、REFLECT、Code-as-Monitor、RoboGuard、AutoRT 等失败检测与安全护栏工作。
tags:
  - 具身智能
  - Agent
  - 机器人
  - 安全
---

# 检查机制：怎么知道做对了，怎么防止做错

!!! abstract "要点"
    让 agent 操控机器人，检查要分五层，越往前越能防患于未然：

    1. **动作前**：Supervisor 审核工作空间、过期观测、关节极限、自碰撞；先预览再提交。
    2. **感知结果**：反投影前检查深度是否连续、是否有效，不合格就拒绝。
    3. **动作后**：读测量回执，比如 `reached`、位置误差、夹爪开度，而不是只看图。
    4. **任务判定**：只认环境的官方判定，模型“觉得做完了”不算数。
    5. **运行层面**：预算、沙箱隔离、审计日志、看门狗、特权隔离。

    文献里对应的两条线：**失败检测**（Inner Monologue、REFLECT、Code-as-Monitor）和**安全护栏**（AutoRT 的机器人宪法、RoboGuard 的时序逻辑约束）。

## 1. 为什么要专门设计检查

在[实测](case-study.md)里，code 方法写的程序第一次抓壶时空抓了，但程序没有停，照样执行“抬起”。模型是读了 stdout 里的 `gripper_opening 0.0011` 才知道失败的。如果回执里没有这个数，或者模型没去读，失败就会一路传下去。

CodeActionBench 分析 675 次尝试的轨迹，把**完成判断**列为三大失败模式之一：有些任务机器人动作都做完了，任务本身却没成功[^cab]。Gemini Robotics-ER 2 的模型卡里，“任务进度分类”的准确率只有 57.4%[^gemini-er2]。让 VLM 看图判断“做成了没有”本身就不可靠，所以检查不能只靠模型看图。

## 2. 第一层：动作前的检查

只有 ORA 有这一层。按 ORA 官方的说法，模型负责观察、推理和写程序，Supervisor 放行每一个运动；机器人和成功检查都在信任边界之后，对模型不可见[^ora]。

- **Supervisor 审核**：每个改变状态的动作都要先作为一份版本化的提议提交，通过后才由环境执行。
- **拒绝码**举例：

    | 拒绝码 | 含义 |
    | --- | --- |
    | `outside_workspace` | 超出工作空间包络（LIBERO 是 x∈[−0.6, 0.6]、y∈[−0.5, 0.5]、z∈[−0.1, 1.3] 米） |
    | `stale_observation` | 基于过期的观测做决策 |
    | `joint_limit` | 超出关节极限 |
    | `self_collision_path` | 路径上会自碰撞 |
    | `start_unreachable` | 起点不可达 |
    | `gripper_drive_limit` | 夹爪驱动超限 |

- **观测绑定**：每个动作都绑定到一次具体的观测。相机一动，旧像素和旧标点就失效（`stale_point`），防止拿过时信息做决策。
- **预览**：`preview_move` 先把候选位姿画在图上，让模型看清楚再提交。
- 注意：工作空间包络只是硬性的工程边界，**不保证可达，也不保证无碰撞**。

**文献对照：安全护栏。** 动作前审核在文献里通常叫 guardrail：

- **AutoRT**[^autort] 给大规模部署的机器人定了一套“机器人宪法”：基础规则（不伤害人类）、安全规则（不碰人、动物、尖锐物体和电器）、本体规则（不搬超过能力的东西）。LLM 提出的任务先由另一个 LLM 按宪法筛一遍。
- **RoboGuard**[^roboguard] 把安全规则写成线性时序逻辑（LTL）约束：一个可信的 LLM 根据当前环境把通用规则落地成具体约束（比如检测到人时生成 `!goto(person)`），再用时序逻辑控制综合，在满足约束的前提下尽量保留原计划。它主要针对越狱攻击：即使规划 LLM 被诱导生成危险计划，护栏也能拦住。

ORA 的 Supervisor 是更底层的版本：不审核“这个任务该不该做”，而是审核“这个动作在几何和运动学上是否合法”。两者互补。

## 3. 第二层：感知结果的检查

- **ORA `mark_point`**：检查深度是否连续、支持样本是否足够、深度值是否有效，不合格就拒绝并说明原因（`depth_discontinuity`、`insufficient_depth_support`、`invalid_depth`）。
- **其他接口没有这层**：`pixel_to_xyz` 打到边缘或背景时会照样返回一个错误的坐标。

在[接口与工具箱](interfaces.md#6-三个坑附数值验证)的数值实验里，物体边缘的邻域只要有 5/9 个像素落在背景上，中位数深度就会跳到背景，反投影误差达 25 cm。这种错误在下游很难发现：`move_to` 会“成功”到达一个错误的位置，然后空抓。在感知这一层拦住，成本最低。

## 4. 第三层：动作后的测量回执

所有接口都会返回实测值，模型据此判断：

| 信号 | 含义 |
| --- | --- |
| `reached: False` 且 `position_error_m` 较大 | 被挡住了（比如压在物体顶上），或者够不到 |
| 闭合后夹爪开度约 0.001 m | 空抓 |
| 闭合后开度约 0.014–0.07 m | 夹住了东西，开度大致等于物体宽度 |
| 抬起后开度变成约 0 | 物体滑掉了 |
| ORA `gripper_stalled_before_target` | 闭合被物体挡住，符合“夹住了”，但还要抬起来看一眼才能确认 |

夹爪开度是最便宜也最可靠的抓取检测：比看图判断“夹住没有”准得多。设计接口时，**把这类可直接判读的测量值放进回执**，比让模型从图像里推断更稳。

**文献对照：失败检测。**

- **Inner Monologue**[^innermono] 最早把成功检测器的输出（“抓取成功 / 失败”）和场景描述作为文字反馈给 LLM，让它重试或改计划，相当于本节回执的雏形。
- **REFLECT**[^reflect] 把机器人的多模态感知（视觉、声音、本体状态）压缩成分层的文字摘要，让 LLM 定位失败发生在哪一步、解释原因，再据此生成纠正计划。
- **Code-as-Monitor**[^cam] 让 VLM 写监控代码：把相关物体抽象成点、线、面等几何元素，把失败条件写成时空约束。代码生成后在跟踪到的几何元素上实时运行，不用每帧都调 VLM，既能在失败发生后报警（reactive），也能在快要失败时提前预警（proactive）。
- **VLM 当成功检测器**[^successvqa]：把“任务成功了吗”当成视觉问答来微调。效果依赖训练分布，换场景就会掉点。

Code-as-Monitor 和 code 接口的思路很像：既然模型能写执行程序，也能写检查程序。我们实测里的 code 程序只顺序执行、从不检查中间结果；如果让模型在每个 `move_to` 后加一行 `assert r['reached']`，空抓就能在程序内部被发现。

## 5. 第四层：任务成功只认官方判定

- **成功只由 benchmark 的判定决定**：LIBERO 的 `env._check_success()`，判定条件见 [具身智能仿真是怎么做的](../robot/simulation.md#8-闭环π05-一次抓空之后怎么继续)。
- **direct / primitives / code**：每一步仿真后都检查，成功的瞬间回合结束，工具返回 `episode_over, official_success: true`。`finish` 只能用来放弃，不能自己宣布成功。
- **ORA**：`check_task` 读取官方判定，但不暴露判定条件；`finish_episode` 只有拿到成功信号后才能声明成功；最终结果由评估阶段单独核验并密封（哈希绑定证据）。

不暴露判定条件，是因为如果模型知道“碗心与盘心水平距离 < 3 cm 即成功”，它可能会针对判定条件优化，而不是真正完成任务，这在强化学习里叫奖励黑客（reward hacking）。CodeActionBench 也用了隐藏的物理结果验证器[^cab]。反过来，官方判定也不一定完全可靠：ORA 团队就指出 benchmark 的官方成功检查可能高估任务完成度[^ora-blog]。我们的实测里也有类似情况：第二个壶刚碰到灶台就判成功，夹爪还没张开。

## 6. 第五层：运行层面的护栏和审计

| 护栏 | 我们实测里的做法 |
| --- | --- |
| **预算** | direct / primitives / code：10,000 控制步、250 次工具调用、30 分钟；ORA：80 次机器人决策、200 次模型调用 |
| **隔离** | Codex 运行在只读沙箱里，只能通过 MCP 工具操作机器人；环境服务用随机 Bearer key 鉴权；`run_code` 每次都是新进程 |
| **审计** | 记录 Codex 有没有调用 MCP 以外的东西（结果为 0）；检查 449 段程序有没有碰文件、os、网络或环境内部（结果为 0）；每个回合保存调用日志、视频和轨迹页 |
| **看门狗** | 超过 420 秒没有动静就终止并恢复会话 |
| **特权隔离** | 策略拿不到真值、分割标注、接触信息、任务源码或成功判定条件；唯一例外是标明为 oracle 的 code_oracle |

code 接口能执行任意 Python，所以**审计程序内容**是必要的：要确认它没有通过读文件、访问环境内部变量来“作弊”拿到真值。实测中 449 段程序全部干净。

## 7. 小结：五层各防什么

| 层 | 防的是什么 | 代价 | 我们实测里谁有 |
| --- | --- | --- | --- |
| 动作前审核 | 危险或不合法的动作 | 每个动作多一次审核，调用和用时增加 | ORA |
| 感知检查 | 错误的 3D 坐标流入下游 | 偶尔拒绝可用的点，需要换点 | ORA |
| 动作后回执 | 失败被忽略、错误累积 | 几乎为零，只要回执里有测量值 | 全部 |
| 官方判定 | 模型自以为成功 | 无 | 全部 |
| 运行护栏 | 失控、作弊、越权 | 工程成本 | 全部 |

仿真里出错只是重来一次，所以前两层主要体现为成本（ORA 的调用次数和用时都高于 code）。到了真机上，一次错误的下压可能损坏设备，这两层才真正有用。

## 参考

[^cab]: *CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation*. arXiv:2609.33807, 2026.
[^gemini-er2]: Google DeepMind. *Gemini Robotics ER 2* 模型卡, 2026-07-30. <https://deepmind.google/models/model-cards/gemini-robotics-er-2/>
[^autort]: M. Ahn et al. *AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents*. arXiv:2401.12963, 2024.
[^roboguard]: Z. Ravichandran et al. *Safety Guardrails for LLM-Enabled Robots*（RoboGuard）. IEEE RA-L 2026. arXiv:2503.07885
[^innermono]: W. Huang et al. *Inner Monologue: Embodied Reasoning through Planning with Language Models*. CoRL 2022. arXiv:2207.05608
[^reflect]: Z. Liu, A. Bahety, S. Song. *REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction*. CoRL 2023. arXiv:2306.15724
[^cam]: E. Zhou et al. *Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection*. CVPR 2025. arXiv:2412.04455
[^successvqa]: Y. Du et al. *Vision-Language Models as Success Detectors*. CoLLAs 2023. arXiv:2303.07280
[^ora]: Y. Yang, S. Chen, Z. Wang, J. Gao, H. Zhang. *ORA: Open Robot-Use Agents*. Hao AI Lab（UC San Diego）, 2026. 项目页 <https://fastrua.ai/ora/> · 代码 <https://github.com/fast-rua/ORA> · 两页论文 <https://fastrua.ai/ora/paper/ora-two-page.pdf> · 轨迹数据 <https://huggingface.co/datasets/FastRUA/ora-traces>
[^ora-blog]: FastRUA. *Introducing ORA*（2026-10 预览版）<https://fastrua.ai/blog/2026-10-ora/>；*ORA v0.1: Robot-use agents now write code, move smoothly…*（2026-11）<https://fastrua.ai/blog/2026-11-code-mode/>
