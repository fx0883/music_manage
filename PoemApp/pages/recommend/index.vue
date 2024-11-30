<script setup>
import { ref, onMounted } from 'vue'
import PoemCard from '@/components/PoemCard.vue'
import { poemApi } from '@/api/poem'

const recommendations = ref([])
const loading = ref(false)

const fetchRecommendations = async () => {
  loading.value = true
  try {
    const res = await poemApi.getDailyRecommendations('zh')
    recommendations.value = res.results
  } catch (error) {
    console.error('获取推荐列表失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecommendations()
})
</script>

<template>
  <view class="recommend">
    <view class="recommend__header">
      <text class="recommend__title">每日推荐</text>
      <text class="recommend__subtitle">每天20首精选诗词</text>
    </view>
    
    <view class="recommend__list">
      <template v-if="loading">
        <view class="recommend__loading">加载中...</view>
      </template>
      
      <template v-else>
        <PoemCard
          v-for="poem in recommendations"
          :key="poem.id"
          :title="poem.title"
          :author="poem.author_name"
          :content="poem.content"
          :image-url="poem.image_url"
          :difficulty="poem.difficulty"
          @click="() => {}"
        />
      </template>
    </view>
  </view>
</template>

<style lang="scss">
.recommend {
  min-height: 100vh;
  background-color: #f5f5f5;
  
  &__header {
    padding: 40rpx;
    background-color: #fff;
  }
  
  &__title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
  }
  
  &__subtitle {
    font-size: 28rpx;
    color: #666;
    margin-top: 8rpx;
    display: block;
  }
  
  &__list {
    padding: 20rpx 0;
  }
  
  &__loading {
    text-align: center;
    padding: 40rpx;
    color: #999;
  }
}
</style> 