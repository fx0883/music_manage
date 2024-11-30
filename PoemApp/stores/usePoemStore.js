import { defineStore } from 'pinia'
import { ref } from 'vue'
import { poemApi } from '@/api/poem'

export const usePoemStore = defineStore('poem', () => {
  const poems = ref([])
  const currentPoem = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const lastUpdateTime = ref(0)
  const retryCount = ref(0)
  const maxRetries = 3

  async function fetchRecommendations(language = 'zh') {
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
      error.value = err.message
      retryCount.value++
      
      if (retryCount.value < maxRetries) {
        const retryDelay = Math.min(1000 * Math.pow(2, retryCount.value), 5000)
        
        setTimeout(() => {
          fetchRecommendations(language)
        }, retryDelay)
      }
    } finally {
      loading.value = false
    }
  }

  function setCurrentPoem(poem) {
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