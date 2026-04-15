---
feature: home-page-redesign
phase: tasks
generated_at: 2026-01-27T03:10:00+08:00
version: 1
---

# 任务清单: 首页欢迎界面重设计

> **功能标识**: home-page-redesign
> **任务拆分阶段**: Phase 3
> **生成时间**: 2026-01-27 03:10

## 任务概览

| 优先级 | 任务数量 | 预计工作量 |
|--------|---------|-----------|
| P0 (核心功能) | 6 | 核心开发 |
| P1 (增强功能) | 4 | 增强体验 |
| P2 (测试文档) | 4 | 质量保证 |
| **总计** | **14** | **完整实现** |

---

## P0 任务（核心功能）

### T-001: 安装依赖包

**描述**: 安装项目所需的新依赖包

**依赖**: 无

**验收标准**:
- [ ] tsparticles 和 @tsparticles/vue3 已安装
- [ ] GSAP 已安装
- [ ] sass 已安装
- [ ] package.json 已更新
- [ ] 依赖安装无错误

**实施步骤**:
1. 在 frontend 目录执行 `npm install tsparticles @tsparticles/vue3 gsap`
2. 安装 sass: `npm install -D sass`
3. 验证安装: `npm list tsparticles gsap sass`

**关联文件**:
- `frontend/package.json`

---

### T-002: 创建基础组件结构和类型定义

**描述**: 创建组件目录结构、类型定义文件和 composables

**依赖**: T-001

**验收标准**:
- [ ] 组件目录结构已创建
- [ ] 类型定义文件已创建
- [ ] Composables 文件已创建
- [ ] 所有文件有基础的 TypeScript 类型定义

**实施步骤**:
1. 创建组件目录: `frontend/src/pages/home/components/`
2. 创建类型定义: `frontend/src/types/home.ts`
3. 创建 composables: `frontend/src/composables/useTheme.ts`, `useDeviceDetect.ts`, `useParticles.ts`
4. 创建样式目录: `frontend/src/styles/home/`

**关联文件**:
- `frontend/src/pages/home/components/` (新建目录)
- `frontend/src/types/home.ts` (新建)
- `frontend/src/composables/useTheme.ts` (新建)
- `frontend/src/composables/useDeviceDetect.ts` (新建)
- `frontend/src/composables/useParticles.ts` (新建)
- `frontend/src/styles/home/` (新建目录)

---

### T-003: 实现粒子背景组件

**描述**: 实现粒子背景组件，支持主题切换和设备适配

**依赖**: T-002

**验收标准**:
- [ ] ParticleBackground.vue 组件已创建
- [ ] 粒子动画正常运行
- [ ] 根据设备类型动态调整粒子数量
- [ ] 支持主题切换（亮色/暗色）
- [ ] 性能良好（60fps）

**实施步骤**:
1. 创建 `ParticleBackground.vue` 组件
2. 配置 tsparticles 参数
3. 实现设备检测逻辑，动态调整粒子数量
4. 实现主题切换逻辑
5. 测试性能和视觉效果

**关联文件**:
- `frontend/src/pages/home/components/ParticleBackground.vue` (新建)
- `frontend/src/composables/useParticles.ts` (修改)

---

### T-004: 实现欢迎标语区域

**描述**: 实现欢迎标语区域，包含主标题和副标题，带淡入动画

**依赖**: T-002

**验收标准**:
- [ ] WelcomeSection.vue 组件已创建
- [ ] 主标题和副标题正常显示
- [ ] 淡入动画流畅
- [ ] 响应式字体大小适配
- [ ] 支持主题切换

**实施步骤**:
1. 创建 `WelcomeSection.vue` 组件
2. 实现主标题和副标题布局
3. 使用 GSAP 实现淡入动画
4. 实现响应式字体大小
5. 测试动画效果

**关联文件**:
- `frontend/src/pages/home/components/WelcomeSection.vue` (新建)

---

### T-005: 实现导航按钮组

**描述**: 实现导航按钮组，支持跳转到 Tech、Life、Projects 页面

**依赖**: T-002

**验收标准**:
- [ ] NavigationButtons.vue 组件已创建
- [ ] 三个导航按钮正常显示
- [ ] 点击按钮正确跳转
- [ ] 悬停动画效果流畅
- [ ] 响应式布局（桌面横排，移动端竖排）

**实施步骤**:
1. 创建 `NavigationButtons.vue` 组件
2. 实现按钮布局和样式
3. 实现路由跳转逻辑
4. 实现悬停动画效果
5. 实现响应式布局
6. 测试跳转功能

**关联文件**:
- `frontend/src/pages/home/components/NavigationButtons.vue` (新建)

---

### T-006: 实现响应式布局和整合首页

