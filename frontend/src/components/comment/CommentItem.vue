<template>
  <div class="comment-item">
    <div class="comment-avatar">
      <el-icon :size="40"><UserFilled /></el-icon>
    </div>

    <div class="comment-content-wrapper">
      <div class="comment-header">
        <span class="comment-username">{{ comment.username }}</span>
        <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
      </div>

      <div class="comment-content">
        {{ comment.content }}
      </div>

      <div class="comment-actions">
        <el-button text size="small" @click="handleReply">
          <el-icon><ChatDotRound /></el-icon>
          回复
        </el-button>

        <template v-if="isOwner">
          <el-button text size="small" @click="handleEdit">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
          <el-button text size="small" type="danger" @click="handleDelete">
            <el-icon><Delete /></el-icon>
            删除
          </el-button>
        </template>
      </div>

      <!-- 回复列表 -->
      <div v-if="comment.replies && comment.replies.length > 0" class="replies">
        <CommentItem
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :is-reply="true"
          @reply="$emit('reply', reply)"
          @edit="$emit('edit', reply)"
          @delete="$emit('delete', reply)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { UserFilled, ChatDotRound, Edit, Delete } from '@element-plus/icons-vue'
import type { Comment } from '@/api/comment'

interface Props {
  comment: Comment
  isReply?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isReply: false
})

const emit = defineEmits<{
  reply: [comment: Comment]
  edit: [comment: Comment]
  delete: [comment: Comment]
}>()

// 检查是否为评论作者
const isOwner = computed(() => {
  const token = localStorage.getItem('access_token')
  if (!token) return false

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.sub === props.comment.user_id
  } catch {
    return false
  }
})

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minute = 60 * 1000
  const hour = 60 * minute
  const day = 24 * hour

  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return `${Math.floor(diff / minute)} 分钟前`
  } else if (diff < day) {
    return `${Math.floor(diff / hour)} 小时前`
  } else if (diff < 7 * day) {
    return `${Math.floor(diff / day)} 天前`
  } else {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
}

const handleReply = () => {
  emit('reply', props.comment)
}

const handleEdit = () => {
  emit('edit', props.comment)
}

const handleDelete = () => {
  emit('delete', props.comment)
}
</script>

<style scoped>
.comment-item {
  display: flex;
  gap: 1rem;
}

.comment-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.comment-content-wrapper {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.comment-username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.comment-time {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

.comment-content {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 0.75rem;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.comment-actions :deep(.el-button) {
  padding: 4px 8px;
  height: auto;
  font-size: 0.85rem;
}

.comment-actions :deep(.el-button .el-icon) {
  margin-right: 4px;
}

.replies {
  margin-top: 1.5rem;
  padding-left: 1rem;
  border-left: 2px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .comment-item {
    gap: 0.75rem;
  }

  .comment-avatar {
    width: 36px;
    height: 36px;
  }

  .comment-avatar :deep(.el-icon) {
    font-size: 20px;
  }

  .replies {
    padding-left: 0.5rem;
  }
}
</style>
