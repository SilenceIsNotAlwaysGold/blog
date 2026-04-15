import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def migrate_categories():
    client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    db = client.personal_blog

    # 1. 定义新的分类映射 (目标分类 -> 源分类列表)
    mapping = {
        "Python 全栈": ["Python 开发", "编程语言-Python", "Web 开发"],
        "Golang 开发": ["编程语言-Golang"],
        "Linux 与运维": ["Linux系统", "Web服务器"],
        "容器与云原生": ["容器与编排"],
        "数据与算法": ["数据分析", "机器学习"],
        "数据库技术": ["数据库"],
        "DevOps 工具": ["版本控制"],
        "其他技术": ["其他"]
    }

    print("开始分类合并与迁移...\n")

    # 2. 创建新分类并迁移文章
    for target_name, source_names in mapping.items():
        print(f"处理目标分类: {target_name}")

        # 获取或创建目标分类
        target_cat = await db.categories.find_one({"name": target_name})
        if not target_cat:
            target_cat = {
                "name": target_name,
                "board": "tech",
                "description": f"{target_name}相关文章",
                "created_at": "2026-01-26T10:00:00Z" # 简化处理
            }
            res = await db.categories.insert_one(target_cat)
            target_cat["_id"] = res.inserted_id
            print(f"  + 创建新分类: {target_name}")
        else:
            print(f"  * 目标分类已存在: {target_name}")

        target_id = target_cat["_id"]
        count = 0

        # 遍历源分类
        for source_name in source_names:
            if source_name == target_name:
                continue

            source_cat = await db.categories.find_one({"name": source_name})
            if source_cat:
                # 迁移文章
                result = await db.articles.update_many(
                    {"category_id": source_cat["_id"]},
                    {"$set": {"category_id": target_id}}
                )
                count += result.modified_count

                # 删除旧分类
                await db.categories.delete_one({"_id": source_cat["_id"]})
                print(f"  - 已合并旧分类: {source_name} ({result.modified_count} 篇)")

        print(f"  => {target_name} 现有文章归档完成\n")

    # 3. 特殊处理：将"其他技术"中标题包含 Redis/MySQL 的文章移动到 "数据库技术"
    print("执行特殊规则迁移...")
    db_cat = await db.categories.find_one({"name": "数据库技术"})
    other_cat = await db.categories.find_one({"name": "其他技术"})

    if db_cat and other_cat:
        # 查找其他分类下的数据库文章
        cursor = db.articles.find({
            "category_id": other_cat["_id"],
            "title": {"$regex": "Redis|MySQL|MongoDB|SQL", "$options": "i"}
        })

        async for article in cursor:
            await db.articles.update_one(
                {"_id": article["_id"]},
                {"$set": {"category_id": db_cat["_id"]}}
            )
            print(f"  > 移动 [{article['title']}] 到 数据库技术")

    # 4. 最终统计
    print("\n迁移后分类统计:")
    async for cat in db.categories.find():
        count = await db.articles.count_documents({"category_id": cat["_id"]})
        print(f"- {cat['name']}: {count} 篇")

    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_categories())
