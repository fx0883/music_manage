import { createSSRApp } from 'vue'
import App from './App.vue'
import { setupPinia } from '@/stores'

// 修改导入方式
import UniIcons from '@dcloudio/uni-ui/lib/uni-icons/uni-icons.vue'
import UniPopup from '@dcloudio/uni-ui/lib/uni-popup/uni-popup.vue'
import UniList from '@dcloudio/uni-ui/lib/uni-list/uni-list.vue'
import UniListItem from '@dcloudio/uni-ui/lib/uni-list-item/uni-list-item.vue'
import CustomTabBar from './custom-tab-bar/index.vue'

export function createApp() {
  const app = createSSRApp(App)
  
  // 设置 Pinia
  setupPinia(app)
  
  // 注册组件
  app.component('uni-icons', UniIcons)
  app.component('uni-popup', UniPopup)
  app.component('uni-list', UniList)
  app.component('uni-list-item', UniListItem)
  app.component('custom-tab-bar', CustomTabBar)
  
  return {
    app
  }
}