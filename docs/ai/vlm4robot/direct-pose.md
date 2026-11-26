---
date: 2026-11-26
description: 详解第一类控制方式：VLM 不借外部规划器与技能库，看图后直接输出末端位姿或增量 ΔEE Pose，底层仅靠 IK 与伺服执行。拆解零样本连续动作块、离散增量词 LoRA SFT、具身思维链联合 SFT、纯仿真 RL 与视觉坐标锚定五种机制。
tags:
  - 具身智能
  - VLM
  - 强化学习
  - 机器人控制
---

# 路线一：直接输出末端位姿或增量（Direct EE Pose / $\Delta\text{EE Pose}$）

!!! abstract "要点"
    在保持交互智能体形态的五类方式里，这一类把接口切得最低：**不挂目标检测器、不挂抓取采样器、不挂避障运动规划器**。每一轮模型直接读取相机画面与当前机械臂状态，输出末端执行器（End-Effector, EE）的目标位姿或位姿增量 $\Delta\text{EE Pose}$，底层只靠逆运动学（IK）或操作空间控制器（OSC）把机械臂拉过去，拍一张新图再进下一轮。

    早期通用 VLM 走这条路几乎寸步难行，核心障碍有三个：**单目图像缺乏米制深度尺度**、**模型不擅长心算相机到机械臂基座的三维坐标旋转**、**每步思考几秒导致控制延迟过高**。围绕怎样在不引入重型外部工具的前提下跨过这三个障碍，演化出了下面五条具体子路线。

## 0. 底层控制回路在做什么

理解这一类方法，先要看清模型吐出一组数之后，底层硬件到底发生了什么：

```mermaid
flowchart LR
    O["多视角 RGB 图 + 本体状态<br/>当前 x,y,z,q 与夹爪开度"] --> V["VLM 推理<br/>（语言头直接生成文本/Token）"]
    V -->|"绝对位姿 p* 或增量 Δp"| IK["逆运动学 IK / 操作空间控制 OSC<br/>无碰撞检测、无绕障规划"]
    IK -->|"关节角 q* 或关节力矩 τ（20–500 Hz）"| R["机械臂直线插补运动<br/>到达或超时停稳"]
    R --> O
```

给定当前末端位姿 $\mathbf{x}_t = (\mathbf{p}_t, \mathbf{R}_t) \in \mathrm{SE}(3)$，若模型输出笛卡尔增量 $\Delta \mathbf{x}_t = (\Delta \mathbf{p}_t, \Delta \mathbf{r}_t)$ 与夹爪指令 $g_t \in \{-1, +1\}$，底层目标位姿就是：

$$
\mathbf{p}_{t}^{\text{des}} = \mathbf{p}_t + \Delta \mathbf{p}_t, \qquad
\mathbf{R}_{t}^{\text{des}} = \exp([\Delta \mathbf{r}_t]_\times)\,\mathbf{R}_t
$$

随后要么由逆运动学求解目标关节角 $\mathbf{q}^{\text{des}} = \mathrm{IK}(\mathbf{p}_t^{\text{des}}, \mathbf{R}_t^{\text{des}})$ 交给关节 PD 控制器跟踪，要么由操作空间阻抗控制（如 robosuite 默认的 `OSC_POSE`）按位姿误差 $\mathbf{e}_t$ 直接算关节力矩 $\boldsymbol{\tau} = J\tp \big(K_p \mathbf{e}_t - K_d \dot{\mathbf{x}}_t\big) + \mathbf{g}(\mathbf{q})$。

这里没有采样规划器（如 RRT*）替它绕开障碍物，也没有抓取器替它修正夹爪偏角——**如果 VLM 报的 $z$ 低了 3 cm，夹爪就会直接撞上桌面；如果中间隔着壶盖，夹爪就会被直接卡住**。下面五种解法都在回答：怎么让 VLM 报准这组数。

---

## 1. 前沿大模型零样本直出连续位姿 / 动作块（Zero-Shot）

### 到底在做什么

