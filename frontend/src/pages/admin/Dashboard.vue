<template>
  <div class="dashboard">
    <div class="header">
      <div class="header-left">
        <h1>管理后台</h1>
        <p class="welcome">欢迎回来，{{ userStore.userInfo?.username }}！</p>
      </div>
      <div class="header-right">
        <el-button :icon="Link" @click="openDocs">API 文档</el-button>
        <el-button :icon="ArrowLeft" @click="router.push('/')">
          返回前台
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card-wrap">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(64, 158, 255, 0.1);">
              <el-icon :size="32" color="#409eff"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalArticles }}</div>
              <div class="stat-label">文章总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card-wrap">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(103, 194, 58, 0.1);">
              <el-icon :size="32" color="#67c23a"><View /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalViews }}</div>
              <div class="stat-label">浏览总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card-wrap">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(245, 108, 108, 0.1);">
              <el-icon :size="32" color="#f56c6c"><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalLikes }}</div>
              <div class="stat-label">获赞总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="hover" class="stat-card-wrap">
          <div class="stat-card">
            <div class="stat-icon" style="background: rgba(230, 162, 60, 0.1);">
              <el-icon :size="32" color="#e6a23c"><Collection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.publishedArticles }}</div>
              <div class="stat-label">已发布</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 管理面板 Tabs -->
    <el-tabs v-model="activeTab" class="admin-tabs" type="border-card">
      <!-- ==================== 文章管理 ==================== -->
      <el-tab-pane label="文章管理" name="articles">
        <template #label>
          <span class="tab-label"><el-icon><Document /></el-icon> 文章管理</span>
        </template>
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="handleCreateArticle">
            新建文章
          </el-button>
          <el-select
            v-model="filterBoard"
            placeholder="按板块筛选"
            clearable
            style="width: 150px"
            @change="fetchArticles"
          >
            <el-option label="技术" value="tech" />
            <el-option label="生活" value="life" />
          </el-select>
          <el-input
            v-model="articleSearch"
            placeholder="搜索文章标题..."
            clearable
            style="width: 250px; margin-left: auto;"
            @input="fetchArticles"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>

        <el-table
          v-loading="articlesLoading"
          :data="filteredArticles"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="board" label="板块" width="90" align="center">
            <template #default="{ row }">
              <el-tag :type="row.board === 'tech' ? 'success' : 'warning'" size="small">
                {{ row.board === 'tech' ? '技术' : '生活' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_published" label="状态" width="90" align="center">
            <template #default="{ row }">
              <el-tag :type="row.is_published ? 'success' : 'info'" size="small">
                {{ row.is_published ? '已发布' : '草稿' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="view_count" label="浏览" width="80" align="center" />
          <el-table-column prop="like_count" label="点赞" width="80" align="center" />
          <el-table-column prop="created_at" label="创建时间" width="170">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="handleEditArticle(row)">编辑</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDeleteArticle(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          v-model:current-page="articlePage"
          v-model:page-size="articlePageSize"
          :total="articleTotal"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @current-change="fetchArticles"
          @size-change="fetchArticles"
          style="margin-top: 1rem; justify-content: center"
        />
      </el-tab-pane>

      <!-- ==================== 分类管理 ==================== -->
      <el-tab-pane label="分类管理" name="categories">
        <template #label>
          <span class="tab-label"><el-icon><Folder /></el-icon> 分类管理</span>
        </template>
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="showCategoryDialog()">
            新建分类
          </el-button>
          <el-select
            v-model="categoryFilterBoard"
            placeholder="按板块筛选"
            clearable
            style="width: 150px"
            @change="fetchCategories"
          >
            <el-option label="技术" value="tech" />
            <el-option label="生活" value="life" />
          </el-select>
        </div>

        <el-table
          v-loading="categoriesLoading"
          :data="categories"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="name" label="分类名称" min-width="180" />
          <el-table-column prop="board" label="所属板块" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="row.board === 'tech' ? 'success' : 'warning'" size="small">
                {{ row.board === 'tech' ? '技术' : '生活' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              {{ row.description || '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="article_count" label="文章数" width="100" align="center" />
          <el-table-column prop="created_at" label="创建时间" width="170">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="showCategoryDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDeleteCategory(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ==================== 标签管理 ==================== -->
      <el-tab-pane label="标签管理" name="tags">
        <template #label>
          <span class="tab-label"><el-icon><PriceTag /></el-icon> 标签管理</span>
        </template>
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="showTagDialog()">
            新建标签
          </el-button>
        </div>

        <el-table
          v-loading="tagsLoading"
          :data="tags"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="name" label="标签名称" min-width="200" />
          <el-table-column prop="article_count" label="文章数" width="120" align="center" />
          <el-table-column prop="created_at" label="创建时间" width="170">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="showTagDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDeleteTag(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ==================== 技能管理 ==================== -->
      <el-tab-pane label="技能管理" name="skills">
        <template #label>
          <span class="tab-label"><el-icon><Trophy /></el-icon> 技能管理</span>
        </template>
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="router.push('/admin/skill/new')">
            新建技能
          </el-button>
        </div>

        <el-table
          v-loading="skillsLoading"
          :data="skillsList"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="name" label="技能名称" min-width="150" />
          <el-table-column prop="category" label="分类" width="120" align="center">
            <template #default="{ row }">
              <el-tag size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="proficiency" label="熟练度" width="200">
            <template #default="{ row }">
              <el-progress :percentage="row.proficiency" :color="getProgressColor(row.proficiency)" />
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              {{ row.description || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="router.push(`/admin/skill/edit/${row.id}`)">编辑</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDeleteSkill(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- ==================== 项目管理 ==================== -->
      <el-tab-pane label="项目管理" name="projects">
        <template #label>
          <span class="tab-label"><el-icon><Briefcase /></el-icon> 项目管理</span>
        </template>
        <div class="toolbar">
          <el-button type="primary" :icon="Plus" @click="router.push('/admin/project/new')">
            新建项目
          </el-button>
        </div>

        <el-table
          v-loading="projectsLoading"
          :data="projectsList"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="name" label="项目名称" min-width="180" />
          <el-table-column prop="status" label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="tech_stack" label="技术栈" min-width="200">
            <template #default="{ row }">
              <el-tag v-for="tech in (row.tech_stack || []).slice(0, 3)" :key="tech" size="small" style="margin-right: 4px; margin-bottom: 2px;">
                {{ tech }}
              </el-tag>
              <span v-if="(row.tech_stack || []).length > 3" class="more-tag">+{{ row.tech_stack.length - 3 }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              {{ row.description || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right" align="center">
            <template #default="{ row }">
              <el-button size="small" :icon="Edit" @click="router.push(`/admin/project/edit/${row.id}`)">编辑</el-button>
              <el-button size="small" type="danger" :icon="Delete" @click="handleDeleteProject(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- ==================== 分类编辑对话框 ==================== -->
    <el-dialog
      v-model="categoryDialogVisible"
      :title="editingCategory ? '编辑分类' : '新建分类'"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="categoryFormRef"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="板块" prop="board">
          <el-select v-model="categoryForm.board" placeholder="请选择板块" style="width: 100%">
            <el-option label="技术" value="tech" />
            <el-option label="生活" value="life" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="categoryForm.description" type="textarea" :rows="3" placeholder="请输入分类描述（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="categoryDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="categorySaving" @click="handleSaveCategory">
          {{ editingCategory ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- ==================== 标签编辑对话框 ==================== -->
    <el-dialog
      v-model="tagDialogVisible"
      :title="editingTag ? '编辑标签' : '新建标签'"
      width="400px"
      destroy-on-close
    >
      <el-form
        ref="tagFormRef"
        :model="tagForm"
        :rules="tagRules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="tagDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="tagSaving" @click="handleSaveTag">
          {{ editingTag ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import {
  Plus, Edit, Delete, Document, View, Star, Collection,
  Folder, PriceTag, Trophy, Briefcase,
  ArrowLeft, Search, Link
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { getArticles, deleteArticle, type Article } from '@/api/article'
import { getCategories, createCategory, updateCategory, deleteCategory, type Category } from '@/api/category'
import { getSkills, deleteSkill, type Skill } from '@/api/skill'
import { getProjects, deleteProject, type Project } from '@/api/project'

const router = useRouter()
const openDocs = () => window.open('/docs', '_blank')
const userStore = useUserStore()

// ==================== 通用状态 ====================
const activeTab = ref('articles')

const stats = ref({
  totalArticles: 0,
  totalViews: 0,
  totalLikes: 0,
  publishedArticles: 0
})

// ==================== 文章管理 ====================
const articlesLoading = ref(false)
const articles = ref<Article[]>([])
const articlePage = ref(1)
const articlePageSize = ref(10)
const articleTotal = ref(0)
const filterBoard = ref<string>('')
const articleSearch = ref('')

const filteredArticles = computed(() => {
  if (!articleSearch.value) return articles.value
  const keyword = articleSearch.value.toLowerCase()
  return articles.value.filter(a => a.title.toLowerCase().includes(keyword))
})

// ==================== 分类管理 ====================
const categoriesLoading = ref(false)
const categories = ref<Category[]>([])
const categoryFilterBoard = ref<string>('')
const categoryDialogVisible = ref(false)
const editingCategory = ref<Category | null>(null)
const categorySaving = ref(false)
const categoryFormRef = ref<FormInstance>()
const categoryForm = reactive({
  name: '',
  board: 'tech',
  description: ''
})
const categoryRules: FormRules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
  board: [{ required: true, message: '请选择板块', trigger: 'change' }]
}

// ==================== 标签管理 ====================
interface Tag {
  id: string
  name: string
  article_count: number
  created_at: string
}
const tagsLoading = ref(false)
const tags = ref<Tag[]>([])
const tagDialogVisible = ref(false)
const editingTag = ref<Tag | null>(null)
const tagSaving = ref(false)
const tagFormRef = ref<FormInstance>()
const tagForm = reactive({ name: '' })
const tagRules: FormRules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

// ==================== 技能管理 ====================
const skillsLoading = ref(false)
const skillsList = ref<Skill[]>([])

// ==================== 项目管理 ====================
const projectsLoading = ref(false)
const projectsList = ref<Project[]>([])

// ==================== 文章操作 ====================
const fetchArticles = async () => {
  articlesLoading.value = true
  try {
    const response = await getArticles({
      board: (filterBoard.value as 'tech' | 'life') || undefined,
      page: articlePage.value,
      page_size: articlePageSize.value
    })
    articles.value = response.data.items
    articleTotal.value = response.data.pagination.total

    // 计算统计
    stats.value.totalArticles = response.data.pagination.total
    stats.value.totalViews = articles.value.reduce((sum, a) => sum + a.view_count, 0)
    stats.value.totalLikes = articles.value.reduce((sum, a) => sum + a.like_count, 0)
    stats.value.publishedArticles = articles.value.filter(a => a.is_published).length
  } catch (error: any) {
    ElMessage.error(error.message || '加载文章失败')
  } finally {
    articlesLoading.value = false
  }
}

const handleCreateArticle = () => {
  router.push('/admin/article/new')
}

const handleEditArticle = (article: Article) => {
  router.push(`/admin/article/edit/${article.id}`)
}

const handleDeleteArticle = async (article: Article) => {
  try {
    await ElMessageBox.confirm(`确定要删除文章「${article.title}」吗？此操作不可恢复。`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteArticle(article.id)
    ElMessage.success('文章已删除')
    fetchArticles()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

// ==================== 分类操作 ====================
const fetchCategories = async () => {
  categoriesLoading.value = true
  try {
    const response = await getCategories(categoryFilterBoard.value || undefined)
    categories.value = response.data
  } catch (error: any) {
    ElMessage.error(error.message || '加载分类失败')
  } finally {
    categoriesLoading.value = false
  }
}

const showCategoryDialog = (cat?: Category) => {
  if (cat) {
    editingCategory.value = cat
    categoryForm.name = cat.name
    categoryForm.board = cat.board
    categoryForm.description = cat.description || ''
  } else {
    editingCategory.value = null
    categoryForm.name = ''
    categoryForm.board = 'tech'
    categoryForm.description = ''
  }
  categoryDialogVisible.value = true
}

const handleSaveCategory = async () => {
  if (!categoryFormRef.value) return
  try {
    await categoryFormRef.value.validate()
    categorySaving.value = true

    if (editingCategory.value) {
      await updateCategory(editingCategory.value.id, {
        name: categoryForm.name,
        description: categoryForm.description || undefined
      })
      ElMessage.success('分类已更新')
    } else {
      await createCategory({
        name: categoryForm.name,
        board: categoryForm.board,
        description: categoryForm.description || undefined
      })
      ElMessage.success('分类已创建')
    }
    categoryDialogVisible.value = false
    fetchCategories()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '保存失败')
  } finally {
    categorySaving.value = false
  }
}

const handleDeleteCategory = async (cat: Category) => {
  try {
    await ElMessageBox.confirm(`确定要删除分类「${cat.name}」吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteCategory(cat.id)
    ElMessage.success('分类已删除')
    fetchCategories()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

// ==================== 标签操作 ====================
import request from '@/utils/request'

const fetchTags = async () => {
  tagsLoading.value = true
  try {
    const response: any = await request({ url: '/tags', method: 'get' })
    tags.value = response.data || []
  } catch (error: any) {
    ElMessage.error(error.message || '加载标签失败')
  } finally {
    tagsLoading.value = false
  }
}

const showTagDialog = (tag?: Tag) => {
  if (tag) {
    editingTag.value = tag
    tagForm.name = tag.name
  } else {
    editingTag.value = null
    tagForm.name = ''
  }
  tagDialogVisible.value = true
}

const handleSaveTag = async () => {
  if (!tagFormRef.value) return
  try {
    await tagFormRef.value.validate()
    tagSaving.value = true

    if (editingTag.value) {
      await request({ url: `/tags/${editingTag.value.id}`, method: 'put', data: { name: tagForm.name } })
      ElMessage.success('标签已更新')
    } else {
      await request({ url: '/tags', method: 'post', data: { name: tagForm.name } })
      ElMessage.success('标签已创建')
    }
    tagDialogVisible.value = false
    fetchTags()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '保存失败')
  } finally {
    tagSaving.value = false
  }
}

const handleDeleteTag = async (tag: Tag) => {
  try {
    await ElMessageBox.confirm(`确定要删除标签「${tag.name}」吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await request({ url: `/tags/${tag.id}`, method: 'delete' })
    ElMessage.success('标签已删除')
    fetchTags()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

// ==================== 技能操作 ====================
const fetchSkills = async () => {
  skillsLoading.value = true
  try {
    const response = await getSkills()
    skillsList.value = response.data || []
  } catch (error: any) {
    ElMessage.error(error.message || '加载技能失败')
  } finally {
    skillsLoading.value = false
  }
}

const handleDeleteSkill = async (skill: Skill) => {
  try {
    await ElMessageBox.confirm(`确定要删除技能「${skill.name}」吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteSkill(skill.id)
    ElMessage.success('技能已删除')
    fetchSkills()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

const getProgressColor = (percentage: number) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#409eff'
  if (percentage >= 40) return '#e6a23c'
  return '#f56c6c'
}

// ==================== 项目操作 ====================
const fetchProjects = async () => {
  projectsLoading.value = true
  try {
    const response = await getProjects({})
    projectsList.value = response.data || []
  } catch (error: any) {
    ElMessage.error(error.message || '加载项目失败')
  } finally {
    projectsLoading.value = false
  }
}

const handleDeleteProject = async (project: Project) => {
  try {
    await ElMessageBox.confirm(`确定要删除项目「${project.name}」吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteProject(project.id)
    ElMessage.success('项目已删除')
    fetchProjects()
  } catch (error: any) {
    if (error !== 'cancel') ElMessage.error(error.message || '删除失败')
  }
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    completed: 'success',
    in_progress: 'warning',
    planned: 'info'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    completed: '已完成',
    in_progress: '进行中',
    planned: '计划中'
  }
  return map[status] || status
}

// ==================== 通用工具函数 ====================
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

// ==================== 生命周期 ====================
onMounted(() => {
  fetchArticles()
  fetchCategories()
  fetchTags()
  fetchSkills()
  fetchProjects()
})
</script>

<style scoped>
.dashboard {
  background: var(--bg-primary);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  transition: background-color 0.3s ease;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.header-left h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  color: var(--text-primary);
  font-weight: 700;
}

.welcome {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 统计卡片 */
.stats-row {
  margin-bottom: 2rem;
}

.stat-card-wrap {
  background: var(--card-bg);
  border-color: var(--border-color);
  transition: all 0.3s ease;
}

.stat-card-wrap:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

/* Tabs */
.admin-tabs {
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.95rem;
}

.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.more-tag {
  color: var(--text-secondary);
  font-size: 0.8rem;
}

/* Element Plus 样式覆盖 */
:deep(.el-tabs__content) {
  padding: 1.5rem;
}

:deep(.el-table) {
  background-color: transparent;
  color: var(--text-primary);
}

:deep(.el-table th) {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-color);
}

:deep(.el-table td) {
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-table tr) {
  background-color: transparent;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: var(--bg-secondary);
}

:deep(.el-table__body tr:hover > td) {
  background-color: var(--bg-secondary) !important;
}

:deep(.el-card) {
  background-color: var(--card-bg);
  border-color: var(--border-color);
}

:deep(.el-tabs__item) {
  color: var(--text-secondary);
}

:deep(.el-tabs__item.is-active) {
  color: var(--accent-primary);
}

:deep(.el-tabs--border-card > .el-tabs__header) {
  background: var(--bg-secondary);
  border-color: var(--border-color);
}

:deep(.el-tabs--border-card) {
  border-color: var(--border-color);
  background: var(--card-bg);
}

:deep(.el-dialog) {
  background: var(--card-bg);
  border: 1px solid var(--border-color);
}

:deep(.el-dialog__header) {
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .tab-label {
    font-size: 0.85rem;
  }
}
</style>
