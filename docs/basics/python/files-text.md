---
date: 2026-11-05
description: pathlib、文件读写与编码、json / jsonl / csv / yaml / pickle、str 与 bytes、Unicode 规范化、常用字符串处理、正则表达式（含从模型输出中提取答案）、文本去重。
tags:
  - Python
---

# 文件与文本处理

大模型方向的日常工作里，有相当一部分时间在处理文本数据：清洗语料、转换格式、从模型输出里抽取答案、统计长度分布。

## 1. 路径：pathlib

```python
from pathlib import Path
import tempfile

root = Path(tempfile.mkdtemp())
out = root / "outputs" / "run1"          # 用 / 拼接路径
out.mkdir(parents=True, exist_ok=True)   # 递归创建，已存在不报错

p = out / "metrics.json"
p.write_text('{"acc": 0.9}', encoding="utf-8")
print(p.name, p.stem, p.suffix)          # metrics.json metrics .json
print(p.parent.name)                     # run1
print(p.exists(), p.is_file(), p.stat().st_size)   # True True 12
print(p.read_text(encoding="utf-8"))     # {"acc": 0.9}
print(p.with_suffix(".bak").name)        # metrics.bak

for f in sorted(root.rglob("*.json")):   # 递归查找
    print(f.relative_to(root))           # outputs/run1/metrics.json
```

比 `os.path.join` 系列函数好读，新代码建议都用 pathlib。大部分库的路径参数都同时接受 `str` 和 `Path`。

## 2. 文件读写

```python
p = root / "a.txt"
with open(p, "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("second line\n")

with open(p, encoding="utf-8") as f:
    for line in f:
        print(repr(line))
# '第一行\n'
# 'second line\n'

with open(p, "a", encoding="utf-8") as f:   # 追加
    print("third", file=f)

print(p.read_text(encoding="utf-8").splitlines())   # ['第一行', 'second line', 'third']
```

| 模式 | 含义 |
| --- | --- |
| `"r"` | 读（默认），文件不存在报错 |
| `"w"` | 写，文件存在会被**清空** |
| `"a"` | 追加到末尾 |
| `"x"` | 新建，文件已存在报错，防止误覆盖 |
| 加 `"b"` | 二进制模式，读写 `bytes` |

**始终显式写 `encoding="utf-8"`**。不写时使用系统默认编码，在 Windows 上通常是 GBK，同一段代码换台机器读中文就乱码或报 `UnicodeDecodeError`。

## 3. 数据格式

### JSON 与 JSONL

```python
import json

rec = {"prompt": "你好", "scores": [0.5, 1.0], "meta": None}
s = json.dumps(rec, ensure_ascii=False)
print(s)                      # {"prompt": "你好", "scores": [0.5, 1.0], "meta": null}
print(json.dumps(rec)[:24])   # {"prompt": "\u4f60\u597d    不加 ensure_ascii=False 时中文被转义
print(json.loads(s) == rec)   # True

with open(root / "cfg.json", "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)
with open(root / "cfg.json", encoding="utf-8") as f:
    print(json.load(f)["prompt"])   # 你好
```

`dumps`/`loads` 处理字符串，`dump`/`load` 处理文件对象。JSON 的 key 只能是字符串：`json.dumps({1: "a"})` 得到 `'{"1": "a"}'`，读回来 key 变成了 `"1"`。

训练数据通常用 JSONL：每行一个 JSON 对象。好处是可以流式读取、可以直接追加、可以用 `head`、`wc -l`、`shuf` 等命令行工具处理。

```python
def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

data = [{"id": i, "text": "x" * i} for i in range(3)]
write_jsonl(root / "d.jsonl", data)
print(read_jsonl(root / "d.jsonl") == data)    # True
```

大文件的流式读法见 [迭代器与生成器](iterators.md)。

### CSV

```python
import csv

rows = [{"model": "a", "acc": 0.71}, {"model": "b", "acc": 0.65}]
with open(root / "r.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["model", "acc"])
    w.writeheader()
    w.writerows(rows)

with open(root / "r.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row)     # 读出来的值都是字符串
# {'model': 'a', 'acc': '0.71'}
# {'model': 'b', 'acc': '0.65'}
```

