import { isMock, mockApi } from '@/mock/data'
import { request } from '@/utils'

export default {
  toggleRole: data => request.post('/auth/role/toggle', data),
  login: async (data) => {
    if (isMock())
      return mockApi.login(data)
    const res = await request.post('/api/auth/login', data, { needToken: false })
    // 后端返回 {access_token, token_type}，转换为前端期望的 {accessToken}
    const tokenData = res.data || res
    return {
      code: 200,
      data: {
        accessToken: tokenData.access_token,
      },
    }
  },
  register: async (data) => {
    if (isMock())
      return mockApi.register(data)
    const res = await request.post('/api/auth/register', data, { needToken: false })
    return { code: 200, data: res.data || res }
  },
  getUser: async () => {
    if (isMock()) {
      const { useAuthStore } = await import('@/store')
      const token = useAuthStore().accessToken
      return mockApi.getUserDetail(token)
    }
    const res = await request.get('/api/auth/profile')
    const profile = res.data || res
    // 转换为前端期望的用户信息格式
    return {
      code: 200,
      data: {
        id: profile.id,
        username: profile.username,
        profile: {
          avatar: null,
          nickName: profile.real_name || profile.username,
          email: profile.email,
        },
        roles: profile.is_admin
          ? [{ code: 'admin', name: '管理员' }]
          : [{ code: 'user', name: '普通用户' }],
        currentRole: profile.is_admin
          ? { code: 'admin', name: '管理员' }
          : { code: 'user', name: '普通用户' },
      },
    }
  },
}
