---
date: 2026-11-05
description: 二叉树的定义、从层序数组（含 null）构建与 ACM 模式输入、四种遍历的递归与迭代写法、"自顶向下"与"自底向上"两类递归、直径与路径和、二叉搜索树、最近公共祖先、构造与序列化、普通树与树形 DP。
tags:
  - 算法
---

# 二叉树

树的题目几乎都是递归。写递归时只想清楚两件事：这个函数对一棵子树返回什么；怎样用左右子树的返回值得到当前子树的结果。不要试图在脑子里展开整个递归过程。

## 1. 定义与构建

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

力扣用层序数组表示二叉树，空节点写作 `null`，例如 `[3,9,20,null,null,15,7]`：

```text
    3
   / \
  9  20
    /  \
   15   7
```

ACM 模式下树的输入通常就是这种格式，需要自己构建。按层序依次给每个节点分配左右孩子：

```python
def build_tree(vals):
    """vals 是层序列表，None 表示空节点"""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root

def to_level_list(root):
    """转回力扣格式，去掉末尾的 None，用于检查结果"""
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node:
            out.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out

root = build_tree([3, 9, 20, None, None, 15, 7])
print(to_level_list(root))    # [3, 9, 20, None, None, 15, 7]
```

注意空节点的孩子不再出现在数组中，所以不能用"下标 i 的孩子是 2i+1 和 2i+2"来建树，那只适用于完全二叉树。

完整的 ACM 程序：一行层序序列，`null` 表示空，输出树的最大深度。

```python
import sys
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q, i = deque([root]), 1
    while q and i < len(vals):
        node = q.popleft()
        for side in ("left", "right"):
            if i < len(vals) and vals[i] is not None:
                child = TreeNode(vals[i])
                setattr(node, side, child)
                q.append(child)
            i += 1
    return root

def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

tokens = sys.stdin.read().replace("[", " ").replace("]", " ").replace(",", " ").split()
vals = [None if t in ("null", "None", "#") else int(t) for t in tokens]
print(max_depth(build_tree(vals)))
```

输入

```text
[3,9,20,null,null,15,7]
```

输出

```text
3
```

先把方括号和逗号都替换成空格再切分，这样不管输入是 `[3,9,20,null]` 还是 `3 9 20 null`，都能正确读入。

另一种常见格式是"n 个节点，接下来 n 行每行给出节点的值、左孩子编号、右孩子编号（-1 表示没有）"，这时先建好所有节点，再按编号连接：

```python
import sys

def main():
    it = iter(sys.stdin.read().split())
    n = int(next(it))
    nodes = [TreeNode() for _ in range(n)]
    is_child = [False] * n
    for i in range(n):
        v, l, r = int(next(it)), int(next(it)), int(next(it))
        nodes[i].val = v
        if l != -1:
            nodes[i].left = nodes[l]; is_child[l] = True
        if r != -1:
            nodes[i].right = nodes[r]; is_child[r] = True
    root = nodes[is_child.index(False)]       # 不是任何节点孩子的就是根
    print(root.val, max_depth(root))

main()
```

输入

```text
4
1 1 2
2 -1 -1
3 3 -1
4 -1 -1
```

输出

```text
1 3
```

## 2. 遍历

```python
root = build_tree([1, 2, 3, 4, 5, None, 6])
#        1
#      /   \
#     2     3
#    / \     \
#   4   5     6

def preorder(node, out):        # 根 左 右
    if node:
        out.append(node.val)
        preorder(node.left, out)
        preorder(node.right, out)
    return out

def inorder(node, out):         # 左 根 右
    if node:
        inorder(node.left, out)
        out.append(node.val)
        inorder(node.right, out)
    return out

def postorder(node, out):       # 左 右 根
    if node:
        postorder(node.left, out)
        postorder(node.right, out)
        out.append(node.val)
    return out

print(preorder(root, []), inorder(root, []), postorder(root, []))
# [1, 2, 4, 5, 3, 6] [4, 2, 5, 1, 3, 6] [4, 5, 2, 6, 3, 1]
```

### 迭代写法

面试常要求不用递归。前序：栈里先压右孩子再压左孩子。

