---
date: 2026-11-05
description: ACM 模式下的各种输入格式（单组、多组、读到 EOF、矩阵、字符串）、快速读入、输出格式、递归深度、整体代码框架，以及核心代码模式和 ACM 模式的转换。
tags:
  - 算法
  - Python
---

# ACM 模式输入输出

ACM 模式下，题目只描述输入输出格式，程序要自己解析标准输入。很多人在力扣上刷题很熟练，笔试时却卡在读入上，或者因为输出多了一个空格而判错。

## 1. 两种读入方式

### input()

```python
n = int(input())
a = list(map(int, input().split()))
print(n, sum(a))
```

输入

```text
3
1 2 3
```

输出

```text
3 6
```

`input()` 每次读一行，去掉末尾换行符。`input().split()` 按任意空白切分，行首行尾多余的空格不影响结果。

### sys.stdin 一次全部读入

```python
import sys

data = sys.stdin.read().split()
n = int(data[0])
a = list(map(int, data[1:1 + n]))
print(n, sum(a))
```

输入

```text
3
1 2
3
```

输出

```text
3 6
```

把整个输入读成一个字符串，按空白切成 token 列表，再用一个下标依次取用。这种写法**不关心换行**：上面的数据本该写在一行，却被拆成了两行，照样能正确读入。很多题目的输入格式描述不严谨（比如说"一行 n 个数"，实际数据却分了多行），这种写法最稳妥，数据量大时也最快。

推荐把它包装成一个迭代器，用 `next()` 取下一个 token：

```python
import sys

def main():
    it = iter(sys.stdin.read().split())
    n, m = int(next(it)), int(next(it))
    grid = [[int(next(it)) for _ in range(m)] for _ in range(n)]
    print(sum(map(sum, grid)))

main()
```

输入

```text
2 3
1 2 3
4 5 6
```

输出

```text
21
```

### 速度对比

读入 $10^6$ 个整数，`input()` 逐行读加 `split` 一般在可接受范围内；但如果是 $10^5$ 行、每行一两个数，循环调用 $10^5$ 次 `input()` 会明显变慢。可以把 `input` 替换成更快的版本：

```python
import sys
input = sys.stdin.readline      # 注意：读到的行末尾带 '\n'

n = int(input())                # int() 会忽略首尾空白，这里没问题
s = input().strip()             # 读字符串时必须 strip，否则末尾多一个换行符
print(n, s, len(s))
```

输入

```text
2
abc
```

输出

```text
2 abc 3
```

字节流读法 `sys.stdin.buffer.read().split()` 还要更快一些，得到的是 `bytes` 列表，`int(b"12")` 可以直接转换，字符串则需要 `.decode()`。

## 2. 常见输入格式

### 先给组数 T

```python
import sys

def solve(a):
    return max(a) - min(a)

def main():
    it = iter(sys.stdin.read().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        out.append(str(solve(a)))
    print("\n".join(out))

main()
```

输入

```text
2
3
1 5 3
4
7 7 7 7
```

输出

```text
4
0
```

结果先收集到列表里，最后一次性输出。比每组 `print` 一次快，组数多时差距明显。

### 不给组数，读到文件末尾

"输入包含多组测试数据"而没说有几组，就要读到 EOF 为止：

```python
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue                 # 跳过空行，很多数据末尾会多一个空行
    a, b = map(int, line.split())
    print(a + b)
```

输入

```text
1 2
10 20

3 4
```

输出

```text
3
30
7
```

用 `input()` 写的话要捕获 `EOFError`：

```python
while True:
    try:
        line = input()
    except EOFError:
        break
    if line.strip():
        print(sum(map(int, line.split())))
```

输入

```text
1 2 3
4 5
```

输出

```text
6
9
```

如果每组数据是"先给 n、再给 n 个数"，而组数未知，用 token 迭代器的写法最省事：

```python
import sys

data = sys.stdin.read().split()
pos, out = 0, []
while pos < len(data):
    n = int(data[pos]); pos += 1
    a = list(map(int, data[pos:pos + n])); pos += n
    out.append(str(sum(a)))
print("\n".join(out))
```

输入

```text
2
1 2
3
4 5 6
```

输出

```text
3
15
```

### 以特殊值结束

"输入以 0 0 结束"这类格式，读到结束标志就退出：

```python
import sys

for line in sys.stdin:
    a, b = map(int, line.split())
    if a == 0 and b == 0:
        break
    print(a * b)
```

输入

```text
2 3
4 5
0 0
```

输出

```text
6
20
```

### 字符串与字符矩阵

```python
import sys

input = sys.stdin.readline
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]       # 每行是一个字符串
cnt = sum(row.count("#") for row in grid)
g = [list(row) for row in grid]                  # 需要修改时转成字符列表
g[0][0] = "@"
print(cnt, "".join(g[0]))
```

输入

```text
2 4
#..#
.##.
```

输出

```text
4 @..#
```

字符串在 Python 中不可变，要修改网格就转成 `list`。

### 一行里是逗号分隔的数据

有些公司的题目直接给一个类似 Python 列表的字符串：

```python
import sys

line = sys.stdin.readline().strip()            # 例如 [1,2,3,4]
nums = [int(x) for x in line.strip("[]").split(",") if x.strip()]
print(nums, sum(nums))
```

输入

```text
[1, 2, 3, 4]
```

输出

```text
[1, 2, 3, 4] 10
```

格式更复杂的（嵌套列表、带引号的字符串）可以用 `ast.literal_eval`，它只解析字面量，比 `eval` 安全：

