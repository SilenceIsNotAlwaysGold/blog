---
feature: personal-blog
complexity: complex
generated_by: architect-planner
generated_at: 2026-01-26T02:52:00Z
version: 1
---

# 技术设计文档: 个人博客系统

> **功能标识**: personal-blog
> **复杂度**: complex
> **生成方式**: architect-planner
> **生成时间**: 2026-01-26

## 1. 系统架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 访客浏览器 │  │ 博主浏览器 │  │ 移动端   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   Nginx (反向代理)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 静态文件服务 │ SSL 终止 │ 负载均衡 │ Gzip 压缩    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐          ┌──────────────────┐
│   前端应用        │          │   后端 API       │
│  Vue 3 + TS      │          │  FastAPI         │
│  Element Plus    │          │  Python 3.10+    │
│  Vditor Editor   │          │  JWT Auth        │
│  Pinia Store     │          │  Motor ODM       │
└──────────────────┘          └──────────────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │   MongoDB 4.4+   │
                              │  数据持久化       │
                              └──────────────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │  文件存储         │
                              │  (本地/OSS)      │
                              └──────────────────┘
```

### 1.2 架构特点

- **前后端分离**: Vue 3 SPA + FastAPI RESTful API
- **容器化部署**: Docker + Docker Compose 统一环境
- **反向代理**: Nginx 处理静态文件和 API 转发
- **NoSQL 数据库**: MongoDB 灵活的文档存储
- **JWT 认证**: 无状态认证，支持跨域
- **响应式设计**: 移动端优先，自适应布局

## 2. 技术选型说明

### 2.1 前端技术栈

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| Vue 3 | 3.3+ | 前端框架 | Composition API，性能优秀，生态成熟 |
| TypeScript | 5.0+ | 类型系统 | 类型安全，提升代码质量和可维护性 |
| Element Plus | 2.4+ | UI 组件库 | Vue 3 原生支持，组件丰富，文档完善 |
| Vditor | 3.9+ | Markdown 编辑器 | 所见即所得，支持实时预览和代码高亮 |
| Pinia | 2.1+ | 状态管理 | Vue 3 官方推荐，API 简洁，TypeScript 友好 |
| Vue Router | 4.2+ | 路由管理 | Vue 3 官方路由，支持动态路由和导航守卫 |
| Axios | 1.6+ | HTTP 客户端 | Promise 封装，拦截器支持，易于集成 |
| Prism.js | 1.29+ | 代码高亮 | 轻量级，支持多种语言，主题丰富 |

### 2.2 后端技术栈

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| Python | 3.10+ | 编程语言 | 语法简洁，异步支持，生态丰富 |
| FastAPI | 0.104+ | Web 框架 | 高性能，自动生成 API 文档，异步原生支持 |
| Motor | 3.3+ | MongoDB 驱动 | 异步 MongoDB 驱动，与 FastAPI 完美配合 |
| Beanie | 1.23+ | ODM | 基于 Motor 的 ODM，提供类似 ORM 的体验 |
| PyJWT | 2.8+ | JWT 认证 | 标准 JWT 实现，安全可靠 |
| Passlib | 1.7+ | 密码加密 | 支持 bcrypt，安全的密码哈希 |
| FastAPI-Mail | 1.4+ | 邮件发送 | 异步邮件发送，支持模板 |
| Python-Multipart | 0.0.6+ | 文件上传 | 处理 multipart/form-data |

### 2.3 数据库与存储

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| MongoDB | 4.4+ | 主数据库 | 文档存储，灵活的 Schema，适合博客内容 |
| 本地文件系统 | - | 图片存储 | 初期使用，简单直接，无额外成本 |
| 阿里云 OSS | - | 图片存储（可选） | 后期扩展，CDN 加速，高可用 |

### 2.4 部署与运维

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| Docker | 24.0+ | 容器化 | 统一环境，简化部署 |
| Docker Compose | 2.20+ | 容器编排 | 本地开发和小规模部署 |
| Nginx | 1.24+ | Web 服务器 | 高性能，反向代理，静态文件服务 |
| Supervisor | 4.2+ | 进程管理 | 自动重启，日志管理 |

## 3. 数据库设计

### 3.1 集合（Collection）设计

#### 3.1.1 用户集合 (users)

```json
{
  "_id": "ObjectId",
  "username": "string (唯一索引)",
  "email": "string (唯一索引)",
  "password_hash": "string",
  "role": "admin | user",
  "avatar": "string (URL)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**索引**:
- `username`: 唯一索引
- `email`: 唯一索引

#### 3.1.2 文章集合 (articles)

```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string (Markdown)",
  "summary": "string",
  "board": "life | tech",
  "category_id": "ObjectId",
  "tags": ["string"],
  "author_id": "ObjectId",
  "cover_image": "string (URL)",
  "view_count": "int (default: 0)",
  "like_count": "int (default: 0)",
  "is_published": "boolean (default: false)",
  "published_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**索引**:
- `board`: 普通索引
- `category_id`: 普通索引
- `tags`: 多键索引
- `is_published`: 普通索引
- `created_at`: 降序索引（用于排序）
- 全文索引: `title`, `content`（用于搜索）


#### 3.1.3 分类集合 (categories)

```json
{
  "_id": "ObjectId",
  "name": "string",
  "board": "life | tech",
  "description": "string",
  "article_count": "int (default: 0)",
  "created_at": "datetime"
}
```

**索引**:
- `board`: 普通索引
- `name + board`: 复合唯一索引

#### 3.1.4 标签集合 (tags)

```json
{
  "_id": "ObjectId",
  "name": "string (唯一索引)",
  "article_count": "int (default: 0)",
  "created_at": "datetime"
}
```

**索引**:
- `name`: 唯一索引


#### 3.1.5 技能集合 (skills)

```json
{
  "_id": "ObjectId",
  "name": "string",
  "category": "frontend | backend | database | devops | other",
  "proficiency": "int (0-100)",
  "icon": "string (URL)",
  "order": "int",
  "created_at": "datetime"
}
```

**索引**:
- `category`: 普通索引
- `order`: 升序索引

#### 3.1.6 项目集合 (projects)

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

**索引**:
- `order`: 升序索引


#### 3.1.7 点赞记录集合 (likes)

```json
{
  "_id": "ObjectId",
  "article_id": "ObjectId",
  "ip_address": "string",
  "user_agent": "string",
  "created_at": "datetime"
}
```

**索引**:
- `article_id + ip_address`: 复合唯一索引（防止重复点赞）
- `created_at`: 降序索引（用于清理旧数据）

#### 3.1.8 阅读记录集合 (views)

```json
{
  "_id": "ObjectId",
  "article_id": "ObjectId",
  "ip_address": "string",
  "created_at": "datetime"
}
```

**索引**:
- `article_id`: 普通索引
- `created_at`: 降序索引（用于统计和清理）


### 3.2 数据关系

```
users (1) ─────┐
               │ author_id
               ↓
articles (N) ──┼─── board: "life" | "tech"
               │
               ├─── category_id → categories (1)
               │
               ├─── tags (N) ──────→ tags (N)
               │
               ├─── article_id ← likes (N)
               │
               └─── article_id ← views (N)

skills (N)

projects (N)
```

## 4. API 设计

### 4.1 API 设计原则

- RESTful 风格，资源导向
- 统一响应格式
- JWT Token 认证
- 接口版本控制（/api/v1）
- 错误码标准化

### 4.2 统一响应格式

**成功响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "错误描述",
  "details": "详细错误信息（可选）"
}
```


### 4.3 API 端点列表

#### 4.3.1 认证模块 (/api/v1/auth)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| POST | /auth/login | 用户登录 | 否 |
| POST | /auth/register | 用户注册（仅管理员） | 是 |
| POST | /auth/refresh | 刷新 Token | 是 |
| GET | /auth/me | 获取当前用户信息 | 是 |

#### 4.3.2 文章模块 (/api/v1/articles)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /articles | 获取文章列表（分页、筛选） | 条件 |
| GET | /articles/{id} | 获取文章详情 | 条件 |
| POST | /articles | 创建文章 | 是 |
| PUT | /articles/{id} | 更新文章 | 是 |
| DELETE | /articles/{id} | 删除文章 | 是 |
| POST | /articles/{id}/like | 点赞文章 | 否 |
| DELETE | /articles/{id}/like | 取消点赞 | 否 |
| POST | /articles/search | 搜索文章 | 否 |

**说明**: 生活板块文章需要认证，技术板块文章公开

#### 4.3.3 分类模块 (/api/v1/categories)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /categories | 获取分类列表 | 否 |
| GET | /categories/{id} | 获取分类详情 | 否 |
| POST | /categories | 创建分类 | 是 |
| PUT | /categories/{id} | 更新分类 | 是 |
| DELETE | /categories/{id} | 删除分类 | 是 |


#### 4.3.4 标签模块 (/api/v1/tags)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /tags | 获取标签列表 | 否 |
| GET | /tags/{id} | 获取标签详情 | 否 |
| POST | /tags | 创建标签 | 是 |
| PUT | /tags/{id} | 更新标签 | 是 |
| DELETE | /tags/{id} | 删除标签 | 是 |

#### 4.3.5 技能模块 (/api/v1/skills)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /skills | 获取技能列表 | 否 |
| GET | /skills/{id} | 获取技能详情 | 否 |
| POST | /skills | 创建技能 | 是 |
| PUT | /skills/{id} | 更新技能 | 是 |
| DELETE | /skills/{id} | 删除技能 | 是 |

#### 4.3.6 项目模块 (/api/v1/projects)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /projects | 获取项目列表 | 否 |
| GET | /projects/{id} | 获取项目详情 | 否 |
| POST | /projects | 创建项目 | 是 |
| PUT | /projects/{id} | 更新项目 | 是 |
| DELETE | /projects/{id} | 删除项目 | 是 |

#### 4.3.7 文件上传模块 (/api/v1/upload)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| POST | /upload/image | 上传图片 | 是 |

#### 4.3.8 邮件模块 (/api/v1/contact)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| POST | /contact | 发送联系邮件 | 否 |


#### 4.3.9 统计模块 (/api/v1/stats)

| 方法 | 端点 | 描述 | 认证 |
|------|------|------|------|
| GET | /stats/dashboard | 获取仪表盘统计数据 | 是 |

## 5. 前端架构设计

### 5.1 目录结构

```
frontend/
├── public/                 # 静态资源
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── api/               # API 接口封装
│   │   ├── auth.ts
│   │   ├── article.ts
│   │   ├── category.ts
│   │   ├── tag.ts
│   │   ├── skill.ts
│   │   ├── project.ts
│   │   ├── upload.ts
│   │   └── contact.ts
│   ├── assets/            # 资源文件
│   │   ├── images/
│   │   └── styles/
│   ├── components/        # 公共组件
│   │   ├── common/        # 通用组件
│   │   │   ├── Header.vue
│   │   │   ├── Footer.vue
│   │   │   └── Loading.vue
│   │   ├── article/       # 文章组件
│   │   │   ├── ArticleCard.vue
│   │   │   ├── ArticleList.vue
│   │   │   └── MarkdownEditor.vue
│   │   └── profile/       # 个人信息组件
│   │       ├── SkillTree.vue
│   │       └── ProjectCard.vue
│   ├── layouts/           # 布局组件
│   │   ├── DefaultLayout.vue
│   │   └── AdminLayout.vue
│   ├── pages/             # 页面组件
│   │   ├── home/
│   │   │   └── Index.vue
│   │   ├── life/
│   │   │   ├── List.vue
│   │   │   └── Detail.vue
│   │   ├── tech/
│   │   │   ├── List.vue
│   │   │   └── Detail.vue
│   │   ├── about/
│   │   │   └── Index.vue
│   │   ├── auth/
│   │   │   └── Login.vue
│   │   └── admin/
│   │       ├── Dashboard.vue
│   │       ├── ArticleList.vue
│   │       ├── ArticleEdit.vue
│   │       ├── SkillManage.vue
│   │       └── ProjectManage.vue
│   ├── router/            # 路由配置
│   │   └── index.ts
│   ├── stores/            # Pinia 状态管理
│   │   ├── user.ts
│   │   ├── article.ts
│   │   └── common.ts
│   ├── types/             # TypeScript 类型定义
│   │   ├── api.ts
│   │   ├── article.ts
│   │   ├── user.ts
│   │   └── common.ts
│   ├── utils/             # 工具函数
│   │   ├── request.ts     # Axios 封装
│   │   ├── auth.ts        # 认证工具
│   │   └── format.ts      # 格式化工具
│   ├── App.vue
│   └── main.ts
├── .env.development       # 开发环境配置
├── .env.production        # 生产环境配置
├── package.json
├── tsconfig.json
└── vite.config.ts


### 5.2 路由设计

```typescript
// router/index.ts
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/home/Index.vue')
  },
  {
    path: '/life',
    name: 'LifeBoard',
    component: () => import('@/pages/life/List.vue'),
    meta: { requiresAuth: true }  // 需要认证
  },
  {
    path: '/life/:id',
    name: 'LifeDetail',
    component: () => import('@/pages/life/Detail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/tech',
    name: 'TechBoard',
    component: () => import('@/pages/tech/List.vue')
  },
  {
    path: '/tech/:id',
    name: 'TechDetail',
    component: () => import('@/pages/tech/Detail.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/pages/about/Index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/auth/Login.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/pages/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]
```

### 5.3 状态管理

**用户状态 (stores/user.ts)**:
```typescript
export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',
    userInfo: null,
    isAuthenticated: false
  }),
  actions: {
    async login(username: string, password: string),
    async logout(),
    async fetchUserInfo(),
    async refreshToken()
  }
})
```

**文章状态 (stores/article.ts)**:
```typescript
export const useArticleStore = defineStore('article', {
  state: () => ({
    articles: [],
    currentArticle: null,
    categories: [],
    tags: []
  }),
  actions: {
    async fetchArticles(params: ArticleQuery),
    async fetchArticleDetail(id: string),
    async createArticle(data: ArticleCreate),
    async updateArticle(id: string, data: ArticleUpdate),
    async deleteArticle(id: string)
  }
})
```


## 6. 后端架构设计

### 6.1 目录结构

```
backend/
├── app/
│   ├── api/                # API 路由
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── articles.py
│   │   │   ├── categories.py
│   │   │   ├── tags.py
│   │   │   ├── skills.py
│   │   │   ├── projects.py
│   │   │   ├── upload.py
│   │   │   ├── contact.py
│   │   │   └── stats.py
│   │   └── router.py
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置管理
│   │   ├── security.py     # 安全相关
│   │   └── database.py     # 数据库连接
│   ├── models/             # 数据模型
│   │   ├── user.py
│   │   ├── article.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   ├── skill.py
│   │   ├── project.py
│   │   ├── like.py
│   │   └── view.py
│   ├── schemas/            # Pydantic 模型
│   │   ├── user.py
│   │   ├── article.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   ├── skill.py
│   │   ├── project.py
│   │   └── common.py
│   ├── services/           # 业务逻辑
│   │   ├── auth.py
│   │   ├── article.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   ├── skill.py
│   │   ├── project.py
│   │   ├── upload.py
│   │   └── email.py
│   ├── dependencies/       # 依赖注入
│   │   └── auth.py
│   ├── middleware/         # 中间件
│   │   ├── cors.py
│   │   └── error_handler.py
│   └── utils/              # 工具函数
│       ├── response.py     # 统一响应
│       └── helpers.py
├── uploads/                # 上传文件目录
├── tests/                  # 测试
│   ├── test_auth.py
│   ├── test_articles.py
│   └── ...
├── alembic/                # 数据库迁移（可选）
├── .env                    # 环境变量
├── requirements.txt        # 依赖
└── main.py                 # 应用入口


