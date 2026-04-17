<template>
  <aside v-if="items.length > 0" class="article-toc" :class="{ visible: showToc }">
    <div class="toc-header">
      <span class="toc-title">目录</span>
      <span class="toc-count">{{ items.length }}</span>
    </div>
    <nav class="toc-list">
      <a
        v-for="item in items"
        :key="item.id"
        :href="'#' + item.id"
        class="toc-item"
        :class="[`level-${item.level}`, { active: activeId === item.id }]"
        @click.prevent="scrollTo(item.id)"
      >
        <span class="toc-dot"></span>
        <span class="toc-text">{{ item.text }}</span>
      </a>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'

interface Props {
  targetSelector: string
  contentKey?: string | number
}

const props = withDefaults(defineProps<Props>(), {
  contentKey: '',
})

interface TocItem {
  id: string
  text: string
  level: number
}

const items = ref<TocItem[]>([])
const activeId = ref('')
const showToc = ref(false)
let observer: IntersectionObserver | null = null
let scanTimer: number | null = null

const slugify = (text: string, index: number) => {
  const base = text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5\s-]/g, '')
    .replace(/\s+/g, '-')
    .slice(0, 40)
  return `toc-${index}-${base || 'heading'}`
}

const collectHeadings = () => {
  const container = document.querySelector(props.targetSelector)
  if (!container) return

  const headings = container.querySelectorAll<HTMLElement>('h1, h2, h3')
  const collected: TocItem[] = []

  headings.forEach((h, i) => {
    if (!h.id) h.id = slugify(h.textContent || '', i)
    collected.push({
      id: h.id,
      text: h.textContent || '',
      level: parseInt(h.tagName.slice(1)),
    })
  })

  items.value = collected
  showToc.value = collected.length > 1
  setupObserver(headings)
}

const setupObserver = (headings: NodeListOf<HTMLElement>) => {
  observer?.disconnect()
  observer = new IntersectionObserver(
    (entries) => {
      const visible = entries.filter((e) => e.isIntersecting)
      if (visible.length > 0) {
        activeId.value = visible[0].target.id
      }
    },
    { rootMargin: '-80px 0px -70% 0px', threshold: 0 }
  )
  headings.forEach((h) => observer!.observe(h))
}

const scrollTo = (id: string) => {
  const el = document.getElementById(id)
  if (!el) return
  const y = el.getBoundingClientRect().top + window.scrollY - 80
  window.scrollTo({ top: y, behavior: 'smooth' })
  activeId.value = id
}

const scheduleScan = () => {
  if (scanTimer) window.clearTimeout(scanTimer)
  scanTimer = window.setTimeout(() => {
    collectHeadings()
  }, 400)
}

onMounted(() => {
  nextTick(scheduleScan)
  const container = document.querySelector(props.targetSelector)
  if (container) {
    const mo = new MutationObserver(scheduleScan)
    mo.observe(container, { childList: true, subtree: true })
    onUnmounted(() => mo.disconnect())
  }
})

watch(() => props.contentKey, scheduleScan)

onUnmounted(() => {
  observer?.disconnect()
  if (scanTimer) window.clearTimeout(scanTimer)
})
</script>

<style scoped>
.article-toc {
  position: fixed;
  top: 90px;
  right: max(1.5rem, calc((100vw - 780px) / 2 - 260px));
  width: 220px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  padding: 1rem 0.75rem;
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--card-border);
  border-radius: 10px;
  opacity: 0;
  transform: translateX(20px);
  transition: opacity 0.4s, transform 0.4s;
  z-index: 50;
}

.article-toc.visible {
  opacity: 1;
  transform: translateX(0);
}

.toc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.5rem 0.6rem;
  border-bottom: 1px solid var(--card-border);
  margin-bottom: 0.5rem;
}

.toc-title {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-tertiary);
}

.toc-count {
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 10px;
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
  font-weight: 600;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.toc-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.5rem;
  font-size: 0.78rem;
  color: var(--text-tertiary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  cursor: pointer;
  line-height: 1.4;
}

.toc-item.level-1 { font-weight: 600; }
.toc-item.level-2 { padding-left: 1rem; }
.toc-item.level-3 { padding-left: 1.6rem; font-size: 0.74rem; }

.toc-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--border-color);
  flex-shrink: 0;
  transition: all 0.2s;
}

.toc-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toc-item:hover {
  background: rgba(129, 140, 248, 0.08);
  color: var(--accent-primary);
}

.toc-item:hover .toc-dot {
  background: var(--accent-primary);
}

.toc-item.active {
  background: rgba(129, 140, 248, 0.15);
  color: var(--accent-primary);
  font-weight: 600;
}

.toc-item.active .toc-dot {
  background: var(--accent-primary);
  box-shadow: 0 0 8px rgba(129, 140, 248, 0.6);
  transform: scale(1.5);
}

@media (max-width: 1280px) {
  .article-toc { display: none; }
}
</style>
