<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  selected: {
    type: Number,
    default: 0
  }
})

const tabList = [
  {
    pagePath: '/pages/poems/index',
    iconPath: '/static/tabbar/poem.png',
    selectedIconPath: '/static/tabbar/poem-active.png',
    text: '诗词'
  },
  {
    pagePath: '/pages/recommend/index',
    iconPath: '/static/tabbar/recommend.png',
    selectedIconPath: '/static/tabbar/recommend-active.png',
    text: '推荐'
  },
  {
    pagePath: '/pages/game/index',
    iconPath: '/static/tabbar/game.png',
    selectedIconPath: '/static/tabbar/game-active.png',
    text: '游戏'
  },
  {
    pagePath: '/pages/user/index',
    iconPath: '/static/tabbar/user.png',
    selectedIconPath: '/static/tabbar/user-active.png',
    text: '我的'
  }
]

const currentTab = ref(props.selected)

// 处理点击事件
const handleTabClick = (index, item) => {
  if (currentTab.value === index) return
  currentTab.value = index
  uni.switchTab({
    url: item.pagePath
  })
}

// 计算样式
const getTabStyle = computed(() => {
  const safeAreaHeight = uni.getSystemInfoSync().safeAreaInsets?.bottom || 0
  return {
    paddingBottom: `${safeAreaHeight}px`
  }
})
</script>

<template>
  <view class="tab-bar" :style="getTabStyle">
    <view 
      v-for="(item, index) in tabList" 
      :key="index"
      class="tab-bar__item"
      :class="{ 'tab-bar__item--active': currentTab === index }"
      @click="handleTabClick(index, item)"
    >
      <image 
        :src="currentTab === index ? item.selectedIconPath : item.iconPath"
        class="tab-bar__icon"
      />
      <text class="tab-bar__text">{{ item.text }}</text>
    </view>
  </view>
</template>

<style lang="scss">
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: calc(50px + constant(safe-area-inset-bottom));
  height: calc(50px + env(safe-area-inset-bottom));
  background: #fff;
  display: flex;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
  
  &__item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 50px;
    
    &--active {
      .tab-bar__text {
        color: #3cc51f;
      }
    }
  }
  
  &__icon {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
  }
  
  &__text {
    font-size: 10px;
    color: #7A7E83;
  }
}
</style>