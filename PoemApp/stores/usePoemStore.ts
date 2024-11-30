import { defineStore } from 'pinia'
import { ref } from 'vue'
import { poemApi } from '@/api/poem'
import type { Poem } from '@/api/types'

export const usePoemStore = defineStore('poem', () => {
  const poems = ref<Poem[]>([])
  const currentPoem = ref<Poem | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const lastUpdateTime = ref(0)
  const retryCount = ref(0)
  const maxRetries = 3

  async function fetchRecommendations(language: string = 'zh') {
    const now = Date.now()
    if (lastUpdateTime.value + 5000 > now) {
      return
    }
    lastUpdateTime.value = now
    
    loading.value = true
    error.value = null
    
    try {
      const res = await poemApi.getDailyRecommendations(language)
      if (res && res.results) {
        poems.value = res.results
        retryCount.value = 0
      } else {
        throw new Error('返回数据格式错误')
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '未知错误'
      error.value = `获取推荐列表失败: ${errorMessage}`
      console.error(error.value)
      
      if (retryCount.value < maxRetries) {
        retryCount.value++
        const retryDelay = 1000 * retryCount.value
        
        uni.showToast({
          title: `加载失败，${retryCount.value}秒后重试...`,
          icon: 'none',
          duration: retryDelay
        })
        
        setTimeout(() => {
          fetchRecommendations(language)
        }, retryDelay)
      }
    } finally {
      loading.value = false
    }
  }

  function setCurrentPoem(poem: Poem) {
    currentPoem.value = poem
  }

  function reset() {
    poems.value = []
    currentPoem.value = null
    error.value = null
    retryCount.value = 0
  }

  return {
    poems,
    currentPoem,
    loading,
    error,
    fetchRecommendations,
    setCurrentPoem,
    reset
  }
}) 