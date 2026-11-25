---
date: 2026-11-05
description: 图的存储、网格与图上的 DFS / BFS（岛屿、最短步数、多源 BFS）、拓扑排序、并查集、Dijkstra、Bellman-Ford 与 Floyd、0-1 BFS、最小生成树（Kruskal、Prim），附 ACM 模式的完整程序。
tags:
  - 算法
---

# 图论

笔试中图论题的比重很高，而且几乎都是 ACM 模式。题型比较固定：连通性、最短路、拓扑排序、并查集，模板熟练之后主要的工作是把题意转成图。

## 1. 存图

点数为 $n$、边数为 $m$。

```python
n, edges = 4, [(0, 1, 5), (0, 2, 1), (2, 1, 2), (1, 3, 1)]

# 邻接表：最常用，空间 O(n + m)
g = [[] for _ in range(n)]
for u, v, w in edges:
    g[u].append((v, w))          # 有向边；无向图再加 g[v].append((u, w))

# 邻接矩阵：适合 n 不超过几百的稠密图，Floyd 用它
INF = float("inf")
mat = [[INF] * n for _ in range(n)]
for i in range(n):
    mat[i][i] = 0
for u, v, w in edges:
    mat[u][v] = min(mat[u][v], w)   # 可能有重边，取最小

print(g[0], mat[0])   # [(1, 5), (2, 1)] [0, 5, 1, inf]
```

题目给的点编号从 1 开始时，要么开 $n+1$ 的数组，要么读入时减 1，选一种并保持一致。

## 2. 网格上的搜索

网格是最常见的"隐式图"：每个格子是一个点，和上下左右四个格子相邻。

```python
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
```

**岛屿数量（力扣 200）**：每遇到一个没访问过的陆地，就从它出发把整座岛标记掉，计数加一。

```python
from collections import deque

def num_islands(grid):
    n, m = len(grid), len(grid[0])
    g = [list(row) for row in grid]
    count = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] != "1":
                continue
            count += 1
            g[i][j] = "0"              # 入队时就标记，避免重复入队
            q = deque([(i, j)])
            while q:
                x, y = q.popleft()
                for dx, dy in DIRS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "1":
                        g[nx][ny] = "0"
                        q.append((nx, ny))
    return count

print(num_islands(["11000", "11000", "00100", "00011"]))   # 3
```

一定要在**入队时**标记已访问，而不是出队时。出队时才标记，同一个格子可能被多个邻居重复加入队列，最坏情况下队列会大很多倍。

用递归 DFS 写更短，但网格是 $1000 \times 1000$ 时递归深度可能达到 $10^6$，Python 会爆栈。笔试中网格题优先用 BFS 或显式栈。

### 最短步数：BFS

在无权图（每步代价相同）中，BFS 第一次到达某个点时的步数就是最短距离。

**例：迷宫最短路径**。ACM 模式：第一行 n、m，接下来 n 行网格，`S` 起点、`E` 终点、`#` 墙，输出最少步数，到不了输出 -1。

```python
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S": sx, sy = i, j
            if grid[i][j] == "E": ex, ey = i, j
    dist = [[-1] * m for _ in range(n)]
    dist[sx][sy] = 0
    q = deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        if (x, y) == (ex, ey):
            break
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != "#" and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    print(dist[ex][ey])

main()
```

输入

```text
4 5
S.#..
..#.#
....E
.##..
```

输出

```text
6
```

如果状态不只是位置（例如"还能打破 k 堵墙"、"手里有哪些钥匙"），就把这些信息加进状态里，`dist` 变成 `dist[x][y][k]`，BFS 的结构不变。

### 多源 BFS

**腐烂的橘子（力扣 994）**：所有腐烂的橘子同时向外扩散。把所有起点一起放进队列，就是多源 BFS。

```python
def oranges_rotting(grid):
    n, m = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    q = deque()
    fresh = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == 2:
                q.append((i, j))
            elif g[i][j] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))
        minutes += 1
    return -1 if fresh else minutes

print(oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]), oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]))   # 4 -1
```

"每个格子到最近的 0 的距离"（力扣 542）、"离陆地最远的海洋"（力扣 1162）都是多源 BFS。

## 3. 一般图上的 DFS

**例：统计连通分量，并判断图中是否有环（无向图）**。用显式栈实现，记录父节点：遇到一个已访问、又不是父节点的邻居，就说明有环。

```python
def components_and_cycle(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    seen = [False] * n
    comps, has_cycle = 0, False
    for s in range(n):
        if seen[s]:
            continue
        comps += 1
        seen[s] = True
        st = [(s, -1)]
        while st:
            u, parent = st.pop()
            for v in g[u]:
                if not seen[v]:
                    seen[v] = True
                    st.append((v, u))
                elif v != parent:
                    has_cycle = True
    return comps, has_cycle

print(components_and_cycle(5, [(0, 1), (1, 2), (3, 4)]))          # (2, False)
print(components_and_cycle(4, [(0, 1), (1, 2), (2, 0), (2, 3)]))  # (1, True)
```

