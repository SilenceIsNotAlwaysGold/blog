import request from '@/utils/request'

export interface Project {
  id: string
  name: string
  description: string
  tech_stack: string[]
  cover_image?: string
  demo_url?: string
  github_url?: string
  start_date?: string
  end_date?: string
  status: 'completed' | 'in_progress' | 'planned'
  highlights?: string[]
  order: number
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  description: string
  tech_stack: string[]
  cover_image?: string
  demo_url?: string
  github_url?: string
  start_date?: string
  end_date?: string
  status?: string
  highlights?: string[]
  order?: number
}

export interface ProjectUpdate {
  name?: string
  description?: string
  tech_stack?: string[]
  cover_image?: string
  demo_url?: string
  github_url?: string
  start_date?: string
  end_date?: string
  status?: string
  highlights?: string[]
  order?: number
}

/**
 * 获取项目列表
 */
export const getProjects = (params?: {
  status?: string
  tech?: string
  skip?: number
  limit?: number
}) => {
  return request({
    url: '/projects',
    method: 'get',
    params
  })
}

/**
 * 获取精选项目
 */
export const getFeaturedProjects = (limit: number = 6) => {
  return request({
    url: '/projects/featured',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取技术栈列表
 */
export const getTechStack = () => {
  return request({
    url: '/projects/tech-stack',
    method: 'get'
  })
}

/**
 * 获取单个项目
 */
export const getProject = (id: string) => {
  return request({
    url: `/projects/${id}`,
    method: 'get'
  })
}

/**
 * 创建项目
 */
export const createProject = (data: ProjectCreate) => {
  return request({
    url: '/projects',
    method: 'post',
    data
  })
}

/**
 * 更新项目
 */
export const updateProject = (id: string, data: ProjectUpdate) => {
  return request({
    url: `/projects/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除项目
 */
export const deleteProject = (id: string) => {
  return request({
    url: `/projects/${id}`,
    method: 'delete'
  })
}
