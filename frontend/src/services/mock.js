const delay = (value) => new Promise((resolve) => setTimeout(() => resolve(value), 240))

const users = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@wic.edu.kg',
    password: 'admin123456',
    is_active: true,
    is_admin: true,
    created_at: '2026-06-08T10:00:00Z',
  },
  {
    id: 2,
    username: 'student',
    email: 'student@wic.edu.kg',
    password: 'student123',
    is_active: true,
    is_admin: false,
    created_at: '2026-06-08T11:00:00Z',
  },
]

let currentUserId = Number(localStorage.getItem('wicmail_mock_user_id') || 2)

let applications = [
  {
    id: 101,
    user_id: 2,
    username: 'student',
    requested_address: 'student@wic.edu.kg',
    display_name: '学生邮箱',
    status: 'approved',
    reason: '课程通知与学术服务',
    review_comment: '材料完整',
    reviewed_at: '2026-06-08T14:00:00Z',
    created_at: '2026-06-08T12:00:00Z',
    mailbox_id: 201,
  },
  {
    id: 102,
    user_id: 2,
    username: 'student',
    requested_address: 'club@wic.edu.kg',
    display_name: '社团邮箱',
    status: 'pending',
    reason: '社团活动通知',
    review_comment: null,
    reviewed_at: null,
    created_at: '2026-06-09T09:10:00Z',
    mailbox_id: null,
  },
]

let mailboxes = [
  {
    id: 201,
    address: 'student@wic.edu.kg',
    display_name: '学生邮箱',
    is_active: true,
    created_at: '2026-06-08T14:00:00Z',
  },
]

let emails = [
  {
    id: 301,
    mailbox_id: 201,
    mailbox_address: 'student@wic.edu.kg',
    subject: '欢迎使用 WicMail',
    header_from: 'WicMail Team <noreply@wic.edu.kg>',
    header_to: 'student@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'noreply@wic.edu.kg',
    envelope_to: 'student@wic.edu.kg',
    message_id: '<welcome-301@wic.edu.kg>',
    sent_at: '2026-06-08T14:12:00Z',
    received_at: '2026-06-08T14:12:09Z',
    raw_size: 2480,
    body_text: '你的 WicMail 邮箱已经开通，可以在用户中心查看邮件与邮箱状态。',
    body_html: '<p>你的 <strong>WicMail</strong> 邮箱已经开通。</p>',
    parse_status: 'parsed',
    is_read: false,
    attachment_count: 0,
    attachments: [],
  },
  {
    id: 302,
    mailbox_id: 201,
    mailbox_address: 'student@wic.edu.kg',
    subject: '校园账号绑定提醒',
    header_from: 'Account Center <account@wic.edu.kg>',
    header_to: 'student@wic.edu.kg',
    header_cc: null,
    header_reply_to: null,
    envelope_from: 'account@wic.edu.kg',
    envelope_to: 'student@wic.edu.kg',
    message_id: '<account-302@wic.edu.kg>',
    sent_at: '2026-06-08T15:30:00Z',
    received_at: '2026-06-08T15:30:05Z',
    raw_size: 3892,
    body_text: '请确认学号、实名信息与邮箱账号完成绑定。',
    body_html: '<p>请确认学号、实名信息与邮箱账号完成绑定。</p>',
    parse_status: 'parsed',
    is_read: true,
    attachment_count: 1,
    attachments: [{ id: 1, filename: 'guide.pdf', content_type: 'application/pdf', size: 120404 }],
  },
]

function publicUser(user) {
  const { password, ...safeUser } = user
  return safeUser
}

function currentUser() {
  return users.find((user) => user.id === currentUserId)
}

function requireUser() {
  const user = currentUser()
  if (!user) {
    throw new Error('未登录')
  }
  return user
}

