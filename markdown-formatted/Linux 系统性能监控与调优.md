---
title: "Linux 系统性能监控与调优"
summary: "深入解析 Linux 性能分析方法论（USE 方法），利用 vmstat、iostat、sar 等工具定位 CPU、内存、磁盘 IO 瓶颈，并提供相应的内核调优策略。"
board: "tech"
category: "Linux系统"
tags:
  - "Linux"
  - "性能监控"
  - "调优"
  - "运维"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Linux 系统性能监控与调优

当系统变慢时，如何快速定位瓶颈？是 CPU 吃紧、内存泄漏，还是磁盘 I/O 阻塞？本文将介绍一套系统的性能分析方法和工具链。

## 1. 分析方法论：USE 方法

Brendan Gregg 提出的 **USE 方法** 是性能分析的黄金法则，针对每个资源（CPU、内存、磁盘、网络），检查以下三项：

1. **Utilization (利用率)**: 资源被使用的时间百分比。
2. **Saturation (饱和度)**: 资源排队任务的长度（如等待队列）。
3. **Errors (错误)**: 错误事件的计数。

## 2. CPU 性能分析

### 监控工具
- **top / htop**: 查看实时负载 (Load Average)。
- **vmstat 1**: 查看上下文切换 (`cs`) 和运行队列 (`r`)。
- **mpstat -P ALL 1**: 查看每个核心的详细使用率。

### 关键指标
- **Load Average**: 如果超过 CPU 核心数，说明 CPU 饱和。
- **User vs System**: User 高通常是应用程序逻辑复杂；System 高可能是系统调用频繁或驱动问题。
- **Context Switches**: 过高会导致 CPU 把大量时间花在切换进程上。

### 调优策略
- 绑定进程到特定 CPU 核 (`taskset`)。
- 调整进程优先级 (`nice` / `renice`)。
- 优化代码算法。

## 3. 内存性能分析

### 监控工具
- **free -h**: 查看内存总量、已用、Buffer/Cache。
- **vmstat 1**: 查看 swap 换入换出 (`si`/`so`)。

### 关键指标
- **Swap 使用**: 如果 `si`/`so` 频繁变化，说明内存不足，系统在抖动（Thrashing），性能会急剧下降。
- **Buffer/Cache**: Linux 会将空闲内存用作缓存，这部分高是正常的。

### 调优策略
- 调整 `vm.swappiness`: 控制使用 Swap 的积极程度（0-100，默认 60，服务器建议调低如 10）。
- 限制应用内存（如 Java Heap、Docker Limit）。
- 检查内存泄漏。

## 4. 磁盘 I/O 性能分析

### 监控工具
- **iostat -xz 1**: 最权威的 I/O 监控工具。
- **iotop**: 类似 top，查看哪个进程在读写磁盘。

### 关键指标
- **%util**: 磁盘利用率。接近 100% 说明磁盘饱和。
- **await**: I/O 请求平均等待时间。如果远大于 svctm，说明队列堆积严重。
- **avgqu-sz**: 平均请求队列长度。

### 调优策略
- 选用 SSD 硬盘。
- 调整 I/O 调度算法 (Noop, Deadline, CFQ)。
- 优化应用读写策略（顺序写优于随机写，批量刷盘）。

## 5. 网络性能分析

### 监控工具
- **sar -n DEV 1**: 查看网卡流量。
- **netstat -s**: 查看网络协议栈统计信息。
- **iftop**: 查看带宽占用详情。

### 关键指标
- **rxpck/s, txpck/s**: 每秒收发包数量。
- **drop / error**: 丢包和错误数。

### 调优策略
- 调整内核 TCP 参数 (`sysctl.conf`)。
- 开启网卡多队列。

## 6. 实战：sysctl.conf 内核调优

以下是一份常见的 Web 服务器 `/etc/sysctl.conf` 优化配置：

```bash
# 增加文件打开数限制 (需配合 ulimit)
fs.file-max = 655350

# 开启 TCP SYN Cookies 防御洪水攻击
net.ipv4.tcp_syncookies = 1

# 允许重用 TIME-WAIT sockets
net.ipv4.tcp_tw_reuse = 1

# 减少 FIN-WAIT-2 时间
net.ipv4.tcp_fin_timeout = 30

# 增加 TCP 接收和发送缓冲区
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# 增加连接追踪表大小 (防止 "table full, dropping packet")
net.netfilter.nf_conntrack_max = 1048576
```

## 7. 总结

性能调优是一个"发现瓶颈 -> 调整 -> 验证"的循环过程。
1. **不要过早优化**：先有测量，再有优化。
2. **全局视角**：CPU、内存、I/O 是相互影响的。
3. **掌握神器**：熟练使用 `vmstat`, `iostat`, `strace`, `perf` 等工具。

保持系统监控的可视化（如 Prometheus + Grafana），能让你在问题发生前就察觉端倪。
