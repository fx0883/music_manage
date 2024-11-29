import { request } from '@/utils/request'
import type { Author, PaginatedResponse } from './types'

export const authorApi = {
  // 获取作者列表
  getAuthors: (page: number = 1) => {
    return request<PaginatedResponse<Author>>({
      url: 'chinese/api/authors/',
      method: 'GET',
      data: { page },
      custom: {
        showLoading: true,
        loadingMsg: '加载作者列表...'
      }
    })
  },

  // 获取作者详情
  getAuthorDetail: (id: number) => {
    return request<Author>({
      url: `chinese/api/authors/${id}/`,
      method: 'GET'
    })
  }
} 