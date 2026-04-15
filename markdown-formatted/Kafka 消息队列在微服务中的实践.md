---
title: "Kafka 消息队列在微服务中的实践"
category: "其他"
board: "tech"
tags: ["Kafka", "消息队列", "微服务", "Python"]
summary: "Kafka 在微服务架构中的实战应用，涵盖生产者/消费者模式、分区策略、消息可靠性与 Python confluent-kafka"
is_published: true
created_at: "2025-01-20T10:00:00Z"
updated_at: "2025-01-20T10:00:00Z"
---

# Kafka 消息队列在微服务中的实践

在微服务架构中，服务间的异步通信是核心挑战之一。Kafka 作为高吞吐量的分布式消息系统，在日志收集、事件驱动和数据管道场景下表现优异。本文分享我在实际项目中使用 Kafka 的经验。

## 一、为什么选择 Kafka

在安全数据平台项目中，我们需要处理的场景：
- 漏洞扫描结果的异步采集（每日百万级消息）
- 多个微服务间的事件通知
- 操作审计日志的可靠存储
- 数据从采集到分析的 ETL 管道

对比了 RabbitMQ 和 Redis Streams 后选择 Kafka 的原因：
- **持久化**：消息默认写磁盘，重启不丢失
- **回溯消费**：可以重新消费历史消息（RabbitMQ 消费即删）
- **高吞吐**：单 broker 轻松 10 万+ TPS
- **消费者组**：天然支持水平扩展

## 二、Python confluent-kafka 实战

### 2.1 生产者

```python
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
import json
import socket

class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'client.id': socket.gethostname(),
            
            # 可靠性配置
            'acks': 'all',                    # 所有副本确认
            'retries': 3,                     # 重试次数
            'retry.backoff.ms': 100,
            'enable.idempotence': True,       # 幂等生产者
            
            # 性能配置
            'batch.size': 32768,              # 32KB 批量
            'linger.ms': 10,                  # 等待 10ms 凑批
            'compression.type': 'snappy',     # 压缩
            'buffer.memory': 67108864,        # 64MB 缓冲区
            
            # 回调
            'delivery.timeout.ms': 30000,
        })
    
    def send(self, topic: str, key: str, value: dict, 
             headers: dict = None, callback=None):
        """发送消息"""
        try:
            kafka_headers = [(k, v.encode()) for k, v in (headers or {}).items()]
            
            self.producer.produce(
                topic=topic,
                key=key.encode('utf-8'),
                value=json.dumps(value, ensure_ascii=False).encode('utf-8'),
                headers=kafka_headers,
                callback=callback or self._delivery_report,
            )
            
            # 触发回调处理（非阻塞）
            self.producer.poll(0)
        except BufferError:
            # 缓冲区满，等待一下
            self.producer.poll(1)
            self.producer.produce(
                topic=topic,
                key=key.encode('utf-8'),
                value=json.dumps(value).encode('utf-8'),
                callback=callback or self._delivery_report,
            )
    
    def _delivery_report(self, err, msg):
        if err:
            logger.error(f"Message delivery failed: {err}, topic={msg.topic()}, key={msg.key()}")
        else:
            logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}")
    
    def flush(self, timeout=10):
        """确保所有消息发送完毕"""
        remaining = self.producer.flush(timeout)
        if remaining > 0:
            logger.warning(f"{remaining} messages were not delivered")
    
    def __del__(self):
        self.flush()

# 使用示例
producer = KafkaProducer("kafka-1:9092,kafka-2:9092,kafka-3:9092")

# 发送漏洞扫描结果
producer.send(
    topic="vuln-scan-results",
    key=f"scanner-{scanner_id}",
    value={
        "scan_id": "scan-20240120-001",
        "target": "192.168.1.100",
        "vulnerabilities": [
            {"cve_id": "CVE-2024-1234", "severity": "high"},
        ],
        "timestamp": datetime.utcnow().isoformat(),
    },
    headers={"source": "nessus", "priority": "high"}
)
```

### 2.2 消费者

