---
date: 2026-11-05
description: 动态规划的思考步骤，从记忆化搜索到递推；线性 DP、打家劫舍、股票问题、网格路径、0-1 背包与完全背包、最长递增子序列、最长公共子序列与编辑距离、区间 DP、状态压缩 DP，以及空间优化。
tags:
  - 算法
---

# 动态规划

动态规划（DP）适用于有**重叠子问题**和**最优子结构**的问题：大问题的最优解可以由小问题的最优解推出，而且同一个小问题会被多次用到。

## 1. 思考步骤

1. **定义状态**：`dp[i]`（或 `dp[i][j]`）表示什么。这一步最关键，定义得好，转移就自然了。常见的定义方式："前 i 个元素的……"、"以第 i 个元素结尾的……"、"区间 [i, j] 的……"。
2. **转移方程**：`dp[i]` 怎样由更小的状态得到。一般考虑"最后一步做了什么"。
3. **初始值和边界**。
4. **计算顺序**：保证计算 `dp[i]` 时，它依赖的状态都已经算好。
5. **答案**是哪个状态。

想不清楚递推时，先写记忆化搜索：递归函数的参数就是状态，函数体就是转移方程。写对之后再改成递推，或者直接提交记忆化版本（数据规模不大时）。

**例：爬楼梯（力扣 70）**，每次走 1 或 2 级，到第 n 级有多少种方法。最后一步要么从 n-1 级走 1 级，要么从 n-2 级走 2 级。

```python
from functools import lru_cache

def climb_memo(n):
    @lru_cache(maxsize=None)
    def f(i):
        if i <= 1:
            return 1
        return f(i - 1) + f(i - 2)
    return f(n)

def climb_dp(n):
    dp = [1] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

def climb_O1(n):
    a, b = 1, 1             # dp[i-2], dp[i-1]
    for _ in range(n - 1):
        a, b = b, a + b
    return b

print(climb_memo(10), climb_dp(10), climb_O1(10))   # 89 89 89
```

`dp[i]` 只依赖前两项时，只保留两个变量，空间从 $O(n)$ 降到 $O(1)$。

## 2. 线性 DP

**打家劫舍（力扣 198）**：不能偷相邻的两家，求最大金额。`dp[i]` = 前 i 家能偷到的最大金额，第 i 家要么不偷（`dp[i-1]`），要么偷（`dp[i-2] + nums[i-1]`）。

```python
def rob(nums):
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1

def rob_circle(nums):          # 力扣 213：房子围成一圈，首尾不能同时偷
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[1:]), rob(nums[:-1]))

print(rob([2, 7, 9, 3, 1]), rob_circle([2, 3, 2]), rob_circle([1, 2, 3, 1]))   # 12 3 4
```

**乘积最大子数组（力扣 152）**：负数会让最大值和最小值互换，所以同时维护以当前元素结尾的最大积和最小积。

```python
def max_product(nums):
    hi = lo = best = nums[0]
    for x in nums[1:]:
        cands = (x, hi * x, lo * x)
        hi, lo = max(cands), min(cands)
        best = max(best, hi)
    return best

print(max_product([2, 3, -2, 4]), max_product([-2, 3, -4]))   # 6 24
```

**解码方法（力扣 91）**：`'A' -> 1, ..., 'Z' -> 26`，求数字串的解码方法数。

```python
def num_decodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]                     # 最后一位单独解码
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:
            dp[i] += dp[i - 2]                     # 最后两位一起解码
    return dp[n]

print(num_decodings("226"), num_decodings("06"), num_decodings("11106"))   # 3 0 2
```

### 股票问题

**买卖股票的最佳时机 II（力扣 122）**：可以多次交易，但手里最多一股。每天有两种状态：持有股票、不持有股票。

```python
def max_profit_multi(prices):
    hold, free = -prices[0], 0
    for p in prices[1:]:
        hold, free = max(hold, free - p), max(free, hold + p)
    return free

def max_profit_cooldown(prices):     # 力扣 309：卖出后第二天不能买
    hold, free, cool = -prices[0], 0, 0      # cool：今天刚卖出
    for p in prices[1:]:
        hold, free, cool = max(hold, free - p), max(free, cool), hold + p
    return max(free, cool)

def max_profit_k(prices, k):         # 力扣 188：最多 k 笔交易
    buy = [float("-inf")] * (k + 1)  # buy[j]：进行第 j 笔交易、目前持有
    sell = [0] * (k + 1)             # sell[j]：已完成 j 笔交易、目前不持有
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]

print(max_profit_multi([7, 1, 5, 3, 6, 4]), max_profit_cooldown([1, 2, 3, 0, 2]), max_profit_k([3, 2, 6, 5, 0, 3], 2))   # 7 3 7
```

