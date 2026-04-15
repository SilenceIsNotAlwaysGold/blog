<template>
  <div class="comment-section">
    <div class="comment-header">
      <h3>
        <el-icon><ChatDotRound /></el-icon>
        评论 ({{ total }})
      </h3>
    </div>

    <!-- 评论输入框 -->
    <div class="comment-input-area" v-if="isLoggedIn">
      <el-input
        v-model="newComment"
        type="textarea"
        :rows="4"
        placeholder="写下你的评论..."
        maxlength="1000"
        show-word-limit
      />
      <div class="comment-actions">
        <el-button
          type="primary"
          @click="handleSubmitComment"
          :loading="submitting"
          :disabled="!newComment.trim()"
        >
          发表评论
        </el-button>
      </div>
    </div>

    <div v-else class="login-prompt">
      <el-icon><Lock /></el-icon>
      <span>请先<a href="/login">登录</a>后再评论</span>
    </div>

    <!-- 评论列表 -->
    <el-skeleton v-if="loading" :rows="5" animated />

    <div v-else-if="comments.length > 0" class="comment-list">
      <CommentItem
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @reply="handleReply"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <el-empty v-else description="暂无评论，快来抢沙发吧！" />

    <!-- 回复弹窗 -->
    <el-dialog v-model="replyDialogVisible" title="回复评论" width="600px">
      <div class="reply-to">
        回复 <strong>{{ replyTo?.username }}</strong>：{{ replyTo?.content }}
      </div>
      <el-input
        v-model="replyContent"
        type="textarea"
        :rows="4"
        placeholder="写下你的回复..."
        maxlength="1000"
        show-word-limit
      />
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleSubmitReply"
          :loading="submitting"
          :disabled="!replyContent.trim()"
        >
          提交回复
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editDialogVisible" title="编辑评论" width="600px">
      <el-input
        v-model="editContent"
        type="textarea"
        :rows="4"
        placeholder="修改你的评论..."
        maxlength="1000"
        show-word-limit
      />
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleSubmitEdit"
          :loading="submitting"
          :disabled="!editContent.trim()"
        >
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ChatDotRound, Lock } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CommentItem from './CommentItem.vue'
import { getArticleComments, createComment, updateComment, deleteComment, type Comment } from '@/api/comment'

interface Props {
  articleId: string
}

const props = defineProps<Props>()

const loading = ref(false)
const comments = ref<Comment[]>([])
const total = ref(0)
const newComment = ref('')
const submitting = ref(false)

// 回复相关
const replyDialogVisible = ref(false)
const replyTo = ref<Comment | null>(null)
const replyContent = ref('')

// 编辑相关
const editDialogVisible = ref(false)
const editingComment = ref<Comment | null>(null)
const editContent = ref('')

// 检查是否登录
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

const fetchComments = async () => {
  loading.value = true
  try {
    const response: any = await getArticleComments(props.articleId)
    const data = response.data
    comments.value = data.comments
    total.value = data.total
  } catch (error: any) {
    console.error('Failed to fetch comments:', error)
  } finally {
    loading.value = false
  }
}

const handleSubmitComment = async () => {
  if (!newComment.value.trim()) return

  submitting.value = true
  try {
    await createComment(props.articleId, {
      content: newComment.value.trim()
    })
    newComment.value = ''
    ElMessage.success('评论成功')
    await fetchComments()
  } catch (error: any) {
    console.error('Failed to create comment:', error)
    ElMessage.error(error.response?.data?.detail || '评论失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleReply = (comment: Comment) => {
  replyTo.value = comment
  replyContent.value = ''
  replyDialogVisible.value = true
}

const handleSubmitReply = async () => {
  if (!replyContent.value.trim() || !replyTo.value) return

  submitting.value = true
  try {
    await createComment(props.articleId, {
      content: replyContent.value.trim(),
      parent_id: replyTo.value.id
    })
    replyContent.value = ''
    replyDialogVisible.value = false
    ElMessage.success('回复成功')
    await fetchComments()
  } catch (error: any) {
    console.error('Failed to reply comment:', error)
    ElMessage.error(error.response?.data?.detail || '回复失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleEdit = (comment: Comment) => {
  editingComment.value = comment
  editContent.value = comment.content
  editDialogVisible.value = true
}

const handleSubmitEdit = async () => {
  if (!editContent.value.trim() || !editingComment.value) return

  submitting.value = true
  try {
    await updateComment(editingComment.value.id, {
      content: editContent.value.trim()
    })
    editContent.value = ''
    editDialogVisible.value = false
    ElMessage.success('修改成功')
    await fetchComments()
  } catch (error: any) {
    console.error('Failed to update comment:', error)
    ElMessage.error(error.response?.data?.detail || '修改失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (comment: Comment) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条评论吗？此操作不可撤销。',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteComment(comment.id)
    ElMessage.success('删除成功')
    await fetchComments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('Failed to delete comment:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败，请稍后重试')
    }
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<style scoped>
.comment-section {
  margin-top: 3rem;
  padding: 2rem;
  background: var(--card-bg);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--border-color);
}

.comment-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
  font-size: 1.5rem;
  color: var(--text-primary);
}

.comment-input-area {
  margin-bottom: 2rem;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.login-prompt {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 2rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.login-prompt a {
  color: var(--accent-primary);
  text-decoration: none;
  font-weight: 500;
}

.login-prompt a:hover {
  text-decoration: underline;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reply-to {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-left: 3px solid var(--accent-primary);
  border-radius: 4px;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.reply-to strong {
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .comment-section {
    padding: 1.5rem;
  }
}
</style>
