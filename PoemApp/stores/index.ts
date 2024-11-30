import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persist-uni'

// 自动导入所有 store 模块
const files = import.meta.glob('./*.ts', { eager: true })
const modules = {}
Object.keys(files).forEach((key) => {
  if (key !== './index.ts') {
    modules[key.replace(/(.*\/)*([^.]+).*/gi, '$2')] = files[key].default
  }
})

export const setupPinia = (app) => {
  const pinia = createPinia()
  pinia.use(piniaPersist)
  app.use(pinia)
}

export default (name) => {
  return modules[name]()
} 