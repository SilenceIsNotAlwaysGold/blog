---
title: "Text2SQL 智能体开发实战：从 Prompt 到生产"
category: "机器学习"
board: "tech"
tags: ["Text2SQL", "LLM", "智能体", "NLP"]
summary: "分享 Text2SQL 智能体从 prompt 设计到生产部署的全流程实战经验，准确率优化到 85%+"
is_published: true
created_at: "2024-08-10T10:00:00Z"
updated_at: "2024-08-10T10:00:00Z"
---

# Text2SQL 智能体开发实战：从 Prompt 到生产

Text2SQL 是将自然语言转换为 SQL 查询的任务，是 LLM 在数据分析领域最有价值的落地场景之一。本文分享我从零构建 Text2SQL 智能体的完整经验，包括 prompt 迭代、多数据库适配、分步加载策略以及准确率从 60% 优化到 85%+ 的全过程。

## 一、系统架构概览

整个 Text2SQL 系统采用 Agent 架构，核心流程：

```
用户问题 → 意图识别 → Schema 加载 → SQL 生成 → SQL 校验 → 执行查询 → 结果格式化
                ↓                              ↓
           非SQL问题直接回答            语法错误则自动修复（最多3轮）
```

### 1.1 核心组件

```python
class Text2SQLAgent:
    def __init__(self, llm_client, db_manager, schema_loader):
        self.llm = llm_client
        self.db = db_manager
        self.schema = schema_loader
        self.max_fix_rounds = 3
    
    async def run(self, question: str, db_name: str) -> AgentResult:
        # Step 1: 意图识别
        intent = await self.classify_intent(question)
        if intent != "sql_query":
            return await self.direct_answer(question)
        
        # Step 2: 加载相关 Schema
        relevant_tables = await self.schema.load_relevant(db_name, question)
        
        # Step 3: 生成 SQL
        sql = await self.generate_sql(question, relevant_tables)
        
        # Step 4: 校验与自动修复
        for round_idx in range(self.max_fix_rounds):
            validation = await self.validate_sql(sql, db_name)
            if validation.is_valid:
                break
            sql = await self.fix_sql(sql, validation.error, question, relevant_tables)
        
        # Step 5: 执行
        result = await self.db.execute(db_name, sql)
        
        # Step 6: 格式化
        return await self.format_result(question, sql, result)
```

## 二、Prompt 设计：从失败到成功的迭代

### 2.1 第一版 Prompt（准确率 ~55%）

最初的 prompt 非常简单，直接把问题和表结构喂给模型：

```
你是一个 SQL 专家。根据以下表结构和用户问题，生成 SQL 查询。

表结构：
{schema}

用户问题：{question}

请生成 SQL：
```

问题非常多：
- 模型经常选错表
- JOIN 条件错误
- 聚合逻辑不正确
- 生成的 SQL 方言不对（MySQL 语法跑在 PostgreSQL 上）

### 2.2 第二版 Prompt（准确率 ~72%）

核心改进：加入了详细的约束和示例。

```python
SYSTEM_PROMPT = """你是一个专业的 SQL 查询生成器。你的任务是根据用户的自然语言问题，生成精确的 SQL 查询。

## 严格规则
1. 只使用提供的表和字段，不要编造任何不存在的表名或字段名
2. 目标数据库类型为 {db_type}，使用对应的 SQL 方言
3. 对于模糊的时间表达，"最近"默认为最近30天，"今年"指当前自然年
4. 字符串匹配优先使用 LIKE 而非 =
5. 涉及金额的计算，保留2位小数
6. 返回结果默认 LIMIT 100，除非用户明确要求所有数据
7. 只输出 SQL，不要输出任何解释

## 数据库方言注意事项
- MySQL: 使用反引号包裹保留字，日期函数用 DATE_FORMAT
- PostgreSQL: 使用双引号包裹保留字，日期函数用 TO_CHAR
- SQLite: 日期函数用 strftime
"""
```

### 2.3 第三版 Prompt（准确率 ~85%）

最终版的关键优化：

**1. 分步思考（Chain of Thought）**

