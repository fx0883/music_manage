<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  placeholder?: string
}>()

const emit = defineEmits(['search'])
const searchText = ref('')

const handleSearch = () => {
  emit('search', searchText.value)
}

const handleClear = () => {
  searchText.value = ''
  emit('search', '')
}
</script>

<template>
  <view class="search-bar">
    <view class="search-bar__inner">
      <uni-icons type="search" size="16" color="#999"/>
      <input
        v-model="searchText"
        class="search-bar__input"
        :placeholder="placeholder || '搜索'"
        confirm-type="search"
        @confirm="handleSearch"
      />
      <uni-icons
        v-if="searchText"
        type="clear"
        size="16"
        color="#999"
        @click="handleClear"
      />
    </view>
  </view>
</template>

<style lang="scss">
.search-bar {
  padding: 20rpx;
  background-color: #fff;
  
  &__inner {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 8rpx;
    padding: 12rpx 20rpx;
  }
  
  &__input {
    flex: 1;
    margin: 0 20rpx;
    font-size: 28rpx;
  }
}
</style> 