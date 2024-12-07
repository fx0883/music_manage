import { request } from '@/utils/request'
import config from '@/config'

export const poemApi = {
  // 获取每日推荐
  getDailyRecommendations(language = 'zh') {
    return request.request({
      url: `${config.baseUrl}/poems/daily_recommendations/`,
      method: 'GET',
      data: { language },
      retryTimes: 3,
      retryDelay: 1000,
      custom: {
        showLoading: true,
        loadingMsg: '加载推荐中...'
      }
    })
  },

  // 获取诗词详情
  getPoemDetail(id, language = 'zh') {
    return request.request({
      url: `${config.baseUrl}/poems/${id}/`,
      method: 'GET',
      data: { language },
      custom: {
        showLoading: true,
        loadingMsg: '加载诗词详情...'
      }
    })
  }
} 