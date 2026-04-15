import request from '@/utils/request'

export interface Skill {
  id: string
  name: string
  category: string
  proficiency: number
  description?: string
  icon?: string
  order: number
  created_at: string
  updated_at: string
}

export interface SkillCreate {
  name: string
  category: string
  proficiency: number
  description?: string
  icon?: string
  order?: number
}

export interface SkillUpdate {
  name?: string
  category?: string
  proficiency?: number
  description?: string
  icon?: string
  order?: number
}

export interface SkillsGrouped {
  [category: string]: Skill[]
}

/**
 * 获取技能列表
 */
export const getSkills = (params?: { category?: string; skip?: number; limit?: number }) => {
  return request({
    url: '/skills',
    method: 'get',
    params
  })
}

/**
 * 获取分组的技能
 */
export const getSkillsGrouped = () => {
  return request({
    url: '/skills/grouped',
    method: 'get'
  })
}

/**
 * 获取所有技能分类
 */
export const getCategories = () => {
  return request({
    url: '/skills/categories',
    method: 'get'
  })
}

/**
 * 获取单个技能
 */
export const getSkill = (id: string) => {
  return request({
    url: `/skills/${id}`,
    method: 'get'
  })
}

/**
 * 创建技能
 */
export const createSkill = (data: SkillCreate) => {
  return request({
    url: '/skills',
    method: 'post',
    data
  })
}

/**
 * 更新技能
 */
export const updateSkill = (id: string, data: SkillUpdate) => {
  return request({
    url: `/skills/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除技能
 */
export const deleteSkill = (id: string) => {
  return request({
    url: `/skills/${id}`,
    method: 'delete'
  })
}
