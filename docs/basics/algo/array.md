---
date: 2026-11-05
description: 哈希表计数、相向与同向双指针、滑动窗口（可变与固定长度）、一维与二维前缀和、前缀和加哈希表、差分数组、原地修改数组的技巧，配例题。
tags:
  - 算法
---

# 数组：双指针、滑动窗口、前缀和

数组题是笔试里出现最多的一类。主要思路是把暴力的 $O(n^2)$ 枚举降到 $O(n)$ 或 $O(n \log n)$，常用的手段就是本章这几种。

## 1. 哈希表

用空间换时间：遍历时把"已经见过的信息"存进 dict 或 set，后面的元素直接查。

**例：最长连续序列（力扣 128）**。给一个未排序的整数数组，求数值连续的最长序列长度，要求 $O(n)$。

```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:          # 只从序列的起点开始数，保证每个数只被数一次
            continue
        y = x
        while y + 1 in s:
            y += 1
        best = max(best, y - x + 1)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))   # 4
```

**例：字母异位词分组（力扣 49）**。把字母相同、顺序不同的单词分到一组。

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)    # 排序后的字符串作为 key
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

## 2. 相向双指针

两个指针分别从两端向中间移动，适用于**有序数组**或者需要从两侧收缩的问题。

**例：两数之和 II（力扣 167）**。有序数组中找两个数，和为 target。

```python
def two_sum_sorted(a, target):
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target:
            return i, j
        if s < target:
            i += 1      # 和太小，左指针右移使和变大
        else:
            j -= 1
    return -1, -1

print(two_sum_sorted([2, 7, 11, 15], 9))   # (0, 1)
```

**例：三数之和（力扣 15）**。找出所有和为 0 的不重复三元组。排序后固定第一个数，剩下的用相向双指针，难点在去重。

```python
def three_sum(nums):
    nums.sort()
    n, res = len(nums), []
    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:      # 第一个数去重
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:   # 第二个数去重
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
    return res

print(three_sum([-1, 0, 1, 2, -1, -4]))   # [[-1, -1, 2], [-1, 0, 1]]
```

**例：盛最多水的容器（力扣 11）**。

```python
def max_area(h):
    i, j, best = 0, len(h) - 1, 0
    while i < j:
        best = max(best, (j - i) * min(h[i], h[j]))
        if h[i] < h[j]:      # 移动较矮的一边，才有可能得到更大的面积
            i += 1
        else:
            j -= 1
    return best

print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))   # 49
```

为什么移动较矮的一边是对的：设 `h[i] < h[j]`，以 `i` 为左端点、`j` 左边任何位置为右端点的容器，宽度更小，高度不超过 `h[i]`，面积不可能超过当前值。所以可以放心地排除 `i`。双指针题都要能说清楚"为什么可以排除"，面试官常会追问。

**例：接雨水（力扣 42）**。每个位置能接的水 = $\min(\text{左边最高}, \text{右边最高}) - \text{自身高度}$。

```python
def trap(h):
    i, j = 0, len(h) - 1
    lmax = rmax = water = 0
    while i < j:
        lmax = max(lmax, h[i])
        rmax = max(rmax, h[j])
        if lmax < rmax:          # 左边的瓶颈更低，位置 i 的水量已经确定
            water += lmax - h[i]
            i += 1
        else:
            water += rmax - h[j]
            j -= 1
    return water

print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
```

## 3. 同向双指针：原地修改数组

一个读指针遍历数组，一个写指针记录下一个要写入的位置。

**例：移动零（力扣 283）**。把所有 0 移到末尾，保持非零元素的相对顺序。

```python
def move_zeroes(a):
    w = 0
    for r in range(len(a)):
        if a[r] != 0:
            a[w], a[r] = a[r], a[w]
            w += 1
    return a

print(move_zeroes([0, 1, 0, 3, 12]))   # [1, 3, 12, 0, 0]
```

**例：删除有序数组中的重复项（力扣 26）**，返回新长度。

```python
def remove_duplicates(a):
    if not a:
        return 0
    w = 1
    for r in range(1, len(a)):
        if a[r] != a[w - 1]:
            a[w] = a[r]
            w += 1
    return w

a = [0, 0, 1, 1, 1, 2, 2, 3]
k = remove_duplicates(a)
print(k, a[:k])    # 4 [0, 1, 2, 3]
```

## 4. 滑动窗口

维护一个区间 `[left, right]`，右端点逐个扩展，不满足条件时收缩左端点。适用于"求满足某条件的最长/最短**连续**子数组（子串）"，前提是条件具有单调性：窗口扩大只会让它更难（或更容易）满足。

