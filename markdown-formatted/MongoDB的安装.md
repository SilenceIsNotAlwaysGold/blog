---
title: "MongoDB 安装配置完全指南"
summary: "MongoDB 安装配置完全指南 目录 1. 系统要求 2. CentOS/RHEL 安装 3. Ubuntu/Debian 安装 4. macOS 安装 5. Windows 安装 6. Docker 安装 7. 配置文件详解 8. 安全配置 9. 验证和测试 10. 常见问题 系统要求 1."
board: "tech"
category: "数据库"
tags:
  - "MongoDB"
  - "NoSQL"
  - "文档数据库"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# MongoDB 安装配置完全指南

## 目录

- [1. 系统要求](#1-系统要求)
- [2. CentOS/RHEL 安装](#2-centosrhel-安装)
- [3. Ubuntu/Debian 安装](#3-ubuntudebian-安装)
- [4. macOS 安装](#4-macos-安装)
- [5. Windows 安装](#5-windows-安装)
- [6. Docker 安装](#6-docker-安装)
- [7. 配置文件详解](#7-配置文件详解)
- [8. 安全配置](#8-安全配置)
- [9. 验证和测试](#9-验证和测试)
- [10. 常见问题](#10-常见问题)

## 1. 系统要求

### 1.1 硬件要求

- **CPU**：64 位处理器
- **内存**：最低 2GB RAM，推荐 4GB 及以上
- **磁盘**：根据数据量确定，推荐使用 SSD
- **网络**：稳定的网络连接

### 1.2 软件要求

- **操作系统**：
  - Linux: CentOS 7+, Ubuntu 18.04+, Debian 9+
  - macOS: 10.13+
  - Windows: Windows Server 2016+, Windows 10+
- **文件系统**：推荐使用 XFS 或 EXT4

### 1.3 版本选择

- **社区版（Community）**：免费开源
- **企业版（Enterprise）**：商业版本，提供额外功能和支持

推荐使用最新的稳定版本（当前为 MongoDB 7.0）。

## 2. CentOS/RHEL 安装

### 2.1 使用 YUM 安装

#### 步骤 1：添加 MongoDB 官方仓库

```bash
# 创建仓库配置文件
sudo vi /etc/yum.repos.d/mongodb-org-7.0.repo

# 添加以下内容
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
```

#### 步骤 2：更新系统并安装 MongoDB

```bash
# 更新系统软件包
sudo yum update -y

# 安装 MongoDB
sudo yum install -y mongodb-org

# 安装特定版本
# sudo yum install -y mongodb-org-7.0.5
```

#### 步骤 3：启动 MongoDB 服务

```bash
# 启动 MongoDB
sudo systemctl start mongod

# 设置开机自启动
sudo systemctl enable mongod

# 查看服务状态
sudo systemctl status mongod

# 查看日志
sudo tail -f /var/log/mongodb/mongod.log
```

#### 步骤 4：验证安装

```bash
# 查看 MongoDB 版本
mongod --version

# 连接 MongoDB
mongosh

# 或使用旧版客户端
# mongo
```

### 2.2 使用 RPM 包安装

```bash
# 下载 RPM 包
wget https://repo.mongodb.org/yum/redhat/7/mongodb-org/7.0/x86_64/RPMS/mongodb-org-server-7.0.5-1.el7.x86_64.rpm
wget https://repo.mongodb.org/yum/redhat/7/mongodb-org/7.0/x86_64/RPMS/mongodb-org-mongos-7.0.5-1.el7.x86_64.rpm
wget https://repo.mongodb.org/yum/redhat/7/mongodb-org/7.0/x86_64/RPMS/mongodb-org-shell-7.0.5-1.el7.x86_64.rpm

# 安装
sudo rpm -ivh mongodb-org-*.rpm

# 启动服务
sudo systemctl start mongod
sudo systemctl enable mongod
```

## 3. Ubuntu/Debian 安装

### 3.1 使用 APT 安装

#### 步骤 1：导入公钥

```bash
# 导入 MongoDB 公钥
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
```

#### 步骤 2：添加 MongoDB 仓库

```bash
# Ubuntu 22.04 (Jammy)
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Ubuntu 20.04 (Focal)
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Debian 11 (Bullseye)
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/7.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

#### 步骤 3：安装 MongoDB

```bash
# 更新软件包列表
sudo apt-get update

# 安装 MongoDB
sudo apt-get install -y mongodb-org

# 安装特定版本
# sudo apt-get install -y mongodb-org=7.0.5 mongodb-org-database=7.0.5 mongodb-org-server=7.0.5 mongodb-org-mongos=7.0.5 mongodb-org-tools=7.0.5
```

#### 步骤 4：启动 MongoDB 服务

```bash
# 启动 MongoDB
sudo systemctl start mongod

# 设置开机自启动
sudo systemctl enable mongod

# 查看服务状态
sudo systemctl status mongod

# 查看日志
sudo tail -f /var/log/mongodb/mongod.log
```

## 4. macOS 安装

### 4.1 使用 Homebrew 安装

#### 步骤 1：安装 Homebrew（如果未安装）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 步骤 2：安装 MongoDB

```bash
# 添加 MongoDB tap
brew tap mongodb/brew

# 安装 MongoDB Community Edition
brew install mongodb-community@7.0

# 查看安装信息
brew info mongodb-community@7.0
```

#### 步骤 3：启动 MongoDB

```bash
# 启动 MongoDB（前台运行）
mongod --config /usr/local/etc/mongod.conf

# 或使用 brew services 管理（后台运行）
brew services start mongodb-community@7.0

# 查看服务状态
brew services list

# 停止服务
brew services stop mongodb-community@7.0
```

#### 步骤 4：连接 MongoDB

```bash
# 使用 mongosh 连接
mongosh
```

### 4.2 手动安装

```bash
# 下载 MongoDB
curl -O https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-7.0.5.tgz

# 解压
tar -zxvf mongodb-macos-x86_64-7.0.5.tgz

# 移动到安装目录
sudo mv mongodb-macos-x86_64-7.0.5 /usr/local/mongodb

# 创建数据目录
sudo mkdir -p /usr/local/var/mongodb
sudo mkdir -p /usr/local/var/log/mongodb

# 设置权限
sudo chown -R $(whoami) /usr/local/var/mongodb
sudo chown -R $(whoami) /usr/local/var/log/mongodb

# 添加到 PATH
echo 'export PATH="/usr/local/mongodb/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 启动 MongoDB
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork
```

## 5. Windows 安装

### 5.1 使用安装程序

#### 步骤 1：下载安装程序

访问 [MongoDB 下载中心](https://www.mongodb.com/try/download/community) 下载 Windows 安装程序（.msi 文件）。

#### 步骤 2：运行安装程序

1. 双击 `.msi` 文件启动安装向导
2. 选择 "Complete" 完整安装
3. 选择 "Install MongoDB as a Service"（作为服务安装）
4. 配置数据目录和日志目录（默认为 `C:\Program Files\MongoDB\Server\7.0\data` 和 `C:\Program Files\MongoDB\Server\7.0\log`）
5. 可选：安装 MongoDB Compass（图形化管理工具）
6. 完成安装

#### 步骤 3：验证安装

```powershell
# 打开 PowerShell 或命令提示符

# 查看 MongoDB 版本
mongod --version

# 连接 MongoDB
mongosh
```

### 5.2 手动安装

```powershell
# 下载 ZIP 包并解压到 C:\mongodb

# 创建数据目录
mkdir C:\data\db
mkdir C:\data\log

# 创建配置文件 C:\mongodb\mongod.cfg
# 内容见下文配置文件详解

# 安装为 Windows 服务
"C:\mongodb\bin\mongod.exe" --config "C:\mongodb\mongod.cfg" --install

# 启动服务
net start MongoDB

# 停止服务
net stop MongoDB

# 删除服务
"C:\mongodb\bin\mongod.exe" --remove
```

## 6. Docker 安装

### 6.1 使用 Docker 运行 MongoDB

```bash
# 拉取 MongoDB 镜像
docker pull mongo:7.0

# 运行 MongoDB 容器
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password123 \
  mongo:7.0

# 查看容器状态
docker ps

# 查看日志
docker logs mongodb

# 连接 MongoDB
docker exec -it mongodb mongosh -u admin -p password123
```

### 6.2 使用 Docker Compose

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
    networks:
      - mongodb_network

volumes:
  mongodb_data:
  mongodb_config:

networks:
  mongodb_network:
    driver: bridge
```

启动服务：

```bash
# 启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f mongodb

# 停止
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

## 7. 配置文件详解

### 7.1 配置文件位置

- **Linux**: `/etc/mongod.conf`
- **macOS**: `/usr/local/etc/mongod.conf`
- **Windows**: `C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg`

### 7.2 配置文件示例

```yaml
# mongod.conf

# 存储配置
storage:
  dbPath: /var/lib/mongodb        # 数据目录
  journal:
    enabled: true                  # 启用日志
  engine: wiredTiger               # 存储引擎
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1               # 缓存大小（GB）

# 日志配置
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log  # 日志文件路径
  logRotate: reopen                   # 日志轮转

# 网络配置
net:
  port: 27017                      # 监听端口
  bindIp: 127.0.0.1                # 绑定 IP（0.0.0.0 允许所有 IP）
  maxIncomingConnections: 65536    # 最大连接数

# 进程管理
processManagement:
  fork: true                       # 后台运行（仅 Linux/macOS）
  pidFilePath: /var/run/mongodb/mongod.pid  # PID 文件路径
  timeZoneInfo: /usr/share/zoneinfo  # 时区信息

# 安全配置
security:
  authorization: enabled           # 启用认证
  # keyFile: /path/to/keyfile      # 副本集密钥文件

# 操作分析
operationProfiling:
  mode: slowOp                     # 慢查询分析模式
  slowOpThresholdMs: 100           # 慢查询阈值（毫秒）

# 副本集配置
# replication:
#   replSetName: rs0               # 副本集名称

# 分片配置
# sharding:
#   clusterRole: shardsvr          # 分片角色
```

### 7.3 常用配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| storage.dbPath | 数据存储目录 | /var/lib/mongodb |
| systemLog.path | 日志文件路径 | /var/log/mongodb/mongod.log |
| net.port | 监听端口 | 27017 |
| net.bindIp | 绑定 IP 地址 | 127.0.0.1 |
| security.authorization | 启用认证 | disabled |
| storage.engine | 存储引擎 | wiredTiger |

## 8. 安全配置

### 8.1 启用认证

#### 步骤 1：创建管理员用户

```bash
# 连接 MongoDB（无认证）
mongosh

# 切换到 admin 数据库
use admin

# 创建管理员用户
db.createUser({
  user: "admin",
  pwd: "securePassword123",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
  ]
})

# 或创建超级管理员
db.createUser({
  user: "root",
  pwd: "rootPassword123",
  roles: [ "root" ]
})

# 退出
exit
```

#### 步骤 2：启用认证

编辑配置文件 `/etc/mongod.conf`：

```yaml
security:
  authorization: enabled
```

重启 MongoDB：

```bash
sudo systemctl restart mongod
```

#### 步骤 3：使用认证连接

```bash
# 方式 1：命令行参数
mongosh -u admin -p securePassword123 --authenticationDatabase admin

# 方式 2：连接字符串
mongosh "mongodb://admin:securePassword123@localhost:27017/?authSource=admin"

# 方式 3：连接后认证
mongosh
use admin
db.auth("admin", "securePassword123")
```

### 8.2 创建应用用户

```javascript
// 连接为管理员
use admin
db.auth("admin", "securePassword123")

// 切换到应用数据库
use myapp

// 创建只读用户
db.createUser({
  user: "reader",
  pwd: "readerPassword123",
  roles: [ { role: "read", db: "myapp" } ]
})

// 创建读写用户
db.createUser({
  user: "writer",
  pwd: "writerPassword123",
  roles: [ { role: "readWrite", db: "myapp" } ]
})

// 创建数据库管理员
db.createUser({
  user: "dbadmin",
  pwd: "dbadminPassword123",
  roles: [ { role: "dbAdmin", db: "myapp" } ]
})
```

### 8.3 常用角色说明

| 角色 | 权限 | 适用场景 |
|------|------|----------|
| read | 读取数据 | 只读应用 |
| readWrite | 读写数据 | 普通应用 |
| dbAdmin | 数据库管理 | 数据库维护 |
| userAdmin | 用户管理 | 用户管理 |
| clusterAdmin | 集群管理 | 集群维护 |
| root | 超级管理员 | 完全控制 |

### 8.4 网络安全

#### 限制访问 IP

编辑配置文件：

```yaml
net:
  bindIp: 127.0.0.1,192.168.1.100  # 只允许本地和指定 IP 访问
```

#### 使用防火墙

```bash
# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port protocol="tcp" port="27017" accept'
sudo firewall-cmd --reload

# Ubuntu/Debian (ufw)
sudo ufw allow from 192.168.1.0/24 to any port 27017
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 27017 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 27017 -j DROP
```

### 8.5 启用 TLS/SSL

#### 生成证书

```bash
# 生成自签名证书（测试用）
openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes \
  -out mongodb-cert.crt -keyout mongodb-cert.key

# 合并证书和密钥
cat mongodb-cert.key mongodb-cert.crt > mongodb.pem

# 设置权限
chmod 400 mongodb.pem
sudo chown mongodb:mongodb mongodb.pem
```

#### 配置 TLS

编辑配置文件：

```yaml
net:
  tls:
    mode: requireTLS
    certificateKeyFile: /etc/ssl/mongodb.pem
    # CAFile: /etc/ssl/ca.pem  # 如果使用 CA 签名证书
```

重启 MongoDB：

```bash
sudo systemctl restart mongod
```

#### 使用 TLS 连接

```bash
mongosh --tls --tlsCertificateKeyFile /etc/ssl/client.pem \
  --host localhost --port 27017
```

## 9. 验证和测试

### 9.1 基本连接测试

```bash
# 连接 MongoDB
mongosh

# 查看数据库列表
show dbs

# 创建测试数据库
use testdb

# 插入测试数据
db.testcollection.insertOne({ name: "test", value: 123 })

# 查询数据
db.testcollection.find()

# 删除测试数据
db.testcollection.drop()
```

### 9.2 性能测试

```bash
# 使用 mongosh 进行简单性能测试
use testdb

// 插入 10000 条数据
for (let i = 0; i < 10000; i++) {
  db.perftest.insertOne({
    index: i,
    name: "user" + i,
    email: "user" + i + "@example.com",
    created: new Date()
  })
}

// 查询性能测试
db.perftest.find({ index: { $gt: 5000 } }).explain("executionStats")

// 创建索引
db.perftest.createIndex({ index: 1 })

// 再次测试查询性能
db.perftest.find({ index: { $gt: 5000 } }).explain("executionStats")

// 清理测试数据
db.perftest.drop()
```

### 9.3 监控和诊断

```javascript
// 查看服务器状态
db.serverStatus()

// 查看数据库统计
db.stats()

// 查看集合统计
db.collection.stats()

// 查看当前操作
db.currentOp()

// 查看慢查询
db.system.profile.find().sort({ ts: -1 }).limit(10)

// 查看连接数
db.serverStatus().connections

// 查看内存使用
db.serverStatus().mem

// 查看网络统计
db.serverStatus().network
```

## 10. 常见问题

### 10.1 启动失败

**问题**：MongoDB 启动失败，提示权限错误。

**解决方案**：

```bash
# 检查数据目录权限
ls -la /var/lib/mongodb

# 修改权限
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb

# 检查 SELinux（CentOS/RHEL）
sudo setenforce 0  # 临时禁用
# 或永久禁用
sudo vi /etc/selinux/config
# 设置 SELINUX=disabled

# 重启 MongoDB
sudo systemctl restart mongod
```

### 10.2 连接被拒绝

**问题**：无法连接到 MongoDB，提示连接被拒绝。

**解决方案**：

```bash
# 1. 检查 MongoDB 是否运行
sudo systemctl status mongod

# 2. 检查端口是否监听
sudo netstat -tlnp | grep 27017
# 或
sudo ss -tlnp | grep 27017

# 3. 检查防火墙
sudo firewall-cmd --list-all  # CentOS/RHEL
sudo ufw status               # Ubuntu/Debian

# 4. 检查 bindIp 配置
grep bindIp /etc/mongod.conf
# 如果需要远程访问，设置为 0.0.0.0

# 5. 重启 MongoDB
sudo systemctl restart mongod
```

### 10.3 认证失败

**问题**：启用认证后无法连接。

**解决方案**：

```bash
# 1. 临时禁用认证
sudo vi /etc/mongod.conf
# 注释掉 security.authorization

# 2. 重启 MongoDB
sudo systemctl restart mongod

# 3. 重新创建用户
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: "newPassword123",
  roles: [ "root" ]
})

# 4. 重新启用认证
sudo vi /etc/mongod.conf
# 取消注释 security.authorization

# 5. 重启 MongoDB
sudo systemctl restart mongod

# 6. 测试连接
mongosh -u admin -p newPassword123 --authenticationDatabase admin
```

### 10.4 磁盘空间不足

**问题**：数据目录磁盘空间不足。

**解决方案**：

```bash
# 1. 检查磁盘使用情况
df -h /var/lib/mongodb

# 2. 清理旧日志
sudo rm /var/log/mongodb/mongod.log.*

# 3. 压缩数据库
mongosh
use admin
db.runCommand({ compact: 'collectionName' })

# 4. 移动数据目录到更大的磁盘
sudo systemctl stop mongod
sudo mv /var/lib/mongodb /new/path/mongodb
sudo ln -s /new/path/mongodb /var/lib/mongodb
# 或修改配置文件中的 storage.dbPath
sudo systemctl start mongod

# 5. 启用日志轮转
sudo vi /etc/logrotate.d/mongodb
# 添加日志轮转配置
```

### 10.5 性能问题

**问题**：MongoDB 查询速度慢。

**解决方案**：

```javascript
// 1. 分析慢查询
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(10)

// 2. 检查是否使用索引
db.collection.find({ field: value }).explain("executionStats")

// 3. 创建合适的索引
db.collection.createIndex({ field: 1 })

// 4. 检查工作集大小
db.serverStatus().wiredTiger.cache

// 5. 增加缓存大小（修改配置文件）
// storage.wiredTiger.engineConfig.cacheSizeGB: 2

// 6. 优化查询
// - 使用投影减少返回数据
// - 使用 limit 限制结果数量
// - 避免全表扫描
```

### 10.6 内存使用过高

**问题**：MongoDB 占用内存过高。

**解决方案**：

```yaml
# 1. 限制缓存大小（编辑配置文件）
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1  # 设置为物理内存的 50-60%

# 2. 重启 MongoDB
sudo systemctl restart mongod

# 3. 监控内存使用
mongosh
db.serverStatus().mem
db.serverStatus().wiredTiger.cache
```

## 参考资源

- [MongoDB 官方文档](https://docs.mongodb.com/)
- [MongoDB 安装指南](https://docs.mongodb.com/manual/installation/)
- [MongoDB 配置文件参考](https://docs.mongodb.com/manual/reference/configuration-options/)
- [MongoDB 安全检查清单](https://docs.mongodb.com/manual/administration/security-checklist/)
- [MongoDB 性能优化](https://docs.mongodb.com/manual/administration/analyzing-mongodb-performance/)

## 下一步

安装完成后，建议：

1. **学习基本操作**：参考 [Mongodb.md](/home/clouditera/xlj/markdown/Mongodb.md)
2. **配置主从复制**：提高可用性
3. **设置监控告警**：及时发现问题
4. **定期备份数据**：防止数据丢失
5. **性能调优**：根据实际负载优化配置