```python
def preorder_iter(root):
    if not root:
        return []
    st, out = [root], []
    while st:
        node = st.pop()
        out.append(node.val)
        if node.right: st.append(node.right)
        if node.left: st.append(node.left)
    return out

def inorder_iter(root):
    st, out, cur = [], [], root
    while cur or st:
        while cur:                 # 一路向左，沿途入栈
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        out.append(cur.val)
        cur = cur.right
    return out

def postorder_iter(root):
    # 按"根 右 左"的顺序前序遍历，再反转，就是"左 右 根"
    if not root:
        return []
    st, out = [root], []
    while st:
        node = st.pop()
        out.append(node.val)
        if node.left: st.append(node.left)
        if node.right: st.append(node.right)
    return out[::-1]

print(preorder_iter(root), inorder_iter(root), postorder_iter(root))
# [1, 2, 4, 5, 3, 6] [4, 2, 5, 1, 3, 6] [4, 5, 2, 6, 3, 1]
```

### 层序遍历（力扣 102）

```python
def level_order(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # 当前队列里恰好是一整层
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res

print(level_order(root))   # [[1], [2, 3], [4, 5, 6]]
```

右视图（力扣 199）取每层最后一个，锯齿形遍历（力扣 103）把奇数层反转，最大宽度（力扣 662）给节点编号，都是在这个框架上改。

## 3. 两类递归

### 自底向上：用子树的返回值计算

**最大深度（力扣 104）**：`depth(node) = 1 + max(depth(left), depth(right))`。

**平衡二叉树（力扣 110）**：返回高度，不平衡时返回 -1，一次遍历同时完成计算高度和判断。

```python
def is_balanced(root):
    def height(node):
        if node is None:
            return 0
        lh = height(node.left)
        if lh == -1:
            return -1
        rh = height(node.right)
        if rh == -1 or abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)
    return height(root) != -1

print(is_balanced(build_tree([3, 9, 20, None, None, 15, 7])), is_balanced(build_tree([1, 2, None, 3])))   # True False
```

**二叉树的直径（力扣 543）**：最长路径不一定经过根。递归函数返回"从当前节点向下的最长链长度"，同时用"左链 + 右链"更新全局答案。

```python
def diameter(root):
    best = 0
    def depth(node):
        nonlocal best
        if node is None:
            return 0
        l, r = depth(node.left), depth(node.right)
        best = max(best, l + r)          # 经过 node 的最长路径（边数）
        return 1 + max(l, r)
    depth(root)
    return best

print(diameter(build_tree([1, 2, 3, 4, 5])))   # 3
```

**二叉树中的最大路径和（力扣 124）**：同样的结构，节点值可能为负，子链为负就不要它。

```python
def max_path_sum(root):
    best = float("-inf")
    def gain(node):
        nonlocal best
        if node is None:
            return 0
        l = max(gain(node.left), 0)
        r = max(gain(node.right), 0)
        best = max(best, node.val + l + r)
        return node.val + max(l, r)      # 向上只能带一条链
    gain(root)
    return best

print(max_path_sum(build_tree([-10, 9, 20, None, None, 15, 7])))   # 42
```

"返回给父节点的值"和"更新答案的值"不同，是这类题的共同特点。

### 自顶向下：把信息从根传到叶子

**路径总和 II（力扣 113）**：找所有从根到叶子、和为 target 的路径。递归参数带上当前路径，到叶子时检查。

```python
def path_sum(root, target):
    res, path = [], []
    def dfs(node, remain):
        if node is None:
            return
        path.append(node.val)
        remain -= node.val
        if node.left is None and node.right is None and remain == 0:
            res.append(path[:])          # 复制一份，path 之后还会变
        dfs(node.left, remain)
        dfs(node.right, remain)
        path.pop()                       # 回溯
    dfs(root, target)
    return res

print(path_sum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]), 22))
# [[5, 4, 11, 2], [5, 8, 4, 5]]
```

**路径总和 III（力扣 437）**：路径不必从根开始、不必到叶子，只要向下。用前缀和加哈希表，与数组中"和为 K 的子数组"一样。

```python
from collections import defaultdict

def path_sum3(root, target):
    cnt = defaultdict(int)
    cnt[0] = 1
    def dfs(node, s):
        if node is None:
            return 0
        s += node.val
        res = cnt[s - target]
        cnt[s] += 1
        res += dfs(node.left, s) + dfs(node.right, s)
        cnt[s] -= 1                      # 离开这个节点时撤销，保证只统计祖先链上的前缀和
        return res
    return dfs(root, 0)

print(path_sum3(build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8))   # 3
```

