---
date: 2026-11-05
description: 回溯的框架与"选或不选""枚举选哪个"两种视角，子集、组合、排列及其去重，剪枝，N 皇后、单词搜索、括号生成、分割回文串，以及记忆化搜索和状态压缩。
tags:
  - 算法
---

# 回溯与搜索

回溯就是带撤销的 DFS：沿着一条路做选择，走到底记录答案，然后撤销最后一步，换一个选择继续。适用于"列出所有方案"类的题目，数据范围一般很小（$n \le 20$ 左右）。

## 1. 框架

```py
def backtrack(状态):
    if 到达终点:
        记录答案（注意复制）
        return
    for 选择 in 当前可做的选择:
        if 不合法: continue
        做选择
        backtrack(新状态)
        撤销选择
```

写回溯时要想清楚三件事：路径（已经做过的选择）、选择列表（当前还能做什么）、结束条件。

## 2. 子集

**子集（力扣 78）**：返回数组所有子集，元素互不相同。

两种视角都能写。

**视角一：每个元素选或不选**。递归到第 i 个元素时，分两支。

```python
def subsets_pick(nums):
    res, path = [], []
    def dfs(i):
        if i == len(nums):
            res.append(path[:])
            return
        dfs(i + 1)                  # 不选 nums[i]
        path.append(nums[i])        # 选 nums[i]
        dfs(i + 1)
        path.pop()
    dfs(0)
    return res

print(subsets_pick([1, 2, 3]))
# [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
```

**视角二：枚举下一个选哪个**。每个递归节点都是一个子集，下一个元素只能从当前位置之后选，保证不重复。

```python
def subsets(nums):
    res, path = [], []
    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return res

print(subsets([1, 2, 3]))
# [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

`res.append(path[:])` 必须复制。如果写 `res.append(path)`，存进去的是同一个列表对象，回溯结束时它是空的，结果会是一堆 `[]`。

$n$ 个元素的子集也可以用二进制枚举：第 $j$ 位为 1 表示选第 $j$ 个元素。

```python
def subsets_bits(nums):
    n = len(nums)
    return [[nums[j] for j in range(n) if mask >> j & 1] for mask in range(1 << n)]

print(len(subsets_bits([1, 2, 3, 4])))   # 16
```

### 有重复元素时去重

**子集 II（力扣 90）**：先排序，让相同的元素相邻。同一层（同一个 for 循环）中，相同的值只选第一个。

```python
def subsets_with_dup(nums):
    nums.sort()
    res, path = [], []
    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:    # 同一层跳过重复值
                continue
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return res

print(subsets_with_dup([1, 2, 2]))   # [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
```

条件是 `i > start` 而不是 `i > 0`：同一层不能重复选同一个值，但下一层可以选和上一层相同的值（比如 `[2, 2]` 中的第二个 2）。

## 3. 组合

**组合总和（力扣 39）**：元素可以重复使用，找所有和为 target 的组合。可以重复使用，所以递归时传 `i` 而不是 `i + 1`。排序后可以剪枝：当前元素已经超过剩余值，后面更大的元素也不用试了。

```python
def combination_sum(candidates, target):
    candidates.sort()
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > remain:
                break                      # 剪枝
            path.append(c)
            dfs(i, remain - c)             # 传 i：可以继续用同一个数
            path.pop()
    dfs(0, target)
    return res

print(combination_sum([2, 3, 6, 7], 7), combination_sum([2, 3, 5], 8))
# [[2, 2, 3], [7]] [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
```

**组合总和 II（力扣 40）**：每个元素只能用一次，数组有重复，结果不能重复。就是把子集 II 的去重和组合总和的剪枝合在一起：

```python
def combination_sum2(candidates, target):
    candidates.sort()
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remain:
                break
            path.append(candidates[i])
            dfs(i + 1, remain - candidates[i])
            path.pop()
    dfs(0, target)
    return res

print(combination_sum2([10, 1, 2, 7, 6, 1, 5], 8))   # [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

**组合（力扣 77）**：从 1～n 中选 k 个。剪枝：剩下的数不够凑满 k 个时停止。

```python
def combine(n, k):
    res, path = [], []
    def dfs(start):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n - (k - len(path)) + 2):    # 至少要留够 k-len(path) 个数
            path.append(i)
            dfs(i + 1)
            path.pop()
    dfs(1)
    return res

print(combine(4, 2))   # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
```

