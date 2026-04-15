---
title: "centos卡夫卡安装"
summary: "centos卡夫卡安装 要在CentOS 7上安装Kafka，可以按照以下步骤进行操作： 首先，确保您的CentOS 7系统已连接到互联网。 使用以下命令安装Java Development Kit（JDK）： 检查Java是否成功安装： 在Kafka官方网站上下载Kafka二进制文件。您可以访问以下链接：https://kafka.apache."
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

# centos卡夫卡安装
要在CentOS 7上安装Kafka，可以按照以下步骤进行操作：


1.  首先，确保您的CentOS 7系统已连接到互联网。 
2.  使用以下命令安装Java Development Kit（JDK）： 


```plain
sudo yum install java-1.8.0-openjdk-devel
```


3. 检查Java是否成功安装：


```plain
java -version
```


4.  在Kafka官方网站上下载Kafka二进制文件。您可以访问以下链接：[https://kafka.apache.org/downloads](https://kafka.apache.org/downloads) 
5.  在您下载的Kafka二进制文件中，解压安装包： 


```plain
tar -xzf kafka_2.13-2.8.0.tgz
```


（请将"kafka_2.13-2.8.0.tgz"替换为您下载的Kafka版本）


6. 进入Kafka目录：


```plain
cd kafka_2.13-2.8.0
```


7. 启动ZooKeeper服务器（Kafka依赖于ZooKeeper）：


```plain
bin/zookeeper-server-start.sh config/zookeeper.properties
```


8. 在新的终端窗口中，启动Kafka服务器：


```plain
binfka-server-start.sh configrver.properties
```


现在，您的CentOS 7系统上已成功安装并启动了Kafka。您可以继续配置和使用Kafka进行相应的操作。


# centos下docker中kafka的下载与启动
## 通过终端验证：
在Linux下使用Docker来验证Kafka的安装，可以按照以下步骤进行：


1.  安装Docker：首先，确保你的Linux系统已经安装了Docker。你可以根据你的Linux发行版选择适当的安装方法，并按照官方文档进行安装。 
2. **zookeeper 安装**

在docker中拉取zookeeper 镜像

```plain
docker pull wurstmeister/zookeeper 
```

 运行zookeeper 服务

```plain
docker run -d --restart=always --log-driver json-file --log-opt max-size=100m --log-opt max-file=2  --name zookeeper -p 2181:2181 -v /etc/localtime:/etc/localtime wurstmeister/zookeeper

```

3.  创建Kafka容器：运行以下命令来创建一个Kafka容器： 

```plain
docker run -d --name kafka -p 9092:9092 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 confluentinc/cp-kafka
```

  
查看docker 下是否正常运行zookeeper 服务

```plain
docker ps
```


    - 拉取kafka镜像

```plain
docker pull wurstmeister/kafka
```

运行kafka

```plain
docker run -d  --log-driver json-file --log-opt max-size=100m --log-opt max-file=2 --name kafka -p 9092:9092 -e KAFKA_BROKER_ID=0 -e KAFKA_ZOOKEEPER_CONNECT=192.168.11.129:2181/kafka -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://192.168.11.129:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 -v /etc/localtime:/etc/localtime wurstmeister/kafka
```

查看kafka是否运行正常

```plain
docker ps
```

进入kafka容器

```plain
docker exec -it kafka /bin/bash
```

进入kafka的bin目录下：cd  /opt/kafka_2.13-2.8.1/bin


创建一个新主题（test-kafka)来存储事件

./kafka-topics.sh --create --topic test-kafka --bootstrap-server localhost:9092


显示新主题：test-kafka 的分区信息

./kafka-topics.sh --describe --topic test-kafka --bootstrap-server localhost:9092


测试消费消息：

./kafka-console-consumer.sh --topic test-kafka --from-beginning --bootstrap-server localhost:9092

测试生产消息：

./kafka-console-producer.sh --topic test-kafka --bootstrap-server localhost:9092

## 代码验证：
可以使用Python的kafka-python库进行测试。下面是一个简单的Python代码示例，用于验证Kafka的安装和连接：

首先，确保已经安装了kafka-python库。可以使用以下命令进行安装：

```plain
pip install kafka-python
```

然后，使用以下Python代码进行验证：

```plain
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# Kafka 服务器的地址和端口
bootstrap_servers = 'localhost:9092'

# 创建一个生产者实例
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# 发送一条测试消息到名为 "test_topic" 的主题
topic = 'test_topic'
message = b'This is a test message'
try:
    producer.send(topic, value=message)
    print("消息发送成功")
except KafkaError as e:
    print("消息发送失败:", e)

# 创建一个消费者实例
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# 从主题中接收消息
try:
    for message in consumer:
        print("接收到消息:", message.value)
except KeyboardInterrupt:
    pass
finally:
    # 关闭消费者连接
    consumer.close()
```

在上面的代码中，我们创建了一个Kafka生产者实例，并使用producer.send()方法发送一条测试消息到名为"test_topic"的主题。然后，我们创建了一个Kafka消费者实例，并使用consumer迭代器从主题中接收消息。你可以将代码中的主题名称和Kafka服务器地址和端口根据实际情况进行修改。
