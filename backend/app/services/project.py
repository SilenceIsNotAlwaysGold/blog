from typing import List, Optional
from beanie import PydanticObjectId
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """项目服务类"""

    @staticmethod
    async def create_project(project_data: ProjectCreate) -> Project:
        """创建项目"""
        project = Project(**project_data.model_dump())
        await project.insert()
        return project

    @staticmethod
    async def get_project(project_id: str) -> Optional[Project]:
        """获取单个项目"""
        return await Project.get(PydanticObjectId(project_id))

    @staticmethod
    async def get_projects(
        status: Optional[str] = None,
        tech: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """获取项目列表"""
        query = Project.find()

        if status:
            query = query.find(Project.status == status)

        if tech:
            # 技术栈包含指定技术
            query = query.find(Project.tech_stack == tech)

        # 按 order 和开始日期排序
        projects = await query.sort(
            [(Project.order, -1), (Project.start_date, -1)]
        ).skip(skip).limit(limit).to_list()

        return projects

    @staticmethod
    async def get_featured_projects(limit: int = 6) -> List[Project]:
        """获取精选项目（按 order 排序，取前 N 个）"""
        projects = await Project.find(
            Project.status == "completed"
        ).sort(
            [(Project.order, -1), (Project.start_date, -1)]
        ).limit(limit).to_list()

        return projects

    @staticmethod
    async def update_project(project_id: str, project_data: ProjectUpdate) -> Optional[Project]:
        """更新项目"""
        project = await Project.get(PydanticObjectId(project_id))
        if not project:
            return None

        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        await project.save()
        return project

    @staticmethod
    async def delete_project(project_id: str) -> bool:
        """删除项目"""
        project = await Project.get(PydanticObjectId(project_id))
        if not project:
            return False

        await project.delete()
        return True

    @staticmethod
    async def get_tech_stack_list() -> List[str]:
        """获取所有使用过的技术栈"""
        projects = await Project.find().to_list()
        tech_set = set()
        for project in projects:
            tech_set.update(project.tech_stack)

        return sorted(list(tech_set))
