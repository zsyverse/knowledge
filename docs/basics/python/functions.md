---
date: 2026-11-05
description: 参数的各种写法、可变默认参数的坑、作用域与闭包、函数作为对象、装饰器（计时、重试、带参数）、functools 中的 partial、lru_cache、wraps。
tags:
  - Python
---

# 函数、闭包与装饰器

## 1. 参数

```python
def train(model, lr=1e-4, *args, epochs=3, **kwargs):
    print(model, lr, args, epochs, kwargs)

train("gpt", 2e-4, "extra", epochs=5, fp16=True, seed=0)
# gpt 0.0002 ('extra',) 5 {'fp16': True, 'seed': 0}
```

- 位置参数 `model`：必须传。
- 默认参数 `lr=1e-4`：可以不传。
- `*args`：收集多余的位置参数，类型是 tuple。
- `epochs=3` 写在 `*args` 后面，只能用关键字传入（keyword-only）。
- `**kwargs`：收集多余的关键字参数，类型是 dict。

不需要 `*args`、只想强制后面的参数用关键字传入时，单独写一个 `*`：

```python
def generate(prompt, *, max_new_tokens=256, temperature=1.0):
    return f"{prompt!r} {max_new_tokens} {temperature}"

print(generate("hi", temperature=0.7))   # 'hi' 256 0.7
# generate("hi", 128)  会报 TypeError：位置参数太多
```

参数多、含义相近（几个 float）的函数，建议都用 keyword-only，调用处一眼能看出每个数字的含义，也避免传错顺序。

调用时 `*` 和 `**` 反过来用于展开：

```python
def f(a, b, c):
    return a + b + c

xs = [1, 2, 3]
cfg = {"a": 1, "b": 2, "c": 3}
print(f(*xs), f(**cfg))    # 6 6
```

把配置 dict 直接展开传给构造函数，例如 `Model(**cfg)`，是训练代码里很常见的写法。

## 2. 可变默认参数

默认参数的值在**函数定义时**计算一次，之后每次调用共享同一个对象：

```python
def append_bad(x, buf=[]):
    buf.append(x)
    return buf

print(append_bad(1))   # [1]
print(append_bad(2))   # [1, 2]，上一次调用的结果还在
```

正确写法是用 `None` 作默认值，在函数里新建：

```python
def append_ok(x, buf=None):
    if buf is None:
        buf = []
    buf.append(x)
    return buf

print(append_ok(1), append_ok(2))   # [1] [2]
```

## 3. 返回值

没有 `return` 或只写 `return` 时，返回 `None`。返回多个值实际上是返回一个 tuple。

```python
def split_xy(batch):
    return batch["x"], batch["y"]

x, y = split_xy({"x": [1, 2], "y": [0, 1]})
print(x, y)    # [1, 2] [0, 1]
```

## 4. 作用域

查找变量的顺序是 LEGB：局部（Local）→ 外层函数（Enclosing）→ 全局（Global）→ 内置（Built-in）。

```python
count = 0

def inc():
    global count     # 不声明的话，下面的赋值会让 count 变成局部变量，然后报错
    count += 1

inc(); inc()
print(count)   # 2
```

在函数里**读取**外部变量不需要声明，**赋值**才需要。尽量少用 `global`，用参数和返回值传递数据。

## 5. 闭包

内层函数引用了外层函数的变量，外层函数返回后这些变量仍然被保留，这就是闭包。

```python
def make_counter():
    n = 0
    def counter():
        nonlocal n       # 修改外层函数的变量需要 nonlocal
        n += 1
        return n
    return counter

c = make_counter()
print(c(), c(), c())   # 1 2 3
```

一个实际例子：生成学习率调度函数。

```python
import math

def cosine_with_warmup(base_lr, warmup, total):
    def lr_at(step):
        if step < warmup:
            return base_lr * (step + 1) / warmup
        progress = (step - warmup) / max(1, total - warmup)
        return base_lr * 0.5 * (1 + math.cos(math.pi * progress))
    return lr_at

sched = cosine_with_warmup(1e-3, warmup=10, total=100)
print([round(sched(s), 6) for s in (0, 9, 10, 55, 99)])
# [0.0001, 0.001, 0.001, 0.0005, 0.0]
```

`base_lr`、`warmup`、`total` 被"记住"在 `lr_at` 里，调用方只需要传 `step`。PyTorch 的 `LambdaLR` 就接受这样一个函数。

### 循环中的闭包陷阱

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])     # [2, 2, 2]

