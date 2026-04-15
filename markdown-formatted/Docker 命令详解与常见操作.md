---
title: "使用官方的Node.js基础镜像"
summary: "启动和管理容器 启动一个容器 使用`docker run`命令来启动一个容器。例如，下面的命令启动一个NGINX容器，并将主机的8080端口映射到容器的80端口： `-d`：后台运行容器。 `-p`：将主机端口映射到容器端口。 列出容器 使用`docker ps`命令来列出正在运行的容器。加上`-a`参数可以列出所有容器，包括已停止的容器。"
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

### 1. 启动和管理容器
#### 启动一个容器
使用`docker run`命令来启动一个容器。例如，下面的命令启动一个NGINX容器，并将主机的8080端口映射到容器的80端口：

```bash
docker run -d -p 8080:80 nginx
```

+ `-d`：后台运行容器。
+ `-p`：将主机端口映射到容器端口。

#### 列出容器
使用`docker ps`命令来列出正在运行的容器。加上`-a`参数可以列出所有容器，包括已停止的容器。

```bash
docker ps        # 列出正在运行的容器
docker ps -a     # 列出所有容器，包括已停止的容器
```

#### 进入容器
使用`docker exec`命令来在正在运行的容器中执行命令。例如，下面的命令在指定名称的容器中打开一个交互式的bash终端：

```bash
docker exec -it container_name /bin/bash
```

+ `-it`：启用交互式终端。

#### 退出容器
要退出Docker容器，可以使用以下命令：

```bash
exit
```

#### 停止容器
使用`docker stop`命令来停止一个容器。例如，下面的命令会停止指定ID的容器：

```bash
docker stop container_id
```

#### 启动已停止的容器
使用`docker start`命令来启动一个已停止的容器。例如，下面的命令会启动指定名称的容器：

```bash
docker start container_name
```

#### 启动并绑定端口
使用`docker start`命令并加上`-p`参数可以启动一个已停止的容器并将其端口绑定到本地端口：

```bash
docker start -p 8080:80 container_name
```

### 2. 管理镜像
#### 列出镜像
使用`docker images`命令来列出所有可用的镜像：

```bash
docker images
```

#### 删除镜像
使用`docker rmi`命令来删除一个镜像。例如，下面的命令会删除指定ID的镜像：

```bash
docker rmi image_id
```

#### 拉取镜像
使用`docker pull`命令来从Docker Hub上拉取一个镜像。例如，下面的命令会拉取最新版本的NGINX镜像：

```bash
docker pull nginx
```

#### 构建镜像
使用`docker build`命令来构建一个自定义的镜像。需要创建一个Dockerfile文件来定义构建过程。例如：

创建一个Dockerfile文件：

```plain
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

然后使用以下命令构建镜像：

```bash
docker build -t myimage:latest .
```

+ `-t`：指定镜像的名称和标签。

#### 推送镜像
使用`docker push`命令将一个镜像推送到Docker Hub或其他镜像仓库。例如，下面的命令会将本地镜像推送到Docker Hub：

```bash
docker push myrepo/myimage:latest
```

### 3. 日志和信息
#### 查看容器日志
使用`docker logs`命令来查看容器的日志输出。例如，下面的命令会显示指定ID的容器日志：

```bash
docker logs container_id
```

#### 查看容器详细信息
使用`docker inspect`命令来查看容器的详细信息。例如，下面的命令会显示指定容器的详细信息：

```bash
docker inspect container_name
```

### 4. Docker Compose 命令
#### 启动和管理服务
使用`docker-compose`命令来启动和管理多容器应用。例如，使用以下命令启动服务：

```bash
docker-compose up -d
```

+ `-d`：后台运行容器。

使用以下命令停止服务：

```bash
docker-compose down
```

#### 查看服务详细信息
使用`docker-compose inspect`命令来查看服务的详细信息。例如，下面的命令会显示指定服务的详细信息：

```bash
docker-compose inspect service_name
```

### 总结
通过以上详细的命令和说明，您可以更好地使用和管理Docker容器。如果有任何具体问题或需要更多的帮助，请随时告诉我。