（这种环判定在有重边时需要额外处理；无向图判环更推荐用下面的并查集。）

**克隆图、所有可能的路径**这类需要"回溯"的题，用递归 DFS 更自然，注意设置递归上限。

## 4. 拓扑排序

有向无环图（DAG）中，把点排成一个序列，使每条边都从前指向后。典型场景：课程先修关系、任务依赖、编译顺序。

**Kahn 算法**：反复取出入度为 0 的点，删掉它的出边。如果最后取出的点数少于 $n$，说明图中有环。

**课程表 II（力扣 210）**：

```python
from collections import deque

def find_order(n, prerequisites):
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in prerequisites:        # 学 a 之前要先学 b：边 b -> a
        g[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []

print(find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), find_order(2, [[1, 0], [0, 1]]))   # [0, 1, 2, 3] []
```

要求字典序最小的拓扑序时，把队列换成小根堆。

**拓扑序上的 DP**：DAG 上的最长路径、关键路径，按拓扑序依次松弛即可。

```python
def longest_path_dag(n, edges):
    g = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        g[u].append((v, w))
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    dist = [0] * n
    while q:
        u = q.popleft()
        for v, w in g[u]:
            dist[v] = max(dist[v], dist[u] + w)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return max(dist)

# 任务 0 耗时 3 后才能做 1 和 2……求完成所有任务的最短总时间（关键路径）
print(longest_path_dag(5, [(0, 1, 3), (0, 2, 2), (1, 3, 4), (2, 3, 1), (3, 4, 2)]))   # 9
```

## 5. 并查集

维护若干个不相交的集合，支持"合并两个集合"和"查询两个元素是否在同一集合"，两种操作都接近 $O(1)$。

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                 # 集合个数

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # 路径压缩：沿途节点直接指向根
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:   # 按大小合并：小树挂到大树下
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

d = DSU(5)
d.union(0, 1); d.union(3, 4)
print(d.find(1) == d.find(0), d.find(1) == d.find(3), d.count)   # True False 3
```

`find` 写成迭代而不是递归，是为了避免链很长时递归过深。

**冗余连接（力扣 684）**：一棵树多加了一条边，找出这条边。依次合并每条边的两个端点，第一条两端已经连通的边就是答案。

```python
def find_redundant(edges):
    d = DSU(len(edges) + 1)
    for u, v in edges:
        if not d.union(u, v):
            return [u, v]

print(find_redundant([[1, 2], [1, 3], [2, 3]]), find_redundant([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))   # [2, 3] [1, 4]
```

账户合并（力扣 721）、等式方程的可满足性（力扣 990）、省份数量（力扣 547）都是直接的并查集应用。元素不是整数时，先用 dict 把它们映射成编号。

## 6. 最短路

| 算法 | 适用 | 复杂度 |
| --- | --- | --- |
| BFS | 边权都相同 | $O(n+m)$ |
| 0-1 BFS | 边权只有 0 和 1 | $O(n+m)$ |
| Dijkstra（堆优化） | 边权非负 | $O(m \log m)$ |
| Bellman-Ford / SPFA | 有负权边；限制边数 | $O(nm)$ |
| Floyd | 所有点对，$n \le 400$ 左右 | $O(n^3)$ |

### Dijkstra

每次从堆中取出当前距离最小的点，它的距离就确定了，然后松弛它的出边。堆中可能有同一个点的多个旧记录，弹出时比较一下，过期的跳过。

```python
import heapq

def dijkstra(n, g, src):
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:                # 过期记录
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist

g = [[] for _ in range(5)]
for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]:
    g[u].append((v, w))
