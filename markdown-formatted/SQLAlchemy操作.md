---
title: "测试"
summary: "SQLAlchemy操作 模型 class User(db.Model): """ ⽤户基本信息 """ __tablename__ = 'user_basic' class STATUS: ENABLE = 1 DISABLE = 0 id = db.Column('user_id', db."
board: "tech"
category: "编程语言-Python"
tags:
  - "SQLAlchemy"
  - "Python"
  - "ORM"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

SQLAlchemy操作  
模型  
  
class User(db.Model): 

""" 

⽤户基本信息 

 """ 

__tablename__ = 'user_basic' 

class STATUS: 

ENABLE = 1 

DISABLE = 0 

id = db.Column('user_id', db.Integer, primary_key=True, doc='⽤户ID') 

mobile = db.Column(db.String, doc='⼿机号') 

password = db.Column(db.String, doc='密码') 

name = db.Column('user_name', db.String, doc='昵称') 

profile_photo = db.Column(db.String, doc='头像') 

last_login = db.Column(db.DateTime, doc='最后登录时间') 

is_media = db.Column(db.Boolean, default=False, doc='是否是⾃媒体') 

is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证') 

introduction = db.Column(db.String, doc='简介') 

certificate = db.Column(db.String, doc='认证') 

article_count = db.Column(db.Integer, default=0, doc='发帖数') 

following_count = db.Column(db.Integer, default=0, doc='关注的⼈数') 

fans_count = db.Column(db.Integer, default=0, doc='被关注的⼈数（粉丝数）') 

like_count = db.Column(db.Integer, default=0, doc='累计点赞⼈数') 

read_count = db.Column(db.Integer, default=0, doc='累计阅读⼈数') 

account = db.Column(db.String, doc='账号') 

email = db.Column(db.String, doc='邮箱') 

status = db.Column(db.Integer, default=1, doc='状态，是否可⽤') 

class UserProfile(db.Model): 

""" 

⽤户资料表 

 """ 

__tablename__ = 'user_profile' 

class GENDER: 

MALE = 0 

FEMALE = 1 

id = db.Column('user_id', db.Integer, primary_key=True, doc='⽤户ID') 

gender = db.Column(db.Integer, default=0, doc='性别') 

birthday = db.Column(db.Date, doc='⽣⽇')

real_name = db.Column(db.String, doc='真实姓名') 

id_number = db.Column(db.String, doc='身份证号') 

id_card_front = db.Column(db.String, doc='身份证正⾯') 

id_card_back = db.Column(db.String, doc='身份证背⾯') 

id_card_handheld = db.Column(db.String, doc='⼿持身份证') 

ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间') 

utime = db.Column('update_time', db.DateTime, default=datetime.now, 

onupdate=datetime.now, doc='更新时间') 

register_media_time = db.Column(db.DateTime, doc='注册⾃媒体时间') 

area = db.Column(db.String, doc='地区') 

company = db.Column(db.String, doc='公司') 

career = db.Column(db.String, doc='职业') 

class Relation(db.Model): 

""" 