所有股票题都是同一个思路：列出每天可能处于的状态（持有/不持有/冷冻期/已交易几次），写出状态之间的转移。

## 3. 网格 DP

**不同路径 II（力扣 63）**：从左上到右下，只能向右或向下，有障碍物。`dp[i][j] = dp[i-1][j] + dp[i][j-1]`。

```python
def unique_paths_with_obstacles(grid):
    m = len(grid[0])
    dp = [0] * m
    dp[0] = 1
    for row in grid:
        for j in range(m):
            if row[j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]          # dp[j] 原值是上方，dp[j-1] 是左方
    return dp[-1]

print(unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))   # 2
```

二维 DP 只依赖上一行和当前行左边时，可以压缩成一维数组，从左到右更新。

**最小路径和（力扣 64）**和**三角形最小路径和（力扣 120）**结构相同。

**最大正方形（力扣 221）**：`dp[i][j]` 是以 `(i, j)` 为右下角的最大全 1 正方形边长，等于左、上、左上三者的最小值加 1。

```python
def maximal_square(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if matrix[i - 1][j - 1] == "1":
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                best = max(best, dp[i][j])
    return best * best

print(maximal_square(["10100", "10111", "11111", "10010"]))   # 4
```

## 4. 背包

### 0-1 背包

$n$ 件物品，第 $i$ 件重量 $w_i$、价值 $v_i$，背包容量 $W$，每件物品最多选一次，求最大价值。

`dp[i][c]` = 只考虑前 i 件物品、容量为 c 时的最大价值。第 i 件不选：`dp[i-1][c]`；选：`dp[i-1][c - w_i] + v_i`。

压缩成一维时，容量必须**从大到小**遍历，这样 `dp[c - w]` 还是上一轮（没有用过第 i 件物品）的值：

```python
def knapsack_01(weights, values, W):
    dp = [0] * (W + 1)
    for w, v in zip(weights, values):
        for c in range(W, w - 1, -1):     # 倒序
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[W]

print(knapsack_01([1, 3, 4], [15, 20, 30], 4))   # 35
```

ACM 模式的标准写法：第一行 n、W，接下来 n 行每行一件物品的重量和价值。

```python
import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, W = data[0], data[1]
    dp = [0] * (W + 1)
    for i in range(n):
        w, v = data[2 + 2 * i], data[3 + 2 * i]
        for c in range(W, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    print(dp[W])

main()
```

输入

```text
4 5
1 2
2 4
3 4
4 5
```

输出

```text
8
```

内层用 `if` 代替 `max()`，避免函数调用开销，在 Python 里能快不少。

很多题目不会直接说"背包"，需要自己看出来：

**分割等和子集（力扣 416）**：能否把数组分成和相等的两部分 = 能否选出一些数，和恰好为 `sum / 2`。

```python
def can_partition(nums):
    s = sum(nums)
    if s % 2:
        return False
    t = s // 2
    dp = [False] * (t + 1)
    dp[0] = True
    for x in nums:
        for c in range(t, x - 1, -1):
            dp[c] = dp[c] or dp[c - x]
    return dp[t]

print(can_partition([1, 5, 11, 5]), can_partition([1, 2, 3, 5]))   # True False
```

Python 里这类"能否凑出"的问题可以用大整数的位运算加速：第 c 位为 1 表示和 c 可以凑出。

```python
def can_partition_bits(nums):
    s = sum(nums)
    if s % 2:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return bits >> (s // 2) & 1 == 1

print(can_partition_bits([1, 5, 11, 5]), can_partition_bits([1, 2, 3, 5]))   # True False
```

**目标和（力扣 494）**：给每个数添加正负号，使总和为 target 的方法数。设正数部分和为 $p$，则 $p - (s - p) = target$，$p = (s + target) / 2$，转化为"选出和为 p 的方案数"。

