<template>
  <el-dialog
    v-model="visible"
    :title="project?.name || '项目详情'"
    width="920px"
    top="6vh"
    destroy-on-close
    class="project-detail-dialog"
  >
    <div v-if="project" class="detail-body">
      <!-- Cover -->
      <div v-if="project.cover_image" class="detail-cover">
        <img :src="project.cover_image" :alt="project.name" />
      </div>

      <!-- Meta -->
      <div class="detail-meta">
        <span class="meta-status" :class="'status-' + project.status">
          <span class="dot" :class="'dot-' + project.status"></span>
          {{ statusLabels[project.status] || project.status }}
        </span>
        <span v-if="dateRange" class="meta-date">{{ dateRange }}</span>
        <span class="meta-spacer"></span>
        <a v-if="project.demo_url" :href="project.demo_url" target="_blank" class="meta-link">Demo →</a>
        <a v-if="project.github_url" :href="project.github_url" target="_blank" class="meta-link">GitHub →</a>
      </div>

      <!-- Tech stack -->
      <div v-if="project.tech_stack?.length" class="detail-section">
        <div class="tech-tags">
          <span v-for="t in project.tech_stack" :key="t" class="tech-tag">{{ t }}</span>
        </div>
      </div>

      <!-- Highlights -->
      <div v-if="project.highlights?.length" class="detail-section">
        <h4 class="section-title">亮点</h4>
        <ul class="highlight-list">
          <li v-for="(h, i) in project.highlights" :key="i">{{ h }}</li>
        </ul>
      </div>

      <!-- Markdown description -->
      <div v-if="project.description" class="detail-section">
        <h4 class="section-title">项目描述</h4>
        <div ref="mdRef" class="md-render"></div>
      </div>
    </div>

    <template #footer>
      <el-button @click="visible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch, nextTick, onBeforeUnmount } from 'vue'
import Vditor from 'vditor'
import 'vditor/dist/index.css'
import type { Project } from '@/api/project'

const props = defineProps<{ modelValue: boolean; project: Project | null }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: boolean): void }>()

const visible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v)
})

const mdRef = ref<HTMLDivElement | null>(null)

const statusLabels: Record<string, string> = {
  completed: '已完成',
  in_progress: '进行中',
  planned: '计划中'
}

const dateRange = computed(() => {
  if (!props.project) return ''
  const fmt = (s?: string) => s ? s.substring(0, 10) : ''
  const s = fmt(props.project.start_date)
  const e = fmt(props.project.end_date)
  if (s && e) return `${s}  →  ${e}`
  if (s) return `${s}  →  至今`
  return e
})

const renderMarkdown = async () => {
  if (!visible.value || !props.project?.description) return
  await nextTick()
  if (!mdRef.value) return
  Vditor.preview(mdRef.value, props.project.description, {
    cdn: '/vditor',
    mode: 'light',
    theme: { current: 'light' },
    hljs: { style: 'github', lineNumber: false }
  })
}

watch(() => [visible.value, props.project?.id], () => {
  if (visible.value) renderMarkdown()
})

onBeforeUnmount(() => {
  if (mdRef.value) mdRef.value.innerHTML = ''
})
</script>

<style scoped>
.project-detail-dialog :deep(.el-dialog__body) {
  padding: 0;
  max-height: 75vh;
  overflow-y: auto;
}

.detail-body { padding: 0 0 1.5rem; }

.detail-cover {
  width: 100%;
  max-height: 260px;
  overflow: hidden;
  background: var(--bg-secondary);
}
.detail-cover img { width: 100%; height: 100%; object-fit: cover; display: block; }

.detail-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--card-border);
}

.meta-status {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.25rem 0.7rem;
  border-radius: 20px;
  background: var(--bg-secondary);
}
.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-completed { background: #10b981; }
.dot-in_progress { background: #3b82f6; }
.dot-planned { background: #f59e0b; }

.meta-date {
  font-size: 0.82rem;
  color: var(--text-tertiary);
  font-family: 'Consolas', monospace;
}

.meta-spacer { flex: 1; }

.meta-link {
  color: var(--accent-primary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
}
.meta-link:hover { opacity: 0.75; }

.detail-section { padding: 1.25rem 1.5rem; }
.detail-section + .detail-section { border-top: 1px solid var(--card-border); }

.section-title {
  margin: 0 0 0.8rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-secondary);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.tech-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.tech-tag {
  font-size: 0.75rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-weight: 500;
}

.highlight-list {
  margin: 0;
  padding-left: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 0.9rem;
}
.highlight-list li { margin-bottom: 0.3rem; }

.md-render :deep(h1),
.md-render :deep(h2),
.md-render :deep(h3) { color: var(--text-primary); }
.md-render :deep(p),
.md-render :deep(li) { color: var(--text-secondary); line-height: 1.75; }
.md-render :deep(code) {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.85em;
}
.md-render :deep(pre) {
  background: var(--bg-tertiary);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
}
.md-render :deep(pre code) { background: transparent; padding: 0; color: var(--text-primary); }
.md-render :deep(a) { color: var(--accent-primary); }
.md-render :deep(blockquote) {
  border-left: 3px solid var(--accent-primary);
  padding-left: 1rem;
  color: var(--text-tertiary);
  margin: 0.8rem 0;
}

@media (max-width: 768px) {
  .project-detail-dialog :deep(.el-dialog) { width: 95% !important; }
}
</style>