### 6.2 核心模块设计

#### 6.2.1 认证模块

- JWT Token 生成和验证
- 密码 bcrypt 加密
- Token 刷新机制
- 依赖注入获取当前用户

#### 6.2.2 权限控制

- 基于角色的访问控制（RBAC）
- 路由守卫（depends）
- 资源所有权验证

#### 6.2.3 文章服务

- CRUD 操作
- 分页查询
- 全文搜索
- 点赞和阅读量统计

## 7. 安全设计

### 7.1 认证与授权

- **密码存储**: bcrypt 加密，salt rounds = 12
- **JWT Token**: HS256 算法，有效期 7 天
- **Token 刷新**: Refresh Token 有效期 30 天
- **权限验证**: 基于角色的访问控制

### 7.2 输入验证

- **前端验证**: 表单输入格式验证
- **后端验证**: Pydantic 模型验证
- **XSS 防护**: 前端对用户输入进行转义
- **SQL/NoSQL 注入防护**: 使用 ODM 参数化查询

### 7.3 文件上传安全

- **文件类型限制**: 仅允许图片（jpg, png, gif, webp）
- **文件大小限制**: 最大 5MB
- **文件名处理**: UUID 重命名，防止路径穿越
- **存储路径**: 独立的 uploads 目录，无执行权限

