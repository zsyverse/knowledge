"""「编码器」一文中所有数字与例子的核对。

    .venv/bin/python scripts/encoder/verify_encoder.py
"""
import itertools

import numpy as np

# 1. 增量式：分辨率与四倍频
ppr = 1000
print(f"[增量] {ppr} 线，四倍频后每圈 {4*ppr} 计数，角分辨率 {360/(4*ppr):.3f}°")
assert 360 / (4 * ppr) == 0.09

# 正交解码：状态表 (A,B) 序列 00→10→11→01 为正转（A 超前）
seq_fwd = [(0, 0), (1, 0), (1, 1), (0, 1)]
idx = {s: i for i, s in enumerate(seq_fwd)}
def decode(states):
    cnt = 0
    for p, q in zip(states, states[1:]):
        d = (idx[q] - idx[p]) % 4
        cnt += {0: 0, 1: +1, 3: -1}[d]          # d == 2 为丢步（非法跳变）
    return cnt
fwd = seq_fwd * 3 + [seq_fwd[0]]
assert decode(fwd) == 12 and decode(fwd[::-1]) == -12
print("[增量] A 超前 B 计 +1，B 超前 A 计 −1：OK")

# 2. 绝对式：格雷码相邻只差 1 位，二进制最多 n 位
for n in (3, 10, 17):
    g = [k ^ (k >> 1) for k in range(2 ** n)]
    gw = max(bin(g[k] ^ g[(k + 1) % 2 ** n]).count("1") for k in range(2 ** n))
    bw = max(bin(k ^ ((k + 1) % 2 ** n)).count("1") for k in range(2 ** n))
    assert gw == 1 and bw == n
    # 格雷码 → 二进制
    def g2b(x):
        b = 0
        while x:
            b ^= x
            x >>= 1
        return b
    assert all(g2b(g[k]) == k for k in range(2 ** n))
print("[绝对] 格雷码相邻 1 位、二进制最坏 n 位翻转、格雷码可逆：OK")
print(f"[绝对] 17 位单圈 = {2**17} 个位置，{360*3600/2**17:.1f} 角秒/位置")

# 3. 8 线-3 线优先编码器（74LS148 逻辑，低电平有效）
def ls148(I, EI=0):
    """I[0..7] 低电平有效输入，I7 优先级最高。返回 (A2,A1,A0,GS,EO)，均低电平有效。"""
    if EI == 1:
        return (1, 1, 1, 1, 1)
    for k in range(7, -1, -1):
        if I[k] == 0:
            code = (~k) & 0b111                   # 输出为反码
            return ((code >> 2) & 1, (code >> 1) & 1, code & 1, 0, 1)
    return (1, 1, 1, 1, 0)
# 例：I3 与 I5 同时有效 → 输出 5 的反码 010
I = [1] * 8; I[3] = 0; I[5] = 0
assert ls148(I)[:3] == (0, 1, 0)
# 全部组合：输出总是最高有效输入的编号
for bits in itertools.product((0, 1), repeat=8):
    out = ls148(list(bits))
    act = [k for k in range(8) if bits[k] == 0]
    if act:
        a = (~((out[0] << 2) | (out[1] << 1) | out[2])) & 7
        assert a == max(act) and out[3] == 0
    else:
        assert out[3] == 1 and out[4] == 0
print("[数字] 74LS148 真值表 256 种输入全部只编码最高优先级：OK")

# 普通编码器在两路同时有效时出错：OR 门实现 Y2=I4|I5|I6|I7 ...
def simple(I):
    return tuple(int(any(I[k] for k in range(8) if (k >> b) & 1)) for b in (2, 1, 0))
I = [0] * 8; I[3] = I[5] = 1
print("[数字] 普通编码器 I3、I5 同时为 1 →", simple(I), "= 7（两者都不是）")
assert simple(I) == (1, 1, 1)

# 4. 视频码率：1080p60 8-bit 4:2:0 原始数据量
raw = 1920 * 1080 * 1.5 * 8 * 60
print(f"[视频] 1080p60 原始 {raw/1e9:.2f} Gbit/s = {raw/8/1e6:.0f} MB/s；压到 6 Mbit/s 约 {raw/6e6:.0f}:1")
raw4k = 3840 * 2160 * 3 * 10 * 60
print(f"[视频] 4K60 10-bit 4:4:4 原始 {raw4k/1e9:.1f} Gbit/s = {raw4k/8/1e9:.2f} GB/s")

# 5. 汉明码 (7,4)：纠正任意 1 位错误
G = np.array([[1,0,0,0,1,1,0],[0,1,0,0,1,0,1],[0,0,1,0,0,1,1],[0,0,0,1,1,1,1]])
H = np.array([[1,1,0,1,1,0,0],[1,0,1,1,0,1,0],[0,1,1,1,0,0,1]])
assert not (G @ H.T % 2).any()
for msg in itertools.product((0, 1), repeat=4):
    c = np.array(msg) @ G % 2
    for e in range(7):
        r = c.copy(); r[e] ^= 1
        s = H @ r % 2
        pos = [j for j in range(7) if (H[:, j] == s).all()][0]
        r[pos] ^= 1
        assert (r == c).all()
print("[信道] 汉明(7,4)：16 个码字 × 7 个错误位置全部纠正，码率 4/7 =", round(4/7, 3))

# 6. One-hot 与序数编码
cats = ["红", "黄", "蓝"]
onehot = np.eye(3, dtype=int)
d = [np.linalg.norm(onehot[i] - onehot[j]) for i, j in ((0, 1), (0, 2), (1, 2))]
assert np.allclose(d, np.sqrt(2))
print("[特征] one-hot 任意两类距离都是 √2；序数 0/1/2 下 红-蓝 距离是 红-黄 的 2 倍")

# 7. Stable Diffusion VAE：512×512×3 → 64×64×4
print(f"[AI] SD VAE 压缩比 {512*512*3/(64*64*4):.0f} 倍（元素数）")
assert 512 * 512 * 3 / (64 * 64 * 4) == 48
print("全部通过")
