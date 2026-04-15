---
title: "Redis 缓存策略与高可用方案"
category: "数据库"
board: "tech"
tags: ["Redis", "缓存", "高可用", "分布式"]
summary: "Redis 缓存穿透/击穿/雪崩解决方案、分布式锁实现、Pipeline 优化与 Sentinel/Cluster 高可用架构"
is_published: true
created_at: "2024-06-12T10:00:00Z"
updated_at: "2024-06-12T10:00:00Z"
---

# Redis 缓存策略与高可用方案

Redis 在生产系统中几乎是标配，但用不好反而会成为系统瓶颈。本文从实际生产场景出发，系统分享 Redis 缓存策略设计和高可用方案。

## 一、缓存三大问题

### 1.1 缓存穿透

缓存穿透是指查询一个不存在的数据，缓存中没有，每次都打到数据库。恶意攻击时尤其危险。

**方案一：空值缓存**

```python
async def get_user(user_id: int) -> dict | None:
    cache_key = f"user:{user_id}"
    
    # 查缓存
    cached = await redis.get(cache_key)
    if cached is not None:
        if cached == "NULL":
            return None  # 空值缓存命中
        return json.loads(cached)
    
    # 查数据库
    user = await db.get_user(user_id)
    
    if user is None:
        # 缓存空值，TTL 较短（防止数据后续被创建后长时间查不到）
        await redis.setex(cache_key, 300, "NULL")
        return None
    
    # 正常缓存
    await redis.setex(cache_key, 3600, json.dumps(user))
    return user
```

**方案二：布隆过滤器（大规模场景）**

```python
from redisbloom.client import Client as BloomClient

bloom = BloomClient()

# 初始化：将所有用户 ID 加入布隆过滤器
async def init_bloom_filter():
    user_ids = await db.get_all_user_ids()
    for uid in user_ids:
        bloom.bfAdd("user_ids_bloom", str(uid))

async def get_user_with_bloom(user_id: int) -> dict | None:
    # 先查布隆过滤器
    if not bloom.bfExists("user_ids_bloom", str(user_id)):
        return None  # 一定不存在
    
    # 可能存在，走正常缓存逻辑
    return await get_user(user_id)
```

### 1.2 缓存击穿

热点 key 过期的瞬间，大量并发请求同时穿透到数据库。

**方案：互斥锁 + 逻辑过期**

```python
async def get_hot_data(key: str) -> dict:
    cached = await redis.get(key)
    
    if cached:
        data = json.loads(cached)
        # 检查逻辑过期时间
        if data["_expire_at"] > time.time():
            return data["value"]
        
        # 已逻辑过期，尝试获取锁进行更新
        lock_key = f"lock:refresh:{key}"
        if await redis.set(lock_key, "1", nx=True, ex=30):
            try:
                # 获取锁成功，异步刷新缓存
                fresh_data = await db.query(key)
                await redis.set(key, json.dumps({
                    "value": fresh_data,
                    "_expire_at": time.time() + 3600
                }))
                return fresh_data
            finally:
                await redis.delete(lock_key)
        else:
            # 获取锁失败，返回旧数据（短暂的数据不一致是可接受的）
            return data["value"]
    
    # 缓存完全不存在，加锁查库
    lock_key = f"lock:init:{key}"
    for _ in range(3):
        if await redis.set(lock_key, "1", nx=True, ex=30):
            try:
                data = await db.query(key)
                await redis.set(key, json.dumps({
                    "value": data,
                    "_expire_at": time.time() + 3600
                }))
                return data
            finally:
                await redis.delete(lock_key)
        else:
            await asyncio.sleep(0.1)
            cached = await redis.get(key)
            if cached:
                return json.loads(cached)["value"]
    
    # 兜底：直接查库
    return await db.query(key)
```

### 1.3 缓存雪崩

大量 key 同时过期或 Redis 宕机，请求全部打到数据库。

**方案：过期时间打散 + 多级缓存**

