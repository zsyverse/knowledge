---
date: 2026-11-05
description: Python 版本、虚拟环境（venv / conda / uv）、依赖管理、PyTorch 与 CUDA 的版本对应、项目目录结构，以及在 GPU 服务器上跑任务的常用操作。
tags:
  - Python
---

# 环境与工具

写代码之前先把环境搭对。大模型方向的项目依赖多、版本敏感（PyTorch、CUDA、transformers、flash-attn 之间互相有约束），环境混乱是最常见的浪费时间的来源。

## 1. Python 版本

建议使用 3.10～3.12。3.10 引入了 `match` 语句和 `X | Y` 类型写法，3.11 速度明显提升，3.12 之后新特性对日常训练代码影响不大。很多 CUDA 相关的包（如 flash-attn、某些版本的 vllm）发布 wheel 的速度比 Python 新版本慢，用最新的 Python 反而容易装不上。

查看当前解释器：

```bash
python --version
which python          # 确认用的是哪个环境里的 python
python -c "import sys; print(sys.executable)"
```

`which python` 指向的路径不是你以为的那个环境，是"明明装了包却 import 失败"的头号原因。

## 2. 虚拟环境

每个项目单独一个环境，不要往系统 Python 或 base 环境里装东西。

### venv（标准库自带）

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -U pip
pip install numpy torch
deactivate
```

### conda

conda 能管理非 Python 的依赖（比如 CUDA toolkit、MKL），在服务器上很常用。

```bash
conda create -n llm python=3.11 -y
conda activate llm
conda env list
conda remove -n llm --all      # 删除环境
```

conda 环境里装包优先用 `pip`，除非某个包只能从 conda 渠道获取。conda 和 pip 混装同一个包会导致版本冲突，且很难排查。

### uv

uv 是近两年流行的包管理工具，解析和安装速度比 pip 快一个数量级，适合依赖多的项目。

```bash
pip install uv                 # 或用官方安装脚本
uv venv --python 3.11
source .venv/bin/activate
uv pip install torch transformers
uv pip install -r requirements.txt
```

## 3. 依赖管理

最简单的做法是维护一个 `requirements.txt`，关键包写死版本：

```text
torch==2.5.1
transformers==4.46.3
datasets>=3.0
numpy<2.0
```

```bash
pip install -r requirements.txt
pip freeze > requirements.lock.txt    # 导出当前环境所有包的精确版本，便于复现
pip show torch                        # 查看某个包的版本和安装位置
```

需要把项目本身作为包安装时（例如想在任意目录 `import mypkg`），在项目根目录写 `pyproject.toml`，然后：

```bash
pip install -e .      # editable 安装，改源码立即生效，不用重装
```

开源训练框架（verl、OpenRLHF、LLaMA-Factory 等）基本都要求这样安装。

## 4. PyTorch 与 CUDA

PyTorch 的 wheel 自带 CUDA 运行时，**不需要**本机装同版本的 CUDA toolkit，只需要显卡驱动足够新。驱动支持的最高 CUDA 版本看 `nvidia-smi` 右上角。

```bash
nvidia-smi                                            # 驱动版本、显存占用
pip install torch --index-url https://download.pytorch.org/whl/cu124
python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
```

输出类似 `2.5.1+cu124 12.4 True`。`is_available()` 为 `False` 时，通常是装成了 CPU 版本（版本号后缀是 `+cpu`）或驱动太旧。

需要编译 CUDA 扩展的包（flash-attn、apex、deepspeed 的部分算子）才需要本机 CUDA toolkit，且 toolkit 的大版本要和 PyTorch 的 CUDA 版本一致。能找到预编译 wheel 就不要自己编译。

## 5. 项目目录结构

一个训练项目常见的组织方式：

```text
project/
├── pyproject.toml
├── README.md
├── configs/              # 实验配置（yaml）
│   └── sft_7b.yaml
├── src/
│   └── mypkg/
│       ├── __init__.py
│       ├── data.py       # 数据集、collate
│       ├── model.py
│       ├── trainer.py
│       └── utils.py
├── scripts/              # 启动脚本、数据预处理脚本
│   ├── train.py
│   └── run_sft.sh
├── tests/
└── outputs/              # checkpoint、日志（加入 .gitignore）
```

原则：库代码放在包里，脚本只负责解析参数和调用库；配置和代码分开；输出目录不进 git。

## 6. Jupyter

适合探索数据、调试单个函数、画图，不适合跑长时间训练。

```bash
pip install jupyterlab ipykernel
python -m ipykernel install --user --name llm   # 把当前环境注册成 kernel
jupyter lab --no-browser --port 8888
```

在远程服务器上用时，本地做端口转发：`ssh -L 8888:localhost:8888 user@server`，然后本地浏览器打开 `localhost:8888`。

常用魔法命令：

```python
%load_ext autoreload
%autoreload 2          # 修改 .py 文件后自动重新加载，不用重启 kernel
%timeit sum(range(1000))
```

## 7. 在 GPU 服务器上跑任务

### 指定显卡

```bash
CUDA_VISIBLE_DEVICES=0,1 python train.py     # 程序里只看得到 0、1 号卡，编号变成 0、1
```

### 断开 SSH 后继续运行

```bash
tmux new -s train          # 新建会话
# 在里面启动训练，然后按 Ctrl-b 再按 d 脱离
tmux ls
tmux attach -t train       # 重新连上
```

或者用 `nohup`：

```bash
nohup python train.py > train.log 2>&1 &
tail -f train.log
```

`2>&1` 把标准错误也写进日志，否则报错信息会丢。

### 查看进程与显存

```bash
nvidia-smi -l 1                # 每秒刷新
watch -n 1 nvidia-smi
ps aux | grep train.py
kill <pid>                     # 先用普通 kill，进程不退出再用 kill -9
```

## 8. 调试

最直接的调试手段是在出问题的地方插一行：

```python
breakpoint()      # 等价于 import pdb; pdb.set_trace()
```

程序运行到这里会停下，进入交互模式。常用命令：

| 命令 | 作用 |
| --- | --- |
| `p x` | 打印变量 `x` |
| `n` | 执行下一行（不进入函数） |
| `s` | 进入函数内部 |
| `c` | 继续运行到下一个断点 |
| `l` | 显示当前位置附近的代码 |
| `w` | 打印调用栈 |
| `q` | 退出 |

程序已经崩溃时，用 `python -m pdb train.py` 运行，出错后会自动停在异常现场。在多进程分布式训练中 `breakpoint()` 不好用，这时退回到在 rank 0 上打印 shape 和数值的办法：

```py
import os
if int(os.environ.get("RANK", 0)) == 0:
    print(x.shape, x.dtype, x.device)
```

VS Code 和 PyCharm 都支持远程调试，配置一次之后体验比 pdb 好很多，推荐长期使用。
