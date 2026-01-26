---
feature: personal-blog
complexity: complex
generated_by: architect-planner
generated_at: 2026-01-26T02:52:00Z
version: 1
---

# 任务拆分文档: 个人博客系统

> **功能标识**: personal-blog
> **复杂度**: complex
> **生成方式**: architect-planner
> **生成时间**: 2026-01-26

## 1. 任务拆分原则

- 任务粒度: 2-4 小时完成
- 遵循 TDD 开发流程（Red-Green-Refactor）
- 优先实现 P0 核心功能
- 识别任务依赖关系，支持并行执行
- 每个任务包含明确的验收标准

## 2. 任务依赖图

```
┌──────────────────────────────────────────────────────────┐
│                     并行分组 0                            │
│  T-001 (项目初始化) ─────────────────────┐                │
└──────────────────────────────────────────┼───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 1                            │
│  T-002 (数据库模型)  T-003 (认证模块)                    │
│  T-004 (响应封装)    T-005 (前端初始化)                  │
└──────────────────────────────────────────┬───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 2                            │
│  T-006 (文章 API)    T-007 (分类标签 API)                │
│  T-008 (前端认证)    T-009 (前端路由)                    │
└──────────────────────────────────────────┬───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 3                            │
│  T-010 (Markdown 编辑器)  T-011 (文章列表页面)           │
│  T-012 (文章详情页面)     T-013 (后台管理)               │
└──────────────────────────────────────────┬───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 4                            │
│  T-014 (技能 API)    T-015 (项目 API)                    │
│  T-016 (技能展示)    T-017 (项目展示)                    │
└──────────────────────────────────────────┬───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 5                            │
│  T-018 (点赞功能)    T-019 (邮件联系)                    │
│  T-020 (文件上传)    T-021 (搜索功能)                    │
└──────────────────────────────────────────┬───────────────┘
                                           │
┌──────────────────────────────────────────▼───────────────┐
│                     并行分组 6                            │
│  T-022 (统计功能)    T-023 (响应式设计)                  │
│  T-024 (部署配置)    T-025 (集成测试)                    │
└──────────────────────────────────────────────────────────┘
```

## 3. 任务列表

### 并行分组 0: 基础设施

#### T-001: 项目初始化和环境搭建

- **优先级**: P0
- **预估时间**: 2 小时
- **依赖**: 无
- **执行者**: task-implementer

**描述**:
搭建前后端项目框架，配置开发环境和工具链。

**实施步骤**:
1. 创建项目目录结构
2. 初始化后端项目（FastAPI + Poetry/pip）
3. 初始化前端项目（Vue 3 + Vite + TypeScript）
4. 配置代码格式化工具（Black, Prettier, ESLint）
5. 配置 Git 忽略文件
6. 编写 README.md

**验收标准**:
- [ ] 后端项目可运行（uvicorn main:app）
- [ ] 前端项目可运行（npm run dev）
- [ ] 代码格式化工具配置正确
- [ ] README.md 包含项目说明和启动步骤

**测试要求**:
```python
# tests/test_main.py
def test_app_startup():
    """测试应用可以成功启动"""
    assert app is not None
```

---

### 并行分组 1: 核心基础模块

#### T-002: 数据库模型和连接

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
实现 MongoDB 数据库模型（User, Article, Category, Tag, Skill, Project, Like, View）和数据库连接配置。

**实施步骤**:
1. 配置 Motor 异步驱动
2. 实现 Beanie ODM 模型
3. 创建数据库连接管理
4. 编写索引创建脚本
5. 编写种子数据脚本

**验收标准**:
- [ ] 所有 8 个模型定义完成
- [ ] 数据库连接正常
- [ ] 索引创建成功
- [ ] 种子数据可插入

**测试要求**:
```python
# tests/test_models.py
async def test_user_model_create():
    """测试用户模型创建"""
    user = await User(username="test", email="test@example.com", password_hash="hash").create()
    assert user.id is not None

async def test_article_model_create():
    """测试文章模型创建"""
    article = await Article(title="Test", content="Content", board="tech").create()
    assert article.id is not None
```

---

