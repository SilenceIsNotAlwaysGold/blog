<template>
  <div class="life-list">
    <div class="header">
      <h1>Life Board</h1>
      <p class="subtitle">Private articles (authentication required)</p>
    </div>

    <el-divider />

    <div v-loading="loading" class="article-list">
      <template v-if="articles.length > 0">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
          @click="handleArticleClick"
        />

        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="fetchArticles"
          @size-change="fetchArticles"
        />
      </template>

      <el-empty v-else description="No articles found" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import ArticleCard from '@/components/article/ArticleCard.vue'
import { getArticles, type Article } from '@/api/article'

const router = useRouter()

const loading = ref(false)
const articles = ref<Article[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await getArticles({
      board: 'life',
      is_published: true,
      page: currentPage.value,
      page_size: pageSize.value
    })

    articles.value = response.data.items
    total.value = response.data.pagination.total
  } catch (error: any) {
    ElMessage.error(error.message || 'Failed to fetch articles')
  } finally {
    loading.value = false
  }
}

const handleArticleClick = (article: Article) => {
  router.push(`/life/${article.id}`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.life-list {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 0.9rem;
}

.article-list {
  min-height: 400px;
}

.el-pagination {
  margin-top: 2rem;
  justify-content: center;
}
</style>
