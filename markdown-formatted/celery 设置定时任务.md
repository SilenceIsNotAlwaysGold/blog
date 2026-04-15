---
title: "celery 设置定时任务"
summary: "要在Celery中设置定时任务，你需要执行以下步骤： 安装Celery：你需要确保系统中已经安装了Celery。你可以使用pip命令来安装Celery，例如 `pip install celery`。 **创建Celery应用**：在你的项目中，你需要创建一个Celery应用。这个应用将用于管理任务队列和定时任务。通常，"
board: "tech"
category: "编程语言-Python"
tags:
  - "Celery"
  - "Python"
  - "任务队列"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

要在Celery中设置定时任务，你需要执行以下步骤：


1.  安装Celery：你需要确保系统中已经安装了Celery。你可以使用pip命令来安装Celery，例如 `pip install celery`。 
2.  **创建Celery应用**：在你的项目中，你需要创建一个Celery应用。这个应用将用于管理任务队列和定时任务。通常，你需要在一个独立的Python文件中创建Celery应用，例如 `celery.py`。 

```python
from celery import Celery

app = Celery('your_app_name', broker='your_broker_url')
```

  
在上面的代码中，你需要提供一个应用名（'your_app_name'）和一个消息代理（broker）。消息代理用于存储任务消息，例如使用Redis或RabbitMQ等。你需要根据你自己的需求设置消息代理。 

3.  **定义任务函数**：在你的应用中，你需要定义要执行的任务函数。这些函数将被Celery调度执行。例如，你可以在你的`celery.py`文件中定义一个简单的任务函数。 

```python
@app.task
def your_task():
    # 执行任务的逻辑
    pass
```

 

4.  **设置定时任务**：要设置定时任务，你可以使用Celery应用的`beat_schedule`属性。这个属性是一个字典，用于定义定时任务的调度规则。你可以在`celery.py`文件中添加以下代码： 

```python
app.conf.beat_schedule = {
    'your_task_name': {
        'task': 'your_task',
        'schedule': 10,  # 指定任务的执行频率，单位为秒
    },
}
```

  
在上面的代码中，你需要为定时任务指定一个名称（'your_task_name'），同时指定要执行的任务函数（'your_task'）以及任务的执行频率（10秒）。 

5.  **启动Celery worker 和 beat**：在你的终端中，进入你的项目目录，并执行以下命令来启动Celery worker 和 beat： 

```python
celery -A your_project_name worker --loglevel=info
celery -A your_project_name beat --loglevel=info
```

  
请将上面的命令中的`your_project_name`替换为你的项目名称。 


现在，你已经成功设置了定时任务。Celery将会按照你定义的调度规则自动执行任务函数。


执行任务的对象是worker，因此需要创建一个worker，创建worker可以使用如下命令：


celery worker -A task -l info -P eventlet

1

-A参数：表示Celery对象所在的py文件的文件名，会自动记录task.py里面被@app.task装饰的函数。

-l参数：日志级别

-P参数：表示事件驱动使用eventlet，这个需要在Windows平台设置，但在Linux平台不需要

-c参数：表示并发数量，比如再加上-c 10，表示限制并发数量为10
