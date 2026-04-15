---
title: "国内镜像下载"
summary: "快速安装Docker-Compose 方式一：国内镜像下载（不推荐） 国内镜像下载 sudo curl -L "https://get.daocloud.io/docker/compose/releases/download/1.29."
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

快速安装Docker-Compose

## 方式一：国内镜像下载（不推荐）
# 国内镜像下载

sudo curl -L "[https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname](https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname) -s)-$(uname -m)" -o /usr/local/bin/docker-compose


# 为docker-compose设置权限

sudo chmod +x /usr/local/bin/docker-compose


# 查看docker-compose版本

docker-compose --version


卸载docker-compose：


sudo rm /usr/local/bin/docker-compose


## 方式二：手动下载（推荐）
官方网址：[https://github.com/docker/compose/releases/tag/v2.18.1](https://github.com/docker/compose/releases/tag/v2.18.1)


在release中下载对应的linux发行版：docker-compose-linux-x86_64


下载下来之后按照步骤上传：


①上传到服务器的【/usr/local/bin】目录下


②执行以下命令：


# 重命名

sudo mv docker-compose-linux-x86_64 docker-compose


# 将可执行权限应用于二进制文件

sudo chmod +x /usr/local/bin/docker-compose


# 创建软链

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


③测试版本号

docker-compose -v


出现以下信息表示成功！


![](https://cdn.nlark.com/yuque/0/2023/png/38572666/1694776492480-2b416101-4f52-4dd9-a213-3ca5a9121679.png)

[https://blog.csdn.net/cl939974883/article/details/126463806](https://blog.csdn.net/cl939974883/article/details/126463806)
