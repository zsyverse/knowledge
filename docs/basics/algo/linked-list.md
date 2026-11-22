---
date: 2026-11-05
description: 链表节点的定义与 ACM 模式下的构建和打印、哑节点、反转（整体、区间、K 个一组）、快慢指针（中点、环、倒数第 k 个）、合并与排序、LRU 缓存。
tags:
  - 算法
---

# 链表

链表题考的是指针操作的细心程度。几乎所有题都能用三个工具解决：**哑节点**、**反转**、**快慢指针**。

## 1. 节点定义与构建

力扣给出的定义：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

ACM 模式下题目只给一串数字，链表要自己建，输出时也要自己遍历打印。写两个辅助函数，后面所有例题都用它们测试：

```python
def build(vals):
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

print(to_list(build([1, 2, 3])))   # [1, 2, 3]
```

一道完整的 ACM 题：第一行 n，第二行 n 个数构成链表，输出反转后的链表。

```python
import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    dummy = cur = ListNode()
    for x in data[1:1 + n]:
        cur.next = ListNode(int(x))
        cur = cur.next
    head = reverse(dummy.next)
    out = []
    while head:
        out.append(str(head.val))
        head = head.next
    print(" ".join(out))

main()
```

输入

```text
5
1 2 3 4 5
```

输出

```text
5 4 3 2 1
```

不少笔试题其实只是"用链表包装的数组题"。ACM 模式下如果题目没有限制，把数据直接放进 list 处理也能通过；但面试手撕时面试官要看的就是指针操作。

## 2. 哑节点

头节点可能被删除或改变时，在前面加一个哑节点（dummy），所有节点就都有前驱了，不用对头节点特判。最后返回 `dummy.next`。

**例：移除链表元素（力扣 203）**。

```python
def remove_elements(head, val):
    dummy = ListNode(0, head)
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next      # 删除 cur.next，cur 不动
        else:
            cur = cur.next
    return dummy.next

print(to_list(remove_elements(build([7, 7, 1, 7, 2]), 7)))   # [1, 2]
```

**例：删除排序链表中的重复元素 II（力扣 82）**。只要重复，就全部删掉。

```python
def delete_duplicates(head):
    dummy = ListNode(0, head)
    cur = dummy
    while cur.next and cur.next.next:
        if cur.next.val == cur.next.next.val:
            v = cur.next.val
            while cur.next and cur.next.val == v:
                cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next

print(to_list(delete_duplicates(build([1, 2, 3, 3, 4, 4, 5]))))   # [1, 2, 5]
```

## 3. 反转

### 整体反转（力扣 206）

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next     # 先保存下一个节点
        cur.next = prev    # 反转指针
        prev = cur
        cur = nxt
    return prev

print(to_list(reverse_list(build([1, 2, 3, 4]))))   # [4, 3, 2, 1]
```

递归写法：

```python
def reverse_rec(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_rec(head.next)
    head.next.next = head      # 让后一个节点指回自己
    head.next = None
    return new_head

print(to_list(reverse_rec(build([1, 2, 3]))))   # [3, 2, 1]
```

### 反转区间 [left, right]（力扣 92）

找到区间前一个节点 `p0`，把区间内的节点逐个"头插"到 `p0` 后面。

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    p0 = dummy
    for _ in range(left - 1):
        p0 = p0.next
    cur = p0.next
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = p0.next
        p0.next = nxt
    return dummy.next

print(to_list(reverse_between(build([1, 2, 3, 4, 5]), 2, 4)))   # [1, 4, 3, 2, 5]
```

### K 个一组反转（力扣 25）

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    p0 = dummy
    while True:
        tail = p0
        for _ in range(k):          # 检查剩余节点是否够 k 个
            tail = tail.next
            if tail is None:
                return dummy.next
        nxt_group = tail.next
        prev, cur = nxt_group, p0.next
        for _ in range(k):          # 反转这一组，反转后组尾接上下一组
            cur.next, prev, cur = prev, cur, cur.next
        first = p0.next             # 反转前的组首，现在是组尾
        p0.next = prev
        p0 = first

print(to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 2)))   # [2, 1, 4, 3, 5]
print(to_list(reverse_k_group(build([1, 2, 3, 4, 5]), 3)))   # [3, 2, 1, 4, 5]
```

`cur.next, prev, cur = prev, cur, cur.next` 这种一行写法：右边三个值先全部算好，再依次赋给左边。它等价于前面用 `nxt` 临时变量的四行写法。

## 4. 快慢指针

### 中间节点（力扣 876）

慢指针每次一步，快指针每次两步，快指针到达末尾时慢指针在中间。

```python
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

print(middle(build([1, 2, 3, 4, 5])).val, middle(build([1, 2, 3, 4])).val)   # 3 3
```

偶数个节点时返回的是中间两个里靠后的那个。

### 环形链表（力扣 141、142）

有环时快指针一定会追上慢指针。相遇后，把一个指针放回头节点，两个指针都每次走一步，再次相遇的位置就是环的入口。

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p = p.next
                slow = slow.next
            return p
    return None

nodes = [ListNode(i) for i in range(6)]
for a, b in zip(nodes, nodes[1:]):
    a.next = b
nodes[-1].next = nodes[2]          # 5 -> 2，构成环
print(detect_cycle(nodes[0]).val, detect_cycle(build([1, 2])))   # 2 None
```

为什么能找到入口：设头到入口距离 $a$，入口到相遇点距离 $b$，环长 $c$。相遇时慢指针走了 $a+b$，快指针走了 $2(a+b)$，多走的 $a+b$ 是环长的整数倍，即 $a + b = kc$，所以 $a = kc - b$：从相遇点再走 $a$ 步恰好回到入口。

