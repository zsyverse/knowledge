---
date: 2026-11-05
description: 可迭代对象与迭代器、生成器与 yield、惰性读取大文件、itertools 常用函数、序列打包示例、with 语句与上下文管理器、torch.no_grad 的原理。
tags:
  - Python
---

# 迭代器、生成器与上下文管理器

处理几十 GB 的语料时，不可能一次性读进内存。生成器让数据"用到时才产生"，是数据流水线的基础。

## 1. 可迭代对象与迭代器

- **可迭代对象**（iterable）：能用 `for` 遍历的对象，实现了 `__iter__`，例如 list、dict、str、文件对象。
- **迭代器**（iterator）：实现了 `__next__`，每调用一次返回下一个元素，没有元素时抛出 `StopIteration`。

```python
xs = [10, 20]
it = iter(xs)        # 调用 xs.__iter__()，得到迭代器
print(next(it))      # 10
print(next(it))      # 20
# next(it)  抛出 StopIteration
print(next(it, None))   # None，提供默认值就不会抛异常
```

`for x in xs:` 做的事情就是：先 `iter(xs)`，然后反复 `next()`，捕获到 `StopIteration` 时结束循环。

迭代器只能遍历一遍：

```python
it = iter([1, 2, 3])
print(list(it), list(it))   # [1, 2, 3] []
```

`zip`、`map`、`filter`、`enumerate`、文件对象都返回迭代器，遍历过一次就空了。需要多次使用时先转成 list。

## 2. 生成器函数

函数体里出现 `yield`，调用它就不再执行函数体，而是返回一个生成器（一种迭代器）。每次 `next()` 执行到下一个 `yield` 暂停，并把值交出去；下次从暂停处继续。

```python
def countdown(n):
    print("start")
    while n > 0:
        yield n
        n -= 1
    print("done")

g = countdown(3)
print(type(g).__name__)     # generator，此时还没有打印 start
for x in g:
    print(x)
# start
# 3
# 2
# 1
# done
```

### 惰性读取 jsonl

```python
import json
import os
import tempfile

# 先造一个示例文件
path = os.path.join(tempfile.mkdtemp(), "data.jsonl")
with open(path, "w", encoding="utf-8") as f:
    for i in range(5):
        f.write(json.dumps({"id": i, "text": f"样本 {i}"}, ensure_ascii=False) + "\n")

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        for line in f:            # 文件对象按行迭代，不会一次读入整个文件
            line = line.strip()
            if line:
                yield json.loads(line)

for rec in read_jsonl(path):
    print(rec["id"], rec["text"])
```

无论文件多大，内存里同时只有一行。

### 生成器组成流水线

每一步都是生成器，串起来之后数据逐条流过，不产生中间列表：

```python
def filter_short(records, min_len):
    for r in records:
        if len(r["text"]) >= min_len:
            yield r

def add_length(records):
    for r in records:
        yield {**r, "length": len(r["text"])}

def batched(items, size):
    batch = []
    for x in items:
        batch.append(x)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

pipe = batched(add_length(filter_short(read_jsonl(path), 2)), size=2)
for b in pipe:
    print([r["id"] for r in b])
# [0, 1]
# [2, 3]
# [4]
```

最后一个不满的 batch 是否保留，要看场景：训练时常常丢弃（对应 `DataLoader(drop_last=True)`），评测时必须保留。

### 生成器表达式

把列表推导式的方括号换成圆括号，得到生成器：

```python
total = sum(len(r["text"]) for r in read_jsonl(path))
print(total)    # 20
```

作为函数唯一的参数时，可以省掉一层括号，如上例。

### yield from

把另一个可迭代对象的元素逐个交出去：

```python
def read_many(paths):
    for p in paths:
        yield from read_jsonl(p)

print(sum(1 for _ in read_many([path, path])))   # 10
```

## 3. 自己实现迭代器类

需要在迭代过程中保存较复杂的状态，或者要支持重复遍历时，用类实现。`__iter__` 每次返回一个新的生成器，就可以遍历多次：

```python
class JsonlDataset:
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        return read_jsonl(self.path)

ds = JsonlDataset(path)
print(sum(1 for _ in ds), sum(1 for _ in ds))   # 5 5
```

PyTorch 的 `IterableDataset` 就是这个形式：实现 `__iter__`，适合流式读取、无法随机访问的数据。

## 4. itertools

