export interface Poem {
  id: number
  title: string
  title_pinyin: string
  content: string
  author_name: string
  author_pinyin: string
  difficulty: number
  image_url?: string
}

export interface PaginatedResponse<T> {
  count: number
  total_pages: number
  current_page: number
  page_size: number
  has_next: boolean
  has_previous: boolean
  next_page: number | null
  previous_page: number | null
  results: T[]
}

export interface DailyRecommendations {
  date: string
  count: number
  results: Poem[]
}

export interface Category {
  code: string
  name: string
} 