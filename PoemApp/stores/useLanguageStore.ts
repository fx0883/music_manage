import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLanguageStore = defineStore('language', () => {
  const currentLanguage = ref('zh')
  
  function setLanguage(lang: string) {
    currentLanguage.value = lang
    try {
      uni.setStorageSync('language', lang)
    } catch (e) {
      console.error('保存语言设置失败:', e)
    }
  }
  
  function initLanguage() {
    try {
      const savedLang = uni.getStorageSync('language')
      if (savedLang) {
        currentLanguage.value = savedLang
      }
    } catch (e) {
      console.error('获取语言设置失败:', e)
    }
  }
  
  return {
    currentLanguage,
    setLanguage,
    initLanguage
  }
}) 