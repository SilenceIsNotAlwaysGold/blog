"""Insert 4 GitHub portfolio projects (bill_CV, Vigil, Phantom, bid-assistant).

Run via: docker exec personal-blog-backend python /app/scripts/insert_github_projects.py
Connects to mongodb via env MONGODB_URL (falls back to in-network hostname).
"""
import asyncio
import os
import sys
sys.path.insert(0, "/app")

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.project import Project


MONGO_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://admin:password@localhost:27017/?authSource=admin",
)
DB_NAME = os.getenv("MONGODB_DB_NAME", "personal_blog")


PROJECTS = [
    {
        "name": "bill_CV — AI 记账小助手",
        "description": (
            "一个基于计算机视觉与 LLM 的智能记账工具。用户拍照上传小票/账单图片，"
            "系统自动完成文本识别、商品类目归类、金额提取，并将结果写入本地账本数据库。"
            "支持按月/按类目可视化统计，帮助个人建立轻量但持续的消费复盘习惯。\n\n"
            "## 核心能力\n"
            "- **OCR 识别管线**：集成多引擎（PaddleOCR / Tesseract）对小票进行文字识别与版面分析\n"
            "- **LLM 语义归类**：将识别结果交给大模型做 structured output，输出「品类 + 金额 + 商家」三元组\n"
            "- **本地账本**：SQLite + Python 客户端，零服务器依赖\n"
            "- **统计可视化**：matplotlib / Plotly 按周、月、品类出图\n\n"
            "## 技术亮点\n"
            "- 提示词工程：用 few-shot + JSON Schema 约束输出，错误率相比纯文本解析下降 40%+\n"
            "- 错误兜底：OCR 置信度低时主动让 LLM 再过一遍，显著提升小票方向/模糊图的成功率\n"
            "- 工程化：单文件 CLI 可用，也可作为 pip 库引入"
        ),
        "tech_stack": ["Python", "LLM", "OCR", "PaddleOCR", "SQLite", "Prompt Engineering"],
        "status": "completed",
        "highlights": [
            "端到端拍照→结构化账本一条龙",
            "多 OCR 引擎 + LLM 二次校验，识别鲁棒性高",
            "本地优先架构，无需云端服务即可使用",
            "开源 MIT License，可作为个人工具直接部署",
        ],
        "github_url": "https://github.com/SilenceIsNotAlwaysGold/bill_CV",
        "order": 20,
        "start_date": datetime(2024, 11, 1),
        "end_date": datetime(2025, 1, 1),
    },
    {
        "name": "Vigil — 漏洞情报聚合监测平台",
        "description": (
            "面向安全研究人员与红蓝对抗团队的漏洞情报实时聚合与预警系统。"
            "从多数据源（CVE、NVD、CNNVD、GitHub Security Advisory、微信公众号、安全社区）"
            "统一采集、去重、打分、订阅推送。\n\n"
            "## 模块拆分\n"
            "- **Collector**：按数据源实现 Adapter，统一落到规范化的 `AdvisoryRecord` 模型\n"
            "- **Ranker**：基于 CVSS + 影响面 + 时效性的综合评分\n"
            "- **Subscriber**：关键词 / 厂商 / CVE 类型订阅，命中即刻通过 IM / 邮件推送\n"
            "- **Dashboard**：Web 面板展示趋势、TOP 漏洞、订阅命中记录\n\n"
            "## 技术亮点\n"
            "- 采集层用 asyncio + aiohttp 并发抓取，一次扫描覆盖 30w+ 条漏洞记录\n"
            "- 写入采用幂等 upsert，重跑安全\n"
            "- FastAPI 提供 REST API，前端 Vue 3 SPA 消费"
        ),
        "tech_stack": ["Python", "FastAPI", "asyncio", "MongoDB", "Vue3", "RAG", "CVE/NVD"],
        "status": "completed",
        "highlights": [
            "30w+ 条漏洞记录一次增量扫描 ≤ 3 小时",
            "多数据源 Adapter 架构，新增情报源零成本",
            "订阅命中后秒级 IM/邮件推送",
            "配套 Web Dashboard 可视化趋势与订阅命中",
        ],
        "github_url": "https://github.com/SilenceIsNotAlwaysGold/Vigil",
        "order": 19,
        "start_date": datetime(2025, 3, 1),
        "end_date": datetime(2025, 9, 1),
    },
    {
        "name": "Phantom — 多平台自动化与内容抓取框架",
        "description": (
            "一个以「可插拔 Site Adapter」为核心的跨平台自动化与数据抓取框架。"
            "针对淘宝、抖音、B 站等主流平台抽象统一的登录态管理、反爬绕行、内容采集接口，"
            "方便做数据分析、行情跟踪、内容归档等二次开发。\n\n"
            "## 架构\n"
            "- **Core**：浏览器上下文管理、登录态持久化、节流队列、错误重试\n"
            "- **Site Adapters**：Taobao / Douyin / Bilibili / XHS 等平台特定策略\n"
            "- **CLI**：`phantom` 子命令暴露所有能力，脚本友好\n"
            "- **Export**：结果可导出为 JSONL / Parquet / SQLite\n\n"
            "## 技术亮点\n"
            "- 基于 Playwright，默认全浏览器指纹伪装，突破常规反爬\n"
            "- Adapter 全部 typed，新增平台只需实现一个协议类\n"
            "- 提供 hook 机制，用户可在生命周期每一环注入自定义逻辑"
        ),
        "tech_stack": ["Python", "Playwright", "asyncio", "CLI", "Scraping", "Type Hints"],
        "status": "completed",
        "highlights": [
            "统一 Core + 可插拔 Site Adapter 架构",
            "Playwright 全指纹伪装，反爬稳定性强",
            "CLI 友好，支持 JSONL / Parquet 多格式导出",
            "Hook 机制便于二次定制，无需改框架源码",
        ],
        "github_url": "https://github.com/SilenceIsNotAlwaysGold/Phantom",
        "order": 18,
        "start_date": datetime(2024, 12, 1),
        "end_date": datetime(2025, 6, 1),
    },
    {
        "name": "bid-assistant — 智能投标辅助系统",
        "description": (
            "面向 ToB 销售与投标运营场景的 AI 辅助工具。围绕「招标文件解析 → 相似历史项目召回 → "
            "投标文件草稿生成 → 人工复核」这条主线，大幅降低人工整理招标响应的时间。\n\n"
            "## 核心流程\n"
            "1. **解析**：上传招标 PDF/DOC，自动抽取关键字段（标的、金额、资格要求、评分项）\n"
            "2. **召回**：用向量检索从过往历史项目库中找出相似度 Top-K 的投标范本\n"
            "3. **生成**：基于召回范本 + 本次招标信息，大模型生成分章节的投标响应草稿\n"
            "4. **复核**：高亮可能不达标的条目，提示人工确认\n\n"
            "## 技术亮点\n"
            "- RAG 管线使用 BGE-large 中文向量 + Milvus 检索\n"
            "- Prompt 模板化，每章节独立 prompt，便于按客户定制\n"
            "- 历史项目知识库在线可维护，上传即增量入库"
        ),
        "tech_stack": ["Python", "LLM", "RAG", "Milvus", "BGE", "FastAPI", "PDF"],
        "status": "completed",
        "highlights": [
            "招标解析 → 相似召回 → 草稿生成 → 复核 全流程自动化",
            "BGE-large + Milvus 中文向量检索，Top-K 召回准确率高",
            "按章节模板化 Prompt，便于客户侧定制",
            "历史项目在线增量入库，越用越准",
        ],
        "github_url": "https://github.com/SilenceIsNotAlwaysGold/bid-assistant",
        "order": 17,
        "start_date": datetime(2025, 1, 1),
        "end_date": datetime(2025, 7, 1),
    },
]


async def main():
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=10000)
    await init_beanie(database=client[DB_NAME], document_models=[Project])

    inserted = 0
    for pd in PROJECTS:
        existing = await Project.find_one(Project.name == pd["name"])
        if existing:
            print(f"  skip (exists): {pd['name']}")
            continue
        p = Project(**pd)
        await p.insert()
        inserted += 1
        print(f"  [+{pd['order']:2d}] {pd['name']}")

    total = await Project.find().count()
    print(f"\nInserted {inserted} new GitHub projects. Total projects: {total}")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
