"""
Tests for response utilities
"""
import pytest
from app.utils.response import success, error, paginated_response


def test_success_response():
    """Test success response format"""
    response = success(data={"key": "value"}, message="操作成功")

    assert response["code"] == 200
    assert response["message"] == "操作成功"
    assert response["data"] == {"key": "value"}


def test_success_response_default():
    """Test success response with defaults"""
    response = success()

    assert response["code"] == 200
    assert response["message"] == "success"
    assert response["data"] is None


def test_success_response_custom_code():
    """Test success response with custom code"""
    response = success(data={"id": 1}, message="Created", code=201)

    assert response["code"] == 201
    assert response["message"] == "Created"
    assert response["data"] == {"id": 1}


def test_error_response():
    """Test error response format"""
    response = error(message="错误信息", code=400)

    assert response["code"] == 400
    assert response["message"] == "错误信息"
    assert "data" not in response


def test_error_response_with_details():
    """Test error response with details"""
    response = error(
        message="Validation error",
        code=422,
        details="Field 'email' is required"
    )

    assert response["code"] == 422
    assert response["message"] == "Validation error"
    assert response["details"] == "Field 'email' is required"


def test_paginated_response():
    """Test paginated response format"""
    items = [{"id": 1}, {"id": 2}, {"id": 3}]
    response = paginated_response(
        items=items,
        total=10,
        page=1,
        page_size=3
    )

    assert response["code"] == 200
    assert response["message"] == "success"
    assert response["data"]["items"] == items
    assert response["data"]["pagination"]["total"] == 10
    assert response["data"]["pagination"]["page"] == 1
    assert response["data"]["pagination"]["page_size"] == 3
    assert response["data"]["pagination"]["total_pages"] == 4
    assert response["data"]["pagination"]["has_next"] is True
    assert response["data"]["pagination"]["has_prev"] is False


def test_paginated_response_last_page():
    """Test paginated response for last page"""
    items = [{"id": 10}]
    response = paginated_response(
        items=items,
        total=10,
        page=4,
        page_size=3
    )

    assert response["data"]["pagination"]["has_next"] is False
    assert response["data"]["pagination"]["has_prev"] is True


def test_paginated_response_single_page():
    """Test paginated response with single page"""
    items = [{"id": 1}, {"id": 2}]
    response = paginated_response(
        items=items,
        total=2,
        page=1,
        page_size=10
    )

    assert response["data"]["pagination"]["total_pages"] == 1
    assert response["data"]["pagination"]["has_next"] is False
    assert response["data"]["pagination"]["has_prev"] is False
