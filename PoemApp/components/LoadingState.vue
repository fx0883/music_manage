<script setup>
defineProps({
  text: String
})
</script>

<template>
  <view class="loading">
    <view class="loading__spinner">
      <uni-icons type="spinner-cycle" size="24" color="#3cc51f" />
    </view>
    <text class="loading__text">{{ text || '加载中...' }}</text>
  </view>
</template>

<style lang="scss">
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
  
  &__spinner {
    animation: rotate 1s linear infinite;
  }
  
  &__text {
    margin-top: 20rpx;
    font-size: 28rpx;
    color: #999;
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style> 