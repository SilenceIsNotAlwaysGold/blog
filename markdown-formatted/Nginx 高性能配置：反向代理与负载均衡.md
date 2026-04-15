---
title: "Nginx 高性能配置：反向代理与负载均衡"
category: "Web服务器"
board: "tech"
tags: ["Nginx", "反向代理", "负载均衡", "SSL"]
summary: "Nginx 生产级配置实战，涵盖 upstream 负载均衡、限流、SSL/TLS、WebSocket 代理与缓存策略"
is_published: true
created_at: "2024-11-08T10:00:00Z"
updated_at: "2024-11-08T10:00:00Z"
---

# Nginx 高性能配置：反向代理与负载均衡

Nginx 是生产环境最常用的反向代理和负载均衡器。本文不讲基础安装，直接进入生产级配置方案。

## 一、核心配置优化

### 1.1 主配置文件

```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes auto;  # 自动匹配 CPU 核数
worker_rlimit_nofile 65535;
pid /run/nginx.pid;

events {
    worker_connections 10240;
    use epoll;           # Linux 下用 epoll
    multi_accept on;     # 一个 worker 同时接受多个连接
}

http {
    # 基础配置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;
    types_hash_max_size 2048;
    server_tokens off;   # 隐藏 Nginx 版本号
    
    # 请求体大小限制
    client_max_body_size 20m;
    client_body_buffer_size 128k;
    
    # 超时配置
    proxy_connect_timeout 10s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 4;       # 4 是性价比最高的压缩级别
    gzip_min_length 256;
    gzip_types
        text/plain text/css text/xml text/javascript
        application/json application/javascript application/xml
        application/rss+xml image/svg+xml;
    
    # 日志格式
    log_format json_combined escape=json
        '{'
            '"time":"$time_iso8601",'
            '"remote_addr":"$remote_addr",'
            '"request":"$request",'
            '"status":$status,'
            '"body_bytes_sent":$body_bytes_sent,'
            '"request_time":$request_time,'
            '"upstream_response_time":"$upstream_response_time",'
            '"http_user_agent":"$http_user_agent",'
            '"http_x_request_id":"$http_x_request_id"'
        '}';
    
    access_log /var/log/nginx/access.log json_combined buffer=32k flush=5s;
    error_log /var/log/nginx/error.log warn;
    
    include /etc/nginx/conf.d/*.conf;
}
```

## 二、upstream 负载均衡

### 2.1 多种负载均衡策略

```nginx
# 加权轮询（默认）
upstream backend_servers {
    server 10.0.0.1:8000 weight=5;    # 权重高，分配更多请求
    server 10.0.0.2:8000 weight=3;
    server 10.0.0.3:8000 weight=2;
    
    keepalive 32;  # 保持长连接，减少握手开销
}

# IP Hash（同一 IP 始终路由到同一后端）
upstream backend_sticky {
    ip_hash;
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    server 10.0.0.3:8000;
}

# 最少连接数
upstream backend_least {
    least_conn;
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
}

# 带健康检查的配置
upstream backend_health {
    server 10.0.0.1:8000 max_fails=3 fail_timeout=30s;
    server 10.0.0.2:8000 max_fails=3 fail_timeout=30s;
    server 10.0.0.3:8000 backup;  # 备用服务器，其他都挂了才启用
}
```

### 2.2 反向代理配置

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    # 强制跳转 HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    # SSL 配置（见下文）
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # API 代理
    location /api/ {
        proxy_pass http://backend_servers;
        
        # 传递真实 IP
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Request-ID $request_id;
        
        # 长连接
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # 缓冲配置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 16k;
        proxy_busy_buffers_size 32k;
    }
    
    # 静态文件
    location /static/ {
        alias /usr/share/nginx/html/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # 前端 SPA
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        
        # HTML 不缓存
        location = /index.html {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
        }
    }
}
```

## 三、限流配置

### 3.1 请求速率限制

```nginx
http {
    # 定义限流区域（按 IP 限制，10m 内存可存约 16 万个 IP）
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login_limit:5m rate=1r/s;
    
    # 连接数限制
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

server {
    # API 限流：每秒 10 个请求，突发允许 20 个排队
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req_status 429;
        
        # 连接数限制：每 IP 最多 50 个并发连接
        limit_conn conn_limit 50;
        
        proxy_pass http://backend_servers;
    }
    
    # 登录接口严格限流
    location /api/auth/login {
        limit_req zone=login_limit burst=3 nodelay;
        limit_req_status 429;
        
        proxy_pass http://backend_servers;
    }
    
    # 自定义 429 响应
    error_page 429 = @rate_limited;
    location @rate_limited {
        default_type application/json;
        return 429 '{"error": "Too many requests", "retry_after": 1}';
    }
}
```

### 3.2 按接口差异化限流

```nginx
# 不同接口不同限流策略
map $uri $limit_zone {
    ~^/api/auth/    login_limit;
    ~^/api/upload   upload_limit;
    default         api_limit;
}
```

## 四、SSL/TLS 配置

### 4.1 安全的 SSL 配置

```nginx
# /etc/nginx/conf.d/ssl.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# 会话复用（减少 TLS 握手）
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;

