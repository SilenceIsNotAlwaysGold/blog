from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse
from app.services.skill import SkillService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.skill import Skill
from app.utils.response import success, error

router = APIRouter(prefix="/skills", tags=["skills"])


def skill_to_dict(skill: Skill) -> dict:
    """将 Skill 对象转换为字典"""
    return {
        "id": str(skill.id),
        "name": skill.name,
        "category": skill.category,
        "proficiency": skill.proficiency,
        "description": skill.description,
        "icon": skill.icon,
        "order": skill.order,
        "created_at": skill.created_at,
        "updated_at": skill.updated_at
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_user)
):
    """创建技能（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create skills"
        )

    skill = await SkillService.create_skill(skill_data)
    return success(
        data=skill_to_dict(skill),
        message="Skill created successfully"
    )


@router.get("", response_model=dict)
async def get_skills(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """获取技能列表（公开访问）"""
    skills = await SkillService.get_skills(category, skip, limit)
    return success(data=[skill_to_dict(s) for s in skills])


@router.get("/grouped", response_model=dict)
async def get_skills_grouped():
    """按分类获取技能（公开访问）"""
    grouped = await SkillService.get_skills_by_category()

    # 转换为响应格式
    result = {}
    for category, skills in grouped.items():
        result[category] = [skill_to_dict(s) for s in skills]

    return success(data=result)


@router.get("/categories", response_model=dict)
async def get_categories():
    """获取所有技能分类（公开访问）"""
    categories = await SkillService.get_categories()
    return success(data=categories)


@router.get("/{skill_id}", response_model=dict)
async def get_skill(skill_id: str):
    """获取单个技能（公开访问）"""
    skill = await SkillService.get_skill(skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return success(data=skill_to_dict(skill))


@router.put("/{skill_id}", response_model=dict)
async def update_skill(
    skill_id: str,
    skill_data: SkillUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新技能（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update skills"
        )

    skill = await SkillService.update_skill(skill_id, skill_data)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return success(
        data=SkillResponse.model_validate(skill).model_dump(),
        message="Skill updated successfully"
    )


@router.delete("/{skill_id}", response_model=dict)
async def delete_skill(
    skill_id: str,
    current_user: User = Depends(get_current_user)
):
    """删除技能（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete skills"
        )

    success_deleted = await SkillService.delete_skill(skill_id)
    if not success_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    return success(message="Skill deleted successfully")
