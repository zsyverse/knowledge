---
date: 2026-11-05
description: 栈（括号匹配、最小栈、表达式求值）、单调栈（下一个更大元素、柱状图最大矩形、接雨水）、单调队列（滑动窗口最大值）、堆（Top K、第 K 大、数据流中位数、多路归并）。
tags:
  - 算法
---

# 栈、队列与堆

Python 里栈直接用 list（`append` / `pop`），队列用 `collections.deque`（`append` / `popleft`），堆用 `heapq`。

## 1. 栈

### 有效的括号（力扣 20）

```python
def is_valid(s):
    pair = {")": "(", "]": "[", "}": "{"}
    st = []
    for c in s:
        if c in pair:
            if not st or st[-1] != pair[c]:
                return False
            st.pop()
        else:
            st.append(c)
    return not st            # 最后栈必须为空

print(is_valid("()[]{}"), is_valid("([)]"), is_valid("(("))   # True False False
```

### 最小栈（力扣 155）

`getMin` 要求 $O(1)$。每次入栈时同时记录"到目前为止的最小值"。

```python
class MinStack:
    def __init__(self):
        self.st = []                   # 存 (值, 当前最小值)

    def push(self, x):
        cur_min = min(x, self.st[-1][1]) if self.st else x
        self.st.append((x, cur_min))

    def pop(self):
        self.st.pop()

    def top(self):
        return self.st[-1][0]

    def getMin(self):
        return self.st[-1][1]

ms = MinStack()
for x in [-2, 0, -3]:
    ms.push(x)
print(ms.getMin(), end=" "); ms.pop(); print(ms.top(), ms.getMin())   # -3 0 -2
```

### 字符串解码（力扣 394）

`3[a2[c]]` 解码为 `accaccacc`。遇到 `[` 把当前的字符串和倍数压栈，遇到 `]` 弹出并拼接。

```python
def decode_string(s):
    st = []
    cur, num = "", 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)        # 倍数可能有多位
        elif c == "[":
            st.append((cur, num))
            cur, num = "", 0
        elif c == "]":
            prev, k = st.pop()
            cur = prev + cur * k
        else:
            cur += c
    return cur

print(decode_string("3[a2[c]]"), decode_string("2[abc]3[cd]ef"))   # accaccacc abcabccdcdcdef
```

### 表达式求值

**基本计算器 II（力扣 227）**：只含非负整数和 `+ - * /`，没有括号。乘除优先：遇到加减把数压栈（减号压相反数），遇到乘除直接和栈顶计算，最后对栈求和。

```python
def calculate(s):
    st = []
    num, op = 0, "+"
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if (not c.isdigit() and c != " ") or i == len(s) - 1:
            if op == "+":
                st.append(num)
            elif op == "-":
                st.append(-num)
            elif op == "*":
                st.append(st.pop() * num)
            else:
                st.append(int(st.pop() / num))    # 向零取整，不能用 //
            op, num = c, 0
    return sum(st)

print(calculate("3+2*2"), calculate(" 14-3/2 "), calculate("2-7/2"))   # 7 13 -1
```

题目要求整数除法向零截断，`-7 // 2` 在 Python 里是 `-4`（向下取整），所以用 `int(a / b)`。

带括号的完整版本，用两个栈（数字栈和运算符栈），遇到运算符时把栈中优先级不低于它的运算先算掉：

```python
def evaluate(expr):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    nums, ops = [], []

    def apply():
        b, a = nums.pop(), nums.pop()
        op = ops.pop()
        if op == "+": nums.append(a + b)
        elif op == "-": nums.append(a - b)
        elif op == "*": nums.append(a * b)
        else: nums.append(int(a / b))

    i, n = 0, len(expr)
    prev_is_operand = False
    while i < n:
        c = expr[i]
        if c == " ":
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            nums.append(int(expr[i:j]))
            i = j
            prev_is_operand = True
            continue
        if c == "(":
            ops.append(c)
            prev_is_operand = False
        elif c == ")":
            while ops[-1] != "(":
                apply()
            ops.pop()
            prev_is_operand = True
        else:
            if c == "-" and not prev_is_operand:   # 开头或左括号后的负号：前面补 0
                nums.append(0)
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[c]:
                apply()
            ops.append(c)
            prev_is_operand = False
        i += 1
    while ops:
        apply()
    return nums[-1]

for e in ["1 + 1", "2*(3+4)-5", "(1+(4+5+2)-3)+(6+8)", "-(2+3)*2", "10/(1-3)"]:
    print(e, "=", evaluate(e))
# 1 + 1 = 2
# 2*(3+4)-5 = 9
# (1+(4+5+2)-3)+(6+8) = 23
# -(2+3)*2 = -10
# 10/(1-3) = -5
```

补 0 的处理只适用于出现在表达式开头或左括号之后的负号（力扣 224 的数据就是这样）。像 `2*-3` 这样紧跟在运算符后面的负号，需要把它当作优先级最高的一元运算符单独处理。

