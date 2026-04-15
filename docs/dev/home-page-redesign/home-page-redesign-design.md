---
feature: home-page-redesign
phase: design
generated_at: 2026-01-27T03:00:00+08:00
version: 1
---

# 技术设计文档: 首页欢迎界面重设计

> **功能标识**: home-page-redesign
> **设计阶段**: Phase 2
> **生成时间**: 2026-01-27 03:00

## 1. 设计概述

### 1.1 设计目标

将当前简单的首页占位页面改造为具有科技感的炫酷欢迎界面，实现以下核心目标：

1. **视觉冲击力**：通过渐变背景、粒子动画、流畅过渡等视觉元素营造科技感
2. **快速导航**：提供清晰的导航按钮，快速跳转到 Tech、Life、Projects 板块
3. **性能优化**：确保动画流畅（60fps），首屏加载时间 < 2 秒
4. **响应式设计**：适配桌面、平板、移动端，根据设备性能动态调整动画复杂度
5. **主题支持**：支持亮色/暗色主题切换，保持视觉协调性

### 1.2 技术选型

基于现有技术栈和需求分析，选择以下技术方案：

| 技术领域 | 选型 | 理由 |
|---------|------|------|
| 前端框架 | Vue 3 + TypeScript | 项目已使用，保持技术栈一致性 |
| UI 组件库 | Element Plus | 项目已使用，可选用于按钮等基础组件 |
| 粒子动画 | tsparticles | 轻量级、性能好、配置灵活、TypeScript 支持 |
| 动画库 | GSAP | 业界标准、性能优秀、API 友好 |
| CSS 预处理 | SCSS | 支持变量、嵌套、混合，便于主题管理 |
| 状态管理 | Pinia | 项目已使用，用于主题状态管理 |

### 1.3 架构设计原则

1. **组件化**：将首页拆分为独立的可复用组件
2. **性能优先**：使用懒加载、代码分割、动态导入优化性能
3. **渐进增强**：确保基础功能在所有浏览器可用，高级特效作为增强
4. **可维护性**：清晰的代码结构、完善的类型定义、充分的注释

---

## 2. 组件架构设计

### 2.1 组件层次结构

```
HomePage (Index.vue)
├── ParticleBackground.vue      # 粒子背景组件
├── WelcomeSection.vue          # 欢迎标语区域
│   ├── MainTitle.vue           # 主标题
│   └── SubTitle.vue            # 副标题
├── NavigationButtons.vue       # 导航按钮组
│   └── NavButton.vue           # 单个导航按钮
└── MouseFollower.vue           # 鼠标跟随光晕效果
```

### 2.2 核心组件设计

#### 2.2.1 HomePage (Index.vue)

**职责**：
- 作为首页的容器组件
- 管理整体布局和主题状态
- 协调各子组件的交互

**关键属性**：
```typescript
interface HomePageProps {
  // 无外部 props，使用内部状态管理
}

interface HomePageState {
  theme: 'light' | 'dark'
  isMobile: boolean
  isTablet: boolean
  isDesktop: boolean
}
```

#### 2.2.2 ParticleBackground.vue

**职责**：
- 渲染粒子动画背景
- 根据设备类型调整粒子数量
- 响应主题切换

**关键属性**：
```typescript
interface ParticleBackgroundProps {
  theme: 'light' | 'dark'
  particleCount?: number  // 可选，默认根据设备自动计算
}
```

**性能优化**：
- 桌面端：100-150 粒子
- 平板端：50-80 粒子
- 移动端：30-50 粒子

#### 2.2.3 WelcomeSection.vue

**职责**：
- 展示欢迎标语（主标题 + 副标题）
- 实现标语的淡入动画
- 响应式字体大小调整

**关键属性**：
```typescript
interface WelcomeSectionProps {
  mainTitle: string    // 主标题：「探索 · 创造 · 分享」
  subTitle: string     // 副标题：「在代码与生活的交汇处，记录思考的轨迹」
}
```

**动画效果**：
- 页面加载后 0.5s 开始淡入
- 主标题先出现，副标题延迟 0.3s
- 使用 GSAP 实现流畅动画

#### 2.2.4 NavigationButtons.vue

