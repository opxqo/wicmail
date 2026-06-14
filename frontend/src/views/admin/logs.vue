<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <div class="w-full flex items-center justify-between">
          <span class="flex items-center gap-8"><i class="i-fe:file-text text-18" /> 操作日志</span>
          <NButton type="primary" ghost size="small" :loading="exportLoading" @click="handleExport">
            <template #icon>
              <i class="i-fe:download" />
            </template>
            导出 CSV
          </NButton>
        </div>
      </template>

      <!-- 搜索筛选区 -->
      <div class="mb-16 flex flex-wrap items-center gap-16">
        <n-select
          v-model:value="searchParams.admin_username"
          placeholder="操作人用户名"
          clearable
          filterable
          :options="adminOptions"
          style="width: 180px"
          @update:value="handleSearch"
        />
        <n-select
          v-model:value="searchParams.action"
          placeholder="操作类型"
          clearable
          filterable
          :options="actionOptions"
          style="width: 180px"
          @update:value="handleSearch"
        />
        <n-select
          v-model:value="searchParams.target_type"
          placeholder="目标类型"
          clearable
          :options="targetTypeOptions"
          style="width: 150px"
          @update:value="handleSearch"
        />
        <n-date-picker
          v-model:value="dateRange"
          type="daterange"
          clearable
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 280px"
          @update:value="handleDateChange"
        />
        <NButton type="primary" ghost @click="handleSearch">
          查询
        </NButton>
        <NButton ghost @click="handleReset">
          重置
        </NButton>
      </div>

      <n-data-table :columns="columns" :data="logs" :loading="loading" />

      <!-- 分页组件 -->
      <div class="mt-16 flex justify-center">
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

    <!-- 日志详情弹窗 -->
    <n-modal
      v-model:show="showDetailModal"
      preset="card"
      title="操作日志详情"
      style="width: 550px"
      :segmented="{ content: 'soft' }"
    >
      <n-descriptions bordered label-placement="left" :column="1">
        <n-descriptions-item label="日志 ID">
          {{ currentDetail.id }}
        </n-descriptions-item>
        <n-descriptions-item label="操作人">
          {{ currentDetail.admin_username }} (ID: {{ currentDetail.admin_id }})
        </n-descriptions-item>
        <n-descriptions-item label="操作动作">
          <NTag type="info" size="small">
            {{ currentDetail.action }}
          </NTag>
        </n-descriptions-item>
        <n-descriptions-item label="目标类型">
          <NTag type="warning" size="small">
            {{ currentDetail.target_type }}
          </NTag>
        </n-descriptions-item>
        <n-descriptions-item label="目标名称">
          {{ currentDetail.target_name }} (ID: {{ currentDetail.target_id || '-' }})
        </n-descriptions-item>
        <n-descriptions-item label="详细说明">
          {{ currentDetail.detail }}
        </n-descriptions-item>
        <n-descriptions-item label="IP 地址">
          {{ currentDetail.ip_address }}
        </n-descriptions-item>
        <n-descriptions-item label="记录时间">
          {{ currentDetail.created_at?.replace('T', ' ').slice(0, 19) }}
        </n-descriptions-item>
      </n-descriptions>
    </n-modal>
  </AppPage>
</template>

<script setup>
import { NButton, NSpace, NTag } from 'naive-ui'
import { computed, h, onMounted, ref } from 'vue'
import { exportAdminLogs, getAdminLogs } from '@/api/wicmail'
import { AppPage } from '@/components'
import { isMock } from '@/mock/data'

const loading = ref(false)
const exportLoading = ref(false)
const logs = ref([])
const optionLogs = ref([])
const dateRange = ref(null)

const searchParams = ref({
  admin_username: '',
  action: '',
  target_type: '',
  start_date: null,
  end_date: null,
})

const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0,
})

const showDetailModal = ref(false)
const currentDetail = ref({})

const targetTypeOptions = [
  { label: '用户', value: 'user' },
  { label: '邮箱申请', value: 'application' },
  { label: '邮箱', value: 'mailbox' },
  { label: '邮件', value: 'email' },
  { label: '系统配置', value: 'config' },
  { label: '管理员', value: 'admin' },
]

const actionLabelMap = {
  update_user: '更新用户',
  toggle_user_active: '启停用户',
  delete_user: '删除用户',
  reset_password: '重置密码',
  approve_application: '批准申请',
  reject_application: '拒绝申请',
  batch_approve_application: '批量批准申请',
  batch_reject_application: '批量拒绝申请',
  create_mailbox: '创建邮箱',
  toggle_mailbox_active: '启停邮箱',
  delete_mailbox: '删除邮箱',
  delete_email: '删除邮件',
  batch_delete_email: '批量删除邮件',
  update_config: '更新配置',
  add_admin: '添加管理员',
  remove_admin: '移除管理员',
  update_role: '更新角色',
}

const adminOptions = computed(() => {
  const usernames = new Set(optionLogs.value.map(log => log.admin_username).filter(Boolean))
  return Array.from(usernames).map(username => ({ label: username, value: username }))
})

const actionOptions = computed(() => {
  const actions = new Set(optionLogs.value.map(log => log.action).filter(Boolean))
  return Array.from(actions).map(action => ({
    label: actionLabelMap[action] || action,
    value: action,
  }))
})

