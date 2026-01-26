from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SkillCreate(BaseModel):
    """技能创建模型"""
    name: str = Field(..., min_length=1, max_length=50, description="技能名称")
    category: str = Field(..., min_length=1, max_length=50, description="技能分类")
    proficiency: int = Field(..., ge=0, le=100, description="熟练度 (0-100)")
    description: Optional[str] = Field(None, max_length=500, description="技能描述")
    icon: Optional[str] = Field(None, max_length=200, description="图标 URL")
    order: int = Field(default=0, description="排序顺序")


class SkillUpdate(BaseModel):
    """技能更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    proficiency: Optional[int] = Field(None, ge=0, le=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=200)
    order: Optional[int] = None


class SkillResponse(BaseModel):
    """技能响应模型"""
    id: str
    name: str
    category: str
    proficiency: int
    description: Optional[str]
    icon: Optional[str]
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
