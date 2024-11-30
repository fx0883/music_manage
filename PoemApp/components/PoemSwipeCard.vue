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
  },
  topMargin: {
    type: [Number, String],
    default: 100
  },
  bottomMargin: {
    type: [Number, String],
    default: 100
  },
  leftMargin: {
    type: [Number, String],
    default: 40
  },
  rightMargin: {
    type: [Number, String],
    default: 40
  }
})

const emit = defineEmits(['swipe', 'animation-complete'])

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
  const swipeThreshold = 150
  const velocity = Math.abs(offsetX.value)
  const direction = offsetX.value > 0 ? 1 : -1
  const totalOffset = Math.sqrt(offsetX.value * offsetX.value + offsetY.value * offsetY.value)
  const screenWidth = uni.getSystemInfoSync().windowWidth
  
  if (totalOffset > swipeThreshold || velocity > 50) {
    isAnimating.value = true
    offsetX.value = direction * screenWidth * 1.5
    offsetY.value = offsetY.value * 1.5
    
    emit('swipe', direction > 0 ? 'right' : 'left')
    
    setTimeout(() => {
      isAnimating.value = false
      offsetX.value = 0
      offsetY.value = 0
      emit('animation-complete')
    }, 500)
  } else {
    isAnimating.value = true
    offsetX.value = 0
    offsetY.value = 0
    
    setTimeout(() => {
      isAnimating.value = false
      emit('animation-complete')
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
    style.transform = `
      translate(${offsetX.value}px, ${offsetY.value}px)
      rotate(${rotate}deg)
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
    :style="[
      cardStyle,
      {
        top: `${topMargin}rpx`,
        bottom: `${bottomMargin}rpx`,
        left: `${leftMargin}rpx`,
        right: `${rightMargin}rpx`
      }
    ]"
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
  position: absolute;
  background-color: #fff;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  padding: 60rpx 40rpx;
  box-sizing: border-box;
  
  &__content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  
  &__lines {
    flex: 1;
    display: flex;
    flex-direction: row-reverse;
    justify-content: center;
    align-items: flex-start;
    gap: 40rpx;
  }
  
  &__line {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  &__character {
    font-size: 42rpx;
    color: #333;
    line-height: 1.8;
    writing-mode: vertical-rl;
  }
  
  &__author {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-top: 60rpx;
  }
  
  &__author-name {
    font-size: 32rpx;
    color: #666;
    margin-bottom: 20rpx;
    writing-mode: vertical-rl;
  }
  
  &__seal {
    width: 60rpx;
    height: 60rpx;
    background-color: #f00;
  }
  
  &--top {
    z-index: 2;
  }
  
  &--animating {
    pointer-events: none;
  }
}
</style> 