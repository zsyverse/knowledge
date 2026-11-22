---
date: 2026-11-05
description: 变量与引用、数值与字符串格式化、list / tuple / dict / set 的用法与复杂度、推导式、可变与不可变、浅拷贝与深拷贝、排序。
tags:
  - Python
---

# 数据类型与容器

## 1. 变量是名字，不是盒子

Python 的变量只是贴在对象上的名字。赋值不复制对象，只是让另一个名字指向同一个对象。

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)          # [1, 2, 3, 4]
print(a is b)     # True，同一个对象
print(id(a) == id(b))  # True
```

`==` 比较值是否相等，`is` 比较是否为同一个对象。判断 `None` 一律用 `is`：

```python
x = None
if x is None:
    print("empty")
```

## 2. 数值

`int` 没有位数上限，不会溢出；`float` 是 64 位双精度浮点数。

```python
print(2 ** 100)            # 1267650600228229401496703205376
print(0.1 + 0.2)           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)    # False
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

浮点数比较不要用 `==`，用 `math.isclose` 或者判断差的绝对值小于某个阈值。

除法相关的三个运算符：

```python
print(7 / 2)     # 3.5，真除法，结果总是 float
print(7 // 2)    # 3，向下取整
print(-7 // 2)   # -4，注意是向下取整，不是向零取整
print(7 % 3)     # 1
print(-7 % 3)    # 2，结果的符号和除数相同
print(divmod(17, 5))  # (3, 2)
```

切分数据时常用到向上取整，例如 1000 条样本、batch size 为 32 需要多少个 batch：

```python
n, bs = 1000, 32
print(math.ceil(n / bs))   # 32
print((n + bs - 1) // bs)  # 32，纯整数写法，不经过浮点
```

## 3. 字符串

字符串不可变，所有"修改"操作都返回新字符串。

```python
s = "  Hello, World  "
print(s.strip())             # 'Hello, World'
print(s.lower())             # '  hello, world  '
print("a,b,,c".split(","))   # ['a', 'b', '', 'c']
print("a b  c".split())      # ['a', 'b', 'c']，不传参数时按任意空白切分并去掉空串
print("-".join(["x", "y", "z"]))  # 'x-y-z'
print("abc".replace("b", "B"))    # 'aBc'
print("model.safetensors".endswith(".safetensors"))  # True
```

拼接大量字符串时用 `"".join(parts)`，不要在循环里 `s += x`，后者每次都创建新对象。

### f-string 格式化

```python
loss, step, lr = 0.123456, 1500, 3e-5
print(f"step {step} loss {loss:.4f} lr {lr:.2e}")   # step 1500 loss 0.1235 lr 3.00e-05
print(f"{1234567:,}")          # 1,234,567
print(f"{0.8567:.1%}")         # 85.7%
print(f"[{'ok':>6}]")          # [    ok]，右对齐，宽度 6
print(f"[{'ok':<6}]")          # [ok    ]
print(f"{7:03d}")              # 007
print(f"{loss=}")              # loss=0.123456，调试时很方便
```

格式说明符的写法是 `{值:[填充][对齐][宽度][,][.精度][类型]}`，记住上面几个就够用了。

## 4. list

list 是动态数组，按下标访问是 $O(1)$，在末尾追加是均摊 $O(1)$，在头部插入或删除是 $O(n)$。

```python
xs = [3, 1, 4, 1, 5]
xs.append(9)          # 末尾追加
xs.extend([2, 6])     # 追加多个元素
xs.insert(0, 0)       # 在下标 0 处插入
last = xs.pop()       # 弹出末尾元素
print(xs, last)       # [0, 3, 1, 4, 1, 5, 9, 2] 6
print(len(xs), xs.count(1), xs.index(4))  # 8 2 3
print(5 in xs)        # True，线性查找，O(n)
```

### 切片

`xs[start:stop:step]`，左闭右开，越界不报错。

