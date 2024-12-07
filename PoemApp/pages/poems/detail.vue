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
  { key: '正文', icon: 'eye' },
  { key: '译文', icon: 'eye-filled' },
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
const handleListen = () => {
  // TODO: 实现收藏功能
  uni.showToast({
    title: '听书功能开发中',
    icon: 'none'
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

// 添加处理诗句的方法
const formatPoem = (content, pinyin) => {
  if (!content || !pinyin) return []
  
  // 按换行符分割内容和拼音
  const contentLines = content.split('\n')
  const pinyinLines = pinyin.split('\n')
  
  // 进一步按标点符号分割每行
  return contentLines.map((line, index) => {
    // 分割当前行的内容和拼音
    const segments = line.split(/([，。、；：？！,.;:?!])/).filter(Boolean)
    const currentPinyin = pinyinLines[index] || ''
    
    // 组合成行对象
    return {
      text: line,
      pinyin: currentPinyin,
      segments: segments
    }
  })
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
		  <uni-icons type="headphones" size="24" color="#333" @click="handleListen" />
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
        <!-- 标题部分只在非作者tab时显示 -->
        <view v-if="currentTab !== '作者'" class="poem-detail__title">
          <text class="poem-detail__title-pinyin">{{ poem.title_pinyin }}</text>
          <text class="poem-detail__title-text">{{ poem.title }}</text>
        </view>
        
        <!-- 正文部分改动 -->
        <view v-if="currentTab === '正文'" class="poem-detail__section">
          <view v-if="poem.banner_image_url" class="poem-detail__banner">
            <image 
              :src="poem.banner_image_url" 
              mode="aspectFill" 
              class="poem-detail__banner-image"
            />
          </view>
          <view class="poem-detail__lines">
            <view 
              v-for="(line, index) in formatPoem(poem.content, poem.pinyin)" 
              :key="index"
              class="poem-detail__line"
            >
              <text class="poem-detail__line-pinyin">{{ line.pinyin }}</text>
              <view class="poem-detail__line-segments">
                <text 
                  v-for="(segment, segIndex) in line.segments"
                  :key="segIndex"
                  class="poem-detail__segment"
                >{{ segment }}</text>
              </view>
            </view>
          </view>
        </view>
        
        <!-- 译文 -->
        <view v-if="currentTab === '译文'" class="poem-detail__section">
          <view class="poem-detail__card">
            <view class="poem-detail__card-title">
              <uni-icons type="info" size="16" color="#666" />
              <text>译文</text>
            </view>
            <view class="poem-detail__card-content">
              <text v-for="(line, index) in (poem.interpretations?.content || '').split('\n')" 
                    :key="index" 
                    class="poem-detail__translation-line"
              >{{ line }}</text>
            </view>
          </view>
        </view>
        
        <!-- 注解 -->
        <view v-if="currentTab === '注解'" class="poem-detail__section">
          <view class="poem-detail__card">
            <view class="poem-detail__card-title">
              <uni-icons type="help" size="16" color="#666" />
              <text>注释</text>
            </view>
            <view class="poem-detail__card-content">
              <view v-for="(note, index) in (poem.annotations || '').split('\\')" 
                    :key="index"
                    class="poem-detail__note"
              >
                <text class="poem-detail__note-text">{{ note ? note.trim() : '' }}</text>
              </view>
            </view>
          </view>
        </view>
        
        <!-- 赏析 -->
        <view v-if="currentTab === '赏析'" class="poem-detail__section">
          <view class="poem-detail__card">
            <view class="poem-detail__card-title">
              <uni-icons type="star" size="16" color="#666" />
              <text>赏析</text>
            </view>
            <view class="poem-detail__card-content">
              <text class="poem-detail__appreciation-text">{{ poem.appreciations || '' }}</text>
            </view>
          </view>
        </view>
        
        <!-- 作者 -->
        <view v-if="currentTab === '作者'" class="poem-detail__section">
          <view class="poem-detail__author-card">
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
      </scroll-view>
      
      <!-- 底部导航 -->
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
    </template>
  </view>
</template>

<style lang="scss">
.poem-detail {
  min-height: 100vh;
  background-color: #f8f8f8;
  
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
    height: calc(100vh - 44px - var(--status-bar-height) - 120rpx);
    padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
  }
  
  &__title {
    padding: 40rpx 30rpx;
    text-align: center;
    
    &-pinyin {
      font-size: 24rpx;
      color: #999;
      margin-bottom: 10rpx;
      display: block;
    }
    
    &-text {
      font-size: 40rpx;
      color: #333;
      font-weight: 500;
      display: block;
    }
  }
  
  &__banner {
    width: 100%;
    height: 300rpx;
    overflow: hidden;
    margin-bottom: 40rpx;
    
    &-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
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
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 16rpx 30rpx;
    background-color: #fff;
    border-top: 1rpx solid #eee;
    z-index: 100;
  }
  
  &__tab {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6rpx;
    min-width: 100rpx;
    padding: 10rpx;
    
    &--active {
      color: #3cc51f;
    }
    
    &-text {
      font-size: 24rpx;
      color: inherit;
      white-space: nowrap;
    }
  }
  
  &__tab-content {
    padding: 30rpx;
  }
  
  &__section {
    margin: 20rpx 0;
    padding: 30rpx;
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
  
  &__lines {
    padding: 0;
  }
  
  &__line {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 40rpx;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    &-pinyin {
      font-size: 24rpx;
      color: #999;
      margin-bottom: 8rpx;
      text-align: center;
    }
    
    &-segments {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
    }
  }
  
  &__segment {
    font-size: 32rpx;
    color: #333;
    line-height: 1.5;
    padding: 0 4rpx;
  }
  
  &__translation-line {
    display: block;
    font-size: 32rpx;
    color: #666;
    line-height: 1.8;
    margin-bottom: 20rpx;
    
    &:last-child {
      margin-bottom: 0;
    }
  }

  &__note {
    margin-bottom: 20rpx;
    
    &-text {
      font-size: 32rpx;
      color: #666;
      line-height: 1.8;
    }
  }

  &__appreciation-text {
    font-size: 32rpx;
    color: #666;
    line-height: 1.8;
    text-align: justify;
  }

  &__author-card {
    padding: 40rpx;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    
    .poem-detail__author-avatar {
      width: 160rpx;
      height: 160rpx;
      border-radius: 50%;
      margin-bottom: 30rpx;
      border: 6rpx solid #fff;
      box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
    }
    
    .poem-detail__author-name {
      font-size: 36rpx;
      color: #333;
      font-weight: 500;
      margin-bottom: 10rpx;
    }
    
    .poem-detail__author-dynasty {
      font-size: 24rpx;
      color: #999;
      margin-bottom: 30rpx;
    }
    
    .poem-detail__author-intro {
      font-size: 32rpx;
      color: #666;
      line-height: 1.8;
      text-align: justify;
    }
  }
}
</style>