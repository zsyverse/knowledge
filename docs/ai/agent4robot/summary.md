---
date: 2026-11-22
description: 把实测过的 5 种接口（ORA、code、code_oracle、primitives、direct）和没实测的 2 种做法（ORA GPU 默认配置、终点 + 传统运控）放在一起：一张对照表、模型输出接在控制链的哪一层、能不能直接给终点交给传统运控、归纳出的规律，以及怎么选、下一步做什么。
tags:
  - 具身智能
  - Agent
  - 机器人
  - 运动规划
---

# 方案总结：试过的 5 种接口和没试的 2 种做法

!!! abstract "要点"
    - **3D 坐标要用工具测，不能让模型估**：没有深度工具的 direct 只有 15/20，长任务 6/10；有 `pixel_to_xyz` 或 `mark_point` 的接口最少 17/20。
    - **一次调用做得越多越省**：工具相同的 code 和 primitives，平均调用 9 / 17 次对 25 / 66 次。
    - **失败集中在抓和放，不在路上**：8 个失败回合里只有 1 个和接近路径有关。
    - 模型的输出可以接在控制链的不同层：任务、技能、路点、控制步。现在的 `move_to` 接在路点这一层；往上一层是“给物体级的终点，交给传统运控”，路线成熟，但难度会转到感知和抓取规划上。

[接口](interfaces.md)、[实测结果](case-study.md)和[检查机制](verification.md)见前几篇，这里把全部方案并排对照。

## 1. 时间线

| 日期 | 做了什么 |
| --- | --- |
| 11-09 | **用 Codex 复现 ORA**：写本地桥接，让 Codex 会话充当 ORA 的策略，ORA 的预检、Supervisor、官方判定和密封照常运行。libero_goal、libero_10 各 10 个任务，20 个全部成功 |
| 11-10 | **不用 ORA，试四种接口**：自己写环境服务和 MCP 工具，direct、primitives、code、code_oracle 各跑 20 个任务。中途发现提示词里客厅场景的桌面高度写错了，libero_10 全部重跑；给卡死的 Codex 请求加了看门狗 |
| 11-17 | **带推理摘要重跑**：把摩卡壶任务（libero_10 t8）用四种接口各跑一遍 |
| 11-18 | **整理**：补上从启动到判定的完整流程和网上的 14 个方案（见[方法谱系](landscape.md)）；查明 code_oracle 从没调用真值位姿，更正之前的结论 |
| 11-19 | **讨论运动接口**：`move_to` 该给多大的目标，能不能直接给终点再交给传统运控（本页第 3、4 节）；渲染了 LIBERO 的 29 种食品（见[术语与素材](glossary.md)） |
| 11-22 | **归纳总结**：即本页 |

## 2. 一张表看全部方案

seed 0，libero_goal 和 libero_10 各 10 个任务，每格只跑一次。调用次数：ORA 按模型调用计，其余按工具调用计。斜线前后分别是 goal 和 long（libero_10）的平均值。

| 方案 | 模型给出什么 | 其余由谁完成 | 20 个任务 | 平均调用 | 平均用时 | 长处 / 短处 |
| --- | --- | --- | --- | --- | --- | --- |
| **ORA**（CPU 版） | 一个动作提议：先标点，再预览，最后提交 | Supervisor 审核通过才执行，执行后给回执；`check_task` 读官方判定 | 20/20 | 34.7 / 52.0 | 272 / 357 s | 动作前有人把关，标点时查深度，全程留证据 / 调用约是 code 的 3–4 倍 |
| **code** | 一段 Python，串起测量和多个动作 | 环境服务逐条执行；`move_to` 内部伺服（容差 4 mm，最多 150 步） | 20/20 | 9.0 / 17.3 | 116 / 218 s | 调用最少、最快 / 程序中途不检查，失败了照样跑完 |
| **code_oracle** | 同 code，另外能读物体真值位姿 | 同 code | 20/20 | 8.0 / 14.6 | 94 / 197 s | 本想测“感知完美”时的上界 / 206 段程序一次都没读真值，对照没有成立 |
| **primitives** | 一次一个原语：测量、移动或开合夹爪 | 同样的伺服；每次返回测量值和新图 | 17/20 | 24.9 / 65.7 | 180 / 427 s | 每一步都看得见，便于调试 / 一步一调用，长任务慢；夹爪只能竖直朝下 |
| **direct** | 原始增量动作 `act`，一次重复 N 步 | OSC 控制器直接执行；没有深度和坐标工具 | 15/20 | 53.5 / 89.6 | 443 / 970 s | 不依赖感知工具，最接近 VLA / 位置全靠看图估，长任务易超时 |
| ORA 默认配置（GPU 版，**没跑**） | 语义动作（移动、转腕、开合）和抓取候选的选择 | SAM3 分割和文字定位、Contact-GraspNet 生成抓取，动作同样经 Supervisor 审核 | — | — | — | 感知和抓取交给专用模型 / 两个模型要常驻 GPU，这台机器跑不了 |
| 终点 + 传统运控（**只讨论过**） | 物体级目标：抓哪个物体、放到哪 | 定位、选抓取、算放置位姿、避障规划、逆运动学、轨迹控制 | — | — | — | 轨迹平滑、能避障，调用大幅减少 / 位姿或抓取估错了，规划器照样执行 |