不微调任何模型权重，直接在系统提示词（System Prompt）里写清楚机械臂的基坐标系方向（例如“$+x$ 朝前、$+y$ 朝左、$+z$ 竖直向上，桌面高度约 $z=0.92\,\mathrm{m}$”）、各路相机的安装视角和当前末端读数，让闭源前沿多模态推理模型（如 GPT-6 Astra、GPT-6.1 Sol）看图推理后，以结构化文本直接输出下一步的连续三维坐标或一小段动作序列。

因为每调一次云端推理模型都要耗费数秒到十余秒，单步只走 1 cm 会慢到无法完成任务。因此零样本路线重点打磨两件事：**用什么动作空间表示最准**，以及**一次推理执行多大粒度的动作块最稳**。

### 代表工作怎么做的

- **Astranomy（Direct Policy，NVIDIA SRL）**[^astranomy]：专门测试无历史会话记忆下，GPT-6 Astra 直接把当前多视角图像与本体读数映射为 **1–10 步可变长动作块**的能力。作者在 120 个任务的仿真基准 RoboLab-120 上严格对比了三种输出空间：
  - 输出**笛卡尔绝对末端位姿序列** $(x, y, z, q_x, q_y, q_z, q_w, g)_{1:k}$：成功率 **66.3%**；
  - 输出**关节角序列** $(q_1, \dots, q_7, g)_{1:k}$：成功率掉到 **50.2%**；
  - 输出**关节空间三次 B-样条控制点**：成功率进一步掉到 **38.8%**。
  原因很直观：图像像素与三维笛卡尔空间满足透视几何投影，VLM 看图能直接判断“杯子在夹爪往左 5 cm、往下 8 cm 处”；但关节角与三维位置之间隔着高度非线性的正运动学雅可比矩阵，让语言模型心算 7 个旋转关节联动走直线，误差极大。
- **JustRUA**[^justrua]：在 42 个双臂操作任务的 RoboDojo 基准上对 GPT-6 Astra 外围脚手架做受控消融（总分从基线 29.7 提升至 50.3）。实验表明，不改模型权重时，最关键的不是花哨的自我反思提示词，而是四项朴素设计：**保留完整回合历史**（让模型看见上一轮移动后手爪在画面中移动了多少像素，相当于在线自标定比例尺）、**单次运动最多 20 步有界截断**（防止单步估错一路撞穿）、紧凑本体读数，以及用单目深度估计（Depth Pro）辅助三维坐标换算。
- **ChunkAct**[^chunkact]：解决智能体一步一推理过慢的问题。它在离线阶段把过往成功轨迹里的连续基本动作连同触发前置条件（precondition）和失败检测规则编译成可复用的“智能体动作块”（chunk）；在线测试时，大模型单次调用即可启动整块动作自主运行，只有动作块跑完或中途触发异常时才把控制权交回大模型，在 LIBERO-Pro 上减少 **2.9 倍模型调用**与 **4.4 倍输入 Token**，同时提升 5.0 个百分点成功率。

---

## 2. 离散语义增量接口 + 轻量模型 LoRA SFT

### 到底在做什么

让小尺寸开源 VLM（如 2B 参数量）直接回归小数点后四位的连续浮点数 `"dz": -0.0375`，既浪费解码 Token，又容易学偏；而且不同机械臂（Franka 与 AgileX）基坐标系定义和工作空间尺寸不同，换一台机器数据就作废。

**Show-Harness**[^show-harness] 的做法是在模型与底层控制器之间插一层**极简离散语义增量词表**：

1. **模型侧只输出单个语义动作词**：把六自由度微小移动和夹爪动作定义成十几个固定词，例如 `<MOVE_FORWARD>`、`<MOVE_DOWN>`、`<ROT_YAW_POS>`、`<GRASP>`、`<RELEASE>`、`<DONE>`。模型每看一帧图，不写长篇思维链，**只解码 1 个动作 Token**。
2. **底层用确定性“本体解释器”（Embodiment Interpreter）翻译**：解释器只是几行确定性配置代码，负责把 `<MOVE_FORWARD>` 翻译成当前机械臂末端坐标系或基坐标系下的固定物理步长（如 $\Delta x = +2\,\mathrm{cm}$ 或旋转 $15^\circ$），再喂给该机械臂自己的 IK 控制器。
3. **用浏览器键盘界面 GUMI 低成本采数据 + LoRA SFT**：因为动作空间已经被离散化成十几个按键，人类根本不需要昂贵的 VR 头显或主从同构遥操作臂，直接在配套网页工具 **GUMI（GUI Manipulation Interface）** 里看着相机画面按键盘就能采集专家轨迹，随后对 **Qwen3.5-2B** 做轻量 LoRA 微调。

