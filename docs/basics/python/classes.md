---
date: 2026-11-05
description: 类与实例、类属性、classmethod / staticmethod / property、继承与 super()、特殊方法（__getitem__、__len__、__call__ 等）、dataclass、注册器模式。读懂 Dataset 和 nn.Module 需要的面向对象知识。
tags:
  - Python
---

# 类与数据模型

PyTorch 的 `Dataset`、`nn.Module`，Hugging Face 的 `PreTrainedModel.from_pretrained`，各种框架的 `Trainer`，背后都是本章这些机制。

## 1. 定义类

```python
class Tokenizer:
    def __init__(self, vocab):
        self.vocab = vocab                          # 实例属性
        self.id2tok = {i: t for t, i in vocab.items()}

    def encode(self, text):
        return [self.vocab.get(t, self.vocab["<unk>"]) for t in text.split()]

    def decode(self, ids):
        return " ".join(self.id2tok[i] for i in ids)

tok = Tokenizer({"<unk>": 0, "hello": 1, "world": 2})
ids = tok.encode("hello big world")
print(ids, tok.decode(ids))     # [1, 0, 2] hello <unk> world
```

- `__init__` 在创建实例后自动调用，用来初始化属性。
- 方法的第一个参数 `self` 就是实例本身。`tok.encode("...")` 等价于 `Tokenizer.encode(tok, "...")`。
- 实例属性在 `__init__` 中通过 `self.xxx = ...` 创建。

## 2. 类属性与实例属性

定义在类体中、方法之外的变量是类属性，所有实例共享：

```python
class Model:
    registry_name = "base"      # 类属性
    num_instances = 0

    def __init__(self, hidden):
        self.hidden = hidden    # 实例属性
        Model.num_instances += 1

a, b = Model(128), Model(256)
print(a.registry_name, b.hidden, Model.num_instances)   # base 256 2
```

类属性不要用可变对象（list、dict）存放每个实例自己的数据，原因和可变默认参数一样：所有实例会共享同一个对象。

## 3. 三种方法

```python
class Config:
    def __init__(self, hidden, layers):
        self.hidden = hidden
        self.layers = layers

    @classmethod
    def from_dict(cls, d):
        return cls(d["hidden"], d["layers"])

    @staticmethod
    def default_hidden():
        return 768

    @property
    def num_params_approx(self):
        return 12 * self.layers * self.hidden ** 2

cfg = Config.from_dict({"hidden": 768, "layers": 12})
print(cfg.layers, Config.default_hidden(), f"{cfg.num_params_approx:,}")
# 12 768 84,934,656
```

- **普通方法**：第一个参数是实例 `self`。
- **classmethod**：第一个参数是类 `cls`，常用作"另一种构造方式"。`AutoModel.from_pretrained(path)` 就是这种写法：读取配置和权重，然后用 `cls(...)` 构造实例。用 `cls` 而不是写死类名，子类调用时得到的就是子类实例。
- **staticmethod**：不接收 `self` 也不接收 `cls`，只是放在类命名空间里的普通函数。
- **property**：把方法伪装成属性，访问时不加括号。适合由其他属性计算得到的值。

property 也可以控制赋值：

```python
class Optimizer:
    def __init__(self, lr):
        self.lr = lr          # 这里会走下面的 setter

    @property
    def lr(self):
        return self._lr

    @lr.setter
    def lr(self, value):
        if value <= 0:
            raise ValueError("lr must be positive")
        self._lr = value

opt = Optimizer(1e-3)
opt.lr = 5e-4
print(opt.lr)     # 0.0005
```

以单下划线开头的属性（`_lr`）表示"内部使用"，这只是约定，外部仍然可以访问。

## 4. 继承

