from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProjectCreate(BaseModel):
    """项目创建模型"""
    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    description: str = Field(..., min_length=1, max_length=1000, description="项目描述")
    tech_stack: List[str] = Field(..., min_items=1, description="技术栈")
    cover_image: Optional[str] = Field(None, max_length=500, description="封面图片 URL")
    demo_url: Optional[str] = Field(None, max_length=500, description="演示地址")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub 地址")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    status: str = Field(default="completed", description="项目状态: completed/in_progress/planned")
    highlights: Optional[List[str]] = Field(None, description="项目亮点")
    order: int = Field(default=0, description="排序顺序")


class ProjectUpdate(BaseModel):
    """项目更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    tech_stack: Optional[List[str]] = Field(None, min_items=1)
    cover_image: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    highlights: Optional[List[str]] = None
    order: Optional[int] = None


class ProjectResponse(BaseModel):
    """项目响应模型"""
    id: str
    name: str
    description: str
    tech_stack: List[str]
    cover_image: Optional[str]
    demo_url: Optional[str]
    github_url: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str
    highlights: Optional[List[str]]
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
