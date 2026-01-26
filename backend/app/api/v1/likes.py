from fastapi import APIRouter, HTTPException, Request, status
from app.services.like import LikeService
from app.utils.response import success, error

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{article_id}", response_model=dict)
async def toggle_like(article_id: str, request: Request):
    """切换点赞状态（点赞/取消点赞）"""
    result = await LikeService.toggle_like(article_id, request)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result["message"]
        )

    return success(
        data={
            "action": result["action"],
            "like_count": result["like_count"]
        },
        message=f"Article {result['action']} successfully"
    )


@router.get("/{article_id}/status", response_model=dict)
async def check_like_status(article_id: str, request: Request):
    """检查当前用户是否已点赞"""
    is_liked = await LikeService.check_like_status(article_id, request)
    return success(data={"is_liked": is_liked})


@router.get("/{article_id}/count", response_model=dict)
async def get_like_count(article_id: str):
    """获取文章点赞数"""
    count = await LikeService.get_article_likes(article_id)
    return success(data={"like_count": count})
