"""验证《仿真是怎么做的》一文中的落球数字：第几步接触、接触速度、穿透深度、峰值接触力、步长对比。
运行：python scripts/robot/verify_ball_drop.py   （需要 pip install mujoco）"""
import mujoco
import numpy as np

XML = """
<mujoco>
  <option timestep="{dt}" gravity="0 0 -9.81"/>
  <worldbody>
    <geom name="floor" type="plane" size="2 2 0.1"/>
    <body name="ball" pos="0 0 1">
      <freejoint/>
      <geom name="ball" type="sphere" size="0.05" mass="0.1"/>
    </body>
  </worldbody>
</mujoco>
"""

def run(dt, T=1.5):
    m = mujoco.MjModel.from_xml_string(XML.format(dt=dt))
    d = mujoco.MjData(m)
    print(f"--- timestep = {dt*1000:g} ms ---")
    print("nq =", m.nq, " nv =", m.nv, " qpos0 =", d.qpos)
    first = None
    peak = (0, 0.0)
    for k in range(1, int(T / dt) + 1):
        z_prev = d.qpos[2]
        mujoco.mj_step(m, d)
        if d.ncon and first is None:
            first = k
            f = np.zeros(6); mujoco.mj_contactForce(m, d, 0, f)
            print(f"first contact at step {k} (t={d.time:.3f}s): z_prev={z_prev:.4f} z={d.qpos[2]:.4f}, "
                  f"vz={d.qvel[2]:.3f} m/s, penetration={-d.contact[0].dist*1000:.2f} mm, normal force={f[0]:.2f} N")
        if d.ncon:
            f = np.zeros(6); mujoco.mj_contactForce(m, d, 0, f)
            if f[0] > peak[1]:
                peak = (k, f[0])
    f = np.zeros(6)
    if d.ncon: mujoco.mj_contactForce(m, d, 0, f)
    print(f"peak normal force {peak[1]:.2f} N at step {peak[0]}; final z={d.qpos[2]:.4f}, force={f[0]:.3f} N (mg={0.1*9.81:.3f})")

print("analytic: v=", np.sqrt(2*9.81*0.95), "m/s, t=", np.sqrt(2*0.95/9.81), "s ->", np.sqrt(2*0.95/9.81)/0.002, "steps")
run(0.002)
run(0.05)
