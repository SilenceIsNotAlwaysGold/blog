---
title: "全局变量，用于存储选择的文件路径"
summary: ""
board: "tech"
category: "数据分析"
tags:
  - "数据分析"
  - "Python"
  - "可视化"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

```python
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# 全局变量，用于存储选择的文件路径
selected_file_path = None


# GUI 界面，选择文件的功能
def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(
        title="选择一个Excel文件",
        filetypes=[("Excel 文件", "*.xlsx")]
    )
    if selected_file_path:
        file_label.config(text="已选择文件: " + os.path.basename(selected_file_path))
        start_button.config(state="normal")  # 选择文件后启用去重按钮


# 处理文件的函数
def process_file():
    global selected_file_path
    if not selected_file_path:
        messagebox.showerror("错误", "请先选择一个文件")
        return

    try:
        # 读取Excel文件
        xls = pd.ExcelFile(selected_file_path)

        # 新建一个字典存储处理后的表
        sheets_dict = {}

        # 用来记录每个图片名称首次出现的表和次数
        image_name_tracker = {}

        # 遍历所有sheet
        for sheet_name in xls.sheet_names:
            # 读取每个表的数据
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # 清理列名中的空格
            df.columns = df.columns.str.strip()

            # 删除 '标注人' 列（如果存在）
            if '标注人' in df.columns:
                df = df.drop(columns=['标注人'])

            # 检查是否有 '图片名称' 列
            if '图片名称' in df.columns:
                # 为当前 DataFrame 添加一个标记列，初始化为空
                df['标记'] = ''

                # 遍历图片名称列，检查是否重复
                for index, row in df.iterrows():
                    image_name = row['图片名称']

                    if image_name in image_name_tracker:
                        # 如果图片名称已经出现过，标记第一次出现的表名
                        first_occurrence_sheet = image_name_tracker[image_name]['表名']
                        df.at[index, '标记'] = f"重复 (首次出现于表: {first_occurrence_sheet})"
                    else:
                        # 如果图片名称是第一次出现，记录它出现的表和行
                        image_name_tracker[image_name] = {'表名': sheet_name, '行号': index}

                # 将处理后的 DataFrame 保存到字典中
                sheets_dict[sheet_name] = df
            else:
                print(f"表 '{sheet_name}' 中没有找到 '图片名称' 列")

        # 让用户选择保存文件的路径
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
            title="保存处理后的文件"
        )

        if save_path:
            # 将所有处理后的数据保存到一个新的Excel文件中
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                for sheet_name, df in sheets_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            messagebox.showinfo("成功", "数据处理完成，已保存到: " + save_path)
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出错: {e}")


# 创建GUI窗口
root = tk.Tk()
root.title("Excel 去重工具")

# 标签提示
label = tk.Label(root, text="请选择一个 Excel 文件进行去重处理：")
label.pack(pady=10)

# 显示文件名的标签
file_label = tk.Label(root, text="未选择文件")
file_label.pack(pady=10)

# 按钮选择文件
select_button = tk.Button(root, text="选择文件", command=select_file)
select_button.pack(pady=10)

# 开始去重按钮（初始为禁用状态）
start_button = tk.Button(root, text="文件保存位置", state="disabled", command=process_file)
start_button.pack(pady=10)

# 启动GUI
root.geometry("400x250")
root.mainloop()
```
