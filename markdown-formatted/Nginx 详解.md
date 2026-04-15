---
title: "Nginx 详解"
summary: "什么是Nginx Nginx 是一款自由的、开源的、高性能的 HTTP 服务器和反向代理服务器，同时也是一个 IMAP、POP3、SMTP 代理服务器。它以其高性能、高稳定性、丰富的功能集以及模块化的设计，成为许多企业的首选。 Nginx的作用 Nginx 可以作为一个 HTTP 服务器进行网站的发布处理，同时可以作为反向代理进行负载均衡的实现。"
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

### 1. 什么是Nginx
Nginx 是一款自由的、开源的、高性能的 HTTP 服务器和反向代理服务器，同时也是一个 IMAP、POP3、SMTP 代理服务器。它以其高性能、高稳定性、丰富的功能集以及模块化的设计，成为许多企业的首选。

### 2. Nginx的作用
Nginx 可以作为一个 HTTP 服务器进行网站的发布处理，同时可以作为反向代理进行负载均衡的实现。

### 3. 正向代理
#### 什么是正向代理
正向代理，"它代理的是客户端"，是一个位于客户端和原始服务器（Origin Server）之间的服务器。为了从原始服务器取得内容，客户端向代理发送一个请求并指定目标（原始服务器）。然后代理向原始服务器转交请求并将获得的内容返回给客户端。客户端必须要进行一些特别的设置才能使用正向代理。

#### 正向代理的用途
+ 访问原来无法访问的资源，如 Google。
+ 做缓存，加速访问资源。
+ 对客户端访问授权，上网进行认证。
+ 记录用户访问记录（上网行为管理），对外隐藏用户信息。

### 4. 反向代理
#### 反向代理举例
例如我国的某宝网站，每天同时连接到网站的访问人数已经爆表，单个服务器远远不能满足日益增长的购买欲望。通过分布式部署，通过多台服务器解决访问人数限制的问题。某宝网站中大部分功能通过Nginx进行反向代理实现，并通过封装Nginx和其他组件之后起了个名字：Tengine。

[Tengine文档](http://tengine.taobao.org/documentation_cn.html)

#### 什么是反向代理
反向代理，"它代理的是服务端"，主要用于服务器集群分布式部署的情况下，反向代理隐藏了服务器的信息。客户端是无感知代理的存在，反向代理对外都是透明的，访问者并不知道自己访问的是一个代理。

#### 反向代理的作用
+ 保证内网的安全，通常将反向代理作为公网访问地址，Web 服务器是内网。
+ 负载均衡，通过反向代理服务器来优化网站的负载。

### 5. 负载均衡
#### 什么是负载均衡
负载均衡是将服务器接收到的请求按照规则分发到不同服务器处理的过程。负载均衡在实际项目操作过程中，有硬件负载均衡和软件负载均衡两种。

#### 硬件负载均衡
硬件负载均衡也称为硬负载，如 F5 负载均衡，虽然成本较高，但数据的稳定性和安全性有很好的保障。

#### 软件负载均衡
Nginx 支持多种负载均衡算法，通过软件实现负载均衡，相对成本较低。

### 6. Nginx的负载均衡算法
#### 轮询（默认）
接收到的请求按照顺序逐一分配到不同的后端服务器。即使某一台后端服务器宕机，Nginx 也会自动将其剔除出队列。可以设置权重值（weight），用于调整请求的分配率。

```nginx
upstream backend {
    server backend1.example.com weight=3;
    server backend2.example.com;
    server backend3.example.com;
}
```

#### ip_hash
每个请求按照发起客户端的 IP 的 hash 结果进行匹配，保证同一个 IP 地址的客户端总是访问同一个后端服务器。

```nginx
upstream backend {
    ip_hash;
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}
```

#### fair
动态根据后端服务器的请求处理到响应的时间进行均衡分配。需要安装 upstream_fair 模块。

```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
    fair;
}
```

#### url_hash
按照访问的 URL 的 hash 结果分配请求，提高缓存效率。需要安装 Nginx 的 hash 软件包。

```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
    hash $request_uri;
}
```

### 7. 项目中的应用场景
在实际项目操作时，正向代理和反向代理可能会存在同一个应用场景中。正向代理代理客户端的请求去访问目标服务器，目标服务器是一个反向代理服务器，反向代理了多台真实的业务处理服务器。

### 8. 参考链接
+ [Tengine文档](http://tengine.taobao.org/documentation_cn.html)
