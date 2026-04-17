<template>
  <div class="project-editor">
    <div class="editor-header">
      <div class="header-left">
        <el-button :icon="ArrowLeft" @click="handleBack">返回</el-button>
        <h1>{{ isEdit ? '编辑项目' : '新建项目' }}</h1>
        <span v-if="dirty" class="dirty-badge">未保存</span>
      </div>
      <div class="header-right">
        <el-button v-if="isEdit" @click="handlePreview">预览</el-button>
        <el-button @click="handleSave" :loading="saving" type="primary">
          {{ isEdit ? '更新项目' : '创建项目' }}
        </el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="editor-form"
    >
      <!-- 基本信息 -->
      <el-card shadow="never" class="form-card">
        <template #header><span class="card-header-title">基本信息</span></template>

        <el-form-item label="项目名称" prop="name">
          <el-input
            v-model="form.name"
            placeholder="请输入项目名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
                <el-option v-for="opt in statusOptions" :key="opt.value" :label="opt.label" :value="opt.value">
                  <span class="status-dot" :class="'dot-' + opt.value"></span>
                  <span>{{ opt.label }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序" prop="order">
              <el-input-number
                v-model="form.order"
                :min="0"
                :max="999"
                style="width: 100%"
              />
              <span class="field-hint">数值越大越靠前</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="技术栈" prop="tech_stack">
          <el-select
            v-model="form.tech_stack"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入技术名，按回车添加"
            style="width: 100%"
          />
          <span class="field-hint">建议 3-8 项，按重要程度排列</span>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始日期" prop="start_date">
              <el-date-picker
                v-model="form.start_date"
                type="date"
                placeholder="选择开始日期"
                style="width: 100%"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期" prop="end_date">
              <el-date-picker
                v-model="form.end_date"
                type="date"
                placeholder="留空表示进行中"
                style="width: 100%"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- 封面与链接 -->
      <el-card shadow="never" class="form-card">
        <template #header><span class="card-header-title">封面与链接</span></template>

        <el-form-item label="封面图片" prop="cover_image">
          <div class="cover-upload">
            <el-upload
              class="cover-uploader"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :before-upload="beforeCoverUpload"
              :on-success="handleCoverSuccess"
              :on-error="handleCoverError"
              name="file"
              accept="image/*"
            >
              <img v-if="form.cover_image" :src="form.cover_image" class="cover-preview" />
              <div v-else class="cover-placeholder">
                <el-icon :size="28"><Plus /></el-icon>
                <span>上传封面</span>
              </div>
            </el-upload>
            <div class="cover-url">
              <el-input
                v-model="form.cover_image"
                placeholder="或直接粘贴图片 URL"
                clearable
              >
                <template #append>
                  <el-button v-if="form.cover_image" @click="form.cover_image = ''">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </template>
              </el-input>
              <span class="field-hint">推荐尺寸 16:9，≤ 2MB，自动压缩为 WebP</span>
            </div>
          </div>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Demo URL" prop="demo_url">
              <el-input
                v-model="form.demo_url"
                placeholder="https://..."
                clearable
              >
                <template #append>
                  <el-button
                    :disabled="!isValidUrl(form.demo_url)"
                    :icon="Link"
                    @click="openUrl(form.demo_url)"
                    title="在新标签打开"
                  />
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="GitHub URL" prop="github_url">
              <el-input
                v-model="form.github_url"
                placeholder="https://github.com/..."
                clearable
              >
                <template #append>
                  <el-button
                    :disabled="!isValidUrl(form.github_url)"
                    :icon="Link"
                    @click="openUrl(form.github_url)"
                    title="在新标签打开"
                  />
                </template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- 项目描述 -->
      <el-card shadow="never" class="form-card">
        <template #header>
          <div class="card-header-row">
            <span class="card-header-title">项目描述</span>
            <span class="field-hint">支持 Markdown，将在项目详情页完整渲染；卡片处仅取前 120 字作为纯文本摘要</span>
          </div>
        </template>

        <el-form-item prop="description" label-width="0">
          <MarkdownEditor
            v-model="form.description"
            height="420px"
            placeholder="用 Markdown 描述这个项目：它解决什么问题、你做了什么、效果如何..."
          />
        </el-form-item>
      </el-card>

      <!-- 亮点 -->
      <el-card shadow="never" class="form-card">
        <template #header>
          <div class="card-header-row">
            <span class="card-header-title">项目亮点</span>
            <span class="field-hint">每行一条，一句话可读；前 2 条会出现在卡片预览</span>
          </div>
        </template>

        <div class="highlight-list">
          <div
            v-for="(_, idx) in form.highlights"
            :key="idx"
            class="highlight-row"
          >
            <span class="highlight-idx">{{ idx + 1 }}</span>
            <el-input
              v-model="form.highlights[idx]"
              placeholder="例如：Text2SQL 智能体解决问题概率达 85%"
              maxlength="200"
              show-word-limit
            />
            <el-button-group>
              <el-button :icon="ArrowUp" :disabled="idx === 0" @click="moveHighlight(idx, -1)" title="上移" />
              <el-button :icon="ArrowDown" :disabled="idx === form.highlights.length - 1" @click="moveHighlight(idx, 1)" title="下移" />
              <el-button :icon="Delete" type="danger" plain @click="removeHighlight(idx)" title="删除" />
            </el-button-group>
          </div>
          <el-button
            class="add-highlight-btn"
            :icon="Plus"
            @click="addHighlight"
          >添加亮点</el-button>
        </div>
      </el-card>
    </el-form>

    <!-- Preview -->
    <ProjectDetailDialog
      v-model="previewVisible"
      :project="previewProject"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onBeforeUnmount, defineAsyncComponent, watch } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { ArrowLeft, ArrowUp, ArrowDown, Delete, Plus, Link } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules, type UploadProps } from 'element-plus'
