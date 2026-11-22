---
date: 2026-11-05
description: 时间与空间复杂度的估算、Python 内置操作的复杂度，以及刷题最常用的标准库：deque、heapq、bisect、Counter、defaultdict、lru_cache、itertools，和 Python 写算法时的提速技巧。
tags:
  - 算法
  - Python
---

# 复杂度与 Python 工具箱

## 1. 复杂度

时间复杂度描述运行时间随输入规模 $n$ 增长的趋势，只保留最高阶项、忽略常数：$3n^2+5n$ 记作 $O(n^2)$。

```python
def pair_sum_exists(a, target):     # O(n^2)
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == target:
                return True
    return False

def pair_sum_exists_fast(a, target):    # O(n)，用哈希集合
    seen = set()
    for x in a:
        if target - x in seen:
            return True
        seen.add(x)
    return False

print(pair_sum_exists([3, 1, 4], 7), pair_sum_exists_fast([3, 1, 4], 8))   # True False
```

几条估算规则：

- 一层循环 $O(n)$，两层嵌套 $O(n^2)$。
- 每次把问题规模减半（二分）是 $O(\log n)$。
- 排序是 $O(n \log n)$。
- 递归的复杂度 = 递归调用的总次数 × 每次调用的工作量。不加记忆化的斐波那契递归是 $O(2^n)$，加了记忆化是 $O(n)$。
- 均摊复杂度：`list.append` 偶尔需要扩容复制，但平均每次是 $O(1)$。单调栈中每个元素最多进栈出栈各一次，所以虽然有嵌套的 `while`，整体仍是 $O(n)$。

空间复杂度同理，看额外开了多大的数组或者递归有多深。题目一般给 256 MB 内存，Python 里一个 `int` 对象约 28 字节，list 中每个元素再多 8 字节的指针，$10^7$ 个整数的 list 就要几百 MB，要注意。

## 2. 内置操作的复杂度

| 操作 | list | dict / set | deque |
| --- | --- | --- | --- |
| 按下标访问 `a[i]` | $O(1)$ | — | $O(n)$ |
| 末尾追加 / 弹出 | $O(1)$ | — | $O(1)$ |
| 头部插入 / 弹出 | $O(n)$ | — | $O(1)$ |
| `x in a` | $O(n)$ | $O(1)$ | $O(n)$ |
| 按 key 增删改查 | — | $O(1)$ | — |
| 切片 `a[i:j]` | $O(j-i)$，会复制 | — | — |
| `len` | $O(1)$ | $O(1)$ | $O(1)$ |
| `sorted` / `sort` | $O(n \log n)$ | — | — |
| `min` / `max` / `sum` | $O(n)$ | $O(n)$ | $O(n)$ |

最常见的超时原因：在循环里对 list 用 `in`、`pop(0)`、`insert(0, x)`、`index`、`remove`、切片，它们都是 $O(n)$，放在循环里就成了 $O(n^2)$。

字符串也一样：`s[1:]` 会复制，`s += c` 在循环里可能退化成平方复杂度，要拼接就先放进 list 最后 `"".join`。

## 3. collections

### deque：双端队列

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)          # 右端加入
q.appendleft(0)      # 左端加入
print(q.popleft(), q.pop(), list(q))   # 0 4 [1, 2, 3]
q.rotate(1)          # 向右循环移动一位
print(list(q), q[0], q[-1])            # [3, 1, 2] 3 2

window = deque(maxlen=3)   # 固定长度，满了以后再加入会从另一端挤出元素
for x in range(5):
    window.append(x)
print(list(window))        # [2, 3, 4]
```

BFS 的队列一定用 `deque`，不要用 list 的 `pop(0)`。

### Counter 与 defaultdict

```python
from collections import Counter, defaultdict

c = Counter("abracadabra")
print(c["a"], c["z"], c.most_common(2))   # 5 0 [('a', 5), ('b', 2)]
print(Counter("listen") == Counter("silent"))   # True，判断字母异位词

g = defaultdict(list)          # 访问不存在的 key 时自动创建空 list
for u, v in [(1, 2), (1, 3), (2, 3)]:
    g[u].append(v)
print(dict(g))                 # {1: [2, 3], 2: [3]}

cnt = defaultdict(int)
for w in "a b a".split():
    cnt[w] += 1
print(dict(cnt))               # {'a': 2, 'b': 1}
```

`Counter` 访问不存在的 key 返回 0 但**不会插入**；`defaultdict` 访问不存在的 key **会插入**默认值。遍历 `defaultdict` 时在循环体里访问新 key，会导致 "dictionary changed size during iteration"。

## 4. heapq：堆

Python 的 `heapq` 是**小根堆**，直接在 list 上操作。

```python
import heapq

h = []
for x in [5, 1, 8, 3]:
    heapq.heappush(h, x)
print(h[0])                     # 1，堆顶是最小值
print(heapq.heappop(h), heapq.heappop(h))   # 1 3

a = [9, 4, 7, 1]
heapq.heapify(a)                # O(n) 原地建堆
print(heapq.nsmallest(2, a), heapq.nlargest(2, a))   # [1, 4] [9, 7]
```

需要**大根堆**时，存相反数：

```python
h = []
for x in [5, 1, 8]:
    heapq.heappush(h, -x)
print(-h[0])                    # 8
```

元素是 tuple 时按字典序比较，常用来按优先级出堆：

```python
tasks = []
heapq.heappush(tasks, (2, "write"))
heapq.heappush(tasks, (1, "read"))
heapq.heappush(tasks, (2, "eat"))
print([heapq.heappop(tasks)[1] for _ in range(3)])   # ['read', 'eat', 'write']
```

优先级相同时会比较第二个元素，如果第二个元素不能比较（例如链表节点对象），会报 `TypeError`。解决办法是在中间插一个自增的序号：`(priority, idx, node)`。

`heapq` 不支持修改或删除堆中任意元素。Dijkstra 等算法的做法是"懒删除"：直接把新值推入堆，弹出时发现是过期的旧值就跳过。

## 5. bisect：有序数组上的二分

```python
from bisect import bisect_left, bisect_right, insort

