from fastapi import APIRouter, Query
from app.services.statistics import StatisticsService
from app.utils.response import success

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/overview", response_model=dict)
async def get_overview_stats():
    """获取总览统计（公开访问）"""
    stats = await StatisticsService.get_overview_stats()
    return success(data=stats)


@router.get("/articles", response_model=dict)
async def get_article_stats(
    days: int = Query(30, ge=1, le=365, description="统计天数")
):
    """获取文章统计（公开访问）"""
    stats = await StatisticsService.get_article_stats(days)
    return success(data=stats)


@router.get("/articles/popular", response_model=dict)
async def get_popular_articles(
    limit: int = Query(10, ge=1, le=50, description="返回数量")
):
    """获取热门文章（公开访问）"""
    articles = await StatisticsService.get_popular_articles(limit)
    return success(data=articles)


@router.get("/articles/trending", response_model=dict)
async def get_trending_articles(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
    limit: int = Query(10, ge=1, le=50, description="返回数量")
):
    """获取趋势文章（公开访问）"""
    articles = await StatisticsService.get_trending_articles(days, limit)
    return success(data=articles)


@router.get("/tags", response_model=dict)
async def get_tag_stats(
    limit: int = Query(20, ge=1, le=100, description="返回数量")
):
    """获取标签统计（公开访问）"""
    tags = await StatisticsService.get_tag_stats(limit)
    return success(data=tags)


@router.get("/skills/categories", response_model=dict)
async def get_skill_category_stats():
    """获取技能分类统计（公开访问）"""
    stats = await StatisticsService.get_skill_category_stats()
    return success(data=stats)


@router.get("/projects", response_model=dict)
async def get_project_stats():
    """获取项目统计（公开访问）"""
    stats = await StatisticsService.get_project_stats()
    return success(data=stats)