fs = [lambda i=i: i for i in range(3)]
print([f() for f in fs])     # [0, 1, 2]
```

闭包捕获的是变量本身，不是当时的值。循环结束时 `i` 是 2，所以三个函数都返回 2。用默认参数在定义时把值固定下来即可。

## 6. 函数是对象

函数可以赋值给变量、放进容器、作为参数传递、作为返回值。

```python
def relu(x): return max(0.0, x)
def identity(x): return x

ACTIVATIONS = {"relu": relu, "identity": identity}
act = ACTIVATIONS["relu"]
print(act(-2.0), act(3.0))   # 0.0 3.0
print(relu.__name__)         # relu
```

用 dict 把字符串映射到函数，是"根据配置选择实现"的标准写法，比一长串 `if/elif` 干净。

### lambda

只能写一个表达式的匿名函数，适合当一次性的 `key` 参数：

```python
pairs = [("b", 2), ("a", 3), ("c", 1)]
print(sorted(pairs, key=lambda p: p[1]))   # [('c', 1), ('b', 2), ('a', 3)]
```

`map` 和 `filter` 也接受函数，但大多数情况下推导式更清楚：

```python
nums = [1, -2, 3]
print(list(map(abs, nums)), [abs(x) for x in nums])   # [1, 2, 3] [1, 2, 3]
```

## 7. 装饰器

装饰器是一个接收函数、返回新函数的函数。`@deco` 写在函数定义上方，等价于 `f = deco(f)`。

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - t0:.3f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.1)
    return a + b

print(slow_add(1, 2))
# slow_add took 0.100s
# 3
```

`wrapper(*args, **kwargs)` 原样接收并转发所有参数，这样装饰器可以套在任何函数上。`functools.wraps` 把原函数的 `__name__`、`__doc__` 等信息复制到 `wrapper` 上，不加的话 `slow_add.__name__` 会变成 `'wrapper'`，日志和报错信息会很难看。

### 带参数的装饰器

调用模型 API 时经常需要失败重试。重试次数、等待时间需要可配置，于是装饰器本身要接收参数，多套一层：

```python
import random
import time
import functools

def retry(times=3, delay=0.5, backoff=2.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times:
                        raise
                    print(f"attempt {attempt} failed: {e}; retry in {wait:.2f}s")
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return decorator

random.seed(1)

@retry(times=4, delay=0.01, exceptions=(ConnectionError,))
def call_api(prompt):
    if random.random() < 0.6:
        raise ConnectionError("timeout")
    return f"response to {prompt!r}"

print(call_api("hello"))
# attempt 1 failed: timeout; retry in 0.01s
# response to 'hello'
```

`@retry(times=4, ...)` 先调用 `retry(...)` 得到真正的装饰器 `decorator`，再用它装饰 `call_api`。这里只捕获 `ConnectionError`，代码写错导致的 `TypeError` 之类的异常会直接抛出，不会被无意义地重试。

多个装饰器叠加时，离函数近的先作用：

```py
@a
@b
def f(): ...
# 等价于 f = a(b(f))
```

## 8. functools 中常用的几个工具

### partial：固定部分参数

```python
from functools import partial

def tokenize(text, max_len, lower):
    toks = text.lower().split() if lower else text.split()
    return toks[:max_len]

tok = partial(tokenize, max_len=3, lower=True)
print(tok("The Quick Brown Fox"))    # ['the', 'quick', 'brown']
```

`DataLoader(..., collate_fn=partial(collate, pad_id=0))` 是 `partial` 最常见的用途：`collate_fn` 只会被传入一个参数，其余参数先用 `partial` 固定。

### lru_cache：缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))             # 23416728348467685
print(fib.cache_info().hits)   # 78
```

参数必须是可哈希的。适合纯函数（同样输入总是同样输出），例如 BPE 里对同一个词反复做合并时缓存结果。缓存会一直占内存，`maxsize` 给一个上限更稳妥。

### reduce

```python
from functools import reduce
import operator
print(reduce(operator.mul, [2, 3, 4]))   # 24，计算张量元素个数时常见
```

## 9. 类型注解与文档字符串

```python
def pad(seq: list[int], length: int, pad_id: int = 0) -> list[int]:
    """把 seq 截断或补齐到 length。"""
    return (seq + [pad_id] * length)[:length]

print(pad([5, 6, 7], 5), pad([5, 6, 7], 2))   # [5, 6, 7, 0, 0] [5, 6]
print(pad.__doc__)
```

注解在运行时不做检查，传错类型照样运行，作用是给读代码的人和编辑器、类型检查工具看。详见 [模块、异常与类型注解](modules.md)。
