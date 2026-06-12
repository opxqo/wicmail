<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <div class="w-full flex items-center justify-between">
          <span class="flex items-center gap-8"><i class="i-fe:inbox text-18" /> 邮件管理</span>
          <NButton
            type="error"
            size="small"
            :disabled="checkedRowKeys.length === 0"
            @click="handleBatchDelete"
          >
            <template #icon>
              <i class="i-fe:trash-2" />
            </template>
            批量删除 ({{ checkedRowKeys.length }})
          </NButton>
        </div>
      </template>

      <!-- 搜索筛选区 -->
      <div class="mb-16 flex flex-wrap items-center justify-between gap-16">
        <div class="flex flex-wrap items-center gap-16">
          <n-input
            v-model:value="searchParams.q"
            placeholder="搜索关键词 (主题/发件人/正文)"
            clearable
            style="width: 260px"
            @keyup.enter="handleSearch"
          />
          <n-input
            v-model:value="searchParams.sender"
            placeholder="筛选发件人"
            clearable
            style="width: 180px"
            @keyup.enter="handleSearch"
          />
          <n-select
            v-model:value="searchParams.is_read"
            placeholder="已读状态"
            clearable
            :options="[
              { label: '已读', value: 'true' },
              { label: '未读', value: 'false' },
            ]"
            style="width: 120px"
            @update:value="handleSearch"
          />
          <NButton type="primary" ghost @click="handleSearch">
            查询
          </NButton>
          <NButton ghost @click="handleReset">
            重置
          </NButton>
        </div>
        <div class="flex items-center gap-8">
          <span class="text-12 opacity-60">全文搜索模式</span>
          <n-switch v-model:value="isFullTextMode" @update:value="handleSearch" />
        </div>
      </div>

      <!-- 数据表格 -->
      <n-data-table
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="emails"
        :loading="loading"
        :row-key="row => row.id"
      />

      <!-- 分页组件 -->
      <div class="mt-16 flex justify-end">
        <n-pagination
          v-model:page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :item-count="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          show-size-picker
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
        />
      </div>
    </n-card>

    <!-- 邮件详情弹窗 -->
    <n-modal
      v-model:show="showDetailModal"
      preset="card"
      title="邮件详情"
      style="width: 780px; max-width: 90vw;"
      :segmented="{ content: 'soft' }"
    >
      <div v-if="detailLoading" class="flex justify-center py-40">
        <n-spin size="large" />
      </div>
      <div v-else>
        <!-- 邮件元信息 -->
        <n-descriptions bordered label-placement="left" :column="2" class="mb-16">
          <n-descriptions-item label="所属邮箱" :span="2">
            {{ currentDetail.mailbox_address }}
          </n-descriptions-item>
          <n-descriptions-item label="发件人">
            {{ currentDetail.header_from }}
          </n-descriptions-item>
          <n-descriptions-item label="收件人">
            {{ currentDetail.header_to }}
          </n-descriptions-item>
          <n-descriptions-item label="邮件主题" :span="2">
            <span class="font-bold">{{ currentDetail.subject }}</span>
          </n-descriptions-item>
          <n-descriptions-item label="接收时间">
            {{ currentDetail.received_at?.replace('T', ' ').slice(0, 16) }}
          </n-descriptions-item>
          <n-descriptions-item label="邮件大小">
            {{ formatSize(currentDetail.raw_size) }}
          </n-descriptions-item>
        </n-descriptions>

        <!-- 邮件正文 -->
        <n-card title="邮件正文" size="small" class="mb-16 bg-gray-50/50">
          <div v-if="currentDetail.body_html" class="email-body-html max-h-400 overflow-x-auto p-8" v-html="currentDetail.body_html" />
          <div v-else class="max-h-400 overflow-y-auto whitespace-pre-wrap text-13 font-mono">
            {{ currentDetail.body_text || '(无正文)' }}
          </div>
        </n-card>

        <!-- 附件列表 -->
        <div v-if="currentDetail.attachments?.length" class="mt-16">
          <div class="mb-8 flex items-center gap-4 font-bold">
            <i class="i-fe:paperclip" /> 附件 ({{ currentDetail.attachments.length }})
          </div>
          <div class="grid grid-cols-2 gap-12">
            <div
              v-for="file in currentDetail.attachments"
              :key="file.id"
              class="flex items-center justify-between border rounded-8 bg-gray-50/30 p-8"
            >
              <div class="min-w-0 flex items-center gap-8">
                <i class="i-fe:file text-20 text-gray-500" />
                <div class="min-w-0">
                  <div class="truncate text-13 font-medium" :title="file.filename">
                    {{ file.filename }}
                  </div>
                  <div class="text-12 opacity-50">
                    {{ formatSize(file.size) }}
                  </div>
                </div>
              </div>
              <NButton size="tiny" secondary type="primary">
                下载
              </NButton>
            </div>
          </div>
        </div>
      </div>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NPopconfirm, NSpace, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import {
  batchDeleteAdminEmails,
  deleteAdminEmail,
  getAdminEmailDetail,
  getAdminEmails,
  searchAdminEmails,
} from '@/api/wicmail'
import { AppPage } from '@/components'

