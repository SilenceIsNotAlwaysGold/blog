# 博客文章格式规范

## 文章结构

每篇文章应包含以下部分：

### 1. YAML Frontmatter（必需）

```yaml
---
title: "文章标题"
summary: "文章摘要（100-200字）"
board: "tech"  # life 或 tech
category: "数据库"  # 分类名称
tags:
  - "MySQL"
  - "数据库优化"
cover_image: ""  # 封面图 URL（可选）
author: "博主名称"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---
```

### 2. 文章正文（Markdown）

- 使用标准 Markdown 语法
- 代码块必须指定语言
- 不使用 HTML 标签（除非必要）
- 图片使用 Markdown 语法

## 分类体系

### 技术板块（tech）分类

- **数据库**：MySQL, Redis, MongoDB, Elasticsearch 等
- **编程语言-Python**：Django, Flask, FastAPI, SQLAlchemy 等
- **编程语言-Golang**：Go 基础、并发、Web 开发等
- **容器与编排**：Docker, Kubernetes, Kafka 等
- **Web服务器**：Nginx, Apache 等
- **机器学习**：监督学习、深度学习、NLP 等
- **Linux系统**：CentOS, Ubuntu, Shell 脚本等
- **版本控制**：Git 操作、工作流等
- **数据分析**：数据处理、可视化等
- **其他**：其他技术主题

### 生活板块（life）分类

- **日记**
- **随笔**
- **旅行**
- **读书笔记**
- **其他**

## 标签规范

- 每篇文章 2-5 个标签
- 标签应具体且相关
- 使用常见技术名称作为标签
- 标签首字母大写（如 "MySQL" 而非 "mysql"）

## 示例文章

```markdown
---
title: "MySQL 数据库基础入门"
summary: "本文介绍 MySQL 数据库的基本概念、安装步骤和 CRUD 操作，适合初学者快速上手 MySQL 数据库开发。"
board: "tech"
category: "数据库"
tags:
  - "MySQL"
  - "数据库"
  - "SQL"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# MySQL 数据库基础入门

## 1. MySQL 简介

MySQL 是一种关系型数据库管理系统...

## 2. 安装 MySQL

### 在 CentOS 上安装

```bash
sudo yum install mysql-server
sudo systemctl start mysqld
```

...
```

## 格式检查清单

- [ ] 包含完整的 YAML frontmatter
- [ ] title 字段不为空
- [ ] summary 字段不为空（100-200字）
- [ ] board 字段为 "tech" 或 "life"
- [ ] category 字段符合分类体系
- [ ] tags 数组包含 2-5 个标签
- [ ] 删除所有 HTML 标签（如 `<font>`）
- [ ] 代码块指定语言
- [ ] 图片使用 Markdown 语法
- [ ] 标题层级正确（# ## ### ####）
