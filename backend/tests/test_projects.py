import pytest
from datetime import datetime
from app.schemas.project import ProjectCreate, ProjectUpdate


def test_project_create_schema():
    """测试项目创建模型"""
    project_data = {
        "name": "Personal Blog System",
        "description": "A full-stack blog system with dual boards",
        "tech_stack": ["Vue 3", "FastAPI", "MongoDB"],
        "cover_image": "blog-cover.jpg",
        "demo_url": "https://blog.example.com",
        "github_url": "https://github.com/user/blog",
        "start_date": datetime(2024, 1, 1),
        "end_date": datetime(2024, 3, 1),
        "status": "completed",
        "highlights": ["Dual board system", "Markdown editor", "Admin dashboard"],
        "order": 1
    }

    project = ProjectCreate(**project_data)
    assert project.name == "Personal Blog System"
    assert len(project.tech_stack) == 3
    assert project.status == "completed"
    assert len(project.highlights) == 3


def test_project_create_validation():
    """测试项目创建验证"""
    # 测试必填字段
    with pytest.raises(ValueError):
        ProjectCreate(
            description="Test project",
            tech_stack=["Python"]
        )  # 缺少 name

    # 测试技术栈至少一项
    with pytest.raises(ValueError):
        ProjectCreate(
            name="Test Project",
            description="Test description",
            tech_stack=[]  # 空列表
        )


def test_project_update_schema():
    """测试项目更新模型"""
    update_data = {
        "status": "in_progress",
        "demo_url": "https://new-demo.example.com"
    }

    project_update = ProjectUpdate(**update_data)
    assert project_update.status == "in_progress"
    assert project_update.demo_url == "https://new-demo.example.com"
    assert project_update.name is None  # 未设置的字段为 None


def test_project_optional_fields():
    """测试项目可选字段"""
    project_data = {
        "name": "Simple Project",
        "description": "A simple test project",
        "tech_stack": ["Python"]
    }

    project = ProjectCreate(**project_data)
    assert project.name == "Simple Project"
    assert project.cover_image is None
    assert project.demo_url is None
    assert project.github_url is None
    assert project.start_date is None
    assert project.end_date is None
    assert project.status == "completed"  # 默认值
    assert project.highlights is None
    assert project.order == 0  # 默认值


def test_project_status_values():
    """测试项目状态值"""
    valid_statuses = ["completed", "in_progress", "planned"]

    for status_val in valid_statuses:
        project_data = {
            "name": "Test Project",
            "description": "Test description",
            "tech_stack": ["Python"],
            "status": status_val
        }
        project = ProjectCreate(**project_data)
        assert project.status == status_val
