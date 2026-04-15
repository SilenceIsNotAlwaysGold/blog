---
title: "git的各种操作"
summary: "对于仓库的操作 git clone: 克隆远程仓库到本地 git remote: 管理远程仓库 git remote -v: 显示远程仓库的详细信息 git remote add : 添加远程仓库 git remote rm : 移除远程仓库 git fetch: 获取远程仓库的最新变动，但不合并到当前分支 git pull: 获取远程仓库的最新变动，"
board: "tech"
category: "版本控制"
tags:
  - "Git"
  - "版本控制"
  - "协作开发"
author: "博主"
created_at: "2026-01-26T10:00:00Z"
updated_at: "2026-01-26T10:00:00Z"
is_published: true
---

## 对于仓库的操作
git clone: 克隆远程仓库到本地  
git remote: 管理远程仓库  
git remote -v: 显示远程仓库的详细信息  
git remote add  : 添加远程仓库  
git remote rm : 移除远程仓库  
git fetch: 获取远程仓库的最新变动，但不合并到当前分支  
git pull: 获取远程仓库的最新变动，并合并到当前分支


## 对于文件的操作
  
git status ：查看文件状态  
git add . ：# 添加项目中所有文件  
git add xxx.py：# 添加指定文件

git reset HEAD  文件名  ：# 将暂存区代码撤销到工作区  
git checkout 文件名  ：撤销工作区代码  
git rm 文件名 : 删除文件  
添加文件git add


## 对于版本的操作


git commit -m '版本描述'

查看历史版本：git log，git reflog  
回退版本：git reset --hard HEAD^ （几个^便是前几个版本） | git reset --hard 版本号


删除后记录删除操作版本：git commit -m '删除描述'  
误删处理：撤销修改即可:git checkout -- 文件名


## 对于分支的操作
  
git push: 将本地分支的提交推送到远程仓库  
git push  : 推送指定分支到远程仓库  
git branch -r: 列出远程分支

git checkout: 切换分支

git checkout -b  /: 基于远程分支创建新的本地分支  
git merge: 合并远程分支到当前分支  
git rebase: 将当前分支的提交移动到基于另一分支的最新提交上

查看当前分支：git branch

创建并切换到dev分支： git checkout -b dev

设置本地分支跟踪远程指定分支（将分支推送到远程）： git push -u origin dev

dev分支合并到master分支  
git checkout master  
git merge dev


## 对比
对比版本库与工作区：git diff HEAD -- xxx.py  
对比版本库 ：git diff HEAD HEAD^ -- xxx.py  


## 克隆远程仓库的命令
使用HTTPS：cd Desktop/manager/git clone [https://github.com/zhangxiaochuZXC/test007.git](https://github.com/zhangxiaochuZXC/test007.git)

使用SSH：cd Desktop/manager/git clone [git@github.com](mailto:git@github.com):Fly744055970/test002.git


## 配置信息：
  
cd 文件路径  
git config user.name '用户名'  
git config user.email '用户邮箱'


## 推送项目到远程仓库：
工作区添加到暂存区：git add .

暂存区提交到仓库区：git commit -m '立项'

推送到远程仓库：git push


## 账号与密码的保持
在 push 的时候需要设置账号与密码，该密码则是 github 的账号与密码：  
设置记住密码（默认15分钟）：  
git config --global credential.helper cache  
如果想自己设置时间，可以这样做(1小时后失效)：  
git config credential.helper 'cache --timeout=3600'  
长期存储密码：  
git config --global credential.helper store


## 多人协同：
  
要使用git命令操作仓库，需要进入到仓库内部  
要同步服务器代码就执行：git pull  
本地仓库记录版本就执行：git commit -am '版本描述'  
推送代码到服务器就执行：git push  
编辑代码前要先pull，编辑完再commit，最后推送是push


## 标签：


在本地打标签： git tag -a 标签名 -m '标签描述'  
推送标签：git push origin 标签名

删除本地标签：git tag -d 标签名

删除远程仓库标签：git push origin --delete tag 标签名