import { createProject, updateProject, getProject, type Project, type ProjectCreate, type ProjectUpdate } from '@/api/project'

const MarkdownEditor = defineAsyncComponent(() => import('@/components/article/MarkdownEditor.vue'))
const ProjectDetailDialog = defineAsyncComponent(() => import('@/components/project/ProjectDetailDialog.vue'))

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInstance>()
const saving = ref(false)
const isEdit = ref(false)
const projectId = ref('')
const previewVisible = ref(false)

const form = reactive({
  name: '',
  description: '',
  tech_stack: [] as string[],
  cover_image: '',
  demo_url: '',
  github_url: '',
  start_date: '',
  end_date: '',
  status: 'in_progress' as 'completed' | 'in_progress' | 'planned',
  highlights: [] as string[],
  order: 0
})

const statusOptions = [
  { label: '已完成', value: 'completed' },
  { label: '进行中', value: 'in_progress' },
  { label: '计划中', value: 'planned' }
]

const urlPattern = /^https?:\/\/[^\s]+$/i
const isValidUrl = (v: string) => !!v && urlPattern.test(v.trim())
const openUrl = (url: string) => {
  if (isValidUrl(url)) window.open(url, '_blank', 'noopener,noreferrer')
}

const rules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 100, message: '名称长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' }
  ],
  tech_stack: [
    { required: true, message: '请至少添加一个技术栈', trigger: 'change', type: 'array', min: 1 }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ],
  demo_url: [
    { validator: (_r, v, cb) => !v || isValidUrl(v) ? cb() : cb(new Error('需要以 http:// 或 https:// 开头')), trigger: 'blur' }
  ],
  github_url: [
    { validator: (_r, v, cb) => !v || isValidUrl(v) ? cb() : cb(new Error('需要以 http:// 或 https:// 开头')), trigger: 'blur' }
  ]
}

