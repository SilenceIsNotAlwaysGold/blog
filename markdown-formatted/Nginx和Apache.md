---
title: "Nginx和Apache的安装及启动服务"
summary: "Nginx和Apache的安装及启动服务 在云服务器上安装Web服务器软件，例如Apache或Nginx。如果你已经安装了Web服务器软件，则可以跳过此步骤。 在CentOS上安装Apache： 在CentOS上安装Nginx： 将HTML文件放置在Web服务器的根目录中。默认情况下，Apache的根目录为/var/www/html，"
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

# Nginx和Apache的安装及启动服务
1. 在云服务器上安装Web服务器软件，例如Apache或Nginx。如果你已经安装了Web服务器软件，则可以跳过此步骤。
    - 在CentOS上安装Apache：
    - 在CentOS上安装Nginx：

```plain
sudo yum install httpd
```

```plain
sudo yum install nginx
```

2. 将HTML文件放置在Web服务器的根目录中。默认情况下，Apache的根目录为/var/www/html，而Nginx的根目录为/usr/share/nginx/html。可以将HTML文件复制到这些目录下，或者创建一个新的目录并将HTML文件放置在其中。
3. 启动Web服务器并设置开机自启：
    - 在CentOS上启动Apache：
    - 在CentOS上启动Nginx：

```bash
sudo systemctl start httpd
sudo systemctl enable httpd
```

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

4. 确保Nginx已经成功安装并正在运行。你可以使用以下命令来检查Nginx的状态：

```lua
sudo systemctl status nginx
```

如果Nginx正在运行，你将看到类似于"active (running)"的状态。

[nginx部署.pdf](https://www.yuque.com/attachments/yuque/0/2026/pdf/38572666/1769411566674-b19d65e1-5d8b-45af-a30d-3b7bf0857722.pdf)


#
