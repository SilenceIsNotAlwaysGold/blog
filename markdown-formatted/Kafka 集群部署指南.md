---
title: "外部网络声明（否则无法使用之前已经定义好的网络）"
summary: "注意事项 在进行网络设置更改之前，请确保您对网络配置有一定的了解，并在修改前备份相关文件，以防止意外情况的发生。 前提条件 使用具有`root`或`sudo`权限的用户登录到CentOS系统。 确保已安装Docker和Docker Compose。 拉取Kafka镜像 拉取Kafka 3.0."
board: "tech"
category: "容器与编排"
tags:
  - "Kafka"
  - "消息队列"
  - "分布式"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

### 1. 注意事项
在进行网络设置更改之前，请确保您对网络配置有一定的了解，并在修改前备份相关文件，以防止意外情况的发生。

### 2. 前提条件
+ 使用具有`root`或`sudo`权限的用户登录到CentOS系统。
+ 确保已安装Docker和Docker Compose。

### 3. 拉取Kafka镜像
拉取Kafka 3.0.0镜像：

```bash
docker pull bitnami/kafka:3.0.0
```

### 4. 创建Docker网络
创建一个名为`zk-net`的默认桥接网络：

```bash
docker network create zk-net
```

### 5. 创建Docker Compose配置文件
在`/home/dockerfiles`目录中创建`docker-compose-kafkas.yml`文件：

```bash
sudo mkdir -p /home/dockerfiles
sudo vi /home/dockerfiles/docker-compose-kafkas.yml
```

将以下内容粘贴到`docker-compose-kafkas.yml`文件中：

```yaml
version: '3.1'

# 外部网络声明（否则无法使用之前已经定义好的网络）
networks:
   zk-net:
        external: true

services:
  kafka1:
    image: 'bitnami/kafka:3.0.0'
    container_name: kafka1
    hostname: kafka1
    networks:
      - zk-net
    ports:
      - '9093:9092'
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=192.168.111.133:2181,192.168.111.133:2182,192.168.111.133:2183/kafka
      - KAFKA_BROKER_ID=1
      - KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://192.168.111.133:9092,EXTERNAL://192.168.111.133:9093
      - KAFKA_CFG_LISTENERS=CLIENT://:9092,EXTERNAL://:9093
      - ALLOW_PLAINTEXT_LISTENER=yes

  kafka2:
    image: 'bitnami/kafka:3.0.0'
    container_name: kafka2
    hostname: kafka2
    networks:
      - zk-net
    ports:
      - '9094:9092'
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2182,zoo3:2183/kafka
      - KAFKA_BROKER_ID=2
      - KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka2:9092,EXTERNAL://kafka2:9094
      - KAFKA_CFG_LISTENERS=CLIENT://:9092,EXTERNAL://:9094
      - ALLOW_PLAINTEXT_LISTENER=yes

  kafka3:
    image: 'bitnami/kafka:3.0.0'
    container_name: kafka3
    hostname: kafka3
    networks:
      - zk-net
    ports:
      - '9095:9092'
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2182,zoo3:2183/kafka
      - KAFKA_BROKER_ID=3
      - KAFKA_INTER_BROKER_LISTENER_NAME=CLIENT
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CLIENT:PLAINTEXT,EXTERNAL:PLAINTEXT
      - KAFKA_CFG_ADVERTISED_LISTENERS=CLIENT://kafka3:9092,EXTERNAL://kafka3:9095
      - KAFKA_CFG_LISTENERS=CLIENT://:9092,EXTERNAL://:9095
      - ALLOW_PLAINTEXT_LISTENER=yes
```

### 6. 启动Kafka集群
启动Kafka集群服务：

```bash
docker-compose -f /home/dockerfiles/docker-compose-kafkas.yml up -d
```

### 7. 验证Kafka集群
#### 检查服务状态
```bash
docker ps
```

#### 验证Kafka是否连接到Zookeeper
进入Zookeeper容器：

```bash
docker exec -it zoo2 /bin/bash
cd bin
./zkCli.sh -server 127.0.0.1:2181
```

查看Kafka节点信息：

```bash
ls /kafka/brokers/ids
```

### 8. 集群验证和测试
#### 创建主题分区
```bash
docker exec -it kafka1 /bin/bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --partitions 3 --replication-factor 3 --topic first
```

#### 查看主题列表
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

#### 测试消费消息
```bash
kafka-console-consumer.sh --topic test-kafka --from-beginning --bootstrap-server localhost:9092
```

#### 测试生产消息
```bash
kafka-console-producer.sh --topic test-kafka --bootstrap-server localhost:9092
```

### 9. 参考链接
+ [如何测试是否已经连接Zookeeper](https://changlu.blog.csdn.net/article/details/126511784?spm=1001.2014)
+ [详细Kafka集群搭建视频](https://www.bilibili.com/video/BV1hP41157qE/?spm_id_from=333.999.0.0&vd_source=a2227b312f216730657841b39ca7be90)

通过以上步骤，您可以成功部署并验证Kafka集群。如果有任何具体问题或需要更详细的解释，请随时告诉我。
