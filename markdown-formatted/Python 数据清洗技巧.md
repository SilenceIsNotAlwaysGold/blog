---
title: Python 数据清洗技巧
summary: 真实世界的数据往往是"脏"的。本文总结了 Python 数据清洗的常见技巧，包括处理缺失值、去除重复项、异常值检测与处理以及数据类型转换。
board: "tech"
category: 数据分析
tags:
  - Python
  - Pandas
  - 数据清洗
  - 预处理
author: CloudItera
created_at: 2026-01-26T10:45:00Z
updated_at: 2026-01-26T10:45:00Z
is_published: true
---

# Python 数据清洗技巧

数据科学家 80% 的时间都花在清洗和准备数据上。Garbage In, Garbage Out（垃圾进，垃圾出）是数据分析界的至理名言。本文将介绍如何使用 Pandas 进行高效的数据清洗。

## 1. 缺失值处理 (Missing Values)

数据集中常出现 `NaN`, `None` 或空字符串。

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': ['foo', 'bar', 'baz', None]
})

# 1. 检查缺失值
print(df.isnull().sum())
# A    1
# B    2
# C    1

# 2. 删除包含缺失值的行
df_dropped = df.dropna()
# 默认删除任何包含 NaN 的行。使用 how='all' 仅删除全为空的行。

# 3. 填充缺失值
# 用常数填充
df['A'] = df['A'].fillna(0)

# 用均值/中位数填充
mean_b = df['B'].mean()
df['B'] = df['B'].fillna(mean_b)

# 前向填充 (用前一个有效值填充)
df.fillna(method='ffill', inplace=True)
```

## 2. 重复数据处理 (Duplicates)

```python
# 检查重复行
duplicates = df.duplicated()
print(f"重复行数: {duplicates.sum()}")

# 删除重复行
# keep='first' 保留第一个，'last' 保留最后一个，False 删除所有重复的
df.drop_duplicates(subset=['A', 'C'], keep='first', inplace=True)
```

## 3. 数据类型转换

有时读取 CSV 后，数字可能被识别为字符串，或者日期列是对象类型。

```python
# 查看类型
print(df.dtypes)

# 转换为数值类型 (强制转换，无法转换的变为 NaN)
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 转换为日期类型
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# 类型转换 (astype)
df['category_code'] = df['category_code'].astype(int)
df['status'] = df['status'].astype('category') # 节省内存
```

## 4. 字符串处理

Pandas 的 `str` 访问器提供了强大的字符串操作功能。

```python
# 去除首尾空格
df['name'] = df['name'].str.strip()

# 统一大小写
df['email'] = df['email'].str.lower()

# 字符串分割
# "New York, USA" -> ["New York", "USA"]
df[['City', 'Country']] = df['Location'].str.split(',', expand=True)

# 字符串替换
df['price'] = df['price'].str.replace('$', '').astype(float)
```

## 5. 异常值检测与处理 (Outliers)

异常值会严重歪曲统计结果。

### 方法一：Z-Score (标准分数)
假定数据符合正态分布，超过 3 倍标准差的值视为异常。

```python
from scipy import stats

z_scores = np.abs(stats.zscore(df['value']))
# 保留 Z-score 小于 3 的数据
df_clean = df[(z_scores < 3)]
```

### 方法二：IQR (四分位距)
更鲁棒的方法，适用于偏态分布。

```python
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 筛选正常范围内的数据
df_clean = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]
```

## 6. 数据标准化 (Normalization)

在机器学习中，通常需要将不同量纲的数据缩放到同一范围。

```python
# Min-Max 归一化 (缩放到 0-1)
df['scaled'] = (df['value'] - df['value'].min()) / (df['value'].max() - df['value'].min())

# Z-Score 标准化 (均值 0，方差 1)
df['standardized'] = (df['value'] - df['value'].mean()) / df['value'].std()
```

## 结语

数据清洗没有固定的标准流程，它需要结合对业务的理解。比如，某个传感器读数为 0 是代表"零值"还是"故障"？这需要领域知识来判断。掌握上述 Pandas 技巧，将为你处理杂乱数据提供强大的工具箱。
