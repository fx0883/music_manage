<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { poemApi } from '@/api/poem'
import PoemSwipeCard from '@/components/PoemSwipeCard.vue'
import LoadingState from '@/components/LoadingState.vue'
import EmptyState from '@/components/EmptyState.vue'
import type { Poem } from '@/api/types'
import { storeToRefs } from 'pinia'
import { useLanguageStore } from '@/stores/useLanguageStore'
import FontSelector from '@/components/FontSelector.vue'

// 添加错误处理相关的状态
const error = ref<string | null>(null)
const retryCount = ref(0)
const maxRetries = 3

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

// 优化的获取推荐诗词函数
const fetchRecommendations = async (language: string = 'zh') => {
  loading.value = true
  error.value = null
  
  try {
    const res = await poemApi.getDailyRecommendations(language)
    if (res && res.results) {
      poems.value = res.results
      retryCount.value = 0 // 成功后重置重试次数
    } else {
      throw new Error('返回数据格式错误')
    }
  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : '未知错误'
    error.value = `获取推荐列表失败: ${errorMessage}`
    console.error(error.value, err)
    
    // 自动重试机制
    if (retryCount.value < maxRetries) {
      retryCount.value++
      const retryDelay = 1000 * retryCount.value // 递增延迟时间
      
      uni.showToast({
        title: `加载失败，${retryCount.value}秒后重试...`,
        icon: 'none',
        duration: retryDelay
      })
      
      setTimeout(() => {
        fetchRecommendations(language)
      }, retryDelay)
    } else {
      // 达到最大重试次数
      uni.showModal({
        title: '提示',
        content: '加载失败，是否重试？',
        success: (res) => {
          if (res.confirm) {
            retryCount.value = 0 // 重置重试次数
            fetchRecommendations(language)
          }
        }
      })
    }
  } finally {
    loading.value = false
  }
}

// 添加错误重试按钮的处理函数
const handleRetry = () => {
  retryCount.value = 0
  fetchRecommendations()
}

// 添加动画状态控制
const isAnimating = ref(false)

// 处理动画完成事件
const handleAnimationComplete = () => {
  isAnimating.value = false
}

// 修改滑动处理函数
const handleSwipe = (direction: 'left' | 'right') => {
  if (isAnimating.value) return
  
  isAnimating.value = true
  if (direction === 'left' && currentIndex.value < poems.value.length - 1) {
    currentIndex.value++
  } else if (direction === 'right' && currentIndex.value > 0) {
    currentIndex.value--
  }
}

// 弹出层控制
const showSettings = ref(false)
const currentFont = ref('文悦古体仿宋')

// 设置选项
const settingItems = [
  { 
    title: '字体切换',
    value: currentFont.value,
    type: 'font',
    showArrow: true 
  },
  { 
    title: '卡片样式',
    type: 'card',
    showArrow: true 
  },
  { 
    title: '练字模式',
    type: 'practice',
    showArrow: true 
  },
  { 
    title: '浏览记录',
    type: 'history',
    showArrow: true 
  }
]

// 字体大小控制
const fontSize = ref(16)

// 字体选择弹出层控制
const showFontSelector = ref(false)

// 添加 fontPopup 的引用
const fontPopup = ref<any>(null)

// 修改处理设置项点击的方法
const handleSettingClick = (type: string) => {
  if (type === 'font') {
    // 先关闭设置弹窗
    popup.value?.close()
    // 延迟一下再打开字体选择弹窗，避免动画冲突
    setTimeout(() => {
      fontPopup.value?.open()
    }, 100)
  }
  console.log('Setting clicked:', type)
}

// 修改字体选择处理方法
const handleFontSelect = (font: any) => {
  currentFont.value = font.name
  fontPopup.value?.close()
}

// 添加 popup 的引用
const popup = ref<any>(null)

// 修改 handleMoreClick 方法
const handleMoreClick = () => {
  // 使用 popup 的 open 方法打开弹出层
  popup.value?.open()
}

// 优化的滚动锁定函数
const lockScroll = (lock: boolean) => {
  // #ifdef H5
  const body = document.querySelector('body')
  if (!body) return
  
  if (lock) {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop
    body.style.cssText = `
      position: fixed;
      width: 100%;
      top: -${scrollTop}px;
      overflow: hidden;
      touch-action: none;
    `
    body.dataset.scrollTop = String(scrollTop)
  } else {
    const scrollTop = Number(body.dataset.scrollTop) || 0
    body.style.cssText = ''
    document.documentElement.scrollTop = document.body.scrollTop = scrollTop
  }
  // #endif
  
  // #ifdef MP
  if (lock) {
    uni.pageScrollTo({
      scrollTop: 0,
      duration: 0
    })
  }
  // #endif
}

// 优化的弹出层状态管理
const handlePopupChange = (e: { show: boolean }) => {
  showFontSelector.value = e.show
  lockScroll(e.show)
  
  // 处理弹出层显示/隐藏的过渡效果
  if (e.show) {
    // 显示弹出层时的处理
    uni.vibrateShort() // 添加触感反馈
  } else {
    // 隐藏弹出层时的处理
    setTimeout(() => {
      // 确保过渡动画完成后再解锁滚动
      lockScroll(false)
    }, 300)
  }
}

onMounted(() => {
  // languageStore = useLanguageStore()
  // languageStore.initLanguage()
  fetchRecommendations()
})
</script>

