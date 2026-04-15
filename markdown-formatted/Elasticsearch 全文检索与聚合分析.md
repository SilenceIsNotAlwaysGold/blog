---
title: "Elasticsearch 全文检索与聚合分析"
category: "数据库"
board: "tech"
tags: ["Elasticsearch", "全文检索", "聚合分析", "Python"]
summary: "Elasticsearch 映射设计、分词器配置、复合查询、聚合分析与 Python elasticsearch-py 实战"
is_published: true
created_at: "2024-12-20T10:00:00Z"
updated_at: "2024-12-20T10:00:00Z"
---

# Elasticsearch 全文检索与聚合分析

在漏洞知识库和安全日志分析项目中，Elasticsearch（ES）是核心搜索引擎。本文总结 ES 在实际项目中的映射设计、查询优化和聚合分析实践。

## 一、映射设计

### 1.1 漏洞索引映射

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(
    ["http://es-node1:9200", "http://es-node2:9200"],
    basic_auth=("elastic", "password"),
    request_timeout=30,
    retry_on_timeout=True,
    max_retries=3,
)

# 创建索引映射
vuln_mapping = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                # 自定义中文分析器
                "ik_smart_pinyin": {
                    "type": "custom",
                    "tokenizer": "ik_smart",
                    "filter": ["lowercase", "pinyin_filter"]
                },
                # 代码/CVE编号分析器
                "code_analyzer": {
                    "type": "custom",
                    "tokenizer": "pattern",
                    "pattern": "[\\W_]+",  # 按非字母数字分割
                    "filter": ["lowercase"]
                }
            },
            "filter": {
                "pinyin_filter": {
                    "type": "pinyin",
                    "keep_first_letter": True,
                    "keep_full_pinyin": True,
                    "keep_original": True,
                    "limit_first_letter_length": 16,
                    "lowercase": True,
                }
            }
        },
        "index": {
            "refresh_interval": "5s",  # 写入后 5 秒可搜索
        }
    },
    "mappings": {
        "properties": {
            "vuln_id": {
                "type": "keyword"  # 精确匹配
            },
            "title": {
                "type": "text",
                "analyzer": "ik_max_word",     # 索引时细粒度分词
                "search_analyzer": "ik_smart",  # 搜索时智能分词
                "fields": {
                    "keyword": {"type": "keyword"},  # 用于排序和聚合
                    "pinyin": {
                        "type": "text",
                        "analyzer": "ik_smart_pinyin"  # 支持拼音搜索
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart"
            },
            "severity": {
                "type": "keyword"
            },
            "cvss_score": {
                "type": "float"
            },
            "affected_products": {
                "type": "keyword"  # 数组类型，用于过滤和聚合
            },
            "cwe_ids": {
                "type": "keyword"
            },
            "published_date": {
                "type": "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd||epoch_millis"
            },
            "solution": {
                "type": "text",
                "analyzer": "ik_max_word"
            },
            "source": {
                "type": "keyword"
            },
            "references": {
                "type": "keyword",
                "index": False  # 不需要搜索 URL，节省空间
            },
            "created_at": {
                "type": "date"
            }
        }
    }
}

es.indices.create(index="vulnerabilities", body=vuln_mapping)
```

### 1.2 映射设计原则

| 场景 | 字段类型 | 说明 |
|------|---------|------|
| 全文搜索 | text | 会分词，支持模糊搜索 |
| 精确匹配/过滤 | keyword | 不分词，适合状态、标签 |
| 既要搜索又要过滤 | text + keyword（multi-field） | 两个需求都满足 |
| 数值范围 | integer/float/long | 支持范围查询 |
| 时间 | date | 支持时间范围和直方图聚合 |
| 嵌套对象 | nested | 需要独立查询嵌套字段时用 |

## 二、复合查询

### 2.1 Bool 查询

```python
def search_vulnerabilities(
    keyword: str = None,
    severity: list[str] = None,
    min_cvss: float = None,
    products: list[str] = None,
    date_from: str = None,
    date_to: str = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """多条件组合搜索"""
    
    query = {"bool": {"must": [], "filter": [], "should": []}}
    
    # 关键词搜索（must：必须匹配，影响评分）
    if keyword:
        query["bool"]["must"].append({
            "multi_match": {
                "query": keyword,
                "fields": [
                    "title^3",          # 标题权重最高
                    "title.pinyin^2",   # 拼音搜索
                    "description",
                    "vuln_id^5",        # CVE 编号精确匹配权重最高
                    "solution",
                ],
                "type": "best_fields",
                "fuzziness": "AUTO",    # 自动模糊匹配（拼写容错）
                "minimum_should_match": "75%"
            }
        })
    
    # 严重等级过滤（filter：不影响评分，有缓存）
    if severity:
        query["bool"]["filter"].append({
            "terms": {"severity": severity}
        })
    
    # CVSS 分数范围
    if min_cvss:
        query["bool"]["filter"].append({
            "range": {"cvss_score": {"gte": min_cvss}}
        })
    
    # 受影响产品
    if products:
        query["bool"]["filter"].append({
            "terms": {"affected_products": products}
        })
    
    # 时间范围
    date_range = {}
    if date_from:
        date_range["gte"] = date_from
    if date_to:
        date_range["lte"] = date_to
    if date_range:
        query["bool"]["filter"].append({
            "range": {"published_date": date_range}
        })
    
    # 如果没有任何条件，匹配所有
    if not query["bool"]["must"] and not query["bool"]["filter"]:
        query = {"match_all": {}}
    
    body = {
        "query": query,
        "from": (page - 1) * page_size,
        "size": page_size,
        "sort": [
            {"_score": {"order": "desc"}},        # 先按相关性
            {"published_date": {"order": "desc"}}  # 再按时间
        ],
        "highlight": {
            "fields": {
                "title": {"number_of_fragments": 0},
                "description": {
                    "fragment_size": 200,
                    "number_of_fragments": 2
                }
            },
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"]
        },
        "_source": {
            "excludes": ["description"]  # 大字段不返回，用 highlight 代替
        }
    }
    
    result = es.search(index="vulnerabilities", body=body)
    
    return {
        "total": result["hits"]["total"]["value"],
        "items": [
            {
                **hit["_source"],
                "score": hit["_score"],
                "highlight": hit.get("highlight", {}),
            }
            for hit in result["hits"]["hits"]
        ]
    }
```

### 2.2 搜索建议（Completion Suggester）

```python
# 索引映射中添加 suggest 字段
"title_suggest": {
    "type": "completion",
    "analyzer": "ik_smart",
    "contexts": [
        {"name": "severity", "type": "category"}
    ]
}

# 搜索建议查询
def get_suggestions(prefix: str, severity: str = None) -> list:
    suggest_body = {
        "vuln_suggest": {
            "prefix": prefix,
            "completion": {
                "field": "title_suggest",
                "size": 10,
                "fuzzy": {"fuzziness": "AUTO"},
            }
        }
    }
    
    if severity:
        suggest_body["vuln_suggest"]["completion"]["contexts"] = {
            "severity": severity
        }
    
    result = es.search(index="vulnerabilities", body={"suggest": suggest_body})
    
    suggestions = result["suggest"]["vuln_suggest"][0]["options"]
    return [s["text"] for s in suggestions]
```

## 三、聚合分析

### 3.1 多维度统计

```python
def get_vulnerability_dashboard() -> dict:
    """漏洞仪表盘聚合"""
    
    body = {
        "size": 0,  # 不返回文档，只要聚合结果
        "aggs": {
            # 按严重等级分布
            "severity_dist": {
                "terms": {"field": "severity", "size": 5}
            },
            
            # CVSS 分数分布直方图
            "cvss_histogram": {
                "histogram": {
                    "field": "cvss_score",
                    "interval": 1,
                    "min_doc_count": 0
                }
            },
            
            # 按月趋势
            "monthly_trend": {
                "date_histogram": {
                    "field": "published_date",
                    "calendar_interval": "month",
                    "format": "yyyy-MM",
                    "min_doc_count": 0
                },
                "aggs": {
                    # 每月按严重等级细分
                    "by_severity": {
                        "terms": {"field": "severity"}
                    },
                    "avg_cvss": {
                        "avg": {"field": "cvss_score"}
                    }
                }
            },
            
            # Top 20 受影响产品
            "top_products": {
                "terms": {
                    "field": "affected_products",
                    "size": 20,
                    "order": {"_count": "desc"}
                }
            },
            
            # CWE 分类统计
            "cwe_stats": {
                "terms": {
                    "field": "cwe_ids",
                    "size": 15
                },
                "aggs": {
                    "avg_cvss": {"avg": {"field": "cvss_score"}},
                    "severity_breakdown": {
                        "terms": {"field": "severity"}
                    }
                }
            },
            
            # 统计数字
            "stats": {
                "stats": {"field": "cvss_score"}
            }
        }
    }
    
    result = es.search(index="vulnerabilities", body=body)
    return result["aggregations"]
```

### 3.2 Pipeline 聚合

```python
# 计算每月环比增长率
pipeline_agg = {
    "size": 0,
    "aggs": {
        "monthly": {
            "date_histogram": {
                "field": "published_date",
                "calendar_interval": "month"
            },
            "aggs": {
                "vuln_count": {"value_count": {"field": "vuln_id"}}
            }
        },
        "monthly_growth": {
            "serial_diff": {
                "buckets_path": "monthly>vuln_count",
                "lag": 1
            }
        }
    }
}
```

## 四、批量操作

### 4.1 Bulk API

```python
from elasticsearch.helpers import bulk, streaming_bulk

def bulk_index_vulnerabilities(records: list[dict], chunk_size=500):
    """批量索引漏洞数据"""
    
    def generate_actions(records):
        for record in records:
            yield {
                "_index": "vulnerabilities",
                "_id": record["vuln_id"],  # 用 CVE ID 作为文档 ID（支持幂等更新）
                "_source": record,
            }
    
    success, errors = bulk(
        es,
        generate_actions(records),
        chunk_size=chunk_size,
        request_timeout=60,
        raise_on_error=False,
    )
    
    if errors:
        logger.error(f"Bulk indexing errors: {len(errors)} failed")
        for error in errors[:5]:  # 只记录前 5 个错误
            logger.error(f"  {error}")
    
    logger.info(f"Bulk indexed {success} documents, {len(errors)} errors")
    return success, errors

# 流式批量写入（内存友好，适合大数据量）
def streaming_index(records_generator, chunk_size=1000):
    for ok, info in streaming_bulk(
        es,
        records_generator,
        chunk_size=chunk_size,
        raise_on_error=False,
    ):
        if not ok:
            logger.error(f"Failed to index: {info}")
```

## 五、性能优化

### 5.1 索引优化

```python
# 写入密集场景的临时优化
def optimize_for_bulk_write(index_name: str):
    """大批量写入前的临时优化"""
    es.indices.put_settings(
        index=index_name,
        body={
            "index": {
                "refresh_interval": "-1",       # 暂停刷新
                "number_of_replicas": 0,         # 暂停副本同步
                "translog.durability": "async",  # 异步事务日志
            }
        }
    )

def restore_after_bulk_write(index_name: str):
    """大批量写入后恢复设置"""
    es.indices.put_settings(
        index=index_name,
        body={
            "index": {
                "refresh_interval": "5s",
                "number_of_replicas": 1,
                "translog.durability": "request",
            }
        }
    )
    # 强制合并段（减少段数量，提升查询性能）
    es.indices.forcemerge(index=index_name, max_num_segments=5)
```

### 5.2 查询优化

```python
# 使用 filter 代替 query（filter 有缓存）
# 不好：所有条件都在 must 中
bad_query = {
    "bool": {
        "must": [
            {"match": {"title": "log4j"}},
            {"term": {"severity": "critical"}},  # 不需要评分
            {"range": {"cvss_score": {"gte": 9}}}  # 不需要评分
        ]
    }
}

# 好：不需要评分的条件放 filter
good_query = {
    "bool": {
        "must": [
            {"match": {"title": "log4j"}}  # 需要评分
        ],
        "filter": [
            {"term": {"severity": "critical"}},  # 精确过滤
            {"range": {"cvss_score": {"gte": 9}}}  # 范围过滤
        ]
    }
}
```

### 5.3 监控关键指标

```python
def get_cluster_health():
    health = es.cluster.health()
    stats = es.indices.stats(index="vulnerabilities")
    
    return {
        "cluster_status": health["status"],
        "active_shards": health["active_shards"],
        "doc_count": stats["_all"]["primaries"]["docs"]["count"],
        "store_size_gb": stats["_all"]["primaries"]["store"]["size_in_bytes"] / 1e9,
        "search_rate": stats["_all"]["total"]["search"]["query_total"],
        "indexing_rate": stats["_all"]["total"]["indexing"]["index_total"],
    }
```

## 总结

Elasticsearch 实战要点：

1. **映射设计**：text 用于搜索，keyword 用于过滤和聚合，multi-field 两者兼顾
2. **分词器选择**：中文用 ik_max_word（索引）+ ik_smart（搜索），加拼音扩展
3. **查询优化**：不需评分的条件放 filter，利用缓存提升性能
4. **聚合分析**：size=0 只要聚合结果，pipeline 聚合做环比计算
5. **批量写入**：用 Bulk API，大量写入时临时关闭 refresh 和副本
6. **highlight**：搜索结果高亮替代返回全文，减少网络传输
