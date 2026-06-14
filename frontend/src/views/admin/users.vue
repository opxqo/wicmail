<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:users text-18" /> 用户管理</span>
      </template>
      <n-data-table :columns="columns" :data="users" :loading="loading" />
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
  </AppPage>
</template>

<script setup>
import { NButton, NPopconfirm, NSpace, NTag } from 'naive-ui'
import { h, onMounted, ref } from 'vue'
import { deleteUser, getAdminUsers, toggleUserActive } from '@/api/wicmail'
import { AppPage } from '@/components'

const loading = ref(false)
const users = ref([])

const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0,
})

const columns = [
  { title: 'ID', key: 'id', width: 60 },
  { title: '用户名', key: 'username', width: 150 },
  { title: '邮箱', key: 'email', render: row => row.email || '-', ellipsis: { tooltip: true } },
  {
    title: '角色',
    key: 'is_admin',
    width: 100,
    render(row) {
      return h(NTag, { type: row.is_admin ? 'warning' : 'default', size: 'small', round: true }, { default: () => row.is_admin ? '管理员' : '用户' })
    },
  },
  {
    title: '状态',
    key: 'is_active',
    width: 100,
    render(row) {
      return h(NTag, { type: row.is_active ? 'success' : 'error', size: 'small', round: true }, { default: () => row.is_active ? '正常' : '已禁用' })
    },
  },
  {
    title: '注册时间',
    key: 'created_at',
    width: 160,
    render: row => row.created_at?.replace('T', ' ').slice(0, 16) || '-',
  },
  {
    title: '操作',
    key: 'actions',
    width: 180,
    fixed: 'right',
    render(row) {
      return h(NSpace, { size: 8 }, {
        default: () => [
          h(NPopconfirm, { onPositiveClick: () => toggleActive(row) }, {
            trigger: () => h(NButton, { size: 'small', type: row.is_active ? 'error' : 'success', ghost: true, disabled: row.is_admin }, { default: () => row.is_active ? '禁用' : '启用' }),
            default: () => `确认${row.is_active ? '禁用' : '启用'}用户 ${row.username}？`,
          }),
          h(NPopconfirm, { onPositiveClick: () => removeUser(row) }, {
            trigger: () => h(NButton, { size: 'small', type: 'error', ghost: true, disabled: row.is_admin }, { default: () => '删除' }),
            default: () => `确认删除用户 ${row.username}？此操作不可撤销。`,
          }),
        ],
      })
    },
  },
]

async function toggleActive(row) {
  try {
    const res = await toggleUserActive(row.id)
    const data = res.data || res
    row.is_active = data.is_active ?? !row.is_active
    $message.success(data.message || '操作成功')
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

async function removeUser(row) {
  try {
    const res = await deleteUser(row.id)
    const data = res.data || res
    $message.success(data.message || '删除成功')
    await loadUsers()
  }
  catch (err) {
    $message.error(err.message || '删除失败')
  }
}

async function loadUsers() {
  loading.value = true
  try {
    const res = await getAdminUsers({
      page: pagination.value.page,
      page_size: pagination.value.pageSize,
    })
    const data = res.data || res
    users.value = Array.isArray(data) ? data : (data.users || [])
    pagination.value.total = Array.isArray(data) ? data.length : (data.total || 0)
  }
  catch (err) {
    console.error('加载用户列表失败:', err)
  }
  finally {
    loading.value = false
  }
}

function handlePageChange(page) {
  pagination.value.page = page
  loadUsers()
}

function handlePageSizeChange(pageSize) {
  pagination.value.pageSize = pageSize
  pagination.value.page = 1
  loadUsers()
}

onMounted(() => loadUsers())
</script>
