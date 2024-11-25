<script setup lang="ts">
import { ref } from 'vue'

const languages = [
  { code: 'zh', name: '中文' },
  { code: 'en', name: 'English' },
  { code: 'ja', name: '日本語' },
  { code: 'es', name: 'Español' },
  { code: 'ar', name: 'العربية' }
]

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits(['update:modelValue'])

const showPicker = ref(false)

const handleChange = (e: any) => {
  const index = e.detail.value
  emit('update:modelValue', languages[index].code)
}

const getCurrentLanguageName = () => {
  return languages.find(lang => lang.code === props.modelValue)?.name || '中文'
}
</script>

<template>
  <view class="language-switch">
    <view class="language-switch__current" @click="showPicker = true">
      <text class="language-switch__text">{{ getCurrentLanguageName() }}</text>
      <uni-icons type="down" size="16" color="#666" />
    </view>
    
    <picker
      v-model="showPicker"
      :range="languages"
      range-key="name"
      @change="handleChange"
    >
      <view class="language-switch__picker">
        <text>{{ getCurrentLanguageName() }}</text>
      </view>
    </picker>
  </view>
</template>

<style lang="scss">
.language-switch {
  display: inline-flex;
  align-items: center;
  
  &__current {
    display: flex;
    align-items: center;
    padding: 12rpx 24rpx;
    background-color: #f5f5f5;
    border-radius: 8rpx;
  }
  
  &__text {
    font-size: 28rpx;
    color: #333;
    margin-right: 8rpx;
  }
  
  &__picker {
    display: none;
  }
}
</style> 