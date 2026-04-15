"""
Category and Tag services
"""
from typing import Optional, List
from bson import ObjectId
from app.models.category import Category
from app.models.tag import Tag
from app.schemas.category import CategoryCreate, CategoryUpdate, TagCreate, TagUpdate


class CategoryService:
    """Category service"""

    @staticmethod
    async def create_category(category_data: CategoryCreate) -> Category:
        """Create a new category"""
        category = Category(
            name=category_data.name,
            board=category_data.board,
            description=category_data.description
        )
        await category.insert()
        return category

    @staticmethod
    async def get_category_by_id(category_id: str) -> Optional[Category]:
        """Get category by ID"""
        try:
            return await Category.get(ObjectId(category_id))
        except Exception:
            return None

    @staticmethod
    async def get_categories(board: Optional[str] = None) -> List[Category]:
        """Get all categories, optionally filtered by board"""
        query = {}
        if board:
            query["board"] = board

        return await Category.find(query).to_list()

    @staticmethod
    async def update_category(
        category_id: str,
        category_data: CategoryUpdate
    ) -> Optional[Category]:
        """Update a category"""
        category = await CategoryService.get_category_by_id(category_id)
        if not category:
            return None

        update_data = category_data.model_dump(exclude_unset=True)
        await category.set(update_data)
        return category

    @staticmethod
    async def delete_category(category_id: str) -> bool:
        """Delete a category"""
        category = await CategoryService.get_category_by_id(category_id)
        if not category:
            return False

        await category.delete()
        return True


class TagService:
    """Tag service"""

    @staticmethod
    async def create_tag(tag_data: TagCreate) -> Tag:
        """Create a new tag"""
        # Check if tag already exists
        existing_tag = await Tag.find_one(Tag.name == tag_data.name)
        if existing_tag:
            return existing_tag

        tag = Tag(name=tag_data.name)
        await tag.insert()
        return tag

    @staticmethod
    async def get_tag_by_id(tag_id: str) -> Optional[Tag]:
        """Get tag by ID"""
        try:
            return await Tag.get(ObjectId(tag_id))
        except Exception:
            return None

    @staticmethod
    async def get_tag_by_name(name: str) -> Optional[Tag]:
        """Get tag by name"""
        return await Tag.find_one(Tag.name == name)

    @staticmethod
    async def get_tags() -> List[Tag]:
        """Get all tags"""
        return await Tag.find().sort("-article_count").to_list()

    @staticmethod
    async def update_tag(tag_id: str, tag_data: TagUpdate) -> Optional[Tag]:
        """Update a tag"""
        tag = await TagService.get_tag_by_id(tag_id)
        if not tag:
            return None

        # Check if new name already exists
        if tag_data.name != tag.name:
            existing_tag = await Tag.find_one(Tag.name == tag_data.name)
            if existing_tag:
                return None

        tag.name = tag_data.name
        await tag.save()
        return tag

    @staticmethod
    async def delete_tag(tag_id: str) -> bool:
        """Delete a tag"""
        tag = await TagService.get_tag_by_id(tag_id)
        if not tag:
            return False

        await tag.delete()
        return True

    @staticmethod
    async def update_tag_counts(tags_to_add: List[str], tags_to_remove: List[str]):
        """Update tag counts"""
        # Handle tags to add
        for tag_name in tags_to_add:
            tag = await Tag.find_one(Tag.name == tag_name)
            if tag:
                tag.article_count += 1
                await tag.save()
            else:
                tag = Tag(name=tag_name, article_count=1)
                await tag.insert()
        
        # Handle tags to remove
        for tag_name in tags_to_remove:
            tag = await Tag.find_one(Tag.name == tag_name)
            if tag:
                tag.article_count = max(0, tag.article_count - 1)
                await tag.save()
