---
date: 2026-11-05
description: 用"找第一个满足条件的位置"统一二分查找的写法：查找边界、旋转数组、峰值、在答案上二分（最小化最大值）、浮点二分、二维矩阵，以及边界条件的检查方法。
tags:
  - 算法
---

# 二分查找

二分的思想很简单，难点全在边界：`left < right` 还是 `left <= right`，`mid + 1` 还是 `mid`，循环结束时返回哪个变量。记多套模板容易混，这里只用一种写法。

## 1. 统一的写法：找第一个满足条件的位置

设有一个判定函数 `check(i)`，它在下标范围上是**单调**的：前面一段为 `False`，后面一段为 `True`。

```text
i:        0     1     2     3     4     5
check:  False False False True  True  True
                          ↑ 要找的位置
```

二分就是找第一个 `True` 的位置：

```python
def first_true(lo, hi, check):
    """在 [lo, hi) 中找第一个使 check 为 True 的位置；都不满足时返回 hi"""
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid          # mid 满足，答案在 [lo, mid]
        else:
            lo = mid + 1      # mid 不满足，答案在 [mid+1, hi)
    return lo

a = [1, 3, 3, 5, 8]
print(first_true(0, len(a), lambda i: a[i] >= 3))   # 1
print(first_true(0, len(a), lambda i: a[i] > 3))    # 3
print(first_true(0, len(a), lambda i: a[i] >= 9))   # 5，不存在时返回 len(a)
```

为什么不会死循环：`lo < hi` 时 `mid = (lo + hi) // 2` 满足 `lo <= mid < hi`，所以无论走哪个分支，区间长度都严格减小。循环结束时 `lo == hi`，就是答案。

各种"查找"都能转化成这个形式：

| 要找的 | check(i) | 结果 |
| --- | --- | --- |
| 第一个 `>= x` 的位置 | `a[i] >= x` | 等价于 `bisect_left` |
| 第一个 `> x` 的位置 | `a[i] > x` | 等价于 `bisect_right` |
| 最后一个 `< x` 的位置 | `a[i] >= x` | 结果减 1 |
| 最后一个 `<= x` 的位置 | `a[i] > x` | 结果减 1 |
| `x` 是否存在 | `a[i] >= x` | 结果 `p < n and a[p] == x` |

**例：在排序数组中查找元素的第一个和最后一个位置（力扣 34）**。

```python
def search_range(a, x):
    n = len(a)
    l = first_true(0, n, lambda i: a[i] >= x)
    if l == n or a[l] != x:
        return [-1, -1]
    r = first_true(0, n, lambda i: a[i] > x) - 1
    return [l, r]

print(search_range([5, 7, 7, 8, 8, 10], 8), search_range([5, 7, 7, 8, 8, 10], 6))   # [3, 4] [-1, -1]
```

笔试时不想传函数，可以把 `check` 直接写进循环，结构不变：

```python
def lower_bound(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] >= x:
            hi = mid
        else:
            lo = mid + 1
    return lo

from bisect import bisect_left
import random
random.seed(1)
for _ in range(1000):
    a = sorted(random.randint(0, 20) for _ in range(random.randint(0, 10)))
    x = random.randint(-1, 21)
    assert lower_bound(a, x) == bisect_left(a, x)
print("ok")
```

## 2. 序列本身不单调的二分

二分需要的不是数组有序，而是**能根据 mid 判断答案在哪一侧**。

**例：搜索旋转排序数组（力扣 33）**。`[4,5,6,7,0,1,2]` 是有序数组旋转后的结果，元素互不相同，查找 target 的下标。

`mid` 把数组分成两半，其中至少有一半是有序的。判断 target 是否落在有序的那一半里，就知道该往哪边走。

```python
def search_rotated(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[lo] <= a[mid]:                    # 左半段 [lo, mid] 有序
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                  # 右半段 [mid, hi] 有序
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0), search_rotated([4, 5, 6, 7, 0, 1, 2], 3))   # 4 -1
```

这里查找的是"某个确定的值"，找到就返回，所以用闭区间 `[lo, hi]` 加 `lo <= hi` 更自然。

**例：寻找旋转排序数组中的最小值（力扣 153）**。和最后一个元素比较：`a[i] <= a[-1]` 对于最小值及其右侧的元素成立，左侧不成立，正好是单调的判定函数。

```python
def find_min(a):
    return a[first_true(0, len(a), lambda i: a[i] <= a[-1])]

print(find_min([3, 4, 5, 1, 2]), find_min([11, 13, 15, 17]))   # 1 11
```

**例：寻找峰值（力扣 162）**。相邻元素不相等，找任意一个比左右邻居都大的元素。判定函数取 `a[i] > a[i + 1]`：如果 `a[mid] > a[mid+1]`，左侧（含 mid）一定有峰值。

```python
def find_peak(a):
    return first_true(0, len(a) - 1, lambda i: a[i] > a[i + 1])

print(find_peak([1, 2, 3, 1]), find_peak([1, 2, 1, 3, 5, 6, 4]))   # 2 5
```

`hi` 取 `len(a) - 1`：所有位置都不满足时返回最后一个下标，此时数组单调递增，最后一个元素就是峰值。

## 3. 在答案上二分

题目问"满足条件的最小（最大）值是多少"，而且"给定一个候选答案，能高效判断它是否可行"、可行性随答案单调变化时，可以对答案二分。这类题的标志是"最大值最小""最小值最大""至少需要多少"。

