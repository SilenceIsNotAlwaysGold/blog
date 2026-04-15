---
title: "requests"
summary: "![](https://cdn.nlark.com/yuque/0/2024/png/38572666/1710416564641-93aa3d01-1d33-4285-8924-b184cd191fef.png) session()：会话，web项目从登录和退出就是一个会话。"
board: "tech"
category: "编程语言-Python"
tags:
  - "Requests"
  - "Python"
  - "HTTP"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

![](https://cdn.nlark.com/yuque/0/2024/png/38572666/1710416564641-93aa3d01-1d33-4285-8924-b184cd191fef.png)


session()：会话，web项目从登录和退出就是一个会话。


post请求中data传参和json传参的本质:

**Postman中Post请求的四种不同的传参方式以及它们对应的请求头:**

文件上传:Content-Type:multipart/form-data

表单:Content-Type:application/x-www-form-urlencoded

文本:

Content-Type:application/json

Content-Type:text/plain

Content-Type:application/javascript

Content-Type:text/html

Content-Type:application/xml

二进制:

Content-Type:application/octrent-stream


## 解析requests底层原理:
好的，我将更详细地说明每个部分的作用和相关内容：


### GET请求传参


+ **params**: 用于传递GET请求的查询参数，通常是一个字典或者字符串。


### POST或PUT请求传参


+ **data**: 用于传递POST或PUT请求的数据，通常是一个字典或者字符串。
+ **json**: 用于传递POST或PUT请求的JSON数据，通常是一个字典。
+ **files**: 用于上传文件的参数，通常是一个字典，包含文件名和文件对象。


### 请求头


+ **headers**: 包含HTTP请求的头部信息，通常是一个字典。


### Cookie信息


+ **cookies**: 用于传递Cookie信息，通常是一个字典。


### 文件上传


+ **files**: 用于上传文件的参数，通常是一个字典，包含文件名和文件对象。


### 鉴权


+ **auth**: 用于指定HTTP身份验证的方式，通常是一个元组，包含用户名和密码。


### 超时处理


+ **timeout**: 指定请求的超时时间，通常是一个浮点数，单位是秒。


### 其他请求参数


+ **allow_redirects**: 是否允许重定向，通常是一个布尔值。
+ **proxies**: 用于指定代理服务器，通常是一个字典。
+ **hooks**: 用于指定回调函数，以便在请求的不同阶段执行自定义操作，通常是一个字典。
+ **stream**: 是否以流的方式处理响应数据，通常是一个布尔值。
+ **verify**: 是否进行SSL证书验证，通常是一个布尔值或指定证书路径的字符串。
+ **cert**: 用于指定客户端SSL证书的路径，通常是一个元组，包含证书和私钥的路径。


### 代理


+ **proxies**: 用于指定代理服务器，通常是一个字典。


### 钩子


+ **hooks**: 用于指定回调函数，以便在请求的不同阶段执行自定义操作，通常是一个字典。


### 文件下载


+ **stream**: 是否以流的方式处理响应数据，通常是一个布尔值。


### 证书验证


+ **verify**: 是否进行SSL证书验证，通常是一个布尔值或指定证书路径的字符串。
+ **cert**: 用于指定客户端SSL证书的路径，通常是一个元组，包含证书和私钥的路径。


### CA证书


+ **cert**: 用于指定客户端SSL证书的路径，通常是一个元组，包含证书和私钥的路径。


这样详细地解释了每个部分的作用和相关内容，希望能够帮助到你更好地理解请求参数的使用。
