#!/usr/bin/env python3
"""
分析 Markdown 文档的脚本
- 统计文档行数和字数
- 识别文档质量（完整、简陋、只有链接）
- 按技术领域分类
- 检测重复文档
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

MARKDOWN_DIR = "/home/clouditera/xlj/markdown"

# 定义分类规则
CATEGORIES = {
    "数据库": ["mysql", "redis", "mongodb", "elasticsearch", "mariadb"],
    "编程语言-Python": ["django", "flask", "fastapi", "sqlalchemy", "celery", "requests", "nltk"],
    "编程语言-Golang": ["golang", "go"],
    "容器与编排": ["docker", "kafka"],
    "Web服务器": ["nginx", "apache"],
    "机器学习": ["学习算法", "深度学习", "聚类", "因子分析", "混淆矩阵", "模型评估", "强化学习"],
    "Linux系统": ["linux", "centos"],
    "版本控制": ["git"],
    "数据分析": ["xlsx", "绘制图表", "分析趋势"],
    "其他": []
}

def analyze_document(file_path):
    """分析单个文档"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    line_count = len(lines)
    word_count = len(content)

    # 检查是否只有链接
    has_only_links = bool(re.match(r'^\[.*\]\(.*\)\s*$', content.strip()))

    # 检查是否有实质内容
    code_blocks = len(re.findall(r'```', content))
    headers = len(re.findall(r'^#+\s', content, re.MULTILINE))

    quality = "完整"
    if has_only_links or line_count < 5:
        quality = "只有链接"
    elif line_count < 30 and code_blocks == 0:
        quality = "简陋"
    elif line_count < 50:
        quality = "需要补充"

    return {
        "line_count": line_count,
        "word_count": word_count,
        "quality": quality,
        "has_code": code_blocks > 0,
        "headers": headers
    }

def categorize_document(filename):
    """根据文件名分类文档"""
    filename_lower = filename.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category

    return "其他"

def find_duplicates(files):
    """查找可能重复的文档"""
    base_names = defaultdict(list)
    for file in files:
        # 移除 (1) 等后缀
        base_name = re.sub(r'\s*\(\d+\)', '', file)
        base_names[base_name].append(file)

    return {k: v for k, v in base_names.items() if len(v) > 1}

def main():
    # 获取所有 Markdown 文件
    md_files = sorted([f for f in os.listdir(MARKDOWN_DIR) if f.endswith('.md')])

    print(f"找到 {len(md_files)} 个 Markdown 文件\n")

    # 分析所有文档
    results = {}
    category_stats = defaultdict(list)
    quality_stats = defaultdict(list)

    for filename in md_files:
        file_path = os.path.join(MARKDOWN_DIR, filename)
        analysis = analyze_document(file_path)
        category = categorize_document(filename)

        results[filename] = {
            **analysis,
            "category": category
        }

        category_stats[category].append(filename)
        quality_stats[analysis["quality"]].append(filename)

    # 查找重复文档
    duplicates = find_duplicates(md_files)

    # 输出分类统计
    print("=" * 80)
    print("文档分类统计")
    print("=" * 80)
    for category, files in sorted(category_stats.items()):
        print(f"\n【{category}】({len(files)} 个文档)")
        for f in files[:5]:  # 只显示前5个
            print(f"  - {f} ({results[f]['line_count']} 行, {results[f]['quality']})")
        if len(files) > 5:
            print(f"  ... 还有 {len(files) - 5} 个文档")

    # 输出质量统计
    print("\n" + "=" * 80)
    print("文档质量统计")
    print("=" * 80)
    for quality, files in sorted(quality_stats.items()):
        print(f"\n【{quality}】({len(files)} 个文档)")
        for f in files:
            print(f"  - {f} ({results[f]['line_count']} 行)")

    # 输出重复文档
    if duplicates:
        print("\n" + "=" * 80)
        print("可能重复的文档")
        print("=" * 80)
        for base_name, files in duplicates.items():
            print(f"\n{base_name}:")
            for f in files:
                print(f"  - {f}")

    # 保存结果到 JSON
    output_file = "/home/clouditera/xlj/docs/dev/personal-blog/doc_analysis.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "results": results,
            "category_stats": {k: list(v) for k, v in category_stats.items()},
            "quality_stats": {k: list(v) for k, v in quality_stats.items()},
            "duplicates": duplicates
        }, f, ensure_ascii=False, indent=2)

    print(f"\n分析结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
