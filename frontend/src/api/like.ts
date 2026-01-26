import request from '@/utils/request'

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
export const toggleLike = (articleId: string) => {
  return request<{ data: LikeResponse }>({
    url: `/likes/${articleId}`,
    method: 'post'
  })
}

/**
 * 检查点赞状态
 */
export const checkLikeStatus = (articleId: string) => {
  return request<{ data: LikeStatus }>({
    url: `/likes/${articleId}/status`,
    method: 'get'
  })
}

/**
 * 获取点赞数
 */
export const getLikeCount = (articleId: string) => {
  return request<{ data: LikeCount }>({
    url: `/likes/${articleId}/count`,
    method: 'get'
  })
}
