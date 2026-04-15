---
title: "Celery 分布式任务队列生产实践"
category: "编程语言-Python"
board: "tech"
tags: ["Celery", "分布式", "任务队列", "Python"]
summary: "Celery 生产环境配置与调优，涵盖 worker 管理、任务编排、错误重试、监控告警等实战经验"
is_published: true
created_at: "2024-04-18T10:00:00Z"
updated_at: "2024-04-18T10:00:00Z"
---

# Celery 分布式任务队列生产实践

Celery 是 Python 生态中最成熟的分布式任务队列。但从开发环境到生产环境，中间有大量的坑需要踩。本文总结我在多个项目中使用 Celery 的生产经验，包括配置调优、任务编排、错误处理和监控方案。

## 一、生产级配置

### 1.1 Celery 配置文件

```python
# celery_config.py
from celery import Celery
from kombu import Queue, Exchange

app = Celery('myapp')

app.conf.update(
    # Broker 配置（推荐 RabbitMQ，Redis 也可）
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    
    # 序列化配置
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # 时区
    timezone='Asia/Shanghai',
    enable_utc=True,
    
    # Worker 配置
    worker_prefetch_multiplier=4,      # 预取数量，CPU密集型设为1
    worker_max_tasks_per_child=1000,   # 防止内存泄漏
    worker_max_memory_per_child=400_000,  # 400MB 内存限制
    
    # 任务配置
    task_acks_late=True,               # 任务完成后才确认
    task_reject_on_worker_lost=True,   # worker 异常退出时拒绝任务（重新入队）
    task_time_limit=600,               # 硬超时 10 分钟
    task_soft_time_limit=540,          # 软超时 9 分钟
    
    # 结果配置
    result_expires=86400,              # 结果保留 24 小时
    result_compression='gzip',
    
    # 队列配置
    task_queues=(
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('high_priority', Exchange('high_priority'), routing_key='high'),
        Queue('low_priority', Exchange('low_priority'), routing_key='low'),
        Queue('email', Exchange('email'), routing_key='email'),
        Queue('data_sync', Exchange('data_sync'), routing_key='sync'),
    ),
    task_default_queue='default',
    
    # 路由配置
    task_routes={
        'app.tasks.email.*': {'queue': 'email'},
        'app.tasks.sync.*': {'queue': 'data_sync'},
        'app.tasks.critical.*': {'queue': 'high_priority'},
        'app.tasks.report.*': {'queue': 'low_priority'},
    },
)
```

### 1.2 Worker 启动策略

```bash
# 高优先级队列：更多并发
celery -A myapp worker -Q high_priority -c 8 -n high@%h --loglevel=warning

# 默认队列
celery -A myapp worker -Q default -c 4 -n default@%h --loglevel=warning

# 邮件队列：单独隔离，防止影响核心业务
celery -A myapp worker -Q email -c 2 -n email@%h --loglevel=warning

# 数据同步队列：CPU 密集型，用 prefork + 低并发
celery -A myapp worker -Q data_sync -c 2 -P prefork -n sync@%h \
    --max-tasks-per-child=100 --loglevel=warning
```

**为什么分队列？** 生产环境中我遇到过一个血的教训：邮件发送任务因为 SMTP 服务器超时导致队列堆积，直接把核心的数据处理任务也堵住了。分队列隔离后，各个业务互不影响。

## 二、任务编排

### 2.1 基础任务定义

```python
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,        # 指数退避
    retry_backoff_max=600,     # 最大退避 10 分钟
    retry_jitter=True,         # 添加随机抖动
    acks_late=True,
    track_started=True,
)
def process_data(self, data_id: int):
    """数据处理任务"""
    try:
        logger.info(f"Processing data {data_id}, attempt {self.request.retries + 1}")
        result = heavy_computation(data_id)
        return {"status": "success", "data_id": data_id, "result": result}
    except SoftTimeLimitExceeded:
        logger.warning(f"Task soft timeout for data {data_id}")
        # 保存中间状态，下次可以从断点恢复
        save_checkpoint(data_id, self.request.retries)
        raise self.retry(countdown=120)
    except Exception as exc:
        logger.error(f"Failed to process data {data_id}: {exc}", exc_info=True)
        if self.request.retries >= self.max_retries:
            # 最终失败，发送告警
            send_alert(f"Task permanently failed: data {data_id}")
        raise
```

