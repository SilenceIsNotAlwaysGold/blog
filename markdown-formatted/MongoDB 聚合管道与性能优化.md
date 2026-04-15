---
title: "MongoDB 聚合管道与性能优化"
category: "数据库"
board: "tech"
tags: ["MongoDB", "聚合管道", "性能优化", "Beanie"]
summary: "MongoDB 聚合管道实战、索引策略、分片设计、Change Streams 与 Beanie ODM 最佳实践"
is_published: true
created_at: "2024-07-22T10:00:00Z"
updated_at: "2024-07-22T10:00:00Z"
---

# MongoDB 聚合管道与性能优化

MongoDB 在非结构化和半结构化数据场景下有天然优势，但如果不懂优化，性能可能比 MySQL 还差。本文总结我在漏洞知识库和日志分析系统中使用 MongoDB 的实战经验。

## 一、聚合管道深入

### 1.1 管道阶段与执行顺序

聚合管道的执行顺序直接影响性能。核心原则：**尽早过滤，减少后续阶段处理的数据量**。

```python
from pymongo import MongoClient

db = MongoClient()["vuln_db"]

# 错误：先 $lookup 再 $match（全量 JOIN 后再过滤）
bad_pipeline = [
    {"$lookup": {
        "from": "products",
        "localField": "product_id",
        "foreignField": "_id",
        "as": "product"
    }},
    {"$match": {"severity": "critical"}},  # 太晚了！
]

# 正确：先 $match 过滤，减少 $lookup 数据量
good_pipeline = [
    {"$match": {"severity": "critical"}},  # 先过滤
    {"$lookup": {
        "from": "products",
        "localField": "product_id",
        "foreignField": "_id",
        "as": "product"
    }},
    {"$unwind": "$product"},
]
```

### 1.2 复杂聚合实战

**场景：漏洞趋势分析** - 按月统计各严重等级漏洞数量，计算环比增长率

```python
pipeline = [
    # 1. 时间范围过滤
    {"$match": {
        "published_date": {
            "$gte": datetime(2024, 1, 1),
            "$lt": datetime(2025, 1, 1)
        }
    }},
    
    # 2. 按月份和严重等级分组
    {"$group": {
        "_id": {
            "month": {"$dateToString": {"format": "%Y-%m", "date": "$published_date"}},
            "severity": "$severity"
        },
        "count": {"$sum": 1},
        "avg_cvss": {"$avg": "$cvss_score"}
    }},
    
    # 3. 按月份重新组织数据
    {"$group": {
        "_id": "$_id.month",
        "severities": {
            "$push": {
                "level": "$_id.severity",
                "count": "$count",
                "avg_cvss": {"$round": ["$avg_cvss", 1]}
            }
        },
        "total": {"$sum": "$count"}
    }},
    
    # 4. 排序
    {"$sort": {"_id": 1}},
    
    # 5. 用 $setWindowFields 计算环比（MongoDB 5.0+）
    {"$setWindowFields": {
        "sortBy": {"_id": 1},
        "output": {
            "prev_total": {
                "$shift": {
                    "output": "$total",
                    "by": -1,
                    "default": 0
                }
            }
        }
    }},
    
    # 6. 计算环比增长率
    {"$addFields": {
        "growth_rate": {
            "$cond": {
                "if": {"$eq": ["$prev_total", 0]},
                "then": None,
                "else": {
                    "$round": [
                        {"$multiply": [
                            {"$divide": [
                                {"$subtract": ["$total", "$prev_total"]},
                                "$prev_total"
                            ]},
                            100
                        ]},
                        1
                    ]
                }
            }
        }
    }},
    
    {"$project": {"prev_total": 0}}
]

results = list(db.vulnerabilities.aggregate(pipeline))
```

**场景：多维度关联分析** - 找出受影响产品最多的 CWE 类型

