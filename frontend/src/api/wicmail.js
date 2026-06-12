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

export function getAdminUsers() {
  if (isMock())
    return mockApi.getAdminUsers()
  return request.get('/api/admin/users')
}

export function toggleUserActive(userId) {
  if (isMock())
    return mockApi.toggleUserActive(userId)
  return request.patch(`/api/admin/users/${userId}/toggle-active`)
}

export function deleteUser(userId) {
  return request.delete(`/api/admin/users/${userId}`)
}
