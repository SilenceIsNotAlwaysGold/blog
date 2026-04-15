import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_categories():
    client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    db = client.personal_blog

    cats_to_check = ["Web 开发", "其他"]

    for cat_name in cats_to_check:
        cat = await db.categories.find_one({"name": cat_name})
        if cat:
            print(f"\n分类 [{cat_name}] 下的文章:")
            async for article in db.articles.find({"category_id": cat["_id"]}):
                print(f"- {article['title']}")
        else:
            print(f"\n分类 [{cat_name}] 不存在")

    client.close()

if __name__ == "__main__":
    asyncio.run(check_categories())
