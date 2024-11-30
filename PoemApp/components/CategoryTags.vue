<script setup>
const props = defineProps({
  categories: {
    type: Array,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const handleSelect = (code) => {
  emit('update:modelValue', code)
}
</script>

<template>
  <scroll-view 
    class="category-tags" 
    scroll-x 
    show-scrollbar="false"
  >
    <view class="category-tags__wrapper">
      <view
        v-for="category in categories"
        :key="category.code"
        class="category-tags__item"
        :class="{ 'category-tags__item--active': modelValue === category.code }"
        @click="handleSelect(category.code)"
      >
        <text class="category-tags__text">{{ category.name }}</text>
      </view>
    </view>
  </scroll-view>
</template>

<style lang="scss">
.category-tags {
  background-color: #fff;
  white-space: nowrap;
  
  &__wrapper {
    padding: 20rpx;
    display: inline-flex;
  }
  
  &__item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12rpx 24rpx;
    margin-right: 20rpx;
    background-color: #f5f5f5;
    border-radius: 8rpx;
    transition: all 0.3s;
    
    &:last-child {
      margin-right: 0;
    }
    
    &--active {
      background-color: #3cc51f;
      .category-tags__text {
        color: #fff;
      }
    }
  }
  
  &__text {
    font-size: 28rpx;
    color: #666;
  }
}
</style> 