```python
class BaseModel:
    def __init__(self, name):
        self.name = name

    def forward(self, x):
        raise NotImplementedError

    def __call__(self, x):
        return self.forward(x)

class Doubler(BaseModel):
    def __init__(self, name, scale=2):
        super().__init__(name)        # 先初始化父类的部分
        self.scale = scale

    def forward(self, x):
        return [v * self.scale for v in x]

m = Doubler("dbl")
print(m.name, m([1, 2, 3]))                     # dbl [2, 4, 6]
print(isinstance(m, BaseModel), issubclass(Doubler, BaseModel))   # True True
```

这正是 `nn.Module` 的结构：子类重写 `forward`，调用 `model(x)` 实际走的是父类的 `__call__`，后者在调用 `forward` 前后还会执行 hook 等逻辑。所以要写 `model(x)`，不要直接写 `model.forward(x)`。

自定义 `nn.Module` 时，`super().__init__()` 必须在给 `self` 赋值任何子模块之前调用，否则会报错：父类的 `__init__` 负责创建存放参数和子模块的内部字典。

### 方法解析顺序

多继承时，Python 按 MRO（Method Resolution Order）查找方法，`super()` 调用的是 MRO 中的下一个类，不一定是直接父类。

```python
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B>" + super().hi()
class C(A):
    def hi(self): return "C>" + super().hi()
class D(B, C):
    def hi(self): return "D>" + super().hi()

print(D().hi())                          # D>B>C>A
print([k.__name__ for k in D.__mro__])   # ['D', 'B', 'C', 'A', 'object']
```

框架里的 Mixin 类（例如 `GenerationMixin`）就是靠这个机制给模型类附加功能。自己写代码时尽量少用多继承。

## 5. 特殊方法

以双下划线开头和结尾的方法（dunder method）让自定义类支持内置语法。

| 方法 | 触发方式 |
| --- | --- |
| `__repr__` | `repr(obj)`、交互环境直接显示、`print` 在没有 `__str__` 时 |
| `__str__` | `str(obj)`、`print(obj)` |
| `__len__` | `len(obj)` |
| `__getitem__` | `obj[key]` |
| `__setitem__` | `obj[key] = v` |
| `__contains__` | `x in obj` |
| `__iter__` | `for x in obj` |
| `__call__` | `obj(...)` |
| `__eq__` / `__hash__` | `==`、放进 set 或作为 dict 的 key |
| `__add__` / `__mul__` 等 | `+`、`*` |
| `__enter__` / `__exit__` | `with obj:` |

### 写一个 Dataset

PyTorch 的 map-style 数据集只要求实现 `__len__` 和 `__getitem__`：

```python
class SFTDataset:
    def __init__(self, samples, tokenizer, max_len=8):
        self.samples = samples
        self.tok = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        s = self.samples[idx]
        ids = self.tok.encode(s["prompt"] + " " + s["response"])[: self.max_len]
        return {"input_ids": ids, "length": len(ids)}

    def __repr__(self):
        return f"SFTDataset(n={len(self)}, max_len={self.max_len})"

vocab = {"<unk>": 0, "hi": 1, "hello": 2, "how": 3, "are": 4, "you": 5}
ds = SFTDataset(
    [{"prompt": "hi", "response": "hello"}, {"prompt": "how are", "response": "you"}],
    Tokenizer(vocab),
)
print(ds)           # SFTDataset(n=2, max_len=8)
print(len(ds), ds[1])   # 2 {'input_ids': [3, 4, 5], 'length': 3}
for item in ds:
    print(item["input_ids"])
# [1, 2]
# [3, 4, 5]
```

没有定义 `__iter__` 的类也能用 `for` 遍历：Python 会退而求其次，从 0 开始依次调用 `__getitem__`，直到抛出 `IndexError`（这里由 `self.samples[idx]` 抛出）。

### `__eq__` 和 `__hash__`

```python
class Span:
    def __init__(self, start, end):
        self.start, self.end = start, end
    def __eq__(self, other):
        return isinstance(other, Span) and (self.start, self.end) == (other.start, other.end)
    def __hash__(self):
        return hash((self.start, self.end))
    def __repr__(self):
        return f"Span({self.start}, {self.end})"

print(Span(1, 3) == Span(1, 3), {Span(1, 3), Span(1, 3)})   # True {Span(1, 3)}
```

