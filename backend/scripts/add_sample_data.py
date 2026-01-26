#!/usr/bin/env python3
"""
Add sample data for Python developer
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.models.article import Article
from app.models.category import Category
from app.models.tag import Tag
from app.models.skill import Skill
from app.models.project import Project
from app.core.config import settings
from datetime import datetime


async def add_sample_data():
    """Add sample data"""
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    # Initialize Beanie
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User, Article, Category, Tag, Skill, Project]
    )

    # Get admin user
    admin = await User.find_one(User.username == "admin")
    if not admin:
        print("❌ Admin user not found!")
        return

    print("✅ Found admin user")

    # Create categories
    print("\n📁 Creating categories...")
    categories = [
        {"name": "Python 开发", "board": "tech", "description": "Python 编程语言相关的技术文章"},
        {"name": "Web 开发", "board": "tech", "description": "Web 开发技术和框架"},
        {"name": "数据库", "board": "tech", "description": "数据库设计和优化"},
    ]

    category_map = {}
    for cat_data in categories:
        existing = await Category.find_one(Category.name == cat_data["name"], Category.board == cat_data["board"])
        if existing:
            print(f"  ⏭️  Category '{cat_data['name']}' already exists")
            category_map[cat_data["name"]] = existing
        else:
            category = Category(**cat_data)
            await category.insert()
            category_map[cat_data["name"]] = category
            print(f"  ✅ Created category: {cat_data['name']}")

    # Create tags
    print("\n🏷️  Creating tags...")
    tag_names = ["Python", "FastAPI", "Django", "Flask", "异步编程", "数据库", "MongoDB", "PostgreSQL", "Docker", "微服务"]

    tag_map = {}
    for tag_name in tag_names:
        existing = await Tag.find_one(Tag.name == tag_name)
        if existing:
            print(f"  ⏭️  Tag '{tag_name}' already exists")
            tag_map[tag_name] = existing
        else:
            tag = Tag(name=tag_name)
            await tag.insert()
            tag_map[tag_name] = tag
            print(f"  ✅ Created tag: {tag_name}")

    # Create articles
    print("\n📝 Creating articles...")
    articles_data = [
        {
            "title": "FastAPI 快速入门指南",
            "content": """# FastAPI 快速入门指南

## 什么是 FastAPI？

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于基于标准 Python 类型提示构建 API。

### 主要特性

- **快速**：性能媲美 NodeJS 和 Go
- **快速编码**：提高开发速度约 200% 到 300%
- **更少的 bug**：减少约 40% 的人为错误
- **直观**：强大的编辑器支持，自动补全
- **简单**：易于使用和学习
- **简短**：减少代码重复

## 安装

```bash
pip install fastapi
pip install uvicorn[standard]
```

## 第一个应用

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## 运行应用

```bash
uvicorn main:app --reload
```

访问 http://localhost:8000 即可看到结果。

## 自动 API 文档

FastAPI 会自动生成交互式 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 总结

FastAPI 是 Python Web 开发的优秀选择，特别适合构建高性能的 API 服务。""",
            "summary": "FastAPI 是一个现代、快速的 Python Web 框架，本文介绍了 FastAPI 的基本使用方法和核心特性。",
            "board": "tech",
            "category": "Python 开发",
            "tags": ["Python", "FastAPI", "Web 开发"]
        },
        {
            "title": "Python 异步编程详解",
            "content": """# Python 异步编程详解

## 什么是异步编程？

异步编程是一种编程范式，允许程序在等待某些操作完成时继续执行其他任务，而不是阻塞等待。

## asyncio 基础

Python 3.5+ 引入了 `async/await` 语法，使异步编程更加简洁。

### 基本示例

```python
import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# 运行异步函数
asyncio.run(say_hello())
```

## 并发执行多个任务

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1 完成"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 完成"

async def main():
    # 并发执行
    results = await asyncio.gather(task1(), task2())
    print(results)

asyncio.run(main())
```

## 异步 HTTP 请求

使用 `aiohttp` 进行异步 HTTP 请求：

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    html = await fetch('https://example.com')
    print(html)

asyncio.run(main())
```

## 最佳实践

1. 使用 `asyncio.gather()` 并发执行多个任务
2. 避免在异步函数中使用阻塞操作
3. 使用异步库（如 aiohttp、asyncpg）
4. 合理使用 `asyncio.create_task()` 创建后台任务

## 总结

异步编程可以显著提高 I/O 密集型应用的性能，是现代 Python 开发的重要技能。""",
            "summary": "深入讲解 Python 异步编程的概念、用法和最佳实践，包括 asyncio 的使用方法。",
            "board": "tech",
            "category": "Python 开发",
            "tags": ["Python", "异步编程"]
        },
        {
            "title": "MongoDB 与 Python 集成实战",
            "content": """# MongoDB 与 Python 集成实战

## 为什么选择 MongoDB？

