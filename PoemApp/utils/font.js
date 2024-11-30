const FONT_BASE_URL = 'http://192.168.31.43:8000/media/fonts'

/**
 * 加载字体
 * @param {string} fontName 字体名称
 * @param {string} fontUrl 字体文件URL
 * @returns {Promise<boolean>} 是否加载成功
 */
export const loadFont = async (fontName, fontUrl) => {
  try {
    // 创建并添加 @font-face 样式
    const style = document.createElement('style')
    style.textContent = `
      @font-face {
        font-family: "${fontName}";
        src: url("${fontUrl}") format("truetype");
      }
    `
    document.head.appendChild(style)
    
    // 加载字体
    const font = new FontFace(
      fontName, 
      `url(${fontUrl})`
    )
    await font.load()
    document.fonts.add(font)
    
    return true
  } catch (error) {
    console.error('字体加载失败:', error)
    return false
  }
}

/**
 * 检查字体是否已加载
 * @param {string} fontName 字体名称
 * @returns {boolean} 是否已加载
 */
export const isFontLoaded = (fontName) => {
  return document.fonts.check(`12px "${fontName}"`)
}

/**
 * 字体管理器
 */
export const fontManager = {
  loadedFonts: new Set(),
  
  /**
   * 加载字体
   * @param {string} fontName 字体名称
   * @param {string} fontUrl 字体文件URL
   * @returns {Promise<boolean>} 是否加载成功
   */
  async loadFont(fontName, fontUrl) {
    if (this.loadedFonts.has(fontName)) {
      return true
    }
    
    const success = await loadFont(fontName, fontUrl)
    if (success) {
      this.loadedFonts.add(fontName)
    }
    return success
  },
  
  /**
   * 检查字体是否已加载
   * @param {string} fontName 字体名称
   * @returns {boolean} 是否已加载
   */
  isLoaded(fontName) {
    return this.loadedFonts.has(fontName) && isFontLoaded(fontName)
  }
} 