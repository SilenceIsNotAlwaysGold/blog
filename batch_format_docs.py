#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量格式化 Markdown 文档脚本
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = "/home/clouditera/xlj/markdown"
OUTPUT_DIR = "/home/clouditera/xlj/markdown-formatted"
ANALYSIS_FILE = "/home/clouditera/xlj/docs/dev/personal-blog/doc_analysis.json"
TIMESTAMP = "2026-01-26T10:00:00Z"

# 已处理的文档
PROCESSED_FILES = [
    "Mongodb.md",
    "Docker 学习指南.md",
    "MySQL数据库的基本信息.md"
]

# 标签映射
TAG_MAPPING = {
    "数据库": {
        "MySQL": ["MySQL", "数据库", "SQL"],
        "Redis": ["Redis", "缓存", "NoSQL"],
        "MongoDB": ["MongoDB", "NoSQL", "文档数据库"],
        "Elasticsearch": ["Elasticsearch", "搜索引擎", "全文检索"],
        "MariaDB": ["MariaDB", "数据库", "SQL"]
    },
    "编程语言-Python": {
        "Django": ["Django", "Python", "Web框架"],
        "Flask": ["Flask", "Python", "Web框架"],
        "FastAPI": ["FastAPI", "Python", "API"],
        "SQLAlchemy": ["SQLAlchemy", "Python", "ORM"],
        "Celery": ["Celery", "Python", "任务队列"],
        "NLTK": ["NLTK", "Python", "NLP"],
        "requests": ["Requests", "Python", "HTTP"]
    },
    "编程语言-Golang": {
        "default": ["Golang", "Go", "编程语言"]
    },
    "容器与编排": {
        "Docker": ["Docker", "容器化", "DevOps"],
        "Kafka": ["Kafka", "消息队列", "分布式"],
        "Kubernetes": ["Kubernetes", "容器编排", "K8s"]
    },
    "Web服务器": {
        "Nginx": ["Nginx", "Web服务器", "反向代理"],
        "Apache": ["Apache", "Web服务器", "HTTP"]
    },
    "Linux系统": {
        "default": ["Linux", "运维", "系统管理"]
    },
    "版本控制": {
        "Git": ["Git", "版本控制", "协作开发"]
    },
    "机器学习": {
        "default": ["机器学习", "AI", "数据科学"]
    },
    "数据分析": {
        "default": ["数据分析", "Python", "可视化"]
    },
    "其他": {
        "default": ["技术", "开发"]
    }
}


