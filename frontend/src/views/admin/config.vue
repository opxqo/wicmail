<template>
  <AppPage show-footer>
    <n-card segmented>
      <template #header>
        <span class="flex items-center gap-8"><i class="i-fe:sliders text-18" /> 系统设置</span>
      </template>

      <n-tabs type="line" animated>
        <!-- Tab 1: 系统参数配置 -->
        <n-tab-pane name="params">
          <template #tab>
            <span class="flex items-center gap-4"><i class="i-fe:settings" /> 参数配置</span>
          </template>
          <div v-if="configLoading" class="flex justify-center py-40">
            <n-spin size="large" />
          </div>
          <n-form
            v-else
            :model="configForm"
            label-placement="left"
            label-width="180"
            style="max-width: 650px; margin-top: 16px;"
          >
            <n-form-item label="邮箱主域名" name="mailbox_domain">
              <n-input v-model:value="configForm.mailbox_domain" disabled placeholder="如 wic.edu.kg" />
              <template #feedback>
                邮箱域名由后端解析系统锁定，修改域名需要更换 SSL 与 DNS 证书
              </template>
            </n-form-item>

            <n-form-item label="开启注册邮箱申请" name="application_enabled">
              <n-switch
                v-model:value="configForm.application_enabled"
                checked-value="true"
                unchecked-value="false"
              />
            </n-form-item>

            <n-form-item label="每人最大申请邮箱数" name="max_mailboxes_per_user">
              <n-input-number v-model:value="configForm.max_mailboxes_per_user" :min="1" :max="20" />
            </n-form-item>

            <n-form-item label="最大附件大小限制 (MB)" name="max_attachment_size_mb">
              <n-input-number v-model:value="configForm.max_attachment_size_mb" :min="1" :max="100" />
            </n-form-item>

            <n-form-item label="申请前必须完善资料" name="application_require_profile">
              <n-switch
                v-model:value="configForm.application_require_profile"
                checked-value="true"
                unchecked-value="false"
              />
            </n-form-item>

            <n-form-item>
              <div class="mt-16 flex gap-12">
                <n-button type="primary" :loading="saveLoading" @click="handleSaveConfig">
                  保存配置
                </n-button>
                <n-button ghost @click="loadConfigs">
                  重置
                </n-button>
              </div>
            </n-form-item>
          </n-form>
        </n-tab-pane>

        <n-tab-pane name="diagnostic">
          <template #tab>
            <span class="flex items-center gap-4"><i class="i-fe:activity" /> 系统连通性与 DNS 诊断</span>
          </template>
          <div class="grid grid-cols-1 mt-16 gap-24 md:grid-cols-2">
            <!-- Cloudflare 诊断 -->
            <n-card size="small" segmented>
              <template #header>
                <span class="flex items-center gap-8"><i class="i-fe:cloud text-18" /> Cloudflare 代理连通性测试</span>
              </template>
              <div class="mb-16 text-13 opacity-70">
                测试当前邮件网关后台向 Cloudflare Email Worker API 发送的认证及回调通讯是否成功。
              </div>
              <n-button type="primary" ghost :loading="cfLoading" @click="handleTestCf">
                立即测试连通性
              </n-button>
              <div v-if="cfResult" class="mt-16">
                <n-alert :type="cfResult.status === 'ok' ? 'success' : 'error'" class="mb-12">
                  {{ cfResult.message }}
                </n-alert>
                <pre class="max-h-200 overflow-auto border rounded-8 bg-gray-50/50 p-12 text-12 font-mono">{{ JSON.stringify(cfResult.data || cfResult, null, 2) }}</pre>
              </div>
            </n-card>

            <!-- DNS 诊断 -->
            <n-card size="small" segmented>
              <template #header>
                <span class="flex items-center gap-8"><i class="i-fe:globe text-18" /> wic.edu.kg 域名 DNS 检查</span>
              </template>
              <div class="mb-16 text-13 opacity-70">
                向本地域名解析服务器查询 WicMail MX 路由指向以及服务器的公网 IP 映射，检验 DNS 生效情况。
              </div>
              <n-button type="info" ghost :loading="dnsLoading" @click="handleTestDns">
                开始域名 DNS 解析检测
              </n-button>
              <div v-if="dnsResult" class="mt-16">
                <n-descriptions bordered label-placement="left" :column="1" size="small">
                  <n-descriptions-item label="诊断域名">
                    <span class="font-bold">{{ dnsResult.domain }}</span>
                  </n-descriptions-item>
                  <n-descriptions-item label="MX 邮件路由记录">
                    <div v-if="Array.isArray(dnsResult.checks?.mx) && dnsResult.checks.mx.length">
                      <div v-for="mx in dnsResult.checks.mx" :key="mx" class="flex items-center gap-8 py-2">
                        <i class="text-success i-fe:check-circle" /> {{ mx }}
                      </div>
                    </div>
                    <span v-else class="text-error">{{ dnsResult.checks?.mx || '未检测到有效 MX 解析' }}</span>
                  </n-descriptions-item>
                  <n-descriptions-item label="A 地址解析记录">
                    <div v-if="Array.isArray(dnsResult.checks?.a) && dnsResult.checks.a.length">
                      <div v-for="a in dnsResult.checks.a" :key="a" class="flex items-center gap-8 py-2">
                        <i class="text-success i-fe:check-circle" /> {{ a }}
                      </div>
                    </div>
                    <span v-else class="text-error">{{ dnsResult.checks?.a || '未检测到 A 记录' }}</span>
                  </n-descriptions-item>
                  <n-descriptions-item label="最新公网解析 IP">
                    <n-tag type="success" size="small">
                      {{ dnsResult.checks?.resolved_ip || '未知' }}
                    </n-tag>
                  </n-descriptions-item>
                </n-descriptions>
              </div>
            </n-card>
          </div>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </AppPage>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  checkDomainDns,
  getAdminConfigs,
  testCloudflareConnection,
  updateAdminConfigs,
} from '@/api/wicmail'
import { AppPage } from '@/components'

