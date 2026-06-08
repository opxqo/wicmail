import axios from 'axios'
import { ElMessage } from 'element-plus'
import { mockApi } from './mock'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || ''
const useMock = import.meta.env.VITE_USE_MOCK !== 'false' || !apiBaseUrl

const client = axios.create({
  baseURL: apiBaseUrl,
  timeout: 15000,
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('wicmail_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(typeof message === 'string' ? message : '请求失败')
    return Promise.reject(error)
  },
)

const realApi = {
  login: (payload) => client.post('/api/auth/login', payload),
  register: (payload) => client.post('/api/auth/register', payload),
  me: () => client.get('/api/auth/me'),
  listEmails: (params) => client.get('/api/emails', { params }),
  getEmail: (id) => client.get(`/api/emails/${id}`),
  markRead: (id) => client.patch(`/api/emails/${id}/read`),
  markUnread: (id) => client.patch(`/api/emails/${id}/unread`),
  applyMailbox: (payload) => client.post('/api/mailbox/apply', payload),
  listApplications: () => client.get('/api/mailbox/applications'),
  listMailboxes: () => client.get('/api/mailbox'),
  adminListApplications: (status) => client.get('/api/admin/applications', { params: { status } }),
  approveApplication: (id, payload) => client.patch(`/api/admin/applications/${id}/approve`, payload),
  rejectApplication: (id, payload) => client.patch(`/api/admin/applications/${id}/reject`, payload),
  adminListUsers: () => client.get('/api/admin/users'),
  toggleUserActive: (id) => client.patch(`/api/admin/users/${id}/toggle-active`),
}

export const api = useMock ? mockApi : realApi
export const apiMode = useMock ? 'mock' : 'real'
