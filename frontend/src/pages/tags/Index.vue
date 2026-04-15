<template>
  <div class="tags-page">
    <!-- Hero -->
    <div class="page-hero">
      <span class="hero-badge">Tags</span>
      <h1 class="hero-title">标签云</h1>
      <p class="hero-desc">共 {{ tags.length }} 个标签</p>
    </div>

    <!-- Tag Cloud -->
    <div class="tag-cloud-section">
      <div v-if="loading" class="loading-state">
        <div class="skeleton-tags">
          <span v-for="i in 12" :key="i" class="skeleton-tag shimmer" :style="{ width: 50 + Math.random() * 60 + 'px' }"></span>
        </div>
      </div>

      <div class="tag-cloud" v-else-if="tags.length > 0">
        <span
          v-for="tag in tags"
          :key="tag.id"
          class="cloud-tag"
          :class="{ active: selectedTag === tag.name }"
          :style="{ fontSize: getTagSize(tag) + 'rem' }"
          @click="selectTag(tag.name)"
        >
          {{ tag.name }}
          <sup class="tag-count">{{ tag.article_count }}</sup>
        </span>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🏷️</div>
        <p class="empty-text">暂无标签</p>
        <p class="empty-sub">发布文章并添加标签后会在这里显示</p>
      </div>
    </div>

    <!-- Filtered Articles -->
    <div v-if="selectedTag" class="filtered-articles">
      <div class="filter-header">
        <h2>
          <span class="filter-tag" @click="clearFilter">
            {{ selectedTag }}
            <span class="filter-close">&times;</span>
          </span>
          <span class="filter-count">{{ filteredArticles.length }} 篇文章</span>
        </h2>
      </div>

      <div v-if="loadingArticles" class="loading-state">
        <div v-for="i in 3" :key="i" class="skeleton-article">
          <div class="skeleton-line short shimmer"></div>
          <div class="skeleton-line long shimmer"></div>
          <div class="skeleton-line medium shimmer"></div>
        </div>
      </div>

      <div v-else-if="filteredArticles.length > 0" class="articles-list">
        <div
          v-for="article in filteredArticles"
          :key="article.id"
          class="article-item"
          @click="goToArticle(article)"
        >
          <div class="article-date">{{ formatDate(article.created_at) }}</div>
          <div class="article-info">
            <h3 class="article-title">{{ article.title }}</h3>
            <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
            <div class="article-meta">
              <span class="board-pill" :class="article.board">
                {{ article.board === 'tech' ? '技术' : '生活' }}
              </span>
              <span class="article-views">
                <el-icon><View /></el-icon> {{ article.view_count }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state small">
        <p class="empty-text">该标签下暂无文章</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { View } from '@element-plus/icons-vue'
import { getArticles, type Article } from '@/api/article'
import request from '@/utils/request'

interface Tag {
  id: string
  name: string
  article_count: number
  created_at: string
}

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const loadingArticles = ref(false)
const tags = ref<Tag[]>([])
const selectedTag = ref<string | null>(null)
const filteredArticles = ref<Article[]>([])

const fetchTags = async () => {
  loading.value = true
  try {
    const response: any = await request({ url: '/tags', method: 'get' })
    tags.value = response.data || []
  } catch (error) {
    console.error('Failed to fetch tags:', error)
  } finally {
    loading.value = false
  }
}

const fetchArticlesByTag = async (tagName: string) => {
  loadingArticles.value = true
  try {
    const response = await getArticles({
      tag: tagName,
      is_published: true,
      page: 1,
      page_size: 50
    })
    filteredArticles.value = response.data.items
  } catch (error) {
    console.error('Failed to fetch articles by tag:', error)
  } finally {
    loadingArticles.value = false
  }
}

const selectTag = (tagName: string) => {
  if (selectedTag.value === tagName) {
    clearFilter()
    return
  }
  selectedTag.value = tagName
  router.replace({ query: { tag: tagName } })
  fetchArticlesByTag(tagName)
}

const clearFilter = () => {
  selectedTag.value = null
  filteredArticles.value = []
  router.replace({ query: {} })
}

const goToArticle = (article: Article) => {
  router.push(`/${article.board}/${article.id}`)
}

const getTagSize = (tag: Tag) => {
  const min = 0.9
  const max = 2.2
  const maxCount = Math.max(...tags.value.map(t => t.article_count), 1)
  return min + (tag.article_count / maxCount) * (max - min)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

watch(
  () => route.query.tag,
  (newTag) => {
    if (newTag && typeof newTag === 'string') {
      selectedTag.value = newTag
      fetchArticlesByTag(newTag)
    }
  }
)

onMounted(() => {
  fetchTags()
  if (route.query.tag && typeof route.query.tag === 'string') {
    selectedTag.value = route.query.tag
    fetchArticlesByTag(route.query.tag)
  }
})
</script>

<style scoped>
.tags-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

/* Hero */
.page-hero {
  padding: 2.5rem 0 1.5rem;
  text-align: center;
}

.hero-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: rgba(129, 140, 248, 0.15);
  color: var(--accent-primary);
  margin-bottom: 0.5rem;
}

.hero-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.hero-desc {
  margin: 0.3rem 0 0;
  font-size: 0.95rem;
  color: var(--text-tertiary);
}

/* Tag Cloud */
.tag-cloud-section {
  padding: 2rem;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 2rem;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 1rem 1.5rem;
  line-height: 2.5;
}

.cloud-tag {
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.3s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  position: relative;
}

.cloud-tag:hover {
  color: var(--accent-primary);
  background: rgba(129, 140, 248, 0.1);
}

.cloud-tag.active {
  color: var(--accent-primary);
  font-weight: 700;
  background: rgba(129, 140, 248, 0.15);
}

.tag-count {
  font-size: 0.7rem;
  color: var(--text-tertiary);
  margin-left: 2px;
}

/* Filter Header */
.filter-header {
  margin-bottom: 1.5rem;
}

.filter-header h2 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
  font-size: 1.2rem;
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tag:hover {
  background: rgba(129, 140, 248, 0.2);
}

.filter-close {
  font-size: 1.1rem;
  line-height: 1;
  opacity: 0.6;
}

.filter-count {
  color: var(--text-tertiary);
  font-size: 0.9rem;
  font-weight: 400;
}

/* Article List */
.article-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  margin-bottom: 0.75rem;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.article-item:hover {
  transform: translateX(6px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-sm);
}

.article-date {
  flex-shrink: 0;
  width: 90px;
  font-size: 0.85rem;
  color: var(--text-tertiary);
  padding-top: 0.2rem;
  font-family: 'Consolas', monospace;
}

.article-info {
  flex: 1;
  min-width: 0;
}

.article-title {
  margin: 0 0 0.4rem 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-primary);
  transition: color 0.3s;
}

