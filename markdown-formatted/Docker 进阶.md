---
title: "第一个阶段：构建阶段"
summary: "多阶段构建（Multi-stage Builds） 多阶段构建允许在Dockerfile中使用多个`FROM`指令，每个指令可以使用不同的基础镜像。这种方法可以减少最终镜像的大小，提高构建效率。 Docker 网络模式 Docker 提供了多种网络模式，适用于不同的应用场景。 **Bridge（默认）**：适用于单机上的容器间通信。"
board: "tech"
category: "容器与编排"
tags:
  - "Docker"
  - "容器化"
  - "DevOps"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

#### 多阶段构建（Multi-stage Builds）
多阶段构建允许在Dockerfile中使用多个`FROM`指令，每个指令可以使用不同的基础镜像。这种方法可以减少最终镜像的大小，提高构建效率。

```plain
# 第一个阶段：构建阶段
FROM golang:1.16 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# 第二个阶段：运行阶段
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]
```

#### Docker 网络模式
Docker 提供了多种网络模式，适用于不同的应用场景。

+ **Bridge（默认）**：适用于单机上的容器间通信。
+ **Host**：容器共享主机的网络栈，性能较高，但隔离性较差。
+ **None**：容器没有网络连接，用于完全隔离。
+ **Overlay**：跨多个Docker主机的网络，用于Docker Swarm或Kubernetes集群。
+ **Macvlan**：为容器分配MAC地址，使其像物理设备一样直接访问网络。

```bash
docker network create -d bridge my_bridge_network
docker network create -d overlay my_overlay_network
docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=eth0 my_macvlan_network
```

#### Docker Swarm
Docker Swarm 是Docker原生的集群管理和编排工具。它将多个Docker主机集合成一个虚拟的Docker主机，并提供服务部署和管理功能。

```bash
# 初始化Swarm集群
docker swarm init --advertise-addr 

# 添加工作节点
docker swarm join --token  :2377

# 部署服务
docker service create --name my_service --replicas 3 -p 80:80 nginx

# 查看服务状态
docker service ls
docker service ps my_service

# 更新服务
docker service update --image nginx:latest my_service

# 删除服务
docker service rm my_service
```

#### Kubernetes
Kubernetes 是一个开源的容器编排平台，用于自动化部署、扩展和管理容器化应用程序。相比Docker Swarm，Kubernetes功能更强大，适合复杂的应用场景。

##### 安装Minikube（用于本地开发和测试）
```bash
# 安装Minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube
sudo mv minikube /usr/local/bin/

# 启动Minikube集群
minikube start

# 安装kubectl
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# 部署应用
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=NodePort

# 查看服务
kubectl get services
```

#### 镜像优化
优化Docker镜像可以减少镜像大小，提高部署效率。

+ **使用官方基础镜像**：如`alpine`，它们通常更小更安全。
+ **最小化层数**：合并多条`RUN`指令。
+ **清理缓存和临时文件**：在同一层中删除它们。

```plain
FROM alpine:latest
RUN apk add --no-cache ca-certificates \
    && rm -rf /var/cache/apk/*
```

#### 安全扫描
定期对Docker镜像进行安全扫描，检测并修复潜在的安全漏洞。

+ **使用Docker Hub的自动扫描功能**。
+ **使用开源工具**如Trivy、Clair。

```bash
# 安装Trivy
brew install aquasecurity/trivy/trivy

# 扫描镜像
trivy image nginx:latest
```

#### 持续集成和持续部署（CI/CD）
将Docker与CI/CD工具（如Jenkins、GitLab CI、GitHub Actions）结合，自动化构建、测试和部署流程。

##### 示例：GitHub Actions
```yaml
name: CI/CD Pipeline

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Build Docker image
      run: docker build -t myimage:latest .

    - name: Push Docker image
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag myimage:latest myrepo/myimage:latest
        docker push myrepo/myimage:latest
```

通过学习这些进阶知识，您将能够更深入地理解和使用Docker，提升容器化应用的管理和部署效率。如果有任何具体问题或需要更多的帮助，请随时告诉我。
