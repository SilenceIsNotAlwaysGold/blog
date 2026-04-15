import request from '@/utils/request'
import type { ApiResponse } from '@/types/common'

export interface LikeResponse {
  action: 'liked' | 'unliked'
  like_count: number
}

export interface LikeStatus {
  is_liked: boolean
}

export interface LikeCount {
  like_count: number
}

/**
 * 切换点赞状态
 */
export const toggleLike = (articleId: string): Promise<ApiResponse<LikeResponse>> => {
  return request({
    url: `/likes/${articleId}`,
    method: 'post'
  })
}

/**
 * 检查点赞状态
 */
export const checkLikeStatus = (articleId: string): Promise<ApiResponse<LikeStatus>> => {
  return request({
    url: `/likes/${articleId}/status`,
    method: 'get'
  })
}

/**
 * 获取点赞数
 */
export const getLikeCount = (articleId: string): Promise<ApiResponse<LikeCount>> => {
  return request({
    url: `/likes/${articleId}/count`,
    method: 'get'
  })
}