```python
USER_PROMPT = """## 可用表结构
{schema_with_comments}

## 表关系
{relationships}

## 用户问题
{question}

## 请按以下步骤思考，然后生成 SQL：
1. 分析问题涉及哪些实体和关系
2. 确定需要用到的表
3. 确定 JOIN 条件
4. 确定 WHERE 筛选条件
5. 确定 SELECT 和聚合逻辑
6. 生成最终 SQL

请将思考过程放在 <think> 标签内，最终 SQL 放在 ```sql 代码块中。"""
```

**2. Schema 注释增强**

裸的表结构信息量不够，需要添加业务语义注释：

```python
def enhance_schema(self, table_info: dict) -> str:
    """增强 Schema 描述，添加业务语义"""
    lines = [f"-- 表名: {table_info['name']} ({table_info['comment']})"]
    lines.append(f"CREATE TABLE {table_info['name']} (")
    
    for col in table_info['columns']:
        comment = col.get('comment', '')
        enum_values = col.get('enum_values', '')
        
        col_desc = f"  {col['name']} {col['type']}"
        if comment:
            col_desc += f"  -- {comment}"
        if enum_values:
            col_desc += f" (可选值: {enum_values})"
        lines.append(col_desc)
    
    lines.append(");")
    
    # 添加示例数据（帮助模型理解数据格式）
    if table_info.get('sample_values'):
        lines.append(f"-- 示例数据: {table_info['sample_values']}")
    
    return "\n".join(lines)
```

**3. Few-shot 示例注入**

```python
def get_few_shot_examples(self, question: str, db_name: str) -> str:
    """基于相似度检索历史成功案例作为 few-shot"""
    # 从向量数据库检索最相似的 3 个问答对
    examples = self.vector_store.search(
        query=question,
        collection=f"text2sql_examples_{db_name}",
        top_k=3
    )
    
    result = "## 参考示例\n"
    for ex in examples:
        result += f"问题: {ex['question']}\nSQL: {ex['sql']}\n\n"
    
    return result
```

## 三、Schema 分步加载策略

生产数据库通常有几十甚至上百张表，全部塞进 prompt 会超过 token 限制且降低准确率。我设计了三级加载策略：

### 3.1 第一级：表名匹配

```python
async def load_relevant_tables(self, db_name: str, question: str) -> list:
    """三级 Schema 加载"""
    all_tables = await self.get_all_tables(db_name)
    
    # Level 1: 关键词匹配
    keyword_tables = self._keyword_match(question, all_tables)
    
    # Level 2: 语义匹配（embedding 相似度）
    semantic_tables = await self._semantic_match(question, all_tables, top_k=5)
    
    # Level 3: 关系补全（补充 JOIN 需要的中间表）
    candidate_tables = set(keyword_tables + semantic_tables)
    final_tables = self._complete_relationships(candidate_tables, all_tables)
    
    return final_tables

def _keyword_match(self, question: str, tables: list) -> list:
    """基于关键词和表名/注释匹配"""
    matched = []
    # 构建关键词映射（包含同义词）
    keyword_map = {
        '订单': ['orders', 'order_items'],
        '用户': ['users', 'user_profiles'],
        '商品': ['products', 'product_categories'],
        '支付': ['payments', 'refunds'],
    }
    
    for keyword, table_names in keyword_map.items():
        if keyword in question:
            matched.extend(table_names)
    
    return matched
```

### 3.2 关系补全

一个常见错误是选中了两张不直接关联的表，遗漏了中间关联表：

```python
def _complete_relationships(self, selected: set, all_tables: list) -> set:
    """检查选中的表之间是否有缺失的关联表"""
    table_graph = self._build_table_graph(all_tables)
    completed = set(selected)
    
    for t1 in selected:
        for t2 in selected:
            if t1 >= t2:
                continue
            # 检查 t1 和 t2 之间是否需要中间表
            path = self._shortest_path(table_graph, t1, t2)
            if path and len(path) <= 4:
                completed.update(path)
    
    return completed
```

## 四、SQL 校验与自动修复

### 4.1 多层校验

```python
class SQLValidator:
    async def validate(self, sql: str, db_name: str) -> ValidationResult:
        errors = []
        
        # Layer 1: 语法校验（用 sqlparse 解析）
        try:
            parsed = sqlparse.parse(sql)
            if not parsed or not parsed[0].tokens:
                errors.append("SQL 语法错误：无法解析")
        except Exception as e:
            errors.append(f"解析错误: {e}")
        
        # Layer 2: 安全校验
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
        sql_upper = sql.upper().strip()
        for kw in dangerous_keywords:
            if sql_upper.startswith(kw):
                errors.append(f"安全拦截：不允许执行 {kw} 操作")
        
        # Layer 3: Schema 校验（检查表名和字段名是否存在）
        referenced_tables = self._extract_tables(sql)
        schema = await self.get_schema(db_name)
        for table in referenced_tables:
            if table not in schema:
                errors.append(f"表 '{table}' 不存在")
        
        # Layer 4: EXPLAIN 校验（在数据库层面验证）
        if not errors:
            try:
                await self.db.execute(f"EXPLAIN {sql}")
            except Exception as e:
                errors.append(f"执行计划错误: {e}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
```

### 4.2 自动修复

```python
FIX_PROMPT = """你之前生成的 SQL 执行出错了。