```python
cwe_analysis_pipeline = [
    {"$match": {"severity": {"$in": ["critical", "high"]}}},
    
    # 展开 CWE 数组和产品数组
    {"$unwind": "$cwe_ids"},
    {"$unwind": "$affected_products"},
    
    # 按 CWE 分组，统计关联产品
    {"$group": {
        "_id": "$cwe_ids",
        "vuln_count": {"$sum": 1},
        "affected_products": {"$addToSet": "$affected_products"},
        "avg_cvss": {"$avg": "$cvss_score"},
        "sample_vulns": {"$push": {"$cond": [
            {"$lt": [{"$size": {"$ifNull": ["$sample_vulns", []]}}, 3]},
            "$vuln_id",
            "$$REMOVE"
        ]}}
    }},
    
    # 计算产品数量
    {"$addFields": {
        "product_count": {"$size": "$affected_products"}
    }},
    
    # 排序和限制
    {"$sort": {"product_count": -1}},
    {"$limit": 20},
    
    # 裁剪产品列表（只保留前10个）
    {"$project": {
        "cwe_id": "$_id",
        "vuln_count": 1,
        "product_count": 1,
        "avg_cvss": {"$round": ["$avg_cvss", 1]},
        "top_products": {"$slice": ["$affected_products", 10]}
    }}
]
```

### 1.3 $facet：一次查询返回多个聚合结果

```python
dashboard_pipeline = [
    {"$match": {"published_date": {"$gte": last_30_days}}},
    
    {"$facet": {
        # 按严重等级分布
        "by_severity": [
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ],
        # 按数据来源分布
        "by_source": [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}}
        ],
        # 每日新增趋势
        "daily_trend": [
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$published_date"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ],
        # 总数
        "total": [
            {"$count": "count"}
        ]
    }}
]
```

## 二、索引策略

### 2.1 复合索引设计原则

遵循 ESR 原则：**E**quality（等值） → **S**ort（排序） → **R**ange（范围）

```python
# 查询：查找某严重等级的漏洞，按发布时间倒序，筛选 CVSS 分数
db.vulnerabilities.find({
    "severity": "critical",      # E: 等值匹配
    "cvss_score": {"$gte": 8.0}  # R: 范围查询
}).sort("published_date", -1)     # S: 排序

# 索引设计（ESR 顺序）
db.vulnerabilities.create_index([
    ("severity", 1),          # E
    ("published_date", -1),   # S
    ("cvss_score", 1)         # R
])
```

### 2.2 explain 分析

```python
# 查看查询计划
explain_result = db.vulnerabilities.find(
    {"severity": "critical", "cvss_score": {"$gte": 8.0}}
).sort("published_date", -1).explain("executionStats")

stats = explain_result["executionStats"]
print(f"扫描文档数: {stats['totalDocsExamined']}")
print(f"返回文档数: {stats['nReturned']}")
print(f"扫描/返回比: {stats['totalDocsExamined'] / max(stats['nReturned'], 1):.1f}")
print(f"执行时间: {stats['executionTimeMillis']}ms")

# 理想情况：扫描/返回比接近 1.0
# 如果远大于 1.0，说明索引不够优化
```

### 2.3 文本索引与部分索引

```python
# 文本索引：支持全文搜索
db.vulnerabilities.create_index([
    ("title", "text"),
    ("description", "text")
], default_language="none", weights={"title": 10, "description": 5})

# 部分索引：只索引高危漏洞，节省空间
db.vulnerabilities.create_index(
    [("affected_products", 1), ("published_date", -1)],
    partialFilterExpression={"severity": {"$in": ["critical", "high"]}}
)
```

## 三、Change Streams

实时监听数据变化，用于缓存失效和事件驱动架构：

