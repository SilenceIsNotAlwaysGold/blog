"""
Tests for category and tag modules
"""
import pytest
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    TagCreate,
    TagUpdate
)


def test_category_create_schema():
    """Test category creation schema"""
    data = {
        "name": "技术分享",
        "board": "tech",
        "description": "技术相关"
    }
    category = CategoryCreate(**data)
    assert category.name == "技术分享"
    assert category.board == "tech"


def test_category_update_schema():
    """Test category update schema"""
    data = {"name": "新分类名"}
    category = CategoryUpdate(**data)
    assert category.name == "新分类名"


def test_tag_create_schema():
    """Test tag creation schema"""
    data = {"name": "Python"}
    tag = TagCreate(**data)
    assert tag.name == "Python"


def test_tag_update_schema():
    """Test tag update schema"""
    data = {"name": "JavaScript"}
    tag = TagUpdate(**data)
    assert tag.name == "JavaScript"


def test_category_board_validation():
    """Test category board validation"""
    # Valid boards
    CategoryCreate(name="Test", board="tech")
    CategoryCreate(name="Test", board="life")

    # Invalid board should raise validation error
    with pytest.raises(Exception):
        CategoryCreate(name="Test", board="invalid")
