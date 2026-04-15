# 技术板块文章导入指南

## 📋 概述

本指南帮助你将格式化后的技术文章导入到个人博客系统的 MongoDB 数据库中。

## ✅ 前置准备

### 1. 确认文档已格式化

所有文章都应该在 `/home/clouditera/xlj/markdown-formatted/` 目录中，并包含完整的 YAML frontmatter。

```bash
ls -l /home/clouditera/xlj/markdown-formatted/
```

### 2. 安装依赖

```bash
pip install motor pyyaml passlib[bcrypt]
```

### 3. 启动 MongoDB

确保 MongoDB 服务正在运行：

```bash
# 检查 MongoDB 状态
sudo systemctl status mongod

# 如果未运行，启动 MongoDB
sudo systemctl start mongod

# 连接测试
mongo --eval "db.version()"
```

## 🚀 导入文章

### 方式一：使用导入脚本（推荐）

```bash
cd /home/clouditera/xlj/scripts
python3 import_articles.py
```

脚本会自动：
1. 创建管理员账户（用户名: admin, 密码: admin123）
2. 解析所有 Markdown 文件
3. 创建分类和标签
4. 导入文章到数据库
5. 显示导入统计

### 方式二：分步导入

如果需要更细粒度的控制，可以使用 Python 交互式导入：

```python
import asyncio
from import_articles import BlogImporter

async def custom_import():
    importer = BlogImporter(
        mongodb_url="mongodb://localhost:27017",
        database_name="personal_blog"
    )

    # 初始化管理员
    author_id = await importer.init_author()

    # 导入单个文件
    await importer.import_article(
        "/home/clouditera/xlj/markdown-formatted/Mongodb.md",
        author_id
    )

    # 或批量导入
    await importer.import_all_articles(
        "/home/clouditera/xlj/markdown-formatted"
    )

    await importer.close()

asyncio.run(custom_import())
```

## 📊 验证导入结果

### 1. 检查数据库

```bash
mongo personal_blog --eval "
  print('文章总数:', db.articles.count());
  print('分类总数:', db.categories.count());
  print('标签总数:', db.tags.count());
  print('用户总数:', db.users.count());
"
```

### 2. 查看导入的文章

```javascript
// 连接 MongoDB
mongo personal_blog

// 查看文章列表
db.articles.find({}, {title: 1, category_id: 1, tags: 1, board: 1}).pretty()

// 查看分类列表
db.categories.find().pretty()

// 查看标签列表
db.tags.find().pretty()

// 查看管理员账户
db.users.find({role: "admin"}).pretty()
```

### 3. 按分类统计

```javascript
db.articles.aggregate([
  {
    $lookup: {
      from: "categories",
      localField: "category_id",
      foreignField: "_id",
      as: "category"
    }
  },
  {
    $unwind: "$category"
  },
  {
    $group: {
      _id: "$category.name",
      count: { $sum: 1 }
    }
  },
  {
    $sort: { count: -1 }
  }
])
```

## 🗂️ 数据结构

### 文章表 (articles)

```json
{
  "_id": ObjectId("..."),
  "title": "MongoDB 完全指南",
  "content": "# MongoDB 完全指南\n\n...",
  "summary": "本文全面介绍 MongoDB...",
  "board": "tech",
  "category_id": ObjectId("..."),
  "tags": ["MongoDB", "NoSQL", "数据库"],
  "author_id": ObjectId("..."),
  "cover_image": "",
  "view_count": 0,
  "like_count": 0,
  "is_published": true,
  "created_at": ISODate("2026-01-26T10:00:00Z"),
  "updated_at": ISODate("2026-01-26T10:00:00Z")
}
```

### 分类表 (categories)

```json
{
  "_id": ObjectId("..."),
  "name": "数据库",
  "board": "tech",
  "description": "数据库相关的技术文章",
  "created_at": ISODate("2026-01-26T10:00:00Z")
}
```

### 标签表 (tags)

```json
{
  "_id": ObjectId("..."),
  "name": "MongoDB",
  "article_count": 5,
  "created_at": ISODate("2026-01-26T10:00:00Z")
}
```

## ⚠️ 注意事项

### 1. 管理员密码安全

导入脚本会创建默认管理员账户：
- 用户名: `admin`
- 密码: `admin123`

**重要**：导入完成后，请立即修改密码！

```javascript
// 连接数据库
mongo personal_blog

// 修改密码（需要先在 Python 中生成新密码的 hash）
db.users.updateOne(
  {username: "admin"},
  {$set: {password_hash: "新的bcrypt hash"}}
)
```

### 2. 重复导入

脚本会检查文章标题，避免重复导入。如果需要重新导入：

```bash
# 清空数据库（慎用！）
mongo personal_blog --eval "
  db.articles.deleteMany({});
  db.categories.deleteMany({});
  db.tags.deleteMany({});
  db.users.deleteMany({role: 'admin'});
"

# 重新导入
python3 import_articles.py
```

### 3. MongoDB 连接配置

如果 MongoDB 不在本地或使用了认证，修改脚本中的配置：

```python
# 在 import_articles.py 中修改
MONGODB_URL = "mongodb://username:password@host:port/database"
DATABASE_NAME = "personal_blog"
```

## 🐛 常见问题

### Q1: ModuleNotFoundError: No module named 'motor'

**解决**：安装依赖
```bash
pip install motor pyyaml passlib[bcrypt]
```

### Q2: pymongo.errors.ServerSelectionTimeoutError

**原因**：MongoDB 服务未启动

**解决**：
```bash
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Q3: yaml.scanner.ScannerError

**原因**：某些文档的 YAML frontmatter 格式有问题

**解决**：检查并修复对应文档的 frontmatter

### Q4: 文章已存在，跳过

**原因**：数据库中已有同标题的文章

**解决**：
- 如果是重复文章，可以忽略
- 如果需要更新，先删除旧文章再导入

## 📝 后续步骤

导入完成后：

1. ✅ 验证数据完整性
2. ✅ 修改管理员密码
3. ✅ 配置后端 API（FastAPI）
4. ✅ 启动前端项目（Vue 3）
5. ✅ 测试文章展示功能
6. ✅ 配置图片存储（如需要）
7. ✅ 部署到生产环境

## 📚 参考资料

- [MongoDB 官方文档](https://docs.mongodb.com/)
- [Motor 异步驱动](https://motor.readthedocs.io/)
- [个人博客需求文档](../docs/dev/personal-blog/personal-blog-requirements.md)
