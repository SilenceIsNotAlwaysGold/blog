---
title: "Django ORM 高级查询优化实战"
category: "编程语言-Python"
board: "tech"
tags: ["Django", "ORM", "数据库优化", "Python"]
summary: "深入剖析 Django ORM 查询优化策略，从 N+1 问题到 raw SQL，全面提升数据库访问性能"
is_published: true
created_at: "2024-03-15T10:00:00Z"
updated_at: "2024-03-15T10:00:00Z"
---

# Django ORM 高级查询优化实战

在生产环境中，Django ORM 的便利性往往伴随着性能陷阱。本文基于我在多个 Django 项目中的优化经验，系统总结 ORM 层面的查询优化方法论。

## 一、N+1 问题的识别与解决

### 1.1 什么是 N+1 问题

N+1 问题是 ORM 中最常见的性能杀手。假设我们有如下模型：

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
```

看似简单的模板渲染：

```python
# 视图层
articles = Article.objects.all()[:20]

# 模板层
{% for article in articles %}
    {{ article.title }} - {{ article.author.name }}
{% endfor %}
```

这段代码会产生 1 + 20 = 21 条 SQL 查询。第一条查询获取 20 篇文章，然后每篇文章都会单独查询一次作者信息。

### 1.2 用 django-debug-toolbar 定位问题

生产环境排查的第一步是安装 `django-debug-toolbar`，但在生产服务器上我更推荐用 `django-silk` 或者自定义中间件：

```python
import logging
from django.db import connection

logger = logging.getLogger('sql')

class SQLLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()
        response = self.get_response(request)
        
        queries = connection.queries
        total_time = sum(float(q['time']) for q in queries)
        
        if len(queries) > 10 or total_time > 0.5:
            logger.warning(
                f"[SQL ALERT] {request.path} - "
                f"{len(queries)} queries, {total_time:.3f}s total"
            )
            for q in queries:
                if float(q['time']) > 0.1:
                    logger.warning(f"  SLOW: {q['sql'][:200]} ({q['time']}s)")
        
        return response
```

这个中间件会在单个请求查询数超过 10 或总时间超过 0.5 秒时发出告警，在生产环境帮我发现了大量隐藏的 N+1 问题。

## 二、select_related 与 prefetch_related

### 2.1 select_related：解决 ForeignKey 的 N+1

`select_related` 通过 SQL JOIN 一次性加载关联对象：

```python
# 优化前：21 条查询
articles = Article.objects.all()[:20]

# 优化后：1 条查询（INNER JOIN）
articles = Article.objects.select_related('author', 'category').all()[:20]
```

生成的 SQL：

```sql
SELECT article.*, author.*, category.*
FROM article
INNER JOIN author ON article.author_id = author.id
LEFT OUTER JOIN category ON article.category_id = category.id
LIMIT 20;
```

**注意事项**：`select_related` 只适用于 ForeignKey 和 OneToOneField，不支持 ManyToManyField。当 JOIN 链过深（超过 3 层）时，可能导致查询变慢，需要权衡。

### 2.2 prefetch_related：解决 ManyToMany 和反向关联

```python
# 获取文章及其所有标签（ManyToMany）
articles = Article.objects.prefetch_related('tags').all()[:20]
# 产生 2 条查询：1条查文章，1条查标签（IN 子查询）

# 获取作者及其所有文章（反向关联）
authors = Author.objects.prefetch_related('articles').all()[:10]
```

### 2.3 Prefetch 对象：精细控制预取逻辑

生产中经常需要对预取的查询集做过滤或排序：

```python
from django.db.models import Prefetch

# 只预取已发布的文章，并按时间倒序
authors = Author.objects.prefetch_related(
    Prefetch(
        'articles',
        queryset=Article.objects.filter(
            is_published=True
        ).select_related('category').order_by('-created_at')[:5],
        to_attr='recent_articles'  # 存为列表属性而非 QuerySet
    )
).all()

for author in authors:
    # author.recent_articles 是一个 Python 列表，不会再产生查询
    for article in author.recent_articles:
        print(f"{article.title} - {article.category.name}")
```

`to_attr` 是一个很容易被忽略但非常强大的参数。它将结果缓存为 Python 列表，避免了后续访问时的重复查询。

## 三、QuerySet 高级技巧

### 3.1 only() 和 defer()：控制字段加载

当表中有大字段（如 TextField）时，选择性加载可以显著减少内存占用：

```python
# 只加载需要的字段
articles = Article.objects.only('id', 'title', 'created_at').all()

# 延迟加载大字段
articles = Article.objects.defer('content', 'html_content').all()
```

**踩坑经验**：`only()` 和 `select_related()` 混用时要特别注意。如果 `only()` 没有包含外键字段，访问关联对象时仍然会产生额外查询：

```python
# 错误：没有包含 author_id，select_related 失效
articles = Article.objects.select_related('author').only('title')

# 正确：必须包含外键字段
articles = Article.objects.select_related('author').only('title', 'author')
```

### 3.2 annotate() 与 aggregate()：数据库层面聚合

把计算逻辑下推到数据库层面，避免在 Python 中遍历：

```python
from django.db.models import Count, Avg, Q, F, Value
from django.db.models.functions import Coalesce

