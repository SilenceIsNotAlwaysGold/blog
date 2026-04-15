---
title: "Redis主从复制和集群配置"
summary: "Redis 主从复制配置 什么是主从复制 Redis的主从复制（Replication）是指将数据从一个主节点（Master）复制到一个或多个从节点（Slave）。主从复制实现了读写分离，主节点负责写操作，从节点负责读操作，从而提高了系统的读性能和数据冗余。 主从复制的配置步骤 **安装Redis**：确保在所有节点上安装Redis。"
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

### Redis 主从复制配置
#### 什么是主从复制
Redis的主从复制（Replication）是指将数据从一个主节点（Master）复制到一个或多个从节点（Slave）。主从复制实现了读写分离，主节点负责写操作，从节点负责读操作，从而提高了系统的读性能和数据冗余。

#### 主从复制的配置步骤
1. **安装Redis**：确保在所有节点上安装Redis。
2. **配置主节点**：

主节点无需特殊配置，只需启动Redis服务即可。

```bash
redis-server /path/to/redis.conf
```

1. **配置从节点**：

在从节点的配置文件中添加以下配置，将``和``替换为主节点的IP地址和端口号：

```properties
replicaof  
```

示例：

```properties
replicaof 192.168.1.100 6379
```

然后启动从节点：

```bash
redis-server /path/to/redis.conf
```

1. **验证主从复制**：

在主节点上设置一个键：

```bash
redis-cli set key1 value1
```

在从节点上检查该键是否存在：

```bash
redis-cli get key1
```

如果从节点返回相同的值，则表示主从复制配置成功。

### Redis Sentinel 配置
#### 什么是Sentinel
Redis Sentinel用于监控Redis主从实例，自动进行故障转移。Sentinel可以检测主节点故障，并将某个从节点提升为新的主节点，从而确保Redis服务的高可用性。

#### Sentinel的配置步骤
1. **安装Redis Sentinel**：Sentinel随Redis一起安装，不需要额外安装。
2. **配置Sentinel**：

创建Sentinel配置文件`sentinel.conf`，添加以下配置，将``和``替换为主节点的IP地址和端口号：

```properties
port 26379
sentinel monitor mymaster   2
sentinel auth-pass mymaster 
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000
```

示例：

```properties
port 26379
sentinel monitor mymaster 192.168.1.100 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000
```

1. **启动Sentinel**：

```bash
redis-sentinel /path/to/sentinel.conf
```

1. **验证Sentinel**：

使用`redis-cli`连接Sentinel实例，执行以下命令查看Sentinel状态：

```bash
redis-cli -p 26379
sentinel masters
sentinel slaves mymaster
```

### Redis 集群配置
#### 什么是Redis集群
Redis集群（Cluster）是一个分布式解决方案，通过数据分片和主从复制实现高可用性和扩展性。集群中的数据分布在多个节点上，每个节点负责一部分数据，并可以有一个或多个从节点作为备份。

#### 集群的配置步骤
1. **安装Redis**：确保在所有节点上安装Redis。
2. **配置集群节点**：

在每个节点的配置文件中添加以下配置：

```properties
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

1. **启动集群节点**：

在每个节点上启动Redis服务：

```bash
redis-server /path/to/redis.conf
```

1. **创建集群**：

使用`redis-cli`创建集群，将``替换为集群节点的IP地址：

```bash
redis-cli --cluster create :6379 :6379 :6379 :6379 :6379 :6379 --cluster-replicas 1
```

示例：

```bash
redis-cli --cluster create 192.168.1.101:6379 192.168.1.102:6379 192.168.1.103:6379 192.168.1.104:6379 192.168.1.105:6379 192.168.1.106:6379 --cluster-replicas 1
```

上述命令将创建一个包含6个节点的集群，每个主节点有一个从节点作为备份。

1. **验证集群**：

使用`redis-cli`连接任意一个集群节点，执行以下命令查看集群状态：

```bash
redis-cli -c -p 6379
cluster info
cluster nodes
```

### 参考配置文件示例
#### 主节点配置（redis.conf）
```properties
port 6379
bind 0.0.0.0
appendonly yes
```

#### 从节点配置（redis.conf）
```properties
port 6379
bind 0.0.0.0
replicaof 192.168.1.100 6379
appendonly yes
```

#### Sentinel配置（sentinel.conf）
```properties
port 26379
sentinel monitor mymaster 192.168.1.100 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000
```

#### 集群节点配置（redis.conf）
```properties
port 6379
bind 0.0.0.0
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```
