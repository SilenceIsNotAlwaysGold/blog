import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def list_categories():
    client = AsyncIOMotorClient("mongodb://admin:password@localhost:27017")
    db = client.personal_blog
    categories = await db.categories.find({}, {"name": 1, "_id": 0}).to_list(length=100)
    print("当前已有的分类：")
    for cat in categories:
        print(f"- {cat['name']}")
    client.close()

if __name__ == "__main__":
    asyncio.run(list_categories())
