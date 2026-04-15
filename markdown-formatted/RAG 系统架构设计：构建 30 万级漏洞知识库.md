---
title: "RAG 系统架构设计：构建 30 万级漏洞知识库"
category: "机器学习"
board: "tech"
tags: ["RAG", "向量数据库", "知识库", "安全"]
summary: "分享构建 30 万条漏洞知识库的 RAG 系统架构，涵盖数据标准化、向量化、检索策略与持续更新机制"
is_published: true
created_at: "2024-09-05T10:00:00Z"
updated_at: "2024-09-05T10:00:00Z"
---

# RAG 系统架构设计：构建 30 万级漏洞知识库

在安全领域，漏洞信息分散在 CVE、NVD、CNNVD 等多个数据源中，格式不统一、更新频繁。我们基于 RAG（Retrieval-Augmented Generation）架构构建了一个包含 30 万+ 条目的漏洞知识库，为安全分析师提供自然语言查询接口。本文分享完整的架构设计和实现细节。

## 一、系统架构

```
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  CVE/NVD     │    │   CNNVD       │    │  CNVD/其他   │
│  数据采集     │    │   数据采集     │    │  数据采集     │
└──────┬───────┘    └───────┬───────┘    └──────┬───────┘
       │                    │                    │
       └──────────┬─────────┴────────────────────┘
                  ▼
        ┌─────────────────┐
        │  数据标准化层     │   ETL Pipeline (Celery)
        │  统一数据格式     │
        └────────┬────────┘
                 ▼
    ┌────────────────────────┐
    │     向量化与索引层       │
    │  Embedding + Milvus    │
    └────────────┬───────────┘
                 ▼
    ┌────────────────────────┐
    │     检索与生成层         │
    │  Retriever + LLM       │
    └────────────────────────┘
```

## 二、多源数据标准化

### 2.1 数据模型设计

三个数据源的字段差异很大，需要统一到一个标准格式：

```python
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"

class VulnerabilityRecord(BaseModel):
    """统一漏洞记录格式"""
    vuln_id: str              # 统一 ID，如 CVE-2024-1234
    title: str                 # 漏洞标题
    description: str           # 详细描述
    severity: SeverityLevel    # 严重程度
    cvss_score: float | None   # CVSS 评分
    cvss_vector: str | None    # CVSS 向量
    affected_products: list[str]  # 受影响产品
    affected_versions: list[str]  # 受影响版本
    cwe_ids: list[str]         # CWE 分类
    references: list[str]      # 参考链接
    solution: str | None       # 修复方案
    source: str                # 数据来源
    published_date: datetime
    last_modified: datetime
    
    # 用于检索的富文本字段
    search_text: str = ""      # 组合字段，用于生成 embedding
```

### 2.2 数据适配器

每个数据源需要一个适配器将原始格式转换为统一格式：

```python
class NVDAdapter:
    """NVD 数据适配器"""
    
    def transform(self, raw: dict) -> VulnerabilityRecord:
        cve_data = raw.get("cve", {})
        metrics = raw.get("metrics", {})
        
        # 提取 CVSS 评分（优先 v3.1，其次 v3.0，最后 v2.0）
        cvss_score, cvss_vector = self._extract_cvss(metrics)
        
        # 提取受影响产品（CPE 解析）
        affected = self._parse_cpe_matches(raw.get("configurations", []))
        
        # 提取描述（优先英文，备选中文）
        description = self._extract_description(cve_data.get("descriptions", []))
        
        record = VulnerabilityRecord(
            vuln_id=cve_data.get("id", ""),
            title=f"{cve_data.get('id', '')} - {description[:100]}",
            description=description,
            severity=self._map_severity(cvss_score),
            cvss_score=cvss_score,
            cvss_vector=cvss_vector,
            affected_products=affected["products"],
            affected_versions=affected["versions"],
            cwe_ids=self._extract_cwe(cve_data.get("weaknesses", [])),
            references=[r["url"] for r in cve_data.get("references", [])],
            solution=self._extract_solution(cve_data),
            source="NVD",
            published_date=cve_data.get("published"),
            last_modified=cve_data.get("lastModified"),
        )
        
        # 构建检索文本
        record.search_text = self._build_search_text(record)
        return record
    
    def _build_search_text(self, record: VulnerabilityRecord) -> str:
        """构建用于 embedding 的富文本"""
        parts = [
            f"漏洞编号: {record.vuln_id}",
            f"标题: {record.title}",
            f"严重程度: {record.severity.value} (CVSS: {record.cvss_score})",
            f"描述: {record.description}",
            f"受影响产品: {', '.join(record.affected_products[:10])}",
            f"CWE分类: {', '.join(record.cwe_ids)}",
        ]
        if record.solution:
            parts.append(f"修复方案: {record.solution}")
        return "\n".join(parts)
```

