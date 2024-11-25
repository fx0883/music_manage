import { ref } from 'vue'

const BASE_URL = 'http://127.0.0.1:8000'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  params?: Record<string, any>
}

export function useRequest() {
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const request = async <T>(options: RequestOptions): Promise<T> => {
    const { url, method = 'GET', data, params } = options
    loading.value = true
    error.value = null

    try {
      let fullUrl = `${BASE_URL}${url}`
      if (params) {
        const queryString = Object.entries(params)
          .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
          .join('&')
        fullUrl += `?${queryString}`
      }

      const response = await uni.request({
        url: fullUrl,
        method,
        data,
        header: {
          'Content-Type': 'application/json'
        }
      })

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return response.data as T
      }

      throw new Error(`Request failed with status ${response.statusCode}`)
    } catch (e) {
      error.value = e as Error
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    request
  }
} 