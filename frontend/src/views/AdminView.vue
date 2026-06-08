<template>
  <div class="page-stack">
    <el-tabs v-model="activeTab" class="admin-tabs">
      <el-tab-pane label="申请审核" name="applications">
        <el-card class="panel-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>申请队列</span>
              <el-segmented v-model="status" :options="statusOptions" @change="loadApplications" />
            </div>
          </template>
          <el-table :data="applications" class="data-table">
            <el-table-column prop="username" label="用户" width="130" />
            <el-table-column prop="requested_address" label="申请邮箱" min-width="220" />
            <el-table-column prop="reason" label="用途说明" min-width="180" />
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="statusMap[row.status]?.type">{{ statusMap[row.status]?.text || row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="190" fixed="right">
              <template #default="{ row }">
                <el-button v-if="row.status === 'pending'" size="small" type="primary" @click="approve(row)">批准</el-button>
                <el-button v-if="row.status === 'pending'" size="small" type="danger" plain @click="reject(row)">拒绝</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="用户管理" name="users">
        <el-card class="panel-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>用户列表</span>
              <el-button :icon="Refresh" @click="loadUsers">刷新</el-button>
            </div>
          </template>
          <el-table :data="users" class="data-table">
            <el-table-column prop="username" label="用户名" min-width="160" />
            <el-table-column prop="email" label="邮箱" min-width="220" />
            <el-table-column label="角色" width="110">
              <template #default="{ row }">
                <el-tag :type="row.is_admin ? 'danger' : 'info'">{{ row.is_admin ? '管理员' : '用户' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button size="small" :disabled="row.is_admin" @click="toggleUser(row)">
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { api } from '@/services/http'

const activeTab = ref('applications')
const status = ref('')
const applications = ref([])
const users = ref([])

const statusOptions = [
  { label: '全部', value: '' },
  { label: '待审核', value: 'pending' },
  { label: '已通过', value: 'approved' },
  { label: '已拒绝', value: 'rejected' },
]

const statusMap = {
  pending: { text: '待审核', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' },
}

async function loadApplications() {
  applications.value = await api.adminListApplications(status.value)
}

async function loadUsers() {
  users.value = await api.adminListUsers()
}

async function approve(row) {
  await api.approveApplication(row.id, { comment: '审核通过' })
  await loadApplications()
}

async function reject(row) {
  await ElMessageBox.confirm(`确认拒绝 ${row.requested_address}？`, '拒绝申请', {
    type: 'warning',
  })
  await api.rejectApplication(row.id, { comment: '材料未通过审核' })
  await loadApplications()
}

async function toggleUser(row) {
  await api.toggleUserActive(row.id)
  await loadUsers()
}

onMounted(async () => {
  await Promise.all([loadApplications(), loadUsers()])
})
</script>