## 2. 单调栈

栈中元素保持单调。新元素入栈前，把破坏单调性的元素弹出，被弹出的元素就找到了"右边第一个比它大（或小）的元素"。每个元素进出栈各一次，总复杂度 $O(n)$。

**每日温度（力扣 739）**：对每一天，求还要等几天才有更高的温度。

```python
def daily_temperatures(t):
    ans = [0] * len(t)
    st = []                          # 存下标，对应的温度单调递减
    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop()
            ans[j] = i - j           # i 是 j 右边第一个更高的
        st.append(i)
    return ans

print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))   # [1, 1, 4, 2, 1, 1, 0, 0]
```

| 要找 | 栈内单调性 | 弹出条件 |
| --- | --- | --- |
| 右边第一个更大 | 递减 | `a[top] < x` |
| 右边第一个更小 | 递增 | `a[top] > x` |
| 左边第一个更大 | 递减 | `a[top] <= x`，弹完后栈顶就是答案 |
| 左边第一个更小 | 递增 | `a[top] >= x`，弹完后栈顶就是答案 |

**下一个更大元素 II（力扣 503）**：循环数组。把数组遍历两遍，下标取模。

```python
def next_greater_circular(a):
    n = len(a)
    ans = [-1] * n
    st = []
    for i in range(2 * n):
        x = a[i % n]
        while st and a[st[-1]] < x:
            ans[st.pop()] = x
        if i < n:
            st.append(i)
    return ans

print(next_greater_circular([1, 2, 1]), next_greater_circular([5, 4, 3, 2, 1]))
# [2, -1, 2] [-1, 5, 5, 5, 5]
```

**柱状图中最大的矩形（力扣 84）**：以每根柱子为高，向左右扩展到第一根更矮的柱子为止。用递增栈，弹出时就确定了该柱子的左右边界。两端补上高度为 0 的哨兵，省去边界判断。

```python
def largest_rectangle(heights):
    h = [0] + heights + [0]
    st = []
    best = 0
    for i, x in enumerate(h):
        while st and h[st[-1]] > x:
            top = st.pop()
            left = st[-1]                # 弹出后的栈顶是左边第一个更矮的
            best = max(best, h[top] * (i - left - 1))
        st.append(i)
    return best

print(largest_rectangle([2, 1, 5, 6, 2, 3]), largest_rectangle([2, 4]))   # 10 4
```

**最大矩形（力扣 85）**：01 矩阵中只含 1 的最大矩形。逐行累计每列连续 1 的高度，每一行都是一次柱状图问题。

```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    heights = [0] * len(matrix[0])
    best = 0
    for row in matrix:
        for j, c in enumerate(row):
            heights[j] = heights[j] + 1 if c == "1" else 0
        best = max(best, largest_rectangle(heights))
    return best

print(maximal_rectangle(["10100", "10111", "11111", "10010"]))   # 6
```

**接雨水的单调栈解法**：遇到比栈顶高的柱子时，栈顶是"坑底"，新的栈顶是左边界，当前柱子是右边界，按层计算水量。

```python
def trap_stack(h):
    st, water = [], 0
    for i, x in enumerate(h):
        while st and h[st[-1]] < x:
            bottom = st.pop()
            if not st:
                break
            left = st[-1]
            water += (min(h[left], x) - h[bottom]) * (i - left - 1)
        st.append(i)
    return water

print(trap_stack([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))   # 6
```

## 3. 单调队列

**滑动窗口最大值（力扣 239）**：用双端队列存下标，对应的值从队首到队尾单调递减，队首就是窗口最大值。新元素从队尾进入前，弹出所有比它小的（它们不可能再成为最大值）；队首下标离开窗口时从队首弹出。

```python
from collections import deque

def max_sliding_window(a, k):
    q = deque()
    res = []
    for i, x in enumerate(a):
        while q and a[q[-1]] <= x:
            q.pop()
        q.append(i)
        if q[0] <= i - k:            # 队首已经不在窗口 [i-k+1, i] 内
            q.popleft()
        if i >= k - 1:
            res.append(a[q[0]])
    return res

print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))   # [3, 3, 5, 5, 6, 7]
```

单调队列也常用来优化 DP：形如 $f[i] = \max_{i-k \le j < i} f[j] + c_i$ 的转移，用单调队列维护窗口内 $f[j]$ 的最大值，从 $O(nk)$ 降到 $O(n)$。

### 用栈实现队列（力扣 232）

```python
class MyQueue:
    def __init__(self):
        self.inp, self.out = [], []
    def push(self, x):
        self.inp.append(x)
    def _move(self):
        if not self.out:                  # out 为空时才把 inp 倒过去，保证顺序
            while self.inp:
                self.out.append(self.inp.pop())
    def pop(self):
        self._move()
        return self.out.pop()
    def peek(self):
        self._move()
        return self.out[-1]
    def empty(self):
        return not self.inp and not self.out

q = MyQueue()
q.push(1); q.push(2)
print(q.peek(), q.pop(), q.empty())   # 1 1 False
```

