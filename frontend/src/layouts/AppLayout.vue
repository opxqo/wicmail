<template>
  <div class="app-shell">
    <aside class="sidebar">
      <router-link class="app-brand" to="/app">
        <span class="brand-mark">
          <el-icon><Message /></el-icon>
        </span>
        <span>WicMail</span>
      </router-link>

      <nav class="side-nav">
        <router-link to="/app">
          <el-icon><DataBoard /></el-icon>
          <span>工作台</span>
        </router-link>
        <router-link to="/app/mailboxes">
          <el-icon><Postcard /></el-icon>
          <span>邮箱申请</span>
        </router-link>
        <router-link to="/app/emails">
          <el-icon><Tickets /></el-icon>
          <span>邮件中心</span>
        </router-link>
        <router-link v-if="auth.isAdmin" to="/app/admin">
          <el-icon><Operation /></el-icon>
          <span>管理审核</span>
        </router-link>
      </nav>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div>
          <p class="eyebrow">WicMail Console</p>
          <h1>{{ routeTitle }}</h1>
        </div>
        <div class="topbar-actions">
          <el-tag :type="apiMode === 'mock' ? 'warning' : 'success'" effect="plain">
            {{ apiMode === 'mock' ? 'Mock 数据' : '云端 API' }}
          </el-tag>
          <el-dropdown>
            <button class="user-menu" type="button">
              <el-avatar :size="32">{{ auth.user?.username?.slice(0, 1).toUpperCase() }}</el-avatar>
              <span>{{ auth.user?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { apiMode } from '@/services/http'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const titles = {
  dashboard: '工作台',
  mailboxes: '邮箱申请',
  emails: '邮件中心',
  admin: '管理审核',
}

const routeTitle = computed(() => titles[route.name] || '工作台')

function logout() {
  auth.logout()
  router.push({ name: 'landing' })
}
</script>
