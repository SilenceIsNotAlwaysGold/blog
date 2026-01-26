---
feature: personal-blog
complexity: complex
generated_by: clarify
generated_at: 2026-01-26T10:30:00Z
version: 1
---

# 需求文档: 个人博客系统

> **功能标识**: personal-blog
> **复杂度**: complex
> **生成方式**: clarify
> **生成时间**: 2026-01-26

## 1. 概述

### 1.1 一句话描述
创建一个双板块个人博客系统，包含私密的生活记录板块和公开的技术展示板块，用于个人内容创作和技能展示。

### 1.2 核心价值
- **生活板块**：提供私密空间记录生活随笔、日记和感悟，仅自己和亲密朋友可访问
- **技术板块**：公开展示技术文章、项目经历和技能栈，作为面试时的技术作品集
- **个人品牌**：通过技术内容输出建立个人技术品牌，提升职业竞争力
- **知识沉淀**：系统化整理和积累个人技术知识体系

### 1.3 目标用户
- **主要用户（本人）**：博客内容创作者，需要便捷的文章编辑和管理功能
- **次要用户（招聘方）**：查看技术文章和项目经历，评估技术能力
- **次要用户（技术社区）**：阅读技术文章，通过邮件或点赞进行互动
- **次要用户（亲密朋友）**：查看生活板块内容（需授权）

---

## 2. 需求与用户故事

### 2.1 需求清单

| ID | 需求点 | 优先级 | 用户故事 |
|----|--------|--------|----------|
| R-001 | 双板块内容管理 | P0 | As a 博主, I want 分别管理生活和技术两个板块的内容, so that 可以区分私密和公开内容 |
| R-002 | 权限控制系统 | P0 | As a 博主, I want 生活板块需要登录才能访问，技术板块完全公开, so that 保护隐私同时展示技术能力 |
| R-003 | 富文本 Markdown 编辑器 | P0 | As a 博主, I want 使用所见即所得的 Markdown 编辑器编写文章, so that 提升写作体验和效率 |
| R-004 | 文章分类和标签 | P0 | As a 博主, I want 为文章添加分类和标签, so that 方便内容组织和检索 |
| R-005 | 个人履历展示系统 | P0 | As a 招聘方, I want 查看博主的技能树、项目经历和简历信息, so that 评估技术能力和工作经验 |
| R-006 | 文章点赞功能 | P1 | As a 访客, I want 为喜欢的技术文章点赞, so that 表达认可和支持 |
| R-007 | 邮件联系功能 | P1 | As a 访客, I want 通过联系表单发送邮件给博主, so that 进行技术交流或合作洽谈 |
| R-008 | 文章搜索功能 | P1 | As a 访客, I want 按关键词搜索技术文章, so that 快速找到感兴趣的内容 |
| R-009 | 响应式设计 | P1 | As a 访客, I want 在手机和电脑上都能良好浏览, so that 随时随地阅读文章 |
| R-010 | 数据统计展示 | P2 | As a 博主, I want 查看文章阅读量、点赞数等统计数据, so that 了解内容受欢迎程度 |

### 2.2 验收标准

#### R-001: 双板块内容管理
- **WHEN** 博主登录后台管理系统, **THEN** 系统 **SHALL** 提供"生活板块"和"技术板块"两个独立的内容管理入口
- **WHEN** 博主创建文章时, **THEN** 系统 **SHALL** 要求选择所属板块（生活/技术）
- **WHEN** 博主查看文章列表时, **THEN** 系统 **SHALL** 支持按板块筛选文章

#### R-002: 权限控制系统
- **WHEN** 未登录用户访问生活板块文章, **THEN** 系统 **SHALL** 跳转到登录页面
- **WHEN** 未登录用户访问技术板块文章, **THEN** 系统 **SHALL** 允许直接阅读
- **WHEN** 博主登录后, **THEN** 系统 **SHALL** 允许访问所有板块内容
- **WHEN** 授权用户登录后, **THEN** 系统 **SHALL** 允许访问生活板块内容

