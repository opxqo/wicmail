<template>
  <div class="page-stack">
    <div class="split-grid">
      <el-card class="panel-card" shadow="never">
        <template #header>
          <span>提交邮箱申请</span>
        </template>
        <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
          <el-form-item label="邮箱前缀" prop="prefix">
            <el-input v-model="form.prefix" size="large">
              <template #append>@wic.edu.kg</template>
            </el-input>
          </el-form-item>
          <el-form-item label="展示名称">
            <el-input v-model="form.display_name" size="large" />
          </el-form-item>
          <el-form-item label="用途说明">
            <el-input v-model="form.reason" type="textarea" :rows="4" />
          </el-form-item>
          <el-button type="primary" size="large" :loading="submitting" @click="submit">提交申请</el-button>
        </el-form>
      </el-card>

      <el-card class="panel-card" shadow="never">
        <template #header>
          <span>已开通邮箱</span>
        </template>
        <el-empty v-if="mailboxes.length === 0" description="暂无邮箱" />
        <div v-else class="mailbox-list">
          <article v-for="mailbox in mailboxes" :key="mailbox.id" class="mailbox-row">
            <div>
              <strong>{{ mailbox.address }}</strong>
              <p>{{ mailbox.display_name || '校园邮箱' }}</p>
            </div>
            <el-tag type="success">已开通</el-tag>
          </article>
        </div>
      </el-card>
    </div>

    <el-card class="panel-card" shadow="never">
      <template #header>
        <span>申请记录</span>
      </template>
      <el-table :data="applications" class="data-table">
        <el-table-column prop="requested_address" label="邮箱地址" min-width="220" />
        <el-table-column prop="display_name" label="展示名称" min-width="140" />
        <el-table-column prop="reason" label="用途说明" min-width="180" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusMap[row.status]?.type">{{ statusMap[row.status]?.text || row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="review_comment" label="审核备注" min-width="160" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '@/services/http'

const formRef = ref()
const submitting = ref(false)
const applications = ref([])
const mailboxes = ref([])

const form = reactive({
  prefix: '',
  display_name: '',
  reason: '',
})

const rules = {
  prefix: [
    { required: true, message: '请输入邮箱前缀', trigger: 'blur' },
    { min: 3, max: 30, message: '长度需为 3-30 个字符', trigger: 'blur' },
  ],
}

const statusMap = {
  pending: { text: '审核中', type: 'warning' },
  approved: { text: '已通过', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' },
}

async function loadData() {
  const [appData, mailboxData] = await Promise.all([
    api.listApplications(),
    api.listMailboxes(),
  ])
  applications.value = appData.applications
  mailboxes.value = mailboxData
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await api.applyMailbox(form)
    ElMessage.success('申请已提交')
    Object.assign(form, { prefix: '', display_name: '', reason: '' })
    await loadData()
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>
