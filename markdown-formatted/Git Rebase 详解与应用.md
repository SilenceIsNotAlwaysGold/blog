---
title: Git Rebase 详解与应用
summary: 深入理解 Git Rebase (变基) 的原理，对比 Merge 的区别，掌握交互式 Rebase 清理提交历史的高级技巧。
board: "tech"
category: 版本控制
tags:
  - Git
  - 进阶教程
  - 历史管理
author: CloudItera
created_at: 2026-01-26T10:15:00Z
updated_at: 2026-01-26T10:15:00Z
is_published: true
---

# Git Rebase 详解与应用

在 Git 中，合并代码有两种主要方式：`Merge`（合并）和 `Rebase`（变基）。很多初学者对 Rebase 敬而远之，因为它"修改了历史"。但实际上，Rebase 是保持提交历史整洁线性的神器。本文将带你揭开 Rebase 的神秘面纱。

## 1. Rebase 是什么？

想象你有两个分支：`main` 和 `feature`。
- `main` 前进了几个提交。
- `feature` 从旧的 `main` 分叉出来，也前进了几个提交。

### Merge 的做法
`git merge main` 会创建一个新的"合并提交" (Merge Commit)，将两个分支的历史交织在一起。历史记录变成了非线性的网状结构。

### Rebase 的做法
`git rebase main` 会把 `feature` 分支上的修改，**重新在** 最新的 `main` 提交之上**播放**一遍。
就像把你的分支"剪下来"，然后"嫁接"到 `main` 的最前端。

**结果**：历史记录是一条完美的直线，就像你是在最新的 `main` 代码上刚刚开发完一样。

## 2. 为什么要用 Rebase？

- **整洁的历史**：没有无意义的 "Merge branch 'main' into feature" 提交。
- **易于回溯**：线性的历史让 `git log` 和 `git bisect` 更容易阅读和排查问题。

## 3. Rebase 实战操作

### 场景一：更新本地分支
你在开发 `feature` 分支，此时同事更新了 `main`。为了同步代码并保持线性历史：

```bash
git checkout feature
git rebase main
```
如果在"播放"提交的过程中遇到冲突，Git 会暂停：
1. 解决冲突。
2. `git add <file>`。
3. `git rebase --continue` (注意：不是 commit)。

### 场景二：交互式 Rebase (Interactive Rebase) —— 整理提交历史
这是 Rebase 最强大的功能。假设你在开发过程中提交了 5 次：
- "implement feature"
- "fix typo"
- "fix bug"
- "update logic"
- "final fix"

在合并到主干前，你想把这 5 个乱七八糟的提交合并成一个整洁的提交。

```bash
# 对最近 5 个提交进行交互式变基
git rebase -i HEAD~5
```

Git 会打开编辑器，显示如下列表：

```text
pick 1fc6c95 implement feature
pick 6b2481b fix typo
pick dd1475d fix bug
pick 9a54fd4 update logic
pick c6e4544 final fix
```

你可以修改前面的命令：
- **pick (p)**: 保留该提交。
- **reword (r)**: 保留提交但修改 Commit Message。
- **squash (s)**: 将该提交融合到**上一个**提交中。
- **drop (d)**: 删除该提交。

**操作示例：**
```text
pick 1fc6c95 implement feature
squash 6b2481b fix typo      <-- 融合到第一个
squash dd1475d fix bug       <-- 融合到第一个
squash 9a54fd4 update logic  <-- 融合到第一个
squash c6e4544 final fix     <-- 融合到第一个
```
保存并关闭，Git 会让你编辑最终的 Commit Message。完成后，5 个提交就变成了一个。

## 4. Rebase 的黄金法则

> **永远不要在公共分支（如 main/master）上使用 Rebase！**

Rebase 会修改提交历史（改变 Commit ID）。
如果你 Rebase 了已经推送到远程、并且别人也在基于此开发的分支，你会把别人的历史搞乱，引发灾难。

**只对尚未推送到远程的本地私有分支，或者只有你一个人使用的 Feature 分支进行 Rebase。**

## 5. Rebase vs Merge：如何选择？

- **本地分支整理**：**必须用 Rebase**。在 Push 前整理自己的提交。
- **拉取公共代码**：`git pull --rebase` 优于 `git pull`，可以避免本地产生合并提交。
- **合并回主干**：
  - 团队喜欢线性历史：使用 Rebase 或 Squash Merge。
  - 团队喜欢保留完整历史节点：使用 Merge (即 `--no-ff`)。

## 6. 常用命令总结

```bash
# 将当前分支变基到 target 分支
git rebase target-branch

# 交互式变基最近 N 个提交
git rebase -i HEAD~N

# 解决冲突后继续
git rebase --continue

# 放弃变基
git rebase --abort
```

## 结语

Rebase 是 Git 进阶的必经之路。虽然初次上手可能觉得危险，但一旦掌握了交互式 Rebase 和线性工作流的技巧，你会发现它对维护代码仓库的整洁度有着不可替代的作用。