### 7.4 接口安全

- **CORS 配置**: 限制允许的域名
- **Rate Limiting**: 防止 DDoS 和暴力破解
- **HTTPS**: 生产环境强制 HTTPS
- **CSRF 防护**: SameSite Cookie 属性

### 7.5 数据安全

- **敏感数据加密**: 数据库连接字符串、SMTP 密码等
- **日志脱敏**: 不记录密码、Token 等敏感信息
- **定期备份**: MongoDB 定期备份


## 8. 部署架构

### 8.1 Docker Compose 部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:1.24
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
      - ./uploads:/usr/share/nginx/uploads
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - JWT_SECRET=${JWT_SECRET}
      - SMTP_HOST=${SMTP_HOST}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - mongodb

  mongodb:
    image: mongo:4.4
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_USER}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}

volumes:
  mongodb_data:
```

### 8.2 Nginx 配置

```nginx
server {
    listen 80;
    server_name blog.example.com;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传文件
    location /uploads/ {
        alias /usr/share/nginx/uploads/;
        expires 30d;
    }
}
```

### 8.3 部署步骤

1. **环境准备**:
   - 安装 Docker 和 Docker Compose
   - 配置域名解析
   - 申请 SSL 证书（Let's Encrypt）

2. **代码部署**:
   ```bash
   git clone <repository>
   cd personal-blog
   ```

3. **配置环境变量**:
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填写配置
   ```

