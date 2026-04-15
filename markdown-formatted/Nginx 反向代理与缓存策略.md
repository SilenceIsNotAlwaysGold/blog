---
title: "Nginx 反向代理与缓存策略"
summary: "详细介绍 Nginx 反向代理配置，以及如何利用 proxy_cache 模块实现静态和动态内容的缓存，降低后端负载，提升网站响应速度。"
board: "tech"
category: "Web服务器"
tags:
  - "Nginx"
  - "反向代理"
  - "缓存"
  - "CDN"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Nginx 反向代理与缓存策略

Nginx 最核心的功能之一就是反向代理。除了简单的转发请求，合理配置代理缓存（Proxy Cache）可以将 Nginx 变成一个强大的内容分发节点（类似 CDN），大幅降低后端应用服务器的压力。

## 1. 反向代理基础

反向代理是指代理服务器接受客户端请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给客户端。

### 基本语法

```nginx
location /api/ {
    # 转发地址
    proxy_pass http://backend_server:8080/;

    # 传递 Host 头，否则后端可能无法识别域名
    proxy_set_header Host $host;

    # 传递真实 IP
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # 协议头 (http/https)
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### URL 尾部斜杠问题

`proxy_pass` URL 末尾是否有斜杠 `/` 行为不同：

- `proxy_pass http://127.0.0.1:8080/;` (有斜杠)：绝对路径替换。请求 `/api/user` 会被代理为 `/user`。
- `proxy_pass http://127.0.0.1:8080;` (无斜杠)：相对路径追加。请求 `/api/user` 会被代理为 `/api/user`。

## 2. Nginx 代理缓存 (Proxy Cache)

Nginx 可以将后端服务器的响应缓存到本地磁盘，下次相同请求直接由 Nginx 返回，无需经过后端。

### 步骤 1: 定义缓存路径 (在 http 块中)

```nginx
http {
    # path: 缓存存储路径
    # levels: 目录层级，1:2 表示两级目录
    # keys_zone: 缓存区名称及内存大小 (my_cache:10m)
    # max_size: 最大硬盘占用空间
    # inactive: 未被访问文件清理时间
    # use_temp_path: 是否使用临时目录，建议 off
    proxy_cache_path /var/cache/nginx/my_cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;
}
```

### 步骤 2: 启用缓存 (在 location 块中)

```nginx
server {
    location / {
        proxy_pass http://backend_upstream;

        # 指定使用的缓存区
        proxy_cache my_cache;

        # 针对不同的响应码设置缓存时间
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;

        # 缓存键值定义 (默认就是这个)
        proxy_cache_key $host$uri$is_args$args;

        # 添加自定义头，用于调试查看是否命中缓存 (HIT/MISS)
        add_header X-Cache-Status $upstream_cache_status;

        # 出现错误时使用过期缓存响应，提高可用性
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;

        # 并发锁，防止缓存失效瞬间大量请求打到后端 (缓存风暴)
        proxy_cache_lock on;
    }
}
```

## 3. 缓存清理

Nginx 开源版默认不直接支持 `PURGE` 请求清理缓存（需要第三方模块 `ngx_cache_purge`）。但在商业版或特定配置下支持。

一种简单的手动清理方式是直接删除缓存文件：
`rm -rf /var/cache/nginx/my_cache/*`

## 4. 动静分离策略

最佳实践是将静态资源和动态 API 分开处理。

```nginx
# 静态资源：使用 Nginx 缓存或直接由 Nginx 提供服务
location ~* \.(jpg|jpeg|png|gif|css|js|ico)$ {
    proxy_pass http://backend;
    proxy_cache my_cache;
    proxy_cache_valid 200 30d;
    expires 30d;
}

# 动态接口：不缓存或短时间缓存
location /api/ {
    proxy_pass http://backend;
    # 通常不缓存 API，除非是读取频率高且变化少的数据
    proxy_cache off;
}
```

## 5. 浏览器缓存与服务端缓存配合

服务端缓存 (`proxy_cache`) 减轻了后端压力，浏览器缓存 (`expires` / `Cache-Control`) 减轻了 Nginx 压力。

```nginx
location /static/ {
    # 告诉浏览器缓存 7 天
    expires 7d;

    # Nginx 自身也缓存
    proxy_cache my_cache;
    proxy_cache_valid 200 7d;
}
```

## 6. 常见问题排查

- **缓存不生效**：检查后端响应头是否包含 `Cache-Control: no-cache` 或 `Set-Cookie`。默认情况下，Nginx 不会缓存带有 `Set-Cookie` 的响应。可以配置 `proxy_ignore_headers Set-Cookie;` 强制缓存，但需小心用户信息泄露。
- **X-Cache-Status**: 观察该 Header。
  - `MISS`: 未命中，回源获取。
  - `HIT`: 命中缓存。
  - `EXPIRED`: 缓存过期，回源更新。
  - `BYPASS`: 强制跳过缓存。

## 总结

通过 Nginx 的反向代理和缓存功能，我们可以：
1. **隐藏后端架构**，提高安全性。
2. **加速内容分发**，显著降低响应时间。
3. **削峰填谷**，在后端故障时仍能提供陈旧数据（Stale Content），提升用户体验。

合理配置缓存策略是 Web 性能优化的必修课。
