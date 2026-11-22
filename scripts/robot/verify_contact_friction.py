"""验证《仿真是怎么做的》补充部分：MuJoCo 默认选项、solref 对接触的影响、摩擦系数与斜面滑动、成功率置信区间。
运行：python scripts/robot/verify_contact_friction.py   （需要 pip install mujoco）"""
import mujoco
import numpy as np

# 1. 默认选项
m = mujoco.MjModel.from_xml_string("<mujoco><worldbody><geom type='plane' size='1 1 .1'/></worldbody></mujoco>")
print("integrator:", mujoco.mjtIntegrator(m.opt.integrator).name,
      "| solver:", mujoco.mjtSolver(m.opt.solver).name,
      "| cone:", mujoco.mjtCone(m.opt.cone).name,
      "| timestep:", m.opt.timestep)
print("geom default friction:", m.geom_friction[0], "solref:", m.geom_solref[0], "solimp:", m.geom_solimp[0])

# 2. solref 时间常数对落球接触的影响
BALL = """<mujoco><option timestep="0.002"/><worldbody>
<geom type="plane" size="2 2 .1" solref="{tc} 1"/>
<body pos="0 0 1"><freejoint/><geom type="sphere" size="0.05" mass="0.1" solref="{tc} 1"/></body>
</worldbody></mujoco>"""
print("\nsolref timeconst | max penetration (mm) | peak normal force (N) | max rebound height (mm)")
for tc in [0.005, 0.01, 0.02, 0.05]:
    m = mujoco.MjModel.from_xml_string(BALL.format(tc=tc)); d = mujoco.MjData(m)
    pen, fmax, landed, reb = 0, 0, False, 0
    f = np.zeros(6)
    for _ in range(1000):
        mujoco.mj_step(m, d)
        if d.ncon:
            landed = True
            pen = max(pen, -d.contact[0].dist)
            mujoco.mj_contactForce(m, d, 0, f); fmax = max(fmax, f[0])
        elif landed:
            reb = max(reb, d.qpos[2] - 0.05)
    print(f"{tc:>16} | {pen*1000:>20.2f} | {fmax:>21.2f} | {reb*1000:>8.2f}")

# 3. 斜面上的方块：摩擦系数决定滑不滑（30°，tan30 = 0.577）
INC = """<mujoco><option timestep="0.002"/><worldbody>
<body euler="0 30 0"><geom type="box" size="1 1 .05" friction="{mu} 0.005 0.0001"/></body>
<body pos="0 0 0.12" euler="0 30 0"><freejoint/><geom type="box" size=".05 .05 .05" mass="0.2" friction="{mu} 0.005 0.0001"/></body>
</worldbody></mujoco>"""
print("\nmu  | displacement after 1 s (cm)   (tan30 = %.3f)" % np.tan(np.radians(30)))
for mu in [0.3, 0.5, 0.7, 1.0]:
    m = mujoco.MjModel.from_xml_string(INC.format(mu=mu)); d = mujoco.MjData(m)
    for _ in range(100): mujoco.mj_step(m, d)   # 先落稳 0.2 s
    p0 = d.qpos[:3].copy()
    for _ in range(500): mujoco.mj_step(m, d)
    print(f"{mu:<3} | {np.linalg.norm(d.qpos[:3]-p0)*100:.2f}")

# 4. 成功率的二项分布置信区间（Wilson）
def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z*z/n
    c = (p + z*z/(2*n)) / den; h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
    return c - h, c + h
print()
for k, n in [(485, 500), (1937, 2000), (2, 2), (48, 50)]:
    lo, hi = wilson(k, n); print(f"{k}/{n} = {k/n:.1%}  95% CI [{lo:.1%}, {hi:.1%}]")