⽤户关系表 

 """ 

__tablename__ = 'user_relation' 

class RELATION: 

DELETE = 0 

FOLLOW = 1 

BLACKLIST = 2 

id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID') 

user_id = db.Column(db.Integer, doc='⽤户ID') 

target_user_id = db.Column(db.Integer, doc='⽬标⽤户ID') 

relation = db.Column(db.Integer, doc='关系') 

ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间') 

utime = db.Column('update_time', db.DateTime, default=datetime.now, 

onupdate=datetime.now, doc='更新时间')

##   
1 新增
  
user = User(mobile='15612345678', name='itcast') 

db.session.add(user) 

db.session.commit() 

profile = Profile(id=user.id) 

db.session.add(profile) 

db.session.commit()


批量添加：


db.session.add_all([user1, user2, user3]) 

db.session.commit()  
  
2 查询  
all()  
查询所有，返回列表

`User.query.all()`

  
first()  
查询第⼀个，返回对象

`User.query.first()`

  
get()  
根据主键ID获取对象，若主键不存在返回None  
另⼀种查询⽅式

`User.query.get(2)`

  
filter_by  
进⾏过滤

``User.query.filter_by(mobile='13911111111').first() 

User.query.filter_by(mobile='13911111111', id=1).first() # and关系 

  
filter  
进⾏过滤

`User.query.filter(User.mobile=='13911111111').first()`

  
逻辑或

``from sqlalchemy import or_ 

User.query.filter(or_(User.mobile=='13911111111', User.name.endswith('号'))).all()

  
逻辑与

``from sqlalchemy import and_ 

User.query.filter(and_(User.name != '13911111111', 

User.mobile.startswith('185'))).all()

offset  
逻辑⾮

``from sqlalchemy import not_ 

User.query.filter(not_(User.mobile == '13911111111')).all()


offset  
偏移，起始位置

`User.query.offset(2).all()`

  
limit  
获取限制数据

`User.query.limit(3).all()`

  
order_by  
排序

``User.query.order_by(User.id).all() # 默认正序 

User.query.order_by(User.id.desc()).all() # 倒序

  
复合查询

``User.query.filter(User.name.startswith('13')).order_by(User.id.desc()).offset(2).limit( 

5).all() 

query = User.query.filter(User.name.startswith('13')) 

query = query.order_by(User.id.desc()) 

query = query.offset(2).limit(5) 

ret = query.all()

  
优化查询

``user = User.query.filter_by(id=1).first() # 查询所有字段 

select user_id, mobile...... 

select * from# 程序不要使⽤ 

select user_id, mobile,.... # 查询指定字段 

from sqlalchemy.orm import load_only 

User.query.options(load_only(User.name, User.mobile)).filter_by(id=1).first() # 查询特定 

字段

  
聚合查询

``from sqlalchemy import func 

db.session.query(Relation.user_id,func.count(Relation.target_user_id)).filter(Relation. 

relation == Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()

  
关联查询

1. 使⽤ForeignKey

``class User(db.Model): 

 ... 

profile = db.relationship('UserProfile', uselist=False) 

followings = db.relationship('Relation') 

class UserProfile(db.Model): 

id = db.Column('user_id', db.Integer, db.ForeignKey('user_basic.user_id'), 

primary_key=True, doc='⽤户ID') 

 ... 

class Relation(db.Model): 

user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='⽤户ID') 

 ... 

# 测试

user = User.query.get(1) 

user.profile.gender 

user.followings


2. 使⽤primaryjoin

``class User(db.Model): 

 ... 

profile = 

db.relationship('UserProfile',primaryjoin='User.id==foreign(UserProfile.id)', 

uselist=False) 

followings = 

db.relationship('Relation',primaryjoin='User.id==foreign(Relation.user_id)') 

# 测试 

user = User.query.get(1) 

user.profile.gender 

user.followings 

  
3. 指定字段关联查询

``class Relation(db.Model): 

 ... 

target_user = db.relationship('User', 

primaryjoin='Relation.target_user_id==foreign(User.id)', uselist=False) 

from sqlalchemy.orm import load_only, contains_eager 

Relation.query.join(Relation.target_user).options(load_only(Relation.target_user_id), 

contains_eager(Relation.target_user).load_only(User.name)).all()

  
3 更新  
⽅式⼀

``user = User.query.get(1) 

user.name = 'Python' 

db.session.add(user) 

db.session.commit()

  
⽅式⼆

``User.query.filter_by(id=1).update({'name':'python'}) 

db.session.commit()

  
4 删除  
⽅式⼀  


``user = User.query.order_by(User.id.desc()).first() 

db.session.delete(user) 

db.session.commit()

⽅式⼆ 

User.query.filter(User.mobile=='18512345678').delete() 

db.session.commit()

# [SQLAlchemy操作.pdf](https://www.yuque.com/attachments/yuque/0/2026/pdf/38572666/1769411720251-07016b1d-c977-4102-a2d3-c2d51383edee.pdf)
