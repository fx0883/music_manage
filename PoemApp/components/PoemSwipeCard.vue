<script setup lang="ts">
import { computed, ref } from 'vue'

// 定义组件接收的属性类型
interface Props {
  poem: {
    title: string      // 诗词标题
    content: string    // 诗词内容
    author_name: string // 作者名
  }
}

// 定义组件的属性和事件
const props = defineProps<Props>()
const emit = defineEmits(['swipe']) // 定义滑动事件

// 处理诗词内容：获取前两句，按标点分段，去除标点
const poemSegments = computed(() => {
  // 获取前两句
  const lines = props.poem.content.split('\n').slice(0, 2)
  
  // 将两句合并，按标点符号分段
  const segments = lines.join('')
    // 在标点符号后添加分隔符
    .replace(/[，。、；：？！,.;:?!]/g, '$&|')
    // 按分隔符分割
    .split('|')
    // 过滤空字符串
    .filter(segment => segment)
    // 去除标点符号
    .map(segment => segment.replace(/[，。、；：？！,.;:?!]/g, ''))
    // 过滤空字符串
    .filter(segment => segment)
    // 将每个段落转为字符数组
    .map(segment => segment.split(''))

  return segments
})

// 拖动状态管理
const isDragging = ref(false)    // 是否正在拖动
const startX = ref(0)            // 触摸起始点X坐标
const startY = ref(0)            // 触摸起始点Y坐标
const offsetX = ref(0)           // X轴偏移量
const offsetY = ref(0)           // Y轴偏移量
const isAnimating = ref(false)   // 是否正在执行动画

// 计算卡片的样式，包括位移、旋转和缩放
const cardStyle = computed(() => {
  // 如果没有拖动也没有动画，返回空对象
  if (!isDragging.value && !isAnimating.value) return {}
  
  // 根据X轴偏移量计算旋转角度
  const rotate = offsetX.value * 0.1
  // 根据偏移量计算缩放比例，最小为0.8
  const scale = Math.max(0.8, 1 - Math.abs(offsetX.value) * 0.001)
  
  return {
    transform: `
      translate(${offsetX.value}px, ${offsetY.value}px)
      rotate(${rotate}deg)
      scale(${scale})
    `,
    // 动画执行时使用贝塞尔曲线，否则不使用过渡效果
    transition: isAnimating.value ? 'all 0.5s cubic-bezier(0.23, 1, 0.32, 1)' : 'none'
  }
})

// 触摸开始事件处理
const handleTouchStart = (event: TouchEvent) => {
  if (isAnimating.value) return  // 如果正在执行动画，忽略触摸
  
  isDragging.value = true
  // 记录触摸起始位置
  startX.value = event.touches[0].clientX
  startY.value = event.touches[0].clientY
  // 重置偏移量
  offsetX.value = 0
  offsetY.value = 0
}

// 触摸移动事件处理
const handleTouchMove = (event: TouchEvent) => {
  if (!isDragging.value || isAnimating.value) return
  
  // 计算当前触摸点位置
  const currentX = event.touches[0].clientX
  const currentY = event.touches[0].clientY
  
  // 计算偏移量
  offsetX.value = currentX - startX.value
  offsetY.value = currentY - startY.value
}

// 触摸结束事件处理
const handleTouchEnd = () => {
  if (!isDragging.value || isAnimating.value) return
  
  isDragging.value = false
  const swipeThreshold = 100 // 滑动阈值，超过这个距离触发滑出效果
  
  if (Math.abs(offsetX.value) > swipeThreshold) {
    // 超过阈值，触发滑出动画
    isAnimating.value = true
    const direction = offsetX.value > 0 ? 1 : -1  // 确定滑动方向
    const screenWidth = uni.getSystemInfoSync().windowWidth
    
    // 设置滑出距离为屏幕宽度的1.5倍
    offsetX.value = direction * screenWidth * 1.5
    offsetY.value = offsetY.value * 1.5
    
    // 动画结束后触发事件
    setTimeout(() => {
      emit('swipe', direction > 0 ? 'right' : 'left')
      isAnimating.value = false
      offsetX.value = 0
      offsetY.value = 0
    }, 500)
  } else {
    // 未超过阈值，返回原位
    isAnimating.value = true
    offsetX.value = 0
    offsetY.value = 0
    
    setTimeout(() => {
      isAnimating.value = false
    }, 500)
  }
}

// 计算可用高度，上下都留出100px的空间
const containerHeight = computed(() => {
  const systemInfo = uni.getSystemInfoSync()
  const topBottomSpace = 100  // 上下各留出100px
  return systemInfo.windowHeight - (topBottomSpace * 2) + 'px'
})

// 计算容器的上边距
const containerStyle = computed(() => {
  return {
    height: containerHeight.value,
    top: '50px',  // 上边距50px
    left: '50px',  // 左边距50px
    right: '50px', // 右边距50px
    width: 'auto'  // 宽度自适应
  }
})
</script>

<template>
  <!-- 诗词卡片容器 -->
  <view 
    class="poem-card" 
    :style="[cardStyle, containerStyle]"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <view class="poem-card__content">
      <!-- 诗句区域：每个竖行显示一个分段 -->
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
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  will-change: transform;
  transform-origin: center center;
  touch-action: none;

  &__content {
    width: 100%;  // 修改为100%以适应新的容器大小
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 60rpx 40rpx;

  }
  
  // 诗句区域
  &__lines {
    display: flex;
    flex-direction: row-reverse;  // 从右向左排列
    justify-content: center;      // 居中显示
    align-items: flex-start;      // 顶部对齐
    flex: 1;
    gap: 1rpx;                  // 将分段之间的间距从60rpx改为15rpx
  }
  
  // 单行诗句
  &__line {
    display: flex;
    flex-direction: column;
    gap: 10rpx;                  // 字符之间的间距
  }
  
  // 单个汉字
  &__character {
    font-size: 48rpx;
    line-height: 1.8;
    color: #333;
    font-weight: 300;
    writing-mode: vertical-rl;    // 竖排显示
  }
  
  // 作者区域
  &__author {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-top: 60rpx;
  }
  
  // 作者名
  &__author-name {
    font-size: 32rpx;
    color: #666;
    margin-bottom: 20rpx;
    writing-mode: vertical-rl;  // 竖排显示
  }
  
  // 印章
  &__seal {
    width: 60rpx;
    height: 60rpx;
    background-color: #f00;
    border-radius: 4rpx;
  }
}
</style> 