只定义 `__eq__` 不定义 `__hash__` 的话，对象会变成不可哈希，不能放进 set。相等的对象必须有相同的哈希值。

## 6. dataclass

主要用来存数据的类，用 `dataclass` 自动生成 `__init__`、`__repr__`、`__eq__`：

```python
from dataclasses import dataclass, field, asdict

@dataclass
class TrainConfig:
    model_name: str
    lr: float = 1e-5
    batch_size: int = 32
    epochs: int = 1
    target_modules: list[str] = field(default_factory=lambda: ["q_proj", "v_proj"])

    def __post_init__(self):
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")

cfg = TrainConfig("qwen-7b", lr=2e-5)
print(cfg)
# TrainConfig(model_name='qwen-7b', lr=2e-05, batch_size=32, epochs=1, target_modules=['q_proj', 'v_proj'])
print(asdict(cfg)["lr"])      # 2e-05
```

- 字段按顺序成为 `__init__` 的参数，有默认值的字段必须放在没有默认值的后面。
- 可变类型的默认值必须用 `field(default_factory=...)`，直接写 `= []` 会报错。
- `__post_init__` 在自动生成的 `__init__` 之后执行，用来做校验或计算派生字段。
- `@dataclass(frozen=True)` 让实例不可修改，同时可哈希。

Hugging Face 的 `TrainingArguments` 就是一个 dataclass，配合 `HfArgumentParser` 把命令行参数直接解析成 dataclass 实例。

## 7. 注册器模式

训练框架里经常看到 `@MODELS.register("xxx")` 这样的写法，作用是让配置文件里的字符串能映射到对应的类：

```python
class Registry:
    def __init__(self, name):
        self.name = name
        self._map = {}

    def register(self, key):
        def deco(cls):
            if key in self._map:
                raise KeyError(f"{key} already registered in {self.name}")
            self._map[key] = cls
            return cls
        return deco

    def build(self, cfg):
        cfg = dict(cfg)
        cls = self._map[cfg.pop("type")]
        return cls(**cfg)

LOSSES = Registry("loss")

@LOSSES.register("mse")
class MSE:
    def __init__(self, reduction="mean"):
        self.reduction = reduction

@LOSSES.register("ce")
class CrossEntropy:
    def __init__(self, label_smoothing=0.0):
        self.label_smoothing = label_smoothing

loss = LOSSES.build({"type": "ce", "label_smoothing": 0.1})
print(type(loss).__name__, loss.label_smoothing)    # CrossEntropy 0.1
```

装饰器同样可以作用在类上：`@LOSSES.register("ce")` 在类定义完成时把它存进字典，再原样返回。

## 8. 抽象基类

希望子类必须实现某些方法时，用 `abc`：

```python
from abc import ABC, abstractmethod

class RewardModel(ABC):
    @abstractmethod
    def score(self, prompt: str, response: str) -> float: ...

class LengthPenalty(RewardModel):
    def score(self, prompt, response):
        return -len(response) / 100

print(LengthPenalty().score("q", "a" * 50))    # -0.5
# RewardModel() 会报 TypeError：不能实例化含有抽象方法的类
```

和第 4 节里 `raise NotImplementedError` 的区别是：抽象基类在**创建实例时**就报错，而不是等到调用方法时。

## 9. `__slots__`

默认情况下每个实例用一个 dict 存属性。需要创建上百万个小对象时（例如 trie 的节点），定义 `__slots__` 可以显著节省内存：

```python
class Node:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}
        self.is_end = False

n = Node()
# n.other = 1  会报 AttributeError，只能有 __slots__ 里列出的属性
```

`@dataclass(slots=True)`（3.10+）可以自动生成 `__slots__`。
