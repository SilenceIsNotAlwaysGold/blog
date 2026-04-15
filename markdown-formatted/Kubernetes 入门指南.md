---
title: "Kubernetes 入门指南"
summary: "Kubernetes (K8s) 核心概念入门，解析 Pod、Deployment、Service 的作用，演示如何编写 YAML 清单文件部署应用，并进行扩缩容和滚动更新。"
board: "tech"
category: "容器与编排"
tags:
  - "Kubernetes"
  - "K8s"
  - "容器编排"
  - "DevOps"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Kubernetes 入门指南

Docker 解决了容器的打包和运行问题，而 Kubernetes (K8s) 解决了大规模容器的**编排**与**管理**问题。它是目前云原生领域的实际标准。

## 1. 核心概念

K8s 的世界里有一堆概念，初学者只需要掌握最核心的几个：

### Node (节点)
集群中的一台机器（物理机或虚拟机）。
- **Master Node**: 控制平面，负责调度和管理。
- **Worker Node**: 工作节点，运行实际的应用容器。

### Pod (豆荚)
K8s 调度的最小单位。一个 Pod 包含一个或多个紧密协作的容器（共享网络 IP 和存储）。通常一个 Pod 只运行一个主容器。

### Deployment (部署)
用于管理无状态应用。它负责创建和更新 Pod，确保指定数量的副本（Replicas）在运行。如果 Pod 挂了，Deployment 会自动创建一个新的。

### Service (服务)
Pod 的 IP 是会变的（重启后变化），Service 定义了一组 Pod 的逻辑集合和访问策略，提供一个固定的 VIP (ClusterIP) 供集群内访问，或者通过 NodePort/LoadBalancer 暴露给外部。

## 2. 搭建本地环境

推荐使用 **Minikube** 或 **Docker Desktop (Enable Kubernetes)** 在本地快速体验。

```bash
# 检查版本
kubectl version

# 查看节点状态
kubectl get nodes
```

## 3. 实战：部署 Nginx

### 方式一：命令式 (Imperative)
适合快速测试。

```bash
# 创建 Deployment
kubectl create deployment nginx-demo --image=nginx:latest

# 暴露端口
kubectl expose deployment nginx-demo --port=80 --type=NodePort

# 查看状态
kubectl get pods
kubectl get svc
```

### 方式二：声明式 (Declarative) - **推荐**
使用 YAML 文件描述期望状态。

创建 `nginx-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3 # 期望 3 个副本
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx # 关联上面的 Label
  ports:
    - protocol: TCP
      port: 80 # Service 端口
      targetPort: 80 # 容器端口
      nodePort: 30080 # 节点暴露端口
  type: NodePort
```

应用配置：
```bash
kubectl apply -f nginx-deployment.yaml
```

## 4. 常用操作

### 查看资源
```bash
# 查看所有 Pod
kubectl get pods

# 查看详细信息（排错必备）
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>
```

### 扩缩容 (Scaling)
```bash
# 将副本数调整为 5
kubectl scale deployment nginx-deployment --replicas=5
```

### 滚动更新 (Rolling Update)
修改 YAML 中的 image 版本，然后再次 apply。

```bash
# 或者使用命令更新镜像
kubectl set image deployment/nginx-deployment nginx=nginx:1.22

# 查看更新进度
kubectl rollout status deployment/nginx-deployment

# 回滚到上一个版本
kubectl rollout undo deployment/nginx-deployment
```

### 进入容器
```bash
kubectl exec -it <pod-name> -- /bin/bash
```

## 5. 配置管理 (ConfigMap & Secret)

不要把配置写死在镜像里。

- **ConfigMap**: 存储普通配置文件。
- **Secret**: 存储敏感信息（密码、证书），base64 编码。

```yaml
env:
  - name: DB_HOST
    valueFrom:
      configMapKeyRef:
        name: my-config
        key: db-host
```

## 6. 总结

Kubernetes 的学习曲线较陡峭，但它带来的自动化运维能力是巨大的：
1. **自动修复** (Self-healing)：容器挂了自动重启。
2. **弹性伸缩** (Auto-scaling)：根据 CPU 负载自动加减机器。
3. **零停机部署**：滚动更新和回滚。

掌握了 Pod, Deployment, Service 这"三驾马车"，你就已经跨入了 K8s 的大门。
