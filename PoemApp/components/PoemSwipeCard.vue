<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  poem: {
    title: string
    content: string
    author_name: string
  }
  slideOffset?: number
  isAnimating?: boolean
}

const props = defineProps<Props>()

// 获取诗词的前两句并转换为字符数组
const poemLines = computed(() => {
  const lines = props.poem.content.split('\n')
  return lines.slice(0, 2).map(line => line.split(''))
})

// 计算滑动和动画样式
const cardStyle = computed(() => {
  if (!props.slideOffset) return {}
  
  const rotate = props.slideOffset * 0.1 // 根据滑动距离计算旋转角度
  const scale = Math.max(0.8, 1 - Math.abs(props.slideOffset) * 0.001) // 滑动时逐渐缩小
  const translateY = Math.abs(props.slideOffset) * 0.3 // 添加垂直位移
  
  return {
    transform: `
      translateX(${props.slideOffset}px)
      translateY(${translateY}px)
      rotate(${rotate}deg)
      scale(${scale})
    `,
    transition: props.isAnimating ? 'all 0.5s cubic-bezier(0.23, 1, 0.32, 1)' : 'none',
    opacity: Math.max(0, 1 - Math.abs(props.slideOffset) * 0.002)
  }
})
</script>

<template>
  <view class="poem-card" :style="cardStyle">
    <view class="poem-card__content">
      <view class="poem-card__lines">
        <view 
          v-for="(line, lineIndex) in poemLines"
          :key="lineIndex"
          class="poem-card__line"
        >
          <text 
            v-for="(char, charIndex) in line"
            :key="charIndex"
            class="poem-card__character"
          >{{ char }}</text>
        </view>
      </view>
      
      <view class="poem-card__author">
        <text class="poem-card__author-name">{{ poem.author_name }}</text>
        <view class="poem-card__seal"></view>
      </view>
    </view>
  </view>
</template>

<style lang="scss">
.poem-card {
  width: 100%;
  height: 100%;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  left: 0;
  top: 0;
  will-change: transform;
  transform-origin: center center;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
  
  &__content {
    width: 80%;
    height: 80%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 60rpx 40rpx;
  }
  
  &__lines {
    display: flex;
    flex-direction: row-reverse;
    justify-content: flex-start;
    flex: 1;
  }
  
  &__line {
    display: flex;
    flex-direction: column;
    margin-right: 60rpx;
    
    &:first-child {
      margin-right: 0;
    }
  }
  
  &__character {
    font-size: 48rpx;
    line-height: 1.8;
    color: #333;
    font-weight: 300;
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
    border-radius: 4rpx;
  }
}
</style> 