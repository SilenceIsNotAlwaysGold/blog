#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复 Markdown 文档格式问题
"""

import os
import re
import yaml
from pathlib import Path

OUTPUT_DIR = "/home/clouditera/xlj/markdown-formatted"

def fix_content(content, filename):
    """修复单个文件的内容"""
    original_content = content
    modified = False

    # 1. 修复 YAML Frontmatter
    if content.startswith('---'):
        try:
            # 提取 frontmatter 部分
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if match:
                frontmatter_str = match.group(1)

                # 简单字符串替换修复，避免重新序列化破坏格式
                new_frontmatter = frontmatter_str

                # 修复 board
                if 'board: 技术' in new_frontmatter or "board: '技术'" in new_frontmatter or 'board: "技术"' in new_frontmatter:
                    new_frontmatter = re.sub(r'board: .*', 'board: "tech"', new_frontmatter)
                    modified = True

                # 修复 is_published
                if 'is_published: false' in new_frontmatter.lower():
                    new_frontmatter = re.sub(r'is_published: .*', 'is_published: true', new_frontmatter, flags=re.IGNORECASE)
                    modified = True

                if modified:
                    content = content.replace(frontmatter_str, new_frontmatter)
        except Exception as e:
            print(f"处理 Frontmatter 出错 {filename}: {e}")

    # 2. 修复缺失语言标识的代码块
    # 查找 ``` 后直接换行的情况
    lines = content.split('\n')
    new_lines = []
    in_code_block = False

    for i, line in enumerate(lines):
        if line.strip() == '```':
            if not in_code_block:
                # 代码块开始
                # 检查是否缺失语言
                # 简单的上下文推断
                lang = "bash" # 默认

                # 检查前几行是否有提示
                prev_lines = lines[max(0, i-3):i]
                prev_text = "\n".join(prev_lines).lower()

                if "python" in prev_text or ".py" in prev_text:
                    lang = "python"
                elif "sql" in prev_text:
                    lang = "sql"
                elif "go" in prev_text or "golang" in prev_text:
                    lang = "go"
                elif "yaml" in prev_text or "yml" in prev_text:
                    lang = "yaml"
                elif "json" in prev_text:
                    lang = "json"
                elif "html" in prev_text:
                    lang = "html"
                elif "docker" in prev_text:
                    lang = "dockerfile"
                elif "nginx" in prev_text:
                    lang = "nginx"

                new_lines.append(f"```{lang}")
                in_code_block = True
                modified = True
            else:
                # 代码块结束
                new_lines.append("```")
                in_code_block = False
        elif line.strip().startswith('```'):
            # 已有语言标识，或者其他情况
            new_lines.append(line)
            if not in_code_block:
                in_code_block = True
            else:
                in_code_block = False
        else:
            new_lines.append(line)

    if modified:
        content = "\n".join(new_lines)

    # 3. 特殊修复：聚类数量的确认.md 的 YAML 问题
    if filename == "聚类数量的确认.md":
        # 修复引号嵌套问题
        if 'summary:' in content:
            # 简单粗暴修复：重新构建这个文件的头
             content = re.sub(r'summary: .*?\n', 'summary: "K-means聚类算法中K值的确定方法，重点介绍手肘法（Elbow Method）的原理和应用。"\n', content)
             modified = True

    return content, modified

def main():
    print("开始批量修复文档...")
    count = 0

    md_files = list(Path(OUTPUT_DIR).glob("*.md"))

    for filepath in md_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content, modified = fix_content(content, filepath.name)

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已修复: {filepath.name}")
                count += 1

        except Exception as e:
            print(f"处理文件失败 {filepath.name}: {e}")

    print(f"修复完成，共修改了 {count} 个文件")

if __name__ == "__main__":
    main()
