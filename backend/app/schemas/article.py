"""
Article schemas (Pydantic models for request/response)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ArticleCreate(BaseModel):
    """Article creation request"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    summary: Optional[str] = Field(None, max_length=500)
    board: str = Field(..., pattern="^(life|tech)$")
    category_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    cover_image: Optional[str] = None
    is_published: bool = Field(default=False)

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


class ArticleUpdate(BaseModel):
    """Article update request"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None
    cover_image: Optional[str] = None
    is_published: Optional[bool] = None


class ArticleResponse(BaseModel):
    """Article response"""
    id: str
    title: str
    content: str
    summary: Optional[str]
    board: str
    category_id: Optional[str]
    tags: List[str]
    author_id: str
    cover_image: Optional[str]
    view_count: int
    like_count: int
    is_published: bool
    published_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "My First Article",
                "content": "# Hello World",
                "summary": "Introduction",
                "board": "tech",
                "category_id": None,
                "tags": ["blog"],
                "author_id": "507f1f77bcf86cd799439012",
                "cover_image": None,
                "view_count": 0,
                "like_count": 0,
                "is_published": True,
                "published_at": "2024-01-01T00:00:00",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class ArticleListQuery(BaseModel):
    """Article list query parameters"""
    board: Optional[str] = Field(None, pattern="^(life|tech)$")
    category_id: Optional[str] = None
    tag: Optional[str] = None
    is_published: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
