import { useRequest } from '@/utils/request'
import type { Poem, DailyRecommendations } from './types'

const { request } = useRequest()

export const poemApi = {
  // 获取每日推荐
  getDailyRecommendations(language: string = 'zh'): Promise<DailyRecommendations> {
    return request({
      url: '/chinese/api/poems/daily_recommendations/',
      params: { language }
    })
  }
} 