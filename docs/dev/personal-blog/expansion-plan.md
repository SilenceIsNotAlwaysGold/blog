# 技术文章扩展计划

## 📋 扩展目标

为文章数量较少的分类扩展内容，使每个分类达到 8-10 篇文章。

## 📊 扩展明细

### 1. 版本控制 (2 → 8篇) +6篇

现有文章：
- git的各种操作.md
- git相关操作.md

新增文章：
1. **Git 分支管理策略与最佳实践** - Git Flow、GitHub Flow、分支命名规范
2. **Git 工作流实战指南** - 团队协作、代码审查、PR 流程
3. **Git 冲突解决完全指南** - 冲突产生原因、解决方法、预防策略
4. **Git Rebase 详解与应用** - Rebase vs Merge、交互式 Rebase、变基最佳实践
5. **Git Hooks 自动化实战** - 客户端 Hooks、服务端 Hooks、实用 Hook 示例
6. **Git 高级技巧与命令** - Cherry-pick、Stash、Reflog、Submodule 等

---

### 2. 数据分析 (3 → 8篇) +5篇

现有文章：
- xlsx 多表去重.md
- 常见的分析趋势方法.md
- 常见的绘制图表类型.md

新增文章：
1. **Pandas 数据处理完全指南** - DataFrame 操作、数据清洗、数据转换
2. **NumPy 数组计算与操作** - 数组创建、索引切片、数学运算、广播机制
3. **Matplotlib 数据可视化实战** - 基础图表、高级定制、子图布局
4. **Python 数据清洗技巧** - 缺失值处理、异常值检测、数据标准化
5. **数据分析实战项目** - 销售数据分析、用户行为分析、数据报表生成

---

### 3. Web服务器 (4 → 8篇) +4篇

现有文章：
- Nginx 详解.md
- Nginx 配置详解.md
- Nginx和Apache.md
- Nginx配置示例.md

新增文章：
1. **Nginx 性能优化完全指南** - 性能调优参数、缓存策略、连接优化
2. **Nginx HTTPS 与 SSL/TLS 配置** - 证书申请、SSL 配置、安全加固
3. **Nginx 负载均衡与高可用** - 负载均衡算法、健康检查、故障转移
4. **Nginx 反向代理与缓存策略** - 代理配置、缓存机制、CDN 集成

---

### 4. Linux系统 (5 → 8篇) +3篇

现有文章：
- CentOS 网络配置指南.md
- CentOS上进行解压.md
- Linux操作系统.md
- 在Linux上打包虚拟环境的依赖项_.md
- 进阶Linux.md

新增文章：
1. **Linux 常用命令大全与实战** - 文件操作、进程管理、网络命令、系统监控
2. **Shell 脚本编程从入门到精通** - 变量、控制流、函数、实战脚本
3. **Linux 系统性能监控与调优** - top、htop、iotop、性能瓶颈分析

---

### 5. 编程语言-Golang (5 → 8篇) +3篇

现有文章：
- Golang基础知识.md
- Golang增删改查（CRUD）操作.md
- Golang的数据库连接.md
- Golang网络编程、数据库编程和Web框架.md
- Golang高级主题.md

新增文章：
1. **Go 并发编程详解** - Goroutine、Channel、Select、并发模式
2. **Go 错误处理与最佳实践** - Error 接口、错误包装、Panic 与 Recover
3. **Go 测试与性能优化** - 单元测试、基准测试、性能分析工具

---

### 6. 容器与编排 (6 → 8篇) +2篇

现有文章：
- Docker 命令详解与常见操作.md
- Docker 学习指南.md
- Docker 进阶.md
- Kafka 集群部署指南.md
- docker安装、验证kafka操作.md
- 快速安装Docker-Compose.md

新增文章：
1. **Docker Compose 实战教程** - 多容器编排、网络配置、数据卷管理
2. **Kubernetes 入门指南** - K8s 架构、Pod、Service、Deployment、实战部署

---

## 📈 扩展统计

| 分类 | 现有 | 目标 | 新增 |
|------|------|------|------|
| 版本控制 | 2 | 8 | +6 |
| 数据分析 | 3 | 8 | +5 |
| Web服务器 | 4 | 8 | +4 |
| Linux系统 | 5 | 8 | +3 |
| 编程语言-Golang | 5 | 8 | +3 |
| 容器与编排 | 6 | 8 | +2 |
| **总计** | **25** | **48** | **+23** |

## ✅ 文章规格要求

每篇新文章都将包含：

1. **完整的 YAML Frontmatter**
   - title, summary, board, category, tags
   - author, created_at, updated_at, is_published

2. **结构化内容**
   - 清晰的章节划分
   - 目录导航（长文档）
   - 代码示例（带语法高亮）

3. **实用性**
   - 实际应用场景
   - 最佳实践建议
   - 常见问题解答

4. **格式标准**
   - Markdown 标准格式
   - 无 HTML 标签
   - 统一的时间戳

## 🚀 执行计划

1. 使用 documentation-architect agent 批量生成文章
2. 按分类顺序生成（从文章数最少的开始）
3. 保存到 `/home/clouditera/xlj/markdown-formatted/` 目录
4. 生成完成后提供统计报告

## ⏱️ 预计时间

- 每篇文章生成时间：约 2-3 分钟
- 总计 23 篇文章：约 50-70 分钟
