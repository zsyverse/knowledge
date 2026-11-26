---
date: 2026-11-26
description: 以控制抽象层级（VLM 直接输出什么、底层由谁接管）为纵轴，将零样本调用、SFT/轨迹蒸馏与强化学习纳入同一二维分类框架，并用同一个操作任务直观对比六条路线的分工边界。
tags:
  - 具身智能
  - VLM
  - VLA
  - Agent
  - 综述
---

# 全景总纲：控制抽象 × 训练范式的统一框架

!!! abstract "要点"
    梳理“视觉语言模型（VLM）怎么控制机器人”时，最容易混淆两个正交的问题：

    1. **控制抽象层级（纵轴：接口切在哪一层）**——每一轮推理结束时，VLM 吐出来的到底是什么（位姿数字、图上的点/轨迹、工具调用与原语脚本、原生 ROS 2 控制循环、给底层策略的子任务/审查指令，还是高频电机 Token），剩下的几何解算与高频伺服由谁接管？
    2. **训练与适应范式（横轴：模型权重怎么来）**——是直接零样本调用预训练通用大模型（Zero-Shot），还是用示范/交互轨迹做监督微调与在线蒸馏（SFT / OPD），抑或在仿真/真机环境里靠成败奖励做强化学习（RL）？

    把这两个维度正交展开，当前 VLM 控制机器人的完整版图可归纳为 **5 类保持交互智能体或分层形态的控制方式**，外加 **2 类位于谱系两端的参照路线**（端到端高频 VLA 与环外策略工程）。

## 1. 为什么要按“控制抽象层级”切分？

一台机械臂完成“把桌上的水壶抓起来往杯子里倒水”这件事，从接收到人类的一句自然语言开始，到底层电机真正输出力矩为止，中间要跨过五个物理与计算环节：

```mermaid
flowchart LR
    T["① 任务与阶段分解<br/>先抓壶把 → 移到杯口上方 → 倾倒"] --> G["② 空间定位与几何关系<br/>壶把在哪？壶嘴怎么对准杯口？"]
    G --> P["③ 运动规划与避障<br/>生成无碰撞的 6-DoF 末端轨迹"]
    P --> K["④ 逆运动学与局部伺服<br/>末端目标 → 关节角 / 阻抗控制（20–100 Hz）"]
    K --> M["⑤ 底层电机闭环<br/>关节位置 / 力矩伺服（500–1000 Hz）"]
```

所谓不同的“VLM 控制路线”，本质区别就在于**让 VLM 包揽从左往右的前几格、从哪一个切口把接力棒交给底层的确定性算法或小模型**：

- 如果 VLM 只做 **①**，把“去抓水壶”作为子任务发给一个已经训好的高频 VLA，或者对底层策略提议的动作做放行与覆写，这就是**路线五（快慢双系统）**；
- 如果系统事先把 **②③** 写成了确定性的感知测量与运动原语（如 `vision_ground("kettle handle")`、`grasp_plan()`、`move_pose()`），让 VLM 写 JSON 工具调用或 Python 脚本去组合它们，这就是**路线三（调原语库或写控制代码）**；
- 如果把人工封装的原语全部撤掉，只给 Linux 终端、原生 ROS 2 话题或裸 `env.action(a)` 接口，逼着 VLM 自己写代码实现 **②③④** 的坐标换算与闭环控制循环，这就是**路线四（零抽象直连原生软件栈）**；
- 如果不写代码，只让 VLM 在图像或三维空间里标出关键点、画出 2D 运动路径或写出“壶嘴对准杯口”的几何代价函数（完成 **①②**），把 **③④** 交给 MPC 轨迹优化器或轻量 3D 策略高频求解，这就是**路线二（输出空间关键点与 2D 轨迹）**；
- 如果连外部规划器和优化器都不用，让 VLM 看完相机图直接报出下一步末端位姿或增量 $\Delta\text{EE Pose}$（包揽 **①②③**），底层只留一个逆运动学（IK）加关节伺服去执行 **④⑤**，这就是**路线一（直接输出末端位姿或增量）**；
- 再往谱系两端走一步：往右端压到底，在成百上千小时遥操作数据上微调 VLM，让它以 10–100 Hz 直接吐出连续动作块接管 **①–④**，就变成**端到端高频 VLA（路线 6.1）**；往左端退到底，让 VLM 完全退出实时控制环，只在离线阶段编写奖励函数、环境重置代码与训练脚本去训一个端侧小策略，就是**环外自动化策略工程（路线 6.2）**。