### 2.3 去重与合并

同一个漏洞在不同数据源中可能有不同信息，需要智能合并：

```python
class VulnerabilityMerger:
    def merge(self, records: list[VulnerabilityRecord]) -> VulnerabilityRecord:
        """合并同一漏洞的多源数据"""
        # 按数据源优先级排序：NVD > CNNVD > CNVD
        priority = {"NVD": 3, "CNNVD": 2, "CNVD": 1}
        records.sort(key=lambda r: priority.get(r.source, 0), reverse=True)
        
        base = records[0].model_copy()
        
        for record in records[1:]:
            # 补充缺失字段
            if not base.solution and record.solution:
                base.solution = record.solution
            if not base.cvss_score and record.cvss_score:
                base.cvss_score = record.cvss_score
            # 合并受影响产品（去重）
            base.affected_products = list(set(
                base.affected_products + record.affected_products
            ))
        
        # 重建搜索文本
        base.search_text = self._build_merged_search_text(base)
        return base
```

## 三、向量化策略

### 3.1 Embedding 模型选择

经过测试，对于中文安全领域文本，效果排序：

| 模型 | 维度 | 检索准确率(Top-5) | 速度 |
|------|------|-------------------|------|
| bge-large-zh | 1024 | 89% | 中 |
| bge-m3 | 1024 | 91% | 慢 |
| text-embedding-3-small | 1536 | 85% | 快(API) |
| m3e-base | 768 | 82% | 快 |

最终选择 `bge-large-zh`，在准确率和速度之间取得平衡。

### 3.2 分块策略

漏洞描述长度差异很大（50~5000 字），需要合理分块：

```python
class VulnChunker:
    def __init__(self, max_chunk_size=512, overlap=50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk(self, record: VulnerabilityRecord) -> list[dict]:
        """将漏洞记录分块"""
        chunks = []
        
        # Chunk 1: 核心信息（始终作为第一个块）
        core_text = (
            f"{record.vuln_id} {record.title}\n"
            f"严重程度: {record.severity.value}\n"
            f"CVSS: {record.cvss_score}\n"
            f"受影响: {', '.join(record.affected_products[:5])}"
        )
        chunks.append({
            "text": core_text,
            "metadata": {
                "vuln_id": record.vuln_id,
                "chunk_type": "core",
                "severity": record.severity.value,
                "cvss_score": record.cvss_score or 0,
            }
        })
        
        # Chunk 2+: 详细描述（可能需要分块）
        if len(record.description) > self.max_chunk_size:
            desc_chunks = self._split_text(record.description)
            for i, text in enumerate(desc_chunks):
                chunks.append({
                    "text": f"{record.vuln_id} 描述({i+1}): {text}",
                    "metadata": {
                        "vuln_id": record.vuln_id,
                        "chunk_type": "description",
                        "chunk_index": i,
                    }
                })
        else:
            chunks.append({
                "text": f"{record.vuln_id}: {record.description}",
                "metadata": {
                    "vuln_id": record.vuln_id,
                    "chunk_type": "description",
                }
            })
        
        # Chunk 3: 修复方案（单独成块，方便直接检索）
        if record.solution:
            chunks.append({
                "text": f"{record.vuln_id} 修复方案: {record.solution}",
                "metadata": {
                    "vuln_id": record.vuln_id,
                    "chunk_type": "solution",
                }
            })
        
        return chunks
```

### 3.3 Milvus 集合设计

```python
from pymilvus import Collection, FieldSchema, CollectionSchema, DataType

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vuln_id", dtype=DataType.VARCHAR, max_length=50),
    FieldSchema(name="chunk_type", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="severity", dtype=DataType.VARCHAR, max_length=10),
    FieldSchema(name="cvss_score", dtype=DataType.FLOAT),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
]

schema = CollectionSchema(fields=fields, description="Vulnerability knowledge base")
collection = Collection("vuln_kb", schema)

# 创建 IVF_FLAT 索引（30万数据量，nlist=1024 效果较好）
index_params = {
    "metric_type": "COSINE",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024}
}
collection.create_index("embedding", index_params)
```

