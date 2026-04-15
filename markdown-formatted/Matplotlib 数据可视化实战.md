---
title: Matplotlib 数据可视化实战
summary: Matplotlib 是 Python 最老牌的绘图库。本文从基础折线图入手，讲解散点图、柱状图的绘制，以及如何定制图例、标题、颜色和多子图布局。
board: "tech"
category: 数据分析
tags:
  - Python
  - Matplotlib
  - 数据可视化
  - 图表绘制
author: CloudItera
created_at: 2026-01-26T10:40:00Z
updated_at: 2026-01-26T10:40:00Z
is_published: true
---

# Matplotlib 数据可视化实战

一图胜千言。在数据分析中，可视化是探索数据和展示结果最直观的方式。**Matplotlib** 是 Python 中最基础也最强大的绘图库，虽然新的库（如 Seaborn, Plotly）层出不穷，但它们大多基于 Matplotlib 构建。

## 1. 基础绘图流程

标准导入方式：
```python
import matplotlib.pyplot as plt
import numpy as np

# 如果在 Jupyter Notebook 中
# %matplotlib inline
```

一个最简单的折线图：
```python
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6)) # 设置画布大小
plt.plot(x, y)              # 绘制折线
plt.show()                  # 显示图表
```

## 2. 常见图表类型

### 散点图 (Scatter Plot)
用于观察两个变量之间的关系。
```python
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 100 * np.random.rand(50)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.5)
plt.title("Random Scatter Plot")
plt.show()
```

### 柱状图 (Bar Chart)
用于比较不同类别的数值。
```python
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 12]

plt.bar(categories, values, color='skyblue')
plt.xlabel("Category")
plt.ylabel("Value")
plt.show()
```

### 直方图 (Histogram)
用于展示数据的分布情况。
```python
data = np.random.randn(1000) # 正态分布数据

plt.hist(data, bins=30, color='green', alpha=0.7)
plt.title("Histogram")
plt.show()
```

## 3. 图表定制化

默认的图表通常比较简陋，我们需要添加信息使其更具可读性。

```python
x = np.linspace(0, 10, 100)

plt.plot(x, np.sin(x), label='Sin(x)', color='blue', linestyle='--')
plt.plot(x, np.cos(x), label='Cos(x)', color='red', linestyle='-')

# 添加标题和轴标签
plt.title("Trigonometric Functions")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

# 添加图例
plt.legend(loc='upper right')

# 添加网格
plt.grid(True)

# 设置坐标轴范围
plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)

plt.show()
```

## 4. 多子图布局 (Subplots)

有时候我们需要在一张图上展示多个维度的信息。

### 使用 `plt.subplots` (推荐)
这是面向对象风格的绘图方式，更加灵活。

```python
# 创建 2行 2列 的画布
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 第一张图 (0,0)
axes[0, 0].plot(x, x**2, 'r')
axes[0, 0].set_title("Square")

# 第二张图 (0,1)
axes[0, 1].plot(x, np.sqrt(x), 'g')
axes[0, 1].set_title("Square Root")

# 第三张图 (1,0)
axes[1, 0].scatter(np.arange(10), np.random.rand(10))
axes[1, 0].set_title("Random Scatter")

# 第四张图 (1,1)
axes[1, 1].bar(['X', 'Y', 'Z'], [10, 20, 15])
axes[1, 1].set_title("Bar Chart")

# 自动调整布局，防止重叠
plt.tight_layout()
plt.show()
```

## 5. 保存图表

分析结果通常需要保存为图片以便插入报告。

```python
plt.savefig('my_analysis_plot.png', dpi=300, bbox_inches='tight')
```
- `dpi=300`：设置分辨率，300 适合打印。
- `bbox_inches='tight'`：自动裁剪掉周围多余的空白。

## 结语

Matplotlib 虽然上手稍微繁琐，但它提供了对图表元素的像素级控制。对于快速探索性分析，你也可以尝试基于 Matplotlib 封装的 **Seaborn**，它提供了更美观的默认样式和更高级的统计图表接口。
