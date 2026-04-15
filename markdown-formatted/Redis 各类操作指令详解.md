---
title: "Redis 各类操作指令详解"
summary: "键操作 字符串操作 哈希操作 列表操作 集合操作 有序集合操作 位图操作 HyperLogLog操作 地理空间操作 发布与订阅 事务 脚本与管道 Lua脚本 管道（Pipeline） 通过客户端库（如Python的redis-py）实现。 服务器管理 通过以上命令，您可以在Redis中执行各种操作，从基本的键操作到高级的 事务和脚本管理。"
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

### 1. 键操作
```bash
DEL key              # 删除指定的键
EXISTS key           # 检查键是否存在
EXPIRE key seconds   # 设置键的过期时间（秒）
TTL key              # 获取键的剩余生存时间（秒）
RENAME key newkey    # 重命名键
TYPE key             # 获取键的数据类型
KEYS pattern         # 查找匹配的键
```

### 2. 字符串操作
```bash
SET key value                # 设置键的值
GET key                      # 获取键的值
GETSET key value             # 设置新值并返回旧值
MGET key1 key2               # 获取多个键的值
SETNX key value              # 仅在键不存在时设置值
SETEX key seconds value      # 设置值及其过期时间
INCR key                     # 将键的值自增1
DECR key                     # 将键的值自减1
INCRBY key increment         # 按增量增加键的值
DECRBY key decrement         # 按减量减少键的值
APPEND key value             # 追加值到字符串末尾
STRLEN key                   # 获取字符串长度
```

### 3. 哈希操作
```bash
HSET key field value         # 设置哈希表中的字段
HGET key field               # 获取哈希表中的字段值
HDEL key field               # 删除一个或多个哈希表字段
HEXISTS key field            # 检查哈希表字段是否存在
HGETALL key                  # 获取哈希表中的所有字段和值
HINCRBY key field increment  # 按增量增加哈希表字段的值
HLEN key                     # 获取哈希表字段数量
HMSET key field value [field value ...]  # 设置多个哈希字段值
HMGET key field [field ...]  # 获取多个哈希字段值
HKEYS key                    # 获取哈希表中的所有字段
HVALS key                    # 获取哈希表中的所有值
```

### 4. 列表操作
```bash
LPUSH key value [value ...]  # 从左侧插入一个或多个值
RPUSH key value [value ...]  # 从右侧插入一个或多个值
LPOP key                     # 从左侧弹出一个值
RPOP key                     # 从右侧弹出一个值
LRANGE key start stop        # 获取列表的子范围
LLEN key                     # 获取列表长度
LINDEX key index             # 获取列表中指定索引的值
LSET key index value         # 设置列表中指定索引的值
LREM key count value         # 删除列表中与值相等的元素
LTRIM key start stop         # 修剪列表到指定范围
RPOPLPUSH source destination # 从右侧弹出并推入到另一个列表
```

### 5. 集合操作
```bash
SADD key member [member ...]     # 添加一个或多个成员到集合
SREM key member [member ...]     # 从集合中移除一个或多个成员
SISMEMBER key member             # 检查成员是否在集合中
SMEMBERS key                     # 获取集合中的所有成员
SCARD key                        # 获取集合中成员数量
SRANDMEMBER key [count]          # 随机获取集合中的一个或多个成员
SPOP key [count]                 # 随机移除集合中的一个或多个成员
SUNION key [key ...]             # 返回多个集合的并集
SINTER key [key ...]             # 返回多个集合的交集
SDIFF key [key ...]              # 返回多个集合的差集
SMOVE source destination member  # 将成员从一个集合移动到另一个集合
```

