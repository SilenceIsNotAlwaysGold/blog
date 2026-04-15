---
title: Pandas 数据处理完全指南
summary: Pandas 是 Python 数据分析的核心库。本文详细介绍了 DataFrame 的基本操作、数据读取、索引选择、分组聚合以及数据合并等核心功能。
board: "tech"
category: 数据分析
tags:
  - Python
  - Pandas
  - 数据处理
  - 数据科学
author: CloudItera
created_at: 2026-01-26T10:30:00Z
updated_at: 2026-01-26T10:30:00Z
is_published: true
---

# Pandas 数据处理完全指南

在 Python 数据分析生态中，**Pandas** 无疑是占据统治地位的工具。它提供了名为 DataFrame 的强大数据结构，让像 Excel 表格一样的结构化数据处理变得极其简单和高效。

## 1. 快速入门

首先，确保已安装 Pandas：
```bash
pip install pandas
```

导入库（通常习惯重命名为 `pd`）：
```python
import pandas as pd
import numpy as np
```

### 创建 DataFrame
```python
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Paris', 'London', 'Tokyo']
}
df = pd.DataFrame(data)
print(df)
```

## 2. 数据读取与导出

Pandas 支持极其丰富的文件格式。

```python
# 读取 CSV
df = pd.read_csv('data.csv')

# 读取 Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 读取 SQL
# df = pd.read_sql(query, connection)

# 导出数据
df.to_csv('output.csv', index=False)
```

## 3. 数据查看与探查

拿到数据的第一步是了解数据。

```python
# 查看前 5 行
print(df.head())

# 查看数据摘要（行数、列类型、非空值数量）
print(df.info())

# 查看数值列的统计信息（均值、标准差、最大最小值）
print(df.describe())

# 查看列名
print(df.columns)
```

## 4. 数据选择与过滤 (Indexing & Selection)

这是 Pandas 最核心的操作之一。

### 选择列
```python
# 选择单列（返回 Series）
ages = df['Age']

# 选择多列（返回 DataFrame）
subset = df[['Name', 'City']]
```

### `loc` vs `iloc`
- **`loc`**：基于**标签 (Label)** 的索引。
- **`iloc`**：基于**位置 (Integer position)** 的索引。

```python
# loc 示例
# 选择索引为 0 的行的 'Name' 列
print(df.loc[0, 'Name'])
# 选择所有行的 'Name' 和 'Age' 列
print(df.loc[:, ['Name', 'Age']])

# iloc 示例
# 选择第一行
print(df.iloc[0])
# 选择前 3 行，前 2 列
print(df.iloc[:3, :2])
```

### 条件过滤
```python
# 筛选年龄大于 30 的人
older_than_30 = df[df['Age'] > 30]

# 组合条件 (注意要用括号和位运算符 & |)
result = df[(df['Age'] > 25) & (df['City'] == 'Paris')]
```

## 5. 数据处理与转换

```python
# 新增一列
df['Is_Senior'] = df['Age'] > 50

# Apply 函数：对列中每个元素应用函数
df['Name_Length'] = df['Name'].apply(len)

# 排序
df_sorted = df.sort_values(by='Age', ascending=False)
```

## 6. 分组与聚合 (Group By)

类似 SQL 的 `GROUP BY` 操作。

```python
# 假设有一个 'Department' 列
# 按部门分组，计算平均年龄
avg_age_by_dept = df.groupby('Department')['Age'].mean()

# 多个聚合函数
stats = df.groupby('Department').agg({
    'Age': ['mean', 'max'],
    'Salary': 'sum'
})
```

## 7. 数据合并

- **`merge`**：类似 SQL Join (inner, outer, left, right)。
- **`concat`**：物理拼接（上下或左右）。

```python
# Merge
merged_df = pd.merge(df1, df2, on='user_id', how='left')

# Concat (上下拼接)
combined_df = pd.concat([df_2023, df_2024], axis=0)
```

## 结语

Pandas 的功能远不止于此，它还支持时间序列分析、透视表 (Pivot Table) 等高级功能。熟练掌握 Pandas，是成为数据分析师的第一步，它能让你从繁琐的数据整理工作中解脱出来，专注于挖掘数据背后的价值。
