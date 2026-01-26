"""
Category model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional


class Category(Document):
    """Category document model"""

    name: str = Field(..., min_length=1, max_length=50)
    board: Indexed(str) = Field(..., pattern="^(life|tech)$")
    description: Optional[str] = Field(None, max_length=200)
    article_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "categories"
        indexes = [
            "board",
            [("name", 1), ("board", 1)]  # Compound unique index
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "技术分享",
                "board": "tech",
                "description": "技术相关的文章分类"
            }
        }
