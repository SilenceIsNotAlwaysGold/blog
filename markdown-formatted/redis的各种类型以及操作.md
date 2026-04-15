---
title: "Redis 数据类型与操作完全指南"
summary: "Redis 数据类型与操作完全指南 目录 1. Redis 简介 2. 五种基本数据类型 3. 三种特殊数据类型 4. 通用命令 5. 实战场景 Redis 简介 1.1 什么是 Redis Redis（Remote Dictionary Server）是一个开源的内存数据结构存储系统，可以用作数据库、缓存和消息中间件。 1."
board: "tech"
category: "数据库"
tags:
  - "Redis"
  - "缓存"
  - "NoSQL"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Redis 数据类型与操作完全指南

## 目录

- [1. Redis 简介](#1-redis-简介)
- [2. 五种基本数据类型](#2-五种基本数据类型)
- [3. 三种特殊数据类型](#3-三种特殊数据类型)
- [4. 通用命令](#4-通用命令)
- [5. 实战场景](#5-实战场景)

## 1. Redis 简介

### 1.1 什么是 Redis

Redis（Remote Dictionary Server）是一个开源的内存数据结构存储系统，可以用作数据库、缓存和消息中间件。

### 1.2 主要特点

- **高性能**：所有数据存储在内存中，读写速度极快
- **丰富的数据类型**：支持多种数据结构
- **持久化**：支持 RDB 和 AOF 两种持久化方式
- **原子性操作**：所有操作都是原子性的
- **支持事务**：通过 MULTI/EXEC 实现事务
- **主从复制**：支持数据复制到多个从服务器

## 2. 五种基本数据类型

### 2.1 String（字符串）

String 是 Redis 最基本的数据类型，一个 key 对应一个 value。String 类型是二进制安全的，可以包含任何数据。

#### 常用命令

```bash
# 设置值
SET key value
SET name "张三"

# 设置值并指定过期时间（秒）
SETEX key seconds value
SETEX session:token 3600 "abc123"

# 只有 key 不存在时才设置
SETNX key value
SETNX lock:user:1001 1

# 获取值
GET key
GET name

# 批量设置
MSET key1 value1 key2 value2
MSET user:1:name "张三" user:1:age 25

# 批量获取
MGET key1 key2
MGET user:1:name user:1:age

# 追加字符串
APPEND key value
APPEND message "Hello"

# 获取字符串长度
STRLEN key
STRLEN name

# 数值操作
INCR key              # 自增 1
INCRBY key increment  # 增加指定值
DECR key              # 自减 1
DECRBY key decrement  # 减少指定值

# 示例：计数器
INCR page:views       # 页面访问量 +1
INCRBY user:score 10  # 用户积分 +10
```

#### 使用场景

- **缓存**：缓存用户信息、配置信息
- **计数器**：文章阅读量、点赞数
- **分布式锁**：使用 SETNX 实现
- **Session 存储**：存储用户会话信息

### 2.2 Hash（哈希）

Hash 是一个 string 类型的 field 和 value 的映射表，适合存储对象。

#### 常用命令

```bash
# 设置单个字段
HSET key field value
HSET user:1001 name "张三"
HSET user:1001 age 25

# 设置多个字段
HMSET key field1 value1 field2 value2
HMSET user:1002 name "李四" age 28 email "lisi@example.com"

# 获取单个字段
HGET key field
HGET user:1001 name

# 获取多个字段
HMGET key field1 field2
HMGET user:1001 name age

# 获取所有字段和值
HGETALL key
HGETALL user:1001

# 获取所有字段名
HKEYS key
HKEYS user:1001

# 获取所有值
HVALS key
HVALS user:1001

# 判断字段是否存在
HEXISTS key field
HEXISTS user:1001 email

# 删除字段
HDEL key field1 field2
HDEL user:1001 email

# 字段数量
HLEN key
HLEN user:1001

# 数值操作
HINCRBY key field increment
HINCRBY user:1001 age 1
HINCRBY user:1001 score 10
```

#### 使用场景

- **存储对象**：用户信息、商品信息
- **购物车**：field 为商品 ID，value 为数量
- **统计信息**：存储多维度统计数据

### 2.3 List（列表）

List 是简单的字符串列表，按照插入顺序排序。可以添加元素到列表的头部或尾部。

#### 常用命令

```bash
# 左侧插入（头部）
LPUSH key value1 value2
LPUSH tasks "task1" "task2"

# 右侧插入（尾部）
RPUSH key value1 value2
RPUSH logs "log1" "log2"

# 左侧弹出
LPOP key
LPOP tasks

# 右侧弹出
RPOP key
RPOP logs

# 阻塞式弹出（用于消息队列）
BLPOP key timeout
BLPOP tasks 30

BRPOP key timeout
BRPOP logs 30

# 获取指定范围元素
LRANGE key start stop
LRANGE logs 0 -1    # 获取所有元素
LRANGE logs 0 9     # 获取前 10 个元素

# 获取指定索引元素
LINDEX key index
LINDEX logs 0

# 获取列表长度
LLEN key
LLEN logs

# 修改指定索引元素
LSET key index value
LSET logs 0 "new log"

# 删除元素
LREM key count value
LREM logs 1 "error"  # 删除 1 个值为 "error" 的元素

# 保留指定范围元素
LTRIM key start stop
LTRIM logs 0 99      # 只保留前 100 个元素
```

#### 使用场景

- **消息队列**：使用 LPUSH + BRPOP 实现
- **最新列表**：最新文章、最新评论
- **日志系统**：存储日志记录
- **任务队列**：异步任务处理

### 2.4 Set（集合）

Set 是 string 类型的无序集合，集合成员是唯一的。

#### 常用命令

```bash
# 添加成员
SADD key member1 member2
SADD tags "redis" "database" "nosql"

# 获取所有成员
SMEMBERS key
SMEMBERS tags

# 判断成员是否存在
SISMEMBER key member
SISMEMBER tags "redis"

# 获取成员数量
SCARD key
SCARD tags

# 删除成员
SREM key member1 member2
SREM tags "nosql"

# 随机获取成员
SRANDMEMBER key count
SRANDMEMBER tags 2

# 随机弹出成员
SPOP key count
SPOP tags 1

# 集合运算
# 交集
SINTER key1 key2
SINTER user:1:tags user:2:tags

# 并集
SUNION key1 key2
SUNION user:1:tags user:2:tags

# 差集
SDIFF key1 key2
SDIFF user:1:tags user:2:tags

# 将交集结果存储到新集合
SINTERSTORE destination key1 key2
SINTERSTORE common:tags user:1:tags user:2:tags
```

#### 使用场景

- **标签系统**：文章标签、用户标签
- **共同好友**：使用交集运算
- **推荐系统**：基于标签的推荐
- **去重**：利用集合的唯一性
- **抽奖系统**：使用 SPOP 随机抽取

### 2.5 Sorted Set（有序集合）

Sorted Set 是 Set 的升级版，每个成员都关联一个分数（score），成员按分数排序。

#### 常用命令

```bash
# 添加成员
ZADD key score1 member1 score2 member2
ZADD leaderboard 100 "user1" 200 "user2" 150 "user3"

# 获取指定范围成员（按分数升序）
ZRANGE key start stop [WITHSCORES]
ZRANGE leaderboard 0 -1 WITHSCORES

# 获取指定范围成员（按分数降序）
ZREVRANGE key start stop [WITHSCORES]
ZREVRANGE leaderboard 0 9 WITHSCORES  # 获取前 10 名

# 获取指定分数范围成员
ZRANGEBYSCORE key min max [WITHSCORES]
ZRANGEBYSCORE leaderboard 100 200 WITHSCORES

# 获取成员分数
ZSCORE key member
ZSCORE leaderboard "user1"

# 获取成员排名
ZRANK key member        # 升序排名
ZREVRANK key member     # 降序排名
ZREVRANK leaderboard "user1"

# 获取成员数量
ZCARD key
ZCARD leaderboard

# 获取指定分数范围成员数量
ZCOUNT key min max
ZCOUNT leaderboard 100 200

# 增加成员分数
ZINCRBY key increment member
ZINCRBY leaderboard 10 "user1"

# 删除成员
ZREM key member1 member2
ZREM leaderboard "user1"

# 删除指定排名范围成员
ZREMRANGEBYRANK key start stop
ZREMRANGEBYRANK leaderboard 0 9

# 删除指定分数范围成员
ZREMRANGEBYSCORE key min max
ZREMRANGEBYSCORE leaderboard 0 100
```

#### 使用场景

- **排行榜**：游戏排行、热门文章
- **延迟队列**：使用时间戳作为分数
- **优先级队列**：使用优先级作为分数
- **范围查询**：按分数范围查询数据

## 3. 三种特殊数据类型

### 3.1 Bitmap（位图）

Bitmap 不是实际的数据类型，而是在 String 类型上定义的一组面向位的操作。

#### 常用命令

```bash
# 设置位值
SETBIT key offset value
SETBIT user:sign:1001:202601 0 1  # 1月1日签到
SETBIT user:sign:1001:202601 1 1  # 1月2日签到

# 获取位值
GETBIT key offset
GETBIT user:sign:1001:202601 0

# 统计位值为 1 的数量
BITCOUNT key [start end]
BITCOUNT user:sign:1001:202601  # 统计本月签到天数

# 位运算
BITOP operation destkey key1 key2
BITOP AND result key1 key2  # 与运算
BITOP OR result key1 key2   # 或运算
BITOP XOR result key1 key2  # 异或运算
BITOP NOT result key1       # 非运算

# 查找第一个指定位值的位置
BITPOS key bit [start end]
BITPOS user:sign:1001:202601 1  # 查找第一次签到的日期
```

#### 使用场景

- **用户签到**：每天一位，节省空间
- **在线状态**：标记用户是否在线
- **统计活跃用户**：使用位运算统计
- **布隆过滤器**：判断元素是否存在

### 3.2 HyperLogLog

HyperLogLog 是用于基数统计的算法，可以用极小的内存空间统计大量数据的基数。

#### 常用命令

```bash
# 添加元素
PFADD key element1 element2
PFADD page:uv:20260126 "user1" "user2" "user3"

# 获取基数估算值
PFCOUNT key
PFCOUNT page:uv:20260126

# 合并多个 HyperLogLog
PFMERGE destkey sourcekey1 sourcekey2
PFMERGE page:uv:total page:uv:20260126 page:uv:20260127
```

#### 使用场景

- **UV 统计**：统计网站独立访客
- **去重计数**：统计不重复元素数量
- **大数据基数统计**：节省内存空间

### 3.3 Geospatial（地理位置）

Geospatial 用于存储地理位置信息，支持地理位置相关的操作。

#### 常用命令

```bash
# 添加地理位置
GEOADD key longitude latitude member
GEOADD cities 116.405285 39.904989 "北京"
GEOADD cities 121.472644 31.231706 "上海"
GEOADD cities 113.264385 23.129112 "广州"

# 获取地理位置
GEOPOS key member
GEOPOS cities "北京"

# 计算两点距离
GEODIST key member1 member2 [unit]
GEODIST cities "北京" "上海" km

# 查找指定范围内的位置
GEORADIUS key longitude latitude radius unit [WITHDIST] [WITHCOORD] [COUNT count]
GEORADIUS cities 116.405285 39.904989 1000 km WITHDIST

# 查找指定成员周围的位置
GEORADIUSBYMEMBER key member radius unit [WITHDIST] [WITHCOORD] [COUNT count]
GEORADIUSBYMEMBER cities "北京" 1000 km WITHDIST

# 获取 Geohash
GEOHASH key member
GEOHASH cities "北京"
```

#### 使用场景

- **附近的人**：查找附近的用户
- **外卖配送**：查找附近的商家
- **打车服务**：查找附近的司机
- **地理围栏**：判断是否在指定区域内

## 4. 通用命令

### 4.1 Key 操作

```bash
# 查看所有 key（生产环境慎用）
KEYS *
KEYS user:*

# 扫描 key（推荐使用）
SCAN cursor [MATCH pattern] [COUNT count]
SCAN 0 MATCH user:* COUNT 100

# 判断 key 是否存在
EXISTS key
EXISTS user:1001

# 删除 key
DEL key1 key2
DEL user:1001

# 设置过期时间（秒）
EXPIRE key seconds
EXPIRE session:token 3600

# 设置过期时间（毫秒）
PEXPIRE key milliseconds
PEXPIRE session:token 3600000

# 设置过期时间戳
EXPIREAT key timestamp
EXPIREAT session:token 1706227200

# 查看剩余生存时间（秒）
TTL key
TTL session:token

# 查看剩余生存时间（毫秒）
PTTL key
PTTL session:token

# 移除过期时间
PERSIST key
PERSIST user:1001

# 重命名 key
RENAME key newkey
RENAME old:key new:key

# 查看 key 的类型
TYPE key
TYPE user:1001

# 随机返回一个 key
RANDOMKEY
```

### 4.2 数据库操作

```bash
# 切换数据库（默认 16 个数据库，索引 0-15）
SELECT index
SELECT 1

# 查看当前数据库 key 数量
DBSIZE

# 清空当前数据库
FLUSHDB

# 清空所有数据库
FLUSHALL

# 保存数据到磁盘
SAVE       # 同步保存（阻塞）
BGSAVE     # 异步保存（后台）

# 查看最后一次保存时间
LASTSAVE
```

## 5. 实战场景

### 5.1 缓存用户信息

```bash
# 使用 Hash 存储用户信息
HMSET user:1001 name "张三" age 25 email "zhangsan@example.com"
EXPIRE user:1001 3600

# 获取用户信息
HGETALL user:1001
```

### 5.2 分布式锁

```bash
# 获取锁
SET lock:resource:1001 1 NX EX 30

# 释放锁（使用 Lua 脚本保证原子性）
# if redis.call("get", KEYS[1]) == ARGV[1] then
#     return redis.call("del", KEYS[1])
# else
#     return 0
# end
```

### 5.3 消息队列

```bash
# 生产者
LPUSH queue:tasks "task1"
LPUSH queue:tasks "task2"

# 消费者
BRPOP queue:tasks 30
```

### 5.4 排行榜

```bash
# 添加用户分数
ZADD leaderboard 1000 "user1"
ZADD leaderboard 1500 "user2"
ZADD leaderboard 1200 "user3"

# 增加分数
ZINCRBY leaderboard 100 "user1"

# 获取前 10 名
ZREVRANGE leaderboard 0 9 WITHSCORES

# 获取用户排名
ZREVRANK leaderboard "user1"
```

### 5.5 用户签到

```bash
# 签到
SETBIT user:sign:1001:202601 25 1  # 1月26日签到

# 查询是否签到
GETBIT user:sign:1001:202601 25

# 统计本月签到天数
BITCOUNT user:sign:1001:202601

# 查询连续签到
# 需要结合应用层逻辑实现
```

### 5.6 UV 统计

```bash
# 记录访问
PFADD page:uv:20260126 "user1"
PFADD page:uv:20260126 "user2"
PFADD page:uv:20260126 "user1"  # 重复访问不会增加计数

# 获取 UV
PFCOUNT page:uv:20260126

# 统计多天 UV
PFMERGE page:uv:week page:uv:20260120 page:uv:20260121 page:uv:20260122
PFCOUNT page:uv:week
```

### 5.7 限流

```bash
# 使用 String + INCR 实现简单限流
# 限制每分钟最多 100 次请求
SET rate:limit:user:1001 0 EX 60 NX
INCR rate:limit:user:1001
GET rate:limit:user:1001  # 如果超过 100 则拒绝请求
```

### 5.8 附近的人

```bash
# 添加用户位置
GEOADD users:location 116.405285 39.904989 "user1"
GEOADD users:location 116.407395 39.904211 "user2"

# 查找附近 5km 内的用户
GEORADIUS users:location 116.405285 39.904989 5 km WITHDIST COUNT 10
```

## 参考资源

- [Redis 官方文档](https://redis.io/documentation)
- [Redis 命令参考](https://redis.io/commands)
- [Redis 中文网](http://www.redis.cn/)
