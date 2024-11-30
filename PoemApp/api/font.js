import { request } from '@/utils/request'
import config from '@/config'

export const fontApi = {
  // 获取字体分类列表
  getFontCategories() {
    return request.request({
      url: `${config.baseUrl}/font-categories`,
      method: 'GET',
      custom: {
        showLoading: true,
        loadingMsg: '加载字体中...'
      }
    })
  },

  // 获取字体文件
  getFontFile(url) {
    return request.request({
      url,
      method: 'GET',
      responseType: 'blob',
      custom: {
        showError: false
      }
    })
  }
} 