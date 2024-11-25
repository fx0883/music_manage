import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useLanguageStore = defineStore('language', () => {
  const currentLanguage = ref('zh')
  
  function setLanguage(lang: string) {
    currentLanguage.value = lang
    // 可以在这里保存到本地存储
    uni.setStorageSync('language', lang)
  }
  
  function initLanguage() {
    const savedLang = uni.getStorageSync('language')
    if (savedLang) {
      currentLanguage.value = savedLang
    }
  }
  
  return {
    currentLanguage,
    setLanguage,
    initLanguage
  }
}) 