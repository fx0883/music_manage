<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'

// 定义组件接收的属性类型
interface Props {
  poem: {
    title: string      // 诗词标题
    content: string    // 诗词内容
    author_name: string // 作者名
  }
}

// 定义组件的属性和事件
const props = defineProps<Props>()
const emit = defineEmits(['swipe']) // 定义滑动事件

// 处理诗词内容：获取前两句，按标点分段，去除标点
const poemSegments = computed(() => {
  // 获取前两句
  const lines = props.poem.content.split('\n').slice(0, 2)
  
  // 将两句合并，按标点符号分段
  const segments = lines.join('')
    // 在标点符号后添加分隔符
    .replace(/[，。、；：？！,.;:?!]/g, '$&|')
    // 按分隔符分割
    .split('|')
    // 过滤空字符串
    .filter(segment => segment)
    // 去除标点符号
    .map(segment => segment.replace(/[，。、；：？！,.;:?!]/g, ''))
    // 过滤空字符串
    .filter(segment => segment)
    // 将每个段落转为字符数组
    .map(segment => segment.split(''))

  return segments
})

// 拖动状态管理
const isDragging = ref(false)    // 是否正在拖动
const startX = ref(0)            // 触摸起始点X坐标
const startY = ref(0)            // 触摸起始点Y坐标
const offsetX = ref(0)           // X轴偏移量
const offsetY = ref(0)           // Y轴偏移量
const isAnimating = ref(false)   // 是否正在执行动画

// 字体加载状态
const fontLoaded = ref(false)
const currentFont = ref('')

// 加载字体
const loadFont = async (fontName: string) => {
  try {
    // 先通过 fetch 获取字体文件
    const response = await fetch(`http://127.0.0.1:8000/media/fonts/${fontName}.TTF`)
    if (!response.ok) {
      throw new Error(`Font file not found: ${response.statusText}`)
    }
    
    // 将响应转换为 blob
    const blob = await response.blob()
    if (!blob) {
      throw new Error('Failed to convert response to blob')
    }
    
    // 创建 blob URL
    const fontUrl = URL.createObjectURL(blob)
    
    // 创建 FontFace 对象
    const font = new FontFace(fontName, `url(${fontUrl})`)
    
    try {
      // 等待字体加载
      await font.load()
      
      // 将字体添加到 document.fonts
      document.fonts.add(font)
      
      // 更新状态
      fontLoaded.value = true
      currentFont.value = fontName
      
      // 清理 blob URL
      URL.revokeObjectURL(fontUrl)
    } catch (loadError) {
      console.error('Font loading failed:', loadError)
      URL.revokeObjectURL(fontUrl)  // 确保在出错时也清理 blob URL
      throw loadError
    }
  } catch (error) {
    console.error('Font loading failed:', error)
    fontLoaded.value = false
    currentFont.value = ''
  }
}

// 组件挂载时加载字体
onMounted(async () => {
  try {
    await loadFont('FZSTK')
  } catch (error) {
    console.error('Failed to load font on mount:', error)
  }
})

// 计算卡片的样式，包括位移、旋转和缩放
const cardStyle = computed(() => {
  // 如果没有拖动也没有动画，返回空对象
  if (!isDragging.value && !isAnimating.value) return {}
  
  // 根据X轴偏移量计算旋转角度
  const rotate = offsetX.value * 0.1
  // 根据偏移量计算缩放比例，最小为0.8
  const scale = Math.max(0.8, 1 - Math.abs(offsetX.value) * 0.001)
  
  // 定义样式对象的类型
  const style: {
    transform: string;
    transition: string;
    fontFamily?: string;  // 添加可选的fontFamily属性
  } = {
    transform: `
      translate(${offsetX.value}px, ${offsetY.value}px)
      rotate(${rotate}deg)
      scale(${scale})
    `,
    transition: isAnimating.value ? 'all 0.5s cubic-bezier(0.23, 1, 0.32, 1)' : 'none'
  }
  
  if (fontLoaded.value) {
    style.fontFamily = currentFont.value
  }
  
  return style
})

// 触摸开始事件处理
const handleTouchStart = (event: TouchEvent) => {
  if (isAnimating.value) return  // 如果正在执行动画，忽略触摸
  
  isDragging.value = true
  // 记录触摸起始位置
  startX.value = event.touches[0].clientX
  startY.value = event.touches[0].clientY
  // 重置偏移量
  offsetX.value = 0
  offsetY.value = 0
}

// 触摸移动事件处理
const handleTouchMove = (event: TouchEvent) => {
  if (!isDragging.value || isAnimating.value) return
  
  // 计算当前触摸点位置
  const currentX = event.touches[0].clientX
  const currentY = event.touches[0].clientY
  
  // 计算偏移量
  offsetX.value = currentX - startX.value
  offsetY.value = currentY - startY.value
}

