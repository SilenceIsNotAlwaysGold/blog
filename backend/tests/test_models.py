"""
Tests for database models
"""
import pytest
from app.models.user import User
from app.models.article import Article
from app.models.category import Category
from app.models.tag import Tag
from app.models.skill import Skill
from app.models.project import Project
from app.models.like import Like
from app.models.view import View
from bson import ObjectId


def test_user_model_structure():
    """Test user model can be instantiated"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "role": "user"
    }
    user = User(**user_data)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "user"


def test_article_model_structure():
    """Test article model can be instantiated"""
    article_data = {
        "title": "Test Article",
        "content": "# Test Content",
        "board": "tech",
        "author_id": ObjectId()
    }
    article = Article(**article_data)
    assert article.title == "Test Article"
    assert article.board == "tech"
    assert article.view_count == 0
    assert article.like_count == 0


def test_category_model_structure():
    """Test category model can be instantiated"""
    category_data = {
        "name": "技术",
        "board": "tech",
        "description": "技术分类"
    }
    category = Category(**category_data)
    assert category.name == "技术"
    assert category.board == "tech"
    assert category.article_count == 0


def test_tag_model_structure():
    """Test tag model can be instantiated"""
    tag_data = {
        "name": "Python"
    }
    tag = Tag(**tag_data)
    assert tag.name == "Python"
    assert tag.article_count == 0


def test_skill_model_structure():
    """Test skill model can be instantiated"""
    skill_data = {
        "name": "Python",
        "category": "backend",
        "proficiency": 90
    }
    skill = Skill(**skill_data)
    assert skill.name == "Python"
    assert skill.category == "backend"
    assert skill.proficiency == 90


def test_project_model_structure():
    """Test project model can be instantiated"""
    project_data = {
        "name": "Personal Blog",
        "description": "A blog system",
        "tech_stack": ["Vue 3", "FastAPI"]
    }
    project = Project(**project_data)
    assert project.name == "Personal Blog"
    assert len(project.tech_stack) == 2


def test_like_model_structure():
    """Test like model can be instantiated"""
    like_data = {
        "article_id": ObjectId(),
        "ip_address": "192.168.1.1"
    }
    like = Like(**like_data)
    assert like.ip_address == "192.168.1.1"


def test_view_model_structure():
    """Test view model can be instantiated"""
    view_data = {
        "article_id": ObjectId(),
        "ip_address": "192.168.1.1"
    }
    view = View(**view_data)
    assert view.ip_address == "192.168.1.1"
