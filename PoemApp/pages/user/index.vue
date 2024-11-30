<script setup>
import { ref } from 'vue'

const userInfo = ref({
  nickname: '游客',
  avatar: '/static/default-avatar.png'
})

const menuItems = [
  { icon: 'star', text: '我的收藏', badge: 0 },
  { icon: 'medal', text: '学习进度', badge: 0 },
  { icon: 'settings', text: '设置', badge: 0 }
]
</script>

<template>
  <view class="user">
    <view class="user__header">
      <image :src="userInfo.avatar" class="user__avatar" />
      <text class="user__nickname">{{ userInfo.nickname }}</text>
    </view>
    
    <view class="user__menu">
      <view 
        v-for="(item, index) in menuItems" 
        :key="index"
        class="user__menu-item"
      >
        <uni-icons :type="item.icon" size="24" color="#666" />
        <text class="user__menu-text">{{ item.text }}</text>
        <uni-icons type="right" size="16" color="#999" />
      </view>
    </view>
  </view>
</template>

<style lang="scss">
.user {
  min-height: 100vh;
  background-color: #f5f5f5;
  
  &__header {
    padding: 60rpx 40rpx;
    background-color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  &__avatar {
    width: 128rpx;
    height: 128rpx;
    border-radius: 50%;
    margin-bottom: 20rpx;
  }
  
  &__nickname {
    font-size: 32rpx;
    color: #333;
    font-weight: bold;
  }
  
  &__menu {
    margin-top: 20rpx;
    background-color: #fff;
  }
  
  &__menu-item {
    display: flex;
    align-items: center;
    padding: 30rpx 40rpx;
    border-bottom: 1rpx solid #eee;
    
    &:last-child {
      border-bottom: none;
    }
  }
  
  &__menu-text {
    flex: 1;
    margin-left: 20rpx;
    font-size: 28rpx;
    color: #333;
  }
}
</style> 