const columns = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '操作人', key: 'admin_username', width: 120 },
  {
    title: '动作',
    key: 'action',
    width: 140,
    render(row) {
      return h(NTag, { type: 'info', size: 'small' }, { default: () => row.action })
    },
  },
  {
    title: '目标类型',
    key: 'target_type',
    width: 100,
    render(row) {
      return h(NTag, { type: 'warning', size: 'small' }, { default: () => row.target_type })
    },
  },
  { title: '目标对象', key: 'target_name', width: 160, ellipsis: { tooltip: true } },
  { title: '操作详情', key: 'detail', ellipsis: { tooltip: true } },
  { title: 'IP 地址', key: 'ip_address', width: 120 },
  {
    title: '时间',
    key: 'created_at',
    width: 160,
    render: row => row.created_at?.replace('T', ' ').slice(0, 16) || '-',
  },
  {
    title: '操作',
    key: 'actions',
    width: 90,
    fixed: 'right',
    render(row) {
      return h(
        NSpace,
        { size: 8 },
        {
          default: () => [
            h(
              NButton,
              { size: 'small', type: 'primary', ghost: true, onClick: () => handleViewDetail(row) },
              { default: () => '详情' },
            ),
          ],
        },
      )
    },
  },
]

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
    }
    if (searchParams.value.admin_username)
      params.admin_username = searchParams.value.admin_username
    if (searchParams.value.action)
      params.action = searchParams.value.action
    if (searchParams.value.target_type)
      params.target_type = searchParams.value.target_type
    if (searchParams.value.start_date)
      params.start_date = searchParams.value.start_date
    if (searchParams.value.end_date)
      params.end_date = searchParams.value.end_date

    const res = await getAdminLogs(params)
    const data = res.data || res
    logs.value = data.logs || []
    mergeOptionLogs(logs.value)
    pagination.value.total = data.total || 0
  }
  catch (err) {
    console.error('加载操作日志失败:', err)
  }
  finally {
    loading.value = false
  }
}

async function loadFilterOptions() {
  try {
    const res = await getAdminLogs({ page: 1, page_size: 100 })
    const data = res.data || res
    optionLogs.value = data.logs || []
  }
  catch (err) {
    console.error('加载日志筛选选项失败:', err)
  }
}

function mergeOptionLogs(items) {
  const byId = new Map(optionLogs.value.map(log => [log.id, log]))
  items.forEach(log => byId.set(log.id, log))
  optionLogs.value = Array.from(byId.values())
}

function handleSearch() {
  pagination.value.page = 1
  loadData()
}

function handleReset() {
  searchParams.value.admin_username = ''
  searchParams.value.action = ''
  searchParams.value.target_type = ''
  searchParams.value.start_date = null
  searchParams.value.end_date = null
  dateRange.value = null
  pagination.value.page = 1
  loadData()
}

function handleDateChange(dates) {
  if (dates) {
    // 转换为 YYYY-MM-DD
    const start = new Date(dates[0]).toISOString().slice(0, 10)
    const end = new Date(dates[1]).toISOString().slice(0, 10)
    searchParams.value.start_date = start
    searchParams.value.end_date = end
  }
  else {
    searchParams.value.start_date = null
    searchParams.value.end_date = null
  }
  handleSearch()
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

function handleViewDetail(row) {
  currentDetail.value = row
  showDetailModal.value = true
}

async function handleExport() {
  exportLoading.value = true
  try {
    const params = {}
    if (searchParams.value.admin_username)
      params.admin_username = searchParams.value.admin_username
    if (searchParams.value.action)
      params.action = searchParams.value.action
    if (searchParams.value.target_type)
      params.target_type = searchParams.value.target_type
    if (searchParams.value.start_date)
      params.start_date = searchParams.value.start_date
    if (searchParams.value.end_date)
      params.end_date = searchParams.value.end_date

    if (isMock()) {
      // 模拟前端导出
      const res = await getAdminLogs({ ...params, page_size: 1000 })
      const data = res.data?.logs || []
      triggerCsvDownload(data)
      $message.success('已导出 Mock 数据操作日志')
    }
    else {
      const res = await exportAdminLogs(params)
      const blob = res instanceof Blob ? res : res.data
      triggerBlobDownload(blob, `admin_logs_${new Date().toISOString().slice(0, 10)}.csv`)
      $message.success('操作日志已导出')
    }
  }
  catch (err) {
    $message.error(err.message || '导出失败')
  }
  finally {
    exportLoading.value = false
  }
}

function triggerBlobDownload(blob, filename) {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

function triggerCsvDownload(data, filename = 'logs.csv') {
  const headers = ['ID', '操作人', '操作类型', '目标类型', '目标名称', '详情描述', 'IP地址', '操作时间']
  const rows = data.map(l => [
    l.id,
    l.admin_username,
    l.action,
    l.target_type,
    l.target_name,
    l.detail,
    l.ip_address,
    l.created_at,
  ])
  const csvContent = `\uFEFF${[headers.join(','), ...rows.map(e => e.map(val => `"${String(val).replace(/"/g, '""')}"`).join(','))].join('\n')}`
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  loadFilterOptions()
  loadData()
})
</script>