```python
xs = list(range(10))
print(xs[2:5])     # [2, 3, 4]
print(xs[:3])      # [0, 1, 2]
print(xs[-3:])     # [7, 8, 9]
print(xs[::2])     # [0, 2, 4, 6, 8]
print(xs[::-1])    # 反转
print(xs[8:100])   # [8, 9]
```

切片返回新的 list（浅拷贝），所以 `ys = xs[:]` 是复制列表的一种写法。这一点和 NumPy 不同：NumPy 的切片返回视图，不复制数据，见 [NumPy](numpy.md)。

把数据按 9:1 划分训练集和验证集：

```python
import random
data = list(range(100))
random.seed(0)
random.shuffle(data)
k = int(len(data) * 0.9)
train, val = data[:k], data[k:]
print(len(train), len(val))  # 90 10
```

## 5. tuple 与解包

tuple 是不可变的序列，常用来返回多个值。

```python
def stats(xs):
    return min(xs), max(xs), sum(xs) / len(xs)

lo, hi, mean = stats([1, 2, 3, 4])
print(lo, hi, mean)   # 1 4 2.5

a, b = 1, 2
a, b = b, a           # 交换
first, *rest = [1, 2, 3, 4]
print(first, rest)    # 1 [2, 3, 4]
*_, last = [1, 2, 3, 4]
print(last)           # 4
```

只有一个元素的 tuple 要写逗号：`(1,)`。`(1)` 只是带括号的整数 1。PyTorch 里 `x.shape` 是 tuple 的子类，打印单维 shape 时会看到 `torch.Size([5])`，用 `(5,)` 和它比较结果为 `True`。

## 6. dict

dict 是哈希表，按 key 查找、插入、删除平均都是 $O(1)$。从 Python 3.7 起，dict 保持插入顺序。

```python
cfg = {"lr": 1e-4, "bs": 32}
cfg["epochs"] = 3
print(cfg["lr"])                 # 0.0001
print(cfg.get("warmup", 0))      # 0，key 不存在时返回默认值，不报错
print("bs" in cfg)               # True
for k, v in cfg.items():
    print(k, v)
cfg.update({"lr": 2e-4, "seed": 42})
removed = cfg.pop("seed")
print(cfg)    # {'lr': 0.0002, 'bs': 32, 'epochs': 3}

merged = {"a": 1, "b": 2} | {"b": 3}   # 3.9+，右边覆盖左边
print(merged)  # {'a': 1, 'b': 3}
```

key 必须是可哈希的（不可变类型：int、str、tuple 等），list 不能当 key。

### defaultdict 和 Counter

统计、分组时比手写 `if k not in d` 简洁：

```python
from collections import defaultdict, Counter

words = "the cat sat on the mat the end".split()

cnt = Counter(words)
print(cnt.most_common(2))   # [('the', 3), ('cat', 1)]

by_len = defaultdict(list)
for w in words:
    by_len[len(w)].append(w)
print(dict(by_len))  # {3: ['the', 'cat', 'sat', 'the', 'mat', 'the', 'end'], 2: ['on']}
```

`Counter` 支持加减：`Counter("aab") + Counter("bc")` 得到 `Counter({'a': 2, 'b': 2, 'c': 1})`。

## 7. set

集合，元素唯一，`in` 判断是 $O(1)$。需要频繁判断"是否出现过"时，一定用 set 而不是 list。

```python
seen = set()
for x in [3, 1, 3, 2, 1]:
    seen.add(x)
print(seen)                     # {1, 2, 3}

a, b = {1, 2, 3}, {2, 3, 4}
print(a & b, a | b, a - b)      # {2, 3} {1, 2, 3, 4} {1}
```

保持原顺序去重：

```python
xs = ["b", "a", "b", "c", "a"]
print(list(dict.fromkeys(xs)))  # ['b', 'a', 'c']
```

## 8. 推导式