## 4. 排列

**全排列（力扣 46）**：每个位置可以放任何还没用过的元素，用 `used` 数组标记。

```python
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)
    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()
            used[i] = False
    dfs()
    return res

print(permute([1, 2, 3]))
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

**全排列 II（力扣 47）**：有重复元素。排序后，相同的值必须按顺序使用：前一个相同的值还没用时，不能用当前这个。

```python
def permute_unique(nums):
    nums.sort()
    res, path = [], []
    used = [False] * len(nums)
    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False
    dfs()
    return res

print(permute_unique([1, 1, 2]))   # [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
```

`not used[i - 1]` 表示前一个相同的值在这一层已经被撤销了，也就是同一层上它已经被试过，跳过当前值才能避免重复。

只需要结果、不考察手写时，`itertools.permutations` 和 `combinations` 更快：

```python
from itertools import permutations
print(sorted(set(permutations([1, 1, 2]))))   # [(1, 1, 2), (1, 2, 1), (2, 1, 1)]
```

## 5. 经典问题

### 括号生成（力扣 22）

左括号数不超过 n、右括号数不超过左括号数，就一定合法。

```python
def generate_parenthesis(n):
    res = []
    def dfs(s, open_, close):
        if len(s) == 2 * n:
            res.append(s)
            return
        if open_ < n:
            dfs(s + "(", open_ + 1, close)
        if close < open_:
            dfs(s + ")", open_, close + 1)
    dfs("", 0, 0)
    return res

print(generate_parenthesis(3))   # ['((()))', '(()())', '(())()', '()(())', '()()()']
```

这里用字符串拼接产生新对象，不需要撤销。

### N 皇后（力扣 51）

逐行放皇后，用三个集合记录已被占用的列、主对角线（`r - c` 相同）和副对角线（`r + c` 相同）。

```python
def solve_n_queens(n):
    res = []
    cols, diag1, diag2 = set(), set(), set()
    queens = []                       # queens[r] 是第 r 行皇后所在的列
    def dfs(r):
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or r - c in diag1 or r + c in diag2:
                continue
            cols.add(c); diag1.add(r - c); diag2.add(r + c)
            queens.append(c)
            dfs(r + 1)
            queens.pop()
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c)
    dfs(0)
    return res

sols = solve_n_queens(4)
print(len(sols), sols[0])          # 2 ['.Q..', '...Q', 'Q...', '..Q.']
print(len(solve_n_queens(8)))      # 92
```

### 单词搜索（力扣 79）

网格中找一条路径拼出单词，每个格子只能用一次。访问时临时把格子改成特殊字符，回溯时改回来。

```python
def exist(board, word):
    n, m = len(board), len(board[0])
    g = [list(row) for row in board]
    def dfs(x, y, k):
        if g[x][y] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        tmp, g[x][y] = g[x][y], "#"
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and dfs(nx, ny, k + 1):
                g[x][y] = tmp
                return True
        g[x][y] = tmp
        return False
    return any(dfs(i, j, 0) for i in range(n) for j in range(m))

