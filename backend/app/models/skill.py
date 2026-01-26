"""
Skill model
"""
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional


class Skill(Document):
    """Skill document model"""

    name: str = Field(..., min_length=1, max_length=50)
    category: str = Field(
        ...,
        pattern="^(frontend|backend|database|devops|other)$"
    )
    proficiency: int = Field(..., ge=0, le=100)
    icon: Optional[str] = None
    order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "skills"
        indexes = [
            "category",
            [("order", 1)]  # Ascending index for ordering
        ]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Python",
                "category": "backend",
                "proficiency": 90,
                "order": 1
            }
        }