```python
import random

def set_cache_with_jitter(key: str, value: str, base_ttl: int):
    """TTL 加随机偏移，防止集体过期"""
    jitter = random.randint(0, base_ttl // 5)  # 20% 的随机偏移
    ttl = base_ttl + jitter
    redis.setex(key, ttl, value)

# 多级缓存：本地缓存 + Redis + 数据库
from cachetools import TTLCache

local_cache = TTLCache(maxsize=10000, ttl=60)  # 本地缓存 60 秒

async def get_with_multilevel(key: str) -> dict:
    # Level 1: 本地缓存
    if key in local_cache:
        return local_cache[key]
    
    # Level 2: Redis
    cached = await redis.get(key)
    if cached:
        data = json.loads(cached)
        local_cache[key] = data
        return data
    
    # Level 3: 数据库
    data = await db.query(key)
    if data:
        await redis.setex(key, 3600, json.dumps(data))
        local_cache[key] = data
    
    return data
```

## 二、分布式锁

### 2.1 基于 Redis 的分布式锁

```python
import uuid

class RedisLock:
    def __init__(self, redis_client, key: str, timeout: int = 10):
        self.redis = redis_client
        self.key = f"distributed_lock:{key}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())
    
    async def acquire(self, blocking: bool = True, block_timeout: int = 5) -> bool:
        start = time.time()
        while True:
            if await self.redis.set(
                self.key, self.token, nx=True, ex=self.timeout
            ):
                return True
            
            if not blocking:
                return False
            
            if time.time() - start > block_timeout:
                return False
            
            await asyncio.sleep(0.05)
    
    async def release(self):
        """使用 Lua 脚本保证原子性"""
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.redis.eval(lua_script, 1, self.key, self.token)
    
    async def __aenter__(self):
        if not await self.acquire():
            raise TimeoutError(f"Failed to acquire lock: {self.key}")
        return self
    
    async def __aexit__(self, *args):
        await self.release()

# 使用
async def deduct_inventory(product_id: int, quantity: int):
    async with RedisLock(redis, f"inventory:{product_id}", timeout=5):
        current = await get_inventory(product_id)
        if current < quantity:
            raise InsufficientInventoryError()
        await set_inventory(product_id, current - quantity)
```

**注意**：单节点 Redis 锁在主从切换时可能失效。对一致性要求高的场景，使用 Redlock 算法或 etcd。

## 三、Pipeline 批量操作

### 3.1 批量读取优化

```python
# 低效：100 次网络往返
async def get_users_slow(user_ids: list[int]) -> list[dict]:
    users = []
    for uid in user_ids:
        data = await redis.get(f"user:{uid}")
        users.append(json.loads(data) if data else None)
    return users

# 高效：1 次网络往返
async def get_users_fast(user_ids: list[int]) -> list[dict]:
    pipe = redis.pipeline()
    for uid in user_ids:
        pipe.get(f"user:{uid}")
    results = await pipe.execute()
    return [json.loads(r) if r else None for r in results]
```

### 3.2 批量写入

```python
async def batch_cache_articles(articles: list[dict]):
    """批量写入文章缓存"""
    pipe = redis.pipeline()
    for article in articles:
        key = f"article:{article['id']}"
        value = json.dumps(article, ensure_ascii=False)
        ttl = 3600 + random.randint(0, 600)
        pipe.setex(key, ttl, value)
    
    # 每 500 个命令执行一批，避免单次 pipeline 过大
    if len(articles) > 500:
        for i in range(0, len(articles), 500):
            batch_pipe = redis.pipeline()
            for article in articles[i:i+500]:
                key = f"article:{article['id']}"
                batch_pipe.setex(key, 3600 + random.randint(0, 600), 
                                json.dumps(article))
            await batch_pipe.execute()
    else:
        await pipe.execute()
```

实测数据：100 个 key 的读取，逐个请求平均 50ms，Pipeline 只需 2ms，提升 25 倍。

## 四、数据结构选型

### 4.1 排行榜：Sorted Set