### 6. 有序集合操作
```bash
ZADD key score member [score member ...]  # 添加一个或多个成员到有序集合
ZREM key member [member ...]              # 移除一个或多个有序集合成员
ZSCORE key member                        # 获取成员的分数
ZRANGE key start stop [WITHSCORES]       # 按索引范围返回有序集合成员
ZREVRANGE key start stop [WITHSCORES]    # 按索引范围逆序返回有序集合成员
ZRANGEBYSCORE key min max [WITHSCORES]   # 按分数范围返回有序集合成员
ZREVRANGEBYSCORE key max min [WITHSCORES]# 按分数范围逆序返回有序集合成员
ZCARD key                                # 获取有序集合成员数量
ZCOUNT key min max                       # 计算指定分数范围的成员数量
ZRANK key member                         # 获取成员的排名（从0开始）
ZREVRANK key member                      # 获取成员的逆序排名
ZINCRBY key increment member             # 增加成员的分数
```

### 7. 位图操作
```bash
SETBIT key offset value          # 设置字符串某个位置的位值
GETBIT key offset                # 获取字符串某个位置的位值
BITCOUNT key [start end]         # 计算字符串中值为1的位数
BITOP operation destkey key [key ...]  # 对一个或多个键进行按位操作
```

### 8. HyperLogLog操作
```bash
PFADD key element [element ...]  # 添加元素到HyperLogLog
PFCOUNT key [key ...]            # 返回HyperLogLog的基数估计值
PFMERGE destkey sourcekey [sourcekey ...]  # 合并多个HyperLogLog
```

### 9. 地理空间操作
```bash
GEOADD key longitude latitude member [longitude latitude member ...]  # 添加地理空间位置
GEOPOS key member [member ...]           # 获取成员的地理位置
GEODIST key member1 member2 [unit]       # 计算两个成员的距离
GEORADIUS key longitude latitude radius unit [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC]  # 按范围查找位置
GEORADIUSBYMEMBER key member radius unit [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC]  # 按成员查找范围
```

### 10. 发布与订阅
```bash
PUBLISH channel message    # 发布消息到频道
SUBSCRIBE channel [channel ...]  # 订阅一个或多个频道
UNSUBSCRIBE [channel [channel ...]]  # 退订一个或多个频道
PSUBSCRIBE pattern [pattern ...]  # 订阅一个或多个模式匹配的频道
PUNSUBSCRIBE [pattern [pattern ...]]  # 退订一个或多个模式匹配的频道
```

### 11. 事务
```bash
MULTI          # 开始事务
EXEC           # 执行事务
DISCARD        # 放弃事务
WATCH key [key ...]  # 监视一个或多个键
UNWATCH        # 取消监视所有键
```

### 12. 脚本与管道
#### Lua脚本
```bash
EVAL script numkeys key [key ...] arg [arg ...]  # 执行Lua脚本
EVALSHA sha1 numkeys key [key ...] arg [arg ...]  # 执行已缓存的Lua脚本
SCRIPT LOAD script     # 缓存Lua脚本
SCRIPT FLUSH           # 清除所有Lua脚本缓存
SCRIPT EXISTS sha1 [sha1 ...]  # 检查Lua脚本是否已缓存
```

#### 管道（Pipeline）
通过客户端库（如Python的redis-py）实现。

```python
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
pipe = r.pipeline()
pipe.set('foo', 'bar')
pipe.get('foo')
pipe.execute()
```

### 13. 服务器管理
```bash
INFO               # 获取Redis服务器的信息和统计
MONITOR            # 实时打印接收到的命令
CONFIG GET parameter  # 获取Redis服务器的配置参数
CONFIG SET parameter value  # 设置Redis服务器的配置参数
CLIENT LIST        # 获取连接到Redis服务器的客户端列表
CLIENT KILL ip:port  # 断开与指定客户端的连接
BGREWRITEAOF       # 异步重写AOF文件
BGSAVE             # 异步保存数据到磁盘
SAVE               # 同步保存数据到磁盘
SHUTDOWN           # 关闭Redis服务器
FLUSHDB            # 删除当前数据库的所有键
FLUSHALL           # 删除所有数据库的所有键
```

通过以上命令，您可以在Redis中执行各种操作，从基本的键操作到高级的

事务和脚本管理。如果有任何具体问题或需要更多的帮助，请随时告诉我。