export const mockApi = {
  async login(payload) {
    const user = users.find((item) => item.username === payload.username && item.password === payload.password)
    if (!user) {
      throw new Error('用户名或密码错误')
    }
    currentUserId = user.id
    localStorage.setItem('wicmail_mock_user_id', String(user.id))
    return delay({ access_token: `mock-token-${user.id}`, token_type: 'bearer' })
  },

  async register(payload) {
    if (users.some((user) => user.username === payload.username)) {
      throw new Error('用户名已存在')
    }
    const user = {
      id: users.length + 1,
      username: payload.username,
      email: payload.email || null,
      password: payload.password,
      is_active: true,
      is_admin: false,
      created_at: new Date().toISOString(),
    }
    users.push(user)
    currentUserId = user.id
    localStorage.setItem('wicmail_mock_user_id', String(user.id))
    return delay(publicUser(user))
  },

  async me() {
    return delay(publicUser(requireUser()))
  },

  async listEmails({ page = 1, page_size = 20 } = {}) {
    const user = requireUser()
    const approvedMailboxIds = applications
      .filter((item) => item.user_id === user.id && item.status === 'approved' && item.mailbox_id)
      .map((item) => item.mailbox_id)
    const list = emails.filter((email) => user.is_admin || approvedMailboxIds.includes(email.mailbox_id))
    const start = (page - 1) * page_size
    return delay({
      total: list.length,
      page,
      page_size,
      emails: list.slice(start, start + page_size),
    })
  },

  async getEmail(id) {
    const email = emails.find((item) => item.id === Number(id))
    if (!email) {
      throw new Error('邮件不存在')
    }
    return delay(email)
  },

  async markRead(id) {
    const email = emails.find((item) => item.id === Number(id))
    if (email) email.is_read = true
    return delay({ status: 'ok', email_id: Number(id), is_read: true })
  },

  async markUnread(id) {
    const email = emails.find((item) => item.id === Number(id))
    if (email) email.is_read = false
    return delay({ status: 'ok', email_id: Number(id), is_read: false })
  },

  async applyMailbox(payload) {
    const user = requireUser()
    const address = `${payload.prefix.toLowerCase()}@wic.edu.kg`
    const application = {
      id: Date.now(),
      user_id: user.id,
      username: user.username,
      requested_address: address,
      display_name: payload.display_name || null,
      status: 'pending',
      reason: payload.reason || null,
      review_comment: null,
      reviewed_at: null,
      created_at: new Date().toISOString(),
      mailbox_id: null,
    }
    applications.unshift(application)
    return delay(application)
  },

  async listApplications() {
    const user = requireUser()
    const list = applications.filter((item) => item.user_id === user.id)
    return delay({ total: list.length, applications: list })
  },

  async listMailboxes() {
    const user = requireUser()
    const mailboxIds = applications
      .filter((item) => item.user_id === user.id && item.status === 'approved' && item.mailbox_id)
      .map((item) => item.mailbox_id)
    return delay(mailboxes.filter((item) => mailboxIds.includes(item.id)))
  },

  async adminListApplications(status) {
    requireUser()
    const list = status ? applications.filter((item) => item.status === status) : applications
    return delay(list)
  },

  async approveApplication(id, payload = {}) {
    const application = applications.find((item) => item.id === Number(id))
    const mailbox = {
      id: Date.now(),
      address: application.requested_address,
      display_name: application.display_name,
      is_active: true,
      created_at: new Date().toISOString(),
    }
    mailboxes.push(mailbox)
    application.status = 'approved'
    application.mailbox_id = mailbox.id
    application.review_comment = payload.comment || null
    application.reviewed_at = new Date().toISOString()
    return delay({ status: 'ok', mailbox_id: mailbox.id })
  },

  async rejectApplication(id, payload = {}) {
    const application = applications.find((item) => item.id === Number(id))
    application.status = 'rejected'
    application.review_comment = payload.comment || null
    application.reviewed_at = new Date().toISOString()
    return delay({ status: 'ok' })
  },

  async adminListUsers() {
    return delay(users.map(publicUser))
  },

  async toggleUserActive(id) {
    const user = users.find((item) => item.id === Number(id))
    if (user) user.is_active = !user.is_active
    return delay({ status: 'ok', is_active: user?.is_active })
  },
}