**描述**: 整合所有组件到首页，实现响应式布局

**依赖**: T-003, T-004, T-005

**验收标准**:
- [ ] Index.vue 已更新，整合所有子组件
- [ ] 响应式布局在所有设备上正常
- [ ] 桌面端、平板端、移动端布局正确
- [ ] 所有组件协调工作
- [ ] 页面加载流畅

**实施步骤**:
1. 更新 `Index.vue`，导入所有子组件
2. 实现整体布局结构
3. 实现响应式媒体查询
4. 测试不同设备上的显示效果
5. 优化布局和间距

**关联文件**:
- `frontend/src/pages/home/Index.vue` (修改)
- `frontend/src/styles/home/home.scss` (新建)

---

## P1 任务（增强功能）

### T-007: 实现鼠标跟随光晕效果

**描述**: 实现鼠标跟随光晕效果，仅在桌面端启用

**依赖**: T-006

**验收标准**:
- [ ] MouseFollower.vue 组件已创建
- [ ] 鼠标跟随效果流畅
- [ ] 仅在桌面端启用
- [ ] 移动端自动禁用
- [ ] 性能良好，无卡顿

**实施步骤**:
1. 创建 `MouseFollower.vue` 组件
2. 实现鼠标位置追踪
3. 使用 requestAnimationFrame 优化性能
4. 实现设备检测，移动端禁用
5. 测试性能和视觉效果

**关联文件**:
- `frontend/src/pages/home/components/MouseFollower.vue` (新建)

---

### T-008: 实现主题切换功能

**描述**: 实现亮色/暗色主题切换功能

**依赖**: T-006

**验收标准**:
- [ ] 主题 store 已创建
- [ ] 主题切换功能正常
- [ ] 主题状态持久化（localStorage）
- [ ] 所有组件响应主题切换
- [ ] 切换动画流畅

**实施步骤**:
1. 创建主题 store (Pinia)
2. 实现主题切换逻辑
3. 实现 localStorage 持久化
4. 更新所有组件支持主题切换
5. 实现切换过渡动画
6. 测试主题切换功能

**关联文件**:
- `frontend/src/stores/theme.ts` (新建)
- `frontend/src/composables/useTheme.ts` (修改)
- `frontend/src/styles/themes/_dark.scss` (新建)
- `frontend/src/styles/themes/_light.scss` (新建)

---

### T-009: 添加页面加载动画

**描述**: 添加页面加载时的入场动画效果

**依赖**: T-006

**验收标准**:
- [ ] 页面加载动画已实现
- [ ] 元素依次淡入
- [ ] 动画时序合理
- [ ] 动画流畅自然
- [ ] 不影响页面性能

**实施步骤**:
1. 使用 GSAP 实现页面加载动画
2. 设置元素淡入时序
3. 优化动画参数
4. 测试动画效果
5. 确保性能良好

**关联文件**:
- `frontend/src/pages/home/Index.vue` (修改)

---

### T-010: 性能优化和代码分割

**描述**: 优化性能，实现代码分割和懒加载

**依赖**: T-007, T-008, T-009

**验收标准**:
- [ ] 粒子组件懒加载
- [ ] GSAP 按需导入
- [ ] 首屏加载时间 < 2 秒
- [ ] Lighthouse 性能评分 > 90
- [ ] 无性能警告

**实施步骤**:
1. 实现组件懒加载
2. 优化依赖导入
3. 使用 Vite 代码分割
4. 运行 Lighthouse 测试
5. 根据报告优化性能

**关联文件**:
- `frontend/src/pages/home/Index.vue` (修改)
- `frontend/vite.config.ts` (可能修改)

---

## P2 任务（测试和文档）

### T-011: 编写单元测试

**描述**: 为 composables 和工具函数编写单元测试

**依赖**: T-010

**验收标准**:
- [ ] useTheme 测试已编写
- [ ] useDeviceDetect 测试已编写
- [ ] useParticles 测试已编写
- [ ] 测试覆盖率 > 80%
- [ ] 所有测试通过

**实施步骤**:
1. 创建测试文件
2. 编写 composables 测试用例
3. 运行测试并确保通过
4. 检查测试覆盖率
5. 补充缺失的测试用例

**关联文件**:
- `frontend/src/composables/__tests__/useTheme.spec.ts` (新建)
- `frontend/src/composables/__tests__/useDeviceDetect.spec.ts` (新建)
- `frontend/src/composables/__tests__/useParticles.spec.ts` (新建)

---

### T-012: 编写 E2E 测试

**描述**: 使用 Playwright 编写端到端测试

**依赖**: T-010

