<script setup lang="ts">
defineProps<{
  text?: string
  icon?: string
}>()
</script>

<template>
  <view class="empty">
    <uni-icons 
      :type="icon || 'info'" 
      size="64" 
      color="#ddd"
    />
    <text class="empty__text">{{ text || '暂无数据' }}</text>
  </view>
</template>

<style lang="scss">
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;
  
  &__text {
    margin-top: 20rpx;
    font-size: 28rpx;
    color: #999;
  }
}
</style> 