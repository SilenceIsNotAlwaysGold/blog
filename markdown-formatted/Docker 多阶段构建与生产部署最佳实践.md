---
title: "Docker 多阶段构建与生产部署最佳实践"
category: "容器与编排"
board: "tech"
tags: ["Docker", "容器化", "部署", "DevOps"]
summary: "Docker 多阶段构建镜像优化、docker-compose 编排、健康检查、日志管理与安全加固实战"
is_published: true
created_at: "2024-10-15T10:00:00Z"
updated_at: "2024-10-15T10:00:00Z"
---

# Docker 多阶段构建与生产部署最佳实践

Docker 不是"写个 Dockerfile 就完了"。生产环境的容器化需要考虑镜像大小、构建速度、安全性、日志管理和健康检查等方方面面。本文是我在多个项目中积累的容器化最佳实践。

## 一、多阶段构建

### 1.1 Python 项目多阶段构建

```dockerfile
# ===== Stage 1: 构建阶段 =====
FROM python:3.11-slim AS builder

WORKDIR /app

# 系统依赖（编译用，最终镜像不需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件（利用 Docker 缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ===== Stage 2: 运行阶段 =====
FROM python:3.11-slim AS runtime

# 安全：创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# 只安装运行时需要的系统库
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制 Python 包
COPY --from=builder /install /usr/local

# 复制应用代码
COPY --chown=appuser:appuser . .

# 切换到非 root 用户
USER appuser

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
```

**镜像大小对比**：

| 方案 | 镜像大小 |
|------|---------|
| python:3.11（未优化） | 1.2 GB |
| python:3.11-slim（单阶段） | 450 MB |
| python:3.11-slim（多阶段） | 280 MB |
| python:3.11-alpine（多阶段） | 180 MB |

### 1.2 前端项目多阶段构建

```dockerfile
# Stage 1: 构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

# Stage 2: Nginx 运行
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 安全头
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf

HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -q --spider http://localhost/ || exit 1

EXPOSE 80
```

### 1.3 构建缓存优化

```dockerfile
# .dockerignore 文件很重要，减少构建上下文
# .dockerignore
__pycache__
*.pyc
.git
.env
node_modules
.venv
*.log
tests/
docs/
```

```bash
# 使用 BuildKit 加速构建
DOCKER_BUILDKIT=1 docker build \
    --cache-from myapp:latest \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    -t myapp:latest .
```

## 二、docker-compose 生产编排

### 2.1 完整的生产配置

```yaml
# docker-compose.prod.yml
version: "3.8"

services:
  app:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: runtime
    image: myapp-backend:${TAG:-latest}
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
        reservations:
          cpus: "0.5"
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"

  celery-worker:
    image: myapp-backend:${TAG:-latest}
    command: celery -A app.celery worker -Q default,high_priority -c 4 --loglevel=warning
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - app
      - redis
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M

  celery-beat:
    image: myapp-backend:${TAG:-latest}
    command: celery -A app.celery beat --loglevel=warning
    restart: unless-stopped
    depends_on:
      - redis
    networks:
      - backend
    deploy:
      replicas: 1  # Beat 只能有 1 个实例

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    deploy:
      resources:
        limits:
          memory: 1G

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - backend

  nginx:
    image: nginx:1.25-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - app
    networks:
      - backend
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  backend:
    driver: bridge
```

### 2.2 环境变量管理

```bash
# .env.production（不提交到 Git）
DB_PASSWORD=s3cur3_p@ssw0rd
REDIS_PASSWORD=r3d1s_p@ss
SECRET_KEY=your-256-bit-secret
TAG=v1.2.3

# 使用方式
docker compose -f docker-compose.prod.yml --env-file .env.production up -d
```

## 三、健康检查设计

### 3.1 应用层健康检查接口

