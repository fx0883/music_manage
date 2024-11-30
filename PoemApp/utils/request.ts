import config from '@/config'

// 请求配置选项接口
interface RequestOptions extends UniApp.RequestOptions {
  retryTimes?: number
  retryDelay?: number
  loading?: boolean
  custom?: {
    showLoading?: boolean
    loadingMsg?: string
  }
}

class Request {
  private loading = false
  private queue: UniApp.RequestTask[] = []

  async request<T>(options: RequestOptions): Promise<T> {
    const { 
      retryTimes = 3,
      retryDelay = 1000,
      loading = true,
      custom,
      ...requestOptions 
    } = options

    let currentRetry = 0

    const execute = async (): Promise<T> => {
      if (loading && !this.loading && custom?.showLoading) {
        this.loading = true
        uni.showLoading({ 
          title: custom?.loadingMsg || '加载中...',
          mask: true 
        })
      }

      try {
        const response = await this._request(requestOptions)
        return response as T
      } catch (error) {
        if (currentRetry < retryTimes) {
          currentRetry++
          await new Promise(resolve => setTimeout(resolve, retryDelay * currentRetry))
          return execute()
        }
        throw error
      } finally {
        if (loading && this.loading && custom?.showLoading) {
          this.loading = false
          uni.hideLoading()
        }
      }
    }

    return execute()
  }

  private _request(options: UniApp.RequestOptions): Promise<any> {
    return new Promise((resolve, reject) => {
      const requestTask = uni.request({
        ...options,
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(res.data)
          } else {
            reject(new Error(res.data.message || '请求失败'))
          }
        },
        fail: reject,
        complete: () => {
          const index = this.queue.indexOf(requestTask)
          if (index > -1) {
            this.queue.splice(index, 1)
          }
        }
      })
      this.queue.push(requestTask)
    })
  }

  cancelAll() {
    this.queue.forEach(task => task.abort())
    this.queue = []
  }
}

export const request = new Request()