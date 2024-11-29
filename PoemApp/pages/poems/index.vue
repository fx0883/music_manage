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

// 处理弹出层状态变化
const handlePopupChange = (e: { show: boolean }) => {
  showFontSelector.value = e.show
  // 当弹出层显示时，禁止底部页面滚动
  if (e.show) {
    document.body.style.overflow = 'hidden'
    document.body.style.position = 'fixed'
    document.body.style.width = '100%'
  } else {
    document.body.style.overflow = ''
    document.body.style.position = ''
    document.body.style.width = ''
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

    <!-- 修改 popup 组件 -->
    <uni-popup 
      ref="popup" 
      type="bottom"
      :show="showSettings"
      @change="(e) => showSettings = e.show"
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
      <view class="font-popup">
        <scroll-view 
          scroll-y 
          class="font-popup__scroll"
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
  padding-bottom: constant(safe-area-inset-bottom); /* iOS 11.2+ */
  padding-bottom: env(safe-area-inset-bottom); /* iOS 11.2+ */
  
  &__scroll {
    height: 100%;
    touch-action: pan-y;
    -webkit-overflow-scrolling: touch;
  }
  
  &__safe-area {
    height: 50px; /* tabbar 的高度 */
    width: 100%;
  }
}

/* 修改 uni-popup 的样式 */
:deep(.uni-popup) {
  /* 确保弹出层在 tabbar 上方 */
  z-index: 999 !important;
}

:deep(.uni-popup__mask) {
  /* 确保遮罩在 tabbar 上方 */
  z-index: 998 !important;
}

/* 修改 tabbar 的样式 */
:deep(.uni-tabbar) {
  /* 确保 tabbar 始终可见 */
  z-index: 997 !important;
}
</style> 