4. **构建和启动**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

5. **初始化数据**:
   ```bash
   # 创建管理员账号
   docker-compose exec backend python scripts/create_admin.py
   ```

6. **验证部署**:
   - 访问 http://blog.example.com
   - 测试登录、发布文章等功能


## 9. 测试策略

### 9.1 单元测试

**后端测试** (pytest):
- 认证服务测试
- 文章 CRUD 测试
- 权限验证测试
- 文件上传测试

**前端测试** (Vitest):
- 组件单元测试
- 状态管理测试
- 工具函数测试

### 9.2 集成测试

- API 端点测试
- 数据库操作测试
- 第三方服务集成测试（邮件发送）

### 9.3 E2E 测试

- 用户登录流程
- 文章发布流程
- 文章浏览流程
- 点赞和联系功能

### 9.4 测试覆盖率

- 目标覆盖率: 80%+
- 关键功能: 90%+

## 10. 性能优化

### 10.1 前端优化

- **代码分割**: 路由懒加载
- **资源压缩**: Gzip/Brotli 压缩
- **图片优化**: WebP 格式，懒加载
- **CDN**: 静态资源 CDN 加速
- **缓存策略**: 浏览器缓存，Service Worker

### 10.2 后端优化

- **数据库索引**: 关键字段建立索引
- **查询优化**: 分页查询，投影查询
- **缓存机制**: Redis 缓存热点数据（可选）
- **异步处理**: 邮件发送、统计更新异步化