## 2. 用同一个任务看懂六条路线各自输出什么

假设当前相机看到了桌上的摩卡壶和左侧灶台，指令是 `"put the moka pot on the stove"`。下表直观展示每一条路线里，VLM 实际输出的字符串 / 张量到底长什么样：

| 路线 | VLM 单轮直接输出的典型形式 | 底层立刻发生什么 |
| --- | --- | --- |
| **[1. 直出末端位姿 / 增量](direct-pose.md)** | `{"dx": 0.04, "dy": -0.02, "dz": -0.12, "droll": 0, "dpitch": 0, "dyaw": 1.57, "grip": 1}` 或离散词 `<FORWARD_4CM> <ROT_Z_+90>` | 无避障规划，直接经 IK + 操作空间控制器（OSC）沿直线伺服到该位姿，停稳后重拍图像进入下一轮 |
| **[2. 空间关键点 / 2D 轨迹](spatial-keypoints.md)** | 像素路径 `[(143,167), (130,120), (64,160), CLOSE@0, OPEN@2]`，或关键点约束代码 `cost = norm(kp_pot_bottom - kp_stove_center)` | 深度图将像素反投影为 3D 点，或由 MPC 优化器 / 底层 3D 策略（RVT-2）以 10–30 Hz 实时闭环跟踪该轨迹/约束 |
| **[3. 原语库 / 控制代码](primitives-and-code.md)** | `p = mark_point("handle", u=120, v=160); move_to(p.x, p.y, p.z+0.10); move_to(p.x, p.y, p.z); close_gripper()` | 预封装的 `mark_point` 负责带深度校验的反投影，`move_to` 内部跑比例伺服并返回到位误差与夹爪实测开度回执 |
| **[4. 零抽象原生软件栈](native-stack.md)** | 一段直接订阅 `/camera/depth`、手写针孔反投影矩阵乘法、在 `while err > 0.005:` 循环里持续调用 `env.action(kp * err)` 或发布 ROS 2 话题的原生程序 | 机载 Python 运行时或 ROS 2 节点在本地高频执行这段手写闭环，直到循环条件满足或抛出异常才返回给大模型 |
| **[5. 快慢双系统](dual-system.md)** | 子任务路由 `call_vla("grasp the moka pot handle")`、6-DoF 引导位姿，或对底层策略提议动作块的审查结论 `OVERRIDE: lift z by +5cm first` | 冻结的高频 VLA（如 $\pi_{0.5}$）或世界动作模型（如 `Cosmos3`）以 20–50 Hz 处理接触细节，顶层 VLM 低频监控进度与纠偏 |
| **[6.1 端到端高频 VLA](vla-and-out-of-loop.md)** | 词表末尾的离散动作 Token `<act_128><act_094>...`，或流匹配动作专家去噪生成的 $H \times 7$ 连续浮点矩阵（如未来 50 步动作块） | 不经过任何语言/符号中间层，以 10–100 Hz 直接送入底层关节位置 / 阻抗伺服连续执行 |
| **[6.2 环外策略工程](vla-and-out-of-loop.md)** | 离线编写的 `compute_reward(obs, action)`、域随机化配置与训练脚本 `train_ppo.py` | 仿真器或自动重置真机工位跑几万回合训出一个几兆大小的 MLP / 扩散小策略，部署时大模型完全不在环内 |

