import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import sys
sys.path.insert(0, "C:/Users/clouditera/project/xlj/backend")
from app.models.project import Project
from datetime import datetime


async def main():
    client = AsyncIOMotorClient("mongodb://182.92.70.220:27017", serverSelectionTimeoutMS=10000)
    db = client.personal_blog
    await init_beanie(database=db, document_models=[Project])

    await Project.find().delete()
    print("Cleared all projects")

    projects = [
        # === 年度总结项目 (2025) ===
        {
            "name": "GFKD 人机协同项目",
            "description": "构建统一的人机协同框架，包含公网/内网漏洞自然语言语义检索系统与 Text2SQL 智能体，实现自然语言到结构化数据查询的全链路能力。覆盖 CVE、NVD、CNNVD 等来源的 30 万+条漏洞知识库。",
            "tech_stack": ["Python", "Text2SQL", "RAG", "LLM", "Docker", "YAML"],
            "status": "completed",
            "highlights": [
                "漏洞检索接口响应时间≤3小时，知识库覆盖 30 万+条数据",
                "Text2SQL 智能体解决问题概率达 85.4%",
                "多版本代码维护机制，系统上线后零重大故障",
                "自然语言→语义解析→结构化数据查询完整链路",
            ],
            "order": 14,
            "start_date": datetime(2025, 5, 1),
            "end_date": datetime(2026, 2, 27),
        },
        {
            "name": "CloudFlow 核心引擎开发",
            "description": "推进 CloudFlow 核心引擎开发与优化，实现多类 LLM 模型的适配集成，参与下一代引擎 CortexFlow 开发。负责核心功能异常排查修复、代码质量管控及项目协作规范搭建。",
            "tech_stack": ["Python", "LLM", "FastAPI", "Docker", "Git"],
            "status": "completed",
            "highlights": [
                "现有核心引擎稳定投入生产",
                "下一代引擎 CortexFlow 迭代推进",
                "多模型适配功能顺利落地",
                "常态化代码质量管控体系建立",
            ],
            "order": 13,
            "start_date": datetime(2025, 5, 1),
            "end_date": datetime(2026, 2, 27),
        },
        {
            "name": "Dify 工作流开发与优化",
            "description": "基于 Dify 低代码 AI 应用编排平台，开发并优化多个安全领域工作流，包括新闻总结、Text2SQL、漏洞信息检索、科大四院演训计划生成等核心工作流。",
            "tech_stack": ["Dify", "Python", "LLM", "RAG", "Prompt Engineering"],
            "status": "completed",
            "highlights": [
                "多个工作流已交付使用",
                "优化后准确率提升 10% 以上",
                "系统可用率达 98% 以上",
                "编写 Dify 工作流教学文档",
            ],
            "order": 12,
            "start_date": datetime(2025, 6, 1),
            "end_date": datetime(2026, 1, 1),
        },
        {
            "name": "漏洞及新闻资讯接口维护",
            "description": "持续维护漏洞及新闻资讯接口，确保插件稳定运行。完成 Docker 及 YAML 一键启动配置，重写 ai-brain 插件文档。",
            "tech_stack": ["Python", "Docker", "YAML", "REST API"],
            "status": "completed",
            "highlights": [
                "Bug 反馈响应时间保持在 3 小时以内",
                "Docker 及 YAML 一键启动配置",
                "多版本代码维护实现兼容和隔离",
            ],
            "order": 11,
            "start_date": datetime(2025, 5, 1),
            "end_date": datetime(2026, 2, 27),
        },
        {
            "name": "Secbenchmark 漏洞挖掘靶场",
            "description": "参与漏洞挖掘靶场测试，开展已知 CVE 复现与 0day 漏洞挖掘工作。针对 MinIO、Nginx、GeoServer 等项目进行安全测试。",
            "tech_stack": ["Python", "Docker", "CVE", "Nginx", "MinIO", "GeoServer"],
            "status": "completed",
            "highlights": [
                "完成已知 CVE 复现 10 个，复现成功率达 50%+",
                "开源项目扫描并分析 8 个",
                "成功复现 GeoServer GetMap 等 CVE 漏洞",
            ],
            "order": 10,
            "start_date": datetime(2025, 9, 1),
            "end_date": datetime(2025, 12, 1),
        },
        # === 简历项目 ===
        {
            "name": "AI 分身",
            "description": "通过 AI 技术模拟博主与用户的互动，提升用户体验。负责线上 0 分 case 的回溯工作，通过分析低分对话识别系统缺陷，为模型优化提供数据支持。编写 prompt 回收数据精确率达 95%。",
            "tech_stack": ["Python", "Prompt Engineering", "LLM", "Reward Model"],
            "status": "completed",
            "highlights": [
                "0 分 case 回溯构建精准标签体系",
                "prompt 编写回收数据精确率达 95%",
                "优化 system prompt 推动对话系统持续优化",
                "提升 AI 分身对话质量与性能表现",
            ],
            "order": 9,
            "start_date": datetime(2024, 10, 1),
        },
        {
            "name": "大模型数据交付平台",
            "description": "负责公司内部多个大模型团队的训练数据交付项目，担任业务流程中的关键节点角色（POC），协调业务方与作业团队之间的沟通与协作，确保模型训练数据的及时性和准确性。",
            "tech_stack": ["Python", "AI", "Prompt Engineering", "数据分析", "项目管理"],
            "status": "completed",
            "highlights": [
                "精准对接业务方需求，筛选并建立供应商合作关系",
                "制定并实施严格的数据质量标准和交付计划",
                "主导制定并实施多项提效方案",
            ],
            "order": 8,
            "start_date": datetime(2024, 8, 1),
            "end_date": datetime(2024, 10, 1),
        },
        {
            "name": "CR 数据标注平台",
            "description": "为 Code Review 项目组打造功能完备的数据标注平台，支持 JSON/CSV 数据导入，构建从数据标注、检查、质检到验收的全流程闭环，引入 OAuth 2.0 鉴权机制保障数据安全。",
            "tech_stack": ["Go", "OAuth 2.0", "JSON", "CSV", "AI"],
            "status": "completed",
            "highlights": [
                "全流程闭环：标注→检查→质检→验收",
                "OAuth 2.0 鉴权保障数据安全",
                "创新运用 AI+ 模式解决跨语言数据处理难题",
                "平台已正式投入数据生产环节",
            ],
            "order": 7,
            "start_date": datetime(2024, 7, 1),
            "end_date": datetime(2024, 8, 1),
        },
        {
            "name": "徽章授予系统",
            "description": "基于业务数据的研发团队徽章授予体系，通过读取日志记录（代码修改行数、Review 行数、提交次数等），结合业务逻辑与算法设计灵活的徽章引擎，量化研发同学工作表现。",
            "tech_stack": ["Python", "Django", "MySQL", "Redis"],
            "status": "completed",
            "highlights": [
                "独立完成徽章引擎核心构建与开发",
                "多维度数据组合条件精准判定徽章类型",
                "数据库结构深度优化，索引优化提升查询效率",
                "项目已在公司内部成功上线",
            ],
            "order": 6,
            "start_date": datetime(2024, 6, 1),
            "end_date": datetime(2024, 7, 1),
        },
        {
            "name": "DS 金融风控数据质量",
            "description": "提升金融风控模型的机器学习能力，通过优化 SFT 训练数据质量提高模型预测准确率。建立自动化检测脚本和人工复核结合的方式，主导离岸团队数据质量控制培训。",
            "tech_stack": ["Python", "SFT", "Machine Learning", "数据分析", "自动化测试"],
            "status": "completed",
            "highlights": [
                "每日抽检正确率稳定在 95% 以上",
                "团队数据产出质量提升 20%",
                "2024 年下半年模型成功上线",
                "模型评估指标显著提升",
            ],
            "order": 5,
            "start_date": datetime(2023, 10, 1),
            "end_date": datetime(2024, 5, 1),
        },
        {
            "name": "智能停车场管理系统",
            "description": "基于 Django 框架的停车管理系统，提供图像识别、支付、预约、评论、查询及导航功能。使用 Celery 实现异步任务调度，Docker 容器化部署，Nginx 负载均衡。",
            "tech_stack": ["Django", "MySQL", "RESTful API", "Celery", "Docker", "Nginx", "Kafka"],
            "status": "completed",
            "highlights": [
                "主导 RESTful API 接口设计，响应时间控制在 200ms 以内",
                "Django ORM 优化数据库查询，实现高并发处理",
                "Docker 容器化部署，系统稳定性达 99.9%",
                "Swagger 接口文档化管理",
            ],
            "order": 4,
            "start_date": datetime(2023, 4, 1),
            "end_date": datetime(2023, 10, 1),
        },
        {
            "name": "图书馆书籍管理系统",
            "description": "基于 Django 框架的图书馆管理项目，集成统计、搜索、借阅、排行和评论系统，显著提升图书馆管理效率和用户体验。CentOS 环境下 Docker 容器化部署。",
            "tech_stack": ["Django", "DRF", "MySQL", "Redis", "Docker", "CentOS"],
            "status": "completed",
            "highlights": [
                "Django ORM 和 DRF 高效处理数据，响应时间 200ms 内",
                "MySQL 索引和分区策略优化数据检索效率",
                "Docker 容器化部署实现负载均衡和高可用",
            ],
            "order": 3,
            "start_date": datetime(2022, 4, 1),
            "end_date": datetime(2023, 2, 1),
        },
        {
            "name": "橙子阅读",
            "description": "基于 Flask 框架的书籍阅读系统，提供分类、搜索、推荐、个性化、离线缓存及作品上传功能。配置 Nginx 反向代理与 Gunicorn 应用服务器。",
            "tech_stack": ["Flask", "MySQL", "Redis", "Elasticsearch", "gRPC", "Nginx", "Celery"],
            "status": "completed",
            "highlights": [
                "第三方接口调用与数据处理",
                "Nginx 反向代理 + Gunicorn 高可用部署",
                "新增 3 个功能模块，系统 bug 率降低 99.9%",
            ],
            "order": 2,
            "start_date": datetime(2021, 5, 1),
            "end_date": datetime(2022, 3, 1),
        },
        {
            "name": "私人助手",
            "description": "基于个性化算法推荐的新闻资讯平台，通过分析用户兴趣和行为数据，设计并实现个性化推荐算法，根据历史搜索、访问记录、浏览时长、点赞率等综合推荐热点新闻。",
            "tech_stack": ["Flask", "MySQL", "Redis", "Celery", "RESTful API"],
            "status": "completed",
            "highlights": [
                "个性化推荐算法设计与实现",
                "多维度用户行为数据分析",
                "数据库结构设计与优化",
            ],
            "order": 1,
            "start_date": datetime(2020, 7, 1),
            "end_date": datetime(2021, 4, 1),
        },
    ]

    for pd in projects:
        p = Project(**pd)
        await p.insert()
        print(f"  [{pd['order']:2d}] {pd['name']}")

    total = await Project.find().count()
    print(f"\nDone! Total: {total} projects, all status=completed")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