board = ["ABCE", "SFCS", "ADEE"]
print(exist(board, "ABCCED"), exist(board, "SEE"), exist(board, "ABCB"))   # True True False
```

### 分割回文串（力扣 131）

枚举第一段在哪里结束，第一段是回文才继续切剩下的部分。先用 DP 预处理 `is_pal[i][j]`，避免反复判断。

```python
def partition(s):
    n = len(s)
    is_pal = [[True] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            is_pal[i][j] = s[i] == s[j] and is_pal[i + 1][j - 1]
    res, path = [], []
    def dfs(start):
        if start == n:
            res.append(path[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()
    dfs(0)
    return res

print(partition("aab"))   # [['a', 'a', 'b'], ['aa', 'b']]
```

### 电话号码的字母组合（力扣 17）

```python
def letter_combinations(digits):
    if not digits:
        return []
    m = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res = []
    def dfs(i, s):
        if i == len(digits):
            res.append(s)
            return
        for c in m[digits[i]]:
            dfs(i + 1, s + c)
    dfs(0, "")
    return res

print(letter_combinations("23"))   # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

## 6. 剪枝

回溯的复杂度是指数级的，剪枝决定了能不能跑完。常用的几种：

- **可行性剪枝**：当前状态已经不可能得到合法解（剩余和为负、剩余元素不够）。
- **最优性剪枝**：求最优解时，当前代价已经不比已知最优解好。
- **排序**：先试更可能成功（或更容易失败）的分支。
- **对称性**：等价的状态只搜一次。

**例：划分为 k 个相等的子集（力扣 698）**。降序排序后先放大的数，更早失败；如果某个桶和前一个桶当前的和相同，放进去的结果是一样的，跳过。

```python
def can_partition_k(nums, k):
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    nums.sort(reverse=True)
    if nums[0] > target:
        return False
    buckets = [0] * k
    def dfs(i):
        if i == len(nums):
            return True
        for b in range(k):
            if buckets[b] + nums[i] > target:
                continue
            if b > 0 and buckets[b] == buckets[b - 1]:    # 对称性剪枝
                continue
            buckets[b] += nums[i]
            if dfs(i + 1):
                return True
            buckets[b] -= nums[i]
        return False
    return dfs(0)

print(can_partition_k([4, 3, 2, 3, 5, 2, 1], 4), can_partition_k([1, 2, 3, 4], 3))   # True False
```

## 7. 记忆化搜索

如果搜索过程中同一个状态会被反复访问，并且状态的结果只取决于状态本身（与怎么到达它无关），就可以把结果缓存起来。这时回溯就变成了动态规划。

**单词拆分（力扣 139）**：判断字符串能否拆成字典中的单词。状态是"从位置 i 开始的后缀能否拆分"。

```python
from functools import lru_cache

def word_break(s, words):
    wordset = set(words)
    maxlen = max(map(len, words))
    @lru_cache(maxsize=None)
    def ok(i):
        if i == len(s):
            return True
        return any(s[i:j] in wordset and ok(j) for j in range(i + 1, min(len(s), i + maxlen) + 1))
    return ok(0)

print(word_break("leetcode", ["leet", "code"]), word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]))   # True False
print(word_break("a" * 200 + "b", ["a", "aa", "aaa"]))    # False，不加缓存会超时
```

### 状态压缩

状态里包含"哪些元素已经用过"，而 $n \le 20$ 时，可以用一个整数的二进制位表示这个集合，作为缓存的 key。

**例：最短哈密顿路径（旅行商问题的简化版）**。从 0 号点出发，访问所有点恰好一次的最短路径长度。

```python
from functools import lru_cache

def shortest_hamilton(dist):
    n = len(dist)
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def f(mask, u):
        """已访问集合为 mask、当前在 u，访问完剩余点的最短距离"""
        if mask == full:
            return 0
        best = float("inf")
        for v in range(n):
            if not mask >> v & 1:
                best = min(best, dist[u][v] + f(mask | 1 << v, v))
        return best
    return f(1, 0)

dist = [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]]
print(shortest_hamilton(dist))    # 16，路径 0 -> 1 -> 2 -> 3
```

状态数是 $2^n \cdot n$，每个状态转移 $O(n)$，总复杂度 $O(2^n n^2)$。暴力枚举所有排列是 $O(n!)$，$n = 15$ 时前者约 $7 \times 10^6$，后者约 $1.3 \times 10^{12}$。

位运算的常用写法：

| 操作 | 写法 |
| --- | --- |
| 判断第 i 位是否为 1 | `mask >> i & 1` |
| 把第 i 位置 1 | `mask \| (1 << i)` |
| 把第 i 位置 0 | `mask & ~(1 << i)` |
| 集合中元素个数 | `mask.bit_count()`（3.10+）或 `bin(mask).count("1")` |
| 最低位的 1 | `mask & -mask` |
| 枚举 mask 的所有子集 | `sub = mask; while sub: ...; sub = (sub - 1) & mask` |

## 练习

| 题目 | 要点 |
| --- | --- |
| 力扣 216 组合总和 III | 组合 + 剪枝 |
| 力扣 93 复原 IP 地址 | 分割，判断每段是否合法 |
| 力扣 37 解数独 | 回溯，用集合记录行列宫 |
| 力扣 301 删除无效的括号 | 先算出最少删除数，再回溯 |
| 力扣 473 火柴拼正方形 | 与 698 相同 |
| 力扣 526 优美的排列 | 回溯或状压 DP |
| 力扣 491 递增子序列 | 无法排序，每层用集合去重 |
