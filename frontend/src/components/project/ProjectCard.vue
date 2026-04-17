<template>
  <div v-tilt class="project-card" @click="handleView">
    <!-- Cover -->
    <div class="card-cover">
      <img v-if="project.cover_image" :src="project.cover_image" :alt="project.name" loading="lazy" />
      <div v-else class="cover-placeholder">
        <span class="placeholder-icon">{{ project.name.charAt(0) }}</span>
      </div>
      <div class="cover-overlay"></div>
      <span class="status-badge" :class="'status-' + normalizedStatus">
        {{ statusLabels[normalizedStatus] || project.status }}
      </span>

      <!-- Admin Actions -->
      <div v-if="isAdmin" class="admin-bar" @click.stop>
        <button class="admin-action edit" @click="handleEdit" title="编辑">
          <el-icon><Edit /></el-icon>
        </button>
        <button class="admin-action delete" @click="handleDelete" title="删除">
          <el-icon><Delete /></el-icon>
        </button>
      </div>
    </div>

    <!-- Body -->
    <div class="card-body">
      <h3 class="card-title">{{ project.name }}</h3>
      <p class="card-desc">{{ plainSummary }}</p>

      <!-- Highlights -->
      <div v-if="project.highlights?.length" class="highlights">
        <div v-for="(h, i) in project.highlights.slice(0, 2)" :key="i" class="highlight">
          <span class="hl-dot"></span>
          {{ h }}
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="tech-tags">
        <span v-for="tech in project.tech_stack.slice(0, 4)" :key="tech" class="tech-tag">{{ tech }}</span>
        <span v-if="project.tech_stack.length > 4" class="tech-tag more">+{{ project.tech_stack.length - 4 }}</span>
      </div>

      <!-- Footer -->
      <div class="card-footer">
        <span v-if="project.start_date" class="card-date">{{ formatDate(project.start_date) }}</span>
        <div class="card-links">
          <a v-if="project.demo_url" :href="project.demo_url" target="_blank" class="link-btn" @click.stop>
            Demo →
          </a>
          <a v-if="project.github_url" :href="project.github_url" target="_blank" class="link-btn" @click.stop>
            GitHub →
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import type { Project } from '@/api/project'
import { useUserStore } from '@/stores/user'

const props = defineProps<{ project: Project }>()
const emit = defineEmits<{ edit: [id: string]; delete: [id: string]; view: [project: Project] }>()

const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const statusLabels: Record<string, string> = {
  completed: '已完成', in_progress: '进行中', planned: '计划中'
}

// 兼容 DB 里可能存在的历史值（active / in-progress 等）
const normalizedStatus = computed(() => {
  const v = (props.project.status || '').toLowerCase().replace(/-/g, '_')
  if (v === 'active') return 'in_progress'
  if (['completed', 'in_progress', 'planned'].includes(v)) return v
  return 'planned'
})

// 去掉 Markdown 语法作为卡片纯文本摘要
const plainSummary = computed(() => {
  const raw = props.project.description || ''
  return raw
    .replace(/```[\s\S]*?```/g, ' ')                  // 代码块
    .replace(/`[^`]*`/g, ' ')                         // 行内代码
    .replace(/!\[[^\]]*]\([^)]*\)/g, ' ')             // 图片
    .replace(/\[([^\]]+)]\([^)]*\)/g, '$1')           // 链接 → 文字
    .replace(/^\s{0,3}#{1,6}\s+/gm, '')               // 标题井号
    .replace(/^\s{0,3}>\s?/gm, '')                    // 引用符号
    .replace(/^[-*+]\s+|^\d+\.\s+/gm, '')             // 列表符号
    .replace(/[*_~]{1,3}([^*_~]+)[*_~]{1,3}/g, '$1')  // 粗体/斜体/删除线
    .replace(/\|/g, ' ')                              // 表格
    .replace(/\s+/g, ' ')
    .trim()
})

const formatDate = (dateString: string) => {
  const d = new Date(dateString)
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}`
}

const handleEdit = () => emit('edit', props.project.id)
const handleDelete = () => emit('delete', props.project.id)
const handleView = () => emit('view', props.project)
</script>

<style scoped>
.project-card {
  position: relative;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.project-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-primary);
}

/* Cover */
.card-cover {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.project-card:hover .card-cover img { transform: scale(1.06); }

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-gradient);
}

.placeholder-icon {
  font-size: 3rem;
  font-weight: 800;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 40%, rgba(0, 0, 0, 0.4) 100%);
}

.status-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  backdrop-filter: blur(8px);
}

.status-completed { background: rgba(16, 185, 129, 0.85); color: #fff; }
.status-in_progress { background: rgba(59, 130, 246, 0.85); color: #fff; }
.status-planned { background: rgba(245, 158, 11, 0.85); color: #fff; }

/* Admin */
.admin-bar {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  display: flex;
  gap: 0.3rem;
  opacity: 0;
  transform: translateY(-4px);
  transition: all 0.25s ease;
}

.project-card:hover .admin-bar {
  opacity: 1;
  transform: translateY(0);
}

.admin-action {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.2s;
  font-size: 0.85rem;
}

.admin-action.edit { background: rgba(99, 102, 241, 0.85); color: #fff; }
.admin-action.edit:hover { background: rgba(99, 102, 241, 1); }
.admin-action.delete { background: rgba(239, 68, 68, 0.85); color: #fff; }
.admin-action.delete:hover { background: rgba(239, 68, 68, 1); }

/* Body */
.card-body {
  padding: 1.25rem 1.5rem 1.5rem;
}

.card-title {
  margin: 0 0 0.4rem;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-primary);
  transition: color 0.2s;
}

.project-card:hover .card-title { color: var(--accent-primary); }

.card-desc {
  margin: 0 0 0.75rem;
  font-size: 0.83rem;
  color: var(--text-secondary);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.6em;
}

/* Highlights */
.highlights { margin-bottom: 0.75rem; }

.highlight {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  color: var(--text-tertiary);
  margin-bottom: 0.3rem;
}

.hl-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent-primary);
  flex-shrink: 0;
}

/* Tech */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-bottom: 0.75rem;
}

.tech-tag {
  font-size: 0.7rem;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  font-weight: 500;
}

.tech-tag.more {
  background: rgba(129, 140, 248, 0.1);
  color: var(--accent-primary);
}

/* Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid var(--card-border);
}

.card-date {
  font-size: 0.75rem;
  color: var(--text-disabled);
  font-family: 'Consolas', monospace;
}

.card-links { display: flex; gap: 0.75rem; }

.link-btn {
  font-size: 0.78rem;
  color: var(--accent-primary);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.link-btn:hover { opacity: 0.7; }

/* Mobile */
@media (max-width: 768px) {
  .admin-bar { opacity: 1; transform: translateY(0); }
}
</style>