```python
# 文章热度排行榜
async def update_article_score(article_id: int, score_delta: float):
    await redis.zincrby("article:hot_rank", score_delta, str(article_id))

async def get_top_articles(top_n: int = 10) -> list:
    return await redis.zrevrange("article:hot_rank", 0, top_n - 1, withscores=True)

# 带时间衰减的热度算法
async def calculate_hot_score(article_id: int):
    views = await get_view_count(article_id)
    likes = await get_like_count(article_id)
    created_hours_ago = (time.time() - article.created_at.timestamp()) / 3600
    
    # Hacker News 算法变种
    score = (views * 0.1 + likes * 2) / pow(created_hours_ago + 2, 1.8)
    await redis.zadd("article:hot_rank", {str(article_id): score})
```

### 4.2 计数器：HyperLogLog

```python
# UV 统计（内存极低，误差约 0.81%）
async def record_page_view(page: str, user_id: str):
    key = f"uv:{page}:{datetime.now().strftime('%Y%m%d')}"
    await redis.pfadd(key, user_id)

async def get_daily_uv(page: str, date: str) -> int:
    return await redis.pfcount(f"uv:{page}:{date}")

# 合并多天 UV
async def get_weekly_uv(page: str) -> int:
    keys = [f"uv:{page}:{(datetime.now() - timedelta(days=i)).strftime('%Y%m%d')}" 
            for i in range(7)]
    dest_key = f"uv:{page}:weekly_tmp"
    await redis.pfmerge(dest_key, *keys)
    count = await redis.pfcount(dest_key)
    await redis.delete(dest_key)
    return count
```

## 五、高可用方案

### 5.1 Sentinel 模式

适用于数据量不大但需要高可用的场景：

```python
from redis.sentinel import Sentinel

sentinel = Sentinel(
    [('sentinel-1', 26379), ('sentinel-2', 26379), ('sentinel-3', 26379)],
    socket_timeout=0.5
)

# 获取主节点（写操作）
master = sentinel.master_for('mymaster', socket_timeout=0.5)

# 获取从节点（读操作）
slave = sentinel.slave_for('mymaster', socket_timeout=0.5)

# 读写分离
async def get_user(user_id: int):
    return await slave.get(f"user:{user_id}")  # 从从节点读

async def set_user(user_id: int, data: dict):
    await master.set(f"user:{user_id}", json.dumps(data))  # 往主节点写
```

### 5.2 Cluster 模式

数据量大需要分片时使用：

```python
from redis.cluster import RedisCluster

rc = RedisCluster(
    startup_nodes=[
        {"host": "redis-1", "port": 6379},
        {"host": "redis-2", "port": 6379},
        {"host": "redis-3", "port": 6379},
    ],
    decode_responses=True
)

# Cluster 模式下，multi-key 操作需要 hash tag
# 错误：不同 key 可能在不同 slot
rc.mget("user:1", "user:2")  # 可能报错 CROSSSLOT

# 正确：使用 hash tag 保证同一 slot
rc.mget("{user}:1", "{user}:2")  # {user} 决定 slot
```

## 六、监控指标

```bash
# 关键监控指标
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses|expired_keys|evicted_keys"

# 缓存命中率计算
# hit_rate = keyspace_hits / (keyspace_hits + keyspace_misses)
# 生产环境应保持在 95% 以上
```

```python
# Python 侧监控
async def get_redis_metrics():
    info = await redis.info()
    return {
        "hit_rate": info["keyspace_hits"] / 
                    max(info["keyspace_hits"] + info["keyspace_misses"], 1),
        "connected_clients": info["connected_clients"],
        "used_memory_mb": info["used_memory"] / 1024 / 1024,
        "ops_per_sec": info["instantaneous_ops_per_sec"],
    }
```

## 总结

Redis 缓存策略的核心要点：

1. **缓存穿透**：空值缓存（简单场景）或布隆过滤器（大规模场景）
2. **缓存击穿**：互斥锁 + 逻辑过期双重保险
3. **缓存雪崩**：TTL 打散 + 多级缓存 + 限流降级
4. **分布式锁**：Lua 脚本保证原子性，注意主从切换风险
5. **Pipeline**：批量操作必用，性能提升 10-50 倍
6. **高可用**：数据量小用 Sentinel，数据量大用 Cluster