每个元素最多被倒一次，均摊 $O(1)$。

## 4. 堆

### 第 K 大的元素（力扣 215）

维护一个大小为 k 的小根堆，堆顶就是第 k 大。复杂度 $O(n \log k)$。

```python
import heapq

def find_kth_largest(nums, k):
    h = nums[:k]
    heapq.heapify(h)
    for x in nums[k:]:
        if x > h[0]:
            heapq.heapreplace(h, x)      # 弹出堆顶并压入 x，比 pop 再 push 快
    return h[0]

print(find_kth_largest([3, 2, 1, 5, 6, 4], 2), find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))   # 5 4
```

面试时还可能要求用快速选择做到平均 $O(n)$：

```python
import random

def quick_select(nums, k):
    """返回第 k 大（k 从 1 开始）"""
    target = len(nums) - k            # 第 k 大 = 升序排序后下标 n-k 的元素
    lo, hi = 0, len(nums) - 1
    a = nums[:]
    while True:
        pivot = a[random.randint(lo, hi)]
        # 三路划分：< pivot | == pivot | > pivot
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1; i += 1
            elif a[i] > pivot:
                a[gt], a[i] = a[i], a[gt]
                gt -= 1
            else:
                i += 1
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return pivot

random.seed(0)
for _ in range(300):
    arr = [random.randint(0, 9) for _ in range(random.randint(1, 12))]
    k = random.randint(1, len(arr))
    assert quick_select(arr, k) == sorted(arr)[-k]
print(quick_select([3, 2, 1, 5, 6, 4], 2))   # 5
```

三路划分能正确处理大量重复元素，否则在全部相同的数组上会退化成 $O(n^2)$。

### 前 K 个高频元素（力扣 347）

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    cnt = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, cnt.items(), key=lambda kv: kv[1])]

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]
```

### 数据流的中位数（力扣 295）

用两个堆：大根堆存较小的一半，小根堆存较大的一半，保持大根堆的元素个数等于小根堆或多一个。

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []      # 大根堆（存相反数），较小的一半
        self.hi = []      # 小根堆，较大的一半

    def addNum(self, x):
        heapq.heappush(self.lo, -x)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))     # 把 lo 的最大值移到 hi
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2

mf = MedianFinder()
res = []
for x in [5, 15, 1, 3, 8]:
    mf.addNum(x)
    res.append(mf.findMedian())
print(res)    # [5.0, 10.0, 5.0, 4.0, 5.0]
```

### 多路归并：有序矩阵 / 数对的第 K 小

**查找和最小的 K 对数字（力扣 373）**：两个升序数组，找和最小的 k 个数对。先把 `(nums1[i], nums2[0])` 全部入堆，每弹出一个 `(i, j)` 就把 `(i, j+1)` 入堆。

```python
import heapq

def k_smallest_pairs(a, b, k):
    h = [(a[i] + b[0], i, 0) for i in range(min(len(a), k))]
    heapq.heapify(h)
    res = []
    while h and len(res) < k:
        _, i, j = heapq.heappop(h)
        res.append([a[i], b[j]])
        if j + 1 < len(b):
            heapq.heappush(h, (a[i] + b[j + 1], i, j + 1))
    return res

print(k_smallest_pairs([1, 7, 11], [2, 4, 6], 3))   # [[1, 2], [1, 4], [1, 6]]
```

### 任务调度类问题

**会议室 II（力扣 253）**：给定若干会议的起止时间，求最少需要几间会议室。按开始时间排序，小根堆存每间会议室的结束时间。

```python
import heapq

def min_meeting_rooms(intervals):
    intervals.sort()
    ends = []
    for s, e in intervals:
        if ends and ends[0] <= s:        # 最早结束的会议室已空出
            heapq.heapreplace(ends, e)
        else:
            heapq.heappush(ends, e)
    return len(ends)

print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]), min_meeting_rooms([[7, 10], [2, 4]]))   # 2 1
```

## 练习

| 题目 | 方法 |
| --- | --- |
| 力扣 150 逆波兰表达式求值 | 栈 |
| 力扣 71 简化路径 | 栈 |
| 力扣 496 下一个更大元素 I | 单调栈 + 哈希表 |
| 力扣 901 股票价格跨度 | 单调栈 |
| 力扣 402 移掉 K 位数字 | 单调栈，贪心 |
| 力扣 316 去除重复字母 | 单调栈 + 计数 |
| 力扣 862 和至少为 K 的最短子数组 | 前缀和 + 单调队列 |
| 力扣 621 任务调度器 | 贪心或堆 |
| 力扣 502 IPO | 两个堆 |