### 10.3 数据库优化

- **索引优化**: 复合索引，覆盖索引
- **连接池**: Motor 连接池配置
- **数据归档**: 定期清理过期数据

## 11. 监控与运维

### 11.1 日志管理

- **应用日志**: FastAPI 日志，分级别记录
- **访问日志**: Nginx 访问日志
- **错误日志**: 错误堆栈跟踪

### 11.2 监控指标

- **应用监控**: API 响应时间，错误率
- **服务器监控**: CPU、内存、磁盘使用率
- **数据库监控**: 连接数，慢查询

### 11.3 备份策略

- **数据库备份**: 每日自动备份，保留 30 天
- **文件备份**: 上传文件定期备份到对象存储
- **代码备份**: Git 版本控制

## 12. 扩展性考虑

### 12.1 短期扩展

- Redis 缓存集成
- 全文搜索引擎（Elasticsearch）
- 图片 CDN（阿里云 OSS/腾讯云 COS）

### 12.2 长期扩展

- 评论系统
- RSS 订阅
- 社交分享
- 多语言支持
- 文章版本历史
- 草稿自动保存

## 13. 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| MongoDB 性能瓶颈 | 高 | 建立合理索引，考虑后续引入 Redis 缓存 |
| 文件存储空间不足 | 中 | 限制上传文件大小，定期清理，考虑对象存储 |
| 第三方邮件服务不稳定 | 低 | 配置备用 SMTP 服务器，增加重试机制 |
| JWT Token 泄露 | 高 | 设置合理的过期时间，HTTPS 传输，不在前端存储敏感信息 |
| XSS 攻击 | 中 | 严格的输入验证和输出转义，CSP 策略 |

---

**设计完成日期**: 2026-01-26
**设计者**: architect-planner Agent
**版本**: 1.0

