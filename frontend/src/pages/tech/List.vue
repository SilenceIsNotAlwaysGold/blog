<template>
  <div class="tech-list">
    <div class="header">
      <h1>Tech Board</h1>
      <el-input
        v-model="searchKeyword"
        placeholder="Search articles..."
        class="search-input"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
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
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ArticleCard from '@/components/article/ArticleCard.vue'
import { getArticles, type Article } from '@/api/article'
import { searchArticles } from '@/api/search'

const router = useRouter()

const loading = ref(false)
const articles = ref<Article[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchKeyword = ref('')

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await getArticles({
      board: 'tech',
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

const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    fetchArticles()
    return
  }

  loading.value = true
  try {
    const response = await searchArticles({
      q: searchKeyword.value,
      board: 'tech',
      limit: pageSize.value
    })

    articles.value = response.data.data
    total.value = articles.value.length
  } catch (error: any) {
    ElMessage.error(error.message || 'Search failed')
  } finally {
    loading.value = false
  }
}

const handleArticleClick = (article: Article) => {
  router.push(`/tech/${article.id}`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.tech-list {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1rem;
}

.header h1 {
  margin: 0;
  font-size: 2rem;
  color: #303133;
}

.search-input {
  max-width: 400px;
}

.article-list {
  min-height: 400px;
}

.el-pagination {
  margin-top: 2rem;
  justify-content: center;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    max-width: 100%;
  }
}
</style>