## 四、检索策略

### 4.1 混合检索

单纯的向量检索在精确匹配（如 CVE 编号）时效果不好，我们采用混合检索：

```python
class HybridRetriever:
    def __init__(self, milvus_client, es_client):
        self.milvus = milvus_client
        self.es = es_client
    
    async def search(self, query: str, top_k: int = 10) -> list[dict]:
        # 判断查询类型
        if self._is_exact_query(query):
            # CVE 编号等精确查询走 ES
            return await self._exact_search(query, top_k)
        
        # 语义检索（Milvus）
        vector_results = await self._vector_search(query, top_k * 2)
        
        # 关键词检索（Elasticsearch）
        keyword_results = await self._keyword_search(query, top_k * 2)
        
        # RRF (Reciprocal Rank Fusion) 融合
        return self._rrf_fusion(vector_results, keyword_results, top_k)
    
    def _rrf_fusion(self, vector_results, keyword_results, top_k, k=60):
        """RRF 排名融合算法"""
        scores = {}
        
        for rank, doc in enumerate(vector_results):
            doc_id = doc["vuln_id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        
        for rank, doc in enumerate(keyword_results):
            doc_id = doc["vuln_id"]
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        
        # 按融合分数排序
        sorted_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
        
        # 合并结果
        all_docs = {d["vuln_id"]: d for d in vector_results + keyword_results}
        return [all_docs[vid] for vid in sorted_ids if vid in all_docs]
```

### 4.2 元数据过滤

利用 Milvus 的标量过滤能力，缩小检索范围：

```python
async def search_with_filters(
    self, query: str, 
    severity: str = None, 
    min_cvss: float = None,
    top_k: int = 10
):
    expr_parts = []
    if severity:
        expr_parts.append(f'severity == "{severity}"')
    if min_cvss is not None:
        expr_parts.append(f'cvss_score >= {min_cvss}')
    
    expr = " && ".join(expr_parts) if expr_parts else None
    
    embedding = await self.embed(query)
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param={"metric_type": "COSINE", "params": {"nprobe": 32}},
        limit=top_k,
        expr=expr,
        output_fields=["vuln_id", "text", "severity", "cvss_score"]
    )
    return results
```

## 五、增量更新机制

漏洞数据库每天都有新增和修改，需要增量同步：

```python
class IncrementalUpdater:
    """增量更新调度器（Celery Beat 每日运行）"""
    
    async def run(self):
        # 获取上次同步时间
        last_sync = await self.get_last_sync_time()
        
        # 拉取增量数据
        new_records = await self.fetch_incremental(last_sync)
        logger.info(f"Fetched {len(new_records)} new/updated records")
        
        # 分类处理
        to_insert = []
        to_update = []
        
        for record in new_records:
            existing = await self.find_existing(record.vuln_id)
            if existing:
                if record.last_modified > existing.last_modified:
                    to_update.append(record)
            else:
                to_insert.append(record)
        
        # 批量处理
        if to_insert:
            await self.batch_insert(to_insert)
        if to_update:
            await self.batch_update(to_update)
        
        # 更新同步时间
        await self.set_last_sync_time(datetime.utcnow())
        
        logger.info(
            f"Sync complete: {len(to_insert)} inserted, "
            f"{len(to_update)} updated"
        )
```

## 六、查询示例

```
用户: Apache Log4j 有哪些高危漏洞？

系统检索 -> 找到 CVE-2021-44228, CVE-2021-45046 等

回答: Apache Log4j 存在多个高危漏洞，最严重的包括：
1. CVE-2021-44228 (Log4Shell) - CVSS 10.0 - 远程代码执行
   影响版本：2.0-beta9 到 2.14.1
   修复方案：升级到 2.17.0+
2. CVE-2021-45046 - CVSS 9.0 - 线程上下文查找导致的 RCE
   ...
```

## 总结

构建 30 万级漏洞知识库的关键经验：

1. **数据标准化是基础**：多源数据必须统一格式，否则后续环节全部受影响
2. **混合检索优于单一检索**：向量检索 + 关键词检索 + RRF 融合效果最佳
3. **分块策略很关键**：按语义分块（核心信息/描述/修复方案），而非机械切割
4. **元数据过滤提升精度**：利用 severity、cvss_score 等结构化字段缩小范围
5. **增量更新不可少**：漏洞数据每天更新，必须建立自动化同步管道