```python
async def watch_vulnerability_changes():
    """监听漏洞数据变化，实时更新向量库"""
    pipeline = [
        {"$match": {
            "operationType": {"$in": ["insert", "update", "replace"]},
            "fullDocument.severity": {"$in": ["critical", "high"]}
        }}
    ]
    
    # resume_token 保存到 Redis，重启后可以继续消费
    resume_token = await redis.get("change_stream:vuln:token")
    
    kwargs = {"pipeline": pipeline, "full_document": "updateLookup"}
    if resume_token:
        kwargs["resume_after"] = json.loads(resume_token)
    
    async with db.vulnerabilities.watch(**kwargs) as stream:
        async for change in stream:
            try:
                doc = change["fullDocument"]
                
                if change["operationType"] == "insert":
                    await vector_store.add(doc)
                    await invalidate_cache(doc["vuln_id"])
                elif change["operationType"] in ("update", "replace"):
                    await vector_store.update(doc)
                    await invalidate_cache(doc["vuln_id"])
                
                # 保存 resume token
                await redis.set(
                    "change_stream:vuln:token",
                    json.dumps(change["_id"])
                )
            except Exception as e:
                logger.error(f"Change stream error: {e}", exc_info=True)
```

## 四、Beanie ODM

Beanie 是基于 Motor 的异步 MongoDB ODM，和 Pydantic 深度集成：

```python
from beanie import Document, Indexed, init_beanie
from pydantic import Field

class Vulnerability(Document):
    vuln_id: Indexed(str, unique=True)
    title: str
    description: str
    severity: Indexed(str)
    cvss_score: Indexed(float) = 0.0
    affected_products: list[str] = Field(default_factory=list)
    cwe_ids: list[str] = Field(default_factory=list)
    published_date: Indexed(datetime)
    source: str
    
    class Settings:
        name = "vulnerabilities"  # 集合名
        indexes = [
            # 复合索引
            [
                ("severity", 1),
                ("published_date", -1),
            ],
        ]

# 初始化
async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client.vuln_db,
        document_models=[Vulnerability]
    )

# CRUD 操作
async def create_vuln(data: VulnCreate) -> Vulnerability:
    vuln = Vulnerability(**data.model_dump())
    await vuln.insert()
    return vuln

async def search_vulns(
    severity: str | None = None,
    min_cvss: float | None = None,
    page: int = 1,
    page_size: int = 20
) -> list[Vulnerability]:
    query = Vulnerability.find()
    
    if severity:
        query = query.find(Vulnerability.severity == severity)
    if min_cvss:
        query = query.find(Vulnerability.cvss_score >= min_cvss)
    
    return await query.sort(-Vulnerability.published_date) \
                      .skip((page - 1) * page_size) \
                      .limit(page_size) \
                      .to_list()

# 聚合
async def severity_stats() -> list:
    return await Vulnerability.aggregate([
        {"$group": {
            "_id": "$severity",
            "count": {"$sum": 1},
            "avg_cvss": {"$avg": "$cvss_score"}
        }},
        {"$sort": {"count": -1}}
    ]).to_list()
```

## 五、性能优化清单

| 问题 | 解决方案 | 收益 |
|------|---------|------|
| 全表扫描 | 创建合适的索引（ESR 原则） | 查询提速 100x+ |
| 大文档传输 | 使用 projection 只返回需要的字段 | 网络带宽降低 50%+ |
| 频繁小写入 | 批量写入（bulk_write） | 写入吞吐提升 10x |
| 内存不足 | allowDiskUse=True | 防止 OOM |
| 热点数据 | 读写分离（readPreference=secondaryPreferred） | 读性能提升 |
| 大集合统计 | estimatedDocumentCount() 替代 count_documents() | 从秒级到毫秒级 |

## 总结

MongoDB 性能优化的核心：

1. **聚合管道顺序**：$match 尽早，减少后续数据量
2. **索引设计**：遵循 ESR 原则，用 explain 验证
3. **数据建模**：合理使用嵌入和引用，避免过大文档
4. **Change Streams**：实现实时数据同步，替代轮询
5. **Beanie ODM**：异步 + Pydantic 集成，开发体验好
