import pytest
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from app.services.image import ImageService


def test_generate_filename():
    """测试文件名生成"""
    service = ImageService()

    filename1 = service._generate_filename("test.jpg")
    filename2 = service._generate_filename("test.jpg")

    # 应该生成不同的文件名
    assert filename1 != filename2
    # 应该保留扩展名
    assert filename1.endswith('.jpg')
    assert filename2.endswith('.jpg')


def test_validate_file_extension():
    """测试文件扩展名验证"""
    service = ImageService()

    # 有效扩展名
    file_valid = Mock()
    file_valid.filename = "test.jpg"
    is_valid, error = service._validate_file(file_valid)
    assert is_valid is True
    assert error is None

    # 无效扩展名
    file_invalid = Mock()
    file_invalid.filename = "test.exe"
    is_valid, error = service._validate_file(file_invalid)
    assert is_valid is False
    assert "not allowed" in error


def test_validate_file_size():
    """测试文件大小验证"""
    service = ImageService(max_size_mb=1)  # 1MB 限制

    # 文件过大
    file_large = Mock()
    file_large.filename = "test.jpg"
    file_large.size = 2 * 1024 * 1024  # 2MB
    is_valid, error = service._validate_file(file_large)
    assert is_valid is False
    assert "too large" in error


def test_allowed_extensions():
    """测试允许的扩展名"""
    service = ImageService()

    allowed = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for ext in allowed:
        file = Mock()
        file.filename = f"test{ext}"
        is_valid, _ = service._validate_file(file)
        assert is_valid is True


def test_custom_allowed_extensions():
    """测试自定义允许的扩展名"""
    service = ImageService(allowed_extensions={'.jpg', '.png'})

    # 允许的
    file_jpg = Mock()
    file_jpg.filename = "test.jpg"
    is_valid, _ = service._validate_file(file_jpg)
    assert is_valid is True

    # 不允许的
    file_gif = Mock()
    file_gif.filename = "test.gif"
    is_valid, error = service._validate_file(file_gif)
    assert is_valid is False


def test_upload_dir_creation():
    """测试上传目录创建"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()
    upload_path = Path(temp_dir) / "test_uploads"

    try:
        service = ImageService(upload_dir=str(upload_path))
        assert upload_path.exists()
        assert upload_path.is_dir()
    finally:
        shutil.rmtree(temp_dir)


def test_max_size_conversion():
    """测试最大大小转换"""
    service = ImageService(max_size_mb=5)
    assert service.max_size_bytes == 5 * 1024 * 1024
