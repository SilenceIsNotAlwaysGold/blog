"""
Database connection and initialization
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

# Global database client
db_client: Optional[AsyncIOMotorClient] = None


async def connect_to_database():
    """Connect to MongoDB database"""
    global db_client

    db_client = AsyncIOMotorClient(settings.MONGODB_URL)

    # Import all models
    from app.models.user import User
    from app.models.article import Article
    from app.models.category import Category
    from app.models.tag import Tag
    from app.models.skill import Skill
    from app.models.project import Project
    from app.models.like import Like
    from app.models.view import View

    # Initialize Beanie with all models
    await init_beanie(
        database=db_client[settings.MONGODB_DB_NAME],
        document_models=[
            User,
            Article,
            Category,
            Tag,
            Skill,
            Project,
            Like,
            View
        ]
    )

    logger.info(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_database_connection():
    """Close database connection"""
    global db_client
    if db_client:
        db_client.close()
        logger.info("Closed MongoDB connection")


async def get_database():
    """Get database instance"""
    return db_client[settings.MONGODB_DB_NAME]
