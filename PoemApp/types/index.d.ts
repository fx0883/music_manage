/// <reference types="@dcloudio/types" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'vue' {
  export * from '@vue/runtime-core'
}

// uni-app API类型声明
declare const uni: UniApp.Uni

// 声明全局类型
declare namespace UniApp {
  interface Uni {
    request(options: RequestOptions): Promise<RequestResponse>
    getSystemInfoSync(): SystemInfo
    // 其他需要的uni API类型
  }

  interface RequestOptions {
    url: string
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
    data?: any
    params?: Record<string, any>
    header?: Record<string, string>
    responseType?: 'text' | 'arraybuffer' | 'blob'
  }

  interface RequestResponse {
    data: any
    statusCode: number
    header: Record<string, string>
  }

  interface SystemInfo {
    windowWidth: number
    // 其他系统信息属性
  }
} 