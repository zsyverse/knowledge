---
date: 2026-11-05
description: 贪心（区间问题、跳跃游戏、分发糖果、加油站）、字符串（KMP、字符串哈希、字典树）、位运算技巧、数学（最大公约数、快速幂、质数筛、取模与逆元、组合数），以及大模型岗位笔试面试中常见的手撕题方向。
tags:
  - 算法
---

# 贪心、字符串与数学

## 1. 贪心

每一步都做当前看起来最好的选择。贪心的难点不在代码，而在于证明（或者至少说服自己）局部最优能导出全局最优。常用的论证方法是**交换论证**：假设最优解在某一步和贪心的选择不同，把它换成贪心的选择，结果不会变差。

拿不准时，写个暴力解对拍几百组随机数据，比证明更快。

### 区间问题

**无重叠区间（力扣 435）**：删除最少的区间使剩下的互不重叠。等价于保留最多的不重叠区间：按**右端点**排序，每次选结束最早的。

```python
def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda x: x[1])
    keep, end = 0, float("-inf")
    for s, e in intervals:
        if s >= end:
            keep += 1
            end = e
    return len(intervals) - keep

print(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))   # 1
```

结束得越早，留给后面的空间越多，这就是交换论证：如果最优解选的第一个区间不是结束最早的，把它换成结束最早的那个，不会和后面的冲突。

**合并区间（力扣 56）**：按**左端点**排序，依次合并。

```python
def merge(intervals):
    intervals.sort()
    res = []
    for s, e in intervals:
        if res and s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res

print(merge([[1, 3], [2, 6], [8, 10], [15, 18]]))   # [[1, 6], [8, 10], [15, 18]]
```

**用最少数量的箭引爆气球（力扣 452）**：和 435 一样按右端点排序，箭射在当前区间的右端点。

```python
def find_min_arrow_shots(points):
    points.sort(key=lambda p: p[1])
    arrows, pos = 0, float("-inf")
    for s, e in points:
        if s > pos:
            arrows += 1
            pos = e
    return arrows

print(find_min_arrow_shots([[10, 16], [2, 8], [1, 6], [7, 12]]))   # 2
```

### 跳跃游戏

**跳跃游戏（力扣 55）**：维护能到达的最远位置。

```python
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True

def jump(nums):           # 力扣 45：最少跳几次
    steps = end = reach = 0
    for i in range(len(nums) - 1):
        reach = max(reach, i + nums[i])
        if i == end:      # 到达当前这一跳的边界，必须再跳一次
            steps += 1
            end = reach
    return steps

print(can_jump([2, 3, 1, 1, 4]), can_jump([3, 2, 1, 0, 4]), jump([2, 3, 1, 1, 4]))   # True False 2
```

`jump` 实际上是按层的 BFS：每一层是"跳 k 次能到达的位置"。

### 其他经典贪心

**分发糖果（力扣 135）**：评分高的孩子要比相邻的孩子糖多。从左到右满足左边的约束，再从右到左满足右边的约束，取两者的最大值。

```python
def candy(ratings):
    n = len(ratings)
    left = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            left[i] = left[i - 1] + 1
    total, right = left[-1], 1
    for i in range(n - 2, -1, -1):
        right = right + 1 if ratings[i] > ratings[i + 1] else 1
        total += max(left[i], right)
    return total

print(candy([1, 0, 2]), candy([1, 2, 2]))   # 5 4
```

**加油站（力扣 134）**：总油量不少于总消耗就一定有解。从起点出发，油量一旦变成负数，说明从起点到当前位置之间的任何一站出发都不行，起点改为下一站。

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start

print(can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]))   # 3
```

**划分字母区间（力扣 763）**：记录每个字母最后出现的位置，当前片段必须延伸到其中所有字母的最后位置。

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    res, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res

print(partition_labels("ababcbacadefegdehijhklij"))   # [9, 7, 8]
```

## 2. 字符串

Python 的字符串方法（`find`、`count`、`split`、`in`）都是 C 实现，日常的子串查找直接用它们就行。需要手写 KMP 的场景主要是面试要求，或者需要用到 KMP 的 `next` 数组本身（例如求最短循环节）。

### KMP

`nxt[i]` 是 `p[0..i]` 的最长相等真前后缀的长度。匹配失败时，模式串不用从头开始，而是跳到 `nxt[j-1]` 继续比较。

