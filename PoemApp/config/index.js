// 开发环境
const isDev = process.env.NODE_ENV === 'dev'

// API基础路径
const baseUrl = isDev 
  ? 'http://192.168.31.143:8000/chinese/api'
  : 'http://192.168.31.143:8000/chinese/api'

export default {
  baseUrl
} 