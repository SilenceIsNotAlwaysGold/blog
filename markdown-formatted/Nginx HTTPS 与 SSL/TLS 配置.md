---
title: "Nginx HTTPS 与 SSL/TLS 配置"
summary: "全面讲解如何在 Nginx 中配置 HTTPS，包括 SSL 证书申请、TLS 优化、HSTS 配置以及 HTTP/2 的开启，保障网站安全与速度。"
board: "tech"
category: "Web服务器"
tags:
  - "Nginx"
  - "HTTPS"
  - "SSL"
  - "安全"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Nginx HTTPS 与 SSL/TLS 配置

随着网络安全意识的提升，HTTPS 已成为网站的标配。本文将指导你如何在 Nginx 上配置稳健且高效的 HTTPS 服务，包括证书配置、强制跳转、安全优化和 HTTP/2 支持。

## 1. 准备 SSL 证书

你需要两个文件：
- `example.com.crt` (公钥证书，包含证书链)
- `example.com.key` (私钥)

通常证书颁发机构（CA）会提供这些文件。如果是 Let's Encrypt，文件通常位于 `/etc/letsencrypt/live/example.com/`。

## 2. 基础 HTTPS 配置

在 `server` 块中开启 SSL 监听。

```nginx
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # 证书路径
    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;

    # 网站根目录
    root /var/www/html;
    index index.html index.php;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 3. HTTP 强制跳转 HTTPS

为了确保所有访问都加密，需要将 HTTP (80) 请求重定向到 HTTPS (443)。

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    # 301 永久重定向
    return 301 https://$host$request_uri;
}
```

## 4. SSL/TLS 安全优化

默认的 SSL 配置可能存在安全隐患。以下是 Mozilla 推荐的现代兼容性配置。

### 协议与加密套件

```nginx
# 禁用过时的 SSLv3, TLS 1.0, TLS 1.1
ssl_protocols TLSv1.2 TLSv1.3;

# 优先使用服务器加密套件
ssl_prefer_server_ciphers on;

# 推荐的加密套件列表
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
```

### 优化 SSL 会话

减少 SSL 握手开销，提高页面加载速度。

```nginx
# 启用 SSL Session Cache
ssl_session_cache shared:SSL:10m; # 10MB 可存储约 40000 个会话
ssl_session_timeout 10m; # 会话超时时间
ssl_session_tickets off; # 禁用 Session Ticket (除非配置了 key rotation)
```

### 配置 Diffie-Hellman 参数

生成更强的 DH 参数文件：

```bash
openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

Nginx 配置：

```nginx
ssl_dhparam /etc/nginx/ssl/dhparam.pem;
```

## 5. 启用 HSTS (HTTP Strict Transport Security)

HSTS 告诉浏览器该网站只能通过 HTTPS 访问，防止中间人攻击。

```nginx
# max-age 单位是秒，31536000 即一年
# includeSubDomains 应用于子域名
# preload 允许申请加入浏览器的 HSTS 预加载列表
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

## 6. 启用 HTTP/2

HTTP/2 相比 HTTP/1.1 有显著的性能提升（多路复用、头部压缩）。

只需在 `listen` 指令后添加 `http2`：

```nginx
listen 443 ssl http2;
```

## 7. 完整配置示例

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    root /var/www/html;
    index index.html;

    # 证书配置
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_dhparam /etc/nginx/ssl/dhparam.pem;

    # SSL 优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全 Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 8. 验证配置

配置完成后，使用以下命令检查语法并重载：

```bash
nginx -t
systemctl reload nginx
```

你可以使用 [SSL Labs](https://www.ssllabs.com/ssltest/) 在线工具测试你的 HTTPS 配置评级，目标是获得 A+。

## 总结

配置 HTTPS 不仅仅是安装证书，还包括选择安全的协议、优化握手性能以及配置 HSTS 等安全头。遵循本文的配置，你可以构建一个既安全又快速的 HTTPS 站点。
