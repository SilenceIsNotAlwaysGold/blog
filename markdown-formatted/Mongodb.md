---
title: "MongoDB 完全指南"
summary: "本文全面介绍 MongoDB 数据库的核心概念、基本操作、索引优化、聚合框架和最佳实践。涵盖从数据库、集合、文档的基础知识到 CRUD 操作、查询优化、聚合管道等高级主题，并提供丰富的代码示例和实战案例，帮助开发者快速掌握 MongoDB 的使用技巧和性能优化方法。"
board: "tech"
category: "数据库"
tags:
  - "MongoDB"
  - "NoSQL"
  - "数据库"
  - "文档数据库"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# MongoDB 完全指南

## 目录

- [1. MongoDB 简介](#1-mongodb-简介)
- [2. 核心概念](#2-核心概念)
- [3. 基本操作](#3-基本操作)
- [4. 索引和查询优化](#4-索引和查询优化)
- [5. 聚合框架](#5-聚合框架)
- [6. 最佳实践](#6-最佳实践)

## 1. MongoDB 简介

### 1.1 什么是 MongoDB

MongoDB 是一个基于文档的 NoSQL 数据库，由 C++ 编写。它将数据存储为灵活的 JSON 样式文档，这意味着字段可以因文档而异，数据结构可以随时间改变。

### 1.2 主要特点

- **文档导向存储**：数据以 BSON（Binary JSON）格式存储
- **高性能**：支持嵌入式数据模型减少 I/O 操作
- **高可用性**：通过副本集提供自动故障转移
- **水平扩展**：通过分片实现横向扩展
- **灵活的数据模型**：无需预定义模式
- **强大的查询语言**：支持丰富的查询表达式

### 1.3 适用场景

- 内容管理系统
- 实时分析和日志记录
- 电子商务产品目录
- 移动应用后端
- 物联网数据存储
- 社交网络应用

## 2. 核心概念

### 2.1 数据库（Database）

MongoDB 中的数据库是集合的物理容器。每个数据库在文件系统中都有自己的文件集。

```bash
# 查看所有数据库
show dbs

# 切换/创建数据库
use myDatabase

# 查看当前数据库
db

# 删除当前数据库
db.dropDatabase()
```

### 2.2 集合（Collection）

集合是 MongoDB 文档的组，类似于关系数据库中的表。集合存在于数据库中，没有固定的结构。

```bash
# 创建集合
db.createCollection("users")

# 查看所有集合
show collections

# 删除集合
db.users.drop()
```

### 2.3 文档（Document）

文档是 MongoDB 中数据的基本单元，类似于关系数据库中的行。文档是一组键值对的集合。

```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "张三",
  "age": 25,
  "email": "zhangsan@example.com",
  "address": {
    "city": "北京",
    "district": "朝阳区"
  },
  "hobbies": ["阅读", "旅游", "编程"]
}
```

### 2.4 BSON 数据类型

MongoDB 使用 BSON（Binary JSON）格式存储文档。常见数据类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| String | 字符串 | "Hello World" |
| Integer | 整数 | 123 |
| Double | 浮点数 | 3.14 |
| Boolean | 布尔值 | true, false |
| Array | 数组 | [1, 2, 3] |
| Object | 嵌套文档 | {name: "张三"} |
| Date | 日期 | new Date() |
| ObjectId | 文档 ID | ObjectId() |
| Null | 空值 | null |

## 3. 基本操作

### 3.1 插入文档（Create）

```javascript
// 插入单个文档
db.users.insertOne({
  name: "李四",
  age: 28,
  email: "lisi@example.com"
})

// 插入多个文档
db.users.insertMany([
  { name: "王五", age: 30, email: "wangwu@example.com" },
  { name: "赵六", age: 22, email: "zhaoliu@example.com" }
])

// insert 方法（兼容旧版本）
db.users.insert({ name: "孙七", age: 26 })
```

### 3.2 查询文档（Read）

```javascript
// 查询所有文档
db.users.find()

// 格式化输出
db.users.find().pretty()

// 条件查询
db.users.find({ age: 25 })

// 查询单个文档
db.users.findOne({ name: "张三" })

// 比较操作符
db.users.find({ age: { $gt: 25 } })  // 大于
db.users.find({ age: { $gte: 25 } }) // 大于等于
db.users.find({ age: { $lt: 30 } })  // 小于
db.users.find({ age: { $lte: 30 } }) // 小于等于
db.users.find({ age: { $ne: 25 } })  // 不等于

// 逻辑操作符
db.users.find({
  $and: [
    { age: { $gte: 25 } },
    { age: { $lte: 30 } }
  ]
})

db.users.find({
  $or: [
    { age: { $lt: 25 } },
    { age: { $gt: 30 } }
  ]
})

// 正则表达式查询
db.users.find({ name: /^张/ })

// 数组查询
db.users.find({ hobbies: "编程" })
db.users.find({ hobbies: { $in: ["编程", "阅读"] } })

// 投影（只返回指定字段）
db.users.find({}, { name: 1, age: 1, _id: 0 })

// 排序
db.users.find().sort({ age: 1 })  // 升序
db.users.find().sort({ age: -1 }) // 降序

// 限制和跳过
db.users.find().limit(10)
db.users.find().skip(5).limit(10)

// 统计
db.users.countDocuments()
db.users.countDocuments({ age: { $gt: 25 } })
```

### 3.3 更新文档（Update）

```javascript
// 更新单个文档
db.users.updateOne(
  { name: "张三" },
  { $set: { age: 26, email: "zhangsan_new@example.com" } }
)

// 更新多个文档
db.users.updateMany(
  { age: { $lt: 25 } },
  { $set: { status: "young" } }
)

// 替换文档
db.users.replaceOne(
  { name: "李四" },
  { name: "李四", age: 29, email: "lisi_new@example.com" }
)

// 更新操作符
db.users.updateOne(
  { name: "张三" },
  {
    $set: { age: 26 },           // 设置字段
    $unset: { status: "" },      // 删除字段
    $inc: { loginCount: 1 },     // 增加数值
    $push: { hobbies: "游泳" },  // 添加数组元素
    $pull: { hobbies: "阅读" },  // 删除数组元素
    $addToSet: { tags: "vip" }   // 添加唯一元素
  }
)

// upsert（不存在则插入）
db.users.updateOne(
  { name: "新用户" },
  { $set: { age: 20 } },
  { upsert: true }
)
```

### 3.4 删除文档（Delete）

```javascript
// 删除单个文档
db.users.deleteOne({ name: "张三" })

// 删除多个文档
db.users.deleteMany({ age: { $lt: 20 } })

// 删除所有文档
db.users.deleteMany({})
```

## 4. 索引和查询优化

### 4.1 索引类型

```javascript
// 创建单字段索引
db.users.createIndex({ email: 1 })  // 1 升序，-1 降序

// 创建复合索引
db.users.createIndex({ age: 1, name: 1 })

// 创建唯一索引
db.users.createIndex({ email: 1 }, { unique: true })

// 创建文本索引
db.articles.createIndex({ content: "text" })

// 创建 TTL 索引（自动过期）
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 3600 }
)

// 查看索引
db.users.getIndexes()

// 删除索引
db.users.dropIndex("email_1")
db.users.dropIndexes()  // 删除所有索引（除了 _id）
```

### 4.2 查询性能分析

```javascript
// 查看查询执行计划
db.users.find({ age: 25 }).explain("executionStats")

// 查看索引使用情况
db.users.find({ age: 25 }).hint({ age: 1 }).explain()
```

### 4.3 查询优化建议

1. **为常用查询字段创建索引**
2. **使用投影减少返回数据量**
3. **避免全表扫描**
4. **合理使用复合索引**
5. **定期分析慢查询日志**

## 5. 聚合框架

### 5.1 聚合管道

聚合管道是 MongoDB 中用于数据处理和转换的强大工具。

```javascript
// 基本聚合示例
db.orders.aggregate([
  // 阶段1：匹配
  { $match: { status: "completed" } },

  // 阶段2：分组
  { $group: {
    _id: "$customerId",
    totalAmount: { $sum: "$amount" },
    orderCount: { $sum: 1 }
  }},

  // 阶段3：排序
  { $sort: { totalAmount: -1 } },

  // 阶段4：限制
  { $limit: 10 }
])
```

### 5.2 常用聚合操作符

```javascript
// $project - 投影
db.users.aggregate([
  { $project: {
    name: 1,
    age: 1,
    ageGroup: {
      $cond: {
        if: { $gte: ["$age", 30] },
        then: "成年",
        else: "青年"
      }
    }
  }}
])

// $lookup - 关联查询（类似 JOIN）
db.orders.aggregate([
  { $lookup: {
    from: "users",
    localField: "userId",
    foreignField: "_id",
    as: "userInfo"
  }}
])

// $unwind - 展开数组
db.users.aggregate([
  { $unwind: "$hobbies" },
  { $group: { _id: "$hobbies", count: { $sum: 1 } }}
])

// $group - 分组统计
db.sales.aggregate([
  { $group: {
    _id: "$category",
    totalSales: { $sum: "$amount" },
    avgPrice: { $avg: "$price" },
    maxPrice: { $max: "$price" },
    minPrice: { $min: "$price" }
  }}
])
```

### 5.3 实战示例

```javascript
// 统计每个城市的用户年龄分布
db.users.aggregate([
  { $match: { age: { $exists: true } } },
  { $group: {
    _id: {
      city: "$address.city",
      ageGroup: {
        $switch: {
          branches: [
            { case: { $lt: ["$age", 20] }, then: "20岁以下" },
            { case: { $lt: ["$age", 30] }, then: "20-30岁" },
            { case: { $lt: ["$age", 40] }, then: "30-40岁" }
          ],
          default: "40岁以上"
        }
      }
    },
    count: { $sum: 1 }
  }},
  { $sort: { "_id.city": 1, "_id.ageGroup": 1 } }
])
```

## 6. 最佳实践

### 6.1 数据建模

1. **嵌入 vs 引用**
   - 一对一、一对少：使用嵌入
   - 一对多、多对多：使用引用

```javascript
// 嵌入式文档（适合一对一）
{
  name: "张三",
  address: {
    city: "北京",
    street: "长安街"
  }
}

// 引用式文档（适合一对多）
// users 集合
{ _id: 1, name: "张三" }

// orders 集合
{ _id: 101, userId: 1, amount: 100 }
```

2. **避免过深的嵌套**
3. **合理使用数组字段**
4. **预留扩展字段**

### 6.2 性能优化

1. **索引策略**
   - 为高频查询字段创建索引
   - 避免过多索引影响写入性能
   - 定期维护索引

2. **查询优化**
   - 使用投影减少数据传输
   - 避免使用 $where 操作符
   - 合理使用分页

3. **连接池配置**
   ```javascript
   // Node.js 示例
   const client = new MongoClient(uri, {
     maxPoolSize: 50,
     minPoolSize: 10,
     maxIdleTimeMS: 30000
   })
   ```

### 6.3 安全建议

1. **启用认证**
   ```bash
   # 创建管理员用户
   use admin
   db.createUser({
     user: "admin",
     pwd: "securePassword",
     roles: ["root"]
   })
   ```

2. **使用角色权限控制**
3. **加密传输（TLS/SSL）**
4. **定期备份数据**
5. **限制网络访问**

### 6.4 备份和恢复

```bash
# 备份数据库
mongodump --db myDatabase --out /backup/

# 恢复数据库
mongorestore --db myDatabase /backup/myDatabase/

# 导出集合为 JSON
mongoexport --db myDatabase --collection users --out users.json

# 导入 JSON 数据
mongoimport --db myDatabase --collection users --file users.json
```

### 6.5 监控和维护

1. **监控关键指标**
   - 连接数
   - 操作延迟
   - 内存使用
   - 磁盘 I/O

2. **定期检查慢查询**
   ```javascript
   // 启用慢查询日志
   db.setProfilingLevel(1, { slowms: 100 })

   // 查看慢查询
   db.system.profile.find().sort({ ts: -1 }).limit(10)
   ```

3. **数据库统计**
   ```javascript
   // 查看数据库统计
   db.stats()

   // 查看集合统计
   db.users.stats()
   ```

## 参考资源

- [MongoDB 官方文档](https://docs.mongodb.com/)
- [MongoDB University](https://university.mongodb.com/)
- [MongoDB 中文社区](https://mongoing.com/)
