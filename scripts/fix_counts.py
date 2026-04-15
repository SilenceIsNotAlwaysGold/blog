import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def fix_counts():
    client = AsyncIOMotorClient("mongodb://182.92.70.220:27017")
    db = client.personal_blog

    print("开始修正分类文章计数...")

    async for category in db.categories.find():
        count = await db.articles.count_documents({"category_id": category["_id"]})
        if count != category.get("article_count", 0):
            await db.categories.update_one(
                {"_id": category["_id"]},
                {"$set": {"article_count": count}}
            )
            print(f"Updated {category['name']}: {count} 篇")
        else:
            print(f"Verified {category['name']}: {count} 篇 (Correct)")

    client.close()

if __name__ == "__main__":
    asyncio.run(fix_counts())
