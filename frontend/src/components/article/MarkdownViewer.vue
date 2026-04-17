<template>
  <div ref="viewerRef" class="markdown-viewer" :class="{ 'dark-theme': isDark }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'

interface Props {
  content: string
}

const props = withDefaults(defineProps<Props>(), {
  content: ''
})

const viewerRef = ref<HTMLDivElement>()

// 检测当前主题
const isDark = computed(() => {
  return document.documentElement.getAttribute('data-theme') === 'dark'
})

const enhanceCodeBlocks = () => {
  if (!viewerRef.value) return
  const pres = viewerRef.value.querySelectorAll('pre')
  pres.forEach((pre) => {
    if (pre.dataset.enhanced === '1') return
    pre.dataset.enhanced = '1'

    const wrapper = document.createElement('div')
    wrapper.className = 'code-block-wrap'
    pre.parentNode?.insertBefore(wrapper, pre)
    wrapper.appendChild(pre)

    const code = pre.querySelector('code')
    const lang = Array.from(code?.classList || [])
      .find((c) => c.startsWith('language-'))
      ?.replace('language-', '') || ''

    if (lang) {
      const label = document.createElement('span')
      label.className = 'code-lang-label'
      label.textContent = lang
      wrapper.appendChild(label)
    }

    const btn = document.createElement('button')
    btn.className = 'code-copy-btn'
    btn.type = 'button'
    btn.setAttribute('aria-label', 'Copy code')
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>复制</span>`

    btn.addEventListener('click', async () => {
      const text = code?.textContent || ''
      try {
        await navigator.clipboard.writeText(text)
        btn.classList.add('copied')
        btn.querySelector('span')!.textContent = '已复制'
        setTimeout(() => {
          btn.classList.remove('copied')
          btn.querySelector('span')!.textContent = '复制'
        }, 1800)
      } catch {
        btn.querySelector('span')!.textContent = '失败'
      }
    })

    wrapper.appendChild(btn)
  })
}

const renderMarkdown = () => {
  if (!viewerRef.value) return

  Vditor.preview(viewerRef.value, props.content, {
    cdn: '/vditor',
    mode: 'light',
    theme: {
      current: isDark.value ? 'dark' : 'classic',
      path: '/vditor/dist/css/content-theme'
    },
    hljs: {
      style: isDark.value ? 'monokai' : 'github'
    },
    after: () => {
      setTimeout(enhanceCodeBlocks, 50)
    }
  })
  setTimeout(enhanceCodeBlocks, 1500)
}

let themeObserver: MutationObserver | null = null

onMounted(() => {
  renderMarkdown()

  // 监听主题变化
  themeObserver = new MutationObserver(() => {
    renderMarkdown()
  })

  themeObserver.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  })
})

onUnmounted(() => {
  themeObserver?.disconnect()
  themeObserver = null
})

watch(() => props.content, () => {
  renderMarkdown()
})
</script>

<style scoped>
.markdown-viewer {
  width: 100%;
  padding: 2.5rem;
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
}

/* 亮色主题 */
.markdown-viewer:not(.dark-theme) :deep(.vditor-reset) {
  color: #24292f;
}

/* 暗色主题 */
.markdown-viewer.dark-theme :deep(.vditor-reset) {
  color: #e6edf3;
}

:deep(.vditor-reset) {
  font-size: 16px;
  line-height: 1.8;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
}

/* 标题样式 */
:deep(.vditor-reset h1),
:deep(.vditor-reset h2),
:deep(.vditor-reset h3),
:deep(.vditor-reset h4),
:deep(.vditor-reset h5),
:deep(.vditor-reset h6) {
  color: var(--text-primary);
  font-weight: 700;
  line-height: 1.4;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
}

:deep(.vditor-reset h1) {
  font-size: 2em;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.4em;
}

:deep(.vditor-reset h2) {
  font-size: 1.5em;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.3em;
}

:deep(.vditor-reset h3) {
  font-size: 1.25em;
}

/* 段落 */
:deep(.vditor-reset p) {
  margin: 1.2em 0;
  color: var(--text-primary);
  line-height: 1.8;
}

/* 代码块 - 增强对比度 */
:deep(.vditor-reset pre) {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
  margin: 0;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* 代码块包装器 + 复制按钮 */
:deep(.code-block-wrap) {
  position: relative;
  margin: 1.5em 0;
}

:deep(.code-block-wrap:hover .code-copy-btn),
:deep(.code-block-wrap:hover .code-lang-label) {
  opacity: 1;
}

:deep(.code-lang-label) {
  position: absolute;
  top: 0.6rem;
  left: 0.8rem;
  padding: 0.15rem 0.55rem;
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-tertiary);
  background: rgba(129, 140, 248, 0.12);
  border-radius: 4px;
  opacity: 0.6;
  transition: opacity 0.2s;
  pointer-events: none;
  z-index: 2;
}

:deep(.code-copy-btn) {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.65rem;
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.2s;
  z-index: 2;
  font-family: inherit;
}

:deep(.code-copy-btn:hover) {
  color: var(--accent-primary);
  border-color: var(--accent-primary);
  background: rgba(129, 140, 248, 0.08);
}

:deep(.code-copy-btn.copied) {
  color: #10b981;
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.08);
  opacity: 1;
}

:deep(.code-copy-btn svg) { flex-shrink: 0; }

/* 行内代码 */
:deep(.vditor-reset code) {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  padding: 0.25em 0.5em;
  border-radius: 6px;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.9em;
  border: 1px solid var(--border-color);
}

:deep(.vditor-reset pre code) {
  background: transparent;
  padding: 0;
  border: none;
  font-size: 0.875em;
}

/* 引用块 - 更明显的样式 */
:deep(.vditor-reset blockquote) {
  border-left: 4px solid var(--accent-primary);
  background: var(--bg-secondary);
  padding: 1rem 1.5rem;
  margin: 1.5em 0;
  border-radius: 6px;
  color: var(--text-secondary);
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

:deep(.vditor-reset blockquote p) {
  margin: 0.5em 0;
  color: var(--text-secondary);
}

:deep(.vditor-reset blockquote p:first-child) {
  margin-top: 0;
}

:deep(.vditor-reset blockquote p:last-child) {
  margin-bottom: 0;
}

/* 链接 */
:deep(.vditor-reset a) {
  color: var(--accent-primary);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
  font-weight: 500;
}

:deep(.vditor-reset a:hover) {
  color: var(--accent-hover);
  border-bottom-color: var(--accent-hover);
}

/* 图片 */
:deep(.vditor-reset img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1.5em 0;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

/* 列表 */
:deep(.vditor-reset ul),
:deep(.vditor-reset ol) {
  padding-left: 2em;
  margin: 1em 0;
}

:deep(.vditor-reset li) {
  margin: 0.5em 0;
  color: var(--text-primary);
  line-height: 1.7;
}

:deep(.vditor-reset li::marker) {
  color: var(--text-secondary);
}

/* 表格 */
:deep(.vditor-reset table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5em 0;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

:deep(.vditor-reset th),
:deep(.vditor-reset td) {
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  text-align: left;
}

:deep(.vditor-reset th) {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-weight: 600;
}

:deep(.vditor-reset td) {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

:deep(.vditor-reset tr:hover td) {
  background: var(--bg-tertiary);
}

/* 分隔线 */
:deep(.vditor-reset hr) {
  border: none;
  border-top: 2px solid var(--border-color);
  margin: 2.5em 0;
}

/* 强调文本 */
:deep(.vditor-reset strong) {
  font-weight: 700;
  color: var(--text-primary);
}

:deep(.vditor-reset em) {
  font-style: italic;
  color: var(--text-secondary);
}

/* 删除线 */
:deep(.vditor-reset del) {
  text-decoration: line-through;
  color: var(--text-tertiary);
  opacity: 0.7;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .markdown-viewer {
    padding: 1.5rem;
  }

  :deep(.vditor-reset) {
    font-size: 15px;
  }

  :deep(.vditor-reset h1) {
    font-size: 1.75em;
  }

  :deep(.vditor-reset h2) {
    font-size: 1.4em;
  }

  :deep(.vditor-reset pre) {
    padding: 1rem;
  }

  :deep(.vditor-reset blockquote) {
    padding: 0.75rem 1rem;
  }
}
</style>
