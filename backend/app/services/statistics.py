from typing import Dict, List
from datetime import datetime, timedelta
from app.models.article import Article
from app.models.view import View
from app.models.like import Like
from app.models.skill import Skill
from app.models.project import Project


class StatisticsService:
    """统计分析服务类"""

    @staticmethod
    async def get_overview_stats() -> Dict:
        """获取总览统计"""
        # 文章统计
        total_articles = await Article.find().count()
        published_articles = await Article.find({"is_published": True}).count()
        tech_articles = await Article.find({"board": "tech", "is_published": True}).count()
        life_articles = await Article.find({"board": "life", "is_published": True}).count()

        # 浏览和点赞统计
        total_views = await View.find().count()
        total_likes = await Like.find().count()

        # 技能和项目统计
        total_skills = await Skill.find().count()
        total_projects = await Project.find().count()
        completed_projects = await Project.find({"status": "completed"}).count()

        return {
            "articles": {
                "total": total_articles,
                "published": published_articles,
                "tech": tech_articles,
                "life": life_articles,
                "draft": total_articles - published_articles
            },
            "engagement": {
                "total_views": total_views,
                "total_likes": total_likes,
                "avg_views_per_article": total_views / published_articles if published_articles > 0 else 0,
                "avg_likes_per_article": total_likes / published_articles if published_articles > 0 else 0
            },
            "portfolio": {
                "total_skills": total_skills,
                "total_projects": total_projects,
                "completed_projects": completed_projects
            }
        }

    @staticmethod
    async def get_article_stats(days: int = 30) -> Dict:
        """获取文章统计（最近 N 天）"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # 最近发布的文章
        recent_articles = await Article.find({
            "is_published": True,
            "published_at": {"$gte": start_date}
        }).count()

        # 按板块统计
        tech_recent = await Article.find({
            "board": "tech",
            "is_published": True,
            "published_at": {"$gte": start_date}
        }).count()

        life_recent = await Article.find({
            "board": "life",
            "is_published": True,
            "published_at": {"$gte": start_date}
        }).count()

        return {
            "period_days": days,
            "total_published": recent_articles,
            "by_board": {
                "tech": tech_recent,
                "life": life_recent
            }
        }

    @staticmethod
    async def get_popular_articles(limit: int = 10) -> List[Dict]:
        """获取热门文章（按浏览量）"""
        articles = await Article.find(
            {"is_published": True}
        ).sort("-view_count").limit(limit).to_list()

        return [
            {
                "id": str(article.id),
                "title": article.title,
                "board": article.board,
                "view_count": article.view_count,
                "like_count": article.like_count,
                "published_at": article.published_at
            }
            for article in articles
        ]

    @staticmethod
    async def get_trending_articles(days: int = 7, limit: int = 10) -> List[Dict]:
        """获取趋势文章（最近 N 天浏览量增长）"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # 获取最近浏览的文章
        recent_views = await View.find({
            "created_at": {"$gte": start_date}
        }).to_list()

        # 统计每篇文章的浏览次数
        view_counts = {}
        for view in recent_views:
            article_id = view.article_id
            view_counts[article_id] = view_counts.get(article_id, 0) + 1

        # 排序并获取前 N 篇
        sorted_articles = sorted(
            view_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

        # 获取文章详情
        trending = []
        for article_id, recent_views_count in sorted_articles:
            article = await Article.get(article_id)
            if article and article.is_published:
                trending.append({
                    "id": str(article.id),
                    "title": article.title,
                    "board": article.board,
                    "recent_views": recent_views_count,
                    "total_views": article.view_count,
                    "like_count": article.like_count
                })

        return trending

    @staticmethod
    async def get_tag_stats(limit: int = 20) -> List[Dict]:
        """获取标签统计"""
        articles = await Article.find({"is_published": True}).to_list()

        tag_stats = {}
        for article in articles:
            for tag in article.tags:
                if tag not in tag_stats:
                    tag_stats[tag] = {
                        "tag": tag,
                        "count": 0,
                        "total_views": 0,
                        "total_likes": 0
                    }
                tag_stats[tag]["count"] += 1
                tag_stats[tag]["total_views"] += article.view_count
                tag_stats[tag]["total_likes"] += article.like_count

        # 排序并返回
        sorted_tags = sorted(
            tag_stats.values(),
            key=lambda x: x["count"],
            reverse=True
        )[:limit]

        return sorted_tags

    @staticmethod
    async def get_skill_category_stats() -> List[Dict]:
        """获取技能分类统计"""
        skills = await Skill.find().to_list()

        category_stats = {}
        for skill in skills:
            category = skill.category
            if category not in category_stats:
                category_stats[category] = {
                    "category": category,
                    "count": 0,
                    "avg_proficiency": 0,
                    "total_proficiency": 0
                }
            category_stats[category]["count"] += 1
            category_stats[category]["total_proficiency"] += skill.proficiency

        # 计算平均熟练度
        for stats in category_stats.values():
            stats["avg_proficiency"] = round(
                stats["total_proficiency"] / stats["count"], 1
            )
            del stats["total_proficiency"]

        return sorted(
            category_stats.values(),
            key=lambda x: x["count"],
            reverse=True
        )

    @staticmethod
    async def get_project_stats() -> Dict:
        """获取项目统计"""
        projects = await Project.find().to_list()

        # 按状态统计
        status_stats = {
            "completed": 0,
            "in_progress": 0,
            "planned": 0
        }

        # 技术栈统计
        tech_stats = {}

        for project in projects:
            status_stats[project.status] = status_stats.get(project.status, 0) + 1

            for tech in project.tech_stack:
                tech_stats[tech] = tech_stats.get(tech, 0) + 1

        # 排序技术栈
        sorted_tech = sorted(
            tech_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]

        return {
            "by_status": status_stats,
            "total": len(projects),
            "top_technologies": [
                {"tech": tech, "count": count}
                for tech, count in sorted_tech
            ]
        }
