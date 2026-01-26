"""
Unified response utilities
"""
from typing import Any, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """Standard API response model"""
    code: int
    message: str
    data: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {}
            }
        }


def success(data: Any = None, message: str = "success", code: int = 200) -> dict:
    """
    Create a success response

    Args:
        data: Response data
        message: Success message
        code: HTTP status code (default: 200)

    Returns:
        dict: Formatted response
    """
    return {
        "code": code,
        "message": message,
        "data": data
    }


def error(message: str, code: int = 400, details: Optional[str] = None) -> dict:
    """
    Create an error response

    Args:
        message: Error message
        code: HTTP status code (default: 400)
        details: Additional error details

    Returns:
        dict: Formatted error response
    """
    response = {
        "code": code,
        "message": message
    }

    if details:
        response["details"] = details

    return response


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "success"
) -> dict:
    """
    Create a paginated response

    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Number of items per page
        message: Success message

    Returns:
        dict: Formatted paginated response
    """
    total_pages = (total + page_size - 1) // page_size

    return success(
        data={
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        },
        message=message
    )
