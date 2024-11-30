<script setup>
import { ref, onMounted, computed } from 'vue'
import { fontApi } from '@/api/font'
import { fontManager } from '@/utils/font'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const categories = ref([])
const loading = ref(false)
const activeCategory = ref('全部')
const selectedFont = ref(props.modelValue)
const loadingFont = ref(false)

// 获取字体分类数据
const fetchFontCategories = async () => {
  loading.value = true
  try {
    const data = await fontApi.getFontCategories()
    categories.value = data
  } catch (error) {
    console.error('获取字体分类失败:', error)
    uni.showToast({
      title: '获取字体分类失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// 处理字体选择
const handleFontSelect = async (font) => {
  if (loadingFont.value) return
  
  loadingFont.value = true
  try {
    // 加载字体文件
    const success = await fontManager.loadFont(font.code, font.file_url)
    if (success) {
      selectedFont.value = font.name
      emit('update:modelValue', font.name)
      emit('select', {
        ...font,
        fontFamily: font.code // 使用字体代码作为 font-family
      })
      
      uni.showToast({
        title: '字体切换成功',
        icon: 'success'
      })
    } else {
      throw new Error('字体加载失败')
    }
  } catch (error) {
    console.error('字体切换失败:', error)
    uni.showToast({
      title: '字体切换失败',
      icon: 'none'
    })
  } finally {
    loadingFont.value = false
  }
}

// 处理分类选择
const handleCategorySelect = (category) => {
  activeCategory.value = category
}

// 获取所有字体
const allFonts = computed(() => {
  if (activeCategory.value === '全部') {
    return categories.value.flatMap(cat => cat.fonts)
  }
  return categories.value.find(cat => cat.name === activeCategory.value)?.fonts || []
})

onMounted(() => {
  fetchFontCategories()
})
</script>

<template>
  <view class="font-selector">
    <!-- 分类选择区域 -->
    <scroll-view 
      scroll-x 
      class="font-selector__categories"
      :show-scrollbar="false"
      enhanced
      :bounces="true"
    >
      <view class="font-selector__tabs">
        <view 
          class="font-selector__tab"
          :class="{ 'font-selector__tab--active': activeCategory === '全部' }"
          @click="handleCategorySelect('全部')"
        >
          全部
        </view>
        <view 
          v-for="category in categories"
          :key="category.code"
          class="font-selector__tab"
          :class="{ 'font-selector__tab--active': activeCategory === category.name }"
          @click="handleCategorySelect(category.name)"
        >
          {{ category.name }}
        </view>
      </view>
    </scroll-view>

    <!-- 字体列表 -->
    <template v-if="loading">
      <LoadingState text="加载字体分类中..." />
    </template>
    
    <template v-else>
      <uni-list class="font-selector__fonts">
        <uni-list-item
          v-for="font in allFonts"
          :key="font.code"
          :class="{ 
            'font-selector__font--active': selectedFont === font.name,
            'font-selector__font--loading': loadingFont && selectedFont === font.name
          }"
          @click="handleFontSelect(font)"
          :show-arrow="false"
          :clickable="true"
        >
          <template #body>
            <view class="font-selector__font-content">
              <image 
                :src="font.preview_url" 
                mode="aspectFit"
                class="font-selector__preview"
              />
              <text class="font-selector__name">{{ font.name }}</text>
            </view>
          </template>
          <template #footer>
            <view class="font-selector__status">
              <uni-icons 
                v-if="loadingFont && selectedFont === font.name"
                type="spinner-cycle"
                size="18"
                color="#3cc51f"
                class="font-selector__loading-icon"
              />
              <text 
                v-else-if="selectedFont === font.name" 
                class="font-selector__check"
              >✓</text>
            </view>
          </template>
        </uni-list-item>
      </uni-list>
    </template>
  </view>
</template>

<style lang="scss">
.font-selector {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  touch-action: pan-y;
  
  &__categories {
    background-color: #f5f5f5;
    white-space: nowrap;
    flex-shrink: 0;
    touch-action: pan-x;
  }
  
  &__tabs {
    display: inline-flex;
    padding: 20rpx;
  }
  
  &__tab {
    padding: 10rpx 30rpx;
    margin-right: 20rpx;
    font-size: 28rpx;
    color: #666;
    background-color: #fff;
    border-radius: 30rpx;
    
    &--active {
      color: #fff;
      background-color: #333;
    }
  }
  
  &__fonts {
    flex: 1;
    height: 0;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  &__font-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 20rpx 0;
  }
  
  &__preview {
    width: 400rpx;
    height: 60rpx;
    margin-bottom: 10rpx;
  }
  
  &__name {
    font-size: 24rpx;
    color: #666;
  }
  
  &__check {
    color: #3cc51f;
    margin-left: 20rpx;
  }
  
  &__font--active {
    background-color: #f8f8f8;
  }
  
  &__font--loading {
    opacity: 0.7;
    pointer-events: none;
  }
  
  &__status {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40rpx;
  }
  
  &__loading-icon {
    animation: rotate 1s linear infinite;
  }
  
  @keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
}

:deep(.uni-list) {
  height: 100%;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

:deep(.uni-list-item) {
  padding: 0 30rpx !important;
}

:deep(.uni-list-item__container) {
  padding: 0 !important;
}
</style> 