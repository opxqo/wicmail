<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:check-square text-18" /> 申请审核</span>
      </template>
      <template #header-extra>
        <n-select
          v-model:value="statusFilter"
          :options="statusOptions"
          placeholder="筛选状态"
          clearable
          style="width: 150px"
          @update:value="loadApplications"
        />
      </template>

      <n-data-table :columns="columns" :data="applications" :loading="loading" />
    </n-card>

    <!-- 审核弹窗 -->
    <n-modal v-model:show="reviewModal.visible" preset="dialog" style="max-width: 560px;" :title="reviewModal.title" positive-text="确认" negative-text="取消" @positive-click="handleReview">
      <!-- 申请材料展示 -->
      <div v-if="reviewModal.attachments?.length" class="mb-16">
        <div class="mb-8 flex items-center gap-6 text-14 font-bold">
          <i class="i-fe:paperclip text-14" /> 申请材料（{{ reviewModal.attachments.length }} 份）
        </div>
        <div class="attachments-grid">
          <div
            v-for="att in reviewModal.attachments"
            :key="att.id"
            class="attachment-card cursor-pointer"
            @click="previewAttachment(att)"
          >
            <img v-if="att.url && isImage(att.content_type)" :src="att.url" class="attachment-thumb" alt="preview">
            <i v-else-if="isImage(att.content_type)" class="i-fe:image text-32 opacity-20" />
            <i v-else class="i-fe:file-text text-32 opacity-20" />
            <div class="mt-6 truncate text-12" :title="att.filename">
              {{ att.filename }}
            </div>
            <div class="text-11 opacity-40">
              {{ formatSize(att.size) }}
            </div>
          </div>
        </div>
        <n-divider class="my-12!" />
      </div>

      <n-input v-model:value="reviewModal.comment" type="textarea" placeholder="审核备注（可选）" :rows="3" />
    </n-modal>

    <!-- 材料大图预览 -->
    <n-modal v-model:show="imagePreview.visible" preset="card" :title="imagePreview.filename" style="max-width: 720px;">
      <div class="flex justify-center">
        <img v-if="imagePreview.url" :src="imagePreview.url" class="max-h-500px max-w-full rounded-8" alt="preview">
        <div v-else class="flex flex-col items-center py-60 opacity-30">
          <i class="i-fe:image text-64" />
          <span class="mt-12">Mock 模式暂无实际文件预览</span>
        </div>
      </div>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NSpace, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import { approveApplication, getAdminApplications, rejectApplication } from '@/api/wicmail'
import { AppPage } from '@/components'

const loading = ref(false)
const applications = ref([])
const statusFilter = ref(null)

const statusOptions = [
  { label: '待审核', value: 'pending' },
  { label: '已批准', value: 'approved' },
  { label: '已拒绝', value: 'rejected' },
]

const statusMap = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已批准', type: 'success' },
  rejected: { label: '已拒绝', type: 'error' },
}

const reviewModal = reactive({
  visible: false,
  title: '',
  action: '',
  appId: null,
  comment: '',
  attachments: [],
})

const imagePreview = reactive({
  visible: false,
  filename: '',
  url: '',
})

function isImage(contentType) {
  return contentType?.startsWith('image/')
}

function formatSize(bytes) {
  if (!bytes)
    return '0 B'
  if (bytes < 1024)
    return `${bytes} B`
  if (bytes < 1024 * 1024)
    return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function previewAttachment(att) {
  imagePreview.filename = att.filename
  imagePreview.url = att.url || ''
  imagePreview.visible = true
}

const columns = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '申请人', key: 'username', width: 100 },
  { title: '申请地址', key: 'requested_address', ellipsis: { tooltip: true } },
  { title: '显示名称', key: 'display_name', render: row => row.display_name || '-', width: 120 },
  {
    title: '状态',
    key: 'status',
    width: 90,
    render(row) {
      const s = statusMap[row.status] || { label: row.status, type: 'default' }
      return h(NTag, { type: s.type, size: 'small', round: true }, { default: () => s.label })
    },
  },
  {
    title: '材料',
    key: 'attachments',
    width: 80,
    render(row) {
      const count = row.attachments?.length || 0
      if (!count)
        return h('span', { class: 'opacity-30 text-12' }, '-')
      return h(NTag, { size: 'small', type: 'info', round: true, bordered: false }, {
        icon: () => h('i', { class: 'i-fe:paperclip text-12 mr-2' }),
        default: () => `${count} 份`,
      })
    },
  },
  { title: '申请理由', key: 'reason', ellipsis: { tooltip: true }, render: row => row.reason || '-' },
  { title: '审核备注', key: 'review_comment', ellipsis: { tooltip: true }, render: row => row.review_comment || '-' },
  {
    title: '申请时间',
    key: 'created_at',
    width: 150,
    render: row => row.created_at?.replace('T', ' ').slice(0, 16) || '-',
  },
  {
    title: '操作',
    key: 'actions',
    width: 160,
    fixed: 'right',
    render(row) {
      if (row.status !== 'pending')
        return h('span', { class: 'opacity-40' }, '已处理')
      return h(NSpace, null, {
        default: () => [
          h(NButton, { type: 'success', size: 'small', onClick: () => openReview(row, 'approve') }, { default: () => '批准' }),
          h(NButton, { type: 'error', size: 'small', onClick: () => openReview(row, 'reject') }, { default: () => '拒绝' }),
        ],
      })
    },
  },
]

function openReview(row, action) {
  reviewModal.visible = true
  reviewModal.action = action
  reviewModal.appId = row.id
  reviewModal.comment = ''
  reviewModal.attachments = row.attachments || []
  reviewModal.title = action === 'approve' ? `批准申请：${row.requested_address}` : `拒绝申请：${row.requested_address}`
}

async function handleReview() {
  try {
    if (reviewModal.action === 'approve') {
      await approveApplication(reviewModal.appId, reviewModal.comment)
      $message.success('已批准')
    }
    else {
      await rejectApplication(reviewModal.appId, reviewModal.comment)
      $message.success('已拒绝')
    }
    await loadApplications()
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

async function loadApplications() {
  loading.value = true
  try {
    const res = await getAdminApplications(statusFilter.value)
    const data = res.data || res
    applications.value = Array.isArray(data) ? data : []
  }
  catch (err) {
    console.error('加载申请列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

onMounted(() => loadApplications())
</script>

<style scoped>
.attachments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.attachment-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  transition: all 0.2s;
}
.attachment-card:hover {
  border-color: #059669;
  background: #ecfdf5;
}
.attachment-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 6px;
}
</style>
