import { createSSRApp } from 'vue'
import * as Pinia from 'pinia'
import App from './App.vue'
import { 
  UniIcons, 
  UniPopup, 
  UniList,
  UniListItem 
} from '@dcloudio/uni-ui'

export function createApp() {
  const app = createSSRApp(App)
  const store = Pinia.createPinia()
  
  app.component('uni-icons', UniIcons)
  app.component('uni-popup', UniPopup)
  app.component('uni-list', UniList)
  app.component('uni-list-item', UniListItem)
  
  app.use(store)
  
  return {
    app,
    Pinia
  }
} 