#### R-003: 富文本 Markdown 编辑器
- **WHEN** 博主创建或编辑文章时, **THEN** 系统 **SHALL** 提供所见即所得的 Markdown 编辑器
- **WHEN** 博主在编辑器中输入 Markdown 语法时, **THEN** 系统 **SHALL** 实时渲染预览效果
- **WHEN** 博主点击工具栏按钮时, **THEN** 系统 **SHALL** 插入对应的 Markdown 语法
- **WHEN** 博主上传图片时, **THEN** 系统 **SHALL** 支持图片上传并自动插入图片链接
- **WHEN** 博主编写代码块时, **THEN** 系统 **SHALL** 支持语法高亮显示

#### R-004: 文章分类和标签
- **WHEN** 博主创建文章时, **THEN** 系统 **SHALL** 允许选择一个分类和多个标签
- **WHEN** 访客浏览文章时, **THEN** 系统 **SHALL** 显示文章的分类和标签
- **WHEN** 访客点击分类或标签时, **THEN** 系统 **SHALL** 显示该分类/标签下的所有文章列表

#### R-005: 个人履历展示系统
- **WHEN** 访客访问"关于我"页面时, **THEN** 系统 **SHALL** 展示技能树、项目经历和简历信息
- **WHEN** 博主在后台编辑技能树时, **THEN** 系统 **SHALL** 支持添加/编辑/删除技能项，并设置熟练度
- **WHEN** 博主在后台编辑项目经历时, **THEN** 系统 **SHALL** 支持添加项目名称、描述、技术栈、项目链接
- **WHEN** 访客查看项目经历时, **THEN** 系统 **SHALL** 以卡片形式展示项目信息

#### R-006: 文章点赞功能
- **WHEN** 访客阅读技术板块文章时, **THEN** 系统 **SHALL** 显示点赞按钮和当前点赞数
- **WHEN** 访客点击点赞按钮时, **THEN** 系统 **SHALL** 增加点赞数并记录（基于 IP 或 Cookie 防止重复点赞）
- **WHEN** 访客已点赞后再次点击时, **THEN** 系统 **SHALL** 取消点赞并减少点赞数
- **WHEN** 访客访问生活板块文章时, **THEN** 系统 **SHALL NOT** 显示点赞功能

#### R-007: 邮件联系功能
- **WHEN** 访客点击"联系我"按钮时, **THEN** 系统 **SHALL** 显示联系表单（姓名、邮箱、主题、内容）
- **WHEN** 访客填写并提交表单时, **THEN** 系统 **SHALL** 发送邮件到博主邮箱
- **WHEN** 邮件发送成功时, **THEN** 系统 **SHALL** 显示"发送成功"提示
- **WHEN** 邮件发送失败时, **THEN** 系统 **SHALL** 显示错误提示并允许重试

#### R-008: 文章搜索功能
- **WHEN** 访客在搜索框输入关键词时, **THEN** 系统 **SHALL** 在技术板块文章的标题和内容中搜索
- **WHEN** 搜索结果存在时, **THEN** 系统 **SHALL** 显示匹配的文章列表，高亮关键词
- **WHEN** 搜索结果为空时, **THEN** 系统 **SHALL** 显示"未找到相关文章"提示

#### R-009: 响应式设计
- **WHEN** 访客使用手机访问时, **THEN** 系统 **SHALL** 自动适配移动端布局
- **WHEN** 访客使用平板或电脑访问时, **THEN** 系统 **SHALL** 显示桌面端布局
- **WHEN** 访客调整浏览器窗口大小时, **THEN** 系统 **SHALL** 平滑切换布局

#### R-010: 数据统计展示
- **WHEN** 博主登录后台时, **THEN** 系统 **SHALL** 在仪表盘显示文章总数、总阅读量、总点赞数
- **WHEN** 博主查看单篇文章详情时, **THEN** 系统 **SHALL** 显示该文章的阅读量和点赞数
- **WHEN** 访客阅读文章时, **THEN** 系统 **SHALL** 自动增加该文章的阅读量（基于 IP 去重）

---

## 3. 功能验收清单

