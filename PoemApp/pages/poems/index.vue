<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePoemStore } from '@/stores/usePoemStore'
import { useLanguageStore } from '@/stores/useLanguageStore'
import PoemSwipeCard from '@/components/PoemSwipeCard.vue'
import LoadingState from '@/components/LoadingState.vue'
import EmptyState from '@/components/EmptyState.vue'
import FontSelector from '@/components/FontSelector.vue'

// Store
const poemStore = usePoemStore()
const languageStore = useLanguageStore()

// 当前诗词索引
const currentIndex = ref(0)

// 计算下一张卡片的索引
const nextIndex = computed(() => {
  if (currentIndex.value < poemStore.poems.length - 1) {
    return currentIndex.value + 1
  }
  return null
})

// 动画状态控制
const isAnimating = ref(false)

// 处理动画完成事件
const handleAnimationComplete = () => {
  isAnimating.value = false
}

// 处理滑动
const handleSwipe = (direction) => {
  if (isAnimating.value) return
  
  isAnimating.value = true
  if (direction === 'left' && currentIndex.value < poemStore.poems.length - 1) {
    currentIndex.value++
  } else if (direction === 'right' && currentIndex.value > 0) {
    currentIndex.value--
  }
}

// 弹出层控制
const showSettings = ref(false)
const currentFont = ref('文悦古体仿宋')
const fontSize = ref(16)
const showFontSelector = ref(false)

// 弹出层引用
const popup = ref(null)
const fontPopup = ref(null)

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

// 处理设置项点击
const handleSettingClick = (type) => {
  if (type === 'font') {
    popup.value?.close()
    setTimeout(() => {
      fontPopup.value?.open()
    }, 100)
  }
}

// 处理字体选择
const handleFontSelect = (font) => {
  currentFont.value = font.name
  fontPopup.value?.close()
}

// 处理更多按钮点击
const handleMoreClick = () => {
  popup.value?.open()
}

// 优化的滚动锁定函数
const lockScroll = (lock) => {
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

// 处理弹出层状态变化
const handlePopupChange = (e) => {
  showFontSelector.value = e.show
  lockScroll(e.show)
  
  if (e.show) {
    uni.vibrateShort()
  } else {
    setTimeout(() => {
      lockScroll(false)
    }, 300)
  }
}

// 初始化
onMounted(async () => {
  languageStore.initLanguage()
  await poemStore.fetchRecommendations(languageStore.currentLanguage)
})
</script>

<template>
  <view class="poems" @touchmove.stop>
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
      <template v-if="poemStore.loading">
        <LoadingState />
      </template>
      
      <template v-else-if="poemStore.error">
        <view class="poems__error">
          <uni-icons type="error" size="64" color="#ff5a5f" />
          <text class="poems__error-text">{{ poemStore.error }}</text>
          <button 
            class="poems__retry-btn"
            @click="poemStore.fetchRecommendations(languageStore.currentLanguage)"
          >
            重试
          </button>
        </view>
      </template>
      
      <template v-else-if="!poemStore.poems.length">
        <EmptyState text="暂无诗词" />
      </template>
      
      <template v-else>
        <!-- 下一张卡片 -->
        <PoemSwipeCard
          v-if="nextIndex !== null"
          :poem="poemStore.poems[nextIndex]"
          :is-top="false"
          class="poems__next-card"
        />
        
        <!-- 当前卡片 -->
        <PoemSwipeCard
          v-if="poemStore.poems[currentIndex]"
          :poem="poemStore.poems[currentIndex]"
          :is-top="true"
          @swipe="handleSwipe"
          @animation-complete="handleAnimationComplete"
          class="poems__current-card"
        />
      </template>
    </view>

    <!-- 设置弹出层 -->
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

    <!-- 字体选择弹出层 -->
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