a = [1, 3, 3, 3, 7]
print(bisect_left(a, 3))    # 1，第一个 >= 3 的位置
print(bisect_right(a, 3))   # 4，第一个 > 3 的位置
print(bisect_right(a, 3) - bisect_left(a, 3))   # 3，3 出现的次数
print(bisect_left(a, 4))    # 4，4 应当插入的位置
print(bisect_left(a, 100))  # 5，比所有元素都大时返回 len(a)

insort(a, 5)                # 插入并保持有序，O(n)
print(a)                    # [1, 3, 3, 3, 5, 7]
```

Python 3.10 起 `bisect` 支持 `key` 参数：`bisect_left(items, x, key=lambda it: it[0])`。

二分的原理和手写模板见 [二分查找](binary-search.md)。

## 6. functools

### lru_cache：记忆化搜索

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def ways(n):
    """爬楼梯：每次 1 或 2 级，到第 n 级的方法数"""
    if n <= 1:
        return 1
    return ways(n - 1) + ways(n - 2)

print(ways(50))     # 20365011074
```

参数必须可哈希，list 要先转成 tuple。Python 3.9 起可以用 `@cache`，等价于 `@lru_cache(maxsize=None)`。

在力扣上，`Solution` 类里定义的记忆化函数要写在方法内部，否则多个测试用例之间会共用缓存：

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        @lru_cache(maxsize=None)
        def dfs(i):
            return 1 if i <= 1 else dfs(i - 1) + dfs(i - 2)
        return dfs(n)

print(Solution().climbStairs(10))   # 89
```

### cmp_to_key：自定义比较

排序规则无法用 key 表达时，写一个比较函数：返回负数表示 `a` 排前面，正数表示 `b` 排前面。

```python
from functools import cmp_to_key

def largest_number(nums):
    """把数字拼成最大的数"""
    strs = list(map(str, nums))
    strs.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
    s = "".join(strs)
    return "0" if s[0] == "0" else s

print(largest_number([3, 30, 34, 5, 9]))   # 9534330
```

## 7. itertools 与其他

```python
from itertools import permutations, combinations, product, accumulate, pairwise

print(list(permutations([1, 2, 3], 2)))   # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
print(list(combinations("abc", 2)))       # [('a', 'b'), ('a', 'c'), ('b', 'c')]
print(list(product([0, 1], repeat=2)))    # [(0, 0), (0, 1), (1, 0), (1, 1)]
print(list(accumulate([1, 2, 3], initial=0)))   # [0, 1, 3, 6]，前缀和
print(list(pairwise([1, 4, 9])))          # [(1, 4), (4, 9)]
```

暴力枚举用 `permutations`、`combinations` 写起来很快，适合 $n$ 很小的题，或者用来写对拍程序。

```python
import math
print(math.gcd(12, 18), math.lcm(4, 6))        # 6 12
print(math.comb(5, 2), math.perm(5, 2))        # 10 20
print(math.isqrt(17))                          # 4，整数平方根，没有浮点误差
print(math.inf > 10**18, -math.inf < -10**18)  # True True
print(pow(2, 10, 1000))                        # 24，快速幂取模
print(divmod(-7, 2))                           # (-4, 1)
```

`math.isqrt` 比 `int(math.sqrt(n))` 可靠，后者在 $n$ 很大时会有浮点误差。Python 的整数没有上限，不会溢出，这是相比 C++ 的一个优势；但在要求取模的题里仍然要及时取模，否则大整数运算会很慢。

## 8. 提速技巧

Python 写算法题，同样的复杂度常数也比 C++ 大很多，下面这些技巧在卡时间的题上有用：

```python
import time

n = 10**6
t0 = time.perf_counter()
s = 0
for i in range(n):
    s += i * i
t_loop = time.perf_counter() - t0

t0 = time.perf_counter()
s2 = sum(i * i for i in range(n))
t_gen = time.perf_counter() - t0
print(s == s2)      # True
```

- **函数里写代码**：局部变量的访问比全局变量快，把主逻辑放进 `main()` 里调用，常能快 20%～30%。
- **用内置函数**：`sum`、`max`、`min`、`sorted`、`map`、`any`、推导式都在 C 层面循环，比手写 for 快。
- **一次性读入、一次性输出**，见 [ACM 模式](acm-io.md)。
- **少用对象和属性访问**：`dist[v]` 比 `node.dist` 快；热点循环里把 `heapq.heappush` 先赋值给局部变量 `push = heapq.heappush`。
- **二维数组展平**：`grid[i * m + j]` 比 `grid[i][j]` 少一次下标访问，网格类题目可以考虑。
- **初始化数组**用 `[0] * n`，二维用 `[[0] * m for _ in range(n)]`（不要写成 `[[0] * m] * n`，那样每行是同一个对象）。
- 递归改迭代，既避免爆栈又更快。

## 9. 对拍

自己的解法过了样例但不确定对不对时，写一个暴力解法，用随机数据比较两者的输出：

```python
import random

def fast(a):           # 待验证的解法：最大子数组和
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

def brute(a):
    return max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1))

random.seed(0)
for _ in range(500):
    a = [random.randint(-10, 10) for _ in range(random.randint(1, 8))]
    assert fast(a) == brute(a), a
print("all passed")
```

随机数据的规模要小，出错时才方便手动分析。面试中能主动提出用暴力解验证，也是加分项。