```python
def find_target_sum_ways(nums, target):
    s = sum(nums)
    if abs(target) > s or (s + target) % 2:
        return 0
    p = (s + target) // 2
    dp = [0] * (p + 1)
    dp[0] = 1
    for x in nums:
        for c in range(p, x - 1, -1):
            dp[c] += dp[c - x]
    return dp[p]

print(find_target_sum_ways([1, 1, 1, 1, 1], 3))   # 5
```

### 完全背包

每件物品可以选无限次。一维写法中，容量**从小到大**遍历，`dp[c - w]` 已经是"可能用过第 i 件物品"的值，正好对应可以重复选。

**零钱兑换（力扣 322）**：凑出金额的最少硬币数。

```python
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for c in coins:
        for a in range(c, amount + 1):    # 正序
            if dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1

print(coin_change([1, 2, 5], 11), coin_change([2], 3))   # 3 -1
```

**零钱兑换 II（力扣 518）**：凑出金额的组合数。外层遍历硬币、内层遍历金额，得到的是**组合数**（不区分顺序）；如果外层遍历金额、内层遍历硬币，得到的是**排列数**（力扣 377）。

```python
def change(amount, coins):        # 组合数
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]

def combination_sum4(nums, target):   # 排列数
    dp = [1] + [0] * target
    for a in range(1, target + 1):
        for x in nums:
            if x <= a:
                dp[a] += dp[a - x]
    return dp[target]

print(change(5, [1, 2, 5]), combination_sum4([1, 2, 3], 4))   # 4 7
```

| 问题 | 遍历顺序 |
| --- | --- |
| 0-1 背包 | 物品在外，容量**倒序** |
| 完全背包 | 物品在外，容量**正序** |
| 求组合数 | 物品在外，容量在内 |
| 求排列数 | 容量在外，物品在内 |

**多重背包**（每件物品最多选 $k_i$ 次）可以把 $k_i$ 拆成 $1, 2, 4, \dots$ 的二进制组合，转成 0-1 背包。

## 5. 子序列 DP

### 最长递增子序列（力扣 300）

$O(n^2)$ 写法：`dp[i]` 是以 `nums[i]` 结尾的最长递增子序列长度。

```python
def lis_n2(nums):
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

$O(n \log n)$ 写法：`tails[k]` 是长度为 k+1 的递增子序列中，最小的结尾元素。`tails` 是严格递增的，每个新元素用二分找到它该替换的位置。

```python
from bisect import bisect_left

def lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

print(lis_n2([10, 9, 2, 5, 3, 7, 101, 18]), lis([10, 9, 2, 5, 3, 7, 101, 18]))   # 4 4
```

求最长**非递减**子序列时，把 `bisect_left` 换成 `bisect_right`。注意 `tails` 本身不一定是一个真实的子序列，只有长度是对的。

**俄罗斯套娃信封（力扣 354）**：按宽度升序、宽度相同时高度**降序**排序，然后对高度求 LIS。高度降序是为了防止宽度相同的信封互相套。

```python
def max_envelopes(envs):
    envs.sort(key=lambda e: (e[0], -e[1]))
    return lis([h for _, h in envs])

print(max_envelopes([[5, 4], [6, 4], [6, 7], [2, 3]]))   # 3
```

### 最长公共子序列（力扣 1143）

`dp[i][j]` 是 `a` 的前 i 个字符和 `b` 的前 j 个字符的 LCS 长度。

```python
def lcs(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # 回溯出一个具体的 LCS
    i, j, out = n, m, []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], "".join(reversed(out))

print(lcs("abcde", "ace"), lcs("abc", "def"))   # (3, 'ace') (0, '')
```

下标从 1 开始，`dp[0][*]` 和 `dp[*][0]` 表示空串，省去边界判断。

### 编辑距离（力扣 72）

把 `a` 变成 `b` 的最少操作数（插入、删除、替换一个字符）。

```python
def min_distance(a, b):
    n, m = len(a), len(b)
    prev = list(range(m + 1))               # dp[0][j] = j：空串变成 b 的前 j 个字符
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j],        # 删除 a[i-1]
                                 cur[j - 1],     # 插入 b[j-1]
                                 prev[j - 1])    # 替换
        prev = cur
    return prev[m]

print(min_distance("horse", "ros"), min_distance("intention", "execution"))   # 3 5
```

编辑距离在大模型方向也常用：语音识别和 OCR 的字错误率（CER/WER）就是编辑距离除以参考文本长度。

### 回文相关

**最长回文子序列（力扣 516）**：区间 DP，`dp[i][j]` 是 `s[i..j]` 中最长回文子序列长度。

```python
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):          # i 倒序，保证 dp[i+1][*] 已算好
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]

