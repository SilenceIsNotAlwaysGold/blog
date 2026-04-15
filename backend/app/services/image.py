import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import aiofiles


class ImageService:
    """图片服务类"""

    def __init__(
        self,
        upload_dir: str = "uploads/images",
        max_size_mb: int = 5,
        allowed_extensions: set = None
    ):
        self.upload_dir = Path(upload_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.allowed_extensions = allowed_extensions or {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

        # 确保上传目录存在
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, original_filename: str) -> str:
        """生成唯一文件名"""
        ext = Path(original_filename).suffix.lower()
        unique_id = uuid.uuid4().hex
        return f"{unique_id}{ext}"

    def _validate_file(self, file: UploadFile) -> tuple[bool, Optional[str]]:
        """验证文件"""
        # 检查扩展名
        ext = Path(file.filename).suffix.lower()
        if ext not in self.allowed_extensions:
            return False, f"File type not allowed. Allowed: {', '.join(self.allowed_extensions)}"

        # 检查文件大小（如果可用）
        if hasattr(file, 'size') and file.size:
            if file.size > self.max_size_bytes:
                max_mb = self.max_size_bytes / (1024 * 1024)
                return False, f"File too large. Max size: {max_mb}MB"

        return True, None

    async def upload_image(
        self,
        file: UploadFile,
        resize: Optional[tuple[int, int]] = None,
        quality: int = 85
    ) -> dict:
        """上传图片"""
        # 验证文件
        is_valid, error_msg = self._validate_file(file)
        if not is_valid:
            return {"success": False, "message": error_msg}

        try:
            # 生成文件名
            filename = self._generate_filename(file.filename)
            file_path = self.upload_dir / filename

            # 读取文件内容
            content = await file.read()

            # 检查实际大小
            if len(content) > self.max_size_bytes:
                max_mb = self.max_size_bytes / (1024 * 1024)
                return {"success": False, "message": f"File too large. Max size: {max_mb}MB"}

            # 如果需要调整大小，使用 PIL
            if resize:
                try:
                    from io import BytesIO
                    img = Image.open(BytesIO(content))

                    # 保持宽高比调整大小
                    img.thumbnail(resize, Image.Resampling.LANCZOS)

                    # 保存到字节流
                    output = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(output, format=img_format, quality=quality, optimize=True)
                    content = output.getvalue()
                except Exception as e:
                    return {"success": False, "message": f"Failed to process image: {str(e)}"}

            # 保存文件
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)

            # 返回相对路径
            relative_path = f"/uploads/images/{filename}"
            return {
                "success": True,
                "filename": filename,
                "url": relative_path,
                "size": len(content)
            }

        except Exception as e:
            return {"success": False, "message": f"Upload failed: {str(e)}"}

    async def delete_image(self, filename: str) -> bool:
        """删除图片"""
        try:
            file_path = self.upload_dir / filename
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

    def get_image_info(self, filename: str) -> Optional[dict]:
        """获取图片信息"""
        try:
            file_path = self.upload_dir / filename
            if not file_path.exists():
                return None

            with Image.open(file_path) as img:
                return {
                    "filename": filename,
                    "size": file_path.stat().st_size,
                    "width": img.width,
                    "height": img.height,
                    "format": img.format
                }
        except Exception:
            return None


# 全局图片服务实例
_image_service: Optional[ImageService] = None


def get_image_service() -> ImageService:
    """获取图片服务实例"""
    global _image_service
    if _image_service is None:
        _image_service = ImageService()
    return _image_service
