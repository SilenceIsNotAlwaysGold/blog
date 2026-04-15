#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证格式化后的 Markdown 文档 (优化版)
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = "/home/clouditera/xlj/markdown-formatted"

def validate_frontmatter(content, filename):
    """验证 YAML frontmatter"""
    errors = []

    # 检查是否有 frontmatter
    if not content.startswith('---'):
        errors.append("缺少 YAML frontmatter")
        return errors

    # 提取 frontmatter
    try:
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            errors.append("YAML frontmatter 格式错误")
            return errors

        frontmatter_str = match.group(1)
        meta = yaml.safe_load(frontmatter_str)

        if not isinstance(meta, dict):
            errors.append("YAML frontmatter 解析后不是字典")
            return errors

    except yaml.YAMLError as e:
        errors.append(f"YAML 解析失败: {str(e)}")
        return errors

    # 检查必需字段
    required_fields = ['title', 'summary', 'board', 'category', 'tags', 'author', 'created_at', 'updated_at', 'is_published']

    for field in required_fields:
        if field not in meta:
            errors.append(f"缺少字段: {field}")

    # 检查字段值
    if meta.get('board') != 'tech':
        errors.append(f"board 字段应该是 'tech', 当前为: {meta.get('board')}")

    if meta.get('is_published') is not True:
        errors.append(f"is_published 字段应该是 true, 当前为: {meta.get('is_published')}")

    # 验证时间格式 (支持 datetime 对象或 ISO 字符串)
    for time_field in ['created_at', 'updated_at']:
        val = meta.get(time_field)
        if val is None:
            continue

        if isinstance(val, datetime):
            continue

        if isinstance(val, str):
            # 简单检查 ISO 格式
            if not re.match(r'\d{4}-\d{2}-\d{2}', val):
                errors.append(f"{time_field} 格式看似不正确: {val}")
        else:
            errors.append(f"{time_field} 类型错误: {type(val)}")

    return errors


def validate_document(filepath):
    """验证单个文档"""
    filename = os.path.basename(filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        errors = validate_frontmatter(content, filename)

        # 检查是否有 HTML 标签 (排除一些合法的如 <br>)
        if re.search(r'<font[^>]*>', content):
            errors.append("仍包含 <font> 标签")

        # 检查代码块
        # 查找 ``` 后直接换行的情况
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == '```':
                # 检查是否是代码块的结束（如果前一行有内容，或者是闭合的）
                # 简单启发式：如果前面也是 ```，或者是奇数个 ```，这里不做太复杂的解析
                # 我们主要抓开头是 ``` 但没有语言标识的

                # 这里使用正则更准确：查找 ``` 后面没有非空白字符直到换行
                pass

        # 使用正则查找 ``` 后没有任何语言标识直接换行的开始块
        # 排除处于代码块内部的情况比较复杂，这里简化处理：
        # 统计 ``` 的出现。奇数次出现时，如果后面没有字符，就是缺失语言标识

        chunks = content.split('```')
        # chunks[0] 是普通文本
        # chunks[1] 是代码块内容 (如果包含语言标识，在开头)
        # chunks[2] 是普通文本
        # ...

        for i in range(1, len(chunks), 2):
            # 这是一个代码块区域
            # 检查这个区域的开头是否包含换行符前的语言标识
            block_content = chunks[i]
            first_line = block_content.split('\n', 1)[0]
            if not first_line.strip():
                errors.append(f"第 {i//2 + 1} 个代码块缺少语言标识")

        return filename, errors

    except Exception as e:
        return filename, [f"读取文件失败: {str(e)}"]


def main():
    """主函数"""
    print("开始验证格式化后的文档 (优化版)...")
    print(f"目录: {OUTPUT_DIR}")
    print()

    # 获取所有 Markdown 文件
    md_files = list(Path(OUTPUT_DIR).glob("*.md"))

    # 排除报告文件
    md_files = [f for f in md_files if not f.name.startswith('处理报告')]

    total = len(md_files)
    print(f"找到 {total} 个文档")
    print()

    # 验证每个文档
    valid_count = 0
    invalid_count = 0
    all_errors = []

    for filepath in md_files:
        filename, errors = validate_document(filepath)

        if errors:
            invalid_count += 1
            all_errors.append((filename, errors))
            # 只显示前5个错误，避免刷屏
            # print(f"✗ {filename}")
        else:
            valid_count += 1
            # print(f"✓ {filename}")

    print()
    print("=" * 60)
    print("验证完成!")
    print(f"有效文档: {valid_count} 个")
    print(f"有问题文档: {invalid_count} 个")
    print(f"总计: {total} 个")
    print("=" * 60)

    if all_errors:
        print()
        print("问题汇总 (前 10 个):")
        for filename, errors in all_errors[:10]:
            print(f"\n{filename}:")
            for error in errors:
                print(f"  - {error}")
        if len(all_errors) > 10:
            print(f"\n... 还有 {len(all_errors) - 10} 个文件有问题")


if __name__ == "__main__":
    main()
