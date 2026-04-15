---
title: Git 冲突解决完全指南
summary: 全面解析 Git 冲突产生的原因、预防策略以及手动解决冲突的详细步骤，包含实用工具推荐。
board: "tech"
category: 版本控制
tags:
  - Git
  - 故障排除
  - 团队协作
author: CloudItera
created_at: 2026-01-26T10:10:00Z
updated_at: 2026-01-26T10:10:00Z
is_published: true
---

# Git 冲突解决完全指南

"合并冲突" (Merge Conflict) 可能是每个开发者最不想看到的提示。但只要理解了它的原理，冲突并不可怕。本文将带你从原理到实战，彻底掌握 Git 冲突的解决之道。

## 1. 为什么会产生冲突？

Git 非常聪明，它通常能自动合并不同开发者的修改。但在以下情况，Git 无法确定该保留哪个版本，从而产生冲突：

1. **同一文件的同一行被修改**：开发者 A 修改了第 10 行，开发者 B 也修改了第 10 行。
2. **文件被删除与修改**：开发者 A 删除了文件 `config.js`，开发者 B 修改了 `config.js`。

## 2. 识别冲突

当你执行 `git merge`、`git pull` 或 `git rebase` 时，如果发生冲突，Git 会暂停操作并提示：

```bash
Auto-merging src/app.js
CONFLICT (content): Merge conflict in src/app.js
Automatic merge failed; fix conflicts and then commit the result.
```

此时，运行 `git status` 会看到：

```bash
Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   src/app.js
```

打开冲突文件，你会看到 Git 插入的冲突标记：

```javascript
<<<<<<< HEAD
const apiUrl = 'https://api.production.com';
=======
const apiUrl = 'https://api.development.com';
>>>>>>> feature/new-api
```

- `<<<<<<< HEAD`：当前分支（目标分支）的内容。
- `=======`：分隔线。
- `>>>>>>> feature/new-api`：要合并进来的分支的内容。

## 3. 手动解决冲突步骤

### 第一步：决定保留哪个版本
你需要分析代码逻辑，决定是：
- 保留 HEAD 的版本？
- 保留 incoming 分支的版本？
- 还是结合两者的修改？

### 第二步：编辑文件
删除 Git 的标记符号（`<<<<<<<`, `=======`, `>>>>>>>`），只保留你想要的代码。

**修改后：**
```javascript
// 假设我们需要根据环境动态配置
const apiUrl = process.env.NODE_ENV === 'prod'
  ? 'https://api.production.com'
  : 'https://api.development.com';
```

### 第三步：标记解决并提交
```bash
# 添加解决后的文件
git add src/app.js

# 完成合并提交
git commit -m "fix: resolve merge conflict in app.js"
```
*注意：如果是 rebase 过程中产生的冲突，解决后使用 `git rebase --continue` 而不是 commit。*

## 4. 实用工具与命令

### 使用命令行参数
有时候你很确定只需要其中一方的版本：

- **保留当前分支版本 (Ours)**：
  ```bash
  git checkout --ours src/app.js
```
- **保留传入分支版本 (Theirs)**：
  ```bash
  git checkout --theirs src/app.js
```

### 图形化工具 (GUI)
相比直接看乱码一样的标记，使用 GUI 工具效率更高：

- **VS Code**：内置了非常强大的冲突解决界面，提供 "Accept Current Change", "Accept Incoming Change", "Accept Both Changes" 等快捷操作。
- **Beyond Compare / KDiff3**：专业的文件对比工具。可以通过 `git mergetool` 配置。

## 5. 如何预防冲突？

最好的解决冲突方法是避免冲突。

1. **频繁同步 (Pull Often)**：每天多次拉取主干代码，保持本地分支最新。
2. **细粒度提交 (Small Commits)**：提交越小，冲突范围越小，解决越容易。
3. **避免修改公共大文件**：如 `package-lock.json` 或自动生成的代码，尽量通过工具统一生成，不要手动修改。
4. **良好的模块化**：代码耦合度越低，不同开发者修改同一文件的概率越小。

## 6. 放弃合并

如果冲突解决过程中搞乱了，想重头再来：

```bash
# 对于 merge
git merge --abort

# 对于 rebase
git rebase --abort
```
这将把工作区回退到合并开始前的状态。

## 结语

冲突是协作开发中的正常现象，不要畏惧它。通过理解 Git 的合并机制，利用好 IDE 工具，并养成良好的同步习惯，解决冲突将变得像写代码一样自然。