## 3. 模型的输出接在控制链的哪一层

机器人控制从粗到细大致分五层。几种方案的区别，就在于**模型从哪一层把输出交给工具**：交得越高，模型要管的细节越少，每次调用能做的事越多。

| 层 | 例子 | direct | primitives | code | ORA | 终点 + 传统运控 |
| --- | --- | --- | --- | --- | --- | --- |
| 任务 | 把两个壶放到灶台上 | 模型 | 模型 | 模型 | 模型 | 模型 |
| 技能 / 子目标 | 抓 A 壶，放到灶台 | 模型 | 模型 | 模型 | 模型 | **模型：`pick_place(…)`** |
| 路点 | 壶把正上方 10 cm | 模型在心里估 | **模型：每次 1 个** | **模型：一段程序写多个** | **模型：预览后提交 1 个** | 规划器生成 |
| 控制步 | 每 50 ms 一个小增量 | **模型：`act` × N** | 伺服（最多 150 步） | 伺服（最多 150 步） | Runtime 执行 | 轨迹控制器 |
| 关节力矩 | 由末端目标换算 | OSC 控制器 | OSC 控制器 | OSC 控制器 | OSC 控制器 | OSC 控制器 |

加粗的格子是模型交出输出的那一层。交出时有没有检查：direct、primitives、code 直接执行；ORA 先经 Supervisor 审核；终点 + 传统运控可以在执行前做逆运动学和碰撞预检。ORA 的 GPU 默认配置多了语义动作和抓取规划，介于路点和技能之间，没有列进表里。成败都由 LIBERO 的官方判定决定，和接口无关。

`move_to` 给的既不是整个任务的终点，也不是每一步的小增量，而是中间的**路点**，也就是一段运动的终点。摩卡壶任务里 primitives 一共调用了 16 次 `move_to`，每次离当前位置 8.4–47.4 cm。环境服务把一次 `move_to` 拆成每 50 ms 一步的小移动，离目标 4 mm 以内就停，最多 150 步：

| 步 | 目标 | 距离 | 控制步 | 结果 |
| --- | --- | --- | --- | --- |
| 第 5 步 | 第一个壶正上方 | 27.1 cm | 25 | 到达，误差 0.6 mm |
| 第 7 步 | 竖直下降到壶顶 | 14.8 cm | 142 | 到达，误差 3.9 mm |
| 第 14 步 | 转 90° 后下降 | 10.5 cm | 150（用完） | 没到：停在 z = 1.041，差 2.75 cm（被壶盖挡住） |
| 第 24 步 | 从灶台上方移到第二个壶上方 | 47.4 cm | 39 | 到达，误差 1.9 mm |

**为什么 `move_to` 不直接给任务终点？**

- **只走直线，不避障。**`move_to` 和 ORA 的 `move_pose` 都没有运动规划，也不查碰撞，所以要先到物体正上方，再竖直下降。第 14 步就是下降时被壶盖挡住了。
- **中间有离散动作。**夹住、抬起、搬走、松开，夹爪开合用一个终点坐标表达不了。
- **每走完一段都能检查。**看 `reached`、误差和开度，失败了可以马上改。

