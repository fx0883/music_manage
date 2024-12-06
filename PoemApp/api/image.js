import { request } from '@/utils/request'
import config from '@/config'

export const imageApi = {
  // 获取指定分类的图片列表
  getCategoryImages(category = 'card_background') {
    return request.request({
      url: `${config.baseUrl}/images/category/`,
      method: 'GET',
      data: { category },
      custom: {
        showLoading: true,
        loadingMsg: '加载图片中...'
      }
    })
  }
} 