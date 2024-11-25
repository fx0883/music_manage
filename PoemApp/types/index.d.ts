declare module 'vue' {
  export * from '@vue/runtime-core'
}

// uni-app API类型声明
declare const uni: {
  request(options: {
    url: string
    method?: string
    data?: any
    header?: Record<string, string>
  }): Promise<{
    data: any
    statusCode: number
    header: Record<string, string>
  }>
  // 其他uni API的类型声明
  [key: string]: any
} 