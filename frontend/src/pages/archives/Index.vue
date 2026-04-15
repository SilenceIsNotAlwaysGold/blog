<template>
  <div class="archives-page">
    <!-- Header -->
    <div class="page-hero">
      <div class="hero-text">
        <span class="hero-badge">Archive</span>
        <h1 class="hero-title">文章归档</h1>
        <p class="hero-desc">共 {{ totalArticles }} 篇文章，记录技术成长轨迹</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div v-for="i in 5" :key="i" class="skeleton-item">
        <div class="skeleton-line w20 shimmer"></div>
        <div class="skeleton-line w70 shimmer"></div>
      </div>
    </div>

    <!-- Timeline -->
    <template v-else-if="Object.keys(groupedArticles).length > 0">
      <div class="timeline">
        <div v-for="year in sortedYears" :key="year" class="year-section">
          <div class="year-header">
            <span class="year-label">{{ year }}</span>
            <span class="year-count">{{ groupedArticles[year].length }} 篇</span>
          </div>

          <div class="article-list">
            <div
              v-for="article in groupedArticles[year]"
              :key="article.id"
              class="archive-item"
              @click="goToArticle(article)"
            >
              <span class="item-date">{{ formatDate(article.created_at) }}</span>
              <div class="item-dot"></div>
              <div class="item-body">
                <h3 class="item-title">{{ article.title }}</h3>
                <div class="item-meta">
                  <span v-for="tag in article.tags.slice(0, 3)" :key="tag" class="item-tag">{{ tag }}</span>
                  <span class="item-views">
                    <el-icon><View /></el-icon> {{ article.view_count }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="empty-state">
      <div class="empty-icon">📚</div>
      <p class="empty-text">暂无文章</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { View } from '@element-plus/icons-vue'
import { getArticles, type Article } from '@/api/article'

const router = useRouter()
const loading = ref(false)
const allArticles = ref<Article[]>([])

const totalArticles = computed(() => allArticles.value.length)

const groupedArticles = computed(() => {
  const groups: Record<string, Article[]> = {}
  allArticles.value.forEach(article => {
    const year = new Date(article.created_at).getFullYear().toString()
    if (!groups[year]) groups[year] = []
    groups[year].push(article)
  })
  return groups
})

const sortedYears = computed(() =>
  Object.keys(groupedArticles.value).sort((a, b) => Number(b) - Number(a))
)

const fetchAllArticles = async () => {
  loading.value = true
  try {
    const techResponse = await getArticles({ board: 'tech', is_published: true, page: 1, page_size: 200 })
    allArticles.value = techResponse.data.items.sort(
      (a: Article, b: Article) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  } catch { /* ignore */ }
  finally { loading.value = false }
}

const goToArticle = (article: Article) => router.push(`/tech/${article.id}`)

const formatDate = (dateString: string) => {
  const d = new Date(dateString)
  return `${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

onMounted(() => { fetchAllArticles() })
</script>

<style scoped>
.archives-page {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

/* Hero */
.page-hero { padding: 2.5rem 0 2rem; }

.hero-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
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

/* Timeline */
.timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--card-border);
}

/* Year */
.year-section { margin-bottom: 2.5rem; }

.year-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  position: relative;
}

.year-header::before {
  content: '';
  position: absolute;
  left: -1.85rem;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent-primary);
  border: 2px solid var(--bg-primary);
  box-shadow: 0 0 0 2px var(--accent-primary);
}

.year-label {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-primary);
}

.year-count {
  font-size: 0.78rem;
  color: var(--text-disabled);
  font-weight: 500;
}

/* Archive Item */
.archive-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  margin-bottom: 0.35rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.archive-item:hover {
  background: var(--bg-secondary);
}

.item-date {
  flex-shrink: 0;
  font-size: 0.78rem;
  font-family: 'Consolas', monospace;
  color: var(--text-disabled);
  min-width: 3rem;
  padding-top: 0.15rem;
}

.item-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--card-border);
  margin-top: 0.45rem;
  flex-shrink: 0;
  transition: background 0.2s;
}

.archive-item:hover .item-dot { background: var(--accent-primary); }

.item-body { flex: 1; min-width: 0; }

.item-title {
  margin: 0 0 0.3rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  transition: color 0.2s;
}

.archive-item:hover .item-title { color: var(--accent-primary); }

.item-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.item-tag {
  font-size: 0.68rem;
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  background: var(--bg-tertiary);
  color: var(--text-disabled);
  font-weight: 500;
}

.item-views {
  display: flex;
  align-items: center;
  gap: 0.15rem;
  font-size: 0.72rem;
  color: var(--text-disabled);
  margin-left: auto;
}

/* Loading */
.loading-state { display: flex; flex-direction: column; gap: 0.8rem; padding-left: 1.5rem; }

.skeleton-item { display: flex; gap: 1rem; }

.skeleton-line { height: 16px; border-radius: 4px; background: var(--bg-tertiary); }
.w20 { width: 20%; }
.w70 { width: 70%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Empty */
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-text { margin: 0; font-size: 1.1rem; font-weight: 600; color: var(--text-secondary); }

/* Mobile */
@media (max-width: 768px) {
  .archives-page { padding: 0 1rem 2rem; }
  .timeline { padding-left: 1rem; }
  .year-header::before { left: -1.35rem; }
}
</style>