```python
from confluent_kafka import Consumer, KafkaError, KafkaException
import signal

class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list[str]):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',  # 新消费者组从头开始
            
            # 手动提交 offset
            'enable.auto.commit': False,
            
            # 消费配置
            'max.poll.interval.ms': 300000,    # 5 分钟处理超时
            'session.timeout.ms': 30000,
            'heartbeat.interval.ms': 10000,
            'fetch.min.bytes': 1024,           # 至少获取 1KB
            'fetch.wait.max.ms': 500,
            
            # 分区分配策略
            'partition.assignment.strategy': 'cooperative-sticky',
        })
        self.consumer.subscribe(topics)
        self.running = True
        
        # 优雅关闭
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
    
    def _shutdown(self, signum, frame):
        logger.info("Shutting down consumer...")
        self.running = False
    
    def consume(self, handler, batch_size=100, batch_timeout=1.0):
        """批量消费模式"""
        try:
            while self.running:
                messages = self.consumer.consume(
                    num_messages=batch_size, 
                    timeout=batch_timeout
                )
                
                if not messages:
                    continue
                
                # 过滤错误消息
                valid_messages = []
                for msg in messages:
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            continue
                        logger.error(f"Consumer error: {msg.error()}")
                        continue
                    valid_messages.append(msg)
                
                if not valid_messages:
                    continue
                
                # 批量处理
                try:
                    handler(valid_messages)
                    # 处理成功后提交 offset
                    self.consumer.commit(asynchronous=False)
                except Exception as e:
                    logger.error(f"Batch processing failed: {e}", exc_info=True)
                    # 不提交 offset，下次重新消费
                    # 可选：发送到死信队列
                    self._send_to_dlq(valid_messages, str(e))
        finally:
            self.consumer.close()
    
    def _send_to_dlq(self, messages, error_msg):
        """发送到死信队列"""
        for msg in messages:
            dlq_producer.send(
                topic=f"{msg.topic()}.dlq",
                key=msg.key().decode() if msg.key() else "",
                value={
                    "original_topic": msg.topic(),
                    "original_partition": msg.partition(),
                    "original_offset": msg.offset(),
                    "payload": msg.value().decode(),
                    "error": error_msg,
                    "failed_at": datetime.utcnow().isoformat(),
                }
            )

# 使用示例
def handle_scan_results(messages):
    """处理扫描结果批次"""
    records = []
    for msg in messages:
        data = json.loads(msg.value().decode())
        records.append(data)
    
    # 批量写入数据库
    bulk_insert_scan_results(records)
    logger.info(f"Processed {len(records)} scan results")

consumer = KafkaConsumer(
    bootstrap_servers="kafka-1:9092,kafka-2:9092",
    group_id="vuln-processor",
    topics=["vuln-scan-results"]
)
consumer.consume(handler=handle_scan_results, batch_size=200)
```

## 三、分区策略

### 3.1 分区数量选择

经验公式：**分区数 = max(消费者数, 目标吞吐量 / 单分区吞吐量)**

```bash
# 创建 topic
kafka-topics.sh --create \
    --topic vuln-scan-results \
    --partitions 12 \
    --replication-factor 3 \
    --config retention.ms=604800000 \
    --config max.message.bytes=10485760 \
    --bootstrap-server kafka-1:9092
```

### 3.2 自定义分区器

```python
# 按扫描器 ID 分区，保证同一扫描器的消息有序
def scanner_partitioner(key, all_partitions, available_partitions):
    """自定义分区策略：按 key hash 分配"""
    if key is None:
        return random.choice(available_partitions)
    
    key_bytes = key if isinstance(key, bytes) else key.encode()
    hash_value = int(hashlib.md5(key_bytes).hexdigest(), 16)
    return available_partitions[hash_value % len(available_partitions)]
```

## 四、消息可靠性保证

### 4.1 生产者可靠性

```python
# 核心配置组合
producer_config = {
    'acks': 'all',                # 所有 ISR 副本确认
    'enable.idempotence': True,   # 幂等性（防止重复发送）
    'max.in.flight.requests.per.connection': 5,  # 幂等模式下最大为 5
    'retries': 2147483647,        # 无限重试
}
```

### 4.2 消费者可靠性