def load_analysis():
    """加载文档分析结果"""
    with open(ANALYSIS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_tags(category, filename):
    """根据分类和文件名生成标签"""
    category_tags = TAG_MAPPING.get(category, {})

    # 尝试从文件名匹配关键词
    for keyword, tags in category_tags.items():
        if keyword.lower() in filename.lower():
            return tags[:4]  # 最多返回4个标签

    # 使用默认标签
    default_tags = category_tags.get("default", ["技术", "开发"])

    # 添加分类相关的标签
    if category == "编程语言-Python":
        return ["Python"] + default_tags[:3]
    elif category == "编程语言-Golang":
        return ["Golang", "Go", "编程"]
    elif category == "数据库":
        return ["数据库", "技术"]

    return default_tags[:3]


def clean_html_tags(content):
    """删除 HTML 标签"""
    # 删除 font 标签
    content = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', content, flags=re.DOTALL)
    # 删除其他常见 HTML 标签
    content = re.sub(r'<[^>]+>', '', content)
    return content


def add_code_language(content):
    """为代码块添加语言标识"""
    lines = content.split('\n')
    result = []
    in_code_block = False

    for i, line in enumerate(lines):
        if line.strip().startswith('```') and not in_code_block:
            # 检查是否已有语言标识
            if line.strip() == '```':
                # 尝试推断语言
                next_lines = '\n'.join(lines[i+1:i+5])
                if 'SELECT' in next_lines or 'INSERT' in next_lines or 'CREATE' in next_lines:
                    result.append('```sql')
                elif 'def ' in next_lines or 'import ' in next_lines:
                    result.append('```python')
                elif 'function' in next_lines or 'const ' in next_lines or 'let ' in next_lines:
                    result.append('```javascript')
                elif 'docker' in next_lines or 'sudo' in next_lines or 'apt' in next_lines:
                    result.append('```bash')
                elif 'FROM ' in next_lines or 'RUN ' in next_lines:
                    result.append('```dockerfile')
                elif 'version:' in next_lines or 'services:' in next_lines:
                    result.append('```yaml')
                else:
                    result.append('```bash')
            else:
                result.append(line)
            in_code_block = True
        elif line.strip().startswith('```') and in_code_block:
            result.append(line)
            in_code_block = False
        else:
            result.append(line)

    return '\n'.join(result)


def clean_empty_lines(content):
    """清理多余的空行"""
    # 将连续的空行替换为最多2个空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content


def generate_summary(content, max_length=180):
    """生成文档摘要"""
    # 移除 frontmatter
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # 移除标题标记
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

    # 移除代码块
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # 移除列表标记
    content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

    # 移除链接
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

    # 移除多余空白
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()

    # 截取前面的内容作为摘要
    if len(content) > max_length:
        summary = content[:max_length]
        # 在句号或逗号处截断
        last_period = max(summary.rfind('。'), summary.rfind('，'), summary.rfind('.'))
        if last_period > max_length * 0.6:
            summary = summary[:last_period + 1]
        else:
            summary = summary + "..."
    else:
        summary = content

    return summary


def extract_title(content, filename):
    """提取文档标题"""
    # 尝试从内容中提取第一个标题
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # 从文件名提取
    title = filename.replace('.md', '').strip()
    return title


def format_document(filepath, analysis_data):
    """格式化单个文档"""
    filename = os.path.basename(filepath)

    # 跳过已处理的文档
    if filename in PROCESSED_FILES:
        print(f"跳过已处理: {filename}")
        return True

    try:
        # 读取文档
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取文档信息
        doc_info = analysis_data['results'].get(filename, {})
        category = doc_info.get('category', '其他')

        # 清理内容
        content = clean_html_tags(content)
        content = add_code_language(content)
        content = clean_empty_lines(content)

        # 提取标题和生成摘要
        title = extract_title(content, filename)
        summary = generate_summary(content)
        tags = get_tags(category, filename)

        # 生成 YAML frontmatter
        frontmatter = f"""---
title: "{title}"
summary: "{summary}"
board: "tech"
category: "{category}"
tags:
"""
        for tag in tags:
            frontmatter += f'  - "{tag}"\n'

        frontmatter += f"""author: "博主"
created_at: "{TIMESTAMP}"
updated_at: "{TIMESTAMP}"
is_published: true
---

"""

        # 移除原有的 frontmatter（如果存在）
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

        # 组合最终内容
        final_content = frontmatter + content.strip() + '\n'

        # 保存文件
        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✓ 已处理: {filename}")
        return True

    except Exception as e:
        print(f"✗ 处理失败 {filename}: {str(e)}")
        return False


def main():
    """主函数"""
    print("开始批量处理文档...")
    print(f"源目录: {SOURCE_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print()

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 加载分析数据
    analysis_data = load_analysis()

    # 获取所有 Markdown 文件
    md_files = list(Path(SOURCE_DIR).glob("*.md"))
    total = len(md_files)

    print(f"找到 {total} 个文档")
    print(f"已处理 {len(PROCESSED_FILES)} 个文档")
    print(f"待处理 {total - len(PROCESSED_FILES)} 个文档")
    print()

    # 处理每个文档
    success_count = 0
    fail_count = 0

    for filepath in md_files:
        if format_document(filepath, analysis_data):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 50)
    print(f"处理完成!")
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    print(f"总计: {total} 个")
    print("=" * 50)


if __name__ == "__main__":
    main()
