import { useRequest } from '@/utils/request'

const { request } = useRequest()

export const fontApi = {
  // 获取字体文件
  getFont(fontName: string): Promise<Blob> {
    return request({
      url: `/media/fonts/${fontName}.ttf`,
      responseType: 'blob'  // 指定响应类型为 blob
    })
  }
} 