### 可变长度窗口模板

```py
left = 0
for right, x in enumerate(a):
    把 x 加入窗口
    while 窗口不合法:
        把 a[left] 移出窗口
        left += 1
    用 right - left + 1 更新答案
```

**例：无重复字符的最长子串（力扣 3）**。

```python
def length_of_longest_substring(s):
    cnt = {}
    left = best = 0
    for right, c in enumerate(s):
        cnt[c] = cnt.get(c, 0) + 1
        while cnt[c] > 1:              # 出现重复，收缩左端
            cnt[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best

print(length_of_longest_substring("abcabcbb"), length_of_longest_substring("pwwkew"))   # 3 3
```

**例：长度最小的子数组（力扣 209）**。正整数数组中，和 ≥ target 的最短连续子数组长度。这里是"满足条件时收缩"，在 `while` 里更新答案。

```python
def min_subarray_len(target, a):
    left = s = 0
    best = float("inf")
    for right, x in enumerate(a):
        s += x
        while s >= target:
            best = min(best, right - left + 1)
            s -= a[left]
            left += 1
    return 0 if best == float("inf") else best

print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]))   # 2
```

数组中有负数时，"窗口扩大，和一定变大"不再成立，滑动窗口失效，要改用前缀和。

**例：最小覆盖子串（力扣 76）**。`s` 中包含 `t` 所有字符（含重复）的最短子串。

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)               # 还缺多少个字符
    left = 0
    best = (float("inf"), 0, 0)
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1               # need 可以变成负数，表示窗口里多出来的
        while missing == 0:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:  # 移出的是必需字符
                missing += 1
            left += 1
    return s[best[1]:best[2]]

print(min_window("ADOBECODEBANC", "ABC"))   # BANC
```

### 固定长度窗口

**例：找到字符串中所有字母异位词（力扣 438）**。

```python
def find_anagrams(s, p):
    k, res = len(p), []
    need = [0] * 26
    win = [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    for i, c in enumerate(s):
        win[ord(c) - 97] += 1
        if i >= k:
            win[ord(s[i - k]) - 97] -= 1     # 移出窗口左端
        if i >= k - 1 and win == need:
            res.append(i - k + 1)
    return res

print(find_anagrams("cbaebabacd", "abc"))   # [0, 6]
```

字母只有 26 个时，用长度 26 的数组计数比 dict 快，比较两个 list 是 $O(26)$。

## 5. 前缀和

$\text{pre}[i] = a_0 + a_1 + \dots + a_{i-1}$，`pre[0] = 0`。区间 $[l, r]$ 的和就是 `pre[r + 1] - pre[l]`，任意区间求和变成 $O(1)$。

```python
from itertools import accumulate

a = [3, 1, 4, 1, 5]
pre = [0] + list(accumulate(a))    # [0, 3, 4, 8, 9, 14]
l, r = 1, 3
print(pre[r + 1] - pre[l], sum(a[l:r + 1]))   # 6 6
```

前缀数组多开一位、让 `pre[0] = 0`，可以避免 $l = 0$ 时的特判。

### 前缀和加哈希表

**例：和为 K 的子数组（力扣 560）**。统计和为 k 的连续子数组个数，数组中有负数。

子数组 $[j, i]$ 的和为 k，等价于 $\text{pre}[i+1] - \text{pre}[j] = k$。遍历时记录每个前缀和出现的次数，对当前前缀和 `s`，查 `s - k` 出现过几次。

```python
from collections import defaultdict

def subarray_sum(nums, k):
    cnt = defaultdict(int)
    cnt[0] = 1                  # 空前缀，对应从下标 0 开始的子数组
    s = res = 0
    for x in nums:
        s += x
        res += cnt[s - k]
        cnt[s] += 1
    return res

print(subarray_sum([1, 1, 1], 2), subarray_sum([1, -1, 0], 0))   # 2 3
```

同样的思路还能解决：和能被 k 整除的子数组（记录前缀和模 k 的余数），0 和 1 个数相同的最长子数组（把 0 当作 -1，求和为 0 的最长子数组，记录每个前缀和**第一次**出现的位置）。

```python
def find_max_length(nums):
    first = {0: -1}
    s = best = 0
    for i, x in enumerate(nums):
        s += 1 if x == 1 else -1
        if s in first:
            best = max(best, i - first[s])
        else:
            first[s] = i
    return best

print(find_max_length([0, 1, 1, 0, 1, 1, 0]))   # 4
```

### 二维前缀和

$P[i][j]$ 表示左上角 $(0,0)$ 到右下角 $(i-1, j-1)$ 的矩形和：

```python
def build_2d(mat):
    n, m = len(mat), len(mat[0])
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + mat[i][j]
    return P

def rect_sum(P, r1, c1, r2, c2):       # 闭区间 [r1, r2] x [c1, c2]
    return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]