### 2.2 任务链与组

```python
from celery import chain, group, chord

# Chain：顺序执行
pipeline = chain(
    fetch_data.s(source_url),           # 1. 拉取数据
    validate_data.s(),                   # 2. 数据校验（上一步结果自动传入）
    transform_data.s(target_format),     # 3. 数据转换
    save_to_database.s(),                # 4. 保存
    notify_completion.si(user_id),       # 5. 通知（si = immutable signature，不接收上游结果）
)
pipeline.apply_async()

# Group：并行执行
parallel_tasks = group([
    process_chunk.s(chunk) for chunk in data_chunks
])
result = parallel_tasks.apply_async()

# Chord：并行执行 + 汇总回调
batch_job = chord(
    [process_item.s(item_id) for item_id in item_ids],
    aggregate_results.s()  # 所有并行任务完成后执行汇总
)
batch_job.apply_async()
```

### 2.3 周期任务（Celery Beat）

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    # 每天凌晨 2 点同步漏洞数据
    'sync-vulnerability-data': {
        'task': 'app.tasks.sync.sync_vulnerabilities',
        'schedule': crontab(hour=2, minute=0),
        'kwargs': {'full_sync': False},
    },
    # 每 5 分钟检查任务队列积压
    'check-queue-depth': {
        'task': 'app.tasks.monitor.check_queue_depth',
        'schedule': 300.0,
        'options': {'queue': 'high_priority'},
    },
    # 每周一生成周报
    'weekly-report': {
        'task': 'app.tasks.report.generate_weekly',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
    # 每小时清理过期缓存
    'cleanup-expired-cache': {
        'task': 'app.tasks.maintenance.cleanup_cache',
        'schedule': crontab(minute=30),
    },
}
```

## 三、错误处理与重试策略

### 3.1 区分可重试和不可重试错误

```python
class PermanentError(Exception):
    """不可重试的错误"""
    pass

class TransientError(Exception):
    """可重试的错误"""
    pass

@shared_task(bind=True, max_retries=3)
def call_external_api(self, endpoint: str, payload: dict):
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as exc:
        # 网络错误：可重试
        raise self.retry(exc=exc, countdown=30)
    except requests.exceptions.HTTPError as exc:
        if exc.response.status_code == 429:
            # 限流：等待更长时间重试
            retry_after = int(exc.response.headers.get('Retry-After', 60))
            raise self.retry(exc=exc, countdown=retry_after)
        elif exc.response.status_code >= 500:
            # 服务器错误：可重试
            raise self.retry(exc=exc, countdown=60)
        else:
            # 4xx 错误（除429）：不重试
            logger.error(f"Permanent failure: {exc}")
            raise PermanentError(str(exc))
```

### 3.2 死信队列处理

```python
@app.task(bind=True)
def on_task_failure(self, exc, task_id, args, kwargs, einfo):
    """全局任务失败回调"""
    # 记录到数据库
    FailedTask.objects.create(
        task_id=task_id,
        task_name=self.name,
        args=json.dumps(args),
        kwargs=json.dumps(kwargs),
        exception=str(exc),
        traceback=str(einfo),
        failed_at=datetime.utcnow(),
    )
    
    # 发送告警
    if isinstance(exc, PermanentError):
        send_alert(f"Permanent task failure: {self.name} ({task_id})")

# 注册全局错误处理
app.conf.task_annotations = {
    '*': {
        'on_failure': on_task_failure,
    }
}
```

## 四、幂等性设计

生产中任务可能被重复执行（worker 重启、网络抖动等），必须保证幂等：

```python
import hashlib