```python
def build_next(p):
    nxt = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j and p[i] != p[j]:
            j = nxt[j - 1]
        if p[i] == p[j]:
            j += 1
        nxt[i] = j
    return nxt

def kmp_search(s, p):
    """返回 p 在 s 中所有出现的起始位置"""
    if not p:
        return list(range(len(s) + 1))
    nxt = build_next(p)
    res, j = [], 0
    for i, c in enumerate(s):
        while j and c != p[j]:
            j = nxt[j - 1]
        if c == p[j]:
            j += 1
        if j == len(p):
            res.append(i - j + 1)
            j = nxt[j - 1]
    return res

print(build_next("abacabab"))                  # [0, 0, 1, 0, 1, 2, 3, 2]
print(kmp_search("ababcabcabababd", "ababd"))  # [10]
print(kmp_search("aaaa", "aa"))                # [0, 1, 2]
```

**重复的子字符串（力扣 459）**：字符串由某个子串重复多次构成，当且仅当 `n % (n - nxt[n-1]) == 0` 且 `nxt[n-1] > 0`，最短循环节长度为 `n - nxt[n-1]`。

```python
def repeated_substring(s):
    n = len(s)
    k = build_next(s)[-1]
    return k > 0 and n % (n - k) == 0

print(repeated_substring("abcabcabc"), repeated_substring("aba"))   # True False
```

不用 KMP 的写法：`s in (s + s)[1:-1]`。

### 字符串哈希

把字符串看成一个 $B$ 进制数并对大质数取模，预处理前缀哈希后，任意子串的哈希值可以 $O(1)$ 得到。用于快速比较子串是否相等。

```python
class StrHash:
    MOD = (1 << 61) - 1
    BASE = 131

    def __init__(self, s):
        n = len(s)
        self.h = [0] * (n + 1)
        self.p = [1] * (n + 1)
        M, B = self.MOD, self.BASE
        for i, c in enumerate(s):
            self.h[i + 1] = (self.h[i] * B + ord(c)) % M
            self.p[i + 1] = self.p[i] * B % M

    def get(self, l, r):
        """子串 s[l:r] 的哈希"""
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.MOD

s = "abcabcx"
H = StrHash(s)
print(H.get(0, 3) == H.get(3, 6), H.get(0, 3) == H.get(1, 4))   # True False
```

**最长重复子串（力扣 1044）**：二分长度 L，对每个 L 用哈希检查是否有两个相同的长度为 L 的子串。复杂度 $O(n \log n)$。

```python
def longest_dup_substring(s):
    H = StrHash(s)
    def find(L):
        seen = {}
        for i in range(len(s) - L + 1):
            h = H.get(i, i + L)
            if h in seen:
                return i
            seen[h] = i
        return -1
    lo, hi, best = 1, len(s) - 1, ""
    while lo <= hi:
        mid = (lo + hi) // 2
        i = find(mid)
        if i != -1:
            best = s[i:i + mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return best

print(longest_dup_substring("banana"))   # ana
```

模数取 $2^{61}-1$ 时冲突概率极低。Python 的大整数让这个乘法不会溢出，C++ 里要用 `__int128` 才能这样写。

### 字典树（Trie）

用于前缀查询：判断某个前缀是否存在、统计以某前缀开头的单词数、自动补全。

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
            node["#cnt"] = node.get("#cnt", 0) + 1     # 经过该节点的单词数
        node["#end"] = True

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.get("#end", False)

    def count_prefix(self, prefix):
        node = self._walk(prefix)
        return 0 if node is None else node.get("#cnt", 0)

    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node:
                return None
            node = node[c]
        return node

t = Trie()
for w in ["apple", "app", "apply", "bat"]:
    t.insert(w)
print(t.search("app"), t.search("appl"), t.count_prefix("app"), t.count_prefix("b"))   # True False 3 1
```

用嵌套 dict 写 Trie 最简洁，`"#cnt"`、`"#end"` 这两个 key 不会和单个字符冲突。

**数组中两个数的最大异或值（力扣 421）**：把每个数的二进制位从高到低插入 Trie，对每个数贪心地往"相反的位"走。

```python
def find_maximum_xor(nums):
    HIGH = max(nums).bit_length()
    root = {}
    best = 0
    for x in nums:
        node = root                        # 插入
        for b in range(HIGH - 1, -1, -1):
            node = node.setdefault(x >> b & 1, {})
        node, cur = root, 0                # 查询
        for b in range(HIGH - 1, -1, -1):
            bit = x >> b & 1
            if 1 - bit in node:
                cur |= 1 << b
                node = node[1 - bit]
            else:
                node = node[bit]
        best = max(best, cur)
    return best

