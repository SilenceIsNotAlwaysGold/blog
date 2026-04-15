---
title: "Docker Compose 实战教程"
summary: "学习如何使用 Docker Compose 定义和运行多容器应用。从 docker-compose.yml 语法详解到微服务编排实战，涵盖网络配置、数据卷挂载和环境变量管理。"
board: "tech"
category: "容器与编排"
tags:
  - "Docker"
  - "DockerCompose"
  - "容器"
  - "DevOps"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Docker Compose 实战教程

Docker 让我们能够轻松打包单个容器，但现实中的应用往往由多个服务组成（Web、DB、Redis 等）。Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。通过一个 YAML 文件，你就可以配置所有的服务。

## 1. 什么是 Docker Compose

Docker Compose 允许你使用 YAML 文件来定义应用的服务、网络和卷，然后通过一条命令创建并启动所有服务。

**核心概念：**
- **Service (服务)**: 一个应用的容器，可以运行多个实例。
- **Project (项目)**: 由一组关联的应用容器组成的一个完整业务单元，默认名为目录名。

## 2. 安装

如果安装了 Docker Desktop (Mac/Windows)，Compose 已经包含在内。
Linux 上通常需要单独安装或通过包管理器安装。

```bash
docker compose version
# 或者旧版命令
docker-compose version
```

## 3. 编写 docker-compose.yml

让我们搭建一个经典的 Python Web 应用：Flask + Redis。

### 目录结构
```python
.
├── app.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### 1. 应用代码 (app.py)
```python
from flask import Flask
from redis import Redis

app = Flask(__name__)
# 注意这里 host 写的是 'redis'，即 Compose 中定义的服务名
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    count = redis.incr('hits')
    return f'Hello World! I have been seen {count} times.\n'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### 2. Dockerfile
```dockerfile
FROM python:3.9-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 3. docker-compose.yml
```yaml
version: "3.8"  # 版本号

services:
  web:
    build: .  # 使用当前目录构建镜像
    ports:
      - "5000:5000"  # 宿主机端口:容器端口
    volumes:
      - .:/code  # 挂载当前目录，实现代码热重载
    environment:
      FLASK_ENV: development
    depends_on:
      - redis

  redis:
    image: "redis:alpine"  # 使用官方镜像
    restart: always
    volumes:
      - redis-data:/data # 数据持久化

volumes:
  redis-data: # 声明卷
```

## 4. 常用命令

### 启动服务
```bash
# 前台启动（可以看到日志）
docker compose up

# 后台启动
docker compose up -d

# 强制重新构建镜像
docker compose up -d --build
```

### 查看状态
```bash
docker compose ps
docker compose logs -f
```

### 停止与清理
```bash
# 停止容器
docker compose stop

# 停止并删除容器、网络
docker compose down

# 停止并删除容器、网络、以及挂载的数据卷（慎用！）
docker compose down -v
```

### 在运行的容器中执行命令
```bash
docker compose exec web sh
```

## 5. 网络与环境变量

### 网络 (Networking)
Compose 默认为项目创建一个网络，服务之间可以通过**服务名**相互访问（DNS 解析）。如上例中，Web 服务直接访问 `redis` 主机名。

### 环境变量
可以在 `.env` 文件中定义变量，在 YAML 中引用。

`.env` 文件：
```bash
TAG=v1.0
DB_PASSWORD=secret
```

`docker-compose.yml`：
```yaml
services:
  web:
    image: myapp:${TAG}
    environment:
      - DB_PASS=${DB_PASSWORD}
```

## 6. 生产环境建议

虽然 Compose 常用于开发环境，但也可以用于单机生产环境部署。

- 使用 `restart: always` 确保开机自启和崩溃重启。
- 使用 `volumes` 确保数据库数据持久化到宿主机。
- 不同环境使用不同的 override 文件（如 `docker-compose.prod.yml`）。

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 总结

Docker Compose 极大地简化了多容器应用的管理。它是开发环境搭建的神器，能让新入职的同事通过一句 `docker compose up` 瞬间在本地拉起包含数据库、缓存、消息队列的完整开发环境。
