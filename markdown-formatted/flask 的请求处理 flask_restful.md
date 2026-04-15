---
title: "Look only in the POST body"
summary: "Flask-RESTful 提供了RequestParser类，用来帮助我们检验和转换请求数据。 创建RequestParser对象 : parser = reqparse.RequestParser() **required** :描述请求是否一定要携带对应参数，"
board: "tech"
category: "编程语言-Python"
tags:
  - "Flask"
  - "Python"
  - "Web框架"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

Flask-RESTful 提供了RequestParser类，用来帮助我们检验和转换请求数据。

```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted', location='args')
parser.add_argument('name')
args = parser.parse_args()
```

1. 创建RequestParser对象 :
    1. parser = reqparse.RequestParser()
    2.  	**required** :描述请求是否一定要携带对应参数，**默认值为False **True 强制要求携带
2. 向RequestParser对象中添加需要检验或转换的参数声明
    1. parser.add_argument('rate', type=int, help='Rate cannot be converted', location='args')
    2. parser.add_argument('name')
        1. help : 参数检验错误时返回的错误描述信息
        2. action "描述对于请求参数中出现多个同名参数时的处理方式
                - action='store' 保留出现的第一个， 默认
                - action='append' 以列表追加保存所有同名参数的值
        3. type:描述参数应该匹配的类型，可以使用python的标准数据类型string、int，也可使用Flask-RESTful提供的检验方法，还可以自己定义
        4. Flask-RESTful提供的正则校验：

```python
from flask_restful import inputs
rp.add_argument('a', type=inputs.regex(r'^\d{2}&'))
```

        5. int_range(low ,high) 整数范围

```python
rp.add_argument('a', type=inputs.int_range(1, 10))
```

        6. location：
            1. 描述参数应该在请求数据中出现的位置

```python
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From json
parser.add_argument('user_id', location='json')

# From file uploads
parser.add_argument('picture', location='files')
```

也可指明多个位置

```python
parser.add_argument('text', location=['headers', 'json'])
```


3. 使用parse_args()方法启动检验处理

args = parser.parse_args()

检验之后从检验结果中获取参数时可按照字典操作或对象属性操作

args.rate  
或  
args['rate']