## 3. 全景二维总表：控制方式 × 训练范式

将纵轴（6 类控制方式）与横轴（Zero-Shot / SFT与蒸馏 / RL）交叉后，2023–2026 年的代表性工作如下表所示（点击角标可查看完整论文出处）：

| 控制方式分类 | VLM 直接输出内容 | 底层接管模块 | 零样本（Zero-Shot）代表 | SFT / 蒸馏 / RL 后训练代表 |
| --- | --- | --- | --- | --- |
| **[1. 直接输出末端位姿 / 增量](direct-pose.md)** | 连续数值 $\Delta\text{EE Pose}$、绝对位姿动作块、或离散增量词 | 仅靠逆运动学（IK）+ 关节/阻抗控制器（无规划器） | Astranomy (Direct)[^astranomy]、JustRUA[^justrua]、ChunkAct[^chunkact]、PIVOT[^pivot]、VIA[^via]、EASG[^easg] | Show-Harness FT[^show-harness]（LoRA SFT）、RT-H[^rth] / ECoT[^ecot] / ThinkWorld[^thinkworld]（推理-动作 SFT+RL）、PEAR[^pear]（纯仿真 RL） |
| **[2. 输出空间关键点与 2D 轨迹](spatial-keypoints.md)** | 像素可供性点、图像平面 2D 粗路径、或三维几何约束方程 | MPC 轨迹优化器、深度反投影、或底层 3D 策略（RVT-2[^rvt2]） | ReKep[^rekep]、VoxPoser[^voxposer]、MOKA[^moka]、CoPa[^copa] | HAMSTER[^hamster]（2D 路径 SFT）、RoboPoint[^robopoint] / FSD[^fsd]（空间点 SFT）、LLARVA[^llarva]（轨迹+动作 SFT）、Embodied-R1[^embodied-r1] / RoboRefer[^roborefer]（空间指认 RL） |
| **[3. 调原语库或写控制代码](primitives-and-code.md)** | 单步工具调用（JSON）或多步原语编排 Python 脚本 | 预封装感知测量工具、抓取采样器与运动规划原语 | ORA[^ora]、PyRUA-Lean[^pyrua]、CaP-X[^capx]、Guava[^guava]、Robo-Harness K1[^k1]、ASPIRE[^aspire]、SHAPER[^shaper]、EvoTER[^evoter] | RoboUniverse-10K[^robouniverse]（多轮轨迹 SFT）、AgenticRoboRL[^agenticroborl]（SFT + RL）、Robo-MOPD[^robomopd]（SFT + 在线逆 KL 蒸馏） |
| **[4. 零抽象直连原生软件栈](native-stack.md)** | 无原语底层 7-DoF 控制循环代码、或原生 ROS 2 节点程序 | 机载 Python 运行时、原生 ROS 2 话题与底层控制器 | OpenRUA[^openrua]、AGP[^agp]、ROSClaw[^rosclaw]、Claude (Code Control)[^claude-robotics]、ROSA[^rosa] | EmbodyAgent[^embodyagent]（黑盒教师合成 → 全参数图文 SFT → 在线 GRPO RL） |
| **[5. 快慢双系统控制底层策略](dual-system.md)** | 子任务路由指令、几何引导目标，或对底层提议动作的放行 / 微调 / 覆写 | 冻结的 VLA（如 $\pi_{0.5}$[^pi05]）、WAM（如 Cosmos3[^astranomy]）或全身控制器（WBC） | Harness VLA[^harness-vla]、Astranomy (Orchestrated)[^astranomy]、Gemini ER 2[^gemini-er2]、InteractVLA[^interactvla]、RHD[^rhd] | Hi Robot[^hirobot]（分层 SFT）、AgenticRoboRL (RPent)[^agenticroborl]（去记忆重构 SFT + 多轮 RL）、ThinkAct[^thinkact]（SFT + 对齐 RL） |
| **[6. 参照：微调为 VLA / 环外工程](vla-and-out-of-loop.md)** | 高频动作 Token、连续流匹配动作块；或离线训练/环境代码 | 关节力矩/位置伺服（10–100 Hz）；或独立端侧小模型 | Eureka[^eureka]、DrEureka[^dreureka]、RoboGen[^robogen]、ENPIRE[^enpire]、RLE-Bench[^rle-bench]（环外写代码训策略） | RT-2[^rt2]、OpenVLA[^openvla] / FAST[^fast]、$\pi_0$[^pi0] / $\pi_{0.5}$[^pi05]、OpenVLA-OFT[^openvla-oft]、MolmoAct2[^molmoact2]、DualVLA[^dualvla]、$\pi^*_{0.6}$[^pi06] / SimpleVLA-RL[^simplevla-rl]（VLA-RL） |

