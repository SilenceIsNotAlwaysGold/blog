import pytest
from app.services.statistics import StatisticsService


def test_statistics_service_exists():
    """测试统计服务类存在"""
    assert StatisticsService is not None


def test_get_overview_stats_method():
    """测试总览统计方法存在"""
    assert hasattr(StatisticsService, 'get_overview_stats')
    assert callable(StatisticsService.get_overview_stats)


def test_get_article_stats_method():
    """测试文章统计方法存在"""
    assert hasattr(StatisticsService, 'get_article_stats')
    assert callable(StatisticsService.get_article_stats)


def test_get_popular_articles_method():
    """测试热门文章方法存在"""
    assert hasattr(StatisticsService, 'get_popular_articles')
    assert callable(StatisticsService.get_popular_articles)


def test_get_trending_articles_method():
    """测试趋势文章方法存在"""
    assert hasattr(StatisticsService, 'get_trending_articles')
    assert callable(StatisticsService.get_trending_articles)


def test_get_tag_stats_method():
    """测试标签统计方法存在"""
    assert hasattr(StatisticsService, 'get_tag_stats')
    assert callable(StatisticsService.get_tag_stats)


def test_get_skill_category_stats_method():
    """测试技能分类统计方法存在"""
    assert hasattr(StatisticsService, 'get_skill_category_stats')
    assert callable(StatisticsService.get_skill_category_stats)


def test_get_project_stats_method():
    """测试项目统计方法存在"""
    assert hasattr(StatisticsService, 'get_project_stats')
    assert callable(StatisticsService.get_project_stats)


# 注意：实际的统计功能测试需要数据库连接和测试数据
# 这里只测试方法存在性和基本结构