<template>
  <view 
    class="poems"
    @touchmove.stop
  >
    <!-- 顶工具栏 -->
    <view class="poems__header">
      <text class="poems__all">全部</text>
      <view class="poems__tools">
        <uni-icons type="star" size="24" color="#333" />
        <uni-icons type="search" size="24" color="#333" />
        <uni-icons type="compose" size="24" color="#333" />
        <uni-icons type="upload" size="24" color="#333" />
        <uni-icons 
          type="more-filled" 
          size="24" 
          color="#333"
          @click="handleMoreClick"
        />
      </view>
    </view>
    
    <!-- 卡片区域 -->
    <view class="poems__content">
      <template v-if="loading">
        <LoadingState />
      </template>
      
      <template v-else-if="error">
        <view class="poems__error">
          <uni-icons type="error" size="64" color="#ff5a5f" />
          <text class="poems__error-text">{{ error }}</text>
          <button 
            class="poems__retry-btn"
            @click="handleRetry"
          >
            重试
          </button>
        </view>
      </template>
      
      <template v-else-if="!poems.length">
        <EmptyState text="暂无诗词" />
      </template>
      
      <template v-else >
        <!-- 下一张卡片 -->
        <PoemSwipeCard
          v-if="nextIndex !== null"
          :poem="poems[nextIndex]"
          :is-top="false"
          class="poems__next-card"
        />
        
        <!-- 当前卡片 -->
        <PoemSwipeCard
          v-if="poems[currentIndex]"
          :poem="poems[currentIndex]"
          :is-top="true"
          @swipe="handleSwipe"
          @animation-complete="handleAnimationComplete"
          class="poems__current-card"
        />
      </template>
    </view>

    <!-- 修改 popup 组件 -->
    <uni-popup 
      ref="popup" 
      type="bottom"
      :show="showSettings"
      @change="handlePopupChange"
    >
      <view class="settings">
        <view 
          v-for="item in settingItems" 
          :key="item.type"
          class="settings__item"
          @click="handleSettingClick(item.type)"
        >
          <text class="settings__title">{{ item.title }}</text>
          <view class="settings__right">
            <text v-if="item.value" class="settings__value">{{ item.value }}</text>
            <uni-icons v-if="item.showArrow" type="right" size="16" color="#999" />
          </view>
        </view>

        <!-- 字体大小滑块 -->
        <view class="settings__item">
          <text class="settings__title">字体大小</text>
          <slider 
            :value="fontSize" 
            @change="e => fontSize = e.detail.value"
            min="12"
            max="24"
            show-value
            class="settings__slider"
          />
        </view>
      </view>
    </uni-popup>

    <!-- 修改字体选择弹出层 -->
    <uni-popup
      ref="fontPopup"
      type="bottom"
      :mask-click="true"
      :safe-area="true"
      @change="handlePopupChange"
    >
      <view class="font-popup" @touchmove.stop>
        <scroll-view 
          scroll-y 
          class="font-popup__scroll"
          @touchmove.stop
        >
          <FontSelector
            v-model="currentFont"
            @select="handleFontSelect"
          />
        </scroll-view>
        <view class="font-popup__safe-area"></view>
      </view>
    </uni-popup>
  </view>
</template>

<style lang="scss">
.poems {
  min-height: 100vh;
  background-color: #f8f8f8;
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 100%;
  height: 100%;
  overflow: hidden;
  touch-action: none;
  
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
    z-index: 1;
  }
  
  &__current-card {
    z-index: 2;
  }

  &__error {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40rpx;
    
    &-text {
      margin: 20rpx 0;
      font-size: 28rpx;
      color: #666;
      text-align: center;
    }
  }
  
  &__retry-btn {
    margin-top: 20rpx;
    padding: 20rpx 60rpx;
    background-color: #3cc51f;
    color: #fff;
    border-radius: 8rpx;
    font-size: 28rpx;
    
    &:active {
      opacity: 0.8;
    }
  }
}

.settings {
  width: 100%;
  height: 45vh;
  background-color: #fff;
  padding: 30rpx;
  box-sizing: border-box;
  
  &__item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30rpx 0;
    border-bottom: 1rpx solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
  }
  
  &__title {
    font-size: 28rpx;
    color: #333;
  }
  
  &__right {
    display: flex;
    align-items: center;
    gap: 10rpx;
  }
  
  &__value {
    font-size: 26rpx;
    color: #999;
  }
  
  &__slider {
    flex: 1;
    margin: 0 20rpx;
  }
}

.font-popup {
  width: 100%;
  height: 60vh;
  background-color: #fff;
  position: relative;
  z-index: 100;
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
  animation: slideUp 0.3s ease-out;
  
  &__scroll {
    height: 100%;
    touch-action: pan-y;
    -webkit-overflow-scrolling: touch;
    overflow-y: auto;
    overscroll-behavior: contain;
    
    &::-webkit-scrollbar {
      display: none;
    }
  }
  
  &__safe-area {
    height: 50px;
    width: 100%;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* 修改 uni-popup 的样式 */
:deep(.uni-popup) {
  z-index: 999 !important;
}

:deep(.uni-popup__mask) {
  z-index: 998 !important;
}

:deep(.uni-tabbar) {
  z-index: 997 !important;
}

:deep(.uni-popup__wrapper) {
  overflow-y: auto !important;
  -webkit-overflow-scrolling: touch !important;
}
</style> 