不要用 `line.split(",")` 解析 CSV，字段里本身含逗号或换行时会出错。

### YAML

实验配置常用 YAML，需要安装 `pyyaml`：

```py
import yaml

with open("configs/sft.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
```

用 `safe_load`，不要用 `load`：后者可以在解析时构造任意 Python 对象。另外 YAML 1.1 会把 `1e-5` 解析成**字符串**（缺少小数点），写成 `1.0e-5` 才是浮点数，这是 PyYAML 一个很常见的坑。

### pickle

```python
import pickle

obj = {"vocab": {"a": 0}, "merges": [("a", "b")]}
with open(root / "obj.pkl", "wb") as f:
    pickle.dump(obj, f)
with open(root / "obj.pkl", "rb") as f:
    print(pickle.load(f) == obj)    # True
```

pickle 能保存几乎任何 Python 对象，但**加载不可信来源的 pickle 文件等于执行对方的代码**。这也是 `torch.load` 在新版本中默认 `weights_only=True`、以及模型权重改用 safetensors 格式的原因。

## 4. str 与 bytes

`str` 是 Unicode 字符序列，`bytes` 是字节序列。二者用编码相互转换：

```python
s = "大模型 LLM"
b = s.encode("utf-8")
print(len(s), len(b))         # 7 13，一个汉字在 UTF-8 中占 3 个字节
print(b[:3])                  # b'\xe5\xa4\xa7'
print(b.decode("utf-8"))      # 大模型 LLM
print(list("é".encode("utf-8")))   # [195, 169]
```

Byte-level BPE（GPT-2、Llama 3、Qwen 使用的 tokenizer）就是在 UTF-8 字节上做合并的，所以任何字符串都能被编码，不会出现未登录字符。

```python
print(ord("A"), chr(20320))   # 65 你
```

截断字节串可能切断一个多字节字符，解码时报错。可以用 `errors` 参数处理：

```python
broken = "你好".encode("utf-8")[:4]
print(broken.decode("utf-8", errors="ignore"))    # 你
print(broken.decode("utf-8", errors="replace"))   # 你�
```

### Unicode 规范化

看起来一样的字符串，底层的码点可能不同：

```python
import unicodedata

a = "café"                       # é 是一个码点 U+00E9
b = "café"                 # e 加上组合重音符 U+0301
print(a == b, len(a), len(b))    # False 4 5
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))   # True

print(unicodedata.normalize("NFKC", "ＡＢＣ１２３"))   # ABC123，全角转半角
```

清洗语料、做去重或精确匹配前，先统一做 NFC（或 NFKC）规范化。NFKC 会把全角字母数字、上标等"兼容字符"也转换掉，处理中文网页数据时常用。

## 5. 常用字符串处理

```python
text = "  Hello\tWorld \n\n  foo   bar  "
print(" ".join(text.split()))                     # Hello World foo bar，合并所有空白
print("abc123".isdigit(), "123".isdigit(), "abc".isalpha())   # False True True
print("Answer: 42".partition(": "))               # ('Answer', ': ', '42')
print("a/b/c".rsplit("/", 1))                     # ['a/b', 'c']
print("<think>".removeprefix("<").removesuffix(">"))   # think，3.9+
print("ab" * 3, "x".center(5, "*"))               # ababab **x**
```

`str.strip("abc")` 去掉的是首尾属于 `{'a','b','c'}` 的**任意字符**，不是去掉前缀字符串 `"abc"`。去前缀用 `removeprefix`。

```python
print("assistant: hi".strip("assistant: "))        # h，末尾的 i 也在字符集合里，被去掉了
print("tanks".strip("assistant: "))                # k
print("assistant: hi".removeprefix("assistant: ")) # hi
```

## 6. 正则表达式

