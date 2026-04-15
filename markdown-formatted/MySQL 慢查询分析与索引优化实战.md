---
title: "MySQL 慢查询分析与索引优化实战"
category: "数据库"
board: "tech"
tags: ["MySQL", "索引优化", "慢查询", "性能调优"]
summary: "MySQL 慢查询日志分析、EXPLAIN 执行计划解读、索引设计原则与覆盖索引、分区表实战"
is_published: true
created_at: "2024-02-08T10:00:00Z"
updated_at: "2024-02-08T10:00:00Z"
---

# MySQL 慢查询分析与索引优化实战

MySQL 性能问题 90% 都出在慢查询和索引上。本文基于我在多个生产系统中的调优经验，系统讲解从发现慢查询到优化索引的完整流程。

## 一、慢查询日志配置与分析

### 1.1 开启慢查询日志

```sql
-- 查看当前配置
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- 动态开启（无需重启）
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 超过 1 秒的查询
SET GLOBAL log_queries_not_using_indexes = ON;  -- 记录未使用索引的查询
SET GLOBAL min_examined_row_limit = 100;  -- 扫描超过100行才记录

-- 持久化配置（my.cnf）
-- [mysqld]
-- slow_query_log = 1
-- slow_query_log_file = /var/log/mysql/slow.log
-- long_query_time = 1
-- log_queries_not_using_indexes = 1
```

### 1.2 用 pt-query-digest 分析

```bash
# 安装 percona-toolkit
apt-get install percona-toolkit

# 分析慢查询日志
pt-query-digest /var/log/mysql/slow.log --limit=20 --output=report

# 输出示例：
# Profile
# Rank Query ID                     Response time  Calls  R/Call  V/M
# ==== ============================ ============== ====== ======= ===
#    1 0xABCD1234...                  245.3s 35.2%    523  0.4694  0.12
#    2 0xEF561234...                  189.7s 27.2%   1234  0.1537  0.08
```

### 1.3 实时抓取慢查询

```sql
-- 查看当前运行的慢查询
SELECT id, user, host, db, command, time, state, 
       LEFT(info, 200) AS query
FROM information_schema.processlist
WHERE command != 'Sleep' AND time > 2
ORDER BY time DESC;

-- Performance Schema 查看 Top SQL
SELECT digest_text, 
       count_star AS exec_count,
       avg_timer_wait/1e12 AS avg_time_sec,
       sum_rows_examined AS total_rows,
       sum_rows_sent AS total_sent
FROM performance_schema.events_statements_summary_by_digest
ORDER BY avg_timer_wait DESC
LIMIT 10;
```

## 二、EXPLAIN 执行计划深度解读

### 2.1 关键字段含义

```sql
EXPLAIN SELECT a.title, u.name, c.name AS category
FROM articles a
JOIN users u ON a.author_id = u.id
JOIN categories c ON a.category_id = c.id
WHERE a.is_published = 1 AND a.created_at > '2024-01-01'
ORDER BY a.created_at DESC
LIMIT 20;
```

```
+----+------+-------+------+-------------------+---------+---------+------+-------+-----------------------------+
| id | type | table | type | possible_keys     | key     | key_len | ref  | rows  | Extra                       |
+----+------+-------+------+-------------------+---------+---------+------+-------+-----------------------------+
|  1 | SIMPLE| a    | range| idx_pub_created   | idx_pub | 5       | NULL | 15234 | Using where; Using filesort |
|  1 | SIMPLE| u    | eq_ref| PRIMARY          | PRIMARY | 4       | a.aid| 1     | NULL                        |
|  1 | SIMPLE| c    | eq_ref| PRIMARY          | PRIMARY | 4       | a.cid| 1     | NULL                        |
+----+------+-------+------+-------------------+---------+---------+------+-------+-----------------------------+
```

**type 字段**（从优到劣）：

| type | 含义 | 性能 |
|------|------|------|
| system/const | 最多一行匹配（主键/唯一索引等值查询） | 极快 |
| eq_ref | JOIN 使用主键/唯一索引 | 快 |
| ref | 使用非唯一索引 | 较快 |
| range | 索引范围扫描 | 一般 |
| index | 全索引扫描 | 较慢 |
| ALL | 全表扫描 | 慢 |

