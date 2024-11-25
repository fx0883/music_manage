<script setup lang="ts">
interface Props {
  title: string
  author: string
  content: string
  imageUrl?: string
  difficulty?: number
}

defineProps<Props>()
defineEmits(['click'])
</script>

<template>
  <view class="poem-card" @click="$emit('click')">
    <view class="poem-card__header">
      <text class="poem-card__title">{{ title }}</text>
      <text class="poem-card__author">{{ author }}</text>
    </view>
    
    <view class="poem-card__content">
      <text class="poem-card__text">{{ content }}</text>
      <image 
        v-if="imageUrl" 
        :src="imageUrl" 
        mode="aspectFill" 
        class="poem-card__image"
      />
    </view>
    
    <view v-if="difficulty" class="poem-card__footer">
      <text class="poem-card__difficulty">
        难度: {{ ['简单', '中等', '困难'][difficulty - 1] }}
      </text>
    </view>
  </view>
</template>

<style lang="scss">
.poem-card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  margin: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.1);

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16rpx;
  }

  &__title {
    font-size: 32rpx;
    font-weight: bold;
    color: #333;
  }

  &__author {
    font-size: 28rpx;
    color: #666;
  }

  &__content {
    margin: 16rpx 0;
  }

  &__text {
    font-size: 28rpx;
    color: #333;
    line-height: 1.6;
  }

  &__image {
    width: 100%;
    height: 300rpx;
    margin-top: 16rpx;
    border-radius: 8rpx;
  }

  &__footer {
    margin-top: 16rpx;
    display: flex;
    justify-content: flex-end;
  }

  &__difficulty {
    font-size: 24rpx;
    color: #666;
    background-color: #f5f5f5;
    padding: 4rpx 12rpx;
    border-radius: 4rpx;
  }
}
</style> 