const loading = ref(false)
const detailLoading = ref(false)
const emails = ref([])
const checkedRowKeys = ref([])
const isFullTextMode = ref(false)

const searchParams = ref({
  q: '',
  sender: '',
  is_read: null,
})

const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0,
})

const showDetailModal = ref(false)
const currentDetail = ref({})

const columns = [
  { type: 'selection' },
  { title: 'ID', key: 'id', width: 60 },
  { title: '所属邮箱', key: 'mailbox_address', width: 180, ellipsis: { tooltip: true } },
  { title: '发件人', key: 'header_from', width: 180, ellipsis: { tooltip: true } },
  { title: '主题', key: 'subject', ellipsis: { tooltip: true } },
  {
    title: '大小',
    key: 'raw_size',
    width: 90,
    render: row => formatSize(row.raw_size),
  },
  {
    title: '状态',
    key: 'is_read',
    width: 90,
    render(row) {
      return h(
        NTag,
        { type: row.is_read ? 'default' : 'info', size: 'small', round: true },
        { default: () => (row.is_read ? '已读' : '未读') },
      )
    },
  },
  {
    title: '接收时间',
    key: 'received_at',
    width: 160,
    render: row => row.received_at?.replace('T', ' ').slice(0, 16) || '-',
  },
  {
    title: '操作',
    key: 'actions',
    width: 140,
    fixed: 'right',
    render(row) {
      return h(
        NSpace,
        { size: 8 },
        {
          default: () => [
            h(
              NButton,
              { size: 'small', type: 'primary', ghost: true, onClick: () => handleViewDetail(row.id) },
              { default: () => '查看' },
            ),
            h(
              NPopconfirm,
              { onPositiveClick: () => handleDelete(row) },
              {
                trigger: () => h(NButton, { size: 'small', type: 'error', ghost: true }, { default: () => '删除' }),
                default: () => `确认删除该邮件吗？此操作不可撤销！`,
              },
            ),
          ],
        },
      )
    },
  },
]

function formatSize(bytes) {
  if (!bytes)
    return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${Number((bytes / k ** i).toFixed(1))} ${sizes[i]}`
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
    }
    if (searchParams.value.q)
      params.q = searchParams.value.q
    if (searchParams.value.sender)
      params.sender = searchParams.value.sender
    if (searchParams.value.is_read !== null) {
      params.is_read = searchParams.value.is_read === 'true'
    }

    const fetchApi = isFullTextMode.value ? searchAdminEmails : getAdminEmails
    const res = await fetchApi(params)
    const data = res.data || res
    emails.value = data.emails || []
    pagination.value.total = data.total || 0
  }
  catch (err) {
    console.error('加载邮件列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.value.page = 1
  loadData()
}

function handleReset() {
  searchParams.value.q = ''
  searchParams.value.sender = ''
  searchParams.value.is_read = null
  pagination.value.page = 1
  loadData()
}

function handlePageChange(page) {
  pagination.value.page = page
  loadData()
}

function handlePageSizeChange(pageSize) {
  pagination.value.pageSize = pageSize
  pagination.value.page = 1
  loadData()
}

async function handleViewDetail(id) {
  showDetailModal.value = true
  detailLoading.value = true
  try {
    const res = await getAdminEmailDetail(id)
    currentDetail.value = res.data || res
  }
  catch (err) {
    $message.error(err.message || '获取邮件详情失败')
    showDetailModal.value = false
  }
  finally {
    detailLoading.value = false
  }
}

async function handleDelete(row) {
  try {
    const res = await deleteAdminEmail(row.id)
    const data = res.data || res
    $message.success(data.message || '删除成功')
    await loadData()
  }
  catch (err) {
    $message.error(err.message || '删除失败')
  }
}

async function handleBatchDelete() {
  $dialog.warning({
    title: '批量删除提示',
    content: `确认批量删除选中的 ${checkedRowKeys.value.length} 封邮件吗？此操作不可逆！`,
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: async () => {
      try {
        const res = await batchDeleteAdminEmails(checkedRowKeys.value)
        const data = res.data || res
        $message.success(data.message || `已成功删除 ${data.count} 封邮件`)
        checkedRowKeys.value = []
        await loadData()
      }
      catch (err) {
        $message.error(err.message || '批量删除失败')
      }
    },
  })
}

onMounted(() => loadData())
</script>

<style scoped>
.email-body-html :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
