---
title: "高可用"
summary: "高可用 作用 对数据备份, 实现高可用 HA 通过读写分离, 提高吞吐量, 实现高性能 主从复制原理 Mysql的复制是一个异步的复制过程 过程本质为 Slave 从 Master 端获取 Binary Log, 然后再在自己身上完全顺序的执行日志中所记录的各种操作 MySQL 复制的基本过程如下: Slave 上面的 IO 线程连接上 Master，"
board: "tech"
category: "数据库"
tags:
  - "MySQL"
  - "数据库"
  - "SQL"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

# 高可用
1. 作用  
对数据备份, 实现高可用 HA  
通过读写分离, 提高吞吐量, 实现高性能
2. 主从复制原理  
Mysql的复制是一个异步的复制过程  
过程本质为 Slave 从 Master 端获取 Binary Log, 然后再在自己身上完全顺序的执行日志中所记录的各种操作  
MySQL 复制的基本过程如下:  
Slave 上面的 IO 线程连接上 Master，  并请求从指定日志文件的指定位置之后的日志内容;  
Master 接收到来自 Slave 的 IO 线程的请求后，   通过负责复制的IO线程 根据请求信息读取日志信息，  
返回给 Slave 端的 IO 线程。  
Slave 的 IO 线程接收到信息后，将接收到的日志内容依次写入到 Slave 端的 Relay Log文件  
Slave 的 SQL 线程检测到 Relay Log 中新增加了内容后，会马上解析该文件中的内容, 并在自身执行这 些 原始SQL语句。


django： mvt， model模型(数据) 、view(视图接收请求，处理响应) 、template(模板渲染数据)  
flask： mvc， model没有， template(Jinja2)， werkzeug(接收请求，处理响应)

# 2.读写分离
## 实现读写分离
  
sqlalchemy 没有内置的读写分离方案, 但是提供了可以自定义的接口 : 官方参考文档示例, 我们可以借此对 flask-sqlalchemy 进行二次开发, 实现读写分离  
https://docs.sqlalchemy.org/en/13/orm/persistence techniques.html#custom-vertical- partitioning 

## 基于flask-sqlalchemy实现读写分离
实现思路分两步:  
1.实现自定义的session类, 继承SignallingSession类  
重写 get bind方法，根据读写需求选择对应的数据库地址  
2.实现自定义的SQLAlchemy类, 继承flask-sqlalchemy提供的SQLAlchemy类。  
重写 create session方法, 在内部使用自定义的 Session类


#现有代码中使用原生 SQLAlchemy类，没有读写分离机制，弃用

db = SQLAlchemy()


#SQLALCHEMY BINDS替换掉原生的SQLALCHEMY DATABASE URI

SQLALCHEMY DATABASE URI = 'postgres://localhost/main'  
_         _  
SQLALCHEMY BINDS = {  
'master': 'mysql://10.211.55.34:3306/toutiao',  
'slave1': 'mysql:///10.211.55.34:8306/toutiao',  
'slave2': 'mysql:///10.211.55.34:8306/toutiao'  
}  
class MyDBSession(SignallingSession):

# 根据不同的数据库操作，返回不同的数据库地址，主库或从库

def get bind():

pass


class MySQLAlchemy(SQLAlchemy):

def create  session(self, options):

return orm.sessionmaker(class  =MyDBSession, db=self, **options)

db = MySQLAlchemy()


[数据库mysql.pdf](https://www.yuque.com/attachments/yuque/0/2023/pdf/38572666/1693967526404-72733dc6-2c94-4657-bc57-4a9a51edbdca.pdf)
