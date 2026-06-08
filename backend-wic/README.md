# WicMail User Service (backend-wic)

用户系统 + 私人邮局业务系统。

## 快速开始

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8001
```

## API 接口

### 认证（公开）
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /api/auth/register | 注册 |
| POST | /api/auth/login | 登录 → JWT |
| GET | /api/auth/me | 当前用户 |

### 邮箱管理（JWT）
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | /api/mailbox/apply | 申请邮箱 |
| GET | /api/mailbox/applications | 我的申请 |
| GET | /api/mailbox | 我的邮箱 |

### 邮件（JWT，限自己邮箱）
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /api/emails | 邮件列表 |
| GET | /api/emails/{id} | 邮件详情 |
| PATCH | /api/emails/{id}/read | 标记已读 |
| PATCH | /api/emails/{id}/unread | 标记未读 |

### 管理员（JWT + admin）
| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /api/admin/applications | 申请列表 |
| PATCH | /api/admin/applications/{id}/approve | 批准 |
| PATCH | /api/admin/applications/{id}/reject | 拒绝 |
| GET | /api/admin/users | 用户列表 |
| PATCH | /api/admin/users/{id}/toggle-active | 启用/禁用 |

## 测试

```bash
pytest tests/ -v
```
