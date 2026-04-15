<template>
  <div class="article-card" @click="handleClick">
    <div v-if="article.cover_image" class="card-cover">
      <img :src="article.cover_image" :alt="article.title" loading="lazy" />
      <div class="cover-overlay"></div>
    </div>
    <div class="card-body">
      <div class="card-header">
        <span class="card-date">{{ formatDate(article.created_at) }}</span>
        <span class="card-board">{{ article.board === 'tech' ? 'Tech' : 'Life' }}</span>
      </div>
      <h3 class="card-title">{{ article.title }}</h3>
      <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
      <div class="card-footer">
        <div class="card-tags" v-if="article.tags.length > 0">
          <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
        </div>
        <div class="card-stats">
          <span><el-icon><View /></el-icon> {{ article.view_count }}</span>
          <span><el-icon><Star /></el-icon> {{ article.like_count }}</span>
        </div>
      </div>
    </div>
    <!-- Admin actions -->
    <div v-if="isAdmin" class="admin-bar" @click.stop>
      <button class="admin-action edit" @click="handleEdit" title="编辑">
        <el-icon><Edit /></el-icon>
      </button>
      <button class="admin-action delete" @click="handleDelete" title="删除">
        <el-icon><Delete /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { View, Star, Edit, Delete } from '@element-plus/icons-vue'
import type { Article } from '@/api/article'
import { useUserStore } from '@/stores/user'

interface Props { article: Article }
interface Emits {
  (e: 'click', article: Article): void
  (e: 'edit', article: Article): void
  (e: 'delete', article: Article): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const handleClick = () => emit('click', props.article)
const handleEdit = () => emit('edit', props.article)
const handleDelete = () => emit('delete', props.article)

const formatDate = (dateString: string) => {
  const d = new Date(dateString)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
.article-card {
  position: relative;
  display: flex;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-primary);
}

/* Cover */
.card-cover {
  flex-shrink: 0;
  width: 240px;
  height: 180px;
  overflow: hidden;
  position: relative;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.article-card:hover .card-cover img { transform: scale(1.08); }

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.article-card:hover .cover-overlay { opacity: 1; }

/* Body */
.card-body {
  flex: 1;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
}

.card-date {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  font-family: 'Consolas', monospace;
}

.card-board {
  font-size: 0.65rem;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  background: rgba(129, 140, 248, 0.1);
  color: var(--accent-primary);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-title {
  margin: 0 0 0.4rem;
  font-size: 1.15rem;
  font-weight: 650;
  color: var(--text-primary);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  transition: color 0.2s;
}

.article-card:hover .card-title { color: var(--accent-primary); }

.card-summary {
  margin: 0 0 0.75rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
  line-height: 1.65;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-tags { display: flex; gap: 0.35rem; flex-wrap: wrap; }

.tag {
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  font-weight: 500;
  transition: all 0.2s;
}

.article-card:hover .tag {
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
}

.card-stats {
  display: flex;
  gap: 0.7rem;
  color: var(--text-disabled);
  font-size: 0.78rem;
}

.card-stats span { display: flex; align-items: center; gap: 0.2rem; }

/* Admin */
.admin-bar {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  gap: 0.3rem;
  opacity: 0;
  transform: translateY(-4px);
  transition: all 0.25s ease;
}

.article-card:hover .admin-bar {
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

.admin-action.edit {
  background: rgba(99, 102, 241, 0.85);
  color: #fff;
}

.admin-action.edit:hover { background: rgba(99, 102, 241, 1); }

.admin-action.delete {
  background: rgba(239, 68, 68, 0.85);
  color: #fff;
}

.admin-action.delete:hover { background: rgba(239, 68, 68, 1); }

/* Mobile */
@media (max-width: 768px) {
  .article-card { flex-direction: column; }
  .card-cover { width: 100%; height: 200px; }
  .card-body { padding: 1rem; }
  .admin-bar { opacity: 1; transform: translateY(0); }
}
</style>
