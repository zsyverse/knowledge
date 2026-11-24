"""智能控制页面：模糊控制器与迭代学习控制的公共实现（插图和验算共用）。"""
import numpy as np


def tri(x, a, b, c):
    """三角隶属函数，a ≤ b ≤ c；a == b 或 b == c 时为肩形。"""
    x = np.asarray(x, dtype=float)
    left = np.ones_like(x) if a == b else (x - a) / (b - a)
    right = np.ones_like(x) if b == c else (c - x) / (c - b)
    return np.clip(np.minimum(left, right), 0, 1)


# 输入 e、ec 的论域 [-3, 3]，三个模糊集
IN = {"N": (-3, -3, 0), "Z": (-3, 0, 3), "P": (0, 3, 3)}
# 输出 u 的论域 [-3, 3]，五个模糊集
OUT = {"NB": (-3, -3, -1.5), "NS": (-3, -1.5, 0), "Z": (-1.5, 0, 1.5),
       "PS": (0, 1.5, 3), "PB": (1.5, 3, 3)}
CENTER = {"NB": -3, "NS": -1.5, "Z": 0, "PS": 1.5, "PB": 3}
# 规则表 RULES[e][ec]，e = r - y
RULES = {"N": {"N": "NB", "Z": "NS", "P": "Z"},
         "Z": {"N": "NS", "Z": "Z", "P": "PS"},
         "P": {"N": "Z", "Z": "PS", "P": "PB"}}
U = np.linspace(-3, 3, 6001)


def fire(e, ec):
    """返回 {输出集: 激活度}，同一输出集取各规则的最大值（min-max 推理）。"""
    act = {}
    for se, pe in IN.items():
        for sc, pc in IN.items():
            w = min(float(tri(e, *pe)), float(tri(ec, *pc)))
            if w > 0:
                o = RULES[se][sc]
                act[o] = max(act.get(o, 0.0), w)
    return act


def mamdani(e, ec):
    """Mamdani 推理 + 重心法解模糊。"""
    act = fire(e, ec)
    mu = np.zeros_like(U)
    for o, w in act.items():
        mu = np.maximum(mu, np.minimum(w, tri(U, *OUT[o])))
    return float((mu * U).sum() / mu.sum()), mu


def weighted_avg(e, ec):
    """简化解模糊：输出集中心按激活度加权平均。"""
    act = fire(e, ec)
    return sum(CENTER[o] * w for o, w in act.items()) / sum(act.values())


# 迭代学习控制：离散二阶对象 x(t+1) = A x(t) + B u(t), y = C x
A = np.array([[0.0, 1.0], [-0.06, 0.5]])
B = np.array([0.0, 1.0])
C = np.array([-0.5, 1.0])
N_T = 50
T = np.arange(N_T + 1)
REF = np.sin(2 * np.pi * T / N_T)


def run(u):
    x = np.zeros(2)
    y = np.zeros(N_T + 1)
    for t in range(N_T):
        x = A @ x + B * u[t]
        y[t + 1] = C @ x
    return y


def ilc(gamma, iters):
    """P 型 ILC：u_{k+1}(t) = u_k(t) + Γ e_k(t+1)。返回每次迭代的最大误差和各次输出。"""
    u = np.zeros(N_T)
    errs, ys = [], []
    for _ in range(iters):
        y = run(u)
        e = REF - y
        errs.append(np.abs(e[1:]).max())
        ys.append(y)
        u = u + gamma * e[1:]
    return np.array(errs), ys