// 触摸结束事件处理
const handleTouchEnd = () => {
  if (!isDragging.value || isAnimating.value) return
  
  isDragging.value = false
  const swipeThreshold = 100 // 滑动阈值，超过这个距离触发滑出效果
  
  if (Math.abs(offsetX.value) > swipeThreshold) {
    // 超过阈值，触发滑出动画
    isAnimating.value = true
    const direction = offsetX.value > 0 ? 1 : -1  // 确定滑动方向
    const screenWidth = uni.getSystemInfoSync().windowWidth
    
    // 设置滑出距离为屏幕宽度的1.5倍
    offsetX.value = direction * screenWidth * 1.5
    offsetY.value = offsetY.value * 1.5
    
    // 动画结束后触发事件
    setTimeout(() => {
      emit('swipe', direction > 0 ? 'right' : 'left')
      isAnimating.value = false
      offsetX.value = 0
      offsetY.value = 0
    }, 500)
  } else {
    // 未超过阈值，返回原位
    isAnimating.value = true
    offsetX.value = 0
    offsetY.value = 0
    
    setTimeout(() => {
      isAnimating.value = false
    }, 500)
  }
}

// 计算可用高度，上下都留出100px的空间
const containerHeight = computed(() => {
  const systemInfo = uni.getSystemInfoSync()
  const topBottomSpace = 100  // 上下各留出100px
  return systemInfo.windowHeight - (topBottomSpace * 2) + 'px'
})

// 计算容器的上边距
const containerStyle = computed(() => {
  return {
    height: containerHeight.value,
    top: '50px',  // 上边距50px
    left: '50px',  // 左边距50px
    right: '50px', // 右边距50px
    width: 'auto'  // 宽度自适应
  }
})
</script>

<template>
  <!-- 诗词卡片容器 -->
  <view 
    class="poem-card" 
    :style="[cardStyle, containerStyle]"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <view class="poem-card__content">
      <!-- 诗句区域：每个竖行显示一个分段 -->
      <view class="poem-card__lines">
        <view 
          v-for="(segment, segmentIndex) in poemSegments"
          :key="segmentIndex"
          class="poem-card__line"
        >
          <text 
            v-for="(char, charIndex) in segment"
            :key="charIndex"
            class="poem-card__character"
          >{{ char }}</text>
        </view>
      </view>
      
      <!-- 作者区域 -->
      <view class="poem-card__author">
        <text class="poem-card__author-name">{{ poem.author_name }}</text>
        <view class="poem-card__seal"></view>
      </view>
    </view>
  </view>
</template>

<style lang="scss">
.poem-card {
  width: 100%;  // 宽度占满容器
  height: 100%;  // 高度占满容器
  background: #fff;  // 白色背景
  display: flex;  // 使用弹性布局
  justify-content: center;  // 水平居中
  align-items: center;  // 垂直居中
  position: absolute;  // 绝对定位
  left: 0;  // 左边距离为0
  top: 0;  // 顶部距离为0
  will-change: transform;  // 优化transform动画性能
  transform-origin: center center;  // 变换原点居中
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);  // 添加阴影效果
  touch-action: none;  // 禁用默认触摸行为
  
  &__content {
    width: 80%;  // 内容区域宽度为容器的80%
    height: 80%;  // 内容区域高度为容器的80%
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    justify-content: space-between;  // 两端对齐
    padding: 60rpx 40rpx;  // 上下60rpx，左右40rpx的内边距
  }
  
  &__lines {
    display: flex;  // 使用弹性布局
    flex-direction: row-reverse;  // 从右向左排列
    justify-content: flex-start;  // 靠右对齐
    flex: 1;  // 占据剩余空间
	
  }
  
  &__line {
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    margin-right: 15rpx;  // 右边距60rpx
    
    &:first-child {
      margin-right: 0;  // 第一个段落不需要右边距
    }
  }
  
  &__character {
    font-size: 36rpx;
    line-height: 1.8;
    color: #333;
    font-weight: 300;
    writing-mode: vertical-rl;    // 竖排显示
    font-family: "FZSTK", "SimSun", serif;  // 直接使用字体名称，添加备选字体
  }
  
  &__author {
    display: flex;  // 使用弹性布局
    flex-direction: column;  // 垂直排列
    align-items: flex-start;  // 左对齐
    margin-top: 60rpx;  // 上边距60rpx
  }
  
  &__author-name {
    font-size: 32rpx;  // 字体大小32rpx
    color: #666;  // 中灰色文字
    margin-bottom: 20rpx;  // 下边距20rpx
    writing-mode: vertical-rl;  // 竖排显示
    font-family: "FZSTK", "SimSun", serif;  // 添加相同的字体设置
  }
  
  &__seal {
    width: 60rpx;  // 印章宽度60rpx
    height: 60rpx;  // 印章高度60rpx
    background-color: #f00;  // 红色背景
    border-radius: 4rpx;  // 圆角4rpx
  }
}
</style> 