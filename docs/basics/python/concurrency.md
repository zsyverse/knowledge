---
date: 2026-11-05
description: 进程、线程与 GIL；CPU 密集任务用 multiprocessing，IO 密集任务用线程池；asyncio 加信号量并发调用模型 API；计时、cProfile 与内存分析。
tags:
  - Python
---

# 并发与性能

两类典型场景：

- **CPU 密集**：tokenize 几亿条文本、解析大量文件、规则打分。瓶颈在计算。
- **IO 密集**：调用模型 API 做数据合成或评测、下载文件、读写网络存储。瓶颈在等待。

两类场景的解决方法不同。

## 1. 进程、线程与 GIL

CPython 有一个全局解释器锁（GIL）：同一个进程里，同一时刻只有一个线程在执行 Python 字节码。因此：

- 多**线程**不能让纯 Python 的计算变快，但在等待 IO（网络、磁盘、`time.sleep`）时线程会释放 GIL，所以多线程适合 IO 密集任务。
- 多**进程**各自有独立的解释器和 GIL，能真正并行计算，代价是进程启动慢、进程间传数据要序列化（pickle）。
- NumPy、PyTorch 的底层运算在 C/C++ 中执行时也会释放 GIL，所以多线程调用它们可以并行。

Python 3.13 开始提供去掉 GIL 的实验性构建（free-threaded），目前主流库对它的支持还不完整，日常仍按上面的规则选择。

## 2. CPU 密集：multiprocessing

```python
import time
from multiprocessing import Pool

def count_words(text):
    # 用一个刻意偏慢的纯 Python 函数模拟 tokenize
    n = 0
    for _ in range(200):
        n = len(text.split())
    return n

def main():
    texts = ["the quick brown fox jumps over the lazy dog " * 50] * 2000

    t0 = time.perf_counter()
    serial = [count_words(t) for t in texts]
    t_serial = time.perf_counter() - t0

    t0 = time.perf_counter()
    with Pool(processes=4) as pool:
        parallel = pool.map(count_words, texts, chunksize=50)
    t_par = time.perf_counter() - t0

    print(serial == parallel, f"serial {t_serial:.2f}s, 4 procs {t_par:.2f}s")

if __name__ == "__main__":
    main()
```

要点：

- 必须放在 `if __name__ == "__main__":` 下面。macOS 和 Windows 默认用 spawn 方式启动子进程，子进程会重新导入主模块。
- 传给 `pool.map` 的函数必须定义在模块顶层（lambda 和嵌套函数无法被 pickle）。
- `chunksize` 让每个子进程一次领一批任务，减少通信次数。任务很小、数量很多时，这个参数对速度影响很大。
- 结果的顺序和输入一致。不关心顺序、想尽早拿到结果时用 `pool.imap_unordered`。
- 每个任务传入和返回的数据都要经过 pickle，如果数据很大（例如整个数据集），通信开销可能超过计算本身。更好的做法是只传文件路径或下标，让子进程自己读。

Hugging Face `datasets` 的 `ds.map(fn, num_proc=8)` 内部就是这样做的。

## 3. IO 密集：线程池

```python
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch(i):
    time.sleep(0.2)          # 模拟一次网络请求
    return i, f"result-{i}"

t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = [ex.submit(fetch, i) for i in range(16)]
    results = {}
    for fut in as_completed(futures):     # 哪个先完成先处理哪个
        i, r = fut.result()               # 任务中的异常会在这里重新抛出
        results[i] = r
print(len(results), f"{time.perf_counter() - t0:.1f}s")   # 16 0.4s，串行需要 3.2s
```

`concurrent.futures` 同时提供 `ProcessPoolExecutor`，接口完全一样，把类名换掉就能切换到多进程。`ex.map(fn, items)` 是按顺序返回结果的简便写法。

## 4. asyncio：大规模并发请求

需要同时发出几百上千个请求时（比如用大模型 API 给十万条数据打标签），asyncio 比线程更轻量。

```python
import asyncio
import random

async def call_llm(prompt, sem):
    async with sem:                          # 同时最多只有 limit 个请求在进行
        await asyncio.sleep(random.uniform(0.05, 0.15))   # 模拟网络延迟
        if random.random() < 0.1:
            raise TimeoutError(prompt)
        return prompt.upper()

async def call_with_retry(prompt, sem, retries=3):
    for attempt in range(retries):
        try:
            return await call_llm(prompt, sem)
        except TimeoutError:
            await asyncio.sleep(0.05 * 2 ** attempt)
    return None

async def run_all(prompts, limit=20):
    sem = asyncio.Semaphore(limit)
    tasks = [call_with_retry(p, sem) for p in prompts]
    return await asyncio.gather(*tasks)      # 结果顺序与输入一致

random.seed(0)
prompts = [f"q{i}" for i in range(100)]
results = asyncio.run(run_all(prompts))
print(len(results), sum(r is None for r in results), results[:3])
```

