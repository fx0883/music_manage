# Uniapp 编码需求

## 一、代码风格与结构
- 编写清晰、可维护且技术准确的 JavaScript 或 TypeScript 代码（根据项目需求选择）。
    - 注重迭代和模块化，遵循 DRY（Don't Repeat Yourself）原则，最小化代码重复。
    - 优先使用组合式 API 的`<script setup>`风格。
    - 使用可组合函数（Composables）封装并在 Uniapp 应用的多个组件间共享可复用的客户端逻辑或状态。

## 二、Uniapp 特定要求
- Uniapp 支持自动导入部分常用功能，无需手动导入如`ref`、`reactive`等（具体依实际情况）。
- 对于页面导航，使用`uni.navigateTo`、`uni.redirectTo`等内置导航函数，并可将相关逻辑封装在可组合函数中以便复用。
- 利用`uni-app`的生命周期函数进行页面初始化、数据加载等操作，如`onLoad`、`onShow`等，也可将相关逻辑提取到可组合函数中。
- 使用`uni.request`进行网络请求，并可封装成可组合函数，实现请求的统一处理、错误拦截等功能。例如：
```javascript
// 可组合函数示例：网络请求封装
import { ref } from 'vue';

export const useHttpRequest = (url, method = 'GET', data = {}) => {
  const loading = ref(false);
  const result = ref(null);
  const error = ref(null);

  const request = async () => {
    loading.value = true;
    try {
      const res = await uni.request({
        url,
        method,
        data,
      });
      result.value = res.data;
    } catch (e) {
      error.value = e;
    } finally {
      loading.value = false;
    }
  };

  return { loading, result, error, request };
};
```
- 使用`uni.setStorage`、`uni.getStorage`等存储相关函数进行本地数据存储，并封装成可组合函数方便使用。

## 三、数据获取
- 使用`uni.request`或封装后的可组合函数进行数据获取。
    - 对于需要在页面加载时获取数据且可能受益于服务器端渲染（如果 Uniapp 支持相关场景）的数据，在`onLoad`生命周期函数中调用数据获取函数。
    - 对于一些非关键数据的获取，可以设置延迟加载机制，例如在页面初次渲染完成后再进行请求，避免影响初始页面加载速度。

## 四、命名约定
- 可组合函数命名为`use<MyComposable>`形式。
- 组件文件名使用**PascalCase**（大驼峰命名法），例如`components/MyComponent.vue`。
- 函数尽量采用命名导出，以保持一致性和可读性。

## 五、TypeScript 使用（如果项目采用 TypeScript）
- 全面使用 TypeScript，优先使用接口（interface）而非类型别名（type），以获得更好的可扩展性和合并性。
- 避免使用枚举（enum），可采用对象字面量或映射类型等方式替代，提高类型安全性和灵活性。
- 使用带 TypeScript 接口的函数式组件。

## 六、UI 与样式
- 使用 Uniapp 官方 UI 组件库进行界面搭建。
- 遵循 Uniapp 官方 UI 组件库的样式规范和使用指南进行样式调整和定制。
- 利用 Uniapp 的样式类和 CSS 预处理器（如 SCSS）实现页面的样式设计，采用响应式设计理念，优先考虑移动端适配，确保应用在不同设备上的良好显示效果。 
- 组件文档：https://uniapp.dcloud.net.cn/component/