<template>
  <el-card class="article-card" shadow="hover" @click="handleClick">
    <div class="card-content">
      <div v-if="article.cover_image" class="cover-image">
        <img :src="article.cover_image" :alt="article.title" />
      </div>

      <div class="article-info">
        <h3 class="title">{{ article.title }}</h3>

        <p v-if="article.summary" class="summary">
          {{ article.summary }}
        </p>

        <div class="meta">
          <span class="tags" v-if="article.tags.length > 0">
            <el-tag
              v-for="tag in article.tags.slice(0, 3)"
              :key="tag"
              size="small"
              type="info"
            >
              {{ tag }}
            </el-tag>
          </span>

          <span class="stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ article.view_count }}
            </span>
            <span class="stat-item" v-if="article.board === 'tech'">
              <el-icon><Star /></el-icon>
              {{ article.like_count }}
            </span>
          </span>
        </div>

        <div class="footer">
          <span class="date">
            {{ formatDate(article.created_at) }}
          </span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { View, Star } from '@element-plus/icons-vue'
import type { Article } from '@/api/article'

interface Props {
  article: Article
}

interface Emits {
  (e: 'click', article: Article): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const handleClick = () => {
  emit('click', props.article)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.article-card {
  cursor: pointer;
  transition: transform 0.3s;
  margin-bottom: 1rem;
}

.article-card:hover {
  transform: translateY(-4px);
}

.card-content {
  display: flex;
  gap: 1rem;
}

.cover-image {
  flex-shrink: 0;
  width: 200px;
  height: 150px;
  overflow: hidden;
  border-radius: 4px;
}

.cover-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.title {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.summary {
  margin: 0 0 1rem 0;
  color: #606266;
  font-size: 0.9rem;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tags {
  display: flex;
  gap: 0.5rem;
}

.stats {
  display: flex;
  gap: 1rem;
  color: #909399;
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.footer {
  margin-top: auto;
  color: #909399;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .card-content {
    flex-direction: column;
  }

  .cover-image {
    width: 100%;
    height: 200px;
  }
}
</style>
