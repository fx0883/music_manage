import { request } from '@/utils/request'
import type { Poem, DailyRecommendations } from './types'

export const poemApi = {
  // 获取每日推荐
	getDailyRecommendations(language : string = 'zh') : Promise<DailyRecommendations> {
    return request<DailyRecommendations>({
      url: '/poems/daily_recommendations/',
      method: 'GET',
      data: { language },
      custom: {
        showLoading: true,
        loadingMsg: '加载推荐中...'
      }
    })
  },

  // 获取诗词详情
  getPoemDetail(id: number): Promise<Poem> {
    return request<Poem>({
      url: `/poems/${id}/`,
      method: 'GET'
    })
  }
} 