其他系统也是这样分层：工业机械臂的 MoveL / MoveJ 指令、ROS 的 MoveIt[^moveit]，参数都是“这一段去哪”；`pick(物体)`、`place(物体, 区域)` 这类技能接口才接近任务级；VLA 和本页的 direct 输出的才是每个控制步的小增量。

## 4. 直接给终点，再交给传统运控？

**可以，这条路线很成熟，但有两个前提**：模型给的“终点”应该是物体的目标状态（把哪个物体放到哪），而不是机械臂的一个坐标；中间缺的几块，比如抓哪里、怎么绕开障碍、先做什么，要由传统模块补上。

| 环节 | 传统做法 | 本项目里对应什么 |
| --- | --- | --- |
| 定位物体 | 深度点云加分割，或 6D 位姿估计（如 FoundationPose[^foundationpose]） | `pixel_to_xyz`、`mark_point`；ORA GPU 版有 SAM3 分割 |
| 选抓取 | Contact-GraspNet[^cgn]、AnyGrasp[^anygrasp] 从点云生成抓取位姿 | ORA GPU 版的 `grasp_plan` |
| 算放置 | 目标位置加上物体在手里的相对位姿，换算成手要去的位姿 | **没有**，靠模型自己估 |
| 避障路径 | 用点云建碰撞模型，再交给 MoveIt / OMPL[^ompl]（采样式规划）或 TrajOpt[^trajopt]（轨迹优化） | **没有**：`move_to` 和 `move_pose` 都只走直线 |
| 关节角和执行 | 逆运动学求关节角，再由轨迹控制器或 OSC 执行 | OSC 控制器（已有） |
| 多步顺序 | 任务与运动联合规划（TAMP[^tamp]，如 PDDLStream[^pddlstream]），或由模型给出子目标序列 | 模型自己安排 |

- **好处**：动作平滑、能避障，调用次数和用时会大幅下降；执行前就能检查逆运动学有没有解、会不会碰撞。
- **代价**：难度从模型转到了感知和规划。位姿估错、抓取选错，规划器照样一路执行下去。拉抽屉、拧旋钮这类受约束的接触动作，纯规划很吃力。
- **瓶颈不在“走过去”**：8 个失败回合里只有 1 个和接近路径有关（见下一节）。code 用一段程序跑完“下降 → 夹 → 抬起 → 搬过去 → 放下”，已经接近只给目标，平均 9 / 17 次调用。换成规划器主要省调用和时间，成功率还得靠抓取、放置选得对。
- **比较稳的做法是混合**：① 模型给语义目标，比如“抓 A 壶的把手，放到灶台中心，再抓 B 壶”；② 传统模块算出抓取位姿和无碰撞轨迹并执行；③ 每个阶段结束后读回执和新图，失败了让模型换个目标再来。[方法谱系](landscape.md) 里的 VoxPoser、ReKep（L4，模型写约束、优化器求轨迹）走的也是这个方向。

## 5. 归纳出的规律

