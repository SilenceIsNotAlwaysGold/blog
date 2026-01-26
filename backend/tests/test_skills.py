import pytest
from app.schemas.skill import SkillCreate, SkillUpdate


def test_skill_create_schema():
    """测试技能创建模型"""
    skill_data = {
        "name": "Python",
        "category": "Programming Languages",
        "proficiency": 90,
        "description": "Advanced Python programming",
        "icon": "python.svg",
        "order": 1
    }

    skill = SkillCreate(**skill_data)
    assert skill.name == "Python"
    assert skill.category == "Programming Languages"
    assert skill.proficiency == 90
    assert skill.description == "Advanced Python programming"
    assert skill.icon == "python.svg"
    assert skill.order == 1


def test_skill_create_validation():
    """测试技能创建验证"""
    # 测试熟练度范围
    with pytest.raises(ValueError):
        SkillCreate(
            name="Python",
            category="Programming",
            proficiency=101  # 超出范围
        )

    with pytest.raises(ValueError):
        SkillCreate(
            name="Python",
            category="Programming",
            proficiency=-1  # 负数
        )

    # 测试必填字段
    with pytest.raises(ValueError):
        SkillCreate(category="Programming", proficiency=90)  # 缺少 name


def test_skill_update_schema():
    """测试技能更新模型"""
    update_data = {
        "proficiency": 95,
        "description": "Expert level Python"
    }

    skill_update = SkillUpdate(**update_data)
    assert skill_update.proficiency == 95
    assert skill_update.description == "Expert level Python"
    assert skill_update.name is None  # 未设置的字段为 None


def test_skill_optional_fields():
    """测试技能可选字段"""
    skill_data = {
        "name": "JavaScript",
        "category": "Programming Languages",
        "proficiency": 85
    }

    skill = SkillCreate(**skill_data)
    assert skill.name == "JavaScript"
    assert skill.description is None
    assert skill.icon is None
    assert skill.order == 0  # 默认值
