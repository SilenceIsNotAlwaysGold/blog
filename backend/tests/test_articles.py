"""
Tests for article module
"""
import pytest
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleListQuery


def test_article_create_schema():
    """Test article creation schema"""
    data = {
        "title": "Test Article",
        "content": "# Test Content",
        "board": "tech",
        "tags": ["test"],
        "is_published": True
    }
    article = ArticleCreate(**data)
    assert article.title == "Test Article"
    assert article.board == "tech"
    assert article.is_published is True


def test_article_update_schema():
    """Test article update schema"""
    data = {
        "title": "Updated Title",
        "is_published": False
    }
    article = ArticleUpdate(**data)
    assert article.title == "Updated Title"
    assert article.is_published is False


def test_article_list_query_defaults():
    """Test article list query with defaults"""
    query = ArticleListQuery()
    assert query.page == 1
    assert query.page_size == 10
    assert query.board is None


def test_article_list_query_with_filters():
    """Test article list query with filters"""
    query = ArticleListQuery(
        board="tech",
        page=2,
        page_size=20
    )
    assert query.board == "tech"
    assert query.page == 2
    assert query.page_size == 20


def test_article_board_validation():
    """Test article board field validation"""
    # Valid boards
    ArticleCreate(title="Test", content="Content", board="tech")
    ArticleCreate(title="Test", content="Content", board="life")

    # Invalid board should raise validation error
    with pytest.raises(Exception):
        ArticleCreate(title="Test", content="Content", board="invalid")
