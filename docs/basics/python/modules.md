---
date: 2026-11-05
description: import 的查找机制、包与相对导入、__name__ == "__main__" 与 python -m、异常处理的写法、类型注解、logging、argparse 与环境变量。
tags:
  - Python
---

# 模块、异常与类型注解

## 1. 模块与 import

一个 `.py` 文件就是一个模块，一个带 `__init__.py` 的目录就是一个包。

```py
import math                        # 导入模块
import numpy as np                 # 起别名
from collections import Counter    # 导入模块中的名字
from mypkg.data import build_dataset
```

不要写 `from xxx import *`：会把一堆名字倒进当前命名空间，看不出某个函数从哪里来，还可能覆盖同名对象。

### 模块的查找路径

`import foo` 时，Python 依次在 `sys.path` 列出的目录里找 `foo.py` 或 `foo/` 目录：

```python
import sys
for p in sys.path[:3]:
    print(p)
```

`sys.path` 的第一项是**被运行脚本所在的目录**（或者交互模式下的当前目录），然后是 `PYTHONPATH` 环境变量里的目录，最后是 site-packages。由此有两个常见问题：

1. 自己的文件名和标准库或第三方库重名（例如起名 `random.py`、`torch.py`、`datasets.py`），会把真正的库遮住，`import` 到的是自己的文件。
2. 在 `scripts/train.py` 里写 `from mypkg import ...`，直接运行 `python scripts/train.py` 时找不到 `mypkg`，因为 `sys.path[0]` 是 `scripts/`。解决办法是用 `pip install -e .` 把项目装成包，或者从项目根目录用 `python -m scripts.train` 运行。

查看一个模块实际是从哪里导入的：

```python
import json
print(json.__file__)
```

### 包与相对导入

```text
mypkg/
├── __init__.py
├── data.py
└── models/
    ├── __init__.py
    ├── llama.py
    └── layers.py
```

在 `models/llama.py` 中：

```py
from .layers import RMSNorm          # 同目录
from ..data import build_dataset     # 上一级
```

相对导入只能在包内使用。含有相对导入的文件不能直接用 `python mypkg/models/llama.py` 运行，要用 `python -m mypkg.models.llama`。

`__init__.py` 会在导入包时执行，常用来把子模块里的名字提到包这一级：

```py
# mypkg/__init__.py
from .data import build_dataset
from .models.llama import LlamaModel

__all__ = ["build_dataset", "LlamaModel"]
```

这样使用者可以写 `from mypkg import LlamaModel`。

### `if __name__ == "__main__"`

模块被直接运行时 `__name__` 是 `"__main__"`，被别人 import 时是模块名。

```py
def main():
    ...

if __name__ == "__main__":
    main()
```

这样文件既能作为脚本运行，又能被 import 而不触发主逻辑。使用 `multiprocessing` 或 `DataLoader(num_workers>0)` 时，在 macOS 和 Windows 上子进程会重新导入主模块，没有这个判断，子进程在导入时又会去创建子进程，程序直接报 RuntimeError 退出。

## 2. 异常

```python
def parse_score(s):
    try:
        x = float(s)
    except ValueError:
        print(f"bad value: {s!r}")
        return None
    else:
        return x                 # try 中没有异常时执行
    finally:
        pass                     # 无论如何都会执行，一般用来释放资源

print(parse_score("0.5"), parse_score("abc"))
# bad value: 'abc'
# 0.5 None
```

### 捕获的范围要窄

```py
# 不好：任何错误都被吞掉，包括拼写错误，连 KeyboardInterrupt 也不例外
try:
    result = process(sample)
except:
    pass

# 好：只处理预料中的错误，并且留下记录
try:
    result = process(sample)
except (KeyError, json.JSONDecodeError) as e:
    logger.warning("skip sample %s: %s", sample_id, e)
```

裸 `except:` 连 `KeyboardInterrupt`（Ctrl-C）都会捕获，导致程序按 Ctrl-C 停不下来。至少写成 `except Exception:`。

数据处理脚本里，"遇到坏样本就跳过"是合理的，但要计数，最后打印跳过了多少条。坏样本比例突然变大往往意味着上游格式变了。

### 主动抛出异常

```python
def check_shape(x, expected):
    if len(x) != expected:
        raise ValueError(f"expected length {expected}, got {len(x)}")

try:
    check_shape([1, 2], 3)
except ValueError as e:
    print(e)      # expected length 3, got 2
```

报错信息里写清楚期望值和实际值，排查时能省很多时间。

在处理一个异常时抛出另一个异常，用 `raise ... from e` 保留原始原因：

```python
class ConfigError(Exception):
    pass

def load_cfg(d):
    try:
        return int(d["layers"])
    except KeyError as e:
        raise ConfigError("missing field in config") from e

try:
    load_cfg({})
except ConfigError as e:
    print(e, "<-", repr(e.__cause__))    # missing field in config <- KeyError('layers')
```

