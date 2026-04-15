---
title: NumPy 数组计算与操作
summary: NumPy 是 Python 科学计算的基石。本文讲解 ndarray 数组的创建、维度操作、索引切片、广播机制以及常用的数学函数。
board: "tech"
category: 数据分析
tags:
  - Python
  - NumPy
  - 数学计算
  - 矩阵运算
author: CloudItera
created_at: 2026-01-26T10:35:00Z
updated_at: 2026-01-26T10:35:00Z
is_published: true
---

# NumPy 数组计算与操作

**NumPy** (Numerical Python) 是 Python 科学计算的基础包。几乎所有的高级数据分析库（如 Pandas, SciPy, Scikit-learn）都构建在 NumPy 之上。它的核心是 `ndarray` 对象，一个高效的多维数组。

## 1. 为什么使用 NumPy？

Python 原生的 `list` 虽然灵活，但在处理大规模数值计算时效率较低。NumPy 数组：
1. **内存连续**：存储紧凑，访问速度快。
2. **向量化运算**：避免显式循环，利用底层 C/Fortran 优化。

## 2. 数组创建

```python
import numpy as np

# 从列表创建
arr = np.array([1, 2, 3, 4, 5])

# 创建全 0 数组
zeros = np.zeros((3, 4))  # 3行4列

# 创建全 1 数组
ones = np.ones((2, 3))

# 创建序列
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace_arr = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1.0]

# 随机数组
rand_arr = np.random.rand(3, 3)  # 0-1 之间的随机数
```

## 3. 数组属性与形状操作

```python
arr = np.zeros((3, 4))

print(arr.ndim)   # 维度数：2
print(arr.shape)  # 形状：(3, 4)
print(arr.size)   # 元素总数：12
print(arr.dtype)  # 数据类型：float64

# 改变形状 (Reshape)
# 注意：reshape 前后元素总数必须一致
arr_reshaped = np.arange(12).reshape((3, 4))
```

## 4. 索引与切片

NumPy 的切片操作与 Python 列表类似，但更强大。

```python
data = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# 获取第 1 行，第 2 列的元素 (索引从 0 开始)
print(data[0, 1])  # 输出 2

# 切片：获取前两行
print(data[:2])
# [[1, 2, 3],
#  [4, 5, 6]]

# 切片：获取所有行的第 1 列
print(data[:, 0]) # [1, 4, 7]
```

## 5. 数学运算

NumPy 最大的威力在于它可以直接对数组进行数学运算（Element-wise）。

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

# 加减乘除
print(a + b)  # [11, 22, 33]
print(a * 10) # [10, 20, 30]

# 常用数学函数
print(np.sqrt(a))  # 开方
print(np.exp(a))   # 指数
print(np.sin(a))   # 正弦
```

### 聚合函数
```python
matrix = np.arange(12).reshape(3, 4)

print(matrix.sum())      # 所有元素之和
print(matrix.mean())     # 平均值
print(matrix.max(axis=0)) # 按列求最大值
print(matrix.max(axis=1)) # 按行求最大值
```

## 6. 广播机制 (Broadcasting)

广播是 NumPy 的黑魔法，它允许不同形状的数组进行算术运算。

**规则**：如果两个数组的后缘维度（trailing dimensions）的轴长度相符，或其中一方的长度为 1，则认为它们是广播兼容的。

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]]) # shape (2, 3)

scalar = 10
# 标量会广播到所有元素
print(A + scalar)

B = np.array([10, 20, 30]) # shape (3,)
# B 会在行方向上复制，变成 (2, 3) 与 A 相加
print(A + B)
# 结果：
# [[11, 22, 33],
#  [14, 25, 36]]
```

## 结语

NumPy 是通往高级数据科学的必经之路。理解了 NumPy 的数组结构和广播机制，你就能更自如地处理图像（像素矩阵）、音频（波形数组）以及各种机器学习模型的输入输出数据。