```python
import ast
import sys

grid = ast.literal_eval(sys.stdin.readline())
words = ast.literal_eval(sys.stdin.readline())
print(len(grid), grid[1][0], words[1])
```

输入

```text
[[1,2],[3,4]]
["abc", "de"]
```

输出

```text
2 3 de
```

### 读入一棵树或一张图

最常见的是"n 个点、m 条边，接下来 m 行每行 u v w"：

```python
import sys

def main():
    it = iter(sys.stdin.read().split())
    n, m = int(next(it)), int(next(it))
    g = [[] for _ in range(n + 1)]          # 点从 1 编号时开 n+1 个
    for _ in range(m):
        u, v, w = int(next(it)), int(next(it)), int(next(it))
        g[u].append((v, w))
        g[v].append((u, w))                 # 无向图两个方向都要加
    print([len(g[i]) for i in range(1, n + 1)])

main()
```

输入

```text
3 2
1 2 5
2 3 7
```

输出

```text
[1, 2, 1]
```

注意题目里的点是从 0 还是从 1 开始编号。链表、二叉树在 ACM 模式下的读入和构建，见 [链表](linked-list.md) 和 [二叉树](tree.md)。

## 3. 输出格式

```python
a = [1, 2, 3]
print(*a)                    # 1 2 3，空格分隔
print(" ".join(map(str, a))) # 同上
print(*a, sep=",")           # 1,2,3
print("\n".join(map(str, a)))   # 每行一个
print(f"{3.14159:.2f}")      # 3.14，保留两位小数
print("%.3f" % 2.0)          # 2.000
print("Yes" if 3 > 2 else "No")
```

注意点：

- 大小写、标点要与题目完全一致：`YES` 和 `Yes` 是不同的输出。
- 保留小数用格式化，不要用 `round`：`round(2.0, 2)` 输出的是 `2.0`，不是 `2.00`。另外 `round` 对恰好一半的情况取偶数（`round(2.5)` 是 `2`），浮点误差还会让 `round(2.675, 2)` 得到 `2.67`。
- 多数评测机会忽略行末空格和文末换行，但不要依赖这一点，用 `" ".join` 就不会产生多余的空格。
- 输出大量数据时，先拼成一个字符串，最后 `sys.stdout.write(s)` 或 `print(s)` 一次输出。

## 4. 递归深度

Python 默认递归深度上限是 1000，DFS 一条长链（例如 $10^5$ 个点排成一条线的树）会抛出 `RecursionError`：

```python
import sys
sys.setrecursionlimit(1 << 20)
```

调大上限之后，深度太大仍然可能因为 C 栈溢出而直接崩溃（不报 Python 异常，进程退出）。可以在新线程里运行并调大线程栈：

```py
import sys, threading

def main():
    ...  # 原来的代码

sys.setrecursionlimit(1 << 25)
threading.stack_size(1 << 27)       # 128 MB
t = threading.Thread(target=main)
t.start()
t.join()
```

最稳妥的办法是把递归改写成用显式栈的迭代，图的 DFS、树的后序遍历都可以这样做，见 [图论](graph.md) 和 [二叉树](tree.md)。

## 5. 完整框架

笔试时可以直接从这个框架开始写：

```python
import sys
from collections import defaultdict, deque, Counter
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from functools import lru_cache
from math import gcd, inf

def solve(n, a):
    # 在这里写算法，返回答案
    return sum(a)

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(next(it)) for _ in range(n)]
        out.append(str(solve(n, a)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
```

输入

```text
2
3 1 2 3
2 10 20
```

输出

```text
6
30
```

把读入、计算、输出分开，`solve` 写成和力扣一样的纯函数，调试时可以直接在本地调用 `solve` 测试。

### 本地测试

把样例存成 `in.txt`，用重定向运行，不用每次手动粘贴：

```bash
python main.py < in.txt
python main.py < in.txt > out.txt && diff out.txt ans.txt
```

## 6. 核心代码模式和 ACM 模式的转换

力扣上一道题：

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        pos = {}
        for i, x in enumerate(nums):
            if target - x in pos:
                return [pos[target - x], i]
            pos[x] = i
        return []

print(Solution().twoSum([2, 7, 11, 15], 9))   # [0, 1]
```

同一道题在笔试中的 ACM 写法，第一行 n 和 target，第二行 n 个数：

```python
import sys

def two_sum(nums, target):
    pos = {}
    for i, x in enumerate(nums):
        if target - x in pos:
            return pos[target - x], i
        pos[x] = i
    return -1, -1

def main():
    it = iter(sys.stdin.read().split())
    n, target = int(next(it)), int(next(it))
    nums = [int(next(it)) for _ in range(n)]
    i, j = two_sum(nums, target)
    print(i, j)

main()
```

输入

```text
4 9
2 7 11 15
```

输出

```text
0 1
```

## 7. 常见错误

| 现象 | 原因 |
| --- | --- |
| `ValueError: invalid literal for int()` | 一行里有多个数却用了 `int(input())`；或者读到了空行 |
| `EOFError` | 输入的行数比代码里读的少，往往是对格式理解有误；用 token 迭代器读入可以避免 |
| 读到的字符串比预期多一个字符 | `sys.stdin.readline()` 没有 `strip()`，末尾带着 `'\n'` |
| 本地正确，提交答案错误 | 输出格式不对（多余空格、大小写、小数位数）；没处理多组数据 |
| 超时 | 逐行 `input()` 读大量数据；在循环里频繁 `print`；算法复杂度本身就不够 |
| 运行错误但看不到报错 | 递归太深导致的崩溃；数组下标越界 |
