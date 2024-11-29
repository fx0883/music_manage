import { request } from '@/utils/request'
import type { FontCategory } from '@/types/font'

export const fontApi = {
  // 获取字体分类列表
  getFontCategories: () => {
    return request<FontCategory[]>({
      url: '/font-categories/',
      method: 'GET',
      custom: {
        showLoading: true,
        loadingMsg: '加载字体中...'
      }
    })
  },

  // 获取字体文件
  getFontFile: (url: string) => {
    return request<Blob>({
      url,
      method: 'GET',
      responseType: 'blob',
      custom: {
        showError: false
      }
    })
  }
} 