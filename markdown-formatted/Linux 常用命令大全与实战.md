---
title: "Linux 常用命令大全与实战"
summary: "整理 Linux 系统中最常用的命令，涵盖文件管理、系统监控、权限控制和网络操作，配合实际应用场景，助你快速掌握 Linux 运维技能。"
board: "tech"
category: "Linux系统"
tags:
  - "Linux"
  - "Shell"
  - "运维"
  - "命令"
cover_image: ""
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# Linux 常用命令大全与实战

Linux 命令行是每一位开发者和运维人员必须掌握的工具。本文不仅列举常用命令，更侧重于通过实际场景演示如何组合使用这些命令来解决问题。

## 1. 文件与目录操作

### 基础导航
- `ls -alh`: 显示当前目录下所有文件的详细信息（包括隐藏文件）。
- `cd -`: 切换回上一次所在的目录（非常实用）。
- `pwd`: 显示当前路径。

### 文件查找：find
`find` 是最强大的搜索工具。

```bash
# 在当前目录查找大于 100MB 的文件
find . -type f -size +100M

# 查找并删除 7 天前的 log 文件
find /var/log -name "*.log" -mtime +7 -exec rm -f {} \;

# 查找名为 config.yaml 的文件
find / -name "config.yaml" 2>/dev/null
```

### 内容搜索：grep
`grep` 用于在文件中搜索文本。

```bash
# 递归搜索当前目录下包含 "error" 的文件，显示行号
grep -rn "error" .

# 排除指定目录搜索
grep -rn "TODO" . --exclude-dir=node_modules

# 统计匹配行数
grep -c "404" access.log
```

## 2. 系统状态监控

### 进程与资源：top / htop
- `top`: 实时显示系统进程。按 `P` 按 CPU 排序，按 `M` 按内存排序。
- `htop`: `top` 的增强版，界面更友好（需安装）。

### 内存查看：free
```bash
# 以人类可读格式显示（MB/GB）
free -h
```

### 磁盘空间：df / du
```bash
# 查看磁盘分区使用情况
df -h

# 查看当前目录下各文件夹大小，并排序（找出磁盘杀手）
du -sh * | sort -rh
```

## 3. 文本处理三剑客 (grep, sed, awk)

这是 Linux 文本处理的神器组合。

### awk：列处理
```bash
# 打印 /etc/passwd 的第一列（用户名），以 : 分隔
awk -F: '{print $1}' /etc/passwd

# 统计 Nginx 日志中访问量最高的 10 个 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
```

### sed：流编辑
```bash
# 替换文件中的字符串（支持正则），-i 直接修改文件
sed -i 's/OldString/NewString/g' file.txt

# 打印第 5 到 10 行
sed -n '5,10p' file.txt
```

## 4. 网络操作

### 端口占用：netstat / ss
```bash
# 查看所有监听的 TCP/UDP 端口及对应进程
netstat -tulpn
# 或者
ss -tulpn

# 检查 80 端口是否被占用
lsof -i :80
```

### 网络连通性：curl / ping
```bash
# 测试网站连通性并查看 Header
curl -I https://www.google.com

# 下载文件
curl -O https://example.com/file.tar.gz

# 发送 POST 请求
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" http://api.example.com
```

## 5. 压缩与解压

### tar
Linux 下最通用的打包工具。

```bash
# 解压
tar -zxvf archive.tar.gz

# 打包并压缩
tar -czvf archive.tar.gz /path/to/directory
```

- `z`: gzip 压缩
- `c`: 创建 (create)
- `x`: 解压 (extract)
- `v`: 显示过程 (verbose)
- `f`: 指定文件名 (file)

## 6. 权限管理

```bash
# 修改文件所有者
chown user:group file.txt
chown -R user:group directory/

# 修改权限 (chmod)
# 755: 所有者可读写执行，其他人可读执行
chmod 755 script.sh
# 给文件添加执行权限
chmod +x script.sh
```

## 7. 实战场景组合

### 场景一：日志分析
查看最近的错误日志：
```bash
# 实时滚动查看最后 100 行
tail -f -n 100 /var/log/nginx/error.log
```

### 场景二：批量杀进程
杀掉所有名为 `python` 的进程：
```bash
# 方法 1
pkill python

# 方法 2
ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill -9
```

### 场景三：查看谁占用了 CPU
```bash
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head
```

## 总结

熟练掌握这些 Linux 命令，能让你在服务器管理和故障排查时游刃有余。建议多在终端中练习，结合 `man` 命令查看手册（如 `man grep`）探索更多参数用法。