mat = [[3, 0, 1, 4],
       [5, 6, 3, 2],
       [1, 2, 0, 1]]
P = build_2d(mat)
print(rect_sum(P, 1, 1, 2, 2), rect_sum(P, 0, 0, 2, 3))   # 11 28
```

## 6. 差分

差分是前缀和的逆运算：$d[i] = a[i] - a[i-1]$。对原数组区间 $[l, r]$ 全部加上 $v$，只需要 `d[l] += v`、`d[r + 1] -= v` 两步，最后对 `d` 求前缀和还原。适用于"多次区间修改、最后一次查询"。

**例：航班预订统计（力扣 1109）**。`bookings[i] = [first, last, seats]` 表示第 first 到 last 个航班（从 1 编号）各预订 seats 个座位，求每个航班的总座位数。

```python
from itertools import accumulate

def corp_flight_bookings(bookings, n):
    d = [0] * (n + 1)
    for first, last, seats in bookings:
        d[first - 1] += seats
        d[last] -= seats
    return list(accumulate(d[:n]))

print(corp_flight_bookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5))   # [10, 55, 45, 25, 25]
```

**例：拼车（力扣 1094）**。判断某一时刻车上人数是否超过容量，做法一样：在上车点加、下车点减，求前缀和看最大值。

```python
def car_pooling(trips, capacity):
    d = [0] * 1001
    for num, start, end in trips:
        d[start] += num
        d[end] -= num           # 在 end 下车，end 时刻已经不在车上
    cur = 0
    for x in d:
        cur += x
        if cur > capacity:
            return False
    return True

print(car_pooling([[2, 1, 5], [3, 3, 7]], 4), car_pooling([[2, 1, 5], [3, 3, 7]], 5))   # False True
```

## 7. 其他常见技巧

**原地标记**：数组元素范围是 $[1, n]$ 时，可以用"把 `a[x-1]` 变成负数"来标记 `x` 出现过，做到 $O(1)$ 额外空间。

```python
def find_disappeared(nums):
    for x in nums:
        i = abs(x) - 1
        nums[i] = -abs(nums[i])
    return [i + 1 for i, x in enumerate(nums) if x > 0]

print(find_disappeared([4, 3, 2, 7, 8, 2, 3, 1]))   # [5, 6]
```

**例：缺失的第一个正数（力扣 41）**。把每个 $x \in [1, n]$ 交换到下标 $x-1$ 的位置，再找第一个不在位的。

```python
def first_missing_positive(a):
    n = len(a)
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]
    for i in range(n):
        if a[i] != i + 1:
            return i + 1
    return n + 1

print(first_missing_positive([3, 4, -1, 1]), first_missing_positive([7, 8, 9]))   # 2 1
```

交换那一行不能写成 `a[i], a[a[i] - 1] = a[a[i] - 1], a[i]`：Python 先算出右边两个值，再**从左到右**赋值，给 `a[i]` 赋值后，左边第二项里的 `a[i] - 1` 已经变了。先把下标存进 `j` 就不会出错。

**矩阵旋转（力扣 48）**：顺时针旋转 90° = 先转置，再把每一行反转。

```python
def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]
    for row in m:
        row.reverse()
    return m

print(rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))   # [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```

**最大子数组和（力扣 53）**：Kadane 算法，以当前元素结尾的最大和，要么接在前面，要么从自己重新开始。

```python
def max_subarray(a):
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # 6
```

## 练习

| 题目 | 方法 |
| --- | --- |
| 力扣 1 两数之和 | 哈希表 |
| 力扣 238 除自身以外数组的乘积 | 前缀积与后缀积 |
| 力扣 189 轮转数组 | 三次反转 |
| 力扣 56 合并区间 | 按左端点排序 |
| 力扣 904 水果成篮 | 滑动窗口 |
| 力扣 1004 最大连续 1 的个数 III | 滑动窗口 |
| 力扣 974 和可被 K 整除的子数组 | 前缀和取模加哈希表 |
| 力扣 304 二维区域和检索 | 二维前缀和 |
| 力扣 54 螺旋矩阵 | 模拟，维护四条边界 |