1. **3D 坐标要用工具测，不能让模型估。**direct 没有深度和坐标工具，20 个任务成功 15 个，长任务只有 6/10。有 `pixel_to_xyz` 或 `mark_point` 的四种接口，最少也有 17/20。
2. **一次调用做得越多，越省。**工具完全相同的 code 和 primitives，平均调用分别是 9.0 / 17.3 次和 24.9 / 65.7 次。direct 每次只能发一串增量动作，要 53.5 / 89.6 次。这和 CaP-X、URAI 报告的“工具抽象越高越好”一致（见[方法谱系](landscape.md#4-文献里反复出现的结论)）。
3. **把关和证据有代价，好处要到真机才看得到。**ORA 和 code 都是 20/20，但 ORA 平均要 34.7 / 52.0 次模型调用、272 / 357 秒，code 只要 9.0 / 17.3 次、116 / 218 秒。Supervisor 防的是撞到东西、用过期观测这类危险动作，仿真里撞了也没有损失，所以只看得到成本。
4. **失败集中在抓和放，不在路上。**8 个失败回合里，只有 1 个和接近路径有关：primitives 在 goal t0 竖直朝下的夹爪被上层抽屉挡住，够不到把手。其余是抓不稳、放不稳、位置估不准和预算用完（明细见[实测 §5](case-study.md#5-失败案例都在说明什么)）。想提高成功率，要在抓取和放置的选择、每个阶段之后的检查上下功夫。
5. **模型几乎不写感知算法。**code 和 code_oracle 写的 449 段程序平均只有 5.2 行，77 段只测量不动作，`pixel_to_xyz` 出现在 172 段里；分割、聚类一类的算法一段都没有，`scipy` 出现的 12 段都只用来换算旋转。Codex 的做法是看图挑像素、让工具算坐标，再把动作批量写进程序。
6. **这些结论的适用范围。**每格只跑一次（seed 0），9/10 和 10/10 的差别不显著，只有 direct 长任务的 6/10 是明确的差距。code_oracle 的真值对照没有成立。环境服务和工具是我们自己写的（`move_to` 只走直线、每回合最多 30 分钟），这些取舍本身也会影响结果。

## 6. 怎么选，下一步做什么

**按需求选：**

| 需求 | 选 |
| --- | --- |
| 要省调用、省时间 | code |
| 要动作前把关、留下能复核的证据，比如上真机 | ORA |
| 要看清每一步、方便调试 | primitives |
| 要和 VLA 对照，不给任何感知工具 | direct |
| 以抓放为主，要轨迹平滑、能避障 | 终点 + 传统运控（还没实现） |

**下一步（都还没开始）：**

1. **实现 `pick_place(物体像素, 目标像素)`**：用深度点云定位物体，按固定模板生成路点（预抓取 → 下降 → 夹 → 抬到安全高度 → 平移 → 下降 → 松开 → 退回），执行前查逆运动学有没有解，在同样 20 个任务上和 code、primitives 比。这台机器没有 GPU，抓取位置先用简单规则选。
2. **跑 ORA 默认配置**：换有 GPU 的机器，带上 SAM3 和 Contact-GraspNet，看专用的感知和抓取模型能省多少调用。
3. **多跑几个 seed**：现在每格只跑了一次，9/10 和 10/10 分不出高下。
4. **重做真值对照**：比如只给 `object_poses`，不给深度和 `pixel_to_xyz`，模型才会真的用真值，这样才测得出感知的上界。
5. **补上没试过的两类**：[方法谱系](landscape.md)里的 L1（把 VLA 当工具）和 L4（模型写约束，交给优化器求轨迹）。

## 参考

本页的实测数据来自作者在 LIBERO 上的运行日志（与[实测](case-study.md)同一批 100 个回合），实测框架见 ORA[^ora]。

[^ora]: Y. Yang, S. Chen, Z. Wang, J. Gao, H. Zhang. *ORA: Open Robot-Use Agents*. Hao AI Lab（UC San Diego）, 2026. 项目页 <https://fastrua.ai/ora/> · 代码 <https://github.com/fast-rua/ORA>
[^moveit]: MoveIt 运动规划框架（ROS）. <https://moveit.ai/>
[^foundationpose]: B. Wen, W. Yang, J. Kautz, S. Birchfield. *FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects*. CVPR 2024. arXiv:2312.08344
[^cgn]: M. Sundermeyer, A. Mousavian, R. Triebel, D. Fox. *Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes*. ICRA 2021. arXiv:2103.14127
[^anygrasp]: H.-S. Fang et al. *AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains*. IEEE T-RO 2023. arXiv:2212.08333
[^ompl]: I. A. Șucan, M. Moll, L. E. Kavraki. *The Open Motion Planning Library*. IEEE Robotics & Automation Magazine, 2012. <https://ompl.kavrakilab.org/>
[^trajopt]: J. Schulman et al. *Motion Planning with Sequential Convex Optimization and Convex Collision Checking*（TrajOpt）. IJRR 2014.
[^tamp]: C. R. Garrett et al. *Integrated Task and Motion Planning*. Annual Review of Control, Robotics, and Autonomous Systems, 2021. arXiv:2010.01083
[^pddlstream]: C. R. Garrett, T. Lozano-Pérez, L. P. Kaelbling. *PDDLStream: Integrating Symbolic Planners and Blackbox Samplers via Optimistic Adaptive Planning*. ICAPS 2020. arXiv:1802.08705
