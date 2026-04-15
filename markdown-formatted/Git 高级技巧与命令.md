---
title: Git 高级技巧与命令
summary: 盘点那些"救命"的 Git 高级命令，包括 Cherry-pick、Stash、Reflog、Submodule 以及二分查找定位 Bug 的技巧。
board: "tech"
category: 版本控制
tags:
  - Git
  - 进阶教程
  - 命令行
author: CloudItera
created_at: 2026-01-26T10:25:00Z
updated_at: 2026-01-26T10:25:00Z
is_published: true
---

# Git 高级技巧与命令

除了日常的 `add`, `commit`, `push`, `pull`，Git 还隐藏着许多强大的命令。掌握它们，不仅能让你在遇到突发状况时化险为夷，还能显著提升工作效率。

## 1. git cherry-pick：精准提取提交

**场景**：你在 `feature` 分支修复了一个 Bug（提交 ID `a1b2c3d`），发现这个 Bug 在 `release` 分支也存在。你不想合并整个 `feature` 分支，只想把那个修复 Bug 的特定提交"复制"过去。

**操作**：
```bash
git checkout release
git cherry-pick a1b2c3d
```

Git 会将该提交的变更应用到当前分支，并生成一个新的提交 ID。
*注意：如果产生冲突，解决方式与 merge 相同。*

## 2. git stash：暂存工作现场

**场景**：你正在开发新功能，改了一半，突然接到紧急线上 Bug 修复任务。你不想提交半成品的代码，也不想丢失进度。

**操作**：
```bash
# 保存当前工作区和暂存区的修改
git stash save "正在开发登录功能"

# 工作区现在变干净了，可以切换分支去修 Bug 了
git checkout hotfix/login-error
# ...修复并提交...

# 回到原来的分支
git checkout feature-login
# 恢复工作现场
git stash pop
```

**常用命令**：
- `git stash list`：查看所有暂存记录。
- `git stash apply`：恢复但不删除记录。
- `git stash drop`：删除最近一条记录。

## 3. git reflog：后悔药

**场景**：你执行了 `git reset --hard`，误删了最新的提交；或者删除了一个还没合并的分支。你以为代码丢了，开始慌了。别怕，Git 记录了你所有的操作。

**操作**：
```bash
git reflog
```

输出示例：
```text
a1b2c3d HEAD@{0}: reset: moving to HEAD~1
e4f5g6h HEAD@{1}: commit: add new feature
...
```

你会发现，那个被"删除"的提交 `e4f5g6h` 其实还在。

**恢复方法**：
```bash
git reset --hard e4f5g6h
```
这就复活了！`reflog` 默认保留 30-90 天的记录，是真正的救命稻草。

## 4. git bisect：二分查找 Bug

**场景**：代码库里出现了一个 Bug，你不知道是什么时候引入的。最近有 100 个提交，一个个检查太慢了。

**操作**：
```bash
# 开始二分查找模式
git bisect start

# 标记当前版本是"坏的" (Bad)
git bisect bad

# 标记之前的某个版本（比如 v1.0）是"好的" (Good)
git bisect good v1.0
```

Git 会自动检出中间的一个提交。你需要测试这个版本：
- 如果 Bug 存在：输入 `git bisect bad`。
- 如果 Bug 不存在：输入 `git bisect good`。

Git 会不断缩小范围，直到告诉你：
`a1b2c3d is the first bad commit`。
找到罪魁祸首后，使用 `git bisect reset` 退出模式。

## 5. git submodule：管理子模块

**场景**：你的项目依赖另一个 Git 仓库（例如一个通用的工具库），你想在项目中直接引用它，而不是复制代码。

**操作**：
```bash
# 添加子模块
git submodule add https://github.com/example/lib-utils.git libs/utils

# 初始化并更新子模块（当克隆一个带子模块的仓库时）
git submodule update --init --recursive
```

*注意：子模块管理比较复杂，现代开发中常被包管理工具（npm, pip, maven）替代，但在某些特定场景仍很有用。*

## 6. 其他实用短命令

- **修改最后一次提交信息**：
  ```bash
  git commit --amend -m "新的提交信息"
```

- **查看某个文件的每一行是谁写的 (甩锅神器)**：
  ```bash
  git blame src/app.js
```

- **查看漂亮的提交日志图**：
  ```bash
  git log --graph --oneline --all --decorate
```
  *建议配置别名：`git config --global alias.lg "log --graph --oneline --all --decorate"`，以后只需输入 `git lg`。*

## 结语

Git 的强大之处在于它提供了极其丰富的工具箱。从 `stash` 的临时暂存，到 `reflog` 的绝地求生，再到 `bisect` 的科学排错，掌握这些高级技巧，你将从 Git 的"使用者"进阶为"掌控者"。
