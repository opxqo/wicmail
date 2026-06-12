<template>
  <AppPage show-footer>
    <div class="grid grid-cols-1 mb-16 gap-16 md:grid-cols-4">
      <!-- 总览数据卡片 -->
      <n-card class="stats-card border-teal-500/20 from-teal-500/10 to-transparent bg-gradient-to-br" size="small" segmented>
        <template #header>
          <div class="flex items-center justify-between opacity-80">
            <span>用户总数</span>
            <i class="i-fe:users text-18 text-teal-600" />
          </div>
        </template>
        <div class="mt-8 flex items-baseline justify-between">
          <span class="text-32 font-bold">{{ overview.total_users ?? 0 }}</span>
          <span class="text-12 text-teal-600 font-medium">今日 +{{ overview.today_new_users ?? 0 }}</span>
        </div>
        <div class="mt-8 text-12 opacity-50">
          活跃用户：{{ overview.active_users ?? 0 }}
        </div>
      </n-card>

      <n-card class="stats-card border-indigo-500/20 from-indigo-500/10 to-transparent bg-gradient-to-br" size="small" segmented>
        <template #header>
          <div class="flex items-center justify-between opacity-80">
            <span>已启用邮箱</span>
            <i class="i-fe:mail text-18 text-indigo-600" />
          </div>
        </template>
        <div class="mt-8 flex items-baseline justify-between">
          <span class="text-32 font-bold">{{ overview.active_mailboxes ?? 0 }}</span>
          <span class="text-12 text-indigo-600 font-medium">总邮箱 {{ overview.total_mailboxes ?? 0 }}</span>
        </div>
        <div class="mt-8 text-12 opacity-50">
          启用率：{{ getPercentage(overview.active_mailboxes, overview.total_mailboxes) }}%
        </div>
      </n-card>

      <n-card class="stats-card border-sky-500/20 from-sky-500/10 to-transparent bg-gradient-to-br" size="small" segmented>
        <template #header>
          <div class="flex items-center justify-between opacity-80">
            <span>邮件总量</span>
            <i class="i-fe:inbox text-18 text-sky-600" />
          </div>
        </template>
        <div class="mt-8 flex items-baseline justify-between">
          <span class="text-32 font-bold">{{ overview.total_emails ?? 0 }}</span>
          <span class="text-12 text-sky-600 font-medium">今日 +{{ overview.today_new_emails ?? 0 }}</span>
        </div>
        <div class="mt-8 text-12 opacity-50">
          未读邮件：{{ overview.unread_emails ?? 0 }} 封
        </div>
      </n-card>

      <n-card class="stats-card border-amber-500/20 from-amber-500/10 to-transparent bg-gradient-to-br" size="small" segmented>
        <template #header>
          <div class="flex items-center justify-between opacity-80">
            <span>邮箱申请</span>
            <i class="i-fe:check-square text-18 text-amber-600" />
          </div>
        </template>
        <div class="mt-8 flex items-baseline justify-between">
          <span class="text-32 font-bold">{{ overview.total_applications ?? 0 }}</span>
          <span class="text-12 text-amber-600 font-medium">待审核 {{ overview.pending_applications ?? 0 }}</span>
        </div>
        <div class="mt-8 text-12 opacity-50">
          申请总数：{{ overview.total_applications ?? 0 }} 次
        </div>
      </n-card>
    </div>

    <!-- 存储使用情况与申请分布 -->
    <div class="grid grid-cols-1 mb-16 gap-16 md:grid-cols-3">
      <n-card size="small" segmented class="md:col-span-2">
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:database text-18" /> 存储与附件统计</span>
        </template>
        <div class="flex flex-col items-center gap-24 py-16 md:flex-row">
          <div class="w-full flex-1">
            <div class="mb-8 flex items-center justify-between">
              <span class="text-14 font-medium opacity-80">存储池总占用量</span>
              <span class="text-16 text-primary font-bold">{{ storage.total_size_mb ?? '0.00' }} MB</span>
            </div>
            <!-- 精美存储进度条 -->
            <n-progress
              type="line"
              status="success"
              :percentage="Math.min(100, Number(((storage.total_size_mb ?? 0) / 100).toFixed(1)))"
              processing
            />
            <div class="mt-8 flex justify-between text-12 opacity-40">
              <span>已用容量</span>
              <span>配额上限 100 MB</span>
            </div>
          </div>
          <n-divider vertical class="hidden md:block h-80!" />
          <div class="grid grid-cols-2 w-full flex-shrink-0 gap-16 md:w-200">
            <div>
              <div class="text-12 opacity-50">
                附件总数
              </div>
              <div class="mt-4 text-18 font-bold">
                {{ storage.total_attachments ?? 0 }} 个
              </div>
            </div>
            <div>
              <div class="text-12 opacity-50">
                平均邮件大小
              </div>
              <div class="mt-4 text-18 font-bold">
                {{ formatBytes(storage.avg_email_size_bytes) }}
              </div>
            </div>
          </div>
        </div>
      </n-card>

      <n-card size="small" segmented>
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:pie-chart text-18" /> 申请审核分布</span>
        </template>
        <div class="h-140">
          <VChart :option="pieOption" autoresize />
        </div>
      </n-card>
    </div>

    <!-- 图表趋势区 -->
    <div class="grid grid-cols-1 mb-16 gap-16 md:grid-cols-2">
      <n-card size="small" segmented>
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:trending-up text-18" /> 用户注册趋势 (近30天)</span>
        </template>
        <div class="h-280">
          <VChart :option="userTrendOption" autoresize />
        </div>
      </n-card>
      <n-card size="small" segmented>
        <template #header>
          <span class="flex items-center gap-8"><i class="i-fe:activity text-18" /> 邮件接收趋势 (近30天)</span>
        </template>
        <div class="h-280">
          <VChart :option="emailTrendOption" autoresize />
        </div>
      </n-card>
    </div>

    <!-- 邮箱使用量排行 Top 20 -->
    <n-card size="small" segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:award text-18" /> 邮箱收信量排行榜 (Top 20)</span>
      </template>
      <div class="overflow-x-auto">
        <n-list hoverable clickable>
          <n-list-item v-for="(item, index) in mailboxRank" :key="item.id">
            <div class="flex items-center gap-16 py-4">
              <!-- 排名色块 -->
              <div
                class="h-24 w-24 flex flex-shrink-0 items-center justify-center rounded-full text-12 font-bold"
                :class="[
                  index === 0 ? 'bg-amber-500 text-white' : '',
                  index === 1 ? 'bg-slate-400 text-white' : '',
                  index === 2 ? 'bg-amber-700 text-white' : '',
                  index > 2 ? 'bg-gray-100 text-gray-600' : '',
                ]"
              >
                {{ index + 1 }}
              </div>
              <div class="min-w-0 flex-1">
                <span class="block truncate text-14 font-medium">{{ item.address }}</span>
              </div>
              <div class="flex flex-shrink-0 items-center gap-12">
                <n-tag size="small" :type="item.unread_count > 0 ? 'warning' : 'default'">
                  未读 {{ item.unread_count }}
                </n-tag>
                <div class="w-120 text-right">
                  <span class="text-14 text-primary font-bold">{{ item.email_count }}</span>
                  <span class="ml-4 text-12 opacity-50">封邮件</span>
                </div>
              </div>
            </div>
          </n-list-item>
        </n-list>
      </div>
    </n-card>
  </AppPage>