```python
squares = [x * x for x in range(5)]                  # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]         # [0, 2, 4, 6, 8]
vocab = {w: i for i, w in enumerate(["<pad>", "a", "b"])}  # {'<pad>': 0, 'a': 1, 'b': 2}
id2tok = {i: w for w, i in vocab.items()}
lens = {len(w) for w in ["hi", "yes", "no"]}         # {2, 3}
pairs = [(i, j) for i in range(3) for j in range(i)] # [(1, 0), (2, 0), (2, 1)]
print(squares, evens, vocab, id2tok, lens, pairs)
```

多重 `for` 的顺序和写嵌套循环时一样：前面的是外层。推导式超过一行、或者嵌套两层以上时，改写成普通循环更好读。

## 9. 可变与不可变、浅拷贝与深拷贝

不可变类型：`int`、`float`、`str`、`tuple`、`frozenset`、`bytes`。可变类型：`list`、`dict`、`set`，以及大部分自定义对象。

用 `*` 初始化二维列表是一个经典错误：

```python
grid = [[0] * 3] * 2
grid[0][0] = 1
print(grid)          # [[1, 0, 0], [1, 0, 0]]，两行是同一个 list

grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 1
print(grid)          # [[1, 0, 0], [0, 0, 0]]
```

浅拷贝只复制最外层，内部元素仍然共享；深拷贝递归复制所有层：

```python
import copy

cfg = {"model": {"layers": 12}, "tags": ["a"]}
shallow = copy.copy(cfg)       # 等价于 dict(cfg) 或 cfg.copy()
deep = copy.deepcopy(cfg)

cfg["model"]["layers"] = 24
print(shallow["model"]["layers"])  # 24，被影响
print(deep["model"]["layers"])     # 12，不受影响
```

在实验脚本里基于一份基础配置派生多份配置时，用 `deepcopy`，否则改一份会把其他几份一起改掉。

## 10. 排序

`sorted()` 返回新列表，`list.sort()` 原地排序。两者都是稳定排序，都接受 `key` 和 `reverse`。

```python
samples = [
    {"id": 1, "len": 120, "score": 0.8},
    {"id": 2, "len": 30, "score": 0.9},
    {"id": 3, "len": 120, "score": 0.7},
]
by_len = sorted(samples, key=lambda s: s["len"])
print([s["id"] for s in by_len])     # [2, 1, 3]

# 先按长度降序，长度相同按分数升序
ranked = sorted(samples, key=lambda s: (-s["len"], s["score"]))
print([s["id"] for s in ranked])     # [3, 1, 2]

print(max(samples, key=lambda s: s["score"])["id"])  # 2
```

按长度排序后再分 batch，可以减少 padding，这是数据加载里常用的技巧。

## 11. 常用内置函数

```python
names = ["a", "b", "c"]
scores = [0.9, 0.5, 0.7]

for i, name in enumerate(names, start=1):
    print(i, name)

for name, s in zip(names, scores):
    print(name, s)

print(dict(zip(names, scores)))          # {'a': 0.9, 'b': 0.5, 'c': 0.7}
print(list(zip(*[(1, "x"), (2, "y")])))  # [(1, 2), ('x', 'y')]，"转置"
print(any(s > 0.8 for s in scores), all(s > 0.4 for s in scores))  # True True
print(sum(scores), round(sum(scores) / len(scores), 3))            # 2.1 0.7
```

`zip` 在长度不同时按最短的截断。希望长度不一致时报错，用 `zip(a, b, strict=True)`（3.10+），这能提前发现数据对不齐的问题。

## 12. 真值判断

以下值在 `if` 中视为假：`None`、`False`、`0`、`0.0`、空字符串、空容器（`[]`、`{}`、`set()`、`()`）。

```python
def describe(xs):
    if not xs:
        return "empty"
    return f"{len(xs)} items"

print(describe([]), describe([1, 2]))   # empty 2 items
```

注意 `if x:` 和 `if x is not None:` 的区别：当 `x = 0` 时前者为假、后者为真。函数参数默认值为 `None`、调用方可能传 0 的情况，要用后者。