原始问题: {question}
生成的 SQL: {sql}
错误信息: {error}
可用表结构: {schema}

请分析错误原因并生成修正后的 SQL。常见错误原因：
1. 字段名拼写错误（检查是否用了不存在的字段）
2. 表名错误（检查是否混淆了相似表名）
3. JOIN 条件不对（检查外键关系）
4. 聚合错误（SELECT 中的非聚合字段必须出现在 GROUP BY 中）

请直接输出修正后的 SQL。"""
```

## 五、准确率优化经验

### 5.1 0 分 Case 回溯分析

我建立了一个错误案例库，定期分析失败的查询：

```python
class ErrorAnalyzer:
    def analyze_failures(self, test_results: list) -> dict:
        categories = {
            'wrong_table': [],      # 选错表
            'wrong_join': [],       # JOIN 条件错误
            'wrong_aggregation': [], # 聚合逻辑错误
            'wrong_filter': [],     # WHERE 条件错误
            'syntax_error': [],     # 语法错误
            'semantic_error': [],   # 语义理解错误
        }
        
        for case in test_results:
            if case['score'] == 0:
                category = self._classify_error(case)
                categories[category].append(case)
        
        return categories
```

通过分析发现，错误分布为：
- 选错表/缺少表：28%
- JOIN 条件错误：22%
- 聚合逻辑错误：18%
- WHERE 条件理解错误：15%
- 语法错误：10%
- 其他：7%

### 5.2 针对性优化

**问题 1**：模型不理解"环比"、"同比"等业务术语

```python
# 在 prompt 中添加业务术语解释
BUSINESS_TERMS = """
## 业务术语说明
- 环比：与上一个周期对比（如本月vs上月）
- 同比：与去年同期对比（如今年1月vs去年1月）
- 留存率：(第N天仍活跃的用户数 / 第0天新增用户数) * 100%
- 转化率：(完成目标动作的用户数 / 总用户数) * 100%
- GMV：成交总额（包含未付款订单）
- 客单价：GMV / 下单用户数
"""
```

**问题 2**：多表 JOIN 时字段名冲突

```python
# 强制要求使用表别名
PROMPT_RULES += """
- 所有查询必须使用表别名，格式为表名首字母，如 users AS u, orders AS o
- 所有字段必须带表别名前缀，如 u.name, o.amount
"""
```

### 5.3 最终准确率

| 查询类型 | 优化前 | 优化后 |
|---------|--------|--------|
| 单表查询 | 82% | 95% |
| 双表 JOIN | 65% | 88% |
| 多表 JOIN | 40% | 75% |
| 聚合统计 | 55% | 82% |
| 子查询/CTE | 35% | 70% |
| **整体** | **60%** | **85%** |

## 六、生产监控

```python
class Text2SQLMetrics:
    """Prometheus 监控指标"""
    
    sql_generation_total = Counter('text2sql_generation_total', 'Total SQL generations', ['status'])
    sql_generation_duration = Histogram('text2sql_generation_seconds', 'SQL generation duration')
    sql_fix_rounds = Histogram('text2sql_fix_rounds', 'Number of fix rounds needed')
    schema_load_duration = Histogram('text2sql_schema_load_seconds', 'Schema loading duration')
```

## 总结

Text2SQL 智能体开发的核心经验：

1. **Prompt 是灵魂**：投入 70% 的精力在 prompt 迭代上，每一版都要有量化的准确率对比
2. **Schema 加载要智能**：不是越多越好，精准加载相关表反而效果更好
3. **自动修复是必须的**：生产环境一次生成的成功率不会超过 90%，修复机制可以补上 5-10%
4. **持续收集错误案例**：建立回溯机制，针对性地改进 prompt 和策略
5. **业务术语标准化**：模型不理解业务黑话，必须显式定义
