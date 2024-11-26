import { createSSRApp } from 'vue'
import * as Pinia from 'pinia'
import App from './App.vue'
import { UniIcons } from '@dcloudio/uni-ui'

export function createApp() {
  const app = createSSRApp(App)
  const store = Pinia.createPinia()
  
  app.component('uni-icons', UniIcons)
  
  app.use(store)
  
  return {
    app,
    Pinia
  }
} 