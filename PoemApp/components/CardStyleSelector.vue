<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { imageApi } from '@/api/image'

const props = defineProps({
  currentStyle: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['select', 'close'])

// 背景图片列表
const backgrounds = ref([])
const loading = ref(false)
const error = ref(null)
const loadedImages = ref(new Set())
const isReady = ref(false)

// 获取背景图片列表
const fetchBackgrounds = async () => {
  loading.value = true
  try {
    console.log('开始获取背景图片列表')
    const result = await imageApi.getCategoryImages()
    console.log('获取背景图片结果:', result)
    if (result?.images) {
      backgrounds.value = result.images
      console.log('背景图片列表已更新:', backgrounds.value)
      await nextTick()
      await nextTick()
      isReady.value = true
    }
  } catch (err) {
    error.value = '获取背景图片失败'
    console.error('获取背景图片失败:', err)
  } finally {
    loading.value = false
  }
}

// 处理图片加载完成
const handleImageLoad = (id) => {
  console.log('图片加载完成:', id)
  loadedImages.value.add(id)
}

// 选择背景
const handleSelect = (background) => {
  console.log('选择背景:', background)
  emit('select', background)
  emit('close')
}

// 关闭弹窗
const handleClose = () => {
  console.log('关闭弹窗')
  emit('close')
}

// 监听滚动容器的挂载
const scrollViewRef = ref(null)

// 初始化
onMounted(async () => {
  console.log('组件挂载')
  try {
    await fetchBackgrounds()
  } catch (err) {
    console.error('初始化失败:', err)
  }
})
</script>

<template>
  <view class="card-style">
    <view class="card-style__header">
      <view class="card-style__title">选择背景</view>
      <view class="card-style__close">
        <uni-icons type="close" size="20" color="#666" @click="handleClose"/>
      </view>
    </view>
    
    <template v-if="loading">
      <view class="card-style__loading">
        <uni-icons type="spinner-cycle" size="24" />
        <text>加载中...</text>
      </view>
    </template>
    
    <template v-else-if="error">
      <view class="card-style__error">
        <text>{{ error }}</text>
        <button @click="fetchBackgrounds">重试</button>
      </view>
    </template>
    
    <template v-else>
      <scroll-view 
        v-if="isReady"
        class="card-style__categories"
        scroll-x 
        :show-scrollbar="false"
        :enhanced="true"
        :scroll-x="true"
        :bounces="true"
      >
        <view class="card-style__container">
          <view 
            v-for="item in backgrounds" 
            :key="item.id"
            class="card-style__item"
            :class="{ 'card-style__item--active': currentStyle?.id === item.id }"
            @click="handleSelect(item)"
          >
            <image 
              :src="item.image_url" 
              mode="aspectFill"
              class="card-style__image"
              @load="() => handleImageLoad(item.id)"
            />
          </view>
        </view>
      </scroll-view>
    </template>
  </view>
</template>

<style lang="scss">
.card-style {
  height: 278rpx;
  padding: 20rpx 0;
  
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30rpx 20rpx;
  }
  
  &__title {
    font-size: 28rpx;
    color: #333;
    font-weight: 500;
  }
  
  &__close {
    padding: 10rpx;
  }
  
  &__loading,
  &__error {
    height: 178rpx;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20rpx;
    color: #666;
    font-size: 28rpx;
  }
  
  &__categories {
    width: 100%;
    height: 178rpx;
    white-space: nowrap;
    position: relative;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  &__container {
    display: inline-flex;
    padding: 0 30rpx;
    height: 100%;
    align-items: center;
    min-width: 100%;
  }
  
  &__item {
    position: relative;
    width: 100rpx;
    height: 178rpx;
    margin-right: 30rpx;
    border-radius: 12rpx;
    overflow: hidden;
    flex-shrink: 0;
    
    &:last-child {
      margin-right: 30rpx;
    }
    
    &--active::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      border: 4rpx solid #007AFF;
      border-radius: 12rpx;
      box-sizing: border-box;
    }
  }
  
  &__image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}
</style> 