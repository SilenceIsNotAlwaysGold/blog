from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project import ProjectService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.response import success, error

router = APIRouter(prefix="/projects", tags=["projects"])


def project_to_response(project) -> dict:
    """Convert Project model to response dict"""
    return ProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        tech_stack=project.tech_stack,
        cover_image=project.cover_image,
        demo_url=project.demo_url,
        github_url=project.github_url,
        start_date=project.start_date,
        end_date=project.end_date,
        status=project.status,
        highlights=project.highlights,
        order=project.order,
        created_at=project.created_at,
        updated_at=project.updated_at,
    ).model_dump()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """创建项目（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create projects"
        )

    project = await ProjectService.create_project(project_data)
    return success(
        data=project_to_response(project),
        message="Project created successfully"
    )


@router.get("", response_model=dict)
async def get_projects(
    status: Optional[str] = None,
    tech: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """获取项目列表（公开访问）"""
    projects = await ProjectService.get_projects(status, tech, skip, limit)

    result = [project_to_response(p) for p in projects]
    return success(data=result)


@router.get("/featured", response_model=dict)
async def get_featured_projects(limit: int = 6):
    """获取精选项目（公开访问）"""
    projects = await ProjectService.get_featured_projects(limit)
    result = [project_to_response(p) for p in projects]
    return success(data=result)


@router.get("/tech-stack", response_model=dict)
async def get_tech_stack():
    """获取所有技术栈列表（公开访问）"""
    tech_list = await ProjectService.get_tech_stack_list()
    return success(data=tech_list)


@router.get("/{project_id}", response_model=dict)
async def get_project(project_id: str):
    """获取单个项目（公开访问）"""
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return success(data=project_to_response(project))


@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新项目（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update projects"
        )

    project = await ProjectService.update_project(project_id, project_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return success(
        data=project_to_response(project),
        message="Project updated successfully"
    )


@router.delete("/{project_id}", response_model=dict)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """删除项目（需要管理员权限）"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete projects"
        )

    success_deleted = await ProjectService.delete_project(project_id)
    if not success_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return success(message="Project deleted successfully")
