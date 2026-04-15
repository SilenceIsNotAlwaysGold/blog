---
title: "Nginx 配置详解"
summary: "Nginx 安装与启动 安装Nginx 在不同的操作系统上安装Nginx的步骤略有不同。以下是常见的安装方式： 在Debian/Ubuntu上安装 在CentOS/RHEL上安装 启动Nginx 检查Nginx状态 Nginx 配置文件结构 Nginx的配置文件一般位于`/etc/nginx/nginx.conf`。"
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

### 1. Nginx 安装与启动
#### 安装Nginx
在不同的操作系统上安装Nginx的步骤略有不同。以下是常见的安装方式：

##### 在Debian/Ubuntu上安装
```bash
sudo apt update
sudo apt install nginx
```

##### 在CentOS/RHEL上安装
```bash
sudo yum install epel-release
sudo yum install nginx
```

#### 启动Nginx
```bash
sudo systemctl start nginx
sudo systemctl enable nginx  # 设置开机自启动
```

#### 检查Nginx状态
```bash
sudo systemctl status nginx
```

### 2. Nginx 配置文件结构
Nginx的配置文件一般位于`/etc/nginx/nginx.conf`。其基本结构如下：

```nginx
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

### 3. 基本配置
#### 主要指令
+ `worker_processes`：设置Nginx的工作进程数。
+ `error_log`：设置错误日志文件路径和日志级别。
+ `pid`：设置Nginx的进程ID文件路径。
+ `worker_connections`：设置每个工作进程的最大连接数。
+ `sendfile`：启用高效文件传输模式。
+ `keepalive_timeout`：保持连接的超时时间。

### 4. 虚拟主机配置
虚拟主机配置通常放在`/etc/nginx/conf.d/`目录中，每个站点一个配置文件，文件名以`.conf`结尾。例如：

```nginx
server {
    listen       80;
    server_name  example.com www.example.com;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    error_page  404              /404.html;
    location = /40x.html {
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
    }
}
```

### 5. 反向代理配置
反向代理用于将客户端的请求转发到后端服务器进行处理。

```nginx
server {
    listen       80;
    server_name  example.com;

    location / {
        proxy_pass http://backend_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

upstream backend_server {
    server 127.0.0.1:8080;
    server 127.0.0.1:8081;
}
```

### 6. 负载均衡配置
Nginx支持多种负载均衡算法，如轮询、ip_hash、least_conn等。

#### 轮询（默认）
```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

#### ip_hash
```nginx
upstream backend {
    ip_hash;
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

#### least_conn
```nginx
upstream backend {
    least_conn;
    server backend1.example.com;
    server backend2.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 7. SSL/TLS 配置
为站点启用HTTPS，配置SSL/TLS。

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  10m;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### 8. 日志管理
#### 访问日志
配置访问日志格式和存储位置。

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for"';

access_log /var/log/nginx/access.log main;
```

#### 错误日志
配置错误日志级别和存储位置。

```nginx
error_log /var/log/nginx/error.log warn;
```

### 9. 常用指令与技巧
#### 测试配置文件
在修改配置文件后，使用以下命令测试配置文件语法是否正确：

```bash
sudo nginx -t
```

#### 重新加载配置
在修改配置文件后，重新加载Nginx配置以使修改生效：

```bash
sudo systemctl reload nginx
```

#### 增加Gzip压缩
启用Gzip压缩以减少传输数据量，提高网页加载速度。

```nginx
http {
    gzip on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

#### 限制连接数和请求速率
使用limit_conn和limit_req模块限制每个IP的连接数和请求速率。

```nginx
http {
    limit_conn_zone $binary_remote_addr zone=addr:10m;
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    server {
        location / {
            limit_conn addr 5;
            limit_req zone=one burst=10 nodelay;
        }
    }
}
```
