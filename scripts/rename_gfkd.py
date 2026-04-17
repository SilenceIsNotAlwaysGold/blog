import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb://blogadmin:Xlj%40Blog2026!Secure@blog-mongodb:27017/?authSource=admin")
    db = client["personal_blog"]
    r = await db.projects.update_one({"name": "GFKD 人机协同项目"}, {"$set": {"name": "人机协同智能检索项目"}})
    print(f"matched: {r.matched_count}, modified: {r.modified_count}")

asyncio.run(main())
