from fastapi import APIRouter, Query
from typing import Optional
from app.services.search import SearchService
from app.schemas.article import ArticleResponse
from app.schemas.skill import SkillResponse
from app.schemas.project import ProjectResponse
from app.utils.response import success

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/articles", response_model=dict)
async def search_articles(
    q: str = Query(..., min_length=1, description="Search keyword"),
    board: Optional[str] = Query(None, description="Filter by board"),
    limit: int = Query(20, ge=1, le=100)
):
    """搜索文章"""
    articles = await SearchService.search_articles(q, board, limit)
    return success(
        data=[ArticleResponse.model_validate(a).model_dump() for a in articles]
    )


@router.get("/skills", response_model=dict)
async def search_skills(
    q: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(20, ge=1, le=100)
):
    """搜索技能"""
    skills = await SearchService.search_skills(q, limit)
    return success(
        data=[SkillResponse.model_validate(s).model_dump() for s in skills]
    )


@router.get("/projects", response_model=dict)
async def search_projects(
    q: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(20, ge=1, le=100)
):
    """搜索项目"""
    projects = await SearchService.search_projects(q, limit)
    return success(
        data=[ProjectResponse.model_validate(p).model_dump() for p in projects]
    )


@router.get("/global", response_model=dict)
async def global_search(
    q: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(10, ge=1, le=50, description="Limit per type")
):
    """全局搜索（所有类型）"""
    results = await SearchService.global_search(q, limit)

    return success(
        data={
            "articles": [ArticleResponse.model_validate(a).model_dump() for a in results["articles"]],
            "skills": [SkillResponse.model_validate(s).model_dump() for s in results["skills"]],
            "projects": [ProjectResponse.model_validate(p).model_dump() for p in results["projects"]],
            "total": results["total"]
        }
    )


@router.get("/suggestions", response_model=dict)
async def get_suggestions(
    q: str = Query(..., min_length=1, description="Search keyword"),
    limit: int = Query(5, ge=1, le=10)
):
    """获取搜索建议"""
    suggestions = await SearchService.search_suggestions(q, limit)
    return success(data=suggestions)


@router.get("/tags/popular", response_model=dict)
async def get_popular_tags(
    limit: int = Query(20, ge=1, le=50)
):
    """获取热门标签"""
    tags = await SearchService.get_popular_tags(limit)
    return success(data=tags)


@router.get("/articles/{article_id}/related", response_model=dict)
async def get_related_articles(
    article_id: str,
    limit: int = Query(5, ge=1, le=20)
):
    """获取相关文章"""
    articles = await SearchService.get_related_articles(article_id, limit)
    return success(
        data=[ArticleResponse.model_validate(a).model_dump() for a in articles]
    )