| ID | 功能点 | 验收步骤 | 优先级 | 关联需求 | 通过 |
|----|--------|----------|--------|----------|------|
| F-001 | 用户注册登录 | 1. 访问登录页面 2. 输入用户名密码 3. 成功登录并跳转到后台 | P0 | R-002 | ☐ |
| F-002 | 生活板块权限控制 | 1. 未登录访问生活板块文章 2. 跳转到登录页 3. 登录后可正常访问 | P0 | R-002 | ☐ |
| F-003 | 技术板块公开访问 | 1. 未登录访问技术板块文章 2. 可直接阅读内容 | P0 | R-002 | ☐ |
| F-004 | 创建生活板块文章 | 1. 登录后台 2. 选择"生活板块" 3. 创建文章 4. 保存成功 | P0 | R-001, R-003 | ☐ |
| F-005 | 创建技术板块文章 | 1. 登录后台 2. 选择"技术板块" 3. 创建文章 4. 保存成功 | P0 | R-001, R-003 | ☐ |
| F-006 | Markdown 编辑器 | 1. 创建文章 2. 输入 Markdown 语法 3. 实时预览渲染效果 4. 使用工具栏插入格式 | P0 | R-003 | ☐ |
| F-007 | 图片上传 | 1. 在编辑器中点击上传图片 2. 选择本地图片 3. 上传成功并插入链接 | P0 | R-003 | ☐ |
| F-008 | 代码高亮 | 1. 在编辑器中插入代码块 2. 选择编程语言 3. 预览显示语法高亮 | P0 | R-003 | ☐ |
| F-009 | 文章分类 | 1. 创建文章时选择分类 2. 保存后在文章详情显示分类 3. 点击分类查看同类文章 | P0 | R-004 | ☐ |
| F-010 | 文章标签 | 1. 创建文章时添加多个标签 2. 保存后在文章详情显示标签 3. 点击标签查看相关文章 | P0 | R-004 | ☐ |
| F-011 | 技能树展示 | 1. 访问"关于我"页面 2. 查看技能树（前端/后端/数据库等分类） 3. 显示熟练度 | P0 | R-005 | ☐ |
| F-012 | 项目经历展示 | 1. 访问"关于我"页面 2. 查看项目卡片列表 3. 显示项目名称、描述、技术栈、链接 | P0 | R-005 | ☐ |
| F-013 | 技能树管理 | 1. 登录后台 2. 进入技能管理 3. 添加/编辑/删除技能项 4. 设置熟练度 | P0 | R-005 | ☐ |
| F-014 | 项目经历管理 | 1. 登录后台 2. 进入项目管理 3. 添加/编辑/删除项目 4. 填写项目信息 | P0 | R-005 | ☐ |
| F-015 | 文章点赞 | 1. 访问技术板块文章 2. 点击点赞按钮 3. 点赞数+1 4. 再次点击取消点赞 | P1 | R-006 | ☐ |
| F-016 | 点赞防重复 | 1. 点赞后刷新页面 2. 点赞状态保持 3. 无法重复点赞 | P1 | R-006 | ☐ |
| F-017 | 联系表单 | 1. 点击"联系我" 2. 填写表单（姓名、邮箱、主题、内容） 3. 提交成功 | P1 | R-007 | ☐ |
| F-018 | 邮件发送 | 1. 提交联系表单 2. 博主邮箱收到邮件 3. 邮件包含访客信息和内容 | P1 | R-007 | ☐ |
| F-019 | 文章搜索 | 1. 在搜索框输入关键词 2. 显示匹配的技术文章列表 3. 关键词高亮显示 | P1 | R-008 | ☐ |
| F-020 | 移动端适配 | 1. 使用手机访问博客 2. 布局自动适配 3. 功能正常使用 | P1 | R-009 | ☐ |
| F-021 | 数据统计仪表盘 | 1. 登录后台 2. 查看仪表盘 3. 显示文章总数、阅读量、点赞数 | P2 | R-010 | ☐ |
| F-022 | 文章阅读量统计 | 1. 访客阅读文章 2. 阅读量+1 3. 同一 IP 短时间内不重复计数 | P2 | R-010 | ☐ |

---

## 4. 技术约束

### 4.1 技术栈

**前端**：
- 框架：Vue 3 + TypeScript
- UI 组件库：Element Plus 或 Ant Design Vue
- Markdown 编辑器：Vditor 或 ByteMD（所见即所得）
- 代码高亮：Prism.js 或 Highlight.js
- 状态管理：Pinia
- 路由：Vue Router
- HTTP 客户端：Axios

