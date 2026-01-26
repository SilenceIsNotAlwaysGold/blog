"""
Project model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional, List


class Project(Document):
    """Project document model"""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=1000)
    tech_stack: List[str] = Field(default_factory=list)
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    cover_image: Optional[str] = None
    order: Indexed(int) = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "projects"
        indexes = [
            [("order", 1)]  # Ascending index for ordering
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Personal Blog",
                "description": "A dual-board personal blog system",
                "tech_stack": ["Vue 3", "FastAPI", "MongoDB"],
                "github_url": "https://github.com/user/personal-blog",
                "order": 1
            }
        }
