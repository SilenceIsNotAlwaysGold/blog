import pytest
from app.services.search import SearchService


def test_search_service_exists():
    """测试搜索服务类存在"""
    assert SearchService is not None


def test_search_articles_method():
    """测试搜索文章方法存在"""
    assert hasattr(SearchService, 'search_articles')
    assert callable(SearchService.search_articles)


def test_search_skills_method():
    """测试搜索技能方法存在"""
    assert hasattr(SearchService, 'search_skills')
    assert callable(SearchService.search_skills)


def test_search_projects_method():
    """测试搜索项目方法存在"""
    assert hasattr(SearchService, 'search_projects')
    assert callable(SearchService.search_projects)


def test_global_search_method():
    """测试全局搜索方法存在"""
    assert hasattr(SearchService, 'global_search')
    assert callable(SearchService.global_search)


def test_search_suggestions_method():
    """测试搜索建议方法存在"""
    assert hasattr(SearchService, 'search_suggestions')
    assert callable(SearchService.search_suggestions)


def test_get_popular_tags_method():
    """测试获取热门标签方法存在"""
    assert hasattr(SearchService, 'get_popular_tags')
    assert callable(SearchService.get_popular_tags)


def test_get_related_articles_method():
    """测试获取相关文章方法存在"""
    assert hasattr(SearchService, 'get_related_articles')
    assert callable(SearchService.get_related_articles)


# 注意：实际的搜索功能测试需要数据库连接和测试数据
# 这里只测试方法存在性和基本结构
