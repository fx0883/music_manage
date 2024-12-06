<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { usePoemStore } from '@/stores/usePoemStore'
import { useLanguageStore } from '@/stores/useLanguageStore'
import PoemSwipeCard from '@/components/PoemSwipeCard.vue'
import LoadingState from '@/components/LoadingState.vue'
import EmptyState from '@/components/EmptyState.vue'
import FontSelector from '@/components/FontSelector.vue'
import { debounce } from '@/utils/debounce'
import CardStyleSelector from '@/components/CardStyleSelector.vue'

// Store
const poemStore = usePoemStore()
const languageStore = useLanguageStore()

// 当前诗词索引
const currentIndex = ref(0)
const nextIndex = computed(() => {
  if (currentIndex.value < poemStore.poems.length - 1) {
    return currentIndex.value + 1
  }
  return null
})

// 计算边距
const margins = computed(() => {
  const paddingHeight = 150
  const systemInfo = uni.getSystemInfoSync()
  const screenHeight = systemInfo.screenHeight
  const statusBarHeight = systemInfo.statusBarHeight
  const navBarHeight = 44 // 导航栏固定高度
  const tabBarHeight = 50 // tabBar 固定高度
  
  // 计算卡片可用空间
  const availableHeight = screenHeight - statusBarHeight - navBarHeight - tabBarHeight
  
  // 计算合适的上下边距
  const topMargin = statusBarHeight + navBarHeight + 20
  const bottomMargin = tabBarHeight + 20
  
  // 计算左右边距 (根据屏幕宽度的比例)
  const sideMargin = Math.floor(systemInfo.screenWidth * 0.2) // 屏幕宽度的10%
  
  return {
    top: topMargin + paddingHeight,
    bottom: bottomMargin + paddingHeight,
    left: sideMargin,
    right: sideMargin
  }
})

// 处理滑动
const handleSwipe = (direction) => {

}

// 处理动画完成
const handleAnimationComplete = (isAnimating) => {
  console.log('Animation state:', isAnimating)
  if (isAnimating &&currentIndex.value < poemStore.poems.length - 1) {
    currentIndex.value++
  }
}

// 状态管理
const showSettings = ref(false)
const currentFont = ref({
  name: '默认字体',
  fontFamily: 'SimSun'
})
const fontSize = ref(16)
const cardFontSize = ref(42)
const showFontSelector = ref(false)
const popup = ref(null)
const fontPopup = ref(null)
const cardStylePopup = ref(null)

// 字体大小变化处理
const handleFontSizeChange = debounce((e) => {
  const size = e.detail.value
  fontSize.value = size
  cardFontSize.value = Math.floor(36 + ((size - 12) / 12) * 12)
  
  uni.setStorageSync('poem-font-size', {
    slider: size,
    actual: cardFontSize.value
  })
}, 100)

// 设置选项
const settingItems = [
  { title: '字体切换', value: currentFont.value, type: 'font', showArrow: true },
  { title: '卡片样式', type: 'card', showArrow: true },
  { title: '练字模式', type: 'practice', showArrow: true },
  { title: '浏览记录', type: 'history', showArrow: true }
]

// 事件处理
const handleSettingClick = (type) => {
  if (type === 'font') {
    popup.value?.close()
    setTimeout(() => {
      fontPopup.value?.open()
    }, 100)
  } else if (type === 'card') {
    popup.value?.close()
    nextTick(async () => {
      await new Promise(resolve => setTimeout(resolve, 100))
      cardStylePopup.value?.open()
    })
  }
}

const handleFontSelect = (font) => {
  currentFont.value = font
  fontPopup.value?.close()
  uni.setStorageSync('poem-font', {
    name: font.name,
    fontFamily: font.fontFamily
  })
}

const handleMoreClick = () => {
  popup.value?.open()
}

// 滚动锁定
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

