import { request } from '@/utils'
import { mockApi, isMock } from '@/mock/data'

export default {
  toggleRole: data => request.post('/auth/role/toggle', data),
  login: (data) => {
    if (isMock()) return mockApi.login(data)
    return request.post('/auth/login', data, { needToken: false })
  },
  getUser: () => request.get('/user/detail'),
}