#### T-003: 认证模块实现

- **优先级**: P0
- **预估时间**: 4 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
实现 JWT 认证系统，包括登录、注册、Token 刷新、密码加密。

**实施步骤**:
1. 实现密码 bcrypt 加密工具
2. 实现 JWT Token 生成和验证
3. 实现登录 API (/api/v1/auth/login)
4. 实现注册 API (/api/v1/auth/register)
5. 实现 Token 刷新 API (/api/v1/auth/refresh)
6. 实现获取当前用户 API (/api/v1/auth/me)
7. 实现依赖注入（get_current_user）

**验收标准**:
- [ ] 登录成功返回 Token
- [ ] Token 验证正确
- [ ] 密码加密存储
- [ ] 依赖注入可获取当前用户

**测试要求**:
```python
# tests/test_auth.py
async def test_login_success():
    """测试登录成功"""
    response = await client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    assert "token" in response.json()["data"]

async def test_login_invalid_credentials():
    """测试登录失败"""
    response = await client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401

async def test_get_current_user():
    """测试获取当前用户"""
    response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "admin"
```

---

#### T-004: 统一响应格式封装

- **优先级**: P0
- **预估时间**: 1 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
实现统一的 API 响应格式和错误处理。

**实施步骤**:
1. 定义响应模型（Pydantic）
2. 实现响应工具函数（success, error）
3. 实现全局异常处理器
4. 实现自定义异常类

**验收标准**:
- [ ] 成功响应格式统一
- [ ] 错误响应格式统一
- [ ] 异常自动捕获并格式化

**测试要求**:
```python
# tests/test_response.py
def test_success_response():
    """测试成功响应格式"""
    response = success(data={"key": "value"}, message="操作成功")
    assert response["code"] == 200
    assert response["message"] == "操作成功"
    assert response["data"] == {"key": "value"}

def test_error_response():
    """测试错误响应格式"""
    response = error(code=400, message="错误信息")
    assert response["code"] == 400
    assert response["message"] == "错误信息"
```

---

#### T-005: 前端项目初始化

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
搭建前端项目框架，配置 Vue 3 + TypeScript + Element Plus + Pinia。

**实施步骤**:
1. 安装依赖（Element Plus, Pinia, Vue Router, Axios）
2. 配置 TypeScript
3. 配置 Vite
4. 封装 Axios 请求工具
5. 创建基础布局组件（Header, Footer）
6. 配置环境变量

**验收标准**:
- [ ] Element Plus 可用
- [ ] Axios 拦截器配置正确
- [ ] TypeScript 类型检查通过
- [ ] 基础布局显示正常

**测试要求**:
```typescript
// tests/utils/request.test.ts
describe('Request Utils', () => {
  test('应该正确添加请求拦截器', () => {
    // 测试请求拦截器
  })

  test('应该正确处理响应', () => {
    // 测试响应拦截器
  })
})
```

---

### 并行分组 2: 核心 API 和前端基础

#### T-006: 文章模块 API 实现

- **优先级**: P0
- **预估时间**: 4 小时
- **依赖**: T-002, T-003, T-004
- **执行者**: task-implementer

**描述**:
实现文章的 CRUD API，包括列表查询、详情查询、创建、更新、删除。

**实施步骤**:
1. 定义文章 Pydantic Schema
2. 实现文章列表查询（分页、筛选）
3. 实现文章详情查询（阅读量+1）
4. 实现文章创建（需认证）
5. 实现文章更新（需认证）
6. 实现文章删除（需认证）
7. 实现权限验证（生活板块需认证）

**验收标准**:
- [ ] 未认证可访问技术板块文章
- [ ] 未认证访问生活板块返回 401
- [ ] 已认证可 CRUD 文章
- [ ] 分页查询正确
- [ ] 阅读量正确增加

**测试要求**:
```python
# tests/test_articles.py
async def test_get_tech_articles_without_auth():
    """测试未认证访问技术板块文章"""
    response = await client.get("/api/v1/articles?board=tech")
    assert response.status_code == 200

async def test_get_life_articles_without_auth():
    """测试未认证访问生活板块文章"""
    response = await client.get("/api/v1/articles?board=life")
    assert response.status_code == 401

async def test_create_article():
    """测试创建文章"""
    response = await client.post("/api/v1/articles",
        json={"title": "Test", "content": "Content", "board": "tech"},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Test"
```

