/**
 * Article API
 */
import request from '@/utils/request'
import type { ApiResponse, PaginatedResponse } from '@/types/common'

export interface Article {
  id: string
  title: string
  content: string
  summary: string | null
  board: 'life' | 'tech'
  category_id: string | null
  tags: string[]
  author_id: string
  cover_image: string | null
  view_count: number
  like_count: number
  is_published: boolean
  published_at: string | null
  created_at: string
  updated_at: string
}

export interface ArticleQuery {
  board?: 'life' | 'tech'
  category_id?: string
  tag?: string
  is_published?: boolean
  page?: number
  page_size?: number
}

export interface ArticleCreate {
  title: string
  content: string
  summary?: string
  board: 'life' | 'tech'
  category_id?: string
  tags?: string[]
  cover_image?: string
  is_published?: boolean
}

export interface ArticleUpdate {
  title?: string
  content?: string
  summary?: string
  category_id?: string
  tags?: string[]
  cover_image?: string
  is_published?: boolean
}

/**
 * Get articles list
 */
export function getArticles(params: ArticleQuery): Promise<ApiResponse<PaginatedResponse<Article>>> {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}

/**
 * Get article by ID
 */
export function getArticle(id: string): Promise<ApiResponse<Article>> {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}

/**
 * Create article
 */
export function createArticle(data: ArticleCreate): Promise<ApiResponse<Article>> {
  return request({
    url: '/articles',
    method: 'post',
    data
  })
}

/**
 * Update article
 */
export function updateArticle(id: string, data: ArticleUpdate): Promise<ApiResponse<Article>> {
  return request({
    url: `/articles/${id}`,
    method: 'put',
    data
  })
}

/**
 * Delete article
 */
export function deleteArticle(id: string): Promise<ApiResponse<void>> {
  return request({
    url: `/articles/${id}`,
    method: 'delete'
  })
}

/**
 * Search articles
 */
export function searchArticles(keyword: string, page = 1, page_size = 10): Promise<ApiResponse<PaginatedResponse<Article>>> {
  return request({
    url: '/articles/search',
    method: 'post',
    data: { keyword },
    params: { page, page_size }
  })
}
