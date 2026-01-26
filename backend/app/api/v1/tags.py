"""
Tag API endpoints
"""
from fastapi import APIRouter, Depends, status
from app.schemas.category import TagCreate, TagUpdate, TagResponse
from app.services.category import TagService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.response import success
from app.utils.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/tags", tags=["Tags"])


def tag_to_response(tag) -> TagResponse:
    """Convert Tag model to TagResponse"""
    return TagResponse(
        id=str(tag.id),
        name=tag.name,
        article_count=tag.article_count,
        created_at=tag.created_at.isoformat()
    )


@router.get("", response_model=dict)
async def get_tags():
    """Get all tags"""
    tags = await TagService.get_tags()
    items = [tag_to_response(tag) for tag in tags]
    return success(data=items)


@router.get("/{tag_id}", response_model=dict)
async def get_tag(tag_id: str):
    """Get tag by ID"""
    tag = await TagService.get_tag_by_id(tag_id)
    if not tag:
        raise NotFoundException("Tag not found")

    return success(data=tag_to_response(tag))


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new tag (requires authentication)"""
    tag = await TagService.create_tag(tag_data)
    return success(
        data=tag_to_response(tag),
        message="Tag created successfully",
        code=201
    )


@router.put("/{tag_id}", response_model=dict)
async def update_tag(
    tag_id: str,
    tag_data: TagUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a tag (requires authentication)"""
    tag = await TagService.update_tag(tag_id, tag_data)
    if not tag:
        raise NotFoundException("Tag not found or name already exists")

    return success(
        data=tag_to_response(tag),
        message="Tag updated successfully"
    )


@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(
    tag_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a tag (requires authentication)"""
    success_delete = await TagService.delete_tag(tag_id)
    if not success_delete:
        raise NotFoundException("Tag not found")

    return success(message="Tag deleted successfully")