---

#### T-007: 分类和标签 API 实现

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-002, T-003, T-004
- **执行者**: task-implementer

**描述**:
实现分类和标签的 CRUD API。

**实施步骤**:
1. 定义分类和标签 Schema
2. 实现分类 CRUD API
3. 实现标签 CRUD API
4. 实现按分类/标签查询文章

**验收标准**:
- [ ] 分类 CRUD 正常
- [ ] 标签 CRUD 正常
- [ ] 按分类/标签查询文章正常

**测试要求**:
```python
# tests/test_categories.py
async def test_create_category():
    """测试创建分类"""
    response = await client.post("/api/v1/categories",
        json={"name": "技术", "board": "tech"},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

async def test_get_categories():
    """测试获取分类列表"""
    response = await client.get("/api/v1/categories")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
```

---

#### T-008: 前端认证模块实现

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-003, T-005
- **执行者**: task-implementer

**描述**:
实现前端登录页面、用户状态管理、Token 存储和刷新。

**实施步骤**:
1. 创建登录页面组件
2. 实现用户 Pinia Store
3. 实现 Token 存储（localStorage）
4. 实现 Axios 请求拦截器（自动添加 Token）
5. 实现 Token 过期刷新

**验收标准**:
- [ ] 登录成功跳转到后台
- [ ] Token 自动添加到请求头
- [ ] Token 过期自动刷新
- [ ] 退出登录清除 Token

**测试要求**:
```typescript
// tests/stores/user.test.ts
describe('User Store', () => {
  test('登录成功后应该存储 Token', async () => {
    const userStore = useUserStore()
    await userStore.login('admin', 'admin123')
    expect(userStore.token).toBeTruthy()
    expect(userStore.isAuthenticated).toBe(true)
  })

  test('退出登录应该清除 Token', async () => {
    const userStore = useUserStore()
    await userStore.logout()
    expect(userStore.token).toBe('')
    expect(userStore.isAuthenticated).toBe(false)
  })
})
```

---

#### T-009: 前端路由和导航守卫

- **优先级**: P0
- **预估时间**: 2 小时
- **依赖**: T-005, T-008
- **执行者**: task-implementer

**描述**:
配置 Vue Router，实现路由导航守卫，保护需要认证的页面。

**实施步骤**:
1. 配置路由表
2. 实现导航守卫（beforeEach）
3. 实现生活板块权限验证
4. 实现后台管理权限验证

**验收标准**:
- [ ] 未认证访问生活板块跳转登录
- [ ] 未认证访问后台跳转登录
- [ ] 已认证可访问所有页面

**测试要求**:
```typescript
// tests/router/guards.test.ts
describe('Router Guards', () => {
  test('未认证访问生活板块应该跳转登录', () => {
    // 测试导航守卫
  })

  test('已认证可访问生活板块', () => {
    // 测试导航守卫
  })
})
```

---

### 并行分组 3: 核心功能实现

#### T-010: Markdown 编辑器集成

- **优先级**: P0
- **预估时间**: 4 小时
- **依赖**: T-005, T-008, T-009
- **执行者**: task-implementer

**描述**:
集成 Vditor Markdown 编辑器，实现所见即所得编辑、代码高亮、图片上传。

**实施步骤**:
1. 安装 Vditor
2. 创建 MarkdownEditor 组件
3. 配置实时预览
4. 配置代码高亮（Prism.js）
5. 配置工具栏
6. 实现图片上传占位（待 T-020 完成）

**验收标准**:
- [ ] Markdown 语法正确渲染
- [ ] 代码块语法高亮
- [ ] 实时预览正常
- [ ] 工具栏功能可用

**测试要求**:
```typescript
// tests/components/MarkdownEditor.test.ts
describe('MarkdownEditor', () => {
  test('应该正确渲染 Markdown 内容', () => {
    // 测试组件渲染
  })

  test('应该支持实时预览', () => {
    // 测试实时预览
  })
})
```

