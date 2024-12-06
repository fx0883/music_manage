<script setup>
import { computed, ref, onMounted } from 'vue'
import { fontManager } from '@/utils/font'

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
  },
  fontFamily: {
    type: String,
    default: 'SimSun'
  },
  fontSize: {
    type: Number,
    default: 42
  },
  backgroundImage: {
    type: String,
    default: ''
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
  const success = await fontManager.loadFont(fontName)
  fontLoaded.value = success
  currentFont.value = success ? fontName : ''
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
  // 如果不是顶层卡片、没有在拖动中、或正在执行动画,则直接返回
  if (!props.isTop || !isDragging.value || isAnimating.value) return
  
  // 阻止事件冒泡和默认行为
  event.stopPropagation()
  event.preventDefault()
  
  // 结束拖动状态
  isDragging.value = false

  // 定义滑动判定的阈值(像素)
  const swipeThreshold = 180
  // 计算水平方向滑动的速度(绝对值)
  const velocity = Math.abs(offsetX.value)
  // 根据滑动速度计算动画持续时间(速度越快,动画时间越短)
  const animationDuration = Math.max(300, 600 - velocity)
  // 判断滑动方向: 右滑为1,左滑为-1
  const direction = offsetX.value > 0 ? 1 : -1
  // 计算总偏移量(考虑水平和垂直方向的位移)
  const totalOffset = Math.sqrt(offsetX.value * offsetX.value + offsetY.value * offsetY.value)
  // 获取屏幕宽度
  const screenWidth = uni.getSystemInfoSync().windowWidth
  
  // 如果总偏移量超过阈值或速度足够快,触发滑动效果
  if (totalOffset > swipeThreshold || velocity > 50) {
    // 设置动画状态
    isAnimating.value = true
    // 设置卡片滑出屏幕的终点位置
    // 水平方向: 向左或向右移动1.5倍屏幕宽度
    offsetX.value = direction * screenWidth * 1.5
    // 垂直方向: 保持当前偏移的1.5倍
    offsetY.value = offsetY.value * 1.5
    
    // 动画结束后的处理
    setTimeout(() => {
      // 触发滑动事件,传递方向
      emit('swipe', direction > 0 ? 'right' : 'left')
      // 重置动画状态
      isAnimating.value = false
      // 重置位置偏移
      offsetX.value = 0
      offsetY.value = 0
      // 触发动画完成事件
      emit('animation-complete', true)
    }, animationDuration)
  } else {
    // 如果未达到滑动条件,执行回弹动画
    isAnimating.value = true
    // 重置位置到原点
    offsetX.value = 0
    offsetY.value = 0
    
    // 动画结束后重置状态
    setTimeout(() => {
      isAnimating.value = false
      emit('animation-complete', false)
    }, animationDuration)
  }
}

// 计算样式
const cardStyle = computed(() => {
  const style = {
    pointerEvents: 'auto',
    transform: '',
    transition: '',
    fontFamily: props.fontFamily,
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
      const velocity = Math.abs(offsetX.value)
      const duration = Math.max(0.3, 0.6 - velocity / 1000)
      style.transition = `all ${duration}s cubic-bezier(0.23, 1, 0.32, 1)`
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
  // 移除默认字体加载,使用传入的 fontFamily
})
</script>

<template>
  <view 
    class="poem-card" 
    :class="{
      'poem-card--top': isTop,
      'poem-card--animating': isAnimating,
      'poem-card--with-bg': backgroundImage
    }"
    :style="[
      cardStyle,
      {
        position: 'fixed',
        top: `${topMargin}rpx`,
        left: `${leftMargin}rpx`,
        right: `${rightMargin}rpx`,
        bottom: `${bottomMargin}rpx`,
        backgroundImage: backgroundImage ? `url(${backgroundImage})` : 'none'
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
            :style="{ fontSize: `${fontSize}rpx` }"
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
  background-color: #fff;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  padding: 60rpx 40rpx;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
  background-size: cover;
  background-position: center;
  
  &--with-bg {
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(255, 255, 255, 0.8); // 白色半透明遮罩
      z-index: 0;
    }
  }
  
  &__content {
    position: relative;
    z-index: 1;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  
  &__lines {
    flex: 1;
    display: flex;
    flex-direction: row-reverse;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 30rpx;
    padding-right: 20rpx;
  }
  
  &__line {
    display: grid;
    grid-auto-rows: min-content;
    row-gap: 30rpx;
  }
  
  &__character {
    font-size: 50rpx;
    color: #333;
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