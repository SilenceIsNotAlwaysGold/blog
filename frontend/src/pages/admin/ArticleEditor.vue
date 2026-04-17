<template>
  <div class="article-editor">
    <div class="editor-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
        <h1>{{ isEdit ? '编辑文章' : '新建文章' }}</h1>
      </div>
      <div class="header-right">
        <el-button @click="handleSaveDraft" :loading="saving">保存草稿</el-button>
        <el-button type="primary" @click="handlePublish" :loading="publishing">
          {{ form.is_published ? '更新发布' : '发布文章' }}
        </el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      class="editor-form"
    >
      <el-card shadow="never" class="form-card">
        <el-form-item label="文章标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入文章标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="文章摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要（可选）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属板块" prop="board">
              <el-select v-model="form.board" placeholder="请选择板块" style="width: 100%">
                <el-option label="技术" value="tech" />
                <el-option label="生活" value="life" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="封面图片" prop="cover_image">
              <el-input
                v-model="form.cover_image"
                placeholder="请输入封面图片 URL（可选）"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="文章标签" prop="tags">
          <el-select
            v-model="form.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请输入标签，按回车添加"
            style="width: 100%"
          >
          </el-select>
        </el-form-item>
      </el-card>

      <el-card shadow="never" class="form-card">
        <el-form-item label="文章内容" prop="content">
          <MarkdownEditor
            v-model="form.content"
            height="600px"
            placeholder="请输入文章内容..."
          />
        </el-form-item>
      </el-card>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { createArticle, updateArticle, getArticle, type ArticleCreate, type ArticleUpdate } from '@/api/article'

const MarkdownEditor = defineAsyncComponent(() => import('@/components/article/MarkdownEditor.vue'))

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInstance>()
const saving = ref(false)
const publishing = ref(false)
const isEdit = ref(false)
const articleId = ref('')

const form = reactive({
  title: '',
  content: '',
  summary: '',
  board: 'tech' as 'tech' | 'life',
  tags: [] as string[],
  cover_image: '',
  is_published: false
})

const rules: FormRules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  board: [
    { required: true, message: '请选择所属板块', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// 加载文章数据（编辑模式）
const loadArticle = async () => {
  try {
    const response = await getArticle(articleId.value)
    const article = response.data

    form.title = article.title
    form.content = article.content
    form.summary = article.summary || ''
    form.board = article.board
    form.tags = article.tags || []
    form.cover_image = article.cover_image || ''
    form.is_published = article.is_published
  } catch (error: any) {
    ElMessage.error(error.message || '加载文章失败')
    router.push('/admin/dashboard')
  }
}

// 返回列表
const handleBack = () => {
  // 根据文章板块返回到对应的列表页
  if (form.board === 'life') {
    router.push('/life')
  } else {
    router.push('/tech')
  }
}

// 保存草稿
const handleSaveDraft = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    const data = {
      title: form.title,
      content: form.content,
      summary: form.summary || undefined,
      board: form.board,
      tags: form.tags.length > 0 ? form.tags : undefined,
      cover_image: form.cover_image || undefined,
      is_published: false
    }

    if (isEdit.value) {
      await updateArticle(articleId.value, data as ArticleUpdate)
      ElMessage.success('草稿保存成功')
    } else {
      const response = await createArticle(data as ArticleCreate)
      articleId.value = response.data.id
      isEdit.value = true
      ElMessage.success('草稿保存成功')
      // 更新 URL 为编辑模式
      router.replace(`/admin/article/edit/${articleId.value}`)
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 发布文章
const handlePublish = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    publishing.value = true

    const data = {
      title: form.title,
      content: form.content,
      summary: form.summary || undefined,
      board: form.board,
      tags: form.tags.length > 0 ? form.tags : undefined,
      cover_image: form.cover_image || undefined,
      is_published: true
    }

    if (isEdit.value) {
      await updateArticle(articleId.value, data as ArticleUpdate)
      ElMessage.success('文章更新成功')
    } else {
      await createArticle(data as ArticleCreate)
      ElMessage.success('文章发布成功')
    }

    // 返回列表页
    setTimeout(() => {
      router.push('/admin/dashboard')
    }, 1000)
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '发布失败')
    }
  } finally {
    publishing.value = false
  }
}

onMounted(() => {
  // 检查是否为编辑模式
  if (route.params.id) {
    isEdit.value = true
    articleId.value = route.params.id as string
    loadArticle()
  }
})
</script>

<style scoped>
.article-editor {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem;
  transition: background-color 0.3s ease;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--card-bg);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-left h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-primary);
  font-weight: 600;
  transition: color 0.3s ease;
}

.header-right {
  display: flex;
  gap: 1rem;
}

.editor-form {
  max-width: 1200px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 1.5rem;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.form-card :deep(.el-card__body) {
  padding: 2rem;
}

:deep(.el-form-item__label) {
  color: var(--text-primary);
  font-weight: 500;
}

:deep(.el-input__inner) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-textarea__inner) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

:deep(.el-select__wrapper) {
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
}

@media (max-width: 768px) {
  .article-editor {
    padding: 1rem;
  }

  .editor-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .header-left {
    width: 100%;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
  }

  .header-left h1 {
    font-size: 1.25rem;
  }
}
</style>
