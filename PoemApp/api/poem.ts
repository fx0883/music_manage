import { useRequest } from '@/utils/request'
import type { Poem, PaginatedResponse, DailyRecommendations } from './types'

const { request } = useRequest()

export const poemApi = {
  // 获取诗词列表
  getPoems(params: {
    page?: number
    page_size?: number
    language?: string
    poem_type?: string
    genre?: string
    difficulty?: number
    sort?: string
  }): Promise<PaginatedResponse<Poem>> {
    return request({
      url: '/chinese/api/poems/',
      params
    })
  },

  // 获取每日推荐
  getDailyRecommendations(language: string = 'zh'): Promise<DailyRecommendations> {
    return request({
      url: '/chinese/api/poems/daily_recommendations/',
      params: { language }
    })
  },

  // 获取随机背诵题目
  getRandomQuiz(): Promise<{
    poem_id: number
    poem_title: string
    quiz_line: string
    answer: Record<number, string>
  }> {
    return request({
      url: '/chinese/api/poems/random_quiz/'
    })
  }
} 