// 弹出层状态变化
const handlePopupChange = (e) => {
  console.log('Popup change:', e.show)
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

// 添加背景样式状态
const currentBackground = ref(null)

// 处理背景选择
const handleBackgroundSelect = (background) => {
  if (background.id === 'none') {
    currentBackground.value = null
    uni.removeStorageSync('poem-background')
  } else {
    currentBackground.value = background
    uni.setStorageSync('poem-background', background)
  }
  cardStylePopup.value?.close()
}

// 处理卡片样式弹窗关闭
const handleCardStyleClose = () => {
  console.log('关闭卡片样式弹窗')
  if (cardStylePopup.value) {
    cardStylePopup.value.close()
  }
}

// 初始化
onMounted(async () => {
  languageStore.initLanguage()
  await poemStore.fetchRecommendations(languageStore.currentLanguage)
  
  try {
    const savedFont = uni.getStorageSync('poem-font')
    if (savedFont) {
      currentFont.value = savedFont
    }
    const savedFontSize = uni.getStorageSync('poem-font-size')
    if (savedFontSize) {
      fontSize.value = savedFontSize.slider
      cardFontSize.value = savedFontSize.actual
    }
    const savedBackground = uni.getStorageSync('poem-background')
    if (savedBackground) {
      currentBackground.value = savedBackground
    }
  } catch (error) {
    console.error('Failed to restore settings:', error)
  }
})
</script>

<template>
  <view class="poems">
    <!-- 顶工具栏 -->
    <view class="poems__header">
      <view class="poems__status-bar" />
      <view class="poems__nav">
        <text class="poems__title">全部</text>
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
    </view>
    
    <!-- 内容区域 -->
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
          :top-margin="margins.top"
          :bottom-margin="margins.bottom"
          :left-margin="margins.left"
          :right-margin="margins.right"
          :font-family="currentFont.fontFamily"
          :font-size="cardFontSize"
		  :background-image="currentBackground?.image_url"
          class="poems__next-card"
        />
        
        <!-- 当前卡片 -->
        <PoemSwipeCard
          v-if="poemStore.poems[currentIndex]"
          :poem="poemStore.poems[currentIndex]"
          :is-top="true"
          :background-image="currentBackground?.image_url"
          :font-family="currentFont.fontFamily"
          :font-size="cardFontSize"
		  :top-margin="margins.top"
		  :bottom-margin="margins.bottom"
		  :left-margin="margins.left"
		  :right-margin="margins.right"
          @swipe="handleSwipe"
          @animation-complete="handleAnimationComplete"
          class="poems__current-card"
        />
      </template>
    </view>


  </view>
  
  <!-- 设置弹出层 -->
  <uni-popup 
    ref="popup" 
    type="bottom"
    :show="showSettings"
    :mask-click="true"
    :safe-area="true"
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
          <text 
            v-if="item.type === 'font'" 
            class="settings__value"
          >{{ currentFont.name }}</text>
          <uni-icons 
            v-if="item.showArrow" 
            type="right" 
            size="16" 
            color="#999" 
          />
        </view>
      </view>
  
      <!-- 字体大小块 -->
      <view class="settings__item">
        <text class="settings__title">字体大小</text>
        <view class="settings__slider-container">
          <slider 
            :value="fontSize" 
            @change="handleFontSizeChange"
            min="18"
            max="32"
            :step="1"
            show-value
            class="settings__slider"
            :block-size="20"
            block-color="#3cc51f"
            active-color="#3cc51f"
            background-color="#eee"
          />
        </view>
      </view>
      <view class="settings__safe-area"></view>
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
    <view class="font-popup">
      <scroll-view 
        scroll-y 
        class="font-popup__scroll"
        @touchmove.stop
      >
        <FontSelector
          v-model="currentFont.name"
          @select="handleFontSelect"
        />
      </scroll-view>
      <view class="font-popup__safe-area"></view>
    </view>
  </uni-popup>
  
  <!-- 添加卡片样式弹出层 -->
  <uni-popup 
    ref="cardStylePopup" 
    type="bottom" 
    :mask-click="true"
    :safe-area="true"
    @change="handlePopupChange"
  >
    <view class="card-style-popup">
      <CardStyleSelector
        :current-style="currentBackground"
        @select="handleBackgroundSelect"
        @close="handleCardStyleClose"
      />
      <view class="card-style-popup__safe-area"></view>
    </view>
  </uni-popup>
</template>

<style lang="scss">
.poems {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f8f8;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  
  &__header {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    background-color: #fff;
    border-bottom: 1rpx solid #eee;
    box-sizing: border-box;
    z-index: 10;
    flex-shrink: 0;
	padding: 0 30rpx 0 50rpx;
  }
  
  &__status-bar {
    width: 100%;
    height: var(--status-bar-height);
  }
  
  &__nav {
    width: 100%;
    height: 44px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40rpx;
  }
  
  &__title {
    font-size: 32rpx;
    color: #333;
    font-weight: 500;
  }
  
  &__tools {
    display: flex;
    gap: 40rpx;
  }
  
  &__content {
    flex: 1;
    position: relative;
    background-color: #f8f8f8;
    box-sizing: border-box;
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
  background-color: #fff;
  padding: 30rpx;
  box-sizing: border-box;
  position: relative;
  z-index: 999;
  
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
  
  &__slider-container {
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 0 0 30rpx;
  }
  
  &__slider {
    flex: 1;
    margin: 0;
  }
  
  &__safe-area {
    height: constant(safe-area-inset-bottom);
    height: env(safe-area-inset-bottom);
    width: 100%;
  }
}

.font-popup {
  width: 100%;
  height: 60vh;
  background-color: #fff;
  position: relative;
  z-index: 999;
  display: flex;
  flex-direction: column;
  
  &__scroll {
    flex: 1;
    height: 0;
    touch-action: pan-y;
    -webkit-overflow-scrolling: touch;
    overflow-y: auto;
    overscroll-behavior: contain;
  }
  
  &__safe-area {
    height: constant(safe-area-inset-bottom);
    height: env(safe-area-inset-bottom);
    width: 100%;
    background-color: #fff;
  }
}

.card-style-popup {
  width: 100%;
  height: 378rpx;
  background-color: #fff;
  position: relative;
  z-index: 999;
  display: flex;
  flex-direction: column;
  
  &__safe-area {
    height: constant(safe-area-inset-bottom);
    height: env(safe-area-inset-bottom);
    width: 100%;
    background-color: #fff;
  }
}

/* uni-popup 样式覆盖 */
:deep(.uni-popup) {
  z-index: 99999 !important;
}

:deep(.uni-popup__mask) {
  z-index: 99998 !important;
  background-color: rgba(0, 0, 0, 0.6) !important;
}

:deep(.uni-popup__wrapper) {
  z-index: 99999 !important;
  max-height: 90vh !important;
  overflow: hidden !important;
  
  &.bottom {
    bottom: 0 !important;
    padding-bottom: constant(safe-area-inset-bottom) !important;
    padding-bottom: env(safe-area-inset-bottom) !important;
    animation: popup-bottom 0.2s ease-out;
  }
}

@keyframes popup-bottom {
  0% { transform: translateY(100%); }
  100% { transform: translateY(0); }
}
</style> 