/**
 * WicMail API 服务层
 * 统一封装 backend-wic 接口调用，支持 Mock 回退
 */
import { isMock, mockApi } from '@/mock/data'
import { request } from '@/utils'

// ---- 认证 ----

export function changePassword(data) {
  return request.post('/api/auth/change-password', data)
}

export function getProfile() {
  if (isMock()) {
    return import('@/store').then(({ useAuthStore }) => {
      const token = useAuthStore().accessToken
      return mockApi.getProfile(token)
    })
  }
  return request.get('/api/auth/profile')
}

export function updateProfile(data) {
  if (isMock()) {
    return import('@/store').then(({ useAuthStore }) => {
      const token = useAuthStore().accessToken
      return mockApi.updateProfile(token, data)
    })
  }
  return request.patch('/api/auth/profile', data)
}

// ---- 邮箱申请 ----

export function applyMailbox(data) {
  if (isMock())
    return mockApi.applyMailbox(data)
  return request.post('/api/mailbox/apply', {
    prefix: data.prefix,
    display_name: data.display_name || null,
    reason: data.reason || null,
  })
}

export function getMyApplications() {
  if (isMock())
    return mockApi.getMyApplications()
  return request.get('/api/mailbox/applications')
}

export function getMyMailboxes() {
  if (isMock())
    return mockApi.getMyMailboxes()
  return request.get('/api/mailbox')
}

// ---- 邮件 ----

export function getEmails(params = {}) {
  if (isMock())
    return mockApi.getEmails(params)
  return request.get('/api/emails', { params })
}

export function getEmailDetail(id) {
  if (isMock())
    return mockApi.getEmailDetail(id)
  return request.get(`/api/emails/${id}`)
}

export function markEmailRead(id) {
  if (isMock())
    return mockApi.markEmailRead(id)
  return request.patch(`/api/emails/${id}/read`)
}

export function markEmailUnread(id) {
  if (isMock())
    return mockApi.markEmailUnread(id)
  return request.patch(`/api/emails/${id}/unread`)
}

export function downloadAttachment(id) {
  if (isMock())
    return mockApi.downloadAttachment(id)
  return request.get(`/api/emails/attachments/${id}/download`)
}

export function getUnreadCount() {
  if (isMock())
    return mockApi.getUnreadCount()
  return request.get('/api/emails/unread-count')
}

// ---- 管理员 ----

export function getAdminApplications(status) {
  if (isMock())
    return mockApi.getAdminApplications(status)
  const params = status ? { status } : {}
  return request.get('/api/admin/applications', { params })
}

export function approveApplication(id, comment) {
  if (isMock())
    return mockApi.approveApplication(id, comment)
  return request.patch(`/api/admin/applications/${id}/approve`, {
    review_comment: comment || null,
  })
}

export function rejectApplication(id, comment) {
  if (isMock())
    return mockApi.rejectApplication(id, comment)
  return request.patch(`/api/admin/applications/${id}/reject`, {
    review_comment: comment || null,
  })
}

export function getAdminUsers(params = {}) {
  if (isMock())
    return mockApi.getAdminUsers(params)
  return request.get('/api/admin/users', { params })
}

export function toggleUserActive(userId) {
  if (isMock())
    return mockApi.toggleUserActive(userId)
  return request.patch(`/api/admin/users/${userId}/toggle-active`)
}

export function deleteUser(userId) {
  if (isMock())
    return mockApi.deleteUser(userId)
  return request.delete(`/api/admin/users/${userId}`)
}

// ---- 管理员 — 邮箱 ----

export function getAdminMailboxes(params = {}) {
  if (isMock())
    return mockApi.getAdminMailboxes(params)
  return request.get('/api/admin/mailboxes', { params })
}

export function getAdminMailboxDetail(id) {
  if (isMock())
    return mockApi.getAdminMailboxDetail(id)
  return request.get(`/api/admin/mailboxes/${id}`)
}

export function createAdminMailbox(data) {
  if (isMock())
    return mockApi.createAdminMailbox(data)
  return request.post('/api/admin/mailboxes', data)
}

