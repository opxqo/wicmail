<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:inbox text-18" /> 邮件中心</span>
      </template>

      <!-- 现代化扁平单行搜索过滤工具栏 -->
      <div class="search-bar-wrapper mb-16">
        <div class="flex flex-wrap items-center justify-between gap-12">
          <div class="min-w-0 flex flex-1 flex-wrap items-center gap-12">
            <n-input
              v-model:value="searchForm.q"
              placeholder="搜索主题、发件人、正文..."
              clearable
              style="max-width: 320px; min-width: 220px;"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <i class="i-fe:search mr-4 text-slate-400" />
              </template>
            </n-input>

            <n-input
              v-model:value="searchForm.sender"
              placeholder="过滤发件人..."
              clearable
              style="max-width: 200px; min-width: 150px;"
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <i class="i-fe:user mr-4 text-slate-400" />
              </template>
            </n-input>

            <n-select
              v-model:value="searchForm.is_read"
              :options="readStatusOptions"
              placeholder="阅读状态"
              clearable
              style="width: 120px;"
              @update:value="handleSearch"
            />
          </div>

          <div class="flex items-center gap-8">
            <n-button type="primary" @click="handleSearch">
              <template #icon>
                <i class="i-fe:search" />
              </template>
              查询
            </n-button>
            <n-button secondary @click="handleReset">
              <template #icon>
                <i class="i-fe:rotate-ccw" />
              </template>
              重置
            </n-button>
          </div>
        </div>
      </div>

      <n-data-table
        :columns="columns"
        :data="emails"
        :loading="loading"
        :pagination="pagination"
        :row-props="rowProps"
        remote
        @update:page="handlePageChange"
      />
    </n-card>

    <!-- 邮件详情抽屉 -->
    <n-drawer v-model:show="drawerVisible" :width="680" placement="right">
      <n-drawer-content v-if="currentEmail" :title="currentEmail.subject || '(无主题)'" closable>
        <div class="email-meta">
          <div class="meta-row">
            <span class="meta-label">发件人：</span>
            <span>{{ currentEmail.header_from }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">收件人：</span>
            <span>{{ currentEmail.header_to || currentEmail.envelope_to }}</span>
          </div>
          <div v-if="currentEmail.header_cc" class="meta-row">
            <span class="meta-label">抄送：</span>
            <span>{{ currentEmail.header_cc }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">时间：</span>
            <span>{{ currentEmail.received_at?.replace('T', ' ').slice(0, 19) }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">邮箱：</span>
            <NTag size="small" type="info" round>
              {{ currentEmail.mailbox_address }}
            </NTag>
          </div>
        </div>

        <n-divider />

        <!-- 邮件正文 -->
        <div v-if="currentEmail.body_html" class="email-body" v-html="currentEmail.body_html" />
        <pre v-else class="email-body-text">{{ currentEmail.body_text }}</pre>

        <!-- 附件 -->
        <template v-if="currentEmail.attachments?.length">
          <n-divider />
          <h4 class="flex items-center gap-8">
            <i class="i-fe:paperclip text-16" /> 附件 ({{ currentEmail.attachments.length }})
          </h4>
          <div class="mt-8 flex flex-col gap-8">
            <div v-for="att in currentEmail.attachments" :key="att.id" class="flex items-center justify-between rounded-8 bg-gray-100 p-12">
              <div class="min-w-0 flex items-center gap-8">
                <i class="i-fe:file-text text-16" />
                <span class="truncate text-14">{{ att.filename }}</span>
              </div>
              <div class="ml-12 flex shrink-0 items-center gap-12">
                <span class="text-12 opacity-50">{{ formatSize(att.size) }}</span>
                <n-button
                  v-if="att.has_file"
                  size="small"
                  text
                  type="primary"
                  @click.stop="handleDownloadAttachment(att)"
                >
                  <template #icon>
                    <i class="i-fe:download" />
                  </template>
                  下载
                </n-button>
              </div>
            </div>
          </div>
        </template>

        <template #footer>
          <n-button
            :type="currentEmail.is_read ? 'default' : 'primary'"
            ghost
            @click="toggleRead"
          >
            {{ currentEmail.is_read ? '标记未读' : '标记已读' }}
          </n-button>
        </template>
      </n-drawer-content>
    </n-drawer>
  </AppPage>
</template>

<script setup>
import { NTag } from 'naive-ui'
import { h, onMounted, reactive, ref } from 'vue'
import {
  downloadAttachment as getAttachmentDownloadUrl,
  getEmailDetail,
  getEmails,
  markEmailRead,
  markEmailUnread,
} from '@/api/wicmail'
import { AppPage } from '@/components'
import { useUserStore } from '@/store'

const loading = ref(false)
const emails = ref([])
const drawerVisible = ref(false)
const currentEmail = ref(null)

const userStore = useUserStore()

const searchForm = reactive({
  q: '',
  sender: '',
  is_read: null,
})

const readStatusOptions = [
  { label: '全部邮件', value: null },
  { label: '已读', value: 'true' },
  { label: '未读', value: 'false' },
]

const pagination = reactive({
  page: 1,
  pageSize: 20,
  pageCount: 1,
  itemCount: 0,
  showSizePicker: false,
  onUpdatePage: handlePageChange,
})

function handleSearch() {
  pagination.page = 1
  loadEmails()
}

function handleReset() {
  searchForm.q = ''
  searchForm.sender = ''
  searchForm.is_read = null
  pagination.page = 1
  loadEmails()
}

const columns = [
  {
    title: '状态',
    key: 'is_read',
    width: 70,
    render(row) {
      return h(NTag, {
        type: row.is_read ? 'default' : 'info',
        size: 'small',
        round: true,
      }, { default: () => row.is_read ? '已读' : '未读' })
    },
  },
  { title: '发件人', key: 'header_from', width: 180, ellipsis: { tooltip: true } },
  { title: '主题', key: 'subject', ellipsis: { tooltip: true }, render: row => row.subject || '(无主题)' },
  {
    title: '收件箱',
    key: 'mailbox_address',
    width: 180,
    ellipsis: { tooltip: true },
  },
  {
    title: '附件',
    key: 'attachment_count',
    width: 70,
    render(row) {
      if (row.attachment_count <= 0)
        return ''
      return h('span', { class: 'flex items-center gap-2' }, [
        h('i', { class: 'i-fe:paperclip text-14' }),
        String(row.attachment_count),
      ])
    },
  },
  {
    title: '时间',
    key: 'received_at',
    width: 160,
    render: row => row.received_at?.replace('T', ' ').slice(0, 16) || '-',
  },
]

function rowProps(row) {
  return {
    style: { cursor: 'pointer' },
    onClick: () => openEmail(row),
  }
}

async function openEmail(row) {
  try {
    const res = await getEmailDetail(row.id)
    currentEmail.value = res.data || res
    drawerVisible.value = true
    if (!row.is_read) {
      await markEmailRead(row.id)
      row.is_read = true
      userStore.updateUnreadCount()
    }
  }
  catch (err) {
    $message.error('加载邮件详情失败')
    console.error(err)
  }
}

async function toggleRead() {
  if (!currentEmail.value)
    return
  try {
    if (currentEmail.value.is_read) {
      await markEmailUnread(currentEmail.value.id)
      currentEmail.value.is_read = false
    }
    else {
      await markEmailRead(currentEmail.value.id)
      currentEmail.value.is_read = true
    }
    // 同步列表中的状态
    const item = emails.value.find(e => e.id === currentEmail.value.id)
    if (item)
      item.is_read = currentEmail.value.is_read
    userStore.updateUnreadCount()
  }
  catch (err) {
    $message.error('操作失败')
    console.error(err)
  }
}

async function handleDownloadAttachment(att) {
  try {
    const res = await getAttachmentDownloadUrl(att.id)
    const data = res.data || res
    if (!data.download_url) {
      $message.error('下载链接无效')
      return
    }
    window.open(data.download_url, '_blank', 'noopener,noreferrer')
  }
  catch (err) {
    $message.error(err?.message || '获取下载链接失败')
    console.error(err)
  }
}

function handlePageChange(page) {
  pagination.page = page
  loadEmails()
}

function formatSize(bytes) {
  if (bytes < 1024)
    return `${bytes} B`
  if (bytes < 1024 * 1024)
    return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

async function loadEmails() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
    }
    if (searchForm.q)
      params.q = searchForm.q
    if (searchForm.sender)
      params.sender = searchForm.sender
    if (searchForm.is_read !== null)
      params.is_read = searchForm.is_read

    const res = await getEmails(params)
    const data = res.data || res
    emails.value = data.emails || []
    pagination.itemCount = data.total || 0
    pagination.pageCount = Math.ceil((data.total || 0) / pagination.pageSize)
  }
  catch (err) {
    console.error('加载邮件列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

onMounted(() => {
  loadEmails()
  userStore.updateUnreadCount()
})
</script>

<style scoped>
.search-bar-wrapper {
  padding: 16px;
  background: var(--n-card-color-modal, #fcfcfc);
  border: 1px solid var(--n-border-color, #efeff5);
  border-radius: 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
}
.email-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
.meta-label {
  color: #64748b;
  min-width: 60px;
  flex-shrink: 0;
}
.email-body {
  padding: 16px 0;
  overflow-x: auto;
}
.email-body-text {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.6;
}
</style>
