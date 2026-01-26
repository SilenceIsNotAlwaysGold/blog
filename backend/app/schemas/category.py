"""
Category and Tag schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    """Category creation request"""
    name: str = Field(..., min_length=1, max_length=50)
    board: str = Field(..., pattern="^(life|tech)$")
    description: Optional[str] = Field(None, max_length=200)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "技术分享",
                "board": "tech",
                "description": "技术相关的文章分类"
            }
        }


class CategoryUpdate(BaseModel):
    """Category update request"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)


class CategoryResponse(BaseModel):
    """Category response"""
    id: str
    name: str
    board: str
    description: Optional[str]
    article_count: int
    created_at: str


class TagCreate(BaseModel):
    """Tag creation request"""
    name: str = Field(..., min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Python"
            }
        }


class TagUpdate(BaseModel):
    """Tag update request"""
    name: str = Field(..., min_length=1, max_length=50)


class TagResponse(BaseModel):
    """Tag response"""
    id: str
    name: str
    article_count: int
    created_at: str