---

#### T-011: 文章列表页面实现

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-006, T-009
- **执行者**: task-implementer

**描述**:
实现技术板块和生活板块的文章列表页面，支持分页、筛选。

**实施步骤**:
1. 创建文章列表页面组件
2. 实现文章卡片组件
3. 实现分页组件
4. 实现按分类/标签筛选
5. 实现文章 Pinia Store

**验收标准**:
- [ ] 文章列表正确显示
- [ ] 分页功能正常
- [ ] 筛选功能正常
- [ ] 卡片点击跳转详情

**测试要求**:
```typescript
// tests/pages/ArticleList.test.ts
describe('ArticleList', () => {
  test('应该正确显示文章列表', () => {
    // 测试列表渲染
  })

  test('应该正确处理分页', () => {
    // 测试分页
  })
})
```

---

#### T-012: 文章详情页面实现

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-006, T-009
- **执行者**: task-implementer

**描述**:
实现文章详情页面，显示 Markdown 渲染内容、分类标签、阅读量。

**实施步骤**:
1. 创建文章详情页面组件
2. 实现 Markdown 渲染（Vditor 预览模式）
3. 显示文章元信息（分类、标签、发布时间）
4. 显示阅读量和点赞数（占位）

**验收标准**:
- [ ] Markdown 内容正确渲染
- [ ] 代码高亮显示正常
- [ ] 元信息显示正确
- [ ] 阅读量自动增加

**测试要求**:
```typescript
// tests/pages/ArticleDetail.test.ts
describe('ArticleDetail', () => {
  test('应该正确渲染 Markdown 内容', () => {
    // 测试内容渲染
  })

  test('应该显示文章元信息', () => {
    // 测试元信息
  })
})
```

---

#### T-013: 后台管理页面实现

- **优先级**: P0
- **预估时间**: 4 小时
- **依赖**: T-006, T-007, T-010
- **执行者**: task-implementer

**描述**:
实现后台管理功能，包括文章列表、创建文章、编辑文章、删除文章。

**实施步骤**:
1. 创建后台布局组件
2. 创建仪表盘页面（占位）
3. 创建文章列表管理页面
4. 创建文章编辑页面（集成 Markdown 编辑器）
5. 实现删除确认

**验收标准**:
- [ ] 文章列表正确显示
- [ ] 创建文章成功
- [ ] 编辑文章成功
- [ ] 删除文章成功

**测试要求**:
```typescript
// tests/pages/admin/ArticleEdit.test.ts
describe('ArticleEdit', () => {
  test('应该正确保存文章', async () => {
    // 测试保存
  })

  test('应该正确验证表单', () => {
    // 测试表单验证
  })
})
```

---

### 并行分组 4: 个人履历系统

#### T-014: 技能模块 API 实现

- **优先级**: P0
- **预估时间**: 2 小时
- **依赖**: T-002, T-003, T-004
- **执行者**: task-implementer

**描述**:
实现技能的 CRUD API。

**实施步骤**:
1. 定义技能 Schema
2. 实现技能 CRUD API
3. 实现按分类查询

**验收标准**:
- [ ] 技能 CRUD 正常
- [ ] 按分类查询正常
- [ ] 排序功能正常

**测试要求**:
```python
# tests/test_skills.py
async def test_create_skill():
    """测试创建技能"""
    response = await client.post("/api/v1/skills",
        json={"name": "Python", "category": "backend", "proficiency": 90},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

async def test_get_skills_by_category():
    """测试按分类查询技能"""
    response = await client.get("/api/v1/skills?category=backend")
    assert response.status_code == 200
```

---

#### T-015: 项目模块 API 实现

- **优先级**: P0
- **预估时间**: 2 小时
- **依赖**: T-002, T-003, T-004
- **执行者**: task-implementer

**描述**:
实现项目的 CRUD API。

**实施步骤**:
1. 定义项目 Schema
2. 实现项目 CRUD API
3. 实现排序功能

**验收标准**:
- [ ] 项目 CRUD 正常
- [ ] 排序功能正常

