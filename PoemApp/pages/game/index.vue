<script setup>
import { ref } from 'vue'

const activeGame = ref('quiz') // 当前选中的游戏类型
</script>

<template>
  <view class="game">
    <view class="game__header">
      <text class="game__title">诗词游戏</text>
    </view>
    
    <view class="game__content">
      <view class="game__menu">
        <view 
          class="game__menu-item"
          :class="{ 'game__menu-item--active': activeGame === 'quiz' }"
          @click="activeGame = 'quiz'"
        >
          <text>填空题</text>
        </view>
        <view 
          class="game__menu-item"
          :class="{ 'game__menu-item--active': activeGame === 'choice' }"
          @click="activeGame = 'choice'"
        >
          <text>选择题</text>
        </view>
      </view>
      
      <!-- 游戏内容区域 -->
      <view class="game__area">
        <text>游戏开发中...</text>
      </view>
    </view>
    <custom-tab-bar :selected="2" />
  </view>
</template>

<style lang="scss">
.game {
  min-height: 100vh;
  background-color: #f5f5f5;
  
  &__header {
    padding: 40rpx;
    background-color: #fff;
  }
  
  &__title {
    font-size: 36rpx;
    font-weight: bold;
    color: #333;
  }
  
  &__content {
    padding: 20rpx;
  }
  
  &__menu {
    display: flex;
    background-color: #fff;
    border-radius: 12rpx;
    margin-bottom: 20rpx;
  }
  
  &__menu-item {
    flex: 1;
    text-align: center;
    padding: 20rpx;
    font-size: 28rpx;
    color: #666;
    
    &--active {
      color: #3cc51f;
      font-weight: bold;
    }
  }
  
  &__area {
    background-color: #fff;
    border-radius: 12rpx;
    padding: 40rpx;
    text-align: center;
    color: #999;
  }
}
</style> 