### 为什么有效（两个反直觉实验结论）

- **在动态任务上，2B 小模型反超 9B 大模型（80% vs. 60%）**：因为每次只生成 1 个 Token，微调后的 Qwen3.5-2B 单步决策延迟只有 **39 ms**（约 25 Hz），而 Qwen3.5-9B 需要 **79 ms**。在“抓取正在桌面上滚动的网球”这类动态任务里，79 ms 时球已经滚走了，反应更快的 2B 模型反而显著胜出。
- **纯仿真 SFT 权重零样本上真机（13/20 vs. 端到端 VLA 0/20）**：端到端 VLA 直接拟合特定相机外参与连续控制量，仿真与真机稍有偏差就会全军覆没（0/20）；而 Show-Harness 的 2B 模型只负责看图决定“现在该往前一点还是往下一点”，底层步长缩放与 IK 差异被新机械臂的本体解释器吸收，因此在 ManiSkill / Isaac Lab 纯仿真训练的权重换个解释器就能在真实 Franka 与 Piper 机械臂上跑出 13/20 成功率。

---

## 3. 中间推理 / 语言动作与 $\Delta\text{EE Pose}$ 联合 SFT

### 到底在做什么

如果直接拿遥操作数据做成 `(图像, 任务指令) -> ΔEE Pose` 训练 VLM，模型往往走捷径：不去理解指令语义，而是背诵“看到桌面左上角有个红点就往右走”，一旦换个新物体或改一句指令就彻底失效。

这条路线的核心机制是**在每一步训练样本的动作前面，人工或自动合成一段显式的中间表征序列**，让自回归交叉熵损失同时监督“中间想了什么”和“最后出什么动作”：

```text
输入: [相机图像] + "把可乐罐挪到盘子右边"
模型自回归输出:
  [Task Plan] 1. 接近可乐罐  2. 闭合夹爪  3. 抬起并移至盘子右侧  4. 松开
  [BBox] coke_can: [112, 140, 148, 210], plate: [180, 150, 240, 195]
  [Gripper Pixel] current: (95, 80) -> subgoal: (130, 165)
  [Language Motion] 向右前方伸展并下压手爪
  [Action] Δx=+0.03, Δy=-0.04, Δz=-0.05, Δr=0, Δp=0, Δyaw=0, grip=-1
```

### 三种代表性的中间桥梁设计

1. **细粒度“语言动作”层级（RT-H）**[^rth]：把“拿碗”与底层的 `(+0.02, 0, -0.05)` 之间拆出一层只有几十种短语的**语言动作**（如 `"move arm forward and down"`、`"rotate wrist counterclockwise"`）。模型先根据图像和总任务预测当前步的语言动作，再以该语言动作为条件预测连续数值 $\Delta\text{EE Pose}$。这样做有两个直接收益：一是不同任务（拿杯子、关抽屉、擦桌子）在“手爪前伸”这一层完全共享底层动作数据；二是**允许人类在真机出错的瞬间直接开口说“再往左一点”**，强行覆盖模型预测的中间语言动作，底层仍能丝滑转成数值增量。
2. **多粒度具身思维链（ECoT）**[^ecot]：利用现成的视觉检测器与大模型，在已有机器人数据集（如 Bridge v2）上离线自动补全每一步的子任务、物体边界框、手爪像素位置和下一步移动方向，与离散动作 Token 拼成一条长序列微调 OpenVLA 基座。在不增加任何一条新真机遥操作数据的前提下，分布外（OOD）任务成功率直接提升 **28 个百分点**（推理时可通过缓存高层子任务避免每帧重复生成整条长链）。
3. **跨本体“动力学链”运动 Token（ThinkWorld）**[^thinkworld]：人类操作视频满世界都是，但人手没有 7-DoF 机械臂关节角。ThinkWorld 先用三维手部姿态估计从人类视频里提取指尖/手掌轨迹，与机械臂末端轨迹一起投射到统一的**归一化 $\Delta\text{EE Pose}$ 空间**，再用类似 FAST 的频域分词器把连续运动片段编码成跨本体的离散动作词，称为 **Chain-of-Dynamics（CoD）**。模型先在有标注的机械臂数据上做 SFT 学会“先生成 CoD 动力学链、再出具体动作”，随后在海量无动作标注的人手与机器人视频上做 **GRPO 强化学习**——奖励函数检查模型生成的 CoD 经世界模型想象出的未来视觉状态，与真实视频下一帧是否一致。