.article-item:hover .article-title {
  color: var(--accent-primary);
}

.article-summary {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.board-pill {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
}

.board-pill.tech {
  background: rgba(52, 211, 153, 0.12);
  color: #34d399;
}

.board-pill.life {
  background: rgba(251, 191, 36, 0.12);
  color: #fbbf24;
}

.article-views {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  color: var(--text-tertiary);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
}

.empty-state.small {
  padding: 2rem;
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-text { margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--text-secondary); }
.empty-sub { margin: 0.3rem 0 0; font-size: 0.85rem; color: var(--text-disabled); }

/* Skeleton */
.skeleton-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.skeleton-tag {
  height: 28px;
  border-radius: 6px;
  background: var(--bg-tertiary);
}

.skeleton-article {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding: 1.25rem 1.5rem;
  margin-bottom: 0.75rem;
  border: 1px solid var(--card-border);
  border-radius: 10px;
}

.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: var(--bg-tertiary);
}

.skeleton-line.short { width: 30%; }
.skeleton-line.long { width: 80%; }
.skeleton-line.medium { width: 55%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Mobile */
@media (max-width: 768px) {
  .tags-page {
    padding: 0 1rem 2rem;
  }

  .tag-cloud-section {
    padding: 1.5rem;
  }

  .article-item {
    flex-direction: column;
    gap: 0.5rem;
  }

  .article-date {
    width: auto;
  }
}
</style>
