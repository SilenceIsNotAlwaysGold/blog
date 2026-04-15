---
title: "全局设置部分"
summary: "配置文件说明 `user`：指定Nginx工作进程的用户。 `worker_processes`：设置工作进程数，通常设置为CPU核心数。 `error_log`：指定错误日志文件及日志级别。 `pid`：指定PID文件位置。 `events`：配置事件模块。 `worker_connections`：每个工作进程的最大连接数。"
board: "tech"
category: "Web服务器"
tags:
  - "Nginx"
  - "Web服务器"
  - "反向代理"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

```nginx
# 全局设置部分
user  nginx;  # 指定Nginx工作进程的用户
worker_processes  auto;  # 自动调整工作进程数，通常设置为CPU核心数

# 错误日志配置
error_log  /var/log/nginx/error.log warn;  # 错误日志文件及日志级别
pid        /var/run/nginx.pid;  # PID文件位置

# 事件模块配置
events {
    worker_connections  1024;  # 每个工作进程的最大连接数
}

# HTTP模块配置
http {
    include       /etc/nginx/mime.types;  # 媒体类型映射表
    default_type  application/octet-stream;  # 默认文件类型

    # 日志格式定义
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;  # 访问日志文件及日志格式

    sendfile        on;  # 启用高效文件传输模式
    #tcp_nopush     on;

    keepalive_timeout  65;  # 保持连接的超时时间

    #gzip  on;  # 启用Gzip压缩

    # 限制连接数和请求速率
    limit_conn_zone $binary_remote_addr zone=addr:10m;  # 定义连接数限制区域
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;  # 定义请求速率限制区域

    include /etc/nginx/conf.d/*.conf;  # 包含虚拟主机配置文件
}

# 虚拟主机配置示例
server {
    listen       80;  # 监听端口
    server_name  example.com www.example.com;  # 配置域名

    location / {
        root   /usr/share/nginx/html;  # 设置站点根目录
        index  index.html index.htm;  # 设置默认首页文件
        limit_conn addr 5;  # 每个IP的最大连接数
        limit_req zone=one burst=10 nodelay;  # 请求速率限制
    }

    # 错误页配置
    error_page  404              /404.html;
    location = /40x.html {
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
    }
}

# 反向代理配置示例
server {
    listen       80;
    server_name  backend.example.com;

    location / {
        proxy_pass http://backend_servers;  # 转发请求到后端服务器
        proxy_set_header Host $host;  # 设置请求头部信息
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 定义后端服务器组
upstream backend_servers {
    server 127.0.0.1:8080;
    server 127.0.0.1:8081;
}

# SSL/TLS 配置示例
server {
    listen 443 ssl;  # 监听443端口
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/nginx.crt;  # SSL证书文件
    ssl_certificate_key /etc/nginx/ssl/nginx.key;  # SSL证书密钥文件

    ssl_session_cache shared:SSL:1m;  # SSL会话缓存
    ssl_session_timeout  10m;  # SSL会话超时时间
    ssl_ciphers HIGH:!aNULL:!MD5;  # SSL加密套件
    ssl_prefer_server_ciphers on;  # 优先使用服务器的加密套件

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}

# 重定向所有HTTP请求到HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### 配置文件说明
+ `user`：指定Nginx工作进程的用户。
+ `worker_processes`：设置工作进程数，通常设置为CPU核心数。
+ `error_log`：指定错误日志文件及日志级别。
+ `pid`：指定PID文件位置。
+ `events`：配置事件模块。
    - `worker_connections`：每个工作进程的最大连接数。
+ `http`：HTTP模块配置。
    - `include`：包含媒体类型映射表。
    - `default_type`：默认文件类型。
    - `log_format`：定义日志格式。
    - `access_log`：指定访问日志文件及日志格式。
    - `sendfile`：启用高效文件传输模式。
    - `keepalive_timeout`：保持连接的超时时间。
    - `limit_conn_zone`：定义连接数限制区域。
    - `limit_req_zone`：定义请求速率限制区域。
    - `include`：包含虚拟主机配置文件。

### 虚拟主机配置
+ `server`：定义一个虚拟主机。
    - `listen`：监听端口。
    - `server_name`：配置域名。
    - `location`：定义请求的处理方式。
        * `root`：设置站点根目录。
        * `index`：设置默认首页文件。
        * `limit_conn`：限制每个IP的最大连接数。
        * `limit_req`：请求速率限制。

### 反向代理配置
+ `server`：定义一个虚拟主机。
    - `listen`：监听端口。
    - `server_name`：配置域名。
    - `location`：定义请求的处理方式。
        * `proxy_pass`：转发请求到后端服务器。
        * `proxy_set_header`：设置请求头部信息。

### SSL/TLS 配置
+ `server`：定义一个虚拟主机。
    - `listen`：监听443端口。
    - `server_name`：配置域名。
    - `ssl_certificate`：SSL证书文件。
    - `ssl_certificate_key`：SSL证书密钥文件。
    - `ssl_session_cache`：SSL会话缓存。
    - `ssl_session_timeout`：SSL会话超时时间。
    - `ssl_ciphers`：SSL加密套件。
    - `ssl_prefer_server_ciphers`：优先使用服务器的加密套件。
    - `location`：定义请求的处理方式。

### 重定向HTTP到HTTPS
+ `server`：定义一个虚拟主机。
    - `listen`：监听80端口。
    - `server_name`：配置域名。
    - `return`：重定向到HTTPS。
