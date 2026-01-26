from typing import Optional
from beanie import PydanticObjectId
from fastapi import Request
from app.models.like import Like
from app.models.article import Article


class LikeService:
    """点赞服务类"""

    @staticmethod
    def get_client_ip(request: Request) -> str:
        """获取客户端 IP 地址"""
        # 优先从 X-Forwarded-For 获取（代理/负载均衡场景）
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # 从 X-Real-IP 获取
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # 直接连接场景
        return request.client.host if request.client else "unknown"

    @staticmethod
    async def toggle_like(article_id: str, request: Request) -> dict:
        """切换点赞状态（点赞/取消点赞）"""
        # 获取文章
        article = await Article.get(PydanticObjectId(article_id))
        if not article:
            return {"success": False, "message": "Article not found"}

        # 获取客户端 IP
        ip_address = LikeService.get_client_ip(request)

        # 检查是否已点赞
        existing_like = await Like.find_one(
            Like.article_id == article_id,
            Like.ip_address == ip_address
        )

        if existing_like:
            # 取消点赞
            await existing_like.delete()
            article.like_count = max(0, article.like_count - 1)
            await article.save()
            return {
                "success": True,
                "action": "unliked",
                "like_count": article.like_count
            }
        else:
            # 添加点赞
            like = Like(article_id=article_id, ip_address=ip_address)
            await like.insert()
            article.like_count += 1
            await article.save()
            return {
                "success": True,
                "action": "liked",
                "like_count": article.like_count
            }

    @staticmethod
    async def check_like_status(article_id: str, request: Request) -> bool:
        """检查用户是否已点赞"""
        ip_address = LikeService.get_client_ip(request)
        existing_like = await Like.find_one(
            Like.article_id == article_id,
            Like.ip_address == ip_address
        )
        return existing_like is not None

    @staticmethod
    async def get_article_likes(article_id: str) -> int:
        """获取文章点赞数"""
        article = await Article.get(PydanticObjectId(article_id))
        return article.like_count if article else 0
