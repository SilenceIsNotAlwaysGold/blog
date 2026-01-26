from typing import List, Optional
from beanie import PydanticObjectId
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


class SkillService:
    """技能服务类"""

    @staticmethod
    async def create_skill(skill_data: SkillCreate) -> Skill:
        """创建技能"""
        skill = Skill(**skill_data.model_dump())
        await skill.insert()
        return skill

    @staticmethod
    async def get_skill(skill_id: str) -> Optional[Skill]:
        """获取单个技能"""
        return await Skill.get(PydanticObjectId(skill_id))

    @staticmethod
    async def get_skills(
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Skill]:
        """获取技能列表"""
        query = Skill.find()

        if category:
            query = query.find(Skill.category == category)

        # 按 order 和创建时间排序
        skills = await query.sort(
            [(Skill.order, -1), (Skill.created_at, -1)]
        ).skip(skip).limit(limit).to_list()

        return skills

    @staticmethod
    async def get_skills_by_category() -> dict:
        """按分类获取技能（分组返回）"""
        skills = await Skill.find().sort(
            [(Skill.order, -1), (Skill.created_at, -1)]
        ).to_list()

        # 按分类分组
        grouped = {}
        for skill in skills:
            if skill.category not in grouped:
                grouped[skill.category] = []
            grouped[skill.category].append(skill)

        return grouped

    @staticmethod
    async def update_skill(skill_id: str, skill_data: SkillUpdate) -> Optional[Skill]:
        """更新技能"""
        skill = await Skill.get(PydanticObjectId(skill_id))
        if not skill:
            return None

        update_data = skill_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(skill, field, value)

        await skill.save()
        return skill

    @staticmethod
    async def delete_skill(skill_id: str) -> bool:
        """删除技能"""
        skill = await Skill.get(PydanticObjectId(skill_id))
        if not skill:
            return False

        await skill.delete()
        return True

    @staticmethod
    async def get_categories() -> List[str]:
        """获取所有技能分类"""
        skills = await Skill.find().to_list()
        categories = list(set(skill.category for skill in skills))
        return sorted(categories)
