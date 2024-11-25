<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { poemApi } from '@/api/poem'
import PoemSwipeCard from '@/components/PoemSwipeCard.vue'
import LoadingState from '@/components/LoadingState.vue'
import EmptyState from '@/components/EmptyState.vue'
import type { Poem } from '@/api/types'
import { storeToRefs } from 'pinia'
import { useLanguageStore } from '@/stores/useLanguageStore'

const poems = ref<Poem[]>([])
const currentIndex = ref(0)
const loading = ref(false)
let languageStore: ReturnType<typeof useLanguageStore>

// 计算下一张卡片的索引
const nextIndex = computed(() => {
  if (currentIndex.value < poems.value.length - 1) {
    return currentIndex.value + 1
  }
  return null
})

// 获取推荐诗词
const fetchRecommendations = async (language: string = 'zh') => {
  loading.value = true
  try {
    const res = await poemApi.getDailyRecommendations(language)
    if (res && res.results) {
      poems.value = res.results
    }
  } catch (error) {
    console.error('获取推荐列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理滑动事件
const handleSwipe = (direction: 'left' | 'right') => {
  if (direction === 'left' && currentIndex.value < poems.value.length - 1) {
    currentIndex.value++
  } else if (direction === 'right' && currentIndex.value > 0) {
    currentIndex.value--
  }
}

onMounted(() => {
  // languageStore = useLanguageStore()
  // languageStore.initLanguage()
  fetchRecommendations()
})
</script>

<template>
  <view class="poems">
    <!-- 顶部工具栏 -->
    <view class="poems__header">
      <text class="poems__all">全部</text>
      <view class="poems__tools">
        <uni-icons type="star" size="24" color="#333" />
        <uni-icons type="search" size="24" color="#333" />
        <uni-icons type="compose" size="24" color="#333" />
        <uni-icons type="upload" size="24" color="#333" />
        <uni-icons type="more-filled" size="24" color="#333" />
      </view>
    </view>
    
    <!-- 卡片区域 -->
    <view class="poems__content">
      <template v-if="loading">
        <LoadingState />
      </template>
      
      <template v-else-if="!poems.length">
        <EmptyState text="暂无诗词" />
      </template>
      
      <template v-else >
        <!-- 下一张卡片（如果存在） -->
        <PoemSwipeCard
          v-if="nextIndex !== null"
          :poem="poems[nextIndex]"
          class="poems__next-card"
        />
        
        <!-- 当前卡片 -->
        <PoemSwipeCard
          v-if="poems[currentIndex]"
          :poem="poems[currentIndex]"
          @swipe="handleSwipe"
          class="poems__current-card"
        />
      </template>
    </view>
  </view>
</template>

<style lang="scss">
.poems {
  min-height: 100vh;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  
  &__header {
    padding: 20rpx 40rpx;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    border-bottom: 1rpx solid #eee;
  }
  
  &__all {
    font-size: 32rpx;
    color: #333;
  }
  
  &__tools {
    display: flex;
    gap: 40rpx;
  }
  
  &__content {
    flex: 1;
    position: relative;
    background-color: #f8f8f8;
    overflow: hidden;
  }
  
  &__next-card {
    z-index: 1;  // 确保在当前卡片下方
  }
  
  &__current-card {
    z-index: 2;  // 确保在最上层
  }
}
</style> 