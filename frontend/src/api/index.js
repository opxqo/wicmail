import { request } from '@/utils'

export default {
  // 获取用户信息
  getUser: () => request.get('/api/auth/profile'),
  // 登出
  logout: () => {
    return Promise.resolve({ code: 200 })
  },
  // 验证菜单路径（始终返回有权限，菜单由 basePermissions 静态配置）
  validateMenuPath: () => Promise.resolve({ code: 200, data: true }),
}