print(longest_palindrome_subseq("bbbab"))   # 4
```

**最长回文子串（力扣 5）**：中心扩展法比 DP 更简单，$O(n^2)$ 时间、$O(1)$ 空间。

```python
def longest_palindrome(s):
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return l + 1, r            # 回文区间 [l+1, r)
    best = (0, 1)
    for i in range(len(s)):
        for l, r in (expand(i, i), expand(i, i + 1)):    # 奇数长度和偶数长度
            if r - l > best[1] - best[0]:
                best = (l, r)
    return s[best[0]:best[1]]

print(longest_palindrome("babad"), longest_palindrome("cbbd"))   # bab bb
```

## 6. 区间 DP

状态定义在区间 `[i, j]` 上，按区间长度从小到大计算，转移时枚举分割点。

**戳气球（力扣 312）**：`dp[i][j]` 是戳破开区间 `(i, j)` 中所有气球能得到的最大硬币数。枚举 `(i, j)` 中**最后**一个被戳破的气球 k，此时它的左右邻居正好是 i 和 j。

```python
def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):                 # j - i
        for i in range(n - length):
            j = i + length
            best = 0
            for k in range(i + 1, j):
                best = max(best, dp[i][k] + dp[k][j] + a[i] * a[k] * a[j])
            dp[i][j] = best
    return dp[0][n - 1]

print(max_coins([3, 1, 5, 8]))   # 167
```

"枚举最后一步"而不是第一步，是因为戳破第一个气球后，剩下的两部分并不独立（它们的边界会变）；而最后一个被戳的气球把区间分成了真正独立的两半。

**石子合并**：一排石子，每次合并相邻两堆，代价是两堆之和，求合并成一堆的最小代价。

```python
from itertools import accumulate

def merge_stones(a):
    n = len(a)
    pre = [0] + list(accumulate(a))
    INF = float("inf")
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j)) + pre[j + 1] - pre[i]
    return dp[0][n - 1]

print(merge_stones([1, 3, 5, 2]))   # 22
```

## 7. 状态压缩 DP

状态中包含一个集合，用整数的二进制位表示，适用于 $n \le 20$。

**例：分配任务**。n 个人、n 个任务，`cost[i][j]` 是第 i 个人做第 j 个任务的代价，每人做一个，求最小总代价。`dp[mask]` 表示前 `popcount(mask)` 个人已经分配了 mask 中的任务时的最小代价。

```python
def min_assign_cost(cost):
    n = len(cost)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        i = bin(mask).count("1")          # 下一个要分配的人
        if i == n:
            continue
        for j in range(n):
            if not mask >> j & 1:
                nm = mask | 1 << j
                if dp[mask] + cost[i][j] < dp[nm]:
                    dp[nm] = dp[mask] + cost[i][j]
    return dp[(1 << n) - 1]

print(min_assign_cost([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]))   # 13
```

## 8. 常见的错误

- 状态定义含糊，导致转移时自己也说不清 `dp[i]` 包含哪些情况。写代码前先用一句话写下状态的含义。
- 初始值错误：求最小值时初始化为 `inf`，求方案数时 `dp[0] = 1`，求最大值且可能为负时初始化为 `-inf` 而不是 0。
- 计算顺序错误：区间 DP 按长度从小到大；`dp[i][j]` 依赖 `dp[i+1][*]` 时 i 要倒序。
- 空间压缩后遍历方向弄反（0-1 背包正序就变成了完全背包）。
- 答案不在 `dp[n]`：定义为"以 i 结尾"时，答案是 `max(dp)`。

## 练习

| 题目 | 类型 |
| --- | --- |
| 力扣 746 使用最小花费爬楼梯 | 线性 |
| 力扣 279 完全平方数 | 完全背包 |
| 力扣 1049 最后一块石头的重量 II | 0-1 背包 |
| 力扣 474 一和零 | 二维费用 0-1 背包 |
| 力扣 32 最长有效括号 | 线性，或用栈 |
| 力扣 115 不同的子序列 | 双序列 |
| 力扣 10 正则表达式匹配 | 双序列 |
| 力扣 1000 合并石头的最低成本 | 区间 |
| 力扣 1125 最小的必要团队 | 状态压缩 |
| 力扣 2008 出租车的最大盈利 | 线性 + 二分 |
