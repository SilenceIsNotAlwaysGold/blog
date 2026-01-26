"""
User model
"""
from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional


class User(Document):
    """User document model"""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password_hash: str
    role: str = Field(default="user", pattern="^(admin|user)$")
    avatar: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = [
            "username",
            "email"
        ]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@example.com",
                "password_hash": "hashed_password",
                "role": "admin"
            }
        }
