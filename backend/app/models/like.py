"""
Like model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from bson import ObjectId


class Like(Document):
    """Like record document model"""

    article_id: Indexed(ObjectId)
    ip_address: str = Field(..., max_length=45)  # IPv6 max length
    user_agent: str = Field(default="")
    created_at: Indexed(datetime) = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "likes"
        indexes = [
            "article_id",
            [("created_at", -1)],
            [("article_id", 1), ("ip_address", 1)]  # Compound unique index
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "article_id": "507f1f77bcf86cd799439011",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0..."
            }
        }
