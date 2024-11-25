import { ref } from 'vue'
import { defineStore } from 'pinia'
import { poemApi } from '@/api/poem'
import type { Poem } from '@/api/types'

export const usePoemStore = defineStore('poem', () => {
  const poems = ref<Poem[]>([])
  const loading = ref(false)
  const currentPage = ref(1)
  const hasMore = ref(true)
  
  async function fetchPoems(params = {}) {
    if (loading.value) return
    
    loading.value = true
    try {
      const res = await poemApi.getPoems({
        page: currentPage.value,
        ...params
      })
      
      poems.value = currentPage.value === 1 
        ? res.results 
        : [...poems.value, ...res.results]
        
      hasMore.value = res.has_next
      currentPage.value++
    } catch (error) {
      console.error('获取诗词列表失败:', error)
    } finally {
      loading.value = false
    }
  }
  
  function reset() {
    poems.value = []
    currentPage.value = 1
    hasMore.value = true
  }
  
  return {
    poems,
    loading,
    hasMore,
    fetchPoems,
    reset
  }
}) 