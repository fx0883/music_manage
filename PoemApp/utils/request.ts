import config from '@/config'

// 请求配置选项接口
interface RequestOptions extends UniApp.RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  custom?: {
    showSuccess?: boolean
    successMsg?: string
    showError?: boolean
    errorMsg?: string
    showLoading?: boolean
    loadingMsg?: string
    auth?: boolean
  }
}

// Loading全局实例
let LoadingInstance = {
  count: 0
}

/**
 * 关闭loading
 */
function closeLoading() {
  if (LoadingInstance.count > 0) LoadingInstance.count--
  if (LoadingInstance.count === 0) uni.hideLoading()
}

// 默认配置
const defaultOptions = {
  showSuccess: false,
  successMsg: '',
  showError: true,
  errorMsg: '',
  showLoading: true,
  loadingMsg: '加载中',
  auth: false
}

/**
 * 请求函数
 */
const request = <T>(options: RequestOptions): Promise<T> => {
  // 合并配置
  const custom = { ...defaultOptions, ...options.custom }
  
  // 处理 URL
  const url = options.url.startsWith('http') 
    ? options.url  // 如果是完整的 URL，直接使用
    : `${config.baseUrl}${options.url}` // 否则拼接 baseUrl

  return new Promise((resolve, reject) => {
    // 显示loading
    if (custom.showLoading) {
      LoadingInstance.count++
      if (LoadingInstance.count === 1) {
        uni.showLoading({
          title: custom.loadingMsg,
          mask: true
        })
      }
    }

    // 发起请求
    uni.request({
      url,  // 使用处理后的 URL
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json;charset=UTF-8',
      },
      success: (res: any) => {
        // 关闭loading
        custom.showLoading && closeLoading()

        // 处理响应
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // 成功提示
          if (custom.showSuccess && custom.successMsg) {
            uni.showToast({
              title: custom.successMsg,
              icon: 'none'
            })
          }
          resolve(res.data)
        } else {
          // 错误提示
          if (custom.showError) {
            uni.showToast({
              title: custom.errorMsg || res.data?.msg || '请求失败',
              icon: 'none'
            })
          }
          reject(res)
        }
      },
      fail: (err) => {
        // 关闭loading
        custom.showLoading && closeLoading()

        // 错误提示
        if (custom.showError) {
          uni.showToast({
            title: '网络请求失败',
            icon: 'none'
          })
        }
        reject(err)
      }
    })
  })
}

export const useRequest = () => {
  return {
    request
  }
}

export { request }