## 4. 全局权衡：每一条路线擅长什么、代价是什么

接口切得越高（如路线 3、5），模型越省力、越抗场景扰动，但能力受底层原语或底层策略限制；接口切得越低（如路线 1、4、6.1），理论动作空间越自由，但对空间测距、推理延迟或遥操作数据量的要求急剧升高：

| 控制方式 | 闭环控制频率 | 训练数据门槛 | 场景与物体扰动泛化 | 富接触灵巧操作上限 | 典型失效机制 |
| --- | --- | --- | --- | --- | --- |
| **1. 直出位姿 / 增量** | 低–中（云端 0.05–0.5 Hz；2B LoRA 可达 25 Hz） | 零样本，或数千条仿真 RL 回合 / 轻量示教 | 高（每步重新看图推理） | 中低（刚性 IK 直线插补易卡死） | 单目尺度估错、无避障碰撞、思考延迟高 |
| **2. 空间关键点 / 2D 轨迹** | 顶层 ~1 Hz + 底层 10–30 Hz | 零样本，或廉价跨域图文轨迹 / 合成空间问答 | 高（顶层语义与底层三维几何解耦） | 中（取决于底层 MPC 或 3D 策略） | 物体边缘深度跳变、遮挡导致关键点跟踪丢失 |
| **3. 原语库 / 控制代码** | 顶层按段调用 + 底层内部伺服 | 零样本，或 ~10⁴ 条仿真多轮交互轨迹 | 高（每轮调用标定工具实测 3D 坐标） | 受限于人工原语集合的表达力 | 原语未覆盖特殊姿态（如侧拉抽屉）、长脚本开环跑空 |
| **4. 零抽象原生软件栈** | 本地生成控制函数可达 10–50 Hz | 零样本强编码模型，或约千条蒸馏 + 在线 RL | 中高（模型自写传感器闭环逻辑） | 中（手写比例/逻辑控制难解软体与复杂摩擦） | API 幻觉与运行时异常、坐标系旋转方向写反 |
| **5. 快慢双系统（VLM+VLA）** | 顶层 0.5–9 Hz + 底层 20–200 Hz | 顶层轻量 SFT/RL + 冻结预训练底层策略 | 高（顶层规划与审查弥补底层记忆盲区） | **高**（继承底层 VLA / WBC 的接触与平衡能力） | 高低层指令语义错位、顶层对任务完成度误判 |
| **6.1 端到端高频 VLA** | **高**（5–100 Hz） | **极高**（数百至数千小时多本体遥操作） | 纯 SFT 易过拟合场景，需靠大规模跨域或 RL | **极高**（端到端拟合高频视觉—接触耦合） | 场景记忆背诵轨迹、连续动作梯度退化通用推理 |
| **6.2 环外自动化策略工程** | 部署时 **极高**（100–1000 Hz 小网络） | 依赖可高并发仿真或可自动重置的真机工位 | 单任务专精（换任务需重新跑工程闭环） | **高**（可针对特定接触力学定制奖励与控制律） | 奖励黑客钻仿真漏洞、真机自动重置机构设计难 |

