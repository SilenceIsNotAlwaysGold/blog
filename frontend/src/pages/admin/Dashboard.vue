<template>
  <div class="dashboard">
    <div class="header">
      <h1>Admin Dashboard</h1>
      <p class="welcome">Welcome, {{ userStore.userInfo?.username }}!</p>
    </div>

    <el-tabs v-model="activeTab" class="admin-tabs">
      <el-tab-pane label="Article Management" name="articles">
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="handleCreate">
            New Article
          </el-button>
          <el-select
            v-model="filterBoard"
            placeholder="Filter by board"
            clearable
            style="width: 150px"
            @change="fetchArticles"
          >
            <el-option label="Tech" value="tech" />
            <el-option label="Life" value="life" />
          </el-select>
        </div>

        <el-table
          v-loading="loading"
          :data="articles"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="title" label="Title" min-width="200" />
          <el-table-column prop="board" label="Board" width="100">
            <template #default="{ row }">
              <el-tag :type="row.board === 'tech' ? 'success' : 'warning'">
                {{ row.board }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_published" label="Status" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_published ? 'success' : 'info'">
                {{ row.is_published ? 'Published' : 'Draft' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="view_count" label="Views" width="100" />
          <el-table-column prop="like_count" label="Likes" width="100" />
          <el-table-column prop="created_at" label="Created" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="200" fixed="right">
            <template #default="{ row }">
              <el-button
                size="small"
                :icon="Edit"
                @click="handleEdit(row)"
              >
                Edit
              </el-button>
              <el-button
                size="small"
                type="danger"
                :icon="Delete"
                @click="handleDelete(row)"
              >
                Delete
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="fetchArticles"
          @size-change="fetchArticles"
          style="margin-top: 1rem; justify-content: center"
        />
      </el-tab-pane>

      <el-tab-pane label="Statistics" name="stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon :size="40" color="#409eff"><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalArticles }}</div>
                  <div class="stat-label">Total Articles</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon :size="40" color="#67c23a"><View /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalViews }}</div>
                  <div class="stat-label">Total Views</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon :size="40" color="#f56c6c"><Star /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalLikes }}</div>
                  <div class="stat-label">Total Likes</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <div class="stat-card">
                <div class="stat-icon">
                  <el-icon :size="40" color="#e6a23c"><Collection /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.publishedArticles }}</div>
                  <div class="stat-label">Published</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Plus, Edit, Delete, Document, View, Star, Collection } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getArticles, deleteArticle, type Article } from '@/api/article'

const userStore = useUserStore()

const activeTab = ref('articles')
const loading = ref(false)
const articles = ref<Article[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const filterBoard = ref<'tech' | 'life' | ''>('')

const stats = ref({
  totalArticles: 0,
  totalViews: 0,
  totalLikes: 0,
  publishedArticles: 0
})

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await getArticles({
      board: filterBoard.value || undefined,
      page: currentPage.value,
      page_size: pageSize.value
    })

    articles.value = response.data.items
    total.value = response.data.pagination.total

    // Calculate stats
    stats.value.totalArticles = response.data.pagination.total
    stats.value.totalViews = articles.value.reduce((sum, a) => sum + a.view_count, 0)
    stats.value.totalLikes = articles.value.reduce((sum, a) => sum + a.like_count, 0)
    stats.value.publishedArticles = articles.value.filter(a => a.is_published).length
  } catch (error: any) {
    ElMessage.error(error.message || 'Failed to fetch articles')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  // TODO: Navigate to article editor
  ElMessage.info('Article editor will be implemented in next phase')
}

const handleEdit = (article: Article) => {
  // TODO: Navigate to article editor with article ID
  ElMessage.info(`Edit article: ${article.title}`)
}

const handleDelete = async (article: Article) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure to delete "${article.title}"?`,
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )

    await deleteArticle(article.id)
    ElMessage.success('Article deleted successfully')
    fetchArticles()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || 'Failed to delete article')
    }
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  color: #303133;
}

.welcome {
  margin: 0;
  color: #909399;
  font-size: 1rem;
}

.admin-tabs {
  margin-top: 1rem;
}

.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #303133;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #909399;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .toolbar {
    flex-direction: column;
  }
}
</style>

