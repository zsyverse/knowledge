"""验证 Agent4Robot《接口与工具箱》中的针孔反投影 pixel_to_xyz：
1) 投影 → 反投影能还原世界坐标；2) 3×3 中位数对噪声的作用；3) 图像多翻转一次时的坐标错位；4) 物体边缘深度跳变。
运行：python scripts/agent4robot/verify_backproject.py   （只需 numpy）"""
import numpy as np

W = H = 256
fovy = np.radians(45.0)                      # robosuite 场景里 agentview 未设 fovy，取 MuJoCo 默认 45°
f = H / 2 / np.tan(fovy / 2)                 # 焦距（像素）
K = np.array([[f, 0, W / 2], [0, f, H / 2], [0, 0, 1]])
print(f"fx = fy = {f:.2f} px, cx = cy = {W/2}")

# 相机放在 (1.0, 0, 1.6)，朝向桌面中心 (0, 0, 0.9)；OpenCV 约定：x 右、y 下、z 前
cam = np.array([1.0, 0.0, 1.6]); target = np.array([0.0, 0.0, 0.9])
z = target - cam; z /= np.linalg.norm(z)
x = np.cross(z, [0, 0, 1.0]); x /= np.linalg.norm(x)
y = np.cross(z, x)
R = np.stack([x, y, z], axis=1)              # 相机系 → 世界系的旋转（列为相机轴）
T = np.eye(4); T[:3, :3] = R; T[:3, 3] = cam # camera_to_world

def project(p):
    pc = R.T @ (p - cam)
    uv = K @ (pc / pc[2])
    return uv[0], uv[1], pc[2]

def backproject(u, v, depth):
    zc = depth
    xc = (u - K[0, 2]) * zc / K[0, 0]
    yc = (v - K[1, 2]) * zc / K[1, 1]
    return (T @ np.array([xc, yc, zc, 1.0]))[:3]

# 1. 往返
p = np.array([0.08, 0.04, 1.005])
u, v, d = project(p)
print(f"\n1) world {p} -> pixel ({u:.2f}, {v:.2f}), depth {d:.4f} m -> back {backproject(u, v, d).round(6)}")

# 2. 取整到像素 + 深度噪声：单像素 vs 3×3 中位数
rng = np.random.default_rng(0)
ui, vi = int(round(u)), int(round(v))
errs_single, errs_med = [], []
for _ in range(2000):
    patch = d + rng.normal(0, 0.01, (3, 3))                   # 1 cm 高斯噪声
    patch[rng.random((3, 3)) < 0.1] = d + 0.3                  # 10% 野值（打到背景）
    errs_single.append(np.linalg.norm(backproject(ui, vi, patch[1, 1]) - p))
    errs_med.append(np.linalg.norm(backproject(ui, vi, np.median(patch)) - p))
print(f"2) mean error: single pixel {np.mean(errs_single)*100:.2f} cm, 3x3 median {np.mean(errs_med)*100:.2f} cm "
      f"(rounding alone {np.linalg.norm(backproject(ui, vi, d) - p)*1000:.1f} mm)")

# 3. 多翻转一次：模型在正向图上挑了 (u, v)，但 API 按上下颠倒的图索引深度和行号
v_wrong = H - 1 - v
print(f"3) flipped row: v {v:.1f} -> {v_wrong:.1f}; back-projected with true depth -> {backproject(u, v_wrong, d).round(3)}, "
      f"error {np.linalg.norm(backproject(u, v_wrong, d) - p)*100:.1f} cm")

# 4. 物体边缘：一半邻域落在壶上（深度 d），一半落在后方桌面（深 0.25 m）
for n_bg in (4, 5):
    patch = np.full((3, 3), d); patch.flat[[2, 5, 8, 1, 4][:n_bg]] = d + 0.25
    zm = np.median(patch)
    print(f"4) edge, {n_bg}/9 pixels on background: median depth {zm:.3f} (true {d:.3f}), "
          f"error {np.linalg.norm(backproject(ui, vi, zm) - p)*100:.1f} cm, max-min {patch.max()-patch.min():.2f} m "
          f"-> depth-discontinuity check rejects")