MongoDB 是一个流行的 NoSQL 数据库，具有以下优势：

- 灵活的文档模型
- 高性能
- 易于扩展
- 丰富的查询功能

## 安装依赖

```bash
pip install pymongo
pip install motor  # 异步驱动
pip install beanie  # ODM 框架
```

## 使用 PyMongo

### 连接数据库

```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['my_database']
collection = db['users']
```

### 插入文档

```python
user = {
    "name": "张三",
    "age": 25,
    "email": "zhangsan@example.com"
}

result = collection.insert_one(user)
print(f"插入的文档 ID: {result.inserted_id}")
```

### 查询文档

```python
# 查询单个文档
user = collection.find_one({"name": "张三"})

# 查询多个文档
users = collection.find({"age": {"$gte": 18}})
for user in users:
    print(user)
```

## 使用 Motor（异步）

```python
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def main():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['my_database']
    collection = db['users']

    # 异步插入
    await collection.insert_one({"name": "李四", "age": 30})

    # 异步查询
    user = await collection.find_one({"name": "李四"})
    print(user)

asyncio.run(main())
```

## 使用 Beanie（ODM）

```python
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field

class User(Document):
    name: str
    age: int
    email: str

    class Settings:
        name = "users"

async def main():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    await init_beanie(database=client['my_database'], document_models=[User])

    # 创建用户
    user = User(name="王五", age=28, email="wangwu@example.com")
    await user.insert()

    # 查询用户
    users = await User.find(User.age >= 18).to_list()
    print(users)

asyncio.run(main())
```

## 最佳实践

1. 使用连接池
2. 创建适当的索引
3. 使用投影减少数据传输
4. 批量操作提高性能
5. 异步操作提高并发性能

## 总结

MongoDB 与 Python 的集成非常简单，无论是同步还是异步场景都有成熟的解决方案。""",
            "summary": "介绍如何在 Python 中使用 MongoDB，包括 PyMongo、Motor 和 Beanie 的使用方法。",
            "board": "tech",
            "category": "数据库",
            "tags": ["Python", "MongoDB", "数据库"]
        }
    ]

    for article_data in articles_data:
        # Check if article already exists
        existing = await Article.find_one(Article.title == article_data["title"])
        if existing:
            print(f"  ⏭️  Article '{article_data['title']}' already exists")
            continue

        # Get category
        category = category_map.get(article_data["category"])

        # Create article
        article = Article(
            title=article_data["title"],
            content=article_data["content"],
            summary=article_data["summary"],
            board=article_data["board"],
            category_id=category.id if category else None,
            tags=article_data["tags"],
            author_id=admin.id,
            is_published=True,
            published_at=datetime.utcnow()
        )
        await article.insert()
        print(f"  ✅ Created article: {article_data['title']}")

    # Create skills
    print("\n💪 Creating skills...")
    skills_data = [
        {"name": "Python", "category": "backend", "proficiency": 90, "order": 1},
        {"name": "FastAPI", "category": "backend", "proficiency": 85, "order": 2},
        {"name": "Django", "category": "backend", "proficiency": 80, "order": 3},
        {"name": "MongoDB", "category": "database", "proficiency": 75, "order": 4},
        {"name": "PostgreSQL", "category": "database", "proficiency": 70, "order": 5},
        {"name": "Docker", "category": "devops", "proficiency": 80, "order": 6},
        {"name": "Git", "category": "devops", "proficiency": 85, "order": 7},
    ]

    for skill_data in skills_data:
        existing = await Skill.find_one(Skill.name == skill_data["name"])
        if existing:
            print(f"  ⏭️  Skill '{skill_data['name']}' already exists")
        else:
            skill = Skill(**skill_data)
            await skill.insert()
            print(f"  ✅ Created skill: {skill_data['name']}")

    # Create projects
    print("\n🚀 Creating projects...")
    projects_data = [
        {
            "name": "个人博客系统",
            "description": "基于 FastAPI + Vue 3 的双板块个人博客系统，支持技术文章和生活随笔的分类管理。",
            "tech_stack": ["Python", "FastAPI", "Vue 3", "MongoDB", "Docker"],
            "github_url": "https://github.com/example/personal-blog",
            "order": 1
        },
        {
            "name": "API 网关服务",
            "description": "高性能的 API 网关服务，支持路由转发、限流、认证等功能。",
            "tech_stack": ["Python", "FastAPI", "Redis", "PostgreSQL"],
            "github_url": "https://github.com/example/api-gateway",
            "order": 2
        }
    ]

    for project_data in projects_data:
        existing = await Project.find_one(Project.name == project_data["name"])
        if existing:
            print(f"  ⏭️  Project '{project_data['name']}' already exists")
        else:
            project = Project(**project_data)
            await project.insert()
            print(f"  ✅ Created project: {project_data['name']}")

    print("\n🎉 Sample data added successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(add_sample_data())