**职责**：
- 渲染三个导航按钮（Tech、Life、Projects）
- 管理按钮的悬停和点击效果
- 响应式布局（桌面横排，移动端竖排）

**关键属性**：
```typescript
interface NavigationButton {
  label: string
  route: string
  icon?: string
  color: string
}

interface NavigationButtonsProps {
  buttons: NavigationButton[]
}
```

**默认按钮配置**：
```typescript
const defaultButtons = [
  { label: 'Tech 技术博客', route: '/tech', color: '#409EFF' },
  { label: 'Life 生活随笔', route: '/life', color: '#67C23A' },
  { label: 'Projects 项目展示', route: '/projects', color: '#E6A23C' }
]
```

#### 2.2.5 MouseFollower.vue

**职责**：
- 实现鼠标跟随光晕效果
- 仅在桌面端启用
- 使用 requestAnimationFrame 优化性能

**关键属性**：
```typescript
interface MouseFollowerProps {
  enabled: boolean  // 是否启用（移动端禁用）
  size?: number     // 光晕大小，默认 200px
  opacity?: number  // 光晕透明度，默认 0.3
}
```

---

## 3. 技术实现方案

### 3.1 粒子动画实现

**使用 tsparticles**：

```typescript
// 粒子配置示例
const particlesConfig = {
  particles: {
    number: {
      value: 100, // 根据设备动态调整
      density: { enable: true, value_area: 800 }
    },
    color: { value: '#409EFF' }, // 根据主题动态调整
    shape: { type: 'circle' },
    opacity: {
      value: 0.5,
      random: true,
      anim: { enable: true, speed: 1, opacity_min: 0.1 }
    },
    size: {
      value: 3,
      random: true,
      anim: { enable: true, speed: 2, size_min: 0.1 }
    },
    move: {
      enable: true,
      speed: 1,
      direction: 'none',
      random: false,
      straight: false,
      out_mode: 'out',
      bounce: false
    }
  },
  interactivity: {
    detect_on: 'canvas',
    events: {
      onhover: { enable: true, mode: 'repulse' },
      onclick: { enable: true, mode: 'push' }
    }
  }
}
```

**性能优化策略**：
1. 根据设备性能动态调整粒子数量
2. 使用 Web Worker 处理粒子计算（如果需要）
3. 移动端降低粒子数量和交互复杂度

### 3.2 动画实现方案

**使用 GSAP 实现页面元素动画**：

```typescript
// 欢迎标语淡入动画
gsap.from('.main-title', {
  opacity: 0,
  y: -50,
  duration: 1,
  delay: 0.5,
  ease: 'power3.out'
})

gsap.from('.sub-title', {
  opacity: 0,
  y: -30,
  duration: 1,
  delay: 0.8,
  ease: 'power3.out'
})

// 导航按钮依次出现
gsap.from('.nav-button', {
  opacity: 0,
  scale: 0.8,
  duration: 0.6,
  stagger: 0.2,
  delay: 1.2,
  ease: 'back.out(1.7)'
})
```

### 3.3 主题系统设计

**主题变量定义**：

```scss
// 暗色主题
$dark-theme: (
  bg-primary: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%),
  bg-secondary: #0f3460,
  text-primary: #eaeaea,
  text-secondary: #a0a0a0,
  accent-color: #409EFF,
  particle-color: #409EFF,
  glow-color: rgba(64, 158, 255, 0.3)
);

// 亮色主题
$light-theme: (
  bg-primary: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%),
  bg-secondary: #ffffff,
  text-primary: #2c3e50,
  text-secondary: #606266,
  accent-color: #409EFF,
  particle-color: #409EFF,
  glow-color: rgba(64, 158, 255, 0.2)
);
```

**主题切换实现**：
- 使用 Pinia store 管理主题状态
- CSS 变量动态切换
- 平滑过渡动画（transition: all 0.3s ease）

### 3.4 响应式设计方案

**断点定义**：

```scss
$breakpoints: (
  mobile: 768px,
  tablet: 1024px,
  desktop: 1440px
);

// 媒体查询混合
@mixin mobile {
  @media (max-width: #{map-get($breakpoints, mobile) - 1px}) {
    @content;
  }
}

@mixin tablet {
  @media (min-width: #{map-get($breakpoints, mobile)}) and (max-width: #{map-get($breakpoints, tablet) - 1px}) {
    @content;
  }
}

@mixin desktop {
  @media (min-width: #{map-get($breakpoints, tablet)}) {
    @content;
  }
}
```

