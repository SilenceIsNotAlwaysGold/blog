from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Query
from typing import Optional
from app.services.image import get_image_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.response import success, error

router = APIRouter(prefix="/images", tags=["images"])


@router.post("/upload", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    resize_width: Optional[int] = Query(None, ge=100, le=4000),
    resize_height: Optional[int] = Query(None, ge=100, le=4000),
    quality: int = Query(85, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """上传图片（需要登录）"""
    image_service = get_image_service()

    # 准备调整大小参数
    resize = None
    if resize_width and resize_height:
        resize = (resize_width, resize_height)

    result = await image_service.upload_image(file, resize=resize, quality=quality)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return success(
        data={
            "filename": result["filename"],
            "url": result["url"],
            "size": result["size"]
        },
        message="Image uploaded successfully"
    )


@router.delete("/{filename}", response_model=dict)
async def delete_image(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """删除图片（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete images"
        )

    image_service = get_image_service()
    success_deleted = await image_service.delete_image(filename)

    if not success_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    return success(message="Image deleted successfully")


@router.get("/{filename}/info", response_model=dict)
async def get_image_info(filename: str):
    """获取图片信息（公开访问）"""
    image_service = get_image_service()
    info = image_service.get_image_info(filename)

    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    return success(data=info)