@shared_task(bind=True)
def process_order(self, order_id: int):
    """幂等的订单处理任务"""
    # 方案 1：Redis 分布式锁
    lock_key = f"task_lock:process_order:{order_id}"
    lock = redis_client.lock(lock_key, timeout=300, blocking=False)
    
    if not lock.acquire(blocking=False):
        logger.info(f"Order {order_id} is already being processed")
        return {"status": "skipped", "reason": "duplicate"}
    
    try:
        # 方案 2：数据库层面的状态检查
        order = Order.objects.select_for_update().get(id=order_id)
        if order.status != "pending":
            logger.info(f"Order {order_id} already processed (status={order.status})")
            return {"status": "skipped"}
        
        # 处理订单
        order.status = "processing"
        order.save()
        
        result = do_process(order)
        
        order.status = "completed"
        order.save()
        
        return {"status": "success", "order_id": order_id}
    finally:
        lock.release()
```

## 五、监控与告警

### 5.1 Flower 监控

```bash
# 启动 Flower
celery -A myapp flower --port=5555 --broker_api=redis://localhost:6379/0 \
    --basic_auth=admin:secret
```

### 5.2 自定义 Prometheus 指标

```python
from prometheus_client import Counter, Histogram, Gauge
from celery.signals import task_prerun, task_postrun, task_failure

task_counter = Counter('celery_tasks_total', 'Total tasks', ['task_name', 'status'])
task_duration = Histogram('celery_task_duration_seconds', 'Task duration', ['task_name'])
active_tasks = Gauge('celery_active_tasks', 'Active tasks', ['queue'])

@task_prerun.connect
def on_task_start(sender=None, **kwargs):
    sender._start_time = time.time()
    active_tasks.labels(queue=sender.request.delivery_info.get('routing_key', 'unknown')).inc()

@task_postrun.connect
def on_task_end(sender=None, **kwargs):
    duration = time.time() - getattr(sender, '_start_time', time.time())
    task_duration.labels(task_name=sender.name).observe(duration)
    task_counter.labels(task_name=sender.name, status='success').inc()
    active_tasks.labels(queue=sender.request.delivery_info.get('routing_key', 'unknown')).dec()

@task_failure.connect
def on_task_fail(sender=None, **kwargs):
    task_counter.labels(task_name=sender.name, status='failure').inc()
    active_tasks.labels(queue=sender.request.delivery_info.get('routing_key', 'unknown')).dec()
```

### 5.3 队列积压监控

```python
@shared_task
def check_queue_depth():
    """检查各队列积压情况"""
    from celery.app.control import Inspect
    
    queues_to_check = ['default', 'high_priority', 'email', 'data_sync']
    
    for queue_name in queues_to_check:
        depth = redis_client.llen(queue_name)
        
        # 记录指标
        queue_depth_gauge.labels(queue=queue_name).set(depth)
        
        # 告警阈值
        thresholds = {
            'high_priority': 50,
            'default': 200,
            'email': 500,
            'data_sync': 100,
        }
        
        if depth > thresholds.get(queue_name, 100):
            send_alert(
                f"Queue '{queue_name}' depth alert: {depth} "
                f"(threshold: {thresholds.get(queue_name, 100)})"
            )
```

## 六、踩坑记录

**坑 1：pickle 反序列化漏洞**
默认序列化用的是 pickle，存在 RCE 风险。必须改为 JSON。

**坑 2：task_acks_late 与 visibility_timeout**
开启 `task_acks_late` 后，如果任务执行时间超过 Redis 的 `visibility_timeout`（默认 1 小时），任务会被重新分配给其他 worker，导致重复执行。解决方案：

```python
app.conf.broker_transport_options = {
    'visibility_timeout': 43200,  # 12 小时
}
```

**坑 3：内存泄漏**
长期运行的 worker 可能因为第三方库的内存泄漏导致 OOM。`worker_max_tasks_per_child` 和 `worker_max_memory_per_child` 是保命配置。

**坑 4：Django ORM 连接池耗尽**
Celery worker 的每个进程都会创建数据库连接。4 个 worker * 4 并发 = 16 个连接。配合 `CONN_MAX_AGE` 和 `close_old_connections()` 使用。

## 总结

Celery 生产环境的核心原则：

1. **队列隔离**：不同业务走不同队列，避免相互阻塞
2. **任务幂等**：假设任何任务都可能重复执行
3. **错误分级**：区分可重试和不可重试错误
4. **监控先行**：上线前先搭好 Flower + Prometheus 监控
5. **资源限制**：内存、超时、并发数都要配上限