print(find_maximum_xor([3, 10, 5, 25, 2, 8]))   # 28
```

## 3. 位运算

```python
x = 0b10110
print(x & 1)                  # 0，判断奇偶
print(x & (x - 1))            # 20 (0b10100)，去掉最低位的 1
print(x & -x)                 # 2，只保留最低位的 1
print(bin(x).count("1"), x.bit_count())   # 3 3
print(x.bit_length())         # 5
print(5 ^ 5, 5 ^ 0)           # 0 5
```

**只出现一次的数字（力扣 136）**：其他数都出现两次，全部异或起来，成对的抵消为 0。

```python
from functools import reduce
from operator import xor
print(reduce(xor, [4, 1, 2, 1, 2]))   # 4
```

**只出现一次的数字 III（力扣 260）**：两个数只出现一次。全部异或得到 `a ^ b`，取它最低位的 1，按这一位把所有数分成两组，每组分别异或。

```python
def single_number3(nums):
    ab = reduce(xor, nums)
    low = ab & -ab
    a = 0
    for x in nums:
        if x & low:
            a ^= x
    return sorted([a, ab ^ a])

print(single_number3([1, 2, 1, 3, 2, 5]))   # [3, 5]
```

**比特位计数（力扣 338）**：`bits[i] = bits[i >> 1] + (i & 1)`。

```python
def count_bits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits

print(count_bits(5))   # [0, 1, 1, 2, 1, 2]
```

Python 的整数是任意精度的，负数的位运算按"无限长的补码"处理，`-1 >> 1` 仍然是 `-1`，`bin(-5)` 是 `'-0b101'`。题目要求按 32 位处理时，用 `x & 0xFFFFFFFF` 截断，结果大于 `0x7FFFFFFF` 时减去 `1 << 32` 还原成负数。

## 4. 数学

### 最大公约数

```python
from math import gcd

def my_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(my_gcd(48, 18), gcd(48, 18), 48 * 18 // gcd(48, 18))   # 6 6 144
```

### 快速幂

```python
def qpow(a, n, mod):
    res = 1
    a %= mod
    while n:
        if n & 1:
            res = res * a % mod
        a = a * a % mod
        n >>= 1
    return res

MOD = 10**9 + 7
print(qpow(2, 10**18, MOD) == pow(2, 10**18, MOD))   # True
```

Python 内置的 `pow(a, n, mod)` 就是快速幂，笔试中直接用。面试可能要求手写，或者扩展到矩阵快速幂（用于 $O(\log n)$ 求斐波那契数列第 n 项这类线性递推）：

```python
def mat_mul(A, B, mod):
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][t] * B[t][j] for t in range(k)) % mod for j in range(m)] for i in range(n)]

def fib(n, mod=10**9 + 7):
    res = [[1, 0], [0, 1]]
    M = [[1, 1], [1, 0]]
    while n:
        if n & 1:
            res = mat_mul(res, M, mod)
        M = mat_mul(M, M, mod)
        n >>= 1
    return res[0][1]

print([fib(i) for i in range(10)], fib(10**18))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34] 209783453
```

### 质数

```python
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def sieve(n):
    """埃氏筛：返回 [0, n] 中每个数是否为质数"""
    is_p = bytearray([1]) * (n + 1)
    is_p[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(range(i * i, n + 1, i)))   # 切片赋值，一次标记所有倍数
    return is_p

def factorize(n):
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res

