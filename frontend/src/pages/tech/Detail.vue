<template>
  <div class="article-detail">
    <!-- Reading progress -->
    <div class="reading-bar" :style="{ width: progress + '%' }"></div>

    <!-- Loading -->
    <div v-if="loading" class="loading-wrap">
      <div class="skeleton-header">
        <div class="skeleton-line w30 shimmer"></div>
        <div class="skeleton-line w80 h-lg shimmer"></div>
        <div class="skeleton-line w50 shimmer"></div>
      </div>
      <div class="skeleton-body">
        <div v-for="i in 8" :key="i" class="skeleton-line shimmer" :class="i % 3 === 0 ? 'w60' : 'w90'"></div>
      </div>
    </div>

    <template v-else-if="article">
      <!-- Admin Bar -->
      <div v-if="isAdmin" class="admin-bar">
        <div class="admin-bar-inner">
          <span class="admin-label">管理操作</span>
          <div class="admin-actions">
            <button class="admin-btn edit" @click="handleEdit">
              <el-icon><Edit /></el-icon> 编辑
            </button>
            <button class="admin-btn danger" @click="handleDelete">
              <el-icon><Delete /></el-icon> 删除
            </button>
            <span v-if="!article.is_published" class="draft-badge">草稿</span>
          </div>
        </div>
      </div>

      <!-- Article Header -->
      <header class="article-header">
        <div class="article-meta-top">
          <span class="board-tag">{{ article.board === 'tech' ? 'Tech' : 'Life' }}</span>
          <span class="meta-date">{{ formatDate(article.created_at) }}</span>
        </div>

        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-meta-bottom">
          <div class="meta-stats">
            <span class="stat"><el-icon><View /></el-icon> {{ article.view_count }} 阅读</span>
            <span class="stat clickable" :class="{ liked: isLiked }" @click="handleLike">
              <el-icon><Star /></el-icon> {{ article.like_count }} 点赞
            </span>
          </div>
          <div v-if="article.tags.length > 0" class="article-tags">
            <span v-for="tag in article.tags" :key="tag" class="tag-pill">{{ tag }}</span>
          </div>
        </div>
      </header>

      <!-- Divider -->
      <div class="content-divider"></div>

      <!-- Article Content -->
      <article class="article-body">
        <MarkdownViewer :content="article.content" />
      </article>

      <!-- Comments -->
      <CommentSection :article-id="(route.params.id as string)" />

      <!-- Article Footer -->
      <footer class="article-footer">
        <div class="footer-actions">
          <button class="like-btn" :class="{ liked: isLiked }" @click="handleLike" :disabled="liking">
            <el-icon><Star /></el-icon>
            {{ isLiked ? '已点赞' : '点赞' }} · {{ article.like_count }}
          </button>
        </div>
        <div class="footer-nav">
          <button class="back-btn" @click="$router.push('/tech')">
            ← 返回文章列表
          </button>
        </div>
      </footer>
    </template>

    <div v-else class="not-found">
      <div class="not-found-icon">404</div>
      <p>文章未找到</p>
      <button class="back-btn" @click="$router.push('/tech')">返回文章列表</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { View, Star, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import MarkdownViewer from '@/components/article/MarkdownViewer.vue'
import CommentSection from '@/components/comment/CommentSection.vue'
import { getArticle, deleteArticle, type Article } from '@/api/article'
import { toggleLike, checkLikeStatus } from '@/api/like'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isAdmin = computed(() => userStore.isAdmin)

const loading = ref(false)
const article = ref<Article | null>(null)
const isLiked = ref(false)
const liking = ref(false)
const progress = ref(0)

const updateProgress = () => {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  progress.value = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0
}

const fetchArticle = async () => {
  loading.value = true
  try {
    const response = await getArticle(route.params.id as string)
    article.value = response.data
    await fetchLikeStatus()
  } catch (error: any) {
    ElMessage.error(error.message || '加载文章失败')
  } finally { loading.value = false }
}

const fetchLikeStatus = async () => {
  if (!article.value) return
  try {
    const response = await checkLikeStatus(article.value.id)
    isLiked.value = response.data.is_liked
  } catch { /* ignore */ }
}

const handleLike = async () => {
  if (!article.value || liking.value) return
  liking.value = true
  try {
    const response = await toggleLike(article.value.id)
    const result = response.data
    isLiked.value = result.action === 'liked'
    article.value.like_count = result.like_count
    ElMessage.success(result.action === 'liked' ? '已点赞' : '已取消点赞')
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally { liking.value = false }
}

const handleEdit = () => {
  if (article.value) router.push(`/admin/article/edit/${article.value.id}`)
}

const handleDelete = async () => {
  if (!article.value) return
  try {
    await ElMessageBox.confirm(`确定要删除文章「${article.value.title}」吗？`, '删除确认', {
      confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning'
    })
    await deleteArticle(article.value.id)
    ElMessage.success('文章已删除')
    router.push('/tech')
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

const formatDate = (dateString: string) => {
  const d = new Date(dateString)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

onMounted(() => { fetchArticle(); window.addEventListener('scroll', updateProgress) })
onUnmounted(() => { window.removeEventListener('scroll', updateProgress) })
</script>

<style scoped>
/* Reading Progress */
.reading-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--accent-gradient);
  z-index: 9999;
  transition: width 0.1s;
  border-radius: 0 2px 2px 0;
}

/* Layout */
.article-detail {
  max-width: 780px;
  margin: 0 auto;
  padding: 1.5rem 2rem 4rem;
}

/* Admin Bar */
.admin-bar {
  margin-bottom: 1.5rem;
}

.admin-bar-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.25rem;
  background: var(--bg-secondary);
  border: 1px dashed var(--accent-primary);
  border-radius: 10px;
}

.admin-label {
  font-size: 0.78rem;
  color: var(--text-tertiary);
  font-weight: 500;
}

.admin-actions { display: flex; gap: 0.5rem; align-items: center; }

.admin-btn {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.85rem;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.admin-btn.edit {
  background: rgba(129, 140, 248, 0.15);
  color: var(--accent-primary);
}

.admin-btn.edit:hover { background: rgba(129, 140, 248, 0.25); }

.admin-btn.danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.admin-btn.danger:hover { background: rgba(239, 68, 68, 0.2); }

.draft-badge {
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  font-weight: 600;
}

/* Header */
.article-header { margin-bottom: 1.5rem; }

.article-meta-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.board-tag {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
}

.meta-date {
  font-size: 0.85rem;
  color: var(--text-tertiary);
  font-family: 'Consolas', monospace;
}

.article-title {
  margin: 0 0 1rem;
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.35;
  letter-spacing: -0.02em;
}

.article-meta-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.meta-stats {
  display: flex;
  gap: 1.25rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.82rem;
  color: var(--text-tertiary);
}

.stat.clickable {
  cursor: pointer;
  transition: color 0.2s;
}

.stat.clickable:hover { color: var(--accent-primary); }
.stat.liked { color: #ef4444; }

.article-tags {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.tag-pill {
  font-size: 0.72rem;
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  font-weight: 500;
}

/* Divider */
.content-divider {
  height: 1px;
  background: var(--card-border);
  margin: 0 0 2rem;
}

/* Article Body */
.article-body {
  font-size: 1rem;
  line-height: 1.8;
  color: var(--text-primary);
}

.article-body :deep(h1),
.article-body :deep(h2),
.article-body :deep(h3) {
  margin-top: 2rem;
  margin-bottom: 0.75rem;
  font-weight: 700;
  color: var(--text-primary);
}

.article-body :deep(h2) {
  font-size: 1.5rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--card-border);
}

.article-body :deep(pre) {
  border-radius: 10px;
  margin: 1.25rem 0;
}

.article-body :deep(blockquote) {
  border-left: 3px solid var(--accent-primary);
  padding: 0.5rem 1rem;
  margin: 1rem 0;
  background: rgba(129, 140, 248, 0.05);
  border-radius: 0 8px 8px 0;
  color: var(--text-secondary);
}

.article-body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
  margin: 1rem 0;
}

.article-body :deep(a) {
  color: var(--accent-primary);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.article-body :deep(a:hover) { border-bottom-color: var(--accent-primary); }

/* Footer */
.article-footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--card-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 1.5rem;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  background: rgba(129, 140, 248, 0.05);
}

.like-btn.liked {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.05);
}

.back-btn {
  background: none;
  border: none;
  color: var(--text-tertiary);
  font-size: 0.85rem;
  cursor: pointer;
  transition: color 0.2s;
}

.back-btn:hover { color: var(--accent-primary); }

/* Not Found */
.not-found {
  text-align: center;
  padding: 5rem 2rem;
}

.not-found-icon {
  font-size: 4rem;
  font-weight: 800;
  color: var(--text-disabled);
  opacity: 0.3;
  margin-bottom: 1rem;
}

.not-found p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

/* Skeleton */
.loading-wrap { padding-top: 1rem; }
.skeleton-header { margin-bottom: 2rem; display: flex; flex-direction: column; gap: 0.8rem; }
.skeleton-body { display: flex; flex-direction: column; gap: 0.7rem; }

.skeleton-line {
  height: 14px;
  border-radius: 4px;
  background: var(--bg-tertiary);
}

.skeleton-line.h-lg { height: 28px; }
.w30 { width: 30%; }
.w50 { width: 50%; }
.w60 { width: 60%; }
.w80 { width: 80%; }
.w90 { width: 90%; }

.shimmer {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, rgba(129, 140, 248, 0.05) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Mobile */
@media (max-width: 768px) {
  .article-detail { padding: 1rem 1rem 3rem; }
  .article-title { font-size: 1.6rem; }
  .article-meta-bottom { flex-direction: column; align-items: flex-start; }
  .article-footer { flex-direction: column; gap: 1rem; align-items: stretch; }
  .like-btn { justify-content: center; }
}
</style>
