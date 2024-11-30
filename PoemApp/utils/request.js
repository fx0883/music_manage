import config from '@/config'

class Request {
  constructor() {
    this.loading = false
    this.queue = []
  }

  async request(options) {
    const { 
      retryTimes = 3,
      retryDelay = 1000,
      loading = true,
      custom = {}
    } = options

    let currentRetry = 0

    const executeRequest = () => {
      return new Promise((resolve, reject) => {
        const requestTask = uni.request({
          ...options,
          success: (res) => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(res.data)
            } else {
              reject(new Error(`请求失败: ${res.statusCode}`))
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

    while (currentRetry <= retryTimes) {
      try {
        return await executeRequest()
      } catch (error) {
        currentRetry++
        if (currentRetry <= retryTimes) {
          await new Promise(resolve => setTimeout(resolve, retryDelay))
          continue
        }
        throw error
      }
    }
  }

  cancelAll() {
    this.queue.forEach(task => task.abort())
    this.queue = []
  }
}

export const request = new Request() 