```python
# 至少一次语义（at-least-once）
# 1. 关闭自动提交
# 2. 处理完成后手动提交
# 3. 业务层保证幂等

def idempotent_handler(messages):
    """幂等消费处理"""
    for msg in messages:
        msg_id = f"{msg.topic()}:{msg.partition()}:{msg.offset()}"
        
        # 检查是否已处理（Redis 去重）
        if redis.sismember("processed_messages", msg_id):
            logger.info(f"Skipping duplicate message: {msg_id}")
            continue
        
        # 处理消息
        process_message(msg)
        
        # 标记为已处理（设置过期时间，避免 Redis 无限增长）
        pipe = redis.pipeline()
        pipe.sadd("processed_messages", msg_id)
        pipe.expire("processed_messages", 86400 * 7)  # 7 天过期
        pipe.execute()
```

### 4.3 事务消息

```python
from confluent_kafka import Producer

transactional_producer = Producer({
    'bootstrap.servers': 'kafka-1:9092',
    'transactional.id': 'my-transactional-producer-001',
    'enable.idempotence': True,
})

transactional_producer.init_transactions()

try:
    transactional_producer.begin_transaction()
    
    # 发送多条消息（原子性）
    transactional_producer.produce('topic-a', key='k1', value='v1')
    transactional_producer.produce('topic-b', key='k2', value='v2')
    
    transactional_producer.commit_transaction()
except Exception as e:
    transactional_producer.abort_transaction()
    logger.error(f"Transaction failed: {e}")
```

## 五、监控与运维

### 5.1 关键监控指标

```python
from confluent_kafka.admin import AdminClient

admin = AdminClient({'bootstrap.servers': 'kafka-1:9092'})

def get_consumer_lag(group_id: str, topic: str):
    """获取消费者 lag"""
    consumer = Consumer({
        'bootstrap.servers': 'kafka-1:9092',
        'group.id': group_id,
    })
    
    # 获取已提交的 offset
    topic_partitions = [TopicPartition(topic, p) for p in range(12)]
    committed = consumer.committed(topic_partitions)
    
    # 获取最新 offset
    total_lag = 0
    for tp in committed:
        low, high = consumer.get_watermark_offsets(tp)
        lag = high - (tp.offset if tp.offset >= 0 else 0)
        total_lag += lag
        print(f"  Partition {tp.partition}: offset={tp.offset}, latest={high}, lag={lag}")
    
    consumer.close()
    return total_lag
```

### 5.2 告警规则

```yaml
# Prometheus 告警规则
groups:
  - name: kafka
    rules:
      - alert: KafkaConsumerLagHigh
        expr: kafka_consumergroup_lag_sum > 10000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consumer group {{ $labels.consumergroup }} lag is high: {{ $value }}"
      
      - alert: KafkaUnderReplicatedPartitions
        expr: kafka_server_replicamanager_underreplicatedpartitions > 0
        for: 1m
        labels:
          severity: critical
```

## 六、生产踩坑记录

**坑 1：消费者 rebalance 风暴**

消费者频繁加入/退出导致 rebalance，期间所有消费暂停。解决：
- 使用 `cooperative-sticky` 分配策略（增量 rebalance）
- 合理设置 `session.timeout.ms` 和 `heartbeat.interval.ms`
- 避免消息处理超过 `max.poll.interval.ms`

**坑 2：消息积压处理不过来**

突然的流量尖峰导致消费跟不上。解决：
- 增加分区数和消费者实例
- 消费者内部用线程池并行处理
- 对非关键消息设置 TTL，过期直接跳过

**坑 3：大消息导致超时**

单条消息 5MB，fetch 一次就超时了。解决：
- 大数据存对象存储，Kafka 只传引用
- 调整 `max.message.bytes` 和 `fetch.max.bytes`

## 总结

Kafka 在微服务中的实践要点：

1. **可靠性配置**：`acks=all` + 幂等生产者 + 手动提交 offset
2. **分区策略**：根据业务选择分区数和分区键，保证局部有序
3. **批量处理**：消费端批量拉取 + 批量写入，提升吞吐
4. **死信队列**：消费失败的消息发到 DLQ，防止阻塞主流程
5. **监控 lag**：消费者 lag 是最核心的监控指标
6. **容量规划**：分区数一旦设定不建议减少，提前规划