**Extra 字段关注点**：
- `Using index`：覆盖索引，无需回表 ✅
- `Using where`：存储引擎返回后还需 server 层过滤 ⚠️
- `Using filesort`：额外排序操作 ⚠️
- `Using temporary`：使用临时表 ❌
- `Using index condition`：索引下推（ICP）✅

### 2.2 EXPLAIN ANALYZE（MySQL 8.0.18+）

```sql
EXPLAIN ANALYZE
SELECT a.title, COUNT(c.id) AS comment_count
FROM articles a
LEFT JOIN comments c ON c.article_id = a.id
WHERE a.is_published = 1
GROUP BY a.id
ORDER BY comment_count DESC
LIMIT 10;

-- 输出包含实际执行时间和行数：
-- -> Limit: 10 row(s) (actual time=125.3..125.3 rows=10 loops=1)
--     -> Sort: comment_count DESC, limit input to 10 row(s) per chunk
--        (actual time=125.3..125.3 rows=10 loops=1)
--         -> Table scan on <temporary>
--            (actual time=120.1..121.5 rows=5234 loops=1)
```

## 三、索引设计原则

### 3.1 最左前缀原则

```sql
-- 复合索引 (is_published, category_id, created_at)
CREATE INDEX idx_pub_cat_date ON articles(is_published, category_id, created_at);

-- 能用到索引的查询 ✅
WHERE is_published = 1                                    -- 最左列
WHERE is_published = 1 AND category_id = 5                -- 前两列
WHERE is_published = 1 AND category_id = 5 AND created_at > '2024-01-01'  -- 全部

-- 不能用到索引的查询 ❌
WHERE category_id = 5                                     -- 跳过最左列
WHERE created_at > '2024-01-01'                          -- 跳过前两列
WHERE is_published = 1 AND created_at > '2024-01-01'     -- 跳过中间列（MySQL 8 可能部分用到）
```

### 3.2 覆盖索引

覆盖索引意味着查询所需的所有字段都在索引中，无需回表访问数据行：

```sql
-- 查询：获取文章列表（只需标题和时间）
SELECT title, created_at FROM articles
WHERE is_published = 1 AND category_id = 5
ORDER BY created_at DESC LIMIT 20;

-- 创建覆盖索引（包含 SELECT 的字段）
CREATE INDEX idx_cover_article_list 
ON articles(is_published, category_id, created_at DESC, title);

-- EXPLAIN 会显示 Using index（不需要回表）
```

**实际收益**：在一个 200 万行的文章表上，覆盖索引将查询时间从 85ms 降低到 3ms。

### 3.3 前缀索引

对长字符串字段建索引时，使用前缀索引节省空间：

```sql
-- 计算最佳前缀长度
SELECT 
    COUNT(DISTINCT LEFT(url, 10)) / COUNT(*) AS sel_10,
    COUNT(DISTINCT LEFT(url, 20)) / COUNT(*) AS sel_20,
    COUNT(DISTINCT LEFT(url, 30)) / COUNT(*) AS sel_30,
    COUNT(DISTINCT url) / COUNT(*) AS sel_full
FROM articles;

-- 如果 sel_20 已经接近 sel_full，用前缀 20
CREATE INDEX idx_url ON articles(url(20));
```

### 3.4 函数索引（MySQL 8.0+）

```sql
-- 如果经常按月份查询
-- 传统方式：索引失效
SELECT * FROM articles WHERE MONTH(created_at) = 3;

-- MySQL 8.0 函数索引
CREATE INDEX idx_created_month ON articles((MONTH(created_at)));

-- 或者用生成列
ALTER TABLE articles ADD COLUMN created_month TINYINT 
    GENERATED ALWAYS AS (MONTH(created_at)) STORED;
CREATE INDEX idx_created_month ON articles(created_month);
```

## 四、实战优化案例

### 4.1 案例一：分页查询优化

