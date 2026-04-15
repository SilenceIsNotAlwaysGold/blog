import request from '@/utils/request'
import type { ApiResponse } from '@/types/common'

export interface Category {
  id: string
  name: string
  board: string
  description: string | null
  article_count: number
  created_at: string
}

export interface CategoryCreate {
  name: string
  board: string
  description?: string
}

export interface CategoryUpdate {
  name?: string
  description?: string
}

export function getCategories(board?: string): Promise<ApiResponse<Category[]>> {
  return request({
    url: '/categories',
    method: 'get',
    params: { board }
  })
}

export function getCategory(id: string): Promise<ApiResponse<Category>> {
  return request({
    url: `/categories/${id}`,
    method: 'get'
  })
}

export function createCategory(data: CategoryCreate): Promise<ApiResponse<Category>> {
  return request({
    url: '/categories',
    method: 'post',
    data
  })
}

export function updateCategory(id: string, data: CategoryUpdate): Promise<ApiResponse<Category>> {
  return request({
    url: `/categories/${id}`,
    method: 'put',
    data
  })
}

export function deleteCategory(id: string): Promise<ApiResponse<void>> {
  return request({
    url: `/categories/${id}`,
    method: 'delete'
  })
}