**测试要求**:
```python
# tests/test_projects.py
async def test_create_project():
    """测试创建项目"""
    response = await client.post("/api/v1/projects",
        json={"name": "个人博客", "description": "...", "tech_stack": ["Vue 3", "FastAPI"]},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

---

#### T-016: 技能树展示页面

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-014
- **执行者**: task-implementer

**描述**:
实现"关于我"页面的技能树展示部分。

**实施步骤**:
1. 创建技能树组件
2. 按分类分组显示技能
3. 显示熟练度进度条
4. 实现后台技能管理页面

**验收标准**:
- [ ] 技能按分类分组
- [ ] 熟练度进度条正确
- [ ] 后台可管理技能

**测试要求**:
```typescript
// tests/components/SkillTree.test.ts
describe('SkillTree', () => {
  test('应该正确分组显示技能', () => {
    // 测试分组
  })

  test('应该正确显示熟练度', () => {
    // 测试熟练度
  })
})
```

---

#### T-017: 项目经历展示页面

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-015
- **执行者**: task-implementer

**描述**:
实现"关于我"页面的项目经历展示部分。

**实施步骤**:
1. 创建项目卡片组件
2. 显示项目信息（名称、描述、技术栈、链接）
3. 实现后台项目管理页面

**验收标准**:
- [ ] 项目卡片正确显示
- [ ] 链接可跳转
- [ ] 后台可管理项目

**测试要求**:
```typescript
// tests/components/ProjectCard.test.ts
describe('ProjectCard', () => {
  test('应该正确显示项目信息', () => {
    // 测试显示
  })

  test('应该正确处理链接跳转', () => {
    // 测试跳转
  })
})
```

---

### 并行分组 5: 增强功能

#### T-018: 文章点赞功能

- **优先级**: P1
- **预估时间**: 3 小时
- **依赖**: T-006
- **执行者**: task-implementer

**描述**:
实现技术板块文章的点赞和取消点赞功能，防止重复点赞。

**实施步骤**:
1. 实现点赞 API（POST /articles/{id}/like）
2. 实现取消点赞 API（DELETE /articles/{id}/like）
3. 基于 IP 地址防止重复点赞
4. 前端实现点赞按钮组件
5. 更新文章详情页显示点赞数

**验收标准**:
- [ ] 点赞成功增加点赞数
- [ ] 取消点赞减少点赞数
- [ ] 同一 IP 不能重复点赞
- [ ] 点赞状态正确显示

**测试要求**:
```python
# tests/test_likes.py
async def test_like_article():
    """测试点赞文章"""
    response = await client.post(f"/api/v1/articles/{article_id}/like")
    assert response.status_code == 200

async def test_duplicate_like_prevention():
    """测试防止重复点赞"""
    await client.post(f"/api/v1/articles/{article_id}/like")
    response = await client.post(f"/api/v1/articles/{article_id}/like")
    assert response.status_code == 400  # 已点赞
```

---

#### T-019: 邮件联系功能

- **优先级**: P1
- **预估时间**: 3 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
实现访客通过表单发送邮件给博主的功能。

**实施步骤**:
1. 配置 FastAPI-Mail
2. 实现邮件发送 API（POST /contact）
3. 定义邮件模板
4. 前端实现联系表单组件
5. 表单验证（姓名、邮箱、主题、内容）

**验收标准**:
- [ ] 表单提交成功
- [ ] 博主邮箱收到邮件
- [ ] 表单验证正确
- [ ] 发送失败显示错误

**测试要求**:
```python
# tests/test_contact.py
async def test_send_contact_email():
    """测试发送联系邮件"""
    response = await client.post("/api/v1/contact",
        json={"name": "张三", "email": "test@example.com", "subject": "合作", "content": "内容"})
    assert response.status_code == 200
