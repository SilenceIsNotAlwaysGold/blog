---
title: "Nginx 负载均衡与高可用"
summary: "解析 Nginx 的负载均衡策略（轮询、权重、IP Hash）及配置方法，结合 Keepalived 实现高可用集群，构建稳定可靠的 Web 架构。"
board: "tech"
category: "Web服务器"
tags:
  - "Nginx"
  - "负载均衡"
  - "高可用"
  - "集群"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Nginx 负载均衡与高可用

随着业务量的增长，单台服务器往往难以支撑。Nginx 提供了强大的反向代理和负载均衡功能，可以轻松实现流量分发。本文将介绍 Nginx 的常用负载均衡策略，并结合 Keepalived 讲解如何构建高可用架构。

## 1. Nginx 负载均衡基础

Nginx 使用 `upstream` 模块定义后端服务器组，并在 `server` 块中通过 `proxy_pass` 进行引用。

### 基本配置

```nginx
http {
    upstream backend_servers {
        server 192.168.1.101:8080;
        server 192.168.1.102:8080;
        server 192.168.1.103:8080;
    }

    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 2. 负载均衡策略

Nginx 支持多种调度算法，以适应不同的业务场景。

### 1. 轮询（Round Robin）- 默认

每个请求按时间顺序逐一分配到不同的后端服务器。如果服务器宕机，能自动剔除。

### 2. 权重（Weight）

指定轮询几率，`weight` 和访问比率成正比，用于后端服务器性能不均的情况。

```nginx
upstream backend_servers {
    server 192.168.1.101:8080 weight=3; # 接收更多请求
    server 192.168.1.102:8080 weight=1;
    server 192.168.1.103:8080 weight=1;
}
```

### 3. IP Hash

每个请求按访问 IP 的 hash 结果分配，这样每个访客固定访问一个后端服务器，**可解决 Session 共享问题**。

```nginx
upstream backend_servers {
    ip_hash;
    server 192.168.1.101:8080;
    server 192.168.1.102:8080;
}
```

### 4. Least Connections（最少连接）

将请求分配给当前连接数最少的服务器，适用于请求处理时间长短不一的场景。

```nginx
upstream backend_servers {
    least_conn;
    server 192.168.1.101:8080;
    server 192.168.1.102:8080;
}
```

## 3. 后端状态与健康检查

Nginx 可以设置后端服务器的状态，如 `down`（暂停服务）和 `backup`（备用）。

```nginx
upstream backend_servers {
    server 192.168.1.101:8080;
    server 192.168.1.102:8080 down;   # 不参与负载均衡
    server 192.168.1.103:8080 backup; # 其他非 backup 机器忙或宕机时启用

    # max_fails: 允许失败次数，fail_timeout: 失败后暂停服务时间
    server 192.168.1.104:8080 max_fails=3 fail_timeout=30s;
}
```

> 注意：Nginx 开源版只有被动健康检查。主动健康检查（Health Check）通常需要 Nginx Plus 或第三方模块。

## 4. Keepalived 实现高可用（HA）

仅有负载均衡是不够的，如果 Nginx 负载均衡器本身宕机，整个服务将不可用。Keepalived 利用 VRRP 协议实现主备切换，解决单点故障。

### 架构图

```bash
        VIP (192.168.1.100)
             |
    +--------+--------+
    |                 |
Master Nginx      Backup Nginx
(192.168.1.10)    (192.168.1.11)
    |                 |
    +--------+--------+
             |
       后端应用服务器
```

### 安装 Keepalived

```bash
# CentOS
yum install keepalived -y
# Ubuntu
apt-get install keepalived
```

### Master 配置 (/etc/keepalived/keepalived.conf)

```conf
global_defs {
    router_id LVS_DEVEL
}

# 脚本：检测 Nginx 是否存活
vrrp_script chk_nginx {
    script "/etc/keepalived/check_nginx.sh"
    interval 2
    weight -20
}

vrrp_instance VI_1 {
    state MASTER          # 主节点
    interface eth0        # 网卡接口
    virtual_router_id 51  # VRID，主备一致
    priority 100          # 优先级，主节点高于备节点
    advert_int 1

    authentication {
        auth_type PASS
        auth_pass 1111
    }

    virtual_ipaddress {
        192.168.1.100     # 虚拟 IP (VIP)
    }

    track_script {
        chk_nginx
    }
}
```

### Backup 配置

```conf
vrrp_instance VI_1 {
    state BACKUP          # 备节点
    interface eth0
    virtual_router_id 51
    priority 90           # 优先级较低
    # ... 其他同上
}
```

### 检查脚本 (check_nginx.sh)

```bash
#!/bin/bash
if ! pidof nginx > /dev/null; then
    # 尝试重启
    systemctl start nginx
    sleep 2
    # 再次检查，如果失败则停止 keepalived，触发 VIP 漂移
    if ! pidof nginx > /dev/null; then
        systemctl stop keepalived
    fi
fi
```

记得给脚本执行权限：`chmod +x /etc/keepalived/check_nginx.sh`。

## 总结

- **负载均衡**：通过 `upstream` 模块实现多台后端服务器的流量分发，支持轮询、权重、IP Hash 等策略。
- **高可用**：结合 Keepalived，通过 VIP（虚拟 IP）漂移机制，确保 Nginx 负载均衡器本身的高可用性。

这套架构是目前中小规模互联网企业最常用的 Web 接入层方案。
