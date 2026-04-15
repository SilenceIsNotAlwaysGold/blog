import request from '@/utils/request'

export interface About {
  id: string
  content: string
  updated_at: string
}

export interface AboutUpdate {
  content: string
}

/**
 * 获取 About 页面内容
 */
export const getAbout = () => {
  return request({
    url: '/about',
    method: 'get'
  })
}

/**
 * 更新 About 页面内容
 */
export const updateAbout = (data: AboutUpdate) => {
  return request({
    url: '/about',
    method: 'put',
    data
  })
}
