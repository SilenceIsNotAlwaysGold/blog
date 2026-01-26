import pytest
from unittest.mock import Mock
from app.services.like import LikeService


def test_get_client_ip_from_forwarded():
    """测试从 X-Forwarded-For 获取 IP"""
    request = Mock()
    request.headers.get = lambda key: "203.0.113.1, 198.51.100.1" if key == "X-Forwarded-For" else None
    request.client = Mock(host="192.168.1.1")

    ip = LikeService.get_client_ip(request)
    assert ip == "203.0.113.1"


def test_get_client_ip_from_real_ip():
    """测试从 X-Real-IP 获取 IP"""
    request = Mock()
    request.headers.get = lambda key: "203.0.113.1" if key == "X-Real-IP" else None
    request.client = Mock(host="192.168.1.1")

    ip = LikeService.get_client_ip(request)
    assert ip == "203.0.113.1"


def test_get_client_ip_from_client():
    """测试从 client.host 获取 IP"""
    request = Mock()
    request.headers.get = lambda key: None
    request.client = Mock(host="192.168.1.1")

    ip = LikeService.get_client_ip(request)
    assert ip == "192.168.1.1"


def test_get_client_ip_unknown():
    """测试无法获取 IP 时返回 unknown"""
    request = Mock()
    request.headers.get = lambda key: None
    request.client = None

    ip = LikeService.get_client_ip(request)
    assert ip == "unknown"


def test_get_client_ip_forwarded_multiple():
    """测试多个代理的 X-Forwarded-For"""
    request = Mock()
    request.headers.get = lambda key: "203.0.113.1, 198.51.100.1, 192.0.2.1" if key == "X-Forwarded-For" else None
    request.client = Mock(host="192.168.1.1")

    ip = LikeService.get_client_ip(request)
    # 应该返回第一个 IP（真实客户端 IP）
    assert ip == "203.0.113.1"
