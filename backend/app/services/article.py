"""
Article service
"""
from typing import Optional, List, Tuple
from datetime import datetime
from bson import ObjectId
from app.models.article import Article
from app.models.view import View
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.services.category import TagService


class ArticleService:
    """Article service"""

    @staticmethod
    async def create_article(
        article_data: ArticleCreate,
        author_id: str
    ) -> Article:
        """Create a new article"""
        article = Article(
            title=article_data.title,
            content=article_data.content,
            summary=article_data.summary,
            board=article_data.board,
            category_id=ObjectId(article_data.category_id) if article_data.category_id else None,
            tags=article_data.tags,
            author_id=ObjectId(author_id),
            cover_image=article_data.cover_image,
            is_published=article_data.is_published,
            published_at=datetime.utcnow() if article_data.is_published else None
        )

        await article.insert()
        
        # Update tags
        if article.tags:
            await TagService.update_tag_counts(article.tags, [])
            
        return article

    @staticmethod
    async def get_article_by_id(article_id: str) -> Optional[Article]:
        """Get article by ID"""
        try:
            return await Article.get(ObjectId(article_id))
        except Exception:
            return None

    @staticmethod
    async def get_articles(
        board: Optional[str] = None,
        category_id: Optional[str] = None,
        tag: Optional[str] = None,
        is_published: Optional[bool] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Article], int]:
        """
        Get articles with filters and pagination
        Returns (articles, total_count)
        """
        # Build query
        query = {}

        if board:
            query["board"] = board

        if category_id:
            query["category_id"] = ObjectId(category_id)

        if tag:
            query["tags"] = tag

        if is_published is not None:
            query["is_published"] = is_published

        # Get total count
        total = await Article.find(query).count()

        # Get paginated results
        skip = (page - 1) * page_size
        articles = await Article.find(query).sort("-created_at").skip(skip).limit(page_size).to_list()

        return articles, total

    @staticmethod
    async def update_article(
        article_id: str,
        article_data: ArticleUpdate
    ) -> Optional[Article]:
        """Update an article"""
        article = await ArticleService.get_article_by_id(article_id)
        if not article:
            return None

        # Update fields
        update_data = article_data.model_dump(exclude_unset=True)

        # Calculate tag changes
        tags_to_add = []
        tags_to_remove = []
        
        if "tags" in update_data:
            old_tags = set(article.tags)
            new_tags = set(update_data["tags"])
            tags_to_add = list(new_tags - old_tags)
            tags_to_remove = list(old_tags - new_tags)

        if "category_id" in update_data and update_data["category_id"]:
            update_data["category_id"] = ObjectId(update_data["category_id"])

        # Handle published status change
        if "is_published" in update_data:
            if update_data["is_published"] and not article.is_published:
                update_data["published_at"] = datetime.utcnow()
            elif not update_data["is_published"]:
                update_data["published_at"] = None

        update_data["updated_at"] = datetime.utcnow()

        # Update article
        await article.set(update_data)
        
        # Update tags
        if tags_to_add or tags_to_remove:
            await TagService.update_tag_counts(tags_to_add, tags_to_remove)
            
        return article

    @staticmethod
    async def delete_article(article_id: str) -> bool:
        """Delete an article"""
        article = await ArticleService.get_article_by_id(article_id)
        if not article:
            return False

        await article.delete()
        
        # Update tags
        if article.tags:
            await TagService.update_tag_counts([], article.tags)
            
        return True

    @staticmethod
    async def increment_view_count(article_id: str, ip_address: str) -> bool:
        """
        Increment article view count
        Only count once per IP per day
        """
        article = await ArticleService.get_article_by_id(article_id)
        if not article:
            return False

        # Check if this IP has viewed today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        existing_view = await View.find_one(
            View.article_id == ObjectId(article_id),
            View.ip_address == ip_address,
            View.created_at >= today_start
        )

        if not existing_view:
            # Create view record
            view = View(
                article_id=ObjectId(article_id),
                ip_address=ip_address
            )
            await view.insert()

            # Increment view count
            article.view_count += 1
            await article.save()

        return True

    @staticmethod
    async def search_articles(
        keyword: str,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Article], int]:
        """
        Search articles by keyword (full-text search)
        Only search in tech board and published articles
        """
        # Full-text search query
        query = {
            "$text": {"$search": keyword},
            "board": "tech",
            "is_published": True
        }

        # Get total count
        total = await Article.find(query).count()

        # Get paginated results
        skip = (page - 1) * page_size
        articles = await Article.find(query).sort("-created_at").skip(skip).limit(page_size).to_list()

        return articles, total