## 4. 二叉搜索树

二叉搜索树（BST）：左子树所有节点 < 根 < 右子树所有节点。**中序遍历结果是升序的**，大部分 BST 题都利用这一点。

**验证二叉搜索树（力扣 98）**：只比较节点和它的孩子是不够的，要传递上下界。

```python
def is_valid_bst(root):
    def ok(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))

print(is_valid_bst(build_tree([2, 1, 3])), is_valid_bst(build_tree([5, 1, 6, None, None, 3, 7])))   # True False
```

第二棵树中 3 是 6 的左孩子，满足"小于父节点"，但它在根 5 的右子树里，却小于 5。

**二叉搜索树中第 K 小的元素（力扣 230）**：中序遍历到第 k 个。

```python
def kth_smallest(root, k):
    st, cur = [], root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right

print(kth_smallest(build_tree([5, 3, 6, 2, 4, None, None, 1]), 3))   # 3
```

**BST 的插入与删除（力扣 701、450）**：

```python
def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def delete(root, key):
    if root is None:
        return None
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right                # 右子树的最小节点
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete(root.right, succ.val)
    return root

t = None
for v in [5, 3, 6, 2, 4, 7]:
    t = insert(t, v)
t = delete(t, 3)
print(inorder(t, []), to_level_list(t))   # [2, 4, 5, 6, 7] [5, 4, 6, 2, None, None, 7]
```

**有序数组转平衡 BST（力扣 108）**：取中间元素作根，递归构建左右两半。

```python
def sorted_array_to_bst(a, lo=0, hi=None):
    if hi is None:
        hi = len(a)
    if lo >= hi:
        return None
    mid = (lo + hi) // 2
    return TreeNode(a[mid], sorted_array_to_bst(a, lo, mid), sorted_array_to_bst(a, mid + 1, hi))

print(to_level_list(sorted_array_to_bst([-10, -3, 0, 5, 9])))   # [0, -3, 9, -10, None, 5]
```

## 5. 最近公共祖先

**二叉树的最近公共祖先（力扣 236）**：

```python
def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:           # p、q 分居两侧，root 就是答案
        return root
    return left or right

def find(root, v):
    if root is None or root.val == v:
        return root
    return find(root.left, v) or find(root.right, v)

t = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
print(lowest_common_ancestor(t, find(t, 5), find(t, 1)).val,
      lowest_common_ancestor(t, find(t, 5), find(t, 4)).val)   # 3 5
```

函数的含义：在以 root 为根的子树中，如果同时包含 p 和 q，返回它们的最近公共祖先；如果只包含其中一个，返回那一个；都不包含返回 None。

BST 上的 LCA（力扣 235）更简单：从根往下走，p、q 都比当前节点小就往左，都比它大就往右，否则当前节点就是答案。

## 6. 构造与序列化

**从前序与中序遍历序列构造二叉树（力扣 105）**：前序的第一个是根，在中序里找到根的位置，左边是左子树、右边是右子树。

```python
def build_from_pre_in(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}     # 值互不相同
    def build(pl, pr, il, ir):                       # 左闭右开区间
        if pl >= pr:
            return None
        root_val = preorder[pl]
        k = pos[root_val]
        left_size = k - il
        root = TreeNode(root_val)
        root.left = build(pl + 1, pl + 1 + left_size, il, k)
        root.right = build(pl + 1 + left_size, pr, k + 1, ir)
        return root
    return build(0, len(preorder), 0, len(inorder))

t = build_from_pre_in([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(to_level_list(t))    # [3, 9, 20, None, None, 15, 7]
```

用哈希表记录中序中每个值的位置，避免每次线性查找；传下标而不是切片，避免复制。总复杂度 $O(n)$。

**序列化与反序列化（力扣 297）**：前序遍历，空节点记为 `#`。

```python
def serialize(root):
    out = []
    def dfs(node):
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ",".join(out)

def deserialize(s):
    it = iter(s.split(","))
    def dfs():
        v = next(it)
        if v == "#":
            return None
        node = TreeNode(int(v))
        node.left = dfs()
        node.right = dfs()
        return node
    return dfs()

s = serialize(build_tree([1, 2, 3, None, None, 4, 5]))
print(s, to_level_list(deserialize(s)))   # 1,2,#,#,3,4,#,#,5,#,# [1, 2, 3, None, None, 4, 5]
```

## 7. 其他常考题

```python
def invert(root):                         # 翻转二叉树（力扣 226）
    if root:
        root.left, root.right = invert(root.right), invert(root.left)
    return root

def is_symmetric(root):                   # 对称二叉树（力扣 101）
    def mirror(a, b):
        if a is None or b is None:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root.left, root.right) if root else True

def flatten(root):                        # 二叉树展开为链表（力扣 114），按前序
    cur = root
    while cur:
        if cur.left:
            pre = cur.left
            while pre.right:
                pre = pre.right
            pre.right = cur.right         # 右子树接到左子树最右节点后面
            cur.right, cur.left = cur.left, None
        cur = cur.right
    return root

print(to_level_list(invert(build_tree([4, 2, 7, 1, 3, 6, 9]))))   # [4, 7, 2, 9, 6, 3, 1]
print(is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3])), is_symmetric(build_tree([1, 2, 2, None, 3, None, 3])))   # True False
f = flatten(build_tree([1, 2, 5, 3, 4, None, 6]))
vals = []
while f:
    vals.append(f.val); f = f.right
print(vals)    # [1, 2, 3, 4, 5, 6]
```

## 8. 一般的树与树形 DP

笔试中更常见的是"n 个节点、n-1 条边"的无根树。用邻接表存，DFS 时传入父节点避免走回头路。

**例：树的直径**。任选一点 BFS 找到最远点 u，再从 u 出发 BFS，最远距离就是直径。下面用迭代 BFS，不受递归深度限制：

```python
from collections import deque

def tree_diameter(n, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    def bfs(src):
        dist = [-1] * n
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        far = max(range(n), key=lambda i: dist[i])
        return far, dist[far]
    u, _ = bfs(0)
    _, d = bfs(u)
    return d

print(tree_diameter(6, [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5)]))   # 4
```

**例：打家劫舍 III（力扣 337）**：相邻（父子）节点不能同时选，求最大和。每个节点返回两个值：选它时子树的最大和、不选它时的最大和。

```python
def rob(root):
    def dfs(node):
        if node is None:
            return 0, 0                       # (选, 不选)
        ls, ln = dfs(node.left)
        rs, rn = dfs(node.right)
        take = node.val + ln + rn             # 选当前节点，孩子都不能选
        skip = max(ls, ln) + max(rs, rn)      # 不选当前节点，孩子随意
        return take, skip
    return max(dfs(root))

print(rob(build_tree([3, 2, 3, None, 3, None, 1])), rob(build_tree([3, 4, 5, 1, 3, None, 1])))   # 7 9
```

这就是树形 DP 的基本形式：状态定义在子树上，按后序遍历从叶子向根计算。

### 无根树上的迭代后序

节点数达到 $10^5$ 时，递归 DFS 在 Python 里很容易爆栈。通用做法是先用栈得到一个 DFS 序，然后**倒序**处理，倒序时每个节点的孩子都已经处理过了。

**例：计算每个节点的子树大小**。

```python
def subtree_sizes(n, edges, root=0):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    parent = [-1] * n
    order = []
    st = [root]
    seen = [False] * n
    seen[root] = True
    while st:
        u = st.pop()
        order.append(u)
        for v in g[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                st.append(v)
    size = [1] * n
    for u in reversed(order):              # 孩子一定在父节点之后出现在 order 中
        if parent[u] != -1:
            size[parent[u]] += size[u]
    return size

print(subtree_sizes(6, [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5)]))   # [6, 5, 1, 3, 2, 1]

n = 200000
chain = [(i, i + 1) for i in range(n - 1)]  # 一条长链，递归写法会爆栈
print(subtree_sizes(n, chain)[0])          # 200000
```

## 练习

| 题目 | 要点 |
| --- | --- |
| 力扣 100 相同的树 | 同时递归两棵树 |
| 力扣 572 另一棵树的子树 | 每个节点判断是否相同 |
| 力扣 222 完全二叉树的节点个数 | 比较左右高度，$O(\log^2 n)$ |
| 力扣 106 从中序与后序遍历序列构造二叉树 | 后序的最后一个是根 |
| 力扣 863 二叉树中所有距离为 K 的结点 | 记录父节点，转成图做 BFS |
| 力扣 968 监控二叉树 | 树形 DP，三种状态 |
| 力扣 1372 二叉树中的最长交错路径 | 返回两个方向的长度 |