p = sieve(100)
print(sum(p), [i for i in range(30) if p[i]])   # 25 [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
print(is_prime(97), factorize(360))             # True [2, 2, 2, 3, 3, 5]
print(sum(sieve(10**6)))                        # 78498
```

筛法里用切片赋值代替内层循环，在 Python 中快很多，$10^7$ 的范围也能在一秒左右完成。

### 取模与组合数

答案很大、要求"对 $10^9+7$ 取模"时，加法和乘法可以随时取模；**除法不能直接取模**，要乘以逆元。$p$ 是质数时，由费马小定理，$a$ 的逆元是 $a^{p-2} \bmod p$。

```python
MOD = 10**9 + 7
print(pow(3, MOD - 2, MOD) * 3 % MOD)   # 1
print(pow(3, -1, MOD) == pow(3, MOD - 2, MOD))   # True，3.8+ 支持 pow(a, -1, m)
```

多次求组合数 $C(n, k) \bmod p$ 时，预处理阶乘和阶乘的逆元：

```python
def build_comb(N, mod=10**9 + 7):
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (N + 1)
    inv[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv[k] % mod * inv[n - k] % mod
    return C

C = build_comb(10**5)
from math import comb
print(C(10, 3), C(100000, 50000) == comb(100000, 50000) % (10**9 + 7))   # 120 True
```

逆阶乘从后往前递推（`inv[i-1] = inv[i] * i`），只需要做一次快速幂。

**不同路径（力扣 62）**：$m \times n$ 网格从左上到右下，答案就是 $C(m+n-2, m-1)$，用组合数比 DP 更快。

```python
print(comb(3 + 7 - 2, 3 - 1))   # 28
```

### 其他常用结论

- $1 + 2 + \dots + n = n(n+1)/2$；等比数列求和。
- 判断一个数是否为完全平方数：`math.isqrt(n) ** 2 == n`。
- 一个数的约数个数：分解质因数 $n = \prod p_i^{a_i}$，约数个数 $\prod (a_i + 1)$。
- 卡特兰数 $C_n = \binom{2n}{n} / (n+1)$：n 对括号的合法序列数、n 个节点的二叉搜索树个数（力扣 96）、出栈序列数。
- 鸽巢原理：n+1 个数放进 n 个盒子，必有一个盒子至少两个。前缀和取模的题目里常用到。

### 随机与采样

**洗牌算法（Fisher-Yates）**：从后往前，每个位置和前面（含自身）随机一个位置交换，得到均匀随机的排列。

```python
import random

def shuffle(a):
    a = a[:]
    for i in range(len(a) - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a

random.seed(0)
from collections import Counter
cnt = Counter(tuple(shuffle([1, 2, 3])) for _ in range(60000))
print(len(cnt), min(cnt.values()) > 9000)   # 6 True，6 种排列出现次数大致相等
```

**蓄水池抽样**：从一个长度未知的数据流中均匀地取 k 个样本，只遍历一次。第 i 个元素（从 1 计）以 $k/i$ 的概率被保留，替换掉蓄水池中随机一个。

```python
def reservoir_sample(stream, k):
    pool = []
    for i, x in enumerate(stream, 1):
        if i <= k:
            pool.append(x)
        else:
            j = random.randint(1, i)
            if j <= k:
                pool[j - 1] = x
    return pool

random.seed(1)
cnt = Counter()
for _ in range(20000):
    cnt.update(reservoir_sample(range(10), 3))
print(sorted(round(cnt[i] / 20000, 2) for i in range(10)))   # 每个元素被选中的概率都约为 0.3
```

从海量语料中随机抽样一部分数据时，蓄水池抽样很实用：不需要知道总数，也不需要把数据全部读进内存。

## 5. 大模型岗位的笔试与面试

算法岗的笔试和其他岗位基本相同，题型就是前面各章的内容，难度多在力扣中等到困难之间。面试手撕代码除了常规算法题，还常要求现场实现模型相关的组件。这部分内容在 [Python 编程](../python/index.md) 中有完整代码：

| 手撕内容 | 位置 |
| --- | --- |
| softmax、log_softmax、交叉熵（数值稳定） | [NumPy](../python/numpy.md) |
| 多头注意力、因果掩码 | [NumPy](../python/numpy.md) |
| top-k / top-p 采样 | [综合练习](../python/exercises.md) |
| BPE 训练与编码 | [综合练习](../python/exercises.md) |
| RMSNorm、LayerNorm | [综合练习](../python/exercises.md) |
| GRPO 组内优势、token 级 log 概率 | [综合练习](../python/exercises.md)、[PyTorch 基础](../python/pytorch.md) |
| 训练循环、梯度累积 | [PyTorch 基础](../python/pytorch.md) |

此外，LRU 缓存、编辑距离、Trie、Top K（堆）、蓄水池抽样、带权随机采样（前缀和加二分）在大模型岗位的面试中出现得比较多，因为它们和 KV cache 管理、文本评测、词表、数据采样等实际问题直接相关。

带权随机采样（力扣 528）：

```python
import random
from bisect import bisect_right
from itertools import accumulate

class WeightedSampler:
    def __init__(self, w):
        self.pre = list(accumulate(w))
    def pick(self):
        r = random.random() * self.pre[-1]
        return bisect_right(self.pre, r)

random.seed(0)
s = WeightedSampler([1, 3, 6])
cnt = Counter(s.pick() for _ in range(100000))
print([round(cnt[i] / 100000, 2) for i in range(3)])   # [0.1, 0.3, 0.6]
```

这就是按概率从词表中采样 token 的基本方法：对概率求前缀和，在 $[0, 1)$ 中取随机数，二分找到它落在哪个区间。