自定义异常继承 `Exception` 即可，一般不需要写任何方法。

### assert

```python
def attention_shapes(q, k):
    assert q[-1] == k[-1], f"head dim mismatch: {q} vs {k}"

attention_shapes((2, 8, 64), (2, 10, 64))
```

`assert` 用于检查"按理说不可能发生"的情况，比如 shape 是否对得上。用 `python -O` 运行时 `assert` 会被去掉，所以不要用它做用户输入的校验。

## 3. 类型注解

```python
from typing import Any, Callable, Literal, Optional, TypedDict

def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)

def find(vocab: dict[str, int], tok: str) -> int | None:     # 3.10+，等价于 Optional[int]
    return vocab.get(tok)

def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)

def set_dtype(dtype: Literal["fp32", "bf16", "fp16"]) -> None:
    ...

class Sample(TypedDict):
    prompt: str
    response: str
    reward: float

s: Sample = {"prompt": "1+1=", "response": "2", "reward": 1.0}
print(mean([1.0, 2.0]), find({"a": 1}, "b"), apply(lambda v: v * 2, 3))   # 1.5 None 6
```

| 写法 | 含义 |
| --- | --- |
| `list[int]`、`dict[str, float]`、`tuple[int, int]` | 容器及元素类型（3.9+ 可直接用内置类型） |
| `tuple[int, ...]` | 任意长度、元素都是 int 的 tuple |
| `X \| None`、`Optional[X]` | 可以是 `None` |
| `Callable[[A, B], R]` | 接收 A、B，返回 R 的函数 |
| `Literal["a", "b"]` | 只能是这几个值之一 |
| `TypedDict` | 有固定 key 的 dict |
| `Any` | 任意类型，不做检查 |

注解不影响运行。要检查，用 `mypy` 或 `pyright`（VS Code 的 Pylance 内置）。对于训练代码，注解最有价值的地方是函数签名：张量的 shape 可以写在文档字符串里，例如 `"""logits: [B, T, V]"""`。

## 4. logging

脚本里调试用 `print` 没问题，长期运行的训练和数据处理用 `logging`，可以带时间、分级别、同时写文件。

```python
import logging
import sys

def get_logger(name, log_file=None, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:            # 避免重复添加 handler 导致每行打印多次
        return logger
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    for h in handlers:
        h.setFormatter(fmt)
        logger.addHandler(h)
    return logger

logger = get_logger("train")
logger.info("step %d loss %.4f", 100, 2.3456)
logger.debug("不会显示，级别低于 INFO")
logger.warning("grad norm is %s", "nan")
# 14:03:12 INFO train: step 100 loss 2.3456
# 14:03:12 WARNING train: grad norm is nan
```

用 `logger.info("... %d", x)` 而不是 f-string，是因为日志级别不够时格式化根本不会执行。多卡训练时通常只在 rank 0 上把级别设为 INFO，其他 rank 设为 WARNING，否则每条日志会打印 N 遍。

## 5. 命令行参数

```python
import argparse

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="SFT training")
    p.add_argument("--model", required=True, help="模型路径或名称")
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--epochs", type=int, default=1)
    p.add_argument("--bf16", action="store_true", help="出现即为 True")
    p.add_argument("--target-modules", nargs="+", default=["q_proj", "v_proj"])
    p.add_argument("--scheduler", choices=["cosine", "linear", "constant"], default="cosine")
    return p.parse_args(argv)

args = parse_args(["--model", "qwen-7b", "--lr", "2e-5", "--bf16", "--target-modules", "q_proj", "k_proj"])
print(args.model, args.lr, args.bf16, args.target_modules, args.scheduler)
# qwen-7b 2e-05 True ['q_proj', 'k_proj'] cosine
```

参数名里的 `-` 会自动转成属性名里的 `_`。`parse_args(argv)` 传 `None` 时读取真实的命令行，传列表时便于测试和在 Notebook 里使用。

参数越来越多时，改成 YAML 配置文件加少量命令行覆盖，见 [文件与文本处理](files-text.md)。

## 6. 环境变量

```python
import os
rank = int(os.environ.get("RANK", 0))
world_size = int(os.environ.get("WORLD_SIZE", 1))
print(rank, world_size)
```

`torchrun` 启动分布式训练时，通过环境变量 `RANK`、`LOCAL_RANK`、`WORLD_SIZE`、`MASTER_ADDR` 把进程信息传给每个进程。API 密钥也应当通过环境变量读取，不要写进代码提交到仓库。

环境变量的值都是字符串，`os.environ.get("DEBUG")` 得到的是 `"0"` 或 `"1"`，而 `"0"` 在 `if` 里是真值，要显式比较：`os.environ.get("DEBUG") == "1"`。