**响应式策略**：

| 设备类型 | 布局调整 | 动画调整 | 粒子数量 |
|---------|---------|---------|---------|
| 桌面端 (>1024px) | 横向布局，大字体 | 完整动画效果 | 100-150 |
| 平板端 (768-1024px) | 横向布局，中等字体 | 简化动画 | 50-80 |
| 移动端 (<768px) | 纵向布局，小字体 | 最简动画 | 30-50 |

---

## 4. 文件结构设计

### 4.1 新增文件清单

```
frontend/src/
├── pages/
│   └── home/
│       ├── Index.vue                    # 首页主组件（修改）
│       └── components/
│           ├── ParticleBackground.vue   # 粒子背景组件
│           ├── WelcomeSection.vue       # 欢迎标语区域
│           ├── NavigationButtons.vue    # 导航按钮组
│           └── MouseFollower.vue        # 鼠标跟随效果
├── composables/
│   ├── useTheme.ts                      # 主题管理 composable
│   ├── useDeviceDetect.ts               # 设备检测 composable
│   └── useParticles.ts                  # 粒子配置 composable
├── styles/
│   ├── home/
│   │   ├── _variables.scss              # 首页变量
│   │   ├── _mixins.scss                 # 首页混合
│   │   └── home.scss                    # 首页样式
│   └── themes/
│       ├── _dark.scss                   # 暗色主题
│       └── _light.scss                  # 亮色主题
└── types/
    └── home.ts                          # 首页类型定义
```

### 4.2 依赖包管理

**需要安装的新依赖**：

```json
{
  "dependencies": {
    "tsparticles": "^3.0.0",
    "@tsparticles/vue3": "^3.0.0",
    "gsap": "^3.12.0"
  },
  "devDependencies": {
    "sass": "^1.69.0"
  }
}
```

---

## 5. 数据流与状态管理

### 5.1 主题状态管理

**使用 Pinia Store**：

```typescript
// stores/theme.ts
export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: 'dark' as 'light' | 'dark',
    systemPreference: 'dark' as 'light' | 'dark'
  }),

  actions: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark'
      this.applyTheme()
    },

    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.currentTheme)
      localStorage.setItem('theme', this.currentTheme)
    }
  }
})
```

### 5.2 设备检测逻辑

```typescript
// composables/useDeviceDetect.ts
export function useDeviceDetect() {
  const isMobile = ref(false)
  const isTablet = ref(false)
  const isDesktop = ref(false)

  const detectDevice = () => {
    const width = window.innerWidth
    isMobile.value = width < 768
    isTablet.value = width >= 768 && width < 1024
    isDesktop.value = width >= 1024
  }

  onMounted(() => {
    detectDevice()
    window.addEventListener('resize', detectDevice)
  })

  return { isMobile, isTablet, isDesktop }
}
```

---

## 6. 性能优化策略

### 6.1 代码分割与懒加载

```typescript
// 动态导入粒子组件
const ParticleBackground = defineAsyncComponent(() =>
  import('./components/ParticleBackground.vue')
)

// 动态导入 GSAP
const loadGSAP = async () => {
  const { gsap } = await import('gsap')
  return gsap
}
```

### 6.2 资源优化

1. **粒子库按需加载**：仅加载需要的粒子效果模块
2. **图片优化**：使用 WebP 格式，提供降级方案
3. **字体优化**：使用系统字体栈，避免额外字体加载

### 6.3 渲染优化

1. **使用 requestAnimationFrame**：优化动画性能
2. **防抖和节流**：优化 resize 和 scroll 事件
3. **CSS 硬件加速**：使用 transform 和 opacity 实现动画

### 6.4 性能监控

```typescript
// 性能监控
const measurePerformance = () => {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log(`${entry.name}: ${entry.duration}ms`)
    }
  })
  observer.observe({ entryTypes: ['measure'] })
}
```

---

## 7. 测试策略

### 7.1 单元测试

**测试范围**：
- Composables 函数（useTheme, useDeviceDetect）
- 工具函数
- 组件 props 验证

