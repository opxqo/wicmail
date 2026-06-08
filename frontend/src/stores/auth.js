import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { ElMessage } from 'element-plus'
import { api } from '@/services/http'

const TOKEN_KEY = 'wicmail_token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const user = ref(null)
  const initialized = ref(false)

  const isAuthenticated = computed(() => Boolean(token.value && user.value))
  const isAdmin = computed(() => Boolean(user.value?.is_admin))

  function setToken(nextToken) {
    token.value = nextToken
    if (nextToken) {
      localStorage.setItem(TOKEN_KEY, nextToken)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
  }

  async function login(payload) {
    const data = await api.login(payload)
    setToken(data.access_token)
    await fetchMe()
    ElMessage.success('登录成功')
  }

  async function register(payload) {
    await api.register(payload)
    await login({ username: payload.username, password: payload.password })
  }

  async function fetchMe() {
    try {
      user.value = await api.me()
    } catch (error) {
      setToken('')
      user.value = null
    } finally {
      initialized.value = true
    }
  }

  function logout() {
    setToken('')
    user.value = null
  }

  return {
    token,
    user,
    initialized,
    isAuthenticated,
    isAdmin,
    login,
    register,
    fetchMe,
    logout,
  }
})
