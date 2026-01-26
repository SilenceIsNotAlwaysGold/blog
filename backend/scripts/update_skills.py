#!/usr/bin/env python3
"""
Update skills to add missing fields
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.skill import Skill
from app.core.config import settings
from datetime import datetime


async def update_skills():
    """Update skills with missing fields"""
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    # Initialize Beanie
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[Skill]
    )

    # Get all skills
    skills = await Skill.find_all().to_list()

    updated_count = 0
    for skill in skills:
        # Add missing fields
        if not hasattr(skill, 'description') or skill.description is None:
            skill.description = None
        if not hasattr(skill, 'updated_at'):
            skill.updated_at = datetime.utcnow()

        await skill.save()
        updated_count += 1
        print(f"✅ Updated skill: {skill.name}")

    print(f"\n🎉 Updated {updated_count} skills successfully!")
    client.close()


if __name__ == "__main__":
    asyncio.run(update_skills())