</template>

<script setup>
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { GridComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { onMounted, ref } from 'vue'
import VChart from 'vue-echarts'
import {
  getAdminStatsApplications,
  getAdminStatsEmails,
  getAdminStatsMailboxes,
  getAdminStatsOverview,
  getAdminStatsStorage,
  getAdminStatsUsers,
} from '@/api/wicmail'
import { AppPage } from '@/components'

// 注册 ECharts 模块
echarts.use([
  TooltipComponent,
  GridComponent,
  LegendComponent,
  BarChart,
  LineChart,
  CanvasRenderer,
  UniversalTransition,
  PieChart,
])

const overview = ref({})
const storage = ref({})
const mailboxRank = ref([])

// 图表配置 options
const pieOption = ref({})
const userTrendOption = ref({})
const emailTrendOption = ref({})

function getPercentage(num, total) {
  if (!total)
    return 0
  return Math.round((num / total) * 100)
}

function formatBytes(bytes) {
  if (!bytes)
    return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${Number((bytes / k ** i).toFixed(1))} ${sizes[i]}`
}

async function loadStats() {
  try {
    const [resOver, resStore, resApps, resUsers, resEmails, resRank] = await Promise.all([
      getAdminStatsOverview(),
      getAdminStatsStorage(),
      getAdminStatsApplications(),
      getAdminStatsUsers(30),
      getAdminStatsEmails(30),
      getAdminStatsMailboxes(20),
    ])

    overview.value = resOver.data || resOver
    storage.value = resStore.data || resStore
    mailboxRank.value = resRank.data || resRank

    // 1. 申请分布饼图
    const appData = resApps.data || resApps
    const appStatusMap = {
      pending: '待审核',
      approved: '已批准',
      rejected: '已拒绝',
    }
    const appColors = {
      pending: '#f59e0b',
      approved: '#10b981',
      rejected: '#ef4444',
    }
    pieOption.value = {
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [
        {
          type: 'pie',
          radius: '75%',
          center: ['65%', '50%'],
          data: appData.map(item => ({
            value: item.count,
            name: appStatusMap[item.status] || item.status,
            itemStyle: { color: appColors[item.status] || '#999' },
          })),
          label: { show: false },
        },
      ],
    }

    // 2. 用户注册折线图
    const userData = resUsers.data || resUsers
    userTrendOption.value = {
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: userData.map(d => d.date.slice(5)), // 截取 MM-DD
      },
      yAxis: { type: 'value' },
      series: [
        {
          name: '新注册用户',
          type: 'line',
          smooth: true,
          data: userData.map(d => d.count),
          itemStyle: { color: '#0ea5e9' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(14, 165, 233, 0.3)' },
              { offset: 1, color: 'rgba(14, 165, 233, 0.01)' },
            ]),
          },
        },
      ],
    }

    // 3. 邮件接收柱状图
    const emailData = resEmails.data || resEmails
    emailTrendOption.value = {
      tooltip: { trigger: 'axis' },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: {
        type: 'category',
        data: emailData.map(d => d.date.slice(5)),
      },
      yAxis: { type: 'value' },
      series: [
        {
          name: '收信量',
          type: 'bar',
          data: emailData.map(d => d.count),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#10b981' },
              { offset: 1, color: '#6ee7b7' },
            ]),
            borderRadius: [4, 4, 0, 0],
          },
        },
      ],
    }
  }
  catch (err) {
    console.error('获取统计数据失败:', err)
  }
}

onMounted(() => loadStats())
</script>

<style scoped>
.stats-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
</style>
