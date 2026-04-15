---
title: "FastAPI 异步架构设计与性能调优"
category: "编程语言-Python"
board: "tech"
tags: ["FastAPI", "异步编程", "Python", "性能优化"]
summary: "深入 FastAPI 异步架构设计，涵盖 async/await 最佳实践、中间件设计、依赖注入与 Pydantic v2 迁移"
is_published: true
created_at: "2024-05-20T10:00:00Z"
updated_at: "2024-05-20T10:00:00Z"
---

# FastAPI 异步架构设计与性能调优

FastAPI 是目前 Python Web 框架中性能最接近 Node.js 和 Go 的选择。但"用了 FastAPI"不等于"写出了高性能代码"。本文分享我在生产环境中落地 FastAPI 的架构设计和调优经验。

## 一、async/await 最佳实践

### 1.1 理解事件循环的本质

FastAPI 底层基于 Starlette + uvicorn（ASGI），核心是单线程事件循环。所有的 `async def` 路由函数都运行在同一个事件循环中，任何阻塞调用都会卡死整个服务。

```python
# 错误示范：在 async 函数中调用同步阻塞代码
@app.get("/bad")
async def bad_endpoint():
    import time
    time.sleep(5)  # 阻塞整个事件循环 5 秒！所有请求都会被卡住
    return {"msg": "done"}

# 正确做法 1：用 asyncio.sleep 替代
@app.get("/good-async")
async def good_async():
    await asyncio.sleep(5)  # 不阻塞事件循环
    return {"msg": "done"}

# 正确做法 2：同步函数用 def 声明，FastAPI 自动放入线程池
@app.get("/good-sync")
def good_sync():
    time.sleep(5)  # 在线程池中运行，不阻塞事件循环
    return {"msg": "done"}
```

**关键原则**：如果函数体内有任何阻塞 I/O（同步数据库驱动、文件操作、requests 库），要么用 `def` 声明让 FastAPI 自动分发到线程池，要么用 `run_in_executor` 手动包装。

### 1.2 异步数据库访问

```python
# 使用 asyncpg + SQLAlchemy async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/dbname",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**踩坑经验**：`expire_on_commit=False` 非常重要。默认情况下，SQLAlchemy 会在 commit 后将所有属性标记为过期，下次访问时触发隐式查询。在异步上下文中，这可能导致 `greenlet_spawn has not been called` 的诡异错误。

### 1.3 并发请求优化

当一个接口需要调用多个外部服务时，用 `asyncio.gather` 并发执行：

```python
import httpx

async_client = httpx.AsyncClient(timeout=10.0)

@app.get("/dashboard")
async def get_dashboard(user_id: int):
    # 三个请求并发执行，总耗时 = max(三个请求耗时)
    user_task = async_client.get(f"{USER_SERVICE}/users/{user_id}")
    orders_task = async_client.get(f"{ORDER_SERVICE}/orders?user_id={user_id}")
    stats_task = async_client.get(f"{STATS_SERVICE}/stats/{user_id}")
    
    user_resp, orders_resp, stats_resp = await asyncio.gather(
        user_task, orders_task, stats_task,
        return_exceptions=True  # 某个失败不影响其他
    )
    
    result = {}
    if not isinstance(user_resp, Exception):
        result['user'] = user_resp.json()
    if not isinstance(orders_resp, Exception):
        result['orders'] = orders_resp.json()
    if not isinstance(stats_resp, Exception):
        result['stats'] = stats_resp.json()
    
    return result
```

## 二、中间件设计

### 2.1 请求生命周期中间件

```python
import time
import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id', default='')

@app.middleware("http")
async def request_lifecycle_middleware(request: Request, call_next):
    # 生成请求 ID
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request_id_var.set(request_id)
    
    # 记录请求开始
    start_time = time.perf_counter()
    
    # 请求体大小限制
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
        return JSONResponse(status_code=413, content={"detail": "Request too large"})
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"[{request_id}] Unhandled error: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    
    # 记录请求耗时
    duration = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    
    # 慢请求告警
    if duration > 2.0:
        logger.warning(
            f"[{request_id}] SLOW REQUEST: {request.method} {request.url.path} "
            f"took {duration:.2f}s"
        )
    
    return response
```

### 2.2 限流中间件

基于 Redis 的滑动窗口限流：

```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost:6379/0")