**验收标准**:
- [ ] 首页加载测试已编写
- [ ] 导航跳转测试已编写
- [ ] 主题切换测试已编写
- [ ] 响应式测试已编写
- [ ] 所有 E2E 测试通过

**实施步骤**:
1. 创建 E2E 测试文件
2. 编写首页加载测试
3. 编写导航功能测试
4. 编写主题切换测试
5. 编写响应式测试
6. 运行测试并确保通过

**关联文件**:
- `tests/e2e/home.spec.ts` (新建)

---

### T-013: 性能测试和优化

**描述**: 进行性能测试，确保达到性能目标

**依赖**: T-012

**验收标准**:
- [ ] Lighthouse 性能评分 > 90
- [ ] 首屏加载时间 < 2 秒
- [ ] 动画帧率保持 60fps
- [ ] 无性能警告
- [ ] 移动端性能良好

**实施步骤**:
1. 运行 Lighthouse 测试
2. 分析性能报告
3. 优化性能瓶颈
4. 测试不同设备性能
5. 确保达到性能目标

**关联文件**:
- 所有相关组件文件

---

### T-014: 更新文档和注释

**描述**: 完善代码注释和更新相关文档

**依赖**: T-013

**验收标准**:
- [ ] 所有组件有完整的注释
- [ ] 所有函数有 JSDoc 注释
- [ ] README 已更新
- [ ] 技术文档已更新
- [ ] 无遗漏的 TODO 注释

**实施步骤**:
1. 检查所有组件注释
2. 补充缺失的注释
3. 更新 README 文档
4. 更新技术文档
5. 清理 TODO 注释

**关联文件**:
- 所有相关文件
- `README.md` (修改)
- `docs/dev/home-page-redesign/` (更新)

---

## 任务依赖关系图

```
T-001 (安装依赖)
  ↓
T-002 (基础结构)
  ↓
  ├─→ T-003 (粒子背景)
  ├─→ T-004 (欢迎标语)
  └─→ T-005 (导航按钮)
       ↓
     T-006 (响应式整合)
       ↓
       ├─→ T-007 (鼠标跟随)
       ├─→ T-008 (主题切换)
       └─→ T-009 (加载动画)
            ↓
          T-010 (性能优化)
            ↓
            ├─→ T-011 (单元测试)
            └─→ T-012 (E2E 测试)
                 ↓
               T-013 (性能测试)
                 ↓
               T-014 (文档更新)
```

---

## 实施建议

### 第一阶段：基础功能（T-001 ~ T-006）

**目标**：完成核心功能，实现基本的首页展示

**预计时间**：2-3 天

**关键里程碑**：
- 粒子背景正常运行
- 欢迎标语和导航按钮显示正常
- 响应式布局适配完成

### 第二阶段：增强功能（T-007 ~ T-010）

**目标**：添加交互特效和性能优化

**预计时间**：1-2 天

**关键里程碑**：
- 鼠标跟随效果流畅
- 主题切换功能正常
- 性能达标（< 2 秒加载，60fps 动画）

### 第三阶段：测试和完善（T-011 ~ T-014）

**目标**：确保质量，完善文档

**预计时间**：1-2 天

**关键里程碑**：
- 所有测试通过
- 性能评分 > 90
- 文档完整

---

## 验收清单

### 功能验收

- [ ] 首页加载正常，无错误
- [ ] 粒子背景动画流畅
- [ ] 欢迎标语显示正确
- [ ] 三个导航按钮功能正常
- [ ] 鼠标跟随效果流畅（桌面端）
- [ ] 主题切换功能正常
- [ ] 响应式布局在所有设备上正常

### 性能验收

- [ ] 首屏加载时间 < 2 秒
- [ ] 动画帧率保持 60fps
- [ ] Lighthouse 性能评分 > 90
- [ ] 移动端性能良好
- [ ] 无性能警告

### 质量验收

- [ ] 所有单元测试通过
- [ ] 所有 E2E 测试通过
- [ ] 代码覆盖率 > 80%
- [ ] 无 ESLint 错误
- [ ] 无 TypeScript 错误

### 文档验收

- [ ] 所有组件有完整注释
- [ ] README 已更新
- [ ] 技术文档已更新
- [ ] 无遗漏的 TODO

---

## 总结

本任务清单包含 14 个任务，分为三个优先级：

- **P0 任务（6 个）**：核心功能，必须完成
- **P1 任务（4 个）**：增强功能，提升体验
- **P2 任务（4 个）**：测试和文档，确保质量

**预计总工作量**：4-7 天

**关键成功因素**：
1. 严格按照任务依赖顺序执行
2. 每个任务完成后进行验收
3. 及时发现和解决性能问题
4. 保持代码质量和文档完整性

**下一步**：开始执行 T-001（安装依赖包）

