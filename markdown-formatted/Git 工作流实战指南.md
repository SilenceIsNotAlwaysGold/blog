---
title: Git 工作流实战指南
summary: 详解 Git 团队协作工作流，涵盖 Pull Request 流程、代码审查 (Code Review) 标准以及 CI/CD 集成策略。
board: "tech"
category: 版本控制
tags:
  - Git
  - 工作流
  - Code Review
  - DevOps
author: CloudItera
created_at: 2026-01-26T10:05:00Z
updated_at: 2026-01-26T10:05:00Z
is_published: true
---

# Git 工作流实战指南

在掌握了基本的分支策略后，如何在团队中高效地执行这些策略？本文将从实战角度出发，详细介绍基于 Pull Request 的协作流程、代码审查要点以及如何将 Git 集成到自动化工作流中。

## 1. 标准协作流程 (The Collaboration Cycle)

一个标准的基于 GitHub/GitLab 的协作周期通常包含以下步骤：

### 第一步：同步与创建
在开始工作前，确保本地代码是最新的。

```bash
# 切换到主干
git checkout main
# 拉取最新代码
git pull origin main
# 创建新分支
git checkout -b feature/new-awesome-feature
```

### 第二步：开发与提交
在本地进行开发，保持提交粒度适中。

```bash
# 添加修改
git add .
# 提交代码（信息清晰）
git commit -m "feat: implement user registration api"
```

### 第三步：推送与发起 PR
开发完成后，推送到远程仓库。

```bash
git push -u origin feature/new-awesome-feature
```
然后在 GitHub/GitLab 界面上点击 "New Pull Request" (或 Merge Request)。

## 2. 打造高质量的 Pull Request (PR)

PR 不仅仅是合并代码的请求，它是一份关于"做了什么"和"为什么做"的文档。

### PR 模板示例
好的 PR 描述应该包含：

```markdown
## 变更摘要
简要描述这个 PR 实现了什么功能或修复了什么问题。

## 相关 Issue
Closes #123

## 测试计划
- [ ] 单元测试已通过
- [ ] 本地手动测试步骤：
  1. 启动服务
  2. 访问 /api/users
  3. 验证返回数据

## 截图 (可选)
如果是 UI 变更，请附上截图或 GIF。
```

### PR 最佳实践
- **单一职责**：一个 PR 只做一件事。不要在一个 PR 里既修复 Bug 又开发新功能。
- **控制大小**：建议一个 PR 不超过 300-500 行代码变更。过大的 PR 难以审查。
- **自测 (Self-Review)**：在指派 Reviewer 之前，自己先看一遍 Diff。

## 3. 代码审查 (Code Review) 指南

Code Review 是保证代码质量的最重要环节。

### 对于审查者 (Reviewer)
- **友善与尊重**：评论针对代码，而非人。使用"我们可以..."代替"你应该..."。
- **关注重点**：
  - **正确性**：代码逻辑是否正确？有没有明显的 Bug？
  - **可读性**：变量命名是否清晰？代码结构是否易懂？
  - **安全性**：是否有 SQL 注入、XSS 等风险？
  - **性能**：是否有明显的性能瓶颈（如循环查库）？
- **区分建议**：明确区分"必须修改 (Blocking)"和"建议修改 (Nitpick)"。

### 对于被审查者 (Author)
- **保持开放心态**：Review 不是批评，是帮助你提升。
- **及时响应**：尽快回复评论或修改代码。
- **解释原因**：如果不同意建议，礼貌地解释你的设计思路。

## 4. Git 与 CI/CD 集成

将 Git 工作流与持续集成/持续部署 (CI/CD) 结合，实现自动化验证。

### 自动化检查 (Checks)
配置 CI 工具（如 GitHub Actions, Jenkins, GitLab CI）在每次 Push 或 PR 时自动运行：

1. **Lint 检查**：代码格式是否符合规范 (ESLint, Pylint)。
2. **单元测试**：运行自动化测试套件。
3. **构建测试**：确保项目能成功编译/构建。

### 示例：GitHub Actions 配置
`.github/workflows/ci.yml` 简单示例：

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: npm install
    - run: npm run lint
    - run: npm test
```

### 分支保护规则 (Branch Protection Rules)
在仓库设置中开启分支保护：
- 要求 **Status Checks** (CI) 必须通过才能合并。
- 要求至少 **1 名 Reviewer** 批准才能合并。
- 禁止 **Force Push** 到受保护分支。

## 结语

优秀的 Git 工作流不仅仅是一系列命令的组合，更是一种团队协作的文化。通过标准化的 PR 流程、严格的 Code Review 和自动化的 CI/CD 护航，团队可以以更快、更稳的节奏交付高质量软件。
