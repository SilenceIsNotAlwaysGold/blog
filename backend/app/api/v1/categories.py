"""
Category API endpoints
"""
from fastapi import APIRouter, Depends, status
from typing import Optional
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)
from app.services.category import CategoryService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.response import success
from app.utils.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/categories", tags=["Categories"])


def category_to_response(category) -> CategoryResponse:
    """Convert Category model to CategoryResponse"""
    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        board=category.board,
        description=category.description,
        article_count=category.article_count,
        created_at=category.created_at.isoformat()
    )


@router.get("", response_model=dict)
async def get_categories(board: Optional[str] = None):
    """Get all categories, optionally filtered by board"""
    categories = await CategoryService.get_categories(board=board)
    items = [category_to_response(cat) for cat in categories]
    return success(data=items)


@router.get("/{category_id}", response_model=dict)
async def get_category(category_id: str):
    """Get category by ID"""
    category = await CategoryService.get_category_by_id(category_id)
    if not category:
        raise NotFoundException("Category not found")

    return success(data=category_to_response(category))


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new category (requires authentication)"""
    category = await CategoryService.create_category(category_data)
    return success(
        data=category_to_response(category),
        message="Category created successfully",
        code=201
    )


@router.put("/{category_id}", response_model=dict)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a category (requires authentication)"""
    category = await CategoryService.update_category(category_id, category_data)
    if not category:
        raise NotFoundException("Category not found")

    return success(
        data=category_to_response(category),
        message="Category updated successfully"
    )


@router.delete("/{category_id}", response_model=dict)
async def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a category (requires authentication)"""
    success_delete = await CategoryService.delete_category(category_id)
    if not success_delete:
        raise NotFoundException("Category not found")

    return success(message="Category deleted successfully")