// ---- upload ----
const uploadUrl = '/api/v1/images/upload'
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${localStorage.getItem('access_token') || ''}`
}))

const beforeCoverUpload: UploadProps['beforeUpload'] = (file) => {
  const okType = /^image\//.test(file.type)
  const okSize = file.size / 1024 / 1024 < 5
  if (!okType) { ElMessage.error('只能上传图片文件'); return false }
  if (!okSize) { ElMessage.error('图片大小不能超过 5MB'); return false }
  return true
}
const handleCoverSuccess: UploadProps['onSuccess'] = (res) => {
  const url = res?.data?.url
  if (url) {
    form.cover_image = url
    ElMessage.success('封面上传成功')
  } else {
    ElMessage.error(res?.message || '上传失败')
  }
}
const handleCoverError: UploadProps['onError'] = (err: any) => {
  ElMessage.error(err?.message || '上传失败')
}

// ---- highlights ----
const addHighlight = () => form.highlights.push('')
const removeHighlight = (idx: number) => form.highlights.splice(idx, 1)
const moveHighlight = (idx: number, delta: number) => {
  const target = idx + delta
  if (target < 0 || target >= form.highlights.length) return
  const moved = form.highlights.splice(idx, 1)[0]
  form.highlights.splice(target, 0, moved)
}

// ---- dirty tracking ----
const initialSnapshot = ref('')
const snapshot = () => JSON.stringify(form)
const dirty = computed(() => snapshot() !== initialSnapshot.value)
const markClean = () => { initialSnapshot.value = snapshot() }

// ---- preview ----
const previewProject = computed<Project>(() => ({
  id: projectId.value || '__preview__',
  name: form.name || '（未命名项目）',
  description: form.description,
  tech_stack: form.tech_stack,
  cover_image: form.cover_image || undefined,
  demo_url: form.demo_url || undefined,
  github_url: form.github_url || undefined,
  start_date: form.start_date || undefined,
  end_date: form.end_date || undefined,
  status: form.status,
  highlights: form.highlights.filter(h => h.trim()),
  order: form.order,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString()
}))
const handlePreview = () => { previewVisible.value = true }

// ---- load / save ----
const loadProject = async () => {
  try {
    const response = await getProject(projectId.value)
    const p = response.data

    form.name = p.name
    form.description = p.description
    form.tech_stack = p.tech_stack || []
    form.cover_image = p.cover_image || ''
    form.demo_url = p.demo_url || ''
    form.github_url = p.github_url || ''
    form.start_date = p.start_date ? p.start_date.substring(0, 10) : ''
    form.end_date = p.end_date ? p.end_date.substring(0, 10) : ''
    form.status = normalizeStatus(p.status)
    form.highlights = p.highlights || []
    form.order = p.order ?? 0

    markClean()
  } catch (error: any) {
    ElMessage.error(error.message || '加载项目失败')
    router.push('/projects')
  }
}

// 兼容 DB 里可能存在的历史状态值
const normalizeStatus = (s: string): 'completed' | 'in_progress' | 'planned' => {
  if (!s) return 'in_progress'
  const v = s.toLowerCase().replace(/-/g, '_')
  if (v === 'active') return 'in_progress'
  if (['completed', 'in_progress', 'planned'].includes(v)) return v as any
  return 'in_progress'
}

const handleBack = async () => {
  if (dirty.value) {
    try {
      await ElMessageBox.confirm('有未保存的更改，确定要离开吗？', '离开提示', {
        confirmButtonText: '放弃并离开', cancelButtonText: '留下', type: 'warning'
      })
    } catch { return }
  }
  router.push('/projects')
}

const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    saving.value = true

    const cleanHighlights = form.highlights.map(h => h.trim()).filter(Boolean)

    const data: ProjectCreate | ProjectUpdate = {
      name: form.name.trim(),
      description: form.description,
      tech_stack: form.tech_stack,
      cover_image: form.cover_image || undefined,
      demo_url: form.demo_url || undefined,
      github_url: form.github_url || undefined,
      start_date: form.start_date || undefined,
      end_date: form.end_date || undefined,
      status: form.status,
      highlights: cleanHighlights.length > 0 ? cleanHighlights : undefined,
      order: form.order
    }

    if (isEdit.value) {
      await updateProject(projectId.value, data as ProjectUpdate)
      ElMessage.success('项目更新成功')
    } else {
      const res = await createProject(data as ProjectCreate)
      projectId.value = res.data.id
      isEdit.value = true
      ElMessage.success('项目创建成功')
      router.replace(`/admin/project/edit/${projectId.value}`)
    }
    markClean()

    setTimeout(() => { router.push('/projects') }, 800)
  } catch (error: any) {
    if (error !== 'cancel' && error?.name !== 'ValidationError') {
      ElMessage.error(error?.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

// Ctrl/Cmd+S 快捷保存
const onKeydown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    handleSave()
  }
}

// Leave-guard
onBeforeRouteLeave(async () => {
  if (!dirty.value) return true
  try {
    await ElMessageBox.confirm('有未保存的更改，确定要离开吗？', '离开提示', {
      confirmButtonText: '放弃并离开', cancelButtonText: '留下', type: 'warning'
    })
    return true
  } catch {
    return false
  }
})

// Auto-save draft to localStorage while typing (new project only)
const DRAFT_KEY = 'project-editor-draft'
watch(() => snapshot(), (v) => {
  if (!isEdit.value) localStorage.setItem(DRAFT_KEY, v)
}, { flush: 'post' })

onMounted(() => {
  window.addEventListener('keydown', onKeydown)

  if (route.params.id) {
    isEdit.value = true
    projectId.value = route.params.id as string
    loadProject()
  } else {
    // 尝试恢复草稿
    const draft = localStorage.getItem(DRAFT_KEY)
    if (draft) {
      try {
        const d = JSON.parse(draft)
        ElMessageBox.confirm('发现上次未完成的草稿，是否恢复？', '草稿恢复', {
          confirmButtonText: '恢复', cancelButtonText: '丢弃', type: 'info'
        }).then(() => {
          Object.assign(form, d)
        }).catch(() => {
          localStorage.removeItem(DRAFT_KEY)
        })
      } catch { localStorage.removeItem(DRAFT_KEY) }
    }
    markClean()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  if (!isEdit.value && !dirty.value) {
    localStorage.removeItem(DRAFT_KEY)
  }
})
</script>

<style scoped>
.project-editor {
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
  position: sticky;
  top: 0;
  z-index: 10;
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
}

.dirty-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  font-size: 0.75rem;
  font-weight: 600;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.header-right { display: flex; gap: 0.75rem; }

.editor-form { max-width: 1200px; margin: 0 auto; }

.form-card {
  margin-bottom: 1.5rem;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
}

.form-card :deep(.el-card__header) {
  padding: 0.85rem 1.5rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.form-card :deep(.el-card__body) { padding: 1.75rem 2rem; }

.card-header-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
  flex-wrap: wrap;
}

.field-hint {
  display: inline-block;
  margin-left: 0.2rem;
  color: var(--text-tertiary);
  font-size: 0.78rem;
}

:deep(.el-form-item__label) { color: var(--text-primary); font-weight: 500; }
:deep(.el-input__inner) { background-color: var(--bg-secondary); border-color: var(--border-color); color: var(--text-primary); }
:deep(.el-textarea__inner) { background-color: var(--bg-secondary); border-color: var(--border-color); color: var(--text-primary); }
:deep(.el-select__wrapper) { background-color: var(--bg-secondary); border-color: var(--border-color); }

/* status dot */
.status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.dot-completed { background: #10b981; }
.dot-in_progress { background: #3b82f6; }
.dot-planned { background: #f59e0b; }

/* cover uploader */
.cover-upload {
  display: flex;
  gap: 1rem;
  width: 100%;
  align-items: flex-start;
}
.cover-uploader :deep(.el-upload) {
  width: 200px;
  height: 120px;
  border: 1px dashed var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  display: block;
  cursor: pointer;
  transition: border-color 0.2s;
  background: var(--bg-secondary);
}
.cover-uploader :deep(.el-upload):hover { border-color: var(--accent-primary); }
.cover-preview { width: 100%; height: 100%; object-fit: cover; display: block; }
.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  color: var(--text-tertiary);
  font-size: 0.85rem;
}
.cover-url { flex: 1; display: flex; flex-direction: column; gap: 0.4rem; }

/* highlights */
.highlight-list { display: flex; flex-direction: column; gap: 0.6rem; }
.highlight-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.highlight-idx {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: rgba(129, 140, 248, 0.12);
  color: var(--accent-primary);
  font-size: 0.78rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.add-highlight-btn {
  align-self: flex-start;
  border-style: dashed;
  margin-top: 0.3rem;
}

@media (max-width: 768px) {
  .project-editor { padding: 1rem; }
  .editor-header { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .header-left, .header-right { width: 100%; }
  .header-right { justify-content: flex-end; }
  .header-left h1 { font-size: 1.25rem; }
  .cover-upload { flex-direction: column; }
  .cover-uploader :deep(.el-upload) { width: 100%; }
  .highlight-row { flex-wrap: wrap; }
}
</style>
