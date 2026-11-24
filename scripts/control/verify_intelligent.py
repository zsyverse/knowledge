"""智能控制页面中所有数值例子的验算。

    .venv/bin/python scripts/control/verify_intelligent.py
"""
from fractions import Fraction as F

from intelligent_common import *

# 1. 模糊化：e = 1, ec = -0.5
e, ec = 1.0, -0.5
mu = {k: float(tri(e, *v)) for k, v in IN.items()}
mc = {k: float(tri(ec, *v)) for k, v in IN.items()}
print("μ(e=1):", mu, " μ(ec=-0.5):", mc)
assert abs(mu["Z"] - 2/3) < 1e-12 and abs(mu["P"] - 1/3) < 1e-12 and mu["N"] == 0
assert abs(mc["N"] - 1/6) < 1e-12 and abs(mc["Z"] - 5/6) < 1e-12

# 2. 规则激活
act = fire(e, ec)
print("激活度:", {k: round(v, 4) for k, v in act.items()})
assert set(act) == {"NS", "Z", "PS"}
assert abs(act["NS"] - 1/6) < 1e-12 and abs(act["Z"] - 2/3) < 1e-12 and abs(act["PS"] - 1/3) < 1e-12

# 3. 解模糊
wa = weighted_avg(e, ec)
exact = (F(-3, 2) * F(1, 6) + 0 * F(2, 3) + F(3, 2) * F(1, 3)) / (F(1, 6) + F(2, 3) + F(1, 3))
assert abs(wa - float(exact)) < 1e-12
cog, _ = mamdani(e, ec)
print(f"加权平均 = {exact} ≈ {wa:.3f}；重心法 ≈ {cog:.3f}")

# 4. 控制面单调、对称
for x in (-2.5, -1, 0, 1, 2.5):
    for y in (-2, 0, 2):
        assert abs(mamdani(x, y)[0] + mamdani(-x, -y)[0]) < 1e-6
assert abs(mamdani(0, 0)[0]) < 1e-9
print("控制面关于原点对称，u(0,0)=0：OK")

# 5. ILC 收敛条件 |1 - Γ CB| < 1
CB = C @ B
print("CB =", CB)
for g in (0.5, 1.0, 1.5, 2.2):
    rho = abs(1 - g * CB)
    errs, _ = ilc(g, 30)
    print(f"Γ={g}: |1-ΓCB|={rho:.2f}, 第 1/5/10/30 次最大误差 =",
          ", ".join(f"{errs[i]:.3g}" for i in (0, 4, 9, 29)))
    if rho < 1:
        assert errs[-1] < 1e-3
    else:
        assert errs[-1] > errs[0]
print("ρ<1 时收敛、ρ>1 时发散：OK")


# 6. 收敛但非单调：慢衰减对象的瞬态暴涨
import intelligent_common as m
m.A = np.array([[0.0, 1.0], [-0.5, 1.2]]); m.C = np.array([0.5, 1.0])
assert m.C @ m.B == 1.0
print("慢对象极点模:", np.abs(np.linalg.eigvals(m.A)).round(3))
errs, _ = m.ilc(0.5, 30)
print(f"慢对象 Γ=0.5：第 30 次最大误差 {errs[-1]:.3g}")
assert 3e5 < errs[-1] < 5e5
print("全部通过")
