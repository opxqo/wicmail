<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:users text-18" /> 用户管理</span>
      </template>
      <n-data-table :columns="columns" :data="users" :loading="loading" />
    </n-card>
  </AppPage>
</template>

<script setup>
import { h, ref, onMounted } from 'vue'
import { NTag, NButton, NPopconfirm } from 'naive-ui'
import { AppPage } from '@/components'
import { mockApi, isMock } from '@/mock/data'

const loading = ref(false)
const users = ref([])

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
    width: 120,
    fixed: 'right',
    render(row) {
      return h(NPopconfirm, { onPositiveClick: () => toggleActive(row) }, {
        trigger: () => h(NButton, { size: 'small', type: row.is_active ? 'error' : 'success', ghost: true }, { default: () => row.is_active ? '禁用' : '启用' }),
        default: () => `确认${row.is_active ? '禁用' : '启用'}用户 ${row.username}？`,
      })
    },
  },
]

async function toggleActive(row) {
  if (!isMock()) return
  try {
    const res = await mockApi.toggleUserActive(row.id)
    row.is_active = res.data.is_active
    $message.success(res.data.message)
  }
  catch (err) {
    $message.error(err.message || '操作失败')
  }
}

async function loadUsers() {
  loading.value = true
  try {
    if (isMock()) {
      const res = await mockApi.getAdminUsers()
      users.value = res.data
    }
  }
  finally {
    loading.value = false
  }
}

onMounted(() => loadUsers())
</script>
