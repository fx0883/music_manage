<script setup>
import { computed, ref, onMounted } from 'vue'
import { fontApi } from '@/api/font'

const props = defineProps({
  poem: {
    type: Object,
    required: true
  },
  isTop: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['swipe', 'animationComplete'])

// 处理诗词内容：获取前两句，按标点分段，去除标点
const poemSegments = computed(() => {
  const lines = props.poem.content.split('\n').slice(0, 2)
  
  const segments = lines.join('')
    .replace(/[，。、；：？！,.;:?!]/g, '$&|')
    .split('|')
    .filter(segment => segment)
    .map(segment => segment.replace(/[，。、；：？！,.;:?!]/g, ''))
    .filter(segment => segment)
    .map(segment => segment.split(''))

  return segments
})

// 拖动状态管理
const isDragging = ref(false)
const startX = ref(0)
const startY = ref(0)
const offsetX = ref(0)
const offsetY = ref(0)
const isAnimating = ref(false)

// 字体加载状态
const fontLoaded = ref(false)
const currentFont = ref('')

// 加载字体
const loadFont = async (fontName) => {
  try {
    const style = document.createElement('style')
    style.textContent = `
      @font-face {
        font-family: "${fontName}";
        src: url("http://127.0.0.1:8000/media/fonts/${fontName}.ttf") format("truetype");
      }
    `
    document.head.appendChild(style)
    
    const font = new FontFace(fontName, `url(http://127.0.0.1:8000/media/fonts/${fontName}.ttf)`)
    await font.load()
    document.fonts.add(font)
    
    fontLoaded.value = true
    currentFont.value = fontName
  } catch (error) {
    console.error('字体加载失败:', error)
    fontLoaded.value = false
    currentFont.value = ''
  }
}

// 触摸事件处理
const handleTouchStart = (event) => {
  if (!props.isTop || isAnimating.value) return
  
  event.stopPropagation()
  event.preventDefault()
  
  isDragging.value = true
  startX.value = event.touches[0].clientX
  startY.value = event.touches[0].clientY
  offsetX.value = 0
  offsetY.value = 0
}

const handleTouchMove = (event) => {
  if (!props.isTop || !isDragging.value || isAnimating.value) return
  
  event.stopPropagation()
  event.preventDefault()
  
  offsetX.value = event.touches[0].clientX - startX.value
  offsetY.value = event.touches[0].clientY - startY.value
}

const handleTouchEnd = (event) => {
  if (!props.isTop || !isDragging.value || isAnimating.value) return
  
  event.stopPropagation()
  event.preventDefault()
  
  isDragging.value = false
  const swipeThreshold = 100
  const velocity = Math.abs(offsetX.value)
  const direction = offsetX.value > 0 ? 1 : -1
  const screenWidth = uni.getSystemInfoSync().windowWidth
  
  if (Math.abs(offsetX.value) > swipeThreshold || velocity > 50) {
    isAnimating.value = true
    offsetX.value = direction * screenWidth * 1.5
    offsetY.value = offsetY.value * 1.5
    
    setTimeout(() => {
      emit('swipe', direction > 0 ? 'right' : 'left')
      isAnimating.value = false
      offsetX.value = 0
      offsetY.value = 0
      emit('animationComplete')
    }, 500)
  } else {
    isAnimating.value = true
    offsetX.value = 0
    offsetY.value = 0
    
    setTimeout(() => {
      isAnimating.value = false
      emit('animationComplete')
    }, 500)
  }
}

// 计算样式
const cardStyle = computed(() => {
  const style = {
    pointerEvents: 'auto',
    transform: '',
    transition: '',
    fontFamily: ''
  }

  if (isAnimating.value || !props.isTop) {
    style.pointerEvents = 'none'
  }

  if (isDragging.value || isAnimating.value) {
    const rotate = offsetX.value * 0.1
    const scale = Math.max(0.8, 1 - Math.abs(offsetX.value) * 0.001)
    
    style.transform = `
      translate(${offsetX.value}px, ${offsetY.value}px)
      rotate(${rotate}deg)
      scale(${scale})
    `
    
    if (isAnimating.value) {
      style.transition = `all ${isDragging.value ? '0.3s' : '0.5s'} cubic-bezier(0.23, 1, 0.32, 1)`
    } else {
      style.transition = 'none'
    }
  }

  if (fontLoaded.value && currentFont.value) {
    style.fontFamily = `"${currentFont.value}", "SimSun", serif`
  }

  return style
})

// 初始化
onMounted(async () => {
  try {
    await loadFont('13')
  } catch (error) {
    console.error('Failed to load font on mount:', error)
  }
})
</script>

<template>
  <view 
    class="poem-card" 
    :class="{
      'poem-card--top': isTop,
      'poem-card--animating': isAnimating
    }"
    :style="cardStyle"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <view class="poem-card__content">
      <!-- 诗句区域 -->
      <view class="poem-card__lines">
        <view 
          v-for="(segment, segmentIndex) in poemSegments"
          :key="segmentIndex"
          class="poem-card__line"
        >
          <text 
            v-for="(char, charIndex) in segment"
            :key="charIndex"
            class="poem-card__character"
          >{{ char }}</text>
        </view>
      </view>
      
      <!-- 作者区域 -->
      <view class="poem-card__author">
        <text class="poem-card__author-name">{{ poem.author_name }}</text>
        <view class="poem-card__seal"></view>
      </view>
    </view>
  </view>
</template>

<style lang="scss">
.poem-card {
  width: 100%;  // 宽度占满容器
  height: 100%;  // 高度占满容器
  background: #fff;  // 白色背景
  display: flex;  // 使用弹性布局
  justify-content: center;  // 水平居中
  align-items: center;  // 垂直居中
  position: absolute;  // 绝对定位
  left: 0;  // 左边距离为0
  top: 0;  // 顶部距离为0
  will-change: transform;  // 优化transform动画性能
  transform-origin: center center;  // 变换原点居中
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);  // 添加阴影效果
  touch-action: none;  // 禁用默认触摸行为
  
  &__content {
    width: 80%;  // 内容区域宽度为容器的80%
    height: 80%;  // 内容区域高度为容器的80%
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    justify-content: space-between;  // 两端对齐
    padding: 60rpx 40rpx;  // 上下60rpx，左右40rpx的内边距
  }
  
  &__lines {
    display: flex;  // 使用弹性布局
    flex-direction: row-reverse;  // 从右向左排列
    justify-content: flex-start;  // 靠右对齐
    flex: 1;  // 占据剩余空间
	
  }
  
  &__line {
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    margin-right: 5rpx;  // 右边距60rpx
    
    &:first-child {
      margin-right: 0;  // 第一个段落不需要右边距
    }
  }
  
  &__character {
    font-size: 42rpx;
    line-height: 1.8;
    color: #333;
    font-weight: 300;
    writing-mode: vertical-rl;    // 竖排显示
  }
  
  &__author {
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    align-items: flex-start;  // 左对齐
    margin-top: 60rpx;  // 上边距60rpx
  }
  
  &__author-name {
    font-size: 32rpx;
    color: #666;
    margin-bottom: 20rpx;
    writing-mode: vertical-rl;
  }
  
  &__seal {
    width: 60rpx;  // 印章宽度60rpx
    height: 60rpx;  // 印章高度60rpx
    background-color: #f00;  // 红色背景
    border-radius: 4rpx;  // 圆角4rpx
  }
  
  &--top {
    z-index: 2;  // 顶层卡片使用更高的 z-index
  }
  
  &--animating {
    pointer-events: none;  // 动画过程中禁用交互
  }
}
</style> 