```python
import re

s = "loss=2.31, acc=0.75; loss=1.98, acc=0.80"
print(re.findall(r"loss=([\d.]+)", s))                 # ['2.31', '1.98']
print(re.findall(r"(\w+)=([\d.]+)", s)[:2])            # [('loss', '2.31'), ('acc', '0.75')]

m = re.search(r"acc=(?P<acc>[\d.]+)", s)
print(m.group(0), m.group("acc"), m.span())            # acc=0.75 0.75 (11, 19)

print(re.sub(r"\s+", " ", "a  b\n\tc"))                # a b c
print(re.split(r"[,;]\s*", s))
# ['loss=2.31', 'acc=0.75', 'loss=1.98', 'acc=0.80']
```

| 写法 | 含义 |
| --- | --- |
| `.` | 除换行外的任意字符（加 `re.S` 后包含换行） |
| `\d` `\w` `\s` | 数字、单词字符（含中文）、空白 |
| `*` `+` `?` `{m,n}` | 0 次以上、1 次以上、0 或 1 次、m 到 n 次 |
| `*?` `+?` | 非贪婪：尽可能少地匹配 |
| `[abc]` `[^abc]` | 字符集合、取反 |
| `^` `$` | 开头、结尾（加 `re.M` 后按行） |
| `(...)` `(?P<name>...)` `(?:...)` | 捕获组、命名组、不捕获的组 |
| `\b` | 单词边界 |

正则字符串前面加 `r`，否则 `\b`、`\d` 等会先被 Python 当作转义处理。

### 贪婪与非贪婪

```python
html = "<b>one</b> and <b>two</b>"
print(re.findall(r"<b>(.*)</b>", html))     # ['one</b> and <b>two']
print(re.findall(r"<b>(.*?)</b>", html))    # ['one', 'two']
```

### 示例：从模型输出中提取答案

数学题的规则奖励（rule-based reward）需要从模型输出里取出最终答案。常见格式是 `\boxed{...}`，答案本身可能含有花括号，例如 `\boxed{\frac{1}{2}}`，用正则无法正确匹配嵌套括号，需要手动数括号：

```python
def extract_boxed(text):
    """返回最后一个 \\boxed{...} 中的内容，找不到返回 None。"""
    start = text.rfind("\\boxed{")
    if start == -1:
        return None
    i = start + len("\\boxed{")
    depth = 1
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i:j]
    return None   # 括号不配对

out = r"所以面积是 \boxed{\frac{1}{2}}，验证……最终答案 \boxed{\frac{\sqrt{3}}{2}}"
print(extract_boxed(out))           # \frac{\sqrt{3}}{2}
print(extract_boxed("no answer"))   # None
```

对于简单格式，正则就够了：

```python
def extract_answer(text):
    m = re.search(r"(?:答案|answer)\s*[:：是为]?\s*(-?\d+(?:\.\d+)?)", text, re.I)
    return float(m.group(1)) if m else None

print(extract_answer("推理过程……答案：-3.5"))      # -3.5
print(extract_answer("The answer is 42."))          # None，"is" 不在允许的分隔符里
```

第二个例子说明正则写得太死会漏判。写抽取规则时，一定要拿真实的模型输出批量跑一遍，统计抽取失败的比例并人工看一些失败样例，再调整规则。

### 预编译

同一个模式在循环中反复使用时，先编译：

```python
NUM = re.compile(r"-?\d+(?:\.\d+)?")
print([NUM.findall(t) for t in ["a 1 b 2.5", "x -3"]])   # [['1', '2.5'], ['-3']]
```

`re` 模块内部有缓存，不编译也不会慢太多，编译的主要好处是代码更清楚。

## 7. 示例：文本精确去重

```python
import hashlib

def norm(text):
    text = unicodedata.normalize("NFKC", text).lower()
    return " ".join(text.split())

def dedup(records, key="text"):
    seen = set()
    for r in records:
        h = hashlib.md5(norm(r[key]).encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            yield r

docs = [{"text": "Hello  World"}, {"text": "hello world"}, {"text": "ＨＥＬＬＯ world"}, {"text": "bye"}]
print([d["text"] for d in dedup(docs)])     # ['Hello  World', 'bye']
```

集合里存 32 个字符的哈希值，而不是原文，几千万条文档也能放进内存。近似去重（MinHash 等）可以识别只有少量改动的重复文档，原理不同，这里不展开。