# HSTS（浏览器强制 HTTPS）
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

### 4.2 安全头

```nginx
# 安全头配置
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'" always;
```

## 五、WebSocket 代理

```nginx
# WebSocket 需要特殊的升级头
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream websocket_backend {
    server 10.0.0.1:8001;
    server 10.0.0.2:8001;
}

server {
    location /ws/ {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket 超时设置（默认 60s 会断开）
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```

## 六、缓存配置

### 6.1 代理缓存

```nginx
http {
    # 定义缓存路径
    proxy_cache_path /var/cache/nginx 
        levels=1:2 
        keys_zone=api_cache:10m 
        max_size=1g 
        inactive=60m 
        use_temp_path=off;
}

server {
    location /api/articles {
        proxy_cache api_cache;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        proxy_cache_valid 200 10m;      # 200 响应缓存 10 分钟
        proxy_cache_valid 404 1m;       # 404 缓存 1 分钟
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503;
        
        # 添加缓存状态头（调试用）
        add_header X-Cache-Status $upstream_cache_status;
        
        # 绕过缓存条件
        proxy_cache_bypass $http_authorization;  # 有认证头不走缓存
        proxy_no_cache $http_authorization;
        
        proxy_pass http://backend_servers;
    }
}
```

### 6.2 浏览器缓存策略

```nginx
# 静态资源（带 hash 的文件名）：长期缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# API 响应：不缓存
location /api/ {
    add_header Cache-Control "no-store, no-cache, must-revalidate";
    add_header Pragma "no-cache";
}
```

## 七、监控与调试

### 7.1 状态监控

```nginx
# 开启 stub_status
location /nginx_status {
    stub_status;
    allow 10.0.0.0/8;
    deny all;
}
```

```bash
# 监控输出
Active connections: 256
server accepts handled requests
 12345678 12345678 45678901
Reading: 5 Writing: 30 Waiting: 221
```

### 7.2 常见故障排查

```bash
# 检查配置语法
nginx -t

# 查看错误日志
tail -f /var/log/nginx/error.log

# 常见错误
# 502 Bad Gateway：后端服务挂了或响应超时
# 504 Gateway Timeout：后端处理太慢，增加 proxy_read_timeout
# 413 Request Entity Too Large：增加 client_max_body_size
# 499 Client Closed Request：客户端主动断开，检查后端响应速度
```

## 八、实际部署配置模板

我在生产中使用的典型配置结构：

```
/etc/nginx/
├── nginx.conf              # 主配置
├── conf.d/
│   ├── ssl.conf           # SSL 通用配置
│   ├── security.conf      # 安全头
│   ├── gzip.conf          # 压缩配置
│   ├── api.example.com.conf  # API 站点
│   └── www.example.com.conf  # 前端站点
└── ssl/
    ├── fullchain.pem
    └── privkey.pem
```

## 总结

Nginx 生产配置要点：

1. **worker_processes auto**：自动匹配 CPU，别写死
2. **upstream keepalive**：保持后端长连接，减少 TCP 握手
3. **限流是必须的**：按 IP 和接口差异化限流，防止恶意请求
4. **SSL 最低 TLSv1.2**：配置 HSTS、OCSP Stapling
5. **缓存分层**：静态资源浏览器缓存，API 用代理缓存
6. **日志用 JSON 格式**：方便后续 ELK 收集分析
7. **server_tokens off**：永远隐藏版本号
