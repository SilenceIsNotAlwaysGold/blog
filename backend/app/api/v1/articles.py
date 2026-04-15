"""
Article API endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request, Body
from typing import Optional
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
    ArticleListQuery
)
from app.services.article import ArticleService
from app.dependencies.auth import get_current_user, get_optional_current_user
from app.models.user import User
from app.utils.response import success, paginated_response
from app.utils.exceptions import NotFoundException, ForbiddenException

router = APIRouter(prefix="/articles", tags=["Articles"])


def article_to_response(article) -> ArticleResponse:
    """Convert Article model to ArticleResponse"""
    return ArticleResponse(
        id=str(article.id),
        title=article.title,
        content=article.content,
        summary=article.summary,
        board=article.board,
        category_id=str(article.category_id) if article.category_id else None,
        tags=article.tags,
        author_id=str(article.author_id),
        cover_image=article.cover_image,
        view_count=article.view_count,
        like_count=article.like_count,
        is_published=article.is_published,
        published_at=article.published_at.isoformat() if article.published_at else None,
        created_at=article.created_at.isoformat(),
        updated_at=article.updated_at.isoformat()
    )


@router.get("", response_model=dict)
async def get_articles(
    board: Optional[str] = None,
    category_id: Optional[str] = None,
    tag: Optional[str] = None,
    is_published: Optional[bool] = None,
    page: int = 1,
    page_size: int = 10,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get articles list with filters and pagination
    Life board requires authentication
    """
    # Check authentication for life board
    if board == "life" and not current_user:
        raise ForbiddenException("Authentication required for life board")

    # Get articles
    articles, total = await ArticleService.get_articles(
        board=board,
        category_id=category_id,
        tag=tag,
        is_published=is_published,
        page=page,
        page_size=page_size
    )

    # Convert to response
    items = [article_to_response(article) for article in articles]

    return paginated_response(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{article_id}", response_model=dict)
async def get_article(
    article_id: str,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get article by ID
    Life board articles require authentication
    Automatically increments view count
    """
    article = await ArticleService.get_article_by_id(article_id)
    if not article:
        raise NotFoundException("Article not found")

    # Check authentication for life board
    if article.board == "life" and not current_user:
        raise ForbiddenException("Authentication required for life board")

    # Increment view count
    client_ip = request.client.host if request.client else "unknown"
    await ArticleService.increment_view_count(article_id, client_ip)

    return success(data=article_to_response(article))


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new article
    Requires authentication
    """
    article = await ArticleService.create_article(
        article_data=article_data,
        author_id=str(current_user.id)
    )

    return success(
        data=article_to_response(article),
        message="Article created successfully",
        code=201
    )


@router.put("/{article_id}", response_model=dict)
async def update_article(
    article_id: str,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update an article
    Requires authentication. Only the author or admin can update.
    """
    existing = await ArticleService.get_article_by_id(article_id)
    if not existing:
        raise NotFoundException("Article not found")

    if str(existing.author_id) != str(current_user.id) and current_user.role != "admin":
        raise ForbiddenException("You can only edit your own articles")

    article = await ArticleService.update_article(article_id, article_data)

    return success(
        data=article_to_response(article),
        message="Article updated successfully"
    )


@router.delete("/{article_id}", response_model=dict)
async def delete_article(
    article_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete an article
    Requires authentication. Only the author or admin can delete.
    """
    existing = await ArticleService.get_article_by_id(article_id)
    if not existing:
        raise NotFoundException("Article not found")

    if str(existing.author_id) != str(current_user.id) and current_user.role != "admin":
        raise ForbiddenException("You can only delete your own articles")

    await ArticleService.delete_article(article_id)

    return success(message="Article deleted successfully")


@router.post("/search", response_model=dict)
async def search_articles(
    keyword: str = Body(...),
    page: int = Body(1),
    page_size: int = Body(10)
):
    """
    Search articles by keyword
    Only searches in tech board published articles
    """
    articles, total = await ArticleService.search_articles(
        keyword=keyword,
        page=page,
        page_size=page_size
    )

    items = [article_to_response(article) for article in articles]

    return paginated_response(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )
