<template>
  <div class="auth-page">
    <router-link class="brand auth-brand" to="/">
      <span class="brand-mark"><el-icon><Message /></el-icon></span>
      <span>WicMail</span>
    </router-link>

    <el-card class="auth-card" shadow="never">
      <template #header>
        <div>
          <p class="eyebrow">CREATE ACCOUNT</p>
          <h1>注册账号</h1>
        </div>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="submit">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" size="large" autocomplete="username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" size="large" autocomplete="email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" size="large" type="password" autocomplete="new-password" show-password />
        </el-form-item>
        <el-button class="full-button" size="large" type="primary" :loading="loading" @click="submit">注册并登录</el-button>
      </el-form>

      <p class="auth-switch">已有账号？<router-link to="/login">去登录</router-link></p>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  email: '',
  password: '',
})

const rules = {
  username: [{ required: true, min: 3, message: '用户名至少 3 个字符', trigger: 'blur' }],
  password: [{ required: true, min: 6, message: '密码至少 6 个字符', trigger: 'blur' }],
}

async function submit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.register(form)
    router.push({ name: 'dashboard' })
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>