export function toggleMailboxActive(id) {
  if (isMock())
    return mockApi.toggleMailboxActive(id)
  return request.patch(`/api/admin/mailboxes/${id}/toggle-active`)
}

export function deleteMailbox(id) {
  if (isMock())
    return mockApi.deleteMailbox(id)
  return request.delete(`/api/admin/mailboxes/${id}`)
}

// ---- 管理员 — 邮件 ----

export function getAdminEmails(params = {}) {
  if (isMock())
    return mockApi.getAdminEmails(params)
  return request.get('/api/admin/emails', { params })
}

export function searchAdminEmails(params = {}) {
  if (isMock())
    return mockApi.searchAdminEmails(params)
  return request.get('/api/admin/emails/search', { params })
}

export function getAdminEmailDetail(id) {
  if (isMock())
    return mockApi.getAdminEmailDetail(id)
  return request.get(`/api/admin/emails/${id}`)
}

export function deleteAdminEmail(id) {
  if (isMock())
    return mockApi.deleteAdminEmail(id)
  return request.delete(`/api/admin/emails/${id}`)
}

export function batchDeleteAdminEmails(ids) {
  if (isMock())
    return mockApi.batchDeleteAdminEmails(ids)
  return request.post('/api/admin/emails/batch-delete', { ids })
}

// ---- 管理员 — 统计 ----

export function getAdminStatsOverview() {
  if (isMock())
    return mockApi.getAdminStatsOverview()
  return request.get('/api/admin/stats/overview')
}

export function getAdminStatsUsers(days = 30) {
  if (isMock())
    return mockApi.getAdminStatsUsers(days)
  return request.get('/api/admin/stats/users', { params: { days } })
}

export function getAdminStatsEmails(days = 30) {
  if (isMock())
    return mockApi.getAdminStatsEmails(days)
  return request.get('/api/admin/stats/emails', { params: { days } })
}

export function getAdminStatsApplications() {
  if (isMock())
    return mockApi.getAdminStatsApplications()
  return request.get('/api/admin/stats/applications')
}

export function getAdminStatsMailboxes(limit = 20) {
  if (isMock())
    return mockApi.getAdminStatsMailboxes(limit)
  return request.get('/api/admin/stats/mailboxes', { params: { limit } })
}

export function getAdminStatsStorage() {
  if (isMock())
    return mockApi.getAdminStatsStorage()
  return request.get('/api/admin/stats/storage')
}

// ---- 管理员 — 日志 ----

export function getAdminLogs(params = {}) {
  if (isMock())
    return mockApi.getAdminLogs(params)
  return request.get('/api/admin/logs', { params })
}

export function exportAdminLogs(params = {}) {
  return request.get('/api/admin/logs/export', {
    params,
    responseType: 'blob',
  })
}

// ---- 管理员 — 配置 ----

export function getAdminConfigs() {
  if (isMock())
    return mockApi.getAdminConfigs()
  return request.get('/api/admin/config')
}

export function updateAdminConfigs(configs) {
  if (isMock())
    return mockApi.updateAdminConfigs(configs)
  return request.patch('/api/admin/config', { configs })
}

export function testCloudflareConnection() {
  if (isMock())
    return mockApi.testCloudflareConnection()
  return request.post('/api/admin/config/test-cloudflare')
}

export function checkDomainDns() {
  if (isMock())
    return mockApi.checkDomainDns()
  return request.get('/api/admin/config/domain-check')
}

// ---- 管理员 — 管理员管理 ----

export function getAdminList() {
  if (isMock())
    return mockApi.getAdminList()
  return request.get('/api/admin/admins')
}

export function addAdmin(username) {
  if (isMock())
    return mockApi.addAdmin(username)
  return request.post('/api/admin/admins', { username })
}

export function removeAdmin(id) {
  if (isMock())
    return mockApi.removeAdmin(id)
  return request.delete(`/api/admin/admins/${id}`)
}

export function updateAdminRole(id, data) {
  if (isMock())
    return mockApi.updateAdminRole(id, data)
  return request.patch(`/api/admin/admins/${id}/role`, data)
}
