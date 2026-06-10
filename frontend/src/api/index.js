import { request } from '@/utils'
import { isMock } from '@/mock/data'

export default {
  // 获取用户信息
  getUser: () => request.get('/user/detail'),
  // 刷新token
  refreshToken: () => request.get('/auth/refresh/token'),
  // 登出
  logout: () => {
    if (isMock()) return Promise.resolve({ code: 0 })
    return request.post('/auth/logout', {}, { needTip: false })
  },
  // 切换当前角色
  switchCurrentRole: role => request.post(`/auth/current-role/switch/${role}`),
  // 获取角色权限
  getRolePermissions: () => request.get('/role/permissions/tree'),
  // 验证菜单路径（Mock 模式下直接返回有权限）
  validateMenuPath: (path) => {
    if (isMock()) return Promise.resolve({ code: 0, data: true })
    return request.get(`/permission/menu/validate?path=${path}`)
  },
}
