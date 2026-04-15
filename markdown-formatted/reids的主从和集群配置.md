---
title: "Redis 主从复制与集群配置完全指南"
summary: "Redis 主从复制与集群配置完全指南 目录 1. Redis 主从复制 2. Redis Sentinel 高可用 3. Redis Cluster 集群 4. 最佳实践 Redis 主从复制 1.1 主从复制简介 Redis 主从复制（Replication）是指将一台 Redis 服务器的数据复制到其他 Redis 服务器。"
board: "tech"
category: "其他"
tags:
  - "技术"
  - "开发"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Redis 主从复制与集群配置完全指南

## 目录

- [1. Redis 主从复制](#1-redis-主从复制)
- [2. Redis Sentinel 高可用](#2-redis-sentinel-高可用)
- [3. Redis Cluster 集群](#3-redis-cluster-集群)
- [4. 最佳实践](#4-最佳实践)

## 1. Redis 主从复制

### 1.1 主从复制简介

Redis 主从复制（Replication）是指将一台 Redis 服务器的数据复制到其他 Redis 服务器。前者称为主节点（Master），后者称为从节点（Slave）。数据的复制是单向的，只能由主节点到从节点。

### 1.2 主从复制的作用

- **数据冗余**：实现数据的热备份
- **故障恢复**：主节点故障时，从节点可以提供服务
- **负载均衡**：读写分离，主节点负责写，从节点负责读
- **高可用基础**：是 Sentinel 和 Cluster 的基础

### 1.3 主从复制原理

1. **全量复制**：从节点首次连接主节点时
   - 从节点发送 SYNC 命令
   - 主节点执行 BGSAVE 生成 RDB 文件
   - 主节点将 RDB 文件发送给从节点
   - 从节点加载 RDB 文件
   - 主节点将缓冲区的写命令发送给从节点

2. **增量复制**：全量复制后的正常同步
   - 主节点将写命令发送给从节点
   - 从节点执行写命令

3. **部分复制**：网络中断后的重新同步
   - 使用复制偏移量和复制积压缓冲区
   - 只同步中断期间的数据

### 1.4 配置主从复制

#### 方式一：配置文件

**主节点配置（redis-master.conf）**

```conf
# 绑定地址
bind 0.0.0.0

# 端口
port 6379

# 后台运行
daemonize yes

# 日志文件
logfile "/var/log/redis/redis-master.log"

# 数据目录
dir /var/lib/redis/master

# RDB 持久化
save 900 1
save 300 10
save 60 10000

# AOF 持久化
appendonly yes
appendfilename "appendonly.aof"

# 设置密码
requirepass masterpassword123
```

**从节点配置（redis-slave.conf）**

```conf
# 绑定地址
bind 0.0.0.0

# 端口
port 6380

# 后台运行
daemonize yes

# 日志文件
logfile "/var/log/redis/redis-slave.log"

# 数据目录
dir /var/lib/redis/slave

# 指定主节点
replicaof 192.168.1.100 6379

# 主节点密码
masterauth masterpassword123

# 从节点只读
replica-read-only yes

# 设置从节点密码
requirepass slavepassword123
```

#### 方式二：命令行

```bash
# 启动主节点
redis-server /etc/redis/redis-master.conf

# 启动从节点
redis-server /etc/redis/redis-slave.conf

# 或者在从节点运行时动态配置
redis-cli -p 6380
> REPLICAOF 192.168.1.100 6379
> CONFIG SET masterauth masterpassword123
```

### 1.5 查看主从状态

```bash
# 主节点
redis-cli -p 6379 -a masterpassword123
> INFO replication

# 输出示例
role:master
connected_slaves:2
slave0:ip=192.168.1.101,port=6380,state=online,offset=1234,lag=0
slave1:ip=192.168.1.102,port=6380,state=online,offset=1234,lag=0

# 从节点
redis-cli -p 6380 -a slavepassword123
> INFO replication

# 输出示例
role:slave
master_host:192.168.1.100
master_port:6379
master_link_status:up
```

### 1.6 主从切换

```bash
# 将从节点提升为主节点
redis-cli -p 6380 -a slavepassword123
> REPLICAOF NO ONE

# 将其他从节点指向新主节点
redis-cli -p 6381 -a slavepassword123
> REPLICAOF 192.168.1.101 6380
```

## 2. Redis Sentinel 高可用

### 2.1 Sentinel 简介

Redis Sentinel 是 Redis 的高可用解决方案，提供以下功能：

- **监控**：监控主从节点是否正常运行
- **通知**：通过 API 通知管理员或其他应用程序
- **自动故障转移**：主节点故障时，自动将从节点提升为主节点
- **配置提供者**：客户端通过 Sentinel 获取主节点地址

### 2.2 Sentinel 架构

```bash
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Sentinel 1 │     │  Sentinel 2 │     │  Sentinel 3 │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
│   Master    │────▶│   Slave 1   │     │   Slave 2   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 2.3 配置 Sentinel

**Sentinel 配置文件（sentinel.conf）**

```conf
# 端口
port 26379

# 后台运行
daemonize yes

# 日志文件
logfile "/var/log/redis/sentinel.log"

# 工作目录
dir /var/lib/redis/sentinel

# 监控主节点
# sentinel monitor    
# quorum: 判定主节点下线需要的 Sentinel 数量
sentinel monitor mymaster 192.168.1.100 6379 2

# 主节点密码
sentinel auth-pass mymaster masterpassword123

# 主节点下线时间（毫秒）
sentinel down-after-milliseconds mymaster 5000

# 故障转移超时时间（毫秒）
sentinel failover-timeout mymaster 60000

# 同时进行复制的从节点数量
sentinel parallel-syncs mymaster 1

# Sentinel 通知脚本
# sentinel notification-script mymaster /var/redis/notify.sh

# 故障转移脚本
# sentinel client-reconfig-script mymaster /var/redis/reconfig.sh
```

### 2.4 启动 Sentinel

```bash
# 启动 Sentinel（至少 3 个节点）
redis-sentinel /etc/redis/sentinel-1.conf
redis-sentinel /etc/redis/sentinel-2.conf
redis-sentinel /etc/redis/sentinel-3.conf

# 或使用 redis-server
redis-server /etc/redis/sentinel-1.conf --sentinel
```

### 2.5 查看 Sentinel 状态

```bash
# 连接 Sentinel
redis-cli -p 26379

# 查看监控的主节点
> SENTINEL masters

# 查看主节点信息
> SENTINEL master mymaster

# 查看从节点信息
> SENTINEL slaves mymaster

# 查看其他 Sentinel 信息
> SENTINEL sentinels mymaster

# 获取主节点地址
> SENTINEL get-master-addr-by-name mymaster

# 手动故障转移
> SENTINEL failover mymaster
```

### 2.6 客户端连接 Sentinel

**Python 示例**

```python
from redis.sentinel import Sentinel

# 连接 Sentinel
sentinel = Sentinel([
    ('192.168.1.100', 26379),
    ('192.168.1.101', 26379),
    ('192.168.1.102', 26379)
], socket_timeout=0.1)

# 获取主节点连接
master = sentinel.master_for('mymaster', 
                              socket_timeout=0.1,
                              password='masterpassword123')

# 获取从节点连接（用于读操作）
slave = sentinel.slave_for('mymaster',
                            socket_timeout=0.1,
                            password='slavepassword123')

# 写操作
master.set('key', 'value')

# 读操作
value = slave.get('key')
```

**Java 示例**

```java
import redis.clients.jedis.JedisSentinelPool;
import redis.clients.jedis.Jedis;

Set sentinels = new HashSet<>();
sentinels.add("192.168.1.100:26379");
sentinels.add("192.168.1.101:26379");
sentinels.add("192.168.1.102:26379");

JedisSentinelPool pool = new JedisSentinelPool(
    "mymaster",
    sentinels,
    "masterpassword123"
);

try (Jedis jedis = pool.getResource()) {
    jedis.set("key", "value");
    String value = jedis.get("key");
}
```

## 3. Redis Cluster 集群

### 3.1 Cluster 简介

Redis Cluster 是 Redis 的分布式解决方案，提供以下功能：

- **数据分片**：自动将数据分散到多个节点
- **高可用**：支持主从复制和自动故障转移
- **水平扩展**：可以动态添加或删除节点
- **无中心架构**：节点之间通过 Gossip 协议通信

### 3.2 Cluster 架构

```bash
┌─────────────────────────────────────────────────────────┐
│                     Redis Cluster                        │
├─────────────────────────────────────────────────────────┤
│  Master 1        Master 2        Master 3               │
│  (0-5460)        (5461-10922)    (10923-16383)          │
│     │                │                │                 │
│  Slave 1         Slave 2         Slave 3                │
└─────────────────────────────────────────────────────────┘
```

### 3.3 数据分片原理

Redis Cluster 使用哈希槽（Hash Slot）进行数据分片：

- 共有 16384 个哈希槽（0-16383）
- 每个 key 通过 CRC16 算法计算槽位：`HASH_SLOT = CRC16(key) % 16384`
- 每个主节点负责一部分槽位
- 客户端根据槽位路由到对应节点

### 3.4 配置 Cluster

**节点配置文件（redis-cluster.conf）**

```conf
# 端口（每个节点不同）
port 7000

# 绑定地址
bind 0.0.0.0

# 后台运行
daemonize yes

# 日志文件
logfile "/var/log/redis/redis-7000.log"

# 数据目录
dir /var/lib/redis/7000

# 启用集群模式
cluster-enabled yes

# 集群配置文件
cluster-config-file nodes-7000.conf

# 节点超时时间（毫秒）
cluster-node-timeout 5000

# AOF 持久化
appendonly yes

# 设置密码
requirepass clusterpassword123

# 集群节点间通信密码
masterauth clusterpassword123
```

### 3.5 创建 Cluster

#### 准备节点

```bash
# 创建 6 个节点（3 主 3 从）
mkdir -p /var/lib/redis/{7000,7001,7002,7003,7004,7005}

# 复制配置文件并修改端口
for port in 7000 7001 7002 7003 7004 7005; do
    cp redis-cluster.conf /etc/redis/redis-${port}.conf
    sed -i "s/7000/${port}/g" /etc/redis/redis-${port}.conf
done

# 启动所有节点
for port in 7000 7001 7002 7003 7004 7005; do
    redis-server /etc/redis/redis-${port}.conf
done
```

#### 创建集群

```bash
# Redis 5.0+ 使用 redis-cli 创建集群
redis-cli --cluster create \
  192.168.1.100:7000 \
  192.168.1.100:7001 \
  192.168.1.100:7002 \
  192.168.1.100:7003 \
  192.168.1.100:7004 \
  192.168.1.100:7005 \
  --cluster-replicas 1 \
  -a clusterpassword123

# --cluster-replicas 1 表示每个主节点有 1 个从节点

# Redis 4.0 使用 redis-trib.rb
# redis-trib.rb create --replicas 1 \
#   192.168.1.100:7000 \
#   192.168.1.100:7001 \
#   192.168.1.100:7002 \
#   192.168.1.100:7003 \
#   192.168.1.100:7004 \
#   192.168.1.100:7005
```

### 3.6 查看 Cluster 状态

```bash
# 连接集群节点
redis-cli -c -p 7000 -a clusterpassword123

# 查看集群信息
> CLUSTER INFO

# 输出示例
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3

# 查看集群节点
> CLUSTER NODES

# 输出示例
# 节点ID 地址 标志 主节点ID 连接状态 槽位范围
a1b2c3... 192.168.1.100:7000@17000 myself,master - 0 0 1 connected 0-5460
d4e5f6... 192.168.1.100:7001@17001 master - 0 1706227200 2 connected 5461-10922
g7h8i9... 192.168.1.100:7002@17002 master - 0 1706227200 3 connected 10923-16383
j1k2l3... 192.168.1.100:7003@17003 slave a1b2c3... 0 1706227200 1 connected
m4n5o6... 192.168.1.100:7004@17004 slave d4e5f6... 0 1706227200 2 connected
p7q8r9... 192.168.1.100:7005@17005 slave g7h8i9... 0 1706227200 3 connected

# 查看槽位分配
> CLUSTER SLOTS
```

### 3.7 Cluster 操作

#### 添加节点

```bash
# 添加主节点
redis-cli --cluster add-node \
  192.168.1.100:7006 \
  192.168.1.100:7000 \
  -a clusterpassword123

# 添加从节点
redis-cli --cluster add-node \
  192.168.1.100:7007 \
  192.168.1.100:7000 \
  --cluster-slave \
  --cluster-master-id  \
  -a clusterpassword123
```

#### 删除节点

```bash
# 删除节点前需要重新分配槽位（如果是主节点）
redis-cli --cluster reshard \
  192.168.1.100:7000 \
  --cluster-from  \
  --cluster-to  \
  --cluster-slots  \
  -a clusterpassword123

# 删除节点
redis-cli --cluster del-node \
  192.168.1.100:7000 \
   \
  -a clusterpassword123
```

#### 重新分片

```bash
# 交互式重新分片
redis-cli --cluster reshard 192.168.1.100:7000 -a clusterpassword123

# 非交互式重新分片
redis-cli --cluster reshard \
  192.168.1.100:7000 \
  --cluster-from  \
  --cluster-to  \
  --cluster-slots 1000 \
  --cluster-yes \
  -a clusterpassword123
```

#### 故障转移

```bash
# 手动故障转移
redis-cli -c -p 7003 -a clusterpassword123
> CLUSTER FAILOVER

# 强制故障转移（不等待主节点同意）
> CLUSTER FAILOVER FORCE

# 接管故障转移（主节点已下线）
> CLUSTER FAILOVER TAKEOVER
```

### 3.8 客户端连接 Cluster

**Python 示例**

```python
from rediscluster import RedisCluster

# 启动节点列表
startup_nodes = [
    {"host": "192.168.1.100", "port": "7000"},
    {"host": "192.168.1.100", "port": "7001"},
    {"host": "192.168.1.100", "port": "7002"}
]

# 创建集群连接
rc = RedisCluster(
    startup_nodes=startup_nodes,
    decode_responses=True,
    password='clusterpassword123',
    skip_full_coverage_check=True
)

# 操作数据
rc.set('key', 'value')
value = rc.get('key')

# 批量操作（需要使用 Hash Tag）
rc.mset({
    '{user:1001}:name': '张三',
    '{user:1001}:age': 25
})
```

**Java 示例**

```java
import redis.clients.jedis.JedisCluster;
import redis.clients.jedis.HostAndPort;

Set nodes = new HashSet<>();
nodes.add(new HostAndPort("192.168.1.100", 7000));
nodes.add(new HostAndPort("192.168.1.100", 7001));
nodes.add(new HostAndPort("192.168.1.100", 7002));

JedisCluster cluster = new JedisCluster(
    nodes,
    2000,
    2000,
    5,
    "clusterpassword123",
    new GenericObjectPoolConfig()
);

cluster.set("key", "value");
String value = cluster.get("key");

cluster.close();
```

**Node.js 示例**

```javascript
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
  { host: '192.168.1.100', port: 7000 },
  { host: '192.168.1.100', port: 7001 },
  { host: '192.168.1.100', port: 7002 }
], {
  redisOptions: {
    password: 'clusterpassword123'
  }
});

await cluster.set('key', 'value');
const value = await cluster.get('key');
```

### 3.9 Hash Tag

在 Cluster 模式下，如果需要确保多个 key 在同一个节点上（例如批量操作），可以使用 Hash Tag。

```bash
# 使用 {} 包裹的部分用于计算槽位
SET {user:1001}:name "张三"
SET {user:1001}:age 25
SET {user:1001}:email "zhangsan@example.com"

# 这三个 key 会被分配到同一个槽位
# 可以使用 MGET 批量获取
MGET {user:1001}:name {user:1001}:age {user:1001}:email
```

## 4. 最佳实践

### 4.1 主从复制最佳实践

1. **合理配置从节点数量**
   - 通常 1-2 个从节点即可
   - 过多从节点会增加主节点负担

2. **启用持久化**
   - 主节点和从节点都应启用持久化
   - 推荐使用 AOF + RDB 混合持久化

3. **网络优化**
   - 主从节点尽量在同一机房
   - 使用高速网络连接

4. **监控复制延迟**
   - 定期检查 `master_link_status` 和 `master_last_io_seconds_ago`
   - 设置告警阈值

5. **避免全量复制**
   - 合理配置 `repl-backlog-size`
   - 避免主节点重启

### 4.2 Sentinel 最佳实践

1. **部署奇数个 Sentinel**
   - 至少 3 个 Sentinel 节点
   - 推荐 3 或 5 个节点

2. **分散部署**
   - Sentinel 节点分散在不同机器
   - 避免单点故障

3. **合理配置参数**
   - `down-after-milliseconds`：不要设置太小，避免误判
   - `failover-timeout`：根据网络情况调整
   - `quorum`：通常设置为 Sentinel 数量的一半 + 1

4. **监控 Sentinel 状态**
   - 定期检查 Sentinel 日志
   - 监控故障转移次数

5. **客户端配置**
   - 使用 Sentinel 客户端库
   - 配置所有 Sentinel 节点地址

### 4.3 Cluster 最佳实践

1. **合理规划节点数量**
   - 至少 6 个节点（3 主 3 从）
   - 根据数据量和 QPS 规划节点数

2. **均匀分配槽位**
   - 确保每个主节点负责的槽位数量相近
   - 定期检查槽位分布

3. **使用 Hash Tag**
   - 对于需要批量操作的 key 使用 Hash Tag
   - 避免跨节点操作

4. **监控集群状态**
   - 定期检查 `cluster_state`
   - 监控节点间通信延迟

5. **扩容和缩容**
   - 在业务低峰期进行
   - 逐步迁移槽位，避免影响服务

6. **客户端配置**
   - 使用支持 Cluster 的客户端库
   - 配置多个节点地址
   - 启用自动重定向

### 4.4 性能优化

1. **网络优化**
   - 使用高速网络
   - 减少网络延迟

2. **内存优化**
   - 合理配置 `maxmemory`
   - 使用合适的淘汰策略

3. **持久化优化**
   - RDB：调整 `save` 参数
   - AOF：使用 `everysec` 策略

4. **慢查询优化**
   - 避免使用 `KEYS *`
   - 使用 `SCAN` 代替 `KEYS`
   - 避免大 key

### 4.5 安全建议

1. **启用密码认证**
   - 设置强密码
   - 定期更换密码

2. **网络隔离**
   - 使用防火墙限制访问
   - 只允许可信 IP 访问

3. **禁用危险命令**
   ```conf
   rename-command FLUSHDB ""
   rename-command FLUSHALL ""
   rename-command CONFIG ""
   ```

4. **启用 TLS/SSL**
   - 加密客户端和服务器之间的通信
   - 加密节点间通信

### 4.6 故障排查

1. **主从复制问题**
   - 检查网络连接
   - 检查密码配置
   - 查看复制偏移量

2. **Sentinel 故障转移失败**
   - 检查 quorum 配置
   - 检查从节点状态
   - 查看 Sentinel 日志

3. **Cluster 槽位迁移失败**
   - 检查节点状态
   - 检查网络连接
   - 查看迁移进度

4. **性能问题**
   - 使用 `INFO` 命令查看统计信息
   - 使用 `SLOWLOG` 查看慢查询
   - 使用 `MONITOR` 监控命令执行

## 参考资源

- [Redis 官方文档 - Replication](https://redis.io/topics/replication)
- [Redis 官方文档 - Sentinel](https://redis.io/topics/sentinel)
- [Redis 官方文档 - Cluster](https://redis.io/topics/cluster-tutorial)
- [Redis 中文网](http://www.redis.cn/)