```python
from fastapi import FastAPI, Response
import asyncpg

@app.get("/health")
async def health_check():
    """浅健康检查：只检查应用是否存活"""
    return {"status": "ok"}

@app.get("/health/ready")
async def readiness_check():
    """深度健康检查：检查所有依赖"""
    checks = {}
    overall_healthy = True
    
    # 检查数据库
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)[:100]}"
        overall_healthy = False
    
    # 检查 Redis
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)[:100]}"
        overall_healthy = False
    
    status_code = 200 if overall_healthy else 503
    return Response(
        content=json.dumps({"status": "healthy" if overall_healthy else "unhealthy", "checks": checks}),
        status_code=status_code,
        media_type="application/json"
    )
```

## 四、日志管理

### 4.1 结构化日志

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()  # 输出 JSON 格式
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# 使用
logger.info("request_processed", 
    method="GET", path="/api/articles", 
    duration_ms=23, status=200, user_id=42)

# 输出：{"event": "request_processed", "method": "GET", "path": "/api/articles", ...}
```

### 4.2 日志轮转与收集

```yaml
# docker-compose 中配置日志驱动
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"
        tag: "{{.Name}}"
```

```bash
# 查看容器日志
docker compose logs -f --tail=100 app

# 导出日志到文件
docker compose logs --no-color app > app.log 2>&1
```

## 五、安全加固

### 5.1 Dockerfile 安全清单

```dockerfile
# 1. 使用固定版本标签，避免 latest
FROM python:3.11.7-slim

# 2. 非 root 用户运行
RUN useradd -r -s /sbin/nologin appuser
USER appuser

# 3. 只读文件系统（需要时再挂载可写目录）
# docker run --read-only --tmpfs /tmp myapp

# 4. 不安装不需要的包
RUN apt-get install -y --no-install-recommends curl

# 5. 清理缓存
RUN rm -rf /var/lib/apt/lists/* /root/.cache

# 6. 使用 COPY 而非 ADD（ADD 会自动解压，可能引入安全问题）
COPY . .

# 7. 扫描镜像漏洞
# docker scout cves myapp:latest
# trivy image myapp:latest
```

### 5.2 运行时安全

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true  # 禁止提权
    read_only: true             # 只读文件系统
    tmpfs:
      - /tmp
    cap_drop:
      - ALL                     # 删除所有 Linux capabilities
    cap_add:
      - NET_BIND_SERVICE        # 只添加需要的
```

## 六、零停机部署

```bash
#!/bin/bash
# deploy.sh - 滚动更新脚本

set -e

TAG=$1
if [ -z "$TAG" ]; then
    echo "Usage: ./deploy.sh <tag>"
    exit 1
fi

echo "Deploying version: $TAG"

# 1. 拉取新镜像
docker compose -f docker-compose.prod.yml pull

# 2. 滚动更新（先启动新容器，健康检查通过后再停止旧容器）
docker compose -f docker-compose.prod.yml up -d --no-deps --build app

# 3. 等待健康检查通过
echo "Waiting for health check..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:8000/health > /dev/null; then
        echo "Health check passed!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Health check failed, rolling back..."
        docker compose -f docker-compose.prod.yml up -d --no-deps app
        exit 1
    fi
    sleep 2
done

# 4. 更新 worker
docker compose -f docker-compose.prod.yml up -d --no-deps celery-worker celery-beat

# 5. 清理旧镜像
docker image prune -f

echo "Deployment complete!"
```

## 总结

Docker 生产部署核心要点：

1. **多阶段构建**：分离构建依赖和运行依赖，镜像瘦身 50%+
2. **缓存优化**：先 COPY 依赖文件，后 COPY 代码；用 .dockerignore
3. **健康检查**：分浅检查（存活）和深检查（就绪），都必须配置
4. **日志管理**：输出 JSON 结构化日志，配置轮转防磁盘爆满
5. **安全加固**：非 root 用户、最小权限、固定镜像版本、定期扫描
6. **资源限制**：CPU 和内存都要设上限，防止单个容器吃满资源