### 删除倒数第 N 个节点（力扣 19）

快指针先走 n 步，然后两个指针一起走，快指针到末尾时慢指针指向倒数第 n+1 个节点。

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next

print(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))   # [1, 2, 3, 5]
print(to_list(remove_nth_from_end(build([1]), 1)))               # []
```

### 回文链表（力扣 234）

找中点，反转后半段，再和前半段逐个比较。综合使用了快慢指针和反转。

```python
def is_palindrome(head):
    mid = middle(head)
    second = reverse_list(mid)
    p, q = head, second
    while q:
        if p.val != q.val:
            return False
        p, q = p.next, q.next
    return True

print(is_palindrome(build([1, 2, 2, 1])), is_palindrome(build([1, 2, 3])))   # True False
```

## 5. 合并与排序

### 合并两个有序链表（力扣 21）

```python
def merge_two(a, b):
    dummy = cur = ListNode()
    while a and b:
        if a.val <= b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next

print(to_list(merge_two(build([1, 2, 4]), build([1, 3, 4]))))   # [1, 1, 2, 3, 4, 4]
```

### 合并 K 个有序链表（力扣 23）

用小根堆保存每个链表当前的头节点。节点对象不能比较大小，堆里放 `(值, 序号, 节点)`。

```python
import heapq

def merge_k(lists):
    h = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(h)
    dummy = cur = ListNode()
    while h:
        _, i, node = heapq.heappop(h)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next

print(to_list(merge_k([build([1, 4, 5]), build([1, 3, 4]), build([2, 6])])))
# [1, 1, 2, 3, 4, 4, 5, 6]
```

复杂度 $O(N \log k)$，$N$ 是节点总数。

### 排序链表（力扣 148）

归并排序：找中点断开，两边分别排序，再合并。

```python
def sort_list(head):
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next          # fast 从 head.next 出发，偶数长度时 slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    right = slow.next
    slow.next = None
    return merge_two(sort_list(head), sort_list(right))

print(to_list(sort_list(build([4, 2, 1, 3, -1, 5, 0]))))   # [-1, 0, 1, 2, 3, 4, 5]
```

这里 `fast` 必须从 `head.next` 出发。如果从 `head` 出发，两个节点的链表中 `slow` 会停在第二个节点，`right` 为空，左半边仍是两个节点，无限递归。

## 6. 其他常考题

### 相交链表（力扣 160）

两个指针分别走完自己的链表后换到对方的链表头继续走，走过的总长度相同，会在交点相遇；没有交点时同时变成 `None`。

```python
def get_intersection(a, b):
    p, q = a, b
    while p is not q:
        p = p.next if p else b
        q = q.next if q else a
    return p

common = build([8, 4, 5])
a = ListNode(4, ListNode(1, common))
b = ListNode(5, ListNode(6, ListNode(1, common)))
print(get_intersection(a, b).val, get_intersection(build([1]), build([2])))   # 8 None
```

### 两数相加（力扣 2）

逆序存储的两个数相加，注意最后的进位。

```python
def add_two_numbers(a, b):
    dummy = cur = ListNode()
    carry = 0
    while a or b or carry:
        s = carry + (a.val if a else 0) + (b.val if b else 0)
        carry, d = divmod(s, 10)
        cur.next = ListNode(d)
        cur = cur.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next

print(to_list(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))))   # [7, 0, 8]
print(to_list(add_two_numbers(build([9, 9]), build([1]))))            # [0, 0, 1]
```

### LRU 缓存（力扣 146）

面试最高频的设计题之一。要求 `get` 和 `put` 都是 $O(1)$：哈希表负责按 key 找到节点，双向链表负责维护使用顺序（最近使用的放在头部，容量满时删除尾部）。

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = Node()             # 哨兵：head.next 是最近使用的
        self.tail = Node()             # 哨兵：tail.prev 是最久未使用的
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]      # 节点里存 key，就是为了这里能删掉哈希表中的项
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)

c = LRUCache(2)
c.put(1, 1); c.put(2, 2)
print(c.get(1))       # 1
c.put(3, 3)           # 淘汰 key 2
print(c.get(2))       # -1
c.put(4, 4)           # 淘汰 key 1
print(c.get(1), c.get(3), c.get(4))   # -1 3 4
```

Python 里也可以用 `collections.OrderedDict` 的 `move_to_end` 和 `popitem(last=False)` 几行写完，笔试中可以这样做；但面试时一般要求手写双向链表。

```python
from collections import OrderedDict

class LRUCache2:
    def __init__(self, capacity):
        self.cap, self.d = capacity, OrderedDict()
    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)
        return self.d[key]
    def put(self, key, value):
        self.d[key] = value
        self.d.move_to_end(key)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)

c = LRUCache2(2)
c.put(1, 1); c.put(2, 2); c.get(1); c.put(3, 3)
print(c.get(2), c.get(1))   # -1 1
```

## 练习

| 题目 | 要点 |
| --- | --- |
| 力扣 24 两两交换链表中的节点 | K 个一组反转的特例 |
| 力扣 61 旋转链表 | 先连成环，再在合适位置断开 |
| 力扣 86 分隔链表 | 两个哑节点分别收集 |
| 力扣 143 重排链表 | 中点 + 反转后半段 + 交替合并 |
| 力扣 138 随机链表的复制 | 哈希表映射旧节点到新节点 |
| 力扣 328 奇偶链表 | 两个指针分别串起奇偶节点 |
