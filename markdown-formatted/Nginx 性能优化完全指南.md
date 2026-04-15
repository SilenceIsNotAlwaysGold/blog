---
title: "Nginx 性能优化完全指南"
summary: "深入探讨 Nginx 性能优化的关键策略，从工作进程配置、连接数限制到 Gzip 压缩和缓冲区调整，帮助你构建高性能的 Web 服务器。"
board: "tech"
category: "Web服务器"
tags:
  - "Nginx"
  - "性能优化"
  - "WebServer"
  - "运维"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Nginx 性能优化完全指南

Nginx 以其高性能和低内存占用而闻名，但默认配置往往无法发挥其最大潜力。本文将详细介绍如何调整 Nginx 配置以适应高并发场景，提升服务器的响应速度和吞吐量。

## 1. 核心进程配置

### Worker Processes

`worker_processes` 定义了 Nginx 运行的工作进程数。最佳实践是将其设置为 CPU 核心数。

```nginx
# nginx.conf
user nginx;
# 自动检测 CPU 核心数
worker_processes auto;

# 绑定 worker 到指定 CPU 核心，减少上下文切换
worker_cpu_affinity auto;
```

### Worker Connections

`worker_connections` 决定了每个工作进程可以打开的最大连接数。

```nginx
events {
    # 每个 worker 进程的最大连接数
    # 最大客户端数 = worker_processes * worker_connections
    worker_connections 65535;

    # 优化 I/O 模型，Linux 下使用 epoll
    use epoll;

    # 允许一个进程同时接受多个新连接
    multi_accept on;
}
```

> **注意**：需要同步调整操作系统的文件描述符限制（`ulimit -n`）。

## 2. HTTP 核心模块优化

### 开启高效传输模式

```nginx
http {
    include       mime.types;
    default_type  application/octet-stream;

    # 开启零拷贝技术，减少上下文切换
    sendfile        on;

    # 在 sendfile 开启时，将数据包累积到一定大小再发送
    tcp_nopush      on;

    # 禁用 Nagle 算法，尽快发送数据，降低延迟
    tcp_nodelay     on;

    # 保持连接超时时间
    keepalive_timeout  65;

    # 隐藏 Nginx 版本号，提高安全性
    server_tokens off;
}
```

## 3. Gzip 压缩优化

开启 Gzip 压缩可以显著减少传输数据量，提高页面加载速度，但会消耗 CPU 资源。

```nginx
http {
    gzip on;
    # 启用压缩的最小文件大小
    gzip_min_length 1k;
    # 压缩缓冲区
    gzip_buffers 4 16k;
    # 压缩版本
    gzip_http_version 1.1;
    # 压缩级别 1-9，建议 4-6，平衡 CPU 和压缩率
    gzip_comp_level 5;
    # 需要压缩的 MIME 类型
    gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
    # 在响应头中添加 Vary: Accept-Encoding
    gzip_vary on;
    # 禁用 IE6 压缩
    gzip_disable "MSIE [1-6]\.";
}
```

## 4. 缓冲区与超时设置

合理的缓冲区和超时设置可以防止资源耗尽攻击，并优化大文件上传。

```nginx
http {
    # 客户端请求头缓冲区大小
    client_header_buffer_size 1k;
    # 大请求头缓冲区
    large_client_header_buffers 4 4k;

    # 客户端请求体最大限制
    client_max_body_size 10m;
    # 客户端请求体缓冲区
    client_body_buffer_size 128k;

    # 客户端请求头读取超时
    client_header_timeout 10;
    # 客户端请求体读取超时
    client_body_timeout 10;
    # 响应客户端超时
    send_timeout 10;
}
```

## 5. 静态文件缓存

为静态资源设置缓存过期时间，减少服务器负载。

```nginx
server {
    # 图片缓存 30 天
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires      30d;
        error_log off;
        access_log off;
    }

    # JS/CSS 缓存 12 小时
    location ~ .*\.(js|css)?$ {
        expires      12h;
        error_log off;
        access_log off;
    }
}
```

## 6. 日志优化

在高并发场景下，频繁写入日志会影响 I/O 性能。

```nginx
# 定义日志格式
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                  '$status $body_bytes_sent "$http_referer" '
                  '"$http_user_agent" "$http_x_forwarded_for"';

# 使用 buffer 缓冲写入，flush 刷新时间
access_log  /var/log/nginx/access.log  main buffer=32k flush=5s;

# 关闭 favicon.ico 和 robots.txt 的日志记录
location = /favicon.ico {
    log_not_found off;
    access_log off;
}
```

## 7. Linux 内核参数调优

除了 Nginx 配置，操作系统的网络参数也至关重要。编辑 `/etc/sysctl.conf`：

```bash
# 允许等待中的 socket 队列大小
net.core.somaxconn = 65535

# TCP 连接回收与复用
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0 # 新版内核建议关闭
net.ipv4.tcp_fin_timeout = 30

# 端口范围
net.ipv4.ip_local_port_range = 1024 65535

# SYN 队列长度
net.ipv4.tcp_max_syn_backlog = 65535
```

执行 `sysctl -p` 生效。

## 总结

Nginx 性能优化是一个系统工程，需要结合具体的硬件配置和业务场景。建议遵循以下步骤：
1. 调整 Worker 进程和连接数。
2. 开启 Gzip 和 Sendfile。
3. 配置合理的超时和缓冲区。
4. 优化静态资源缓存。
5. 配合内核参数调优。

通过这些设置，你的 Nginx 服务器将能够从容应对更高的并发流量。