**后端**：
- 框架：Python 3.10+ + FastAPI
- 认证：JWT (JSON Web Token)
- 邮件发送：SMTP (使用 aiosmtplib 或 FastAPI-Mail)
- 图片存储：本地文件系统或对象存储（阿里云 OSS/腾讯云 COS）
- API 文档：FastAPI 自动生成 Swagger UI

**数据库**：
- 主数据库：MongoDB 4.4+
- ORM：Motor (异步 MongoDB 驱动) 或 Beanie (ODM)

**部署**：
- 服务器：云服务器（阿里云/腾讯云）
- 容器化：Docker + Docker Compose
- Web 服务器：Nginx（反向代理 + 静态文件服务）
- 进程管理：Supervisor 或 systemd

### 4.2 数据模型设计

**用户表 (users)**：
```json
{
  "_id": "ObjectId",
  "username": "string",
  "email": "string",
  "password_hash": "string",
  "role": "admin|user",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**文章表 (articles)**：
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string (Markdown)",
  "summary": "string",
  "board": "life|tech",
  "category_id": "ObjectId",
  "tags": ["string"],
  "author_id": "ObjectId",
  "cover_image": "string (URL)",
  "view_count": "int",
  "like_count": "int",
  "is_published": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**分类表 (categories)**：
```json
{
  "_id": "ObjectId",
  "name": "string",
  "board": "life|tech",
  "description": "string",
  "created_at": "datetime"
}
```

**标签表 (tags)**：
```json
{
  "_id": "ObjectId",
  "name": "string",
  "article_count": "int",
  "created_at": "datetime"
}
```

**技能表 (skills)**：
```json
{
  "_id": "ObjectId",
  "name": "string",
  "category": "frontend|backend|database|devops|other",
  "proficiency": "int (0-100)",
  "icon": "string (URL)",
  "order": "int",
  "created_at": "datetime"
}
```

**项目表 (projects)**：
```json
{
  "_id": "ObjectId",
  "name": "string",
  "description": "string",
  "tech_stack": ["string"],
  "project_url": "string",
  "github_url": "string",
  "cover_image": "string (URL)",
  "order": "int",
  "created_at": "datetime"
}
```

**点赞记录表 (likes)**：
```json
{
  "_id": "ObjectId",
  "article_id": "ObjectId",
  "ip_address": "string",
  "user_agent": "string",
  "created_at": "datetime"
}
```

**阅读记录表 (views)**：
```json
{
  "_id": "ObjectId",
  "article_id": "ObjectId",
  "ip_address": "string",
  "created_at": "datetime"
}
```

### 4.3 API 设计规范

- RESTful API 设计风格
- 统一响应格式：
  ```json
  {
    "code": 200,
    "message": "success",
    "data": {}
  }
  ```
- 认证方式：Bearer Token (JWT)
- 错误处理：统一错误码和错误信息

### 4.4 性能要求

- 首页加载时间 < 2秒
- 文章详情页加载时间 < 1秒
- API 响应时间 < 500ms
- 支持并发用户数 > 100

### 4.5 安全要求

- 密码使用 bcrypt 加密存储
- JWT Token 有效期 7 天，支持刷新
- 防止 XSS 攻击：前端对用户输入进行转义
- 防止 CSRF 攻击：使用 CSRF Token
- 防止 SQL 注入：使用 ORM 参数化查询
- 图片上传限制：文件类型、大小限制
- 接口限流：防止恶意请求

---

## 5. 排除项

- **评论系统**：不实现评论功能，使用邮件联系替代
- **社交分享**：暂不支持一键分享到社交媒体
- **RSS 订阅**：暂不支持 RSS 订阅功能
- **多语言支持**：仅支持中文
- **文章版本历史**：不记录文章修改历史
- **草稿箱自动保存**：不实现自动保存草稿功能
- **文章定时发布**：不支持定时发布功能
- **访客注册**：不允许访客注册账号，仅博主和授权用户可登录
- **文章收藏功能**：暂不实现收藏功能
- **站内消息通知**：不实现站内消息系统

---

## 6. 下一步

✅ 需求已澄清，建议在新会话中执行：

```bash
/clouditera:dev:spec-dev personal-blog --skip-requirements
```

该命令将：
1. 读取本需求文档
2. 生成技术设计文档 (design.md)
3. 生成任务分解文档 (tasks.md)
4. 执行 TDD 开发流程
