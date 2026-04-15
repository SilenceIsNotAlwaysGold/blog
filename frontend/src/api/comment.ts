import request from '@/utils/request'

export interface Comment {
  id: string
  article_id: string
  user_id: string
  username: string
  content: string
  parent_id?: string
  created_at: string
  updated_at: string
  is_deleted: boolean
  replies: Comment[]
}

export interface CommentListResponse {
  total: number
  comments: Comment[]
}

/**
 * 创建评论
 */
export const createComment = (articleId: string, data: { content: string; parent_id?: string }) => {
  return request({
    url: `/comments/${articleId}`,
    method: 'post',
    data
  })
}

/**
 * 获取文章评论列表
 */
export const getArticleComments = (articleId: string, params?: { skip?: number; limit?: number }) => {
  return request<{ data: CommentListResponse }>({
    url: `/comments/${articleId}`,
    method: 'get',
    params
  })
}

/**
 * 更新评论
 */
export const updateComment = (commentId: string, data: { content: string }) => {
  return request({
    url: `/comments/${commentId}`,
    method: 'put',
    data
  })
}

/**
 * 删除评论
 */
export const deleteComment = (commentId: string) => {
  return request<{ data: null }>({
    url: `/comments/${commentId}`,
    method: 'delete'
  })
}

/**
 * 获取评论数量
 */
export const getCommentCount = (articleId: string) => {
  return request<{ data: { count: number } }>({
    url: `/comments/${articleId}/count`,
    method: 'get'
  })
}