# 统计每个分类下的文章数和平均阅读量
categories = Category.objects.annotate(
    article_count=Count('articles'),
    avg_views=Coalesce(Avg('articles__view_count'), Value(0)),
    published_count=Count('articles', filter=Q(articles__is_published=True))
).filter(article_count__gt=0).order_by('-article_count')

# 用 F() 表达式避免竞态条件
Article.objects.filter(id=article_id).update(view_count=F('view_count') + 1)
```

### 3.3 Subquery 和 OuterRef：复杂关联查询

```python
from django.db.models import Subquery, OuterRef

# 获取每个作者最新发布的文章标题
latest_article = Article.objects.filter(
    author=OuterRef('pk'),
    is_published=True
).order_by('-created_at')

authors = Author.objects.annotate(
    latest_article_title=Subquery(latest_article.values('title')[:1])
)
```

## 四、Raw SQL 的正确使用方式

当 ORM 无法表达复杂查询时，不要强行用 ORM 拼接，直接使用 Raw SQL：

```python
from django.db import connection

def get_article_statistics(start_date, end_date):
    """获取文章统计数据，包括每日发布量和累计量"""
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH daily_stats AS (
                SELECT 
                    DATE(created_at) as pub_date,
                    COUNT(*) as daily_count
                FROM articles
                WHERE created_at BETWEEN %s AND %s
                    AND is_published = TRUE
                GROUP BY DATE(created_at)
            )
            SELECT 
                pub_date,
                daily_count,
                SUM(daily_count) OVER (ORDER BY pub_date) as cumulative_count
            FROM daily_stats
            ORDER BY pub_date
        """, [start_date, end_date])
        
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

**安全要点**：永远使用参数化查询（`%s` 占位符），绝不要用 f-string 拼接 SQL，这是 SQL 注入的入口。

## 五、查询计划分析

### 5.1 用 explain() 查看执行计划

Django 3.0+ 提供了 `explain()` 方法：

```python
# 查看查询执行计划
qs = Article.objects.select_related('author').filter(
    is_published=True,
    created_at__year=2024
)
print(qs.explain(format='JSON', analyze=True))
```

### 5.2 常见的执行计划问题

```
# 全表扫描 - 需要加索引
type: ALL, rows: 150000

# 索引未命中 - 检查查询条件是否匹配索引
type: ALL, possible_keys: idx_created_at, key: NULL

# 文件排序 - 考虑联合索引覆盖 ORDER BY
Extra: Using filesort
```

### 5.3 索引优化建议

```python
class Article(models.Model):
    # ... 字段定义 ...
    
    class Meta:
        indexes = [
            # 联合索引：覆盖常用查询条件
            models.Index(
                fields=['is_published', '-created_at'],
                name='idx_published_created'
            ),
            # 条件索引（PostgreSQL）：只索引已发布文章
            models.Index(
                fields=['created_at'],
                condition=Q(is_published=True),
                name='idx_published_articles_date'
            ),
        ]
```

## 六、实战案例：文章列表页优化

优化前的代码（我在某项目中实际遇到的）：

```python
def article_list(request):
    articles = Article.objects.filter(is_published=True)
    data = []
    for article in articles:
        data.append({
            'title': article.title,
            'author': article.author.name,           # N+1
            'category': article.category.name,        # N+1
            'tags': [t.name for t in article.tags.all()],  # N+1
            'comment_count': article.comments.count(),     # N+1
        })
    return JsonResponse({'articles': data})
```

优化后：

```python
def article_list(request):
    articles = Article.objects.filter(
        is_published=True
    ).select_related(
        'author', 'category'
    ).prefetch_related(
        Prefetch('tags', queryset=Tag.objects.only('id', 'name'))
    ).annotate(
        comment_count=Count('comments')
    ).only(
        'id', 'title', 'created_at',
        'author__name', 'category__name'
    ).order_by('-created_at')[:20]
    
    data = [
        {
            'title': a.title,
            'author': a.author.name,
            'category': a.category.name if a.category else None,
            'tags': [t.name for t in a.tags.all()],
            'comment_count': a.comment_count,
        }
        for a in articles
    ]
    return JsonResponse({'articles': data})
```

优化结果：从 80+ 条 SQL 查询降到 2 条，响应时间从 320ms 降到 18ms。

## 总结

Django ORM 查询优化的核心原则：

1. **先度量后优化**：用中间件或工具监控 SQL 查询数量和耗时
2. **减少查询数量**：`select_related` / `prefetch_related` 解决 N+1
3. **减少数据传输**：`only()` / `defer()` / `values()` 控制字段
4. **下推计算到数据库**：`annotate()` / `aggregate()` 替代 Python 循环
5. **索引覆盖查询**：`explain()` 分析执行计划，针对性建索引
6. **合理使用 Raw SQL**：ORM 搞不定的场景不要硬凑

性能优化不是一次性的工作，而是需要持续监控和迭代的过程。建议在 CI 流程中加入查询数量断言（django-perf-rec），防止优化成果被后续开发冲掉。
