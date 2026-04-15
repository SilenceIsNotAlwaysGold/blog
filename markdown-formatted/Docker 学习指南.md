---
title: "Docker 学习指南"
summary: "本文全面介绍 Docker 容器化平台的基础概念、安装配置、常用命令和最佳实践。涵盖 Docker Engine、镜像、容器、仓库等核心组件，详细讲解容器管理、镜像构建、网络配置、存储管理等操作，并介绍 Dockerfile 编写、Docker Compose 使用、安全实践等进阶主题，帮助开发者快速掌握 Docker 技术。"
board: "tech"
category: "容器与编排"
tags:
  - "Docker"
  - "容器化"
  - "DevOps"
  - "微服务"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Docker 学习指南

## 1. Docker基础概念

### 什么是Docker

Docker 是一个开源的容器化平台，旨在简化应用程序的部署和管理。它通过容器技术将应用程序及其依赖环境打包成一个标准化的单元，以便在任何环境中运行。

### Docker的组成部分

- **Docker Engine**：运行容器的核心引擎，包括Docker守护进程（daemon）、Docker CLI和REST API。
- **Docker镜像**：只读模板，用于创建Docker容器。
- **Docker容器**：镜像的运行实例，包含应用程序及其依赖环境。
- **Docker仓库（Registry）**：用于存储和分发Docker镜像，如Docker Hub。

### Docker的优势

- **轻量级**：容器共享主机操作系统内核，资源开销小。
- **可移植性**：一次构建，到处运行。
- **隔离性**：容器之间互相隔离，提升安全性。
- **快速启动**：容器启动速度快，适合快速迭代和部署。

## 2. Docker安装与配置

### 安装Docker

#### 在Debian/Ubuntu上安装

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

#### 在CentOS/RHEL上安装

```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
```

### 配置Docker

编辑 `/etc/docker/daemon.json` 文件，添加或修改配置。例如，配置镜像加速：

```json
{
  "registry-mirrors": ["https://your-mirror-url"]
}
```

重启Docker服务使配置生效：

```bash
sudo systemctl restart docker
```

## 3. Docker常用命令

### 容器管理命令

```bash
docker run -it ubuntu /bin/bash  # 运行一个Ubuntu容器并进入交互模式
docker ps  # 列出正在运行的容器
docker ps -a  # 列出所有容器
docker stop container_id  # 停止一个容器
docker rm container_id  # 删除一个容器
docker logs container_id  # 查看容器日志
docker exec -it container_id /bin/bash  # 进入一个正在运行的容器
```

### 镜像管理命令

```bash
docker pull ubuntu  # 拉取Ubuntu镜像
docker images  # 列出本地镜像
docker rmi image_id  # 删除一个镜像
docker build -t myimage:latest .  # 基于Dockerfile构建镜像
docker tag myimage:latest myrepo/myimage:latest  # 标记镜像
docker push myrepo/myimage:latest  # 推送镜像到仓库
```

### 网络管理命令

```bash
docker network ls  # 列出所有网络
docker network create mynet  # 创建一个自定义网络
docker network inspect mynet  # 查看网络详情
docker network connect mynet container_id  # 将容器连接到网络
docker network disconnect mynet container_id  # 将容器从网络断开
```

### 存储管理命令

```bash
docker volume ls  # 列出所有卷
docker volume create myvolume  # 创建一个卷
docker volume inspect myvolume  # 查看卷详情
docker volume rm myvolume  # 删除一个卷
```

## 4. Dockerfile

### Dockerfile基础

Dockerfile 是一个包含一系列指令的文本文件，用于定义镜像的构建过程。

### Dockerfile指令

- `FROM`：指定基础镜像
- `MAINTAINER`：镜像维护者信息
- `RUN`：运行命令
- `COPY`：复制文件到镜像
- `ADD`：复制文件或URL内容到镜像，并自动处理压缩文件
- `WORKDIR`：设置工作目录
- `CMD`：指定容器启动时运行的命令
- `ENTRYPOINT`：配置容器启动程序和参数
- `EXPOSE`：声明容器监听的端口
- `ENV`：设置环境变量
- `VOLUME`：创建挂载点

### Dockerfile示例

```dockerfile
# 使用官方的Node.js基础镜像
FROM node:14

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器
COPY . .

# 安装依赖
RUN npm install

# 暴露应用端口
EXPOSE 3000

# 启动应用
CMD ["node", "app.js"]
```

## 5. Docker Compose

### 什么是Docker Compose

Docker Compose 是一个用于定义和运行多容器Docker应用程序的工具。通过一个Compose文件，您可以使用单个命令启动和管理应用程序的多个服务。

### Docker Compose的安装

#### 在Debian/Ubuntu上安装

```bash
sudo apt install docker-compose
```

#### 在CentOS/RHEL上安装

```bash
sudo yum install docker-compose
```

### Docker Compose基本用法

创建 `docker-compose.yml` 文件：

```yaml
version: '3'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
  redis:
    image: redis:alpine
```

使用以下命令启动服务：

```bash
docker-compose up -d
```

使用以下命令停止服务：

```bash
docker-compose down
```

## 6. Docker网络与存储管理

### Docker网络

Docker 提供了几种网络模式：

- **bridge**：默认网络，适用于单机上的容器间通信。
- **host**：容器共享主机网络栈。
- **none**：容器没有网络连接。
- **overlay**：跨多个Docker主机的网络。
- **macvlan**：为容器分配MAC地址，允许它们像物理设备一样直接访问网络。

创建自定义桥接网络：

```bash
docker network create mynet
```

将容器连接到自定义网络：

```bash
docker run -d --network=mynet --name mycontainer nginx
```

### Docker存储

Docker 提供了两种存储方式：

- **卷（Volume）**：由Docker管理，适用于持久化数据。
- **绑定挂载（Bind Mount）**：将主机目录挂载到容器，适用于开发环境。

创建卷并挂载到容器：

```bash
docker volume create myvolume
docker run -d -v myvolume:/data --name mycontainer nginx
```

绑定主机目录到容器：

```bash
docker run -d -v /path/on/host:/path/in/container --name mycontainer nginx
```

## 7. Docker安全实践

- **最小权限原则**：仅授予容器运行所需的最小权限。
- **使用非root用户**：尽量避免在容器中使用root用户。
- **限制资源**：使用 `--memory` 和 `--cpus` 选项限制容器资源。
- **定期更新镜像**：保持镜像和基础镜像的最新版本。
- **启用内容信任**：使用Docker内容信任（DCT）确保镜像来源可信。
- **扫描镜像漏洞**：使用工具如Clair、Trivy扫描镜像漏洞。

## 8. 常见问题

### 容器无法启动

检查容器日志：

```bash
docker logs container_id
```

### 镜像拉取失败

检查网络连接和Docker配置，确保镜像仓库地址正确。

### 容器无法访问网络

检查容器网络配置，确保容器连接到正确的网络。

## 9. 参考链接

- [Docker官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker GitHub](https://github.com/docker/docker)
