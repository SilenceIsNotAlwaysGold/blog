<template>
  <div class="tech-detail">
    <el-skeleton v-if="loading" :rows="10" animated />

    <template v-else-if="article">
      <div class="article-header">
        <h1 class="title">{{ article.title }}</h1>

        <div class="meta">
          <span class="date">
            <el-icon><Calendar /></el-icon>
            {{ formatDate(article.created_at) }}
          </span>
          <span class="stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ article.view_count }}
            </span>
            <span class="stat-item">
              <el-icon :class="{ liked: isLiked }" @click="handleLike">
                <Star />
              </el-icon>
              {{ article.like_count }}
            </span>
          </span>
        </div>

        <div v-if="article.tags.length > 0" class="tags">
          <el-tag
            v-for="tag in article.tags"
            :key="tag"
            type="info"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <el-divider />

      <div class="article-content">
        <MarkdownViewer :content="article.content" />
      </div>
    </template>

    <el-empty v-else description="Article not found" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Calendar, View, Star } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import MarkdownViewer from '@/components/article/MarkdownViewer.vue'
import { getArticle, type Article } from '@/api/article'

const route = useRoute()

const loading = ref(false)
const article = ref<Article | null>(null)
const isLiked = ref(false)

const fetchArticle = async () => {
  loading.value = true
  try {
    const response = await getArticle(route.params.id as string)
    article.value = response.data
  } catch (error: any) {
    ElMessage.error(error.message || 'Failed to fetch article')
  } finally {
    loading.value = false
  }
}

const handleLike = async () => {
  if (!article.value) return

  // TODO: Implement like API call
  ElMessage.info('Like feature coming soon')
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.tech-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.article-header {
  margin-bottom: 2rem;
}

.title {
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #303133;
  line-height: 1.3;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  color: #909399;
  font-size: 0.9rem;
}

.date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-item .el-icon {
  cursor: pointer;
  transition: color 0.3s;
}

.stat-item .el-icon:hover {
  color: #409eff;
}

.stat-item .el-icon.liked {
  color: #f56c6c;
}

.tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.article-content {
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .tech-detail {
    padding: 1rem;
  }

  .title {
    font-size: 1.75rem;
  }

  .meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
