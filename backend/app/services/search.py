from typing import List, Optional
from app.models.article import Article
from app.models.skill import Skill
from app.models.project import Project


class SearchService:
    """搜索服务类 - 提供全局搜索功能"""

    @staticmethod
    async def search_articles(
        keyword: str,
        board: Optional[str] = None,
        limit: int = 20
    ) -> List[Article]:
        """搜索文章（标题、内容、标签）"""
        query = Article.find()

        # 板块过滤
        if board:
            query = query.find(Article.board == board)

        # 仅搜索已发布的文章
        query = query.find(Article.is_published == True)

        # 全文搜索（标题、内容、标签）
        # MongoDB 全文索引搜索
        articles = await query.find(
            {"$text": {"$search": keyword}}
        ).sort([("score", {"$meta": "textScore"})]).limit(limit).to_list()

        # 如果全文搜索没有结果，尝试正则匹配
        if not articles:
            articles = await query.find({
                "$or": [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"summary": {"$regex": keyword, "$options": "i"}},
                    {"tags": {"$regex": keyword, "$options": "i"}}
                ]
            }).sort("-created_at").limit(limit).to_list()

        return articles

    @staticmethod
    async def search_skills(keyword: str, limit: int = 20) -> List[Skill]:
        """搜索技能（名称、分类、描述）"""
        skills = await Skill.find({
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"category": {"$regex": keyword, "$options": "i"}},
                {"description": {"$regex": keyword, "$options": "i"}}
            ]
        }).sort([("order", -1), ("created_at", -1)]).limit(limit).to_list()

        return skills

    @staticmethod
    async def search_projects(keyword: str, limit: int = 20) -> List[Project]:
        """搜索项目（名称、描述、技术栈）"""
        projects = await Project.find({
            "$or": [
                {"name": {"$regex": keyword, "$options": "i"}},
                {"description": {"$regex": keyword, "$options": "i"}},
                {"tech_stack": {"$regex": keyword, "$options": "i"}}
            ]
        }).sort([("order", -1), ("start_date", -1)]).limit(limit).to_list()

        return projects

    @staticmethod
    async def global_search(keyword: str, limit_per_type: int = 10) -> dict:
        """全局搜索（所有类型）"""
        # 并发搜索所有类型
        articles = await SearchService.search_articles(keyword, limit=limit_per_type)
        skills = await SearchService.search_skills(keyword, limit=limit_per_type)
        projects = await SearchService.search_projects(keyword, limit=limit_per_type)

        return {
            "articles": articles,
            "skills": skills,
            "projects": projects,
            "total": len(articles) + len(skills) + len(projects)
        }

    @staticmethod
    async def search_suggestions(keyword: str, limit: int = 5) -> List[str]:
        """搜索建议（基于标题和标签）"""
        suggestions = set()

        # 从文章标题获取建议
        articles = await Article.find(
            {"title": {"$regex": keyword, "$options": "i"}},
            {"is_published": True}
        ).limit(limit).to_list()

        for article in articles:
            suggestions.add(article.title)

        # 从标签获取建议
        tag_articles = await Article.find(
            {"tags": {"$regex": keyword, "$options": "i"}},
            {"is_published": True}
        ).limit(limit).to_list()

        for article in tag_articles:
            for tag in article.tags:
                if keyword.lower() in tag.lower():
                    suggestions.add(tag)

        return sorted(list(suggestions))[:limit]

    @staticmethod
    async def get_popular_tags(limit: int = 20) -> List[dict]:
        """获取热门标签（按使用频率）"""
        # 聚合所有已发布文章的标签
        articles = await Article.find({"is_published": True}).to_list()

        tag_counts = {}
        for article in articles:
            for tag in article.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 排序并返回
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [
            {"tag": tag, "count": count}
            for tag, count in sorted_tags[:limit]
        ]

    @staticmethod
    async def get_related_articles(
        article_id: str,
        limit: int = 5
    ) -> List[Article]:
        """获取相关文章（基于标签和分类）"""
        article = await Article.get(article_id)
        if not article:
            return []

        # 查找相同标签或分类的文章
        query = {
            "_id": {"$ne": article.id},
            "is_published": True,
            "board": article.board,
            "$or": [
                {"tags": {"$in": article.tags}},
                {"category_id": article.category_id}
            ]
        }

        related = await Article.find(query).sort("-created_at").limit(limit).to_list()
        return related
