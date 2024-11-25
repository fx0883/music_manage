<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})
onShow(() => {
  console.log('App Show')
})
onHide(() => {
  console.log('App Hide')
})
</script>

<template>
  <view class="container">
    <router-view></router-view>
  </view>
</template>

<style>
.container {
  width: 100%;
  height: 100%;
}
</style>
