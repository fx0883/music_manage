<script setup>
import { ref, onMounted } from 'vue'
import { useLanguageStore } from '@/stores/useLanguageStore'
import { poemApi } from '@/api/poem'

const languageStore = useLanguageStore()
const poem = ref(null)
const loading = ref(true)
const error = ref(null)
const currentTab = ref('正文')

// 标签页配置
const tabs = [
  { key: '正文', icon: 'file-text' },
  { key: '译文', icon: 'language' },
  { key: '注解', icon: 'info' },
  { key: '赏析', icon: 'star' },
  { key: '作者', icon: 'person' }
]

// 获取诗词详情
const fetchPoemDetail = async (id) => {
  loading.value = true
  error.value = null
  
  try {
    const response = await poemApi.getPoemDetail(id, languageStore.currentLanguage)
    poem.value = response
  } catch (err) {
    error.value = err.message || '加载失败'
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 处理返回
const handleBack = () => {
  uni.navigateBack()
}

// 处理分享
const handleShare = () => {
  uni.showShareMenu({
    withShareTicket: true
  })
}

// 处理收藏
const handleFavorite = () => {
  // TODO: 实现收藏功能
  uni.showToast({
    title: '收藏功能开发中',
    icon: 'none'
  })
}

// 切换标签页
const handleTabChange = (tab) => {
  currentTab.value = tab
}

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1]
  const { id } = currentPage.options
  
  if (id) {
    fetchPoemDetail(id)
  }
})
</script>

<template>
  <view class="poem-detail">
    <!-- 顶部导航栏 -->
    <view class="poem-detail__header">
      <view class="poem-detail__status-bar" />
      <view class="poem-detail__nav">
        <view class="poem-detail__back" @click="handleBack">
          <uni-icons type="left" size="24" color="#333" />
        </view>
        <view class="poem-detail__actions">
          <uni-icons type="star" size="24" color="#333" @click="handleFavorite" />
          <uni-icons type="redo" size="24" color="#333" @click="handleShare" />
        </view>
      </view>
    </view>
    
    <!-- 加载状态 -->
    <template v-if="loading">
      <LoadingState />
    </template>
    
    <!-- 错误状态 -->
    <template v-else-if="error">
      <view class="poem-detail__error">
        <uni-icons type="error" size="64" color="#ff5a5f" />
        <text>{{ error }}</text>
        <button @click="fetchPoemDetail">重试</button>
      </view>
    </template>
    
    <!-- 内容区域 -->
    <template v-else-if="poem">
      <scroll-view 
        class="poem-detail__content" 
        scroll-y
        :show-scrollbar="false"
        enhanced
        :bounces="true"
      >
        <!-- 诗词标题 -->
        <view class="poem-detail__title">
          <text class="poem-detail__title-text">{{ poem.title }}</text>
          <text class="poem-detail__title-pinyin">{{ poem.title_pinyin }}</text>
        </view>
        
        <!-- 作者信息 -->
        <view class="poem-detail__author">
          <text class="poem-detail__author-text">[{{ poem.type.name }}] {{ poem.author.name }}</text>
        </view>
        
        <!-- 标签页导航 -->
        <view class="poem-detail__tabs">
          <view 
            v-for="tab in tabs"
            :key="tab.key"
            class="poem-detail__tab"
            :class="{ 'poem-detail__tab--active': currentTab === tab.key }"
            @click="handleTabChange(tab.key)"
          >
            <uni-icons :type="tab.icon" size="20" :color="currentTab === tab.key ? '#3cc51f' : '#666'" />
            <text class="poem-detail__tab-text">{{ tab.key }}</text>
          </view>
        </view>
        
        <!-- 标签页内容 -->
        <view class="poem-detail__tab-content">
          <!-- 正文 -->
          <view v-if="currentTab === '正文'" class="poem-detail__section">
            <view class="poem-detail__content-text">{{ poem.content }}</view>
            <view class="poem-detail__pinyin">{{ poem.pinyin }}</view>
          </view>
          
          <!-- 译文 -->
          <view v-if="currentTab === '译文'" class="poem-detail__section">
            <text class="poem-detail__translation">{{ poem.interpretations.content }}</text>
          </view>
          
          <!-- 注解 -->
          <view v-if="currentTab === '注解'" class="poem-detail__section">
            <text class="poem-detail__annotations">{{ poem.annotations }}</text>
          </view>
          
          <!-- 赏析 -->
          <view v-if="currentTab === '赏析'" class="poem-detail__section">
            <text class="poem-detail__appreciation">{{ poem.appreciations }}</text>
          </view>
          
          <!-- 作者 -->
          <view v-if="currentTab === '作者'" class="poem-detail__section">
            <view class="poem-detail__author-info">
              <image 
                v-if="poem.author.image"
                :src="poem.author.image"
                mode="aspectFill"
                class="poem-detail__author-avatar"
              />
              <text class="poem-detail__author-name">{{ poem.author.name }}</text>
              <text class="poem-detail__author-intro">{{ poem.author.introduction }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </template>
  </view>
</template>

<style lang="scss">
.poem-detail {
  min-height: 100vh;
  background-color: #fff;
  
  &__header {
    background-color: #fff;
    border-bottom: 1rpx solid #eee;
  }
  
  &__status-bar {
    height: var(--status-bar-height);
  }
  
  &__nav {
    height: 44px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30rpx;
  }
  
  &__back {
    padding: 20rpx;
    margin-left: -20rpx;
  }
  
  &__actions {
    display: flex;
    gap: 40rpx;
  }
  
  &__content {
    height: calc(100vh - 44px - var(--status-bar-height));
  }
  
  &__title {
    padding: 40rpx 30rpx;
    text-align: center;
    
    &-text {
      font-size: 40rpx;
      color: #333;
      font-weight: 500;
      display: block;
      margin-bottom: 10rpx;
    }
    
    &-pinyin {
      font-size: 24rpx;
      color: #999;
    }
  }
  
  &__author {
    text-align: center;
    margin-bottom: 40rpx;
    
    &-text {
      font-size: 28rpx;
      color: #666;
    }
  }
  
  &__tabs {
    display: flex;
    justify-content: space-around;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #eee;
  }
  
  &__tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8rpx;
    padding: 10rpx 30rpx;
    
    &--active {
      color: #3cc51f;
    }
    
    &-text {
      font-size: 24rpx;
      color: inherit;
    }
  }
  
  &__tab-content {
    padding: 30rpx;
  }
  
  &__section {
    line-height: 1.8;
  }
  
  &__content-text {
    font-size: 32rpx;
    color: #333;
    margin-bottom: 20rpx;
  }
  
  &__pinyin {
    font-size: 24rpx;
    color: #999;
    margin-bottom: 40rpx;
  }
  
  &__translation,
  &__annotations,
  &__appreciation {
    font-size: 28rpx;
    color: #666;
  }
  
  &__author-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  &__author-avatar {
    width: 120rpx;
    height: 120rpx;
    border-radius: 50%;
    margin-bottom: 20rpx;
  }
  
  &__author-name {
    font-size: 32rpx;
    color: #333;
    margin-bottom: 20rpx;
  }
  
  &__author-intro {
    font-size: 28rpx;
    color: #666;
    text-align: justify;
  }
}
</style>