**例：爱吃香蕉的珂珂（力扣 875）**。`piles[i]` 堆香蕉，每小时吃 `k` 根（一堆不足 k 根时吃完这一堆就停），要在 `h` 小时内吃完，求最小的 `k`。

速度越大，用时越少，`check(k) = 用时 <= h` 关于 k 单调。

```python
def min_eating_speed(piles, h):
    def hours(k):
        return sum((p + k - 1) // k for p in piles)     # 每堆向上取整
    return first_true(1, max(piles) + 1, lambda k: hours(k) <= h)

print(min_eating_speed([3, 6, 7, 11], 8), min_eating_speed([30, 11, 23, 4, 20], 6))   # 4 23
```

复杂度是 $O(n \log M)$，$M$ 是答案的范围。

**例：分割数组的最大值（力扣 410）**。把数组分成 `k` 个连续的非空子数组，使各子数组和的最大值最小。

给定上限 `limit`，贪心地往当前段里加元素，超过 `limit` 就开新的一段，看需要几段。`limit` 越大需要的段数越少。

```python
def split_array(nums, k):
    def pieces(limit):
        cnt, s = 1, 0
        for x in nums:
            if s + x > limit:
                cnt += 1
                s = 0
            s += x
        return cnt
    return first_true(max(nums), sum(nums) + 1, lambda lim: pieces(lim) <= k)

print(split_array([7, 2, 5, 10, 8], 2))   # 18
```

下界取 `max(nums)`：上限比最大元素还小时，单个元素都放不下。

**例：最小值最大化**。在 `positions` 中选 `m` 个位置放球，使任意两球之间的最小距离尽可能大（力扣 1552）。距离越大越难满足，判定函数 `能放下 m 个` 是"前面 True、后面 False"，求最后一个 True：把条件取反找第一个 True，再减 1。

```python
def max_distance(positions, m):
    positions.sort()
    def can(d):
        cnt, last = 1, positions[0]
        for p in positions[1:]:
            if p - last >= d:
                cnt += 1
                last = p
        return cnt >= m
    return first_true(1, positions[-1] - positions[0] + 2, lambda d: not can(d)) - 1

print(max_distance([1, 2, 3, 4, 7], 3), max_distance([5, 4, 3, 2, 1, 1000000000], 2))   # 3 999999999
```

## 4. 浮点数二分

答案是实数时，不按 `lo < hi` 判断结束，而是固定迭代次数（每次区间减半，迭代 100 次精度远超 double 的有效位数）：

```python
def cube_root(x):
    lo, hi = min(-1.0, x), max(1.0, x)
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid ** 3 >= x:
            hi = mid
        else:
            lo = mid
    return lo

print(f"{cube_root(27):.6f} {cube_root(-0.001):.6f} {cube_root(2):.6f}")   # 3.000000 -0.100000 1.259921
```

## 5. 整数平方根

**例：x 的平方根（力扣 69）**，返回 $\lfloor \sqrt x \rfloor$。等价于找第一个满足 $k^2 > x$ 的 $k$，再减 1。

```python
def my_sqrt(x):
    return first_true(0, x + 2, lambda k: k * k > x) - 1

import math
assert all(my_sqrt(x) == math.isqrt(x) for x in range(2000))
print(my_sqrt(8), my_sqrt(2**62))    # 2 2147483648
```

## 6. 二维矩阵

**搜索二维矩阵（力扣 74）**：每行有序，且每行第一个数大于上一行最后一个数。把矩阵看作长度 $nm$ 的一维有序数组，下标 `i` 对应 `(i // m, i % m)`。

```python
def search_matrix(mat, target):
    n, m = len(mat), len(mat[0])
    p = first_true(0, n * m, lambda i: mat[i // m][i % m] >= target)
    return p < n * m and mat[p // m][p % m] == target

print(search_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3))   # True
```

**搜索二维矩阵 II（力扣 240）**：每行从左到右递增、每列从上到下递增，但行与行之间没有关系。这时不用二分，而是从右上角出发：比 target 大就左移一列，比 target 小就下移一行，$O(n+m)$。

```python
def search_matrix2(mat, target):
    i, j = 0, len(mat[0]) - 1
    while i < len(mat) and j >= 0:
        if mat[i][j] == target:
            return True
        if mat[i][j] > target:
            j -= 1
        else:
            i += 1
    return False

M = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
print(search_matrix2(M, 5), search_matrix2(M, 15))   # True False
```

## 7. 检查边界的方法

写完二分，用这几种输入过一遍：

- 空数组、只有一个元素。
- 答案在第一个位置、在最后一个位置、不存在。
- 所有元素都相同。
- 只有两个元素（最容易暴露死循环）。

再用暴力解法对拍，就能放心了。

## 练习

| 题目 | 要点 |
| --- | --- |
| 力扣 35 搜索插入位置 | 第一个 `>= target` |
| 力扣 278 第一个错误的版本 | 标准的第一个 True |
| 力扣 81 搜索旋转排序数组 II | 有重复元素，`a[lo] == a[mid]` 时只能 `lo += 1` |
| 力扣 4 寻找两个正序数组的中位数 | 在较短数组的切分位置上二分 |
| 力扣 1011 在 D 天内送达包裹的能力 | 二分答案，与 410 相同 |
| 力扣 378 有序矩阵中第 K 小的元素 | 在值域上二分，计数用 240 的走法 |
| 力扣 300 最长递增子序列 | 贪心加二分，见 [动态规划](dp.md) |