!!! tip "本框架之外还有哪些重要拼图？"
    除了上表补齐的**空间指认 RL**（路线 2）与**端到端 VLA 强化学习 / 知识隔离**（路线 6.1）外，当前具身智能还有四块与上述框架互补的前沿方向：**① 生成式视频与三维点流世界动作模型（Video-as-Policy / WAM）**、**② 力控与可变阻抗柔顺抽象**、**③ 移动操作 / 足式导航 / 多指灵巧手本体**、**④ 动作前安全护栏与实时失败监测**。它们在 [查漏补缺专题](gaps-and-frontiers.md) 中单独展开。

## 参考文献

[^astranomy]: J. X. Yang, A. Khetan, S. Zhang. *Astranomy: An Empirical Study of GPT-6 Astra as a Native Robot Policy*. NVIDIA Seattle Robotics Lab, CoRL 2026 Late-Breaking Results. <https://research.nvidia.com/labs/srl/projects/astranomy/>
[^justrua]: Z. Wang, Y. Dang, X. Shi et al. *JustRUA: A Controlled Study of GPT-6 Robot-Use Agents*. 2026. [arXiv:2611.16009](https://arxiv.org/abs/2611.16009)
[^chunkact]: B. Xu, W. Bao, X. Liu, J. Zhou, Y. Shang, E. Ferrara. *ChunkAct: Action Chunking for Agentic Robotics*. 2026. [arXiv:2610.18874](https://arxiv.org/abs/2610.18874)
[^show-harness]: Y. Chen, Z. Bai, Z. Cao et al. *Show-Harness: Just a VLM Agent Can Play Robots*. Show Lab (NUS), 2026. [arXiv:2609.10522](https://arxiv.org/abs/2609.10522)
[^rth]: S. Belkhale, T. Ding, T. Xiao et al. *RT-H: Action Hierarchies Using Language*. RSS 2024. [arXiv:2403.01823](https://arxiv.org/abs/2403.01823)
[^ecot]: M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, S. Levine. *Robotic Control via Embodied Chain-of-Thought Reasoning*. CoRL 2024. [arXiv:2407.08693](https://arxiv.org/abs/2407.08693)
[^thinkworld]: C. Kim, C.-P. Huang, J. Kim et al. *ThinkWorld: World Imagination Reinforces Chain-of-Dynamics Reasoning*. NeurIPS 2026. [arXiv:2610.37666](https://arxiv.org/abs/2610.37666)
[^pear]: X. Tang, Y. Zhang, Z. Guo et al. *Training Reasoning Models in Simulation to Natively Use Real Robots* (PEAR / Robot-Use RL). MIT HAN Lab, 2026. [arXiv:2611.18562](https://arxiv.org/abs/2611.18562) · [项目页](https://mit-han-lab.github.io/pear-blog/)
[^pivot]: S. Nasiriany, F. Xia, W. Yu et al. *PIVOT: Iterative Visual Prompting Elicits Actionable Knowledge for VLMs*. ICML 2024. [arXiv:2402.07872](https://arxiv.org/abs/2402.07872)
[^via]: H. Hu, J. Gao, P. Sundaresan, S. Sharma, J. Bohg, D. Sadigh. *VIA: Visual Interface Agent for Robot Control*. 2026. [arXiv:2607.11119](https://arxiv.org/abs/2607.11119)
[^easg]: J. Yi, S. Zhang, Z. Zhou et al. *VLMs are Native Action Models: Unleashing the Manipulation Capabilities of VLMs with Explicit Action-Space Grounding*. 2026. [arXiv:2610.12832](https://arxiv.org/abs/2610.12832)
[^moka]: F. Liu, K. Fang, P. Abbeel, S. Levine. *MOKA: Open-World Robotic Manipulation through Mark-Based Visual Prompting*. RSS 2024. [arXiv:2403.03174](https://arxiv.org/abs/2403.03174)
[^rekep]: W. Huang, C. Wang, Y. Li, R. Zhang, L. Fei-Fei. *ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation*. CoRL 2024. [arXiv:2409.01652](https://arxiv.org/abs/2409.01652)
[^voxposer]: W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, L. Fei-Fei. *VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models*. CoRL 2023. [arXiv:2307.05973](https://arxiv.org/abs/2307.05973)
[^copa]: H. Huang, F. Lin, Y. Hu, S. Wang, Y. Gao. *CoPa: General Robotic Manipulation through Spatial Constraints of Parts with Foundation Models*. IROS 2024. [arXiv:2403.08248](https://arxiv.org/abs/2403.08248)
[^hamster]: Y. Li, Y. Deng, J. Zhang et al. *HAMSTER: Hierarchical Action Models for Open-World Robot Manipulation*. ICLR 2025. [arXiv:2502.05485](https://arxiv.org/abs/2502.05485)
[^rvt2]: A. Goyal, V. Blukis, J. Xu, Y. Guo, Y.-W. Chao, D. Fox. *RVT-2: Learning Precise Manipulation from Few Demonstrations*. RSS 2024. [arXiv:2406.08545](https://arxiv.org/abs/2406.08545)
[^robopoint]: W. Yuan, J. Duan, V. Blukis et al. *RoboPoint: A Vision-Language Model for Spatial Affordance Prediction for Robotics*. CoRL 2024. [arXiv:2406.10721](https://arxiv.org/abs/2406.10721)
[^fsd]: Y. Yuan, H. Cui, Y. Chen et al. *From Seeing to Doing: Bridging Reasoning and Decision for Robotic Manipulation* (FSD). ICLR 2026. [arXiv:2505.08548](https://arxiv.org/abs/2505.08548)
[^llarva]: D. Niu, Y. Sharma, G. Biamby et al. *LLARVA: Vision-Action Instruction Tuning Enhances Robot Learning*. CoRL 2024. [arXiv:2406.11815](https://arxiv.org/abs/2406.11815)
[^embodied-r1]: Y. Yuan, H. Cui, Y. Huang et al. *Embodied-R1: Reinforced Embodied Reasoning for General Robotic Manipulation*. ICLR 2026. [arXiv:2508.13998](https://arxiv.org/abs/2508.13998)
[^roborefer]: E. Zhou, J. An, C. Chi et al. *RoboRefer: Towards Spatial Referring with Reasoning in Vision-Language Models for Robotics*. NeurIPS 2025. [arXiv:2506.04308](https://arxiv.org/abs/2506.04308)
[^ora]: Y. Yang, S. Chen, Z. Wang, J. Gao, H. Zhang. *ORA: Open Robot-Use Agents*. Hao AI Lab (UC San Diego), CoRL 2026 LBR. <https://fastrua.ai/ora/> · [GitHub](https://github.com/fast-rua/ORA)
[^guava]: H. Liu, X. Li, S. Yao et al. *Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness*. 2026. [arXiv:2606.18363](https://arxiv.org/abs/2606.18363)
[^k1]: Z. Li, Y. Zhang, W. Li et al. *Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation*. 2026. [arXiv:2609.29389](https://arxiv.org/abs/2609.29389)
[^capx]: M. Fu et al. *CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation*. ICML 2026. [arXiv:2603.22435](https://arxiv.org/abs/2603.22435)
[^pyrua]: R. Si, J. Bi, S. Yang et al. *Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens* (PyRUA-Lean). 2026. [arXiv:2610.01939](https://arxiv.org/abs/2610.01939)
[^aspire]: R. Lu, Y. Wu, E. Kou et al. *ASPIRE: Agentic /Skills Discovery for Robotics*. NVIDIA GEAR Lab et al., 2026. [arXiv:2607.00272](https://arxiv.org/abs/2607.00272)
[^shaper]: P. Wang, Z. Ma, Y. Chang et al. *Self-Evolving Embodied Agents via Skill-Harness Evolution* (SHAPER). 2026. [arXiv:2608.11350](https://arxiv.org/abs/2608.11350)
[^evoter]: Y. Zhou, Y. Zhou, Y. Wang, H. Li, D. Zhao. *EvoTER: Evolving Embodied Agents via Tool-Use Experience and Reflection*. 2026. [arXiv:2611.27797](https://arxiv.org/abs/2611.27797)
[^robouniverse]: J. Liu, Y. Wang, S. Wang et al. *RoboUniverse-10K: Toward the Scaling Era of Agentic Robotics via Real-to-Sim Environments*. 2026. [arXiv:2611.31002](https://arxiv.org/abs/2611.31002)
[^agenticroborl]: X. Liu, B. Xu, W. Bao, M. Li, W. Bao, C. Chen, Y. Shang. *AgenticRoboRL: Bringing Coding-Agent Post-Training to Agentic Robotics*. 2026. [arXiv:2610.28589](https://arxiv.org/abs/2610.28589)
[^robomopd]: X. Liu, A. Dao, W. Bao et al. *Generalizing Agentic Robotics via Multi-Teacher On-Policy Distillation* (Robo-MOPD). 2026. [arXiv:2611.30997](https://arxiv.org/abs/2611.30997)
[^openrua]: Z. Chu, E. T. Barr, C. Le Goues et al. *OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies*. 2026. [arXiv:2610.02459](https://arxiv.org/abs/2610.02459)
[^agp]: M. Jia, Y. Lin, X. Zhang, Z. Zhang, M. Jiang. *Agent as Policy for Robotic Manipulation* (AGP). 2026. [arXiv:2609.12541](https://arxiv.org/abs/2609.12541)
[^rosclaw]: I. S. Cardenas, M. A. Arnett, N. C. Yeo, L. Shah, J.-H. Kim. *ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction*. 2026. [arXiv:2603.26997](https://arxiv.org/abs/2603.26997)
[^claude-robotics]: S. Berman, M. Ilie, J. Deng, D. Freeman. *How Claude performs on robotics tasks* (Claude plays robotics). Anthropic Research, 2026-07. <https://www.anthropic.com/research/claude-plays-robotics>
[^rosa]: R. Royce, M. Kaufmann, J. Becktor et al. *Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent*. IEEE Aerospace Conference 2025. [arXiv:2410.06472](https://arxiv.org/abs/2410.06472)
[^embodyagent]: W. Dai, J. Liu, J. Chen, H. Liu, W. Ding, S. Huang. *EmbodyAgent: Post-Training Embodied VLM Agents via Distillation, SFT, and RL*. 2026. [arXiv:2611.26196](https://arxiv.org/abs/2611.26196)
[^gemini-er2]: Google DeepMind. *Gemini Robotics ER 2 Model Card*. 2026-07. <https://deepmind.google/models/model-cards/gemini-robotics-er-2/>
[^harness-vla]: Y. Zhang, H. Zhang, F. Gao et al. *Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents* (RPent). 2026. [arXiv:2607.08448](https://arxiv.org/abs/2607.08448) · [GitHub](https://github.com/RLinf/RPent)
[^interactvla]: C. Zhao, Z. Ye, S. Bao et al. *InteractVLA: Turning VLAs into Interactive Tools for Agentic Robotic Manipulation*. 2026. [arXiv:2611.22584](https://arxiv.org/abs/2611.22584)
[^rhd]: S. Kim, J. Lee, M. Kim, B. Kim, N. Kwak. *Recursive Harness Distillation across Agents for Robot Manipulation* (RHD). 2026. [arXiv:2609.33378](https://arxiv.org/abs/2609.33378)
[^hirobot]: L. X. Shi, B. Ichter, M. Equi et al. *Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models*. ICML 2025. [arXiv:2502.19417](https://arxiv.org/abs/2502.19417)
[^thinkact]: C.-P. Huang, Y.-H. Wu, M.-H. Chen, Y.-C. F. Wang, F.-E. Yang. *ThinkAct: Vision-Language-Action Reasoning via Reinforced Visual Latent Planning*. NeurIPS 2025. [arXiv:2507.16815](https://arxiv.org/abs/2507.16815)
[^rt2]: A. Brohan, N. Brown, J. Carbajal et al. *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*. CoRL 2023. [arXiv:2307.15818](https://arxiv.org/abs/2307.15818)
[^openvla]: M. J. Kim, K. Pertsch, S. Karamcheti et al. *OpenVLA: An Open-Source Vision-Language-Action Model*. CoRL 2024. [arXiv:2406.09246](https://arxiv.org/abs/2406.09246)
[^fast]: K. Pertsch, K. Stachowicz, B. Ichter et al. *FAST: Efficient Action Tokenization for Vision-Language-Action Models*. RSS 2025. [arXiv:2501.09747](https://arxiv.org/abs/2501.09747)
[^pi0]: K. Black, N. Brown, D. Driess et al. *$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control*. RSS 2025. [arXiv:2410.24164](https://arxiv.org/abs/2410.24164)
[^pi05]: Physical Intelligence. *$\pi_{0.5}$: a Vision-Language-Action Model with Open-World Generalization*. 2025. [arXiv:2504.16054](https://arxiv.org/abs/2504.16054)
[^openvla-oft]: M. J. Kim, C. Finn, P. Liang. *Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success* (OpenVLA-OFT). RSS 2025. [arXiv:2502.19645](https://arxiv.org/abs/2502.19645)
[^molmoact2]: H. Fang, J. Duan, D. Clay et al. *MolmoAct2: Action Reasoning Models for Real-world Deployment*. Allen Institute for AI (Ai2), 2026. [arXiv:2605.02881](https://arxiv.org/abs/2605.02881)
[^dualvla]: Z. Fang, Z. Liu, J. Liu et al. *DualVLA: Building a Generalizable Embodied Agent via Partial Decoupling of Reasoning and Action*. 2025. [arXiv:2511.22134](https://arxiv.org/abs/2511.22134)
[^pi06]: Physical Intelligence. *$\pi^*_{0.6}$: a VLA That Learns From Experience*. 2025. [arXiv:2511.14759](https://arxiv.org/abs/2511.14759)
[^simplevla-rl]: H. Li, Y. Zuo, J. Yu et al. *SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning*. 2025. [arXiv:2509.09674](https://arxiv.org/abs/2509.09674)
[^eureka]: Y. J. Ma, W. Liang, G. Wang et al. *Eureka: Human-Level Reward Design via Coding Large Language Models*. ICLR 2024. [arXiv:2310.12931](https://arxiv.org/abs/2310.12931)
[^dreureka]: Y. J. Ma, W. Liang, H.-J. Wang et al. *DrEureka: Language Model Guided Sim-To-Real Transfer*. RSS 2024. [arXiv:2406.01967](https://arxiv.org/abs/2406.01967)
[^robogen]: Y. Wang, Z. Xian, F. Chen et al. *RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation*. ICML 2024. [arXiv:2311.01455](https://arxiv.org/abs/2311.01455)
[^enpire]: W. Xiao, J. Xie, T. Zhang et al. *ENPIRE: Agentic Robot Policy Self-Improvement in the Real World*. CoRL 2026. [arXiv:2606.19980](https://arxiv.org/abs/2606.19980)
[^rle-bench]: H. Ma, C. Gao, R. Qiang, B. Dai, N. Li. *RLE-Bench: A Qualifying Exam for Coding Agents as Robot Learning Engineers*. 2026. [arXiv:2609.34210](https://arxiv.org/abs/2609.34210)