async def rate_limit(key: str, limit: int, window: int) -> bool:
    """滑动窗口限流"""
    pipe = redis_client.pipeline()
    now = time.time()
    window_start = now - window
    
    pipe.zremrangebyscore(key, 0, window_start)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    
    results = await pipe.execute()
    return results[2] <= limit

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    if not await rate_limit(key, limit=100, window=60):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"},
            headers={"Retry-After": "60"}
        )
    
    return await call_next(request)
```

## 三、依赖注入体系设计

FastAPI 的依赖注入是其最强大的特性之一。在生产项目中，我构建了分层的依赖注入体系：

### 3.1 分层依赖

```python
# 基础层：数据库连接
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# 认证层：依赖数据库
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_jwt(token)
    user = await db.get(User, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# 权限层：依赖认证
def require_role(*roles: str):
    async def _check_role(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _check_role

# 业务层：依赖权限
@app.delete("/articles/{article_id}")
async def delete_article(
    article_id: int,
    user: User = Depends(require_role("admin", "editor")),
    db: AsyncSession = Depends(get_db)
):
    article = await db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404)
    await db.delete(article)
    return {"msg": "deleted"}
```

### 3.2 分页依赖

```python
from dataclasses import dataclass

@dataclass
class Pagination:
    page: int
    page_size: int
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

def get_pagination(
    page: int = Query(1, ge=1, le=1000),
    page_size: int = Query(20, ge=1, le=100)
) -> Pagination:
    return Pagination(page=page, page_size=page_size)

@app.get("/articles")
async def list_articles(
    pagination: Pagination = Depends(get_pagination),
    db: AsyncSession = Depends(get_db)
):
    query = select(Article).offset(pagination.offset).limit(pagination.page_size)
    result = await db.execute(query)
    return result.scalars().all()
```

## 四、Pydantic v2 迁移与优化

Pydantic v2 用 Rust 重写了核心逻辑，序列化速度提升 5-50 倍。

### 4.1 关键变更

```python
# v1 -> v2 主要变化
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class ArticleCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除首尾空白
        str_min_length=1,
        from_attributes=True,  # 替代 orm_mode = True
    )
    
    title: str = Field(..., max_length=200)
    content: str = Field(..., min_length=10)
    category_id: int = Field(..., gt=0)
    tags: list[str] = Field(default_factory=list, max_length=10)
    
    # v2 使用 field_validator 替代 validator
    @field_validator('tags', mode='before')
    @classmethod
    def validate_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(',') if t.strip()]
        return v
    
    # model_validator 替代 root_validator
    @model_validator(mode='after')
    def check_content_length(self):
        if len(self.content) < 50 and not self.tags:
            raise ValueError('Short articles must have at least one tag')
        return self

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    summary: str | None = None
    author: AuthorBrief
    created_at: datetime
```

### 4.2 性能对比

在我的项目中，迁移到 Pydantic v2 后的实测数据：

| 场景 | v1 耗时 | v2 耗时 | 提升 |
|------|---------|---------|------|
| 单对象序列化 | 0.12ms | 0.008ms | 15x |
| 列表(100条)序列化 | 8.5ms | 0.45ms | 19x |
| 复杂嵌套验证 | 2.1ms | 0.15ms | 14x |

## 五、生产部署配置

### 5.1 uvicorn 配置

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 5000
max_requests_jitter = 500
timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "warning"
```

### 5.2 生命周期管理

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    app.state.redis = redis.from_url("redis://localhost:6379/0")
    app.state.http_client = httpx.AsyncClient(
        timeout=10.0,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )
    logger.info("Application started")
    
    yield
    
    # 关闭时清理资源
    await app.state.redis.close()
    await app.state.http_client.aclose()
    await engine.dispose()
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)
```

## 总结

FastAPI 的性能优势需要正确的使用方式才能发挥出来。核心要点：

1. **区分 async def 和 def**：有阻塞调用用 def，纯异步用 async def
2. **避免事件循环阻塞**：使用异步驱动（asyncpg、motor、httpx）
3. **善用依赖注入**：构建分层的依赖体系，让代码可测试、可复用
4. **拥抱 Pydantic v2**：性能提升是免费的，迁移成本不高
5. **中间件要轻量**：中间件在每个请求都执行，复杂逻辑用依赖注入
6. **连接池管理**：数据库、HTTP 客户端、Redis 都要配置连接池并在 lifespan 中管理