```python
import itertools as it

print(list(it.islice(it.count(start=0, step=2), 5)))   # [0, 2, 4, 6, 8]，对迭代器做切片
print(list(it.chain([1, 2], [3], [4, 5])))             # [1, 2, 3, 4, 5]
print(list(it.chain.from_iterable([[1, 2], [3]])))     # [1, 2, 3]，展平一层
print(list(it.accumulate([3, 1, 4])))                  # [3, 4, 8]，前缀和
print(list(it.product([1e-4, 1e-5], [16, 32])))        # 超参数网格
# [(0.0001, 16), (0.0001, 32), (1e-05, 16), (1e-05, 32)]
print(list(it.combinations("abc", 2)))                 # [('a', 'b'), ('a', 'c'), ('b', 'c')]
print(list(it.pairwise([1, 2, 4])))                    # [(1, 2), (2, 4)]，3.10+
```

`islice` 很实用：`for x in islice(dataset, 100)` 只取前 100 条做调试。Python 3.12 起还有 `itertools.batched(iterable, n)`，功能和上面手写的 `batched` 相同，区别是每个 batch 是 tuple 而不是 list。

`groupby` 把**相邻的**相同 key 的元素分到一组，使用前通常要先按同一个 key 排序：

```python
rows = [("math", 1), ("code", 2), ("math", 3)]
rows.sort(key=lambda r: r[0])
for key, grp in it.groupby(rows, key=lambda r: r[0]):
    print(key, [v for _, v in grp])
# code [2]
# math [1, 3]
```

## 5. 示例：把文档打包成固定长度的序列

预训练时常把多篇文档首尾相接、用分隔符隔开，再切成长度为 `seq_len` 的块，以避免 padding 浪费：

```python
def pack(docs, seq_len, eos_id):
    buf = []
    for doc in docs:
        buf.extend(doc)
        buf.append(eos_id)
        while len(buf) >= seq_len:
            yield buf[:seq_len]
            buf = buf[seq_len:]

docs = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
for chunk in pack(docs, seq_len=4, eos_id=0):
    print(chunk)
# [1, 2, 3, 0]
# [4, 5, 0, 6]
# [7, 8, 9, 0]
```

这里最后不满 `seq_len` 的部分被丢弃。`buf = buf[seq_len:]` 每次都会复制剩余部分，文档很长时可以改用下标记录起点，或者用 `collections.deque`。

## 6. 上下文管理器与 with

`with` 保证资源在用完后被正确释放，即使中间出了异常：

```python
with open(path, encoding="utf-8") as f:
    first = f.readline()
print(f.closed)    # True
```

它等价于：

```py
f = open(path, encoding="utf-8")
try:
    first = f.readline()
finally:
    f.close()
```

### 用类实现

```python
import time

class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self                      # 返回值绑定到 as 后面的变量
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.t0
        print(f"[{self.name}] {self.elapsed:.3f}s")
        return False                     # False 表示不吞掉异常

with Timer("sleep") as t:
    time.sleep(0.05)
# [sleep] 0.050s
```

`__exit__` 的三个参数在没有异常时都是 `None`；有异常时是异常的类型、值和 traceback。返回 `True` 会把异常吞掉，一般不要这样做。

### 用 contextlib 实现

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        print(f"[{name}] {time.perf_counter() - t0:.3f}s")

with timer("sum"):
    s = sum(range(10**6))
```

`yield` 之前的代码相当于 `__enter__`，之后的相当于 `__exit__`。写 `try/finally` 是为了在 `with` 块内出现异常时，后半段代码仍然执行。

一个"临时修改、自动恢复"的例子：

```python
import os

@contextmanager
def env_var(key, value):
    old = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old is None:
            del os.environ[key]
        else:
            os.environ[key] = old

with env_var("TOKENIZERS_PARALLELISM", "false"):
    print(os.environ["TOKENIZERS_PARALLELISM"])   # false
print(os.environ.get("TOKENIZERS_PARALLELISM"))    # None（假设之前没有设置）
```

### torch.no_grad 是怎么工作的

`torch.no_grad()` 就是一个上下文管理器：`__enter__` 时把全局的"是否记录梯度"开关关掉，`__exit__` 时恢复原值。用同样的思路可以写出一个简化版：

```python
class Flags:
    grad_enabled = True

class no_grad:
    def __enter__(self):
        self.prev = Flags.grad_enabled
        Flags.grad_enabled = False
    def __exit__(self, *exc):
        Flags.grad_enabled = self.prev

with no_grad():
    print(Flags.grad_enabled)   # False
print(Flags.grad_enabled)       # True
```

PyTorch 里的 `torch.autocast`、`torch.inference_mode`、`model.no_sync()`（DDP 梯度累积时跳过同步）也都是这种模式。

多个上下文管理器可以写在同一个 `with` 里：

```py
with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
    logits = model(input_ids)
```
