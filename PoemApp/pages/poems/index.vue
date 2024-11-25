<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRequest } from '@/utils/request'
import PoemSwipeCard from '@/components/PoemSwipeCard.vue'
import type { Poem } from '@/api/types'

const { request, loading } = useRequest()
const poems = ref<Poem[]>([])
const currentIndex = ref(0)
const touchStartX = ref(0)
const slideOffset = ref(0)
const isAnimating = ref(false)

// 获取推荐诗词
const fetchRecommendations = async () => {
  try {
    const res = await request({
      url: '/chinese/api/poems/daily_recommendations/',
      params: { language: 'zh' }
    })
    poems.value = res.results
  } catch (error) {
    console.error('获取推荐列表失败:', error)
  }
}

// 处理滑动
const handleTouchStart = (event: any) => {
  if (isAnimating.value) return
  touchStartX.value = event.touches[0].clientX
}

const handleTouchMove = (event: any) => {
  if (isAnimating.value) return
  const deltaX = event.touches[0].clientX - touchStartX.value
  
  // 限制滑动方向
  if ((currentIndex.value === 0 && deltaX > 0) || 
      (currentIndex.value === poems.value.length - 1 && deltaX < 0)) {
    slideOffset.value = deltaX * 0.2
  } else {
    slideOffset.value = deltaX
  }
}

const handleTouchEnd = () => {
  if (isAnimating.value) return
  
  const threshold = 80 // 降低滑动阈值使动画更容易触发
  const screenWidth = uni.getSystemInfoSync().windowWidth
  
  if (Math.abs(slideOffset.value) > threshold) {
    // 滑动距离足够，触发切换动画
    isAnimating.value = true
    const direction = slideOffset.value > 0 ? 1 : -1
    
    // 设置飞出动画的终点位置
    slideOffset.value = direction * screenWidth * 1.5 // 增加飞出距离
    
    // 等待动画完成后重置状态
    setTimeout(() => {
      currentIndex.value -= direction
      slideOffset.value = 0
      isAnimating.value = false
    }, 500) // 匹配动画持续时间
  } else {
    // 回弹动画
    isAnimating.value = true
    slideOffset.value = 0
    setTimeout(() => {
      isAnimating.value = false
    }, 500)
  }
}

onMounted(() => {
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
    <view 
      class="poems__content"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <template v-if="loading">
        <view class="poems__loading">
          <uni-icons type="spinner-cycle" size="24" color="#999" />
          <text>加载中...</text>
        </view>
      </template>
      
      <template v-else>
        <PoemSwipeCard
          v-if="poems.length > 0"
          :poem="poems[currentIndex]"
          :slide-offset="slideOffset"
          :is-animating="isAnimating"
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
    background-color: #fff;
    overflow: hidden;
  }
  
  &__loading {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    
    text {
      margin-top: 20rpx;
      font-size: 28rpx;
      color: #999;
    }
  }
}
</style> 