- `async def` 定义协程函数，调用它得到协程对象，本身不执行。
- `await` 等待另一个协程完成；等待期间事件循环去执行其他协程。
- `asyncio.gather` 并发运行多个协程并收集结果。
- `asyncio.Semaphore` 限制并发数。不加限制一次发出上万个请求，会被服务端限流（HTTP 429）或者耗尽本地连接。
- 协程里不能调用会阻塞的函数（`time.sleep`、`requests.get`），否则整个事件循环都会停住。要用对应的异步版本：`asyncio.sleep`、`httpx.AsyncClient`、`openai.AsyncOpenAI` 等。

在 Jupyter 里事件循环已经在运行，不能用 `asyncio.run`，直接在单元格里 `await run_all(prompts)`。

### 断点续跑

长时间的批量调用一定会遇到中断。把每条结果一完成就追加写入文件，重启时跳过已完成的部分：

```py
done = {json.loads(l)["id"] for l in open(out_path)} if os.path.exists(out_path) else set()
todo = [x for x in data if x["id"] not in done]

async def worker(item, sem, f):
    result = await call_with_retry(item["prompt"], sem)
    f.write(json.dumps({"id": item["id"], "output": result}, ensure_ascii=False) + "\n")
    f.flush()
```

单线程的事件循环里，多个协程轮流执行，`f.write` 一行不会被打断，所以不需要加锁。

## 5. 计时

```python
import timeit

print(timeit.timeit("sum(range(1000))", number=10000) > 0)   # True
```

在 Jupyter 里更方便：`%timeit sum(range(1000))`。计时较长的代码段用 `time.perf_counter()`，不要用 `time.time()`（后者会受系统时间调整影响，精度也低）。

测 GPU 代码的耗时要注意：CUDA 操作是异步的，函数返回时 GPU 可能还没算完。计时前后都要调用 `torch.cuda.synchronize()`。

## 6. 找到慢的地方

不要凭感觉优化，先测量。

```python
import cProfile
import pstats

def slow():
    total = 0
    for i in range(200000):
        total += sum([i, i + 1])
    return total

def fast():
    return sum(range(10000))

def work():
    slow()
    fast()

pr = cProfile.Profile()
pr.enable()
work()
pr.disable()
stats = pstats.Stats(pr).sort_stats("cumulative")
stats.print_stats(5)       # 打印耗时最多的 5 个函数
```

命令行里对整个脚本做分析：

```bash
python -m cProfile -s cumtime script.py | head -30
```

`py-spy` 可以在不修改代码、不重启的情况下，查看一个**正在运行**的 Python 进程卡在哪里，排查训练卡住、数据加载变慢很有用：

```bash
pip install py-spy
py-spy dump --pid 12345        # 打印当前所有线程的调用栈
py-spy top --pid 12345         # 类似 top 的实时视图
```

## 7. 内存

```python
import sys
import tracemalloc

print(sys.getsizeof([]), sys.getsizeof([0] * 1000))   # 只算容器本身，不含元素

tracemalloc.start()
data = [str(i) * 10 for i in range(100000)]
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"peak {peak / 1e6:.1f} MB")
```

大规模数据处理中节省内存的常用办法：

- 用生成器流式处理，不要把整个数据集读成 list。
- 大量数值存进 NumPy 数组，而不是 Python list：一个 Python `int` 对象约占 28 字节，`np.int32` 只占 4 字节。
- 大量小对象用 `__slots__` 或 tuple，而不是 dict。
- 及时 `del` 不再使用的大对象。PyTorch 中还要注意：保留了带计算图的张量（比如把 `loss` 而不是 `loss.item()` 存进列表），会让整张计算图都无法释放。

## 8. 一些简单有效的优化

```python
import time

words = [f"w{i}" for i in range(10000)]
queries = words[::7]

as_list, as_set = words, set(words)
t0 = time.perf_counter(); sum(q in as_list for q in queries); t_list = time.perf_counter() - t0
t0 = time.perf_counter(); sum(q in as_set for q in queries); t_set = time.perf_counter() - t0
print(t_list > 50 * t_set)     # True
```

- 成员判断用 set/dict，不用 list。
- 字符串拼接用 `"".join`。
- 循环中不变的计算提到循环外；正则提前编译。
- 能用内置函数（`sum`、`max`、`sorted`）和 NumPy 的地方，不手写循环。
- 重复计算的纯函数加 `functools.lru_cache`。

这些都做了还是慢，再考虑多进程，或者把热点用 NumPy 向量化、用 Cython/Rust 重写。tokenizers 库就是 Rust 写的，比纯 Python 实现快几十倍。
