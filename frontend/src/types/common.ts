/**
 * Common TypeScript type definitions
 */

// API Response
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// Pagination
export interface Pagination {
  total: number
  page: number
  page_size: number
  total_pages: number
  has_next: boolean
  has_prev: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  pagination: Pagination
}

// Query parameters
export interface QueryParams {
  page?: number
  page_size?: number
  [key: string]: any
}