print(dijkstra(5, g, 0))     # [0, 3, 1, 4, 7]
```

完整的 ACM 程序：n 个点 m 条无向边，求 1 号点到 n 号点的最短距离，不连通输出 -1。

```python
import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    g = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        u, v, w = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        g[u].append((v, w))
        g[v].append((u, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[1] = 0
    h = [(0, 1)]
    push, pop = heapq.heappush, heapq.heappop
    while h:
        d, u = pop(h)
        if d > dist[u]:
            continue
        if u == n:
            break
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                push(h, (nd, v))
    print(dist[n] if dist[n] < INF else -1)

main()
```

输入

```text
4 5
1 2 2
1 3 5
2 3 1
2 4 7
3 4 3
```

输出

```text
6
```

网络延迟时间（力扣 743）、概率最大的路径（力扣 1514，把加法换成乘法、最小换成最大）、最小体力消耗路径（力扣 1631，路径代价是边权最大值）都是 Dijkstra 的变形：只要"路径代价随边数增加而不变好"，Dijkstra 就适用。

### 0-1 BFS

边权只有 0 和 1 时，用双端队列：经过权为 0 的边到达的点放到队首，权为 1 的放到队尾。

```python
from collections import deque

def min_cost_grid(grid):
    """力扣 1368：格子上的箭头 1右 2左 3下 4上，顺着走代价 0，改方向代价 1"""
    n, m = len(grid), len(grid[0])
    dirs = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}
    dist = [[float("inf")] * m for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        for k, (dx, dy) in dirs.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                w = 0 if grid[x][y] == k else 1
                if dist[x][y] + w < dist[nx][ny]:
                    dist[nx][ny] = dist[x][y] + w
                    if w == 0:
                        q.appendleft((nx, ny))
                    else:
                        q.append((nx, ny))
    return dist[n - 1][m - 1]

print(min_cost_grid([[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]]))   # 3
```

### Bellman-Ford：限制边数的最短路

**K 站中转内最便宜的航班（力扣 787）**：最多经过 k 个中转站，即最多 k+1 条边。Bellman-Ford 第 i 轮松弛后得到的是"最多用 i 条边"的最短路。每轮要基于上一轮的结果松弛，所以先复制一份。

```python
def find_cheapest_price(n, flights, src, dst, k):
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        prev = dist[:]
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return -1 if dist[dst] == INF else dist[dst]

flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
print(find_cheapest_price(4, flights, 0, 3, 1), find_cheapest_price(4, flights, 0, 3, 2))   # 700 400
```

没有边数限制时，做 $n-1$ 轮；第 $n$ 轮还能松弛，说明存在负环。

### Floyd：任意两点间最短路

```python
def floyd(n, edges):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
        d[v][u] = min(d[v][u], w)
    for k in range(n):                 # 中转点 k 必须在最外层
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return d

d = floyd(4, [(0, 1, 3), (1, 2, 1), (2, 3, 7), (0, 3, 15)])
print(d[0], d[3])    # [0, 3, 4, 11] [11, 8, 7, 0]
```

把 `d[k]`、`d[i][k]`、`d[i]` 提到外层的局部变量，在 Python 里能快一倍以上。$n = 400$ 时内层要跑 $6.4 \times 10^7$ 次，Python 仍然很吃力，能用 Dijkstra 跑 $n$ 次的就不要用 Floyd。

## 7. 最小生成树

连通无向图中选 $n-1$ 条边把所有点连起来，使总权值最小。

**Kruskal**：边按权值从小到大排序，依次加入，用并查集跳过会形成环的边。

```python
def kruskal(n, edges):
    d = DSU(n)
    total, used = 0, 0
    for w, u, v in sorted((w, u, v) for u, v, w in edges):
        if d.union(u, v):
            total += w
            used += 1
            if used == n - 1:
                break
    return total if used == n - 1 else -1      # -1 表示图不连通

edges = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (2, 4, 5)]
print(kruskal(5, edges))    # 8
```

**Prim**：从一个点出发，每次用堆选出连接"已选集合"和"未选集合"的最短边。稠密图（例如力扣 1584，所有点两两之间都有边）用 $O(n^2)$ 的朴素 Prim 更快：

```python
def min_cost_connect_points(points):
    n = len(points)
    INF = float("inf")
    dist = [INF] * n            # 每个未选点到已选集合的最短距离
    dist[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=lambda i: dist[i])
        used[u] = True
        total += dist[u]
        ux, uy = points[u]
        for v in range(n):
            if not used[v]:
                w = abs(points[v][0] - ux) + abs(points[v][1] - uy)
                if w < dist[v]:
                    dist[v] = w
    return total

print(min_cost_connect_points([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]))   # 20
```

## 8. 二分图判定

**判断二分图（力扣 785）**：用 BFS 给点染两种颜色，相邻点颜色必须不同。

```python
def is_bipartite(g):
    n = len(g)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in g[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True

print(is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]), is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]))   # True False
```

## 练习

| 题目 | 方法 |
| --- | --- |
| 力扣 130 被围绕的区域 | 从边界出发 DFS/BFS |
| 力扣 417 太平洋大西洋水流问题 | 从两个海洋反向 BFS |
| 力扣 127 单词接龙 | BFS，或双向 BFS |
| 力扣 207 课程表 | 拓扑排序判环 |
| 力扣 399 除法求值 | 带权并查集或 DFS |
| 力扣 1584 连接所有点的最小费用 | 最小生成树 |
| 力扣 882 细分图中的可到达节点 | Dijkstra |
| 力扣 1293 网格中的最短路径 | BFS，状态带上剩余消除次数 |
