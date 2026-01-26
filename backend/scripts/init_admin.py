#!/usr/bin/env python3
"""
Initialize admin user
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash


async def init_admin():
    """Initialize admin user"""
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    # Initialize Beanie
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User]
    )

    # Check if admin already exists
    existing_admin = await User.find_one(User.username == "admin")
    if existing_admin:
        print("❌ Admin user already exists!")
        print(f"   Username: admin")
        return

    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@example.com",
        password_hash=get_password_hash("admin123"),
        role="admin"
    )

    await admin_user.insert()

    print("✅ Admin user created successfully!")
    print(f"   Username: admin")
    print(f"   Password: admin123")
    print(f"   Email: admin@example.com")
    print("")
    print("⚠️  Please change the password after first login!")

    client.close()


if __name__ == "__main__":
    asyncio.run(init_admin())
