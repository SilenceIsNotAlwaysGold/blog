---
title: Git Hooks 自动化实战
summary: 学习如何利用 Git Hooks 实现开发流程自动化，包括代码风格检查 (Linting)、提交信息规范校验和自动化测试触发。
board: "tech"
category: 版本控制
tags:
  - Git
  - 自动化
  - Hooks
  - Husky
author: CloudItera
created_at: 2026-01-26T10:20:00Z
updated_at: 2026-01-26T10:20:00Z
is_published: true
---

# Git Hooks 自动化实战

Git Hooks 是 Git 在特定事件（如 commit、push、merge）触发时执行的脚本。利用 Hooks，我们可以把代码质量检查、测试运行等任务前置到开发者本地，从而在源头阻止劣质代码进入仓库。

## 1. Git Hooks 基础

Git Hooks 脚本存放在仓库的 `.git/hooks/` 目录下。默认情况下，里面有很多以 `.sample` 结尾的示例文件。

**常见的客户端 Hooks：**
- `pre-commit`：在键入 Commit Message 前执行。常用于代码格式化、Lint 检查。如果脚本返回非 0 状态，提交将被终止。
- `commit-msg`：在提交信息编辑器关闭后执行。常用于校验 Commit Message 格式。
- `pre-push`：在 Push 之前执行。常用于运行单元测试。

## 2. 原生 Hook 编写示例

让我们写一个简单的 `pre-commit` hook，禁止提交包含 "TODO" 的代码（仅作演示）。

1. 创建文件 `.git/hooks/pre-commit`
2. 添加执行权限：`chmod +x .git/hooks/pre-commit`
3. 写入内容：

```bash
#!/bin/sh
# 检查暂存区的文件是否包含 'TODO'
if git grep -q "TODO" --cached; then
    echo "Error: 代码中包含 TODO，请处理后再提交！"
    exit 1
fi
exit 0
```

现在，如果你尝试提交包含 "TODO" 的代码，Git 会拒绝提交。

## 3. 现代化 Hooks 管理工具：Husky

原生 Hooks 存在一个问题：`.git/hooks` 目录不会被提交到远程仓库，团队成员需要手动复制脚本，难以同步。

在 Node.js/Web 开发中，**Husky** 是管理 Git Hooks 的标准工具。

### 安装 Husky

```bash
npm install husky --save-dev
npx husky install
```

在 `package.json` 中添加脚本以确保其他人 install 时自动启用 husky：
```json
"scripts": {
  "prepare": "husky install"
}
```

### 实战 1：pre-commit 自动 Lint (配合 lint-staged)

我们要实现：提交时，只对**本次修改的文件**运行 ESLint 和 Prettier，修复格式问题后再提交。

1. 安装 lint-staged：
   ```bash
   npm install lint-staged --save-dev
```

2. 配置 `package.json`：
   ```json
   "lint-staged": {
     "*.{js,ts,jsx,tsx}": [
       "eslint --fix",
       "prettier --write"
     ]
   }
```

3. 添加 Husky hook：
   ```bash
   npx husky add .husky/pre-commit "npx lint-staged"
```

现在，每次 `git commit` 时，Husky 会触发 `lint-staged`，自动修复代码格式。如果修复失败，提交会自动中止。

### 实战 2：commit-msg 规范校验 (配合 commitlint)

我们要实现：强制 Commit Message 必须符合 Conventional Commits 规范（如 `feat: add feature`）。

1. 安装 commitlint：
   ```bash
   npm install @commitlint/config-conventional @commitlint/cli --save-dev
```

2. 创建配置文件 `commitlint.config.js`：
   ```javascript
   module.exports = {extends: ['@commitlint/config-conventional']};
```

3. 添加 Husky hook：
   ```bash
   npx husky add .husky/commit-msg "npx --no -- commitlint --edit ${1}"
```

现在，如果提交信息是 "fixed bug"（不符合规范），提交会被拒绝；如果是 "fix: resolve login bug"（符合规范），则通过。

## 4. 服务端 Hooks (Server-side Hooks)

除了本地 Hooks，Git 服务器（如 GitLab, GitHub Enterprise）也支持服务端 Hooks，用于更严格的管控。
*注意：GitHub.com SaaS 版通常不支持自定义服务端 Shell 脚本，而是通过 "Webhooks" 或 "Branch Protection Rules" 实现类似功能。*

- `pre-receive`：处理来自客户端的推送操作时触发。可以用来强制拒绝非快进式推送、检查大文件等。

## 5. 跳过 Hooks

在紧急情况下（如需要立即修复生产环境 Bug，且确定代码没问题），可以通过 `--no-verify` 参数跳过客户端 Hooks：

```bash
git commit -m "hotfix: urgent fix" --no-verify
```
*慎用此选项！*

## 总结

Git Hooks 是构建工程化前端/后端工作流的重要一环。通过 **Husky + Lint-staged + Commitlint** 的组合，我们可以在代码进入仓库之前就建立起第一道质量防线，极大地降低了 Code Review 的负担和 CI 构建失败的概率。
