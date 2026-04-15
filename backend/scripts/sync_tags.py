#!/usr/bin/env python3
"""
Sync tags from articles to tags collection
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.article import Article
from app.models.tag import Tag
from app.core.config import settings

async def sync_tags():
    """Sync tags"""
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[Article, Tag]
    )

    print("Clearing existing tags...")
    await Tag.delete_all()

    print("Fetching all articles...")
    articles = await Article.find().to_list()
    
    tag_counts = {}
    
    for article in articles:
        if article.tags:
            for tag_name in article.tags:
                if tag_name not in tag_counts:
                    tag_counts[tag_name] = 0
                tag_counts[tag_name] += 1
    
    print(f"Found {len(tag_counts)} unique tags.")
    
    for tag_name, count in tag_counts.items():
        tag = Tag(name=tag_name, article_count=count)
        await tag.insert()
        print(f"Created tag: {tag_name} ({count})")

    print("✅ Tags synced successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(sync_tags())

