"""
Tag model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime


class Tag(Document):
    """Tag document model"""

    name: str = Field(..., min_length=1, max_length=50)
    article_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "tags"
        indexes = [
            "name"
        ]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Python",
                "article_count": 5
            }
        }
