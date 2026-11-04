# 电路

「电路与模拟电子技术」中电路理论部分的学习笔记：从参考方向和基尔霍夫定律出发，经过电阻电路的等效与分析方法、电路定理，到正弦稳态、互感、三相、非正弦，最后是动态电路的时域分析。每篇都有带完整解答的例题（点开折叠框查看），所有数值都经过独立重算。

!!! note "约定"
    - 电压、电流默认取**关联参考方向**，功率按"吸收"计算。
    - 正弦量默认用 **sin 约定 + 有效值相量**：$u=\sqrt2U\sin(\omega t+\psi)\leftrightarrow\dot U=U\angle\psi$（邱关源教材用 cos 约定，只要全题统一，结果一致）。
    - 电路图中电压源上的 $+$/$-$ 为参考极性，电流源箭头为参考方向，线圈旁的 "$\bullet$" 为同名端。

## 学习路线

```mermaid
graph LR
    A[基本概念<br/>KCL / KVL] --> B[等效变换]
    B --> C[分析方法<br/>节点 / 网孔]
    C --> D[电路定理<br/>叠加 / 戴维南]
    D --> E[相量法]
    E --> F[功率与谐振]
    F --> G[互感与变压器]
    F --> H[三相电路]
    F --> I[非正弦与频率响应]
    D --> J[动态电路<br/>三要素]
    G & H & I & J --> K[题型与解题套路]
```

## 目录

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **知识点**

    ---

    11 篇，从 KCL/KVL 到动态电路，含例题

    [:octicons-arrow-right-24: 进入](notes/index.md)

-   :material-pencil-box-multiple-outline:{ .lg .middle } **习题**

    ---

    按章节配套的练习题，附答案与详细解析

    [:octicons-arrow-right-24: 进入](exercises/index.md)

</div>
