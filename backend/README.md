# WicMail Backend

私人收件系统后端 — 接收 Cloudflare Email Worker 推送的邮件，解析并入库，提供 JWT 认证的查询接口。

## 架构

```
发件人 → Cloudflare Email Routing → Email Worker → FastAPI → MySQL → Web UI
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 复制环境变量（按需修改）
cp .env.example .env

# 执行数据库迁移
alembic upgrade head

# 启动服务（首次启动会自动创建 admin 管理员）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

默认管理员：`admin` / `admin123456`（请尽快修改密码）

## API 接口

### 认证

| 方法 | 路径 | 认证 | 功能 |
|---|---|---|---|
| `POST` | `/api/auth/login` | 无 | 登录，返回 JWT access_token |
| `GET` | `/api/auth/me` | JWT | 获取当前登录用户 |

### 邮件入站

| 方法 | 路径 | 认证 | 功能 |
|---|---|---|---|
| `POST` | `/api/inbound/cloudflare` | X-Secret-Key | 接收 Worker 推送的邮件 |

### 邮件查询（需要 JWT）

| 方法 | 路径 | 功能 |
|---|---|---|
| `GET` | `/api/emails?page=1&page_size=20` | 分页邮件列表 |
| `GET` | `/api/emails/{id}` | 邮件详情 |
| `PATCH` | `/api/emails/{id}/read` | 标记已读 |
| `PATCH` | `/api/emails/{id}/unread` | 标记未读 |

### 健康检查

| 方法 | 路径 | 功能 |
|---|---|---|
| `GET` | `/health` | 健康检查 |

## 认证示例

```bash
# 登录获取 token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123456"}' | jq -r .access_token)

# 使用 token 访问接口
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/api/emails
```

## 测试

```bash
pytest tests/ -v
```

## 数据库迁移

```bash
# 生成新迁移
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head
```

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `DATABASE_URL` | MySQL 连接串 | `mysql+asyncmy://...` |
| `CLOUDFLARE_EMAIL_SECRET_KEY` | Worker 共享密钥 | `change-me` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | `change-me` |
| `JWT_ALGORITHM` | JWT 算法 | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token 过期时间 | `1440` |
| `DEFAULT_ADMIN_USERNAME` | 默认管理员用户名 | `admin` |
| `DEFAULT_ADMIN_PASSWORD` | 默认管理员密码 | `admin123456` |