---

## 4. 无 SFT 的纯仿真强化学习直出连续 $\Delta\text{EE Pose}$（Pure Sim RL）

### 到底在做什么

前面第 2、3 种路线仍然要先采集示范轨迹做 SFT，而离线 SFT 很难遍历所有抓空、碰歪后的恢复状态。MIT HAN Lab 提出的 **PEAR（Robot-Use RL）**[^pear] 验证了一个更激进的设想：**完全不要任何人类遥操作示教、完全不做 SFT**，直接把开源强推理模型（Qwen3.8-27B）放进并行物理仿真器（LIBERO、RoboDojo）里，只凭回合结束时仿真器给出的 `0 / 1` 成败信号做多轮强化学习（完整细节见本站 [PEAR 论文笔记](../robot/pear.md)）。

### 训练与运行闭环是怎么转起来的

1. **多轮上下文不截断**：与 computer-use agent 操作电脑桌面完全同构。第 $k$ 轮输入包含任务描述、三路相机画面（头部 + 双腕部）、机械臂当前状态文本，以及前面 $1 \dots k-1$ 轮所有的历史画面、思考链和已执行动作。
2. **先自由思考，再吐出一个 JSON 位姿增量**：
   ```json
   {"left_arm":  {"x": 0.0, "y": 1.0, "z": -17.4, "roll": 0.0, "pitch": 0.0, "yaw": 0.0},
    "right_arm": {"x": 0.0, "y": 0.0, "z": 0.0,   "roll": 0.0, "pitch": 0.0, "yaw": 0.0},
    "left_gripper": {"width": -6.5}, "right_gripper": {"width": 0.0}}
   ```
   底层 IK + 控制器执行完这一个目标点后停稳，拍新画面追加到上下文末尾，进入第 $k+1$ 轮（平均一个回合约 20 轮、共约 94k Token）。
3. **异步多轮 GRPO + 动态组过滤**：对同一初始场景并行跑 8 条完整多轮 rollout，用 DAPO 策略过滤掉 8 条全成功或全失败（组内优势全为 0）的无效组，对其余组计算归一化组内优势 $A_i = (r_i - \bar{r}) / \sigma_r$，并且**只在模型自己生成的思维链与 JSON 动作 Token 上计算策略梯度**（环境插入的图像与状态 Token 全部 mask 掉）。

### 解决了什么核心痛点

- **从几乎不会到学会在线目测纠偏**：未经训练的 Qwen3.8-27B 在 LIBERO 上只有 **1.6%** 成功率，经过纯仿真 RL 后跃升至 **74.4%**；且当测试中途把目标指令临时改掉或挪动物体时，传统端到端 VLA（如 $\pi_{0.5}$）因背诵固定轨迹跌至 **0.75%**，而 PEAR 仍保持 **57.4%**。
- **零真机数据迁移与零通用能力退化**：因为没有用窄域 SFT 强行扭曲预训练分布，模型在 9 个数学、代码与通用视觉问答基准上没有任何退化；仅靠修改系统提示词里的双臂坐标系说明，纯仿真训出的权重直接部署到真实双臂 YAM 机器人上即取得 **18/30（60%）** 成功率。代价则是每步前平均生成约 3.2k 思考 Token，单步耗时数秒，难以处理高速动态任务。

---

## 5. 视觉提示采样与显式坐标系锚定（Visual Prompting）

