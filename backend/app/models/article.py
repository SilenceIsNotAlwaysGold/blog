"""
Article model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId


class Article(Document):
    """Article document model"""

    title: str = Field(..., min_length=1, max_length=200)
    content: str  # Markdown content
    summary: Optional[str] = Field(None, max_length=500)
    board: Indexed(str) = Field(..., pattern="^(life|tech)$")
    category_id: Optional[ObjectId] = None
    tags: List[str] = Field(default_factory=list)
    author_id: ObjectId
    cover_image: Optional[str] = None
    view_count: int = Field(default=0, ge=0)
    like_count: int = Field(default=0, ge=0)
    is_published: Indexed(bool) = Field(default=False)
    published_at: Optional[datetime] = None
    created_at: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "articles"
        indexes = [
            "board",
            "category_id",
            "tags",
            "is_published",
            [("created_at", -1)],  # Descending index for sorting
            [("title", "text"), ("content", "text")]  # Full-text search
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "My First Article",
                "content": "# Hello World\n\nThis is my first article.",
                "summary": "Introduction to my blog",
                "board": "tech",
                "tags": ["introduction", "blog"],
                "is_published": True
            }
        }