```sql
-- 原始查询（深分页问题，offset 越大越慢）
SELECT * FROM articles 
WHERE is_published = 1 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 100000;
-- 耗时：1.2s（需要扫描 100020 行）

-- 优化方案：游标分页
SELECT * FROM articles 
WHERE is_published = 1 AND id < 50000  -- 上一页最后一条的 ID
ORDER BY id DESC 
LIMIT 20;
-- 耗时：2ms

-- 如果必须用 offset，使用延迟关联
SELECT a.* FROM articles a
INNER JOIN (
    SELECT id FROM articles 
    WHERE is_published = 1 
    ORDER BY created_at DESC 
    LIMIT 20 OFFSET 100000
) t ON a.id = t.id;
-- 耗时：45ms（子查询用覆盖索引，只扫描索引不回表）
```

### 4.2 案例二：ORDER BY 优化

```sql
-- 问题：Using filesort
SELECT * FROM articles 
WHERE category_id IN (1, 2, 3) 
ORDER BY created_at DESC LIMIT 20;

-- 原因：IN 条件破坏了索引排序
-- 解决：拆成 UNION ALL
(SELECT * FROM articles WHERE category_id = 1 ORDER BY created_at DESC LIMIT 20)
UNION ALL
(SELECT * FROM articles WHERE category_id = 2 ORDER BY created_at DESC LIMIT 20)
UNION ALL
(SELECT * FROM articles WHERE category_id = 3 ORDER BY created_at DESC LIMIT 20)
ORDER BY created_at DESC LIMIT 20;
```

### 4.3 案例三：COUNT 优化

```sql
-- 慢：精确 count
SELECT COUNT(*) FROM articles WHERE is_published = 1;
-- 50万行耗时 200ms

-- 方案 1：缓存计数器（Redis）
-- 每次文章发布/下架时更新计数器

-- 方案 2：近似值（如果业务可接受）
EXPLAIN SELECT COUNT(*) FROM articles WHERE is_published = 1;
-- 从 EXPLAIN 的 rows 估算值获取近似行数

-- 方案 3：汇总表
CREATE TABLE article_stats (
    category_id INT PRIMARY KEY,
    published_count INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 用触发器或应用层维护
```

## 五、分区表

数据量超千万时，考虑分区：

```sql
-- 按时间范围分区
CREATE TABLE access_logs (
    id BIGINT AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50),
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    -- ...
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 查询时自动分区裁剪
SELECT * FROM access_logs 
WHERE created_at BETWEEN '2024-03-01' AND '2024-03-31';
-- 只扫描 p202403 分区

-- 自动管理分区的存储过程
DELIMITER $$
CREATE PROCEDURE manage_partitions()
BEGIN
    -- 删除超过 1 年的分区
    -- 创建未来 3 个月的分区
END$$
DELIMITER ;
```

## 六、索引维护

```sql
-- 查看索引使用情况
SELECT object_schema, object_name, index_name, count_star
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE object_schema = 'mydb'
ORDER BY count_star ASC;
-- count_star = 0 的索引可能是废弃索引，考虑删除

-- 查看索引大小
SELECT table_name, index_name,
       ROUND(stat_value * @@innodb_page_size / 1024 / 1024, 2) AS size_mb
FROM mysql.innodb_index_stats
WHERE stat_name = 'size' AND database_name = 'mydb'
ORDER BY stat_value DESC;

-- 索引碎片检查
SELECT table_name, data_free, data_length,
       ROUND(data_free / data_length * 100, 2) AS fragmentation_pct
FROM information_schema.tables
WHERE table_schema = 'mydb' AND data_free > 0
ORDER BY fragmentation_pct DESC;
```

## 总结

MySQL 优化的核心思路：

1. **发现问题**：慢查询日志 + pt-query-digest 定位 Top SQL
2. **分析原因**：EXPLAIN / EXPLAIN ANALYZE 看执行计划
3. **索引优化**：遵循最左前缀、考虑覆盖索引、避免索引失效场景
4. **SQL 改写**：深分页用游标、COUNT 用缓存、IN + ORDER BY 拆 UNION
5. **架构层面**：数据量大用分区表、读写分离、缓存前置
6. **持续监控**：定期清理废弃索引、检查碎片、关注慢查询趋势