### 到底在做什么

如果既不能微调模型（只能调现成 API），模型本身直接心算三维坐标又总是偏几厘米，那就**在喂给 VLM 的输入图像上先画好几何参考尺或候选动作**，把困难的“三维连续回归题”改写成 VLM 最擅长的“看图选择题”或“局部坐标读数题”。

```mermaid
flowchart LR
    C["原始相机画面 + 标定内参/外参"] --> P["在三维空间采样位移 / 构造坐标轴<br/>用相机投影矩阵画到原图上"]
    P --> V["VLM 看叠加后的新图<br/>选箭头编号 / 拖拽虚拟夹爪 / 读局部轴刻度"]
    V --> E["换算回精确 3D 位姿增量<br/>IK 控制器执行"]
```

### 三种具体画法

1. **画带编号的候选位移箭头（PIVOT）**[^pivot]：系统先在当前夹爪三维位置附近按高斯分布随机采样一批三维位移向量 $\Delta \mathbf{p}_1, \dots, \Delta \mathbf{p}_K$，用已知的相机内外参把每个三维终点投影到二维画面上，画成带圆圈编号的彩色箭头。VLM 不需要报任何坐标，只需回答“3 号和 7 号箭头最朝向杯把”；系统立刻在 3 号和 7 号附近缩小方差重新采样画第二轮箭头，迭代 2–3 轮后收敛并执行。
2. **搭带世界轴与虚拟夹爪手柄的三维浏览器界面（VIA）**[^via]：Stanford 提出的 VIA（Visual Interface Agent）利用 RGB-D 相机重建工作空间，在浏览器界面里渲染出**红绿蓝世界坐标轴箭头**和一个**带局部三轴拖拽/旋转手柄（gizmo）的半透明虚拟目标夹爪**。Claude Code、Codex 等通用 computer-use 智能体通过 MCP 工具点击像素探查三维坐标、微调虚拟夹爪姿态，从多视角截图确认虚拟夹爪正好卡住物体后，再一键触发底层控制器走过去。
3. **把夹爪局部坐标系直接画进腕部相机图（EASG）**[^easg]：每次拍完腕部相机照片后，按相机标定直接把以夹爪指尖（TCP）为原点的 $X/Y/Z$ 三维刻度轴叠加画在画面中心，同时在解码端施加形式语法约束（grammar-constrained decoding）保证动作格式合法。27B 通用 VLM 在零样本下只需顺着图上画出的红绿蓝轴线目测距离，就能报出与微调 VLA 相当的连续动作；消融实验显示，一旦去掉画在图上的坐标系或度量深度，成功率立刻跌至 0%。

---

## 小结：五种解法该怎么对比

| 子路线 | 改不改权重 | 靠什么解决空间精度 | 单步延迟 | 最适用场景 |
| --- | --- | --- | --- | --- |
| **1. 前沿模型零样本动作块** | 不改 | 强基座空间推理 + 历史画面自标定 + 笛卡尔位姿块 | 慢（5–20 s） | 快速验证、无训练预算的准静态桌面操作 |
| **2. 离散语义词 + 轻量 LoRA** | 轻量 LoRA SFT | 人类键盘示教 + 单步固定微小增量高频闭环修正 | **极快（~39 ms）** | 动态追踪（如抓滚球）、低算力端侧跨本体迁移 |
| **3. 中间推理链联合 SFT** | 全量 / LoRA SFT | 框、像素点、语言动作或动力学链 Token 充当桥梁 | 中（0.2–1 s） | 有现成示范轨迹、需抗物体/指令分布外变化或人机口头纠偏 |
| **4. 纯仿真无 SFT 强化学习** | 多轮 GRPO RL | 仿真成败试错倒逼模型学会看多视角图目测对准与纠错 | 慢（数秒/步） | 无遥操作数据、追求强指令泛化且不能牺牲通用推理能力 |
| **5. 视觉提示与坐标锚定** | 不改 | 把已知相机标定画进图里（候选箭头 / 虚拟夹爪 / TCP 坐标轴） | 中–慢（多轮看图） | 有准确相机标定、希望直接用现成 VLM 零样本精确对准 |

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
