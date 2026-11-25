"""Verify the numbers on docs/ai/rl/importance-sampling.md."""
import numpy as np
from math import erfc, exp, sqrt

sf = lambda z: 0.5 * erfc(z / sqrt(2))
mu = sf(3)                                 # P(X>3), X~N(0,1)
assert abs(mu - 1.35e-3) < 1e-5, mu

N = 10_000
# direct MC: relative std of the hit-rate estimator
rel_mc = np.sqrt((1 - mu) / (N * mu))
assert abs(rel_mc - 0.272) < 2e-3, rel_mc

# IS with q = N(3,1): w = p/q = exp(-3x + 4.5)
# E_q[w^2 1{x>3}] = E_p[w 1{x>3}] = e^{9} P(X>6), X~N(0,1)  (closed form)
m2 = exp(9) * sf(6)
rel_is = np.sqrt((m2 - mu**2) / N) / mu
assert abs(rel_is - 0.0184) < 2e-4, rel_is
# variance ratio
ratio = (mu * (1 - mu)) / (m2 - mu**2)
assert 215 < ratio < 222, ratio

# Monte Carlo check with a fixed seed
rng = np.random.default_rng(0)
reps = 2000
x = rng.standard_normal((reps, N)); mc = (x > 3).mean(1)
y = rng.standard_normal((reps, N)) + 3
is_ = ((y > 3) * np.exp(-3 * y + 4.5)).mean(1)
assert abs(mc.std() / mu - rel_mc) < 0.02
assert abs(is_.std() / mu - rel_is) < 0.003
assert abs(is_.mean() / mu - 1) < 0.002

# RL weight example and trajectory weight
assert 0.8 / 0.2 == 4
w_traj = 1.1 ** 20
assert abs(w_traj - 6.73) < 0.01, w_traj
assert abs(0.9 ** 20 - 0.122) < 1e-3

# ESS example
w = np.array([4.0, 1, 1, 1, 1, 1, 1, 1, 1, 1])  # 10 samples, one weight 4
ess = w.sum() ** 2 / (w**2).sum()
assert abs(ess - 6.76) < 1e-9, ess

print(f"mu={mu:.4e} rel_mc={rel_mc:.3f} rel_is={rel_is:.4f} ratio={ratio:.0f} "
      f"1.1^20={w_traj:.2f} ess={ess}")
print("OK")