const configLoading = ref(false)
const saveLoading = ref(false)
const cfLoading = ref(false)
const dnsLoading = ref(false)

const configForm = ref({
  mailbox_domain: '',
  application_enabled: 'true',
  max_mailboxes_per_user: 3,
  max_attachment_size_mb: 10,
  application_require_profile: 'true',
})

const cfResult = ref(null)
const dnsResult = ref(null)

async function loadConfigs() {
  configLoading.value = true
  try {
    const res = await getAdminConfigs()
    const data = res.data || res
    if (Array.isArray(data)) {
      const form = {}
      data.forEach((item) => {
        if (item.key === 'max_mailboxes_per_user' || item.key === 'max_attachment_size_mb') {
          form[item.key] = Number(item.value)
        }
        else {
          form[item.key] = item.value
        }
      })
      configForm.value = { ...configForm.value, ...form }
    }
  }
  catch (err) {
    console.error('加载系统配置失败:', err)
  }
  finally {
    configLoading.value = false
  }
}

async function handleSaveConfig() {
  saveLoading.value = true
  try {
    const payload = {}
    Object.keys(configForm.value).forEach((key) => {
      payload[key] = String(configForm.value[key])
    })
    const res = await updateAdminConfigs(payload)
    const data = res.data || res
    $message.success(`保存成功（更新了 ${data.updated?.length || 0} 项配置）`)
    await loadConfigs()
  }
  catch (err) {
    $message.error(err.message || '保存失败')
  }
  finally {
    saveLoading.value = false
  }
}

async function handleTestCf() {
  cfLoading.value = true
  cfResult.value = null
  try {
    const res = await testCloudflareConnection()
    cfResult.value = res.data || res
  }
  catch (err) {
    cfResult.value = {
      status: 'error',
      message: err.message || '测试失败',
    }
  }
  finally {
    cfLoading.value = false
  }
}

async function handleTestDns() {
  dnsLoading.value = true
  dnsResult.value = null
  try {
    const res = await checkDomainDns()
    dnsResult.value = res.data || res
  }
  catch (err) {
    $message.error(err.message || '检查 DNS 失败')
  }
  finally {
    dnsLoading.value = false
  }
}

onMounted(() => loadConfigs())
</script>
