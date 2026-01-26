import request from '@/utils/request'
import type { Article } from './article'
import type { Skill } from './skill'
import type { Project } from './project'

export interface GlobalSearchResult {
  articles: Article[]
  skills: Skill[]
  projects: Project[]
  total: number
}

export interface PopularTag {
  tag: string
  count: number
}

/**
 * 搜索文章
 */
export const searchArticles = (params: { q: string; board?: string; limit?: number }) => {
  return request<{ data: Article[] }>({
    url: '/search/articles',
    method: 'get',
    params
  })
}

/**
 * 搜索技能
 */
export const searchSkills = (params: { q: string; limit?: number }) => {
  return request<{ data: Skill[] }>({
    url: '/search/skills',
    method: 'get',
    params
  })
}

/**
 * 搜索项目
 */
export const searchProjects = (params: { q: string; limit?: number }) => {
  return request<{ data: Project[] }>({
    url: '/search/projects',
    method: 'get',
    params
  })
}

/**
 * 全局搜索
 */
export const globalSearch = (params: { q: string; limit?: number }) => {
  return request<{ data: GlobalSearchResult }>({
    url: '/search/global',
    method: 'get',
    params
  })
}

/**
 * 获取搜索建议
 */
export const getSearchSuggestions = (params: { q: string; limit?: number }) => {
  return request<{ data: string[] }>({
    url: '/search/suggestions',
    method: 'get',
    params
  })
}

/**
 * 获取热门标签
 */
export const getPopularTags = (params?: { limit?: number }) => {
  return request<{ data: PopularTag[] }>({
    url: '/search/tags/popular',
    method: 'get',
    params
  })
}

/**
 * 获取相关文章
 */
export const getRelatedArticles = (articleId: string, params?: { limit?: number }) => {
  return request<{ data: Article[] }>({
    url: `/search/articles/${articleId}/related`,
    method: 'get',
    params
  })
}