**测试工具**：Vitest + @vue/test-utils

### 7.2 E2E 测试

**测试场景**：
- 首页加载和渲染
- 导航按钮点击跳转
- 主题切换功能
- 响应式布局适配
- 动画性能测试

**测试工具**：Playwright

---

## 8. 任务拆分建议

### 8.1 任务优先级分组

**P0 任务（核心功能）**：
- T-001: 安装依赖包（tsparticles, GSAP, sass）
- T-002: 创建基础组件结构和类型定义
- T-003: 实现粒子背景组件
- T-004: 实现欢迎标语区域
- T-005: 实现导航按钮组
- T-006: 实现响应式布局

**P1 任务（增强功能）**：
- T-007: 实现鼠标跟随光晕效果
- T-008: 实现主题切换功能
- T-009: 添加页面加载动画
- T-010: 性能优化和代码分割

**P2 任务（测试和文档）**：
- T-011: 编写单元测试
- T-012: 编写 E2E 测试
- T-013: 性能测试和优化
- T-014: 更新文档和注释

### 8.2 任务依赖关系

```
T-001 (安装依赖)
  ↓
T-002 (基础结构) → T-003 (粒子背景)
  ↓                    ↓
T-004 (欢迎标语)    T-007 (鼠标跟随)
  ↓                    ↓
T-005 (导航按钮) → T-006 (响应式)
  ↓
T-008 (主题切换) → T-009 (加载动画)
  ↓
T-010 (性能优化)
  ↓
T-011/T-012/T-013 (测试)
  ↓
T-014 (文档)
```

---

## 9. 风险评估与缓解

### 9.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 粒子动画性能问题 | 高 | 中 | 根据设备动态调整粒子数量，移动端简化 |
| 浏览器兼容性问题 | 中 | 低 | 使用渐进增强，提供降级方案 |
| 首屏加载时间过长 | 高 | 中 | 代码分割、懒加载、CDN 加速 |
| GSAP 库体积较大 | 中 | 高 | 按需导入，仅加载使用的模块 |

### 9.2 用户体验风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 动画过于炫酷分散注意力 | 中 | 中 | 适度使用动画，确保不影响内容阅读 |
| 移动端体验不佳 | 高 | 中 | 充分测试移动端，简化动画效果 |
| 主题切换不流畅 | 低 | 低 | 使用 CSS 过渡动画，确保平滑切换 |

---

## 10. 实施建议

### 10.1 开发顺序

1. **第一阶段**：基础功能（T-001 ~ T-006）
   - 搭建基础组件结构
   - 实现核心视觉效果
   - 完成响应式布局

2. **第二阶段**：增强功能（T-007 ~ T-010）
   - 添加交互特效
   - 实现主题切换
   - 性能优化

3. **第三阶段**：测试和完善（T-011 ~ T-014）
   - 编写测试用例
   - 性能测试
   - 文档完善

### 10.2 质量保证

1. **代码审查**：每个任务完成后进行代码审查
2. **性能测试**：使用 Lighthouse 进行性能评分
3. **跨浏览器测试**：在主流浏览器中测试
4. **设备测试**：在不同尺寸设备上测试

### 10.3 上线检查清单

- [ ] 所有 P0 功能已实现并测试通过
- [ ] 首屏加载时间 < 2 秒
- [ ] 动画帧率保持 60fps
- [ ] 响应式布局在所有设备上正常
- [ ] 主题切换功能正常
- [ ] E2E 测试全部通过
- [ ] 性能评分 > 90 分
- [ ] 无控制台错误和警告

---

## 11. 总结

本技术设计文档详细规划了首页欢迎界面的重设计方案，包括：

1. **组件架构**：清晰的组件层次和职责划分
2. **技术选型**：基于现有技术栈，选择合适的动画库
3. **性能优化**：多层次的性能优化策略
4. **响应式设计**：全面的设备适配方案
5. **任务拆分**：14 个可执行的开发任务

**预期成果**：
- 视觉冲击力强的科技感欢迎界面
- 流畅的动画效果（60fps）
- 快速的加载速度（< 2 秒）
- 完善的响应式支持
- 良好的用户体验

**下一步**：进入任务拆分阶段，生成详细的任务清单。

