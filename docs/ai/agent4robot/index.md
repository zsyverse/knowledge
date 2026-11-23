# Agent4Robot

让大模型 agent 操控机器人：模型输出什么、由谁把它变成电机指令、怎么知道做对了。

这个模块关心的不是训练一个端到端的机器人策略，而是**把通用大模型（LLM / VLM / 编程 agent）接到机器人上**时的接口设计：给它什么工具，它一次能执行多少动作，执行后读什么回执，谁来判定成败。

## 建议阅读顺序

1. [方法谱系](landscape.md)：按模型输出的抽象程度，把 SayCan、Code as Policies、VoxPoser、MOKA、ReKep 到 2026 年的 CaP-X、URAI、InteractVLA 分成五层。
2. [接口与工具箱](interfaces.md)：direct、primitives、code、ORA 四种接口各给了模型哪些工具；`pixel_to_xyz` 的反投影公式和常见的坑。
3. [实测：Codex 在 LIBERO 上](case-study.md)：同一个模型、四种接口、40 个任务的结果，以及一段真实的“抓两个摩卡壶”程序。
4. [检查机制](verification.md)：动作前审核、感知检查、动作后回执、官方判定、运行护栏五层，以及失败检测和安全护栏的相关文献。
5. [方案总结](summary.md)：实测的 5 种接口和没实测的 2 种做法并排对照；模型输出接在控制链的哪一层，能不能直接给终点交给传统运控，归纳出的规律和下一步。
6. [术语与素材](glossary.md)：常用术语，以及 LIBERO / LIBERO-Pro 的 29 种食品素材图。

## 关于 ORA

模块里反复出现的 ORA（Open Robot-Use Agents）是 UC San Diego Hao AI Lab 开源的机器人 agent 运行框架（harness）[^ora]：不用 VLA、不做机器人训练，让通用模型零样本地观察、推理、写程序；每个运动都要经过 Supervisor 放行，成功检查对模型不可见，每次运行都会封存、可回放。它有工具调用和代码两种模式，官方在 RoboTwin、LIBERO-Pro、RoboDojo、RoboLab 上报告了结果[^ora-blog]。本模块的实测用的是它的 CPU 精简版，接 Codex 运行。

仿真环境本身（MuJoCo、robosuite、LIBERO 怎样推进物理和判分）见 [具身智能仿真是怎么做的](../robot/simulation.md)。

## 全部文章

<!-- articles -->

## 参考

[^ora]: Y. Yang, S. Chen, Z. Wang, J. Gao, H. Zhang. *ORA: Open Robot-Use Agents*. Hao AI Lab（UC San Diego）, 2026. 项目页 <https://fastrua.ai/ora/> · 代码 <https://github.com/fast-rua/ORA> · 两页论文 <https://fastrua.ai/ora/paper/ora-two-page.pdf> · 轨迹数据 <https://huggingface.co/datasets/FastRUA/ora-traces>
[^ora-blog]: FastRUA. *Introducing ORA*（2026-10 预览版）<https://fastrua.ai/blog/2026-10-ora/>；*ORA v0.1: Robot-use agents now write code, move smoothly…*（2026-11）<https://fastrua.ai/blog/2026-11-code-mode/>