```

---

#### T-020: 图片上传功能

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-010
- **执行者**: task-implementer

**描述**:
实现图片上传功能，支持 Markdown 编辑器图片上传。

**实施步骤**:
1. 实现图片上传 API（POST /upload/image）
2. 文件类型和大小验证
3. 文件名 UUID 重命名
4. 集成到 Markdown 编辑器
5. 配置 Nginx 静态文件服务

**验收标准**:
- [ ] 图片上传成功
- [ ] 返回图片 URL
- [ ] 图片可访问
- [ ] 文件类型验证正确

**测试要求**:
```python
# tests/test_upload.py
async def test_upload_image():
    """测试上传图片"""
    files = {'file': ('test.jpg', open('test.jpg', 'rb'), 'image/jpeg')}
    response = await client.post("/api/v1/upload/image", files=files,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "url" in response.json()["data"]

async def test_upload_invalid_file_type():
    """测试上传无效文件类型"""
    files = {'file': ('test.txt', b'content', 'text/plain')}
    response = await client.post("/api/v1/upload/image", files=files,
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
```

---

#### T-021: 文章搜索功能

- **优先级**: P1
- **预估时间**: 3 小时
- **依赖**: T-006
- **执行者**: task-implementer

**描述**:
实现技术板块文章的全文搜索功能，关键词高亮。

**实施步骤**:
1. 在 Article 模型创建全文索引
2. 实现搜索 API（POST /articles/search）
3. 前端实现搜索框组件
4. 实现搜索结果页面
5. 实现关键词高亮

**验收标准**:
- [ ] 搜索结果正确
- [ ] 关键词高亮显示
- [ ] 仅搜索技术板块
- [ ] 空结果提示正确

**测试要求**:
```python
# tests/test_search.py
async def test_search_articles():
    """测试搜索文章"""
    response = await client.post("/api/v1/articles/search", json={"keyword": "Python"})
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0

async def test_search_no_results():
    """测试搜索无结果"""
    response = await client.post("/api/v1/articles/search", json={"keyword": "不存在的关键词"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 0
```

---

### 并行分组 6: 完善和部署

#### T-022: 统计功能实现

- **优先级**: P2
- **预估时间**: 3 小时
- **依赖**: T-006
- **执行者**: task-implementer

**描述**:
实现后台仪表盘统计数据展示。

**实施步骤**:
1. 实现统计 API（GET /stats/dashboard）
2. 统计文章总数、总阅读量、总点赞数
3. 前端实现仪表盘页面
4. 显示统计图表（可选：使用 ECharts）

**验收标准**:
- [ ] 统计数据正确
- [ ] 仪表盘显示正常
- [ ] 数据实时更新

**测试要求**:
```python
# tests/test_stats.py
async def test_get_dashboard_stats():
    """测试获取仪表盘统计"""
    response = await client.get("/api/v1/stats/dashboard",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "total_articles" in response.json()["data"]
```

---

#### T-023: 响应式设计实现

- **优先级**: P1
- **预估时间**: 4 小时
- **依赖**: T-011, T-012
- **执行者**: task-implementer

**描述**:
实现移动端适配，确保所有页面在手机和平板上正常显示。

**实施步骤**:
1. 配置 Element Plus 响应式断点
2. 优化文章列表移动端布局
3. 优化文章详情移动端布局
4. 优化导航栏移动端布局（汉堡菜单）
5. 优化后台管理移动端布局

**验收标准**:
- [ ] 手机访问布局正常
- [ ] 平板访问布局正常
- [ ] 触摸交互正常
- [ ] 图片自适应

**测试要求**:
```typescript
// tests/responsive.test.ts
describe('Responsive Design', () => {
  test('移动端应该显示汉堡菜单', () => {
    // 测试移动端布局
  })

  test('桌面端应该显示完整导航', () => {
    // 测试桌面端布局
  })
})
```

---

#### T-024: Docker 部署配置

- **优先级**: P0
- **预估时间**: 3 小时
- **依赖**: T-001
- **执行者**: task-implementer

**描述**:
编写 Docker 和 Docker Compose 配置，实现一键部署。

**实施步骤**:
1. 编写后端 Dockerfile
2. 编写前端 Dockerfile
3. 编写 docker-compose.yml
4. 编写 Nginx 配置文件
5. 编写部署文档（README.md）
6. 编写初始化脚本（创建管理员）

**验收标准**:
- [ ] docker-compose up -d 可启动
- [ ] 前后端正常通信
- [ ] Nginx 反向代理正确
- [ ] 数据库持久化正常

**测试要求**:
```bash
# 测试部署
docker-compose build
docker-compose up -d
curl http://localhost  # 应该返回前端页面
curl http://localhost/api/v1/health  # 应该返回健康检查
```

---

#### T-025: 集成测试和文档

- **优先级**: P1
- **预估时间**: 4 小时
- **依赖**: 所有任务
- **执行者**: task-implementer

**描述**:
编写 E2E 测试，完善项目文档。

**实施步骤**:
1. 编写用户登录 E2E 测试
2. 编写文章发布 E2E 测试
3. 编写文章浏览 E2E 测试
4. 完善 README.md
5. 编写 API 文档（FastAPI 自动生成）
6. 编写用户手册

**验收标准**:
- [ ] E2E 测试通过
- [ ] 文档完整清晰
- [ ] API 文档可访问

**测试要求**:
```typescript
// tests/e2e/login.spec.ts
describe('E2E: Login Flow', () => {
  test('用户登录流程', async () => {
    // 访问登录页
    // 输入用户名密码
    // 点击登录
    // 验证跳转到后台
  })
})
```

---

## 4. 任务执行顺序

**第 1 批（顺序执行）**:
1. T-001 (项目初始化)

**第 2 批（并行执行）**:
2. T-002 (数据库模型)
3. T-003 (认证模块)
4. T-004 (响应封装)
5. T-005 (前端初始化)

**第 3 批（并行执行）**:
6. T-006 (文章 API)
7. T-007 (分类标签 API)
8. T-008 (前端认证)
9. T-009 (前端路由)

**第 4 批（并行执行）**:
10. T-010 (Markdown 编辑器)
11. T-011 (文章列表页面)
12. T-012 (文章详情页面)
13. T-013 (后台管理)

**第 5 批（并行执行）**:
14. T-014 (技能 API)
15. T-015 (项目 API)
16. T-016 (技能展示)
17. T-017 (项目展示)

**第 6 批（并行执行）**:
18. T-018 (点赞功能)
19. T-019 (邮件联系)
20. T-020 (图片上传)
21. T-021 (搜索功能)

**第 7 批（并行执行）**:
22. T-022 (统计功能)
23. T-023 (响应式设计)
24. T-024 (部署配置)
25. T-025 (集成测试)

---

## 5. 预估工时

| 批次 | 任务数 | 预估工时 | 并行执行 | 实际工时 |
|------|--------|----------|----------|----------|
| 第 1 批 | 1 | 2h | 否 | 2h |
| 第 2 批 | 4 | 11h | 是 | 4h |
| 第 3 批 | 4 | 13h | 是 | 4h |
| 第 4 批 | 4 | 14h | 是 | 4h |
| 第 5 批 | 4 | 10h | 是 | 3h |
| 第 6 批 | 4 | 12h | 是 | 3h |
| 第 7 批 | 4 | 14h | 是 | 4h |
| **总计** | **25** | **76h** | **部分** | **24h** |

**说明**: 预估总工时 76 小时，通过并行执行可压缩至约 24 小时（3 个工作日）。

---

## 6. 风险和注意事项

| 风险 | 影响 | 缓解措施 | 负责任务 |
|------|------|---------|---------|
| Markdown 编辑器集成复杂 | 中 | 提前调研 Vditor，准备降级方案 | T-010 |
| 邮件发送可能失败 | 低 | 配置备用 SMTP，增加重试 | T-019 |
| 图片上传安全风险 | 中 | 严格验证文件类型和大小 | T-020 |
| MongoDB 全文索引性能 | 低 | 合理设计索引，考虑后续 Elasticsearch | T-021 |
| 响应式设计工作量大 | 中 | 使用 Element Plus 响应式组件 | T-023 |
| Docker 部署环境差异 | 中 | 充分测试，提供详细文档 | T-024 |

---

**任务拆分完成日期**: 2026-01-26
**拆分者**: architect-planner Agent
**版本**: 1.0
