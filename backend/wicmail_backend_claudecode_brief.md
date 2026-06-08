# WicMail 私人收件系统后端构建说明

> 供 Claude Code 读取和执行的项目上下文文档。  
> 当前目标：基于已经调通的 Cloudflare Email Worker，请 Claude Code 构建 FastAPI 后端接收接口。

---

## 1. 项目背景

本项目原始目标是搭建一个“私人电子邮局 / 私人收件系统”。

一开始讨论过两条路线：

1. **完整自建邮件服务器**
   - 使用 Postfix / Dovecot / Roundcube / Mailcow / iRedMail 等组件。
   - 优点是完全掌控邮件系统。
   - 缺点是运维复杂，尤其是发信送达率、IP 信誉、反垃圾配置、SPF / DKIM / DMARC 等问题较多。

2. **使用域名邮箱 / 邮件转发服务**
   - 借助 Cloudflare Email Routing、ImprovMX、ForwardEmail、Zoho Mail 等服务。
   - 优点是轻量、省心，不需要维护完整 SMTP / IMAP 邮件服务器。
   - 缺点是功能受平台限制，邮件入口依赖第三方。

最终选择了第二条路线中的一个变体：

```text
Cloudflare Email Routing → Email Worker → FastAPI → MySQL → 自己的 Web 管理界面
```

当前阶段只做 **收件系统**，暂不做发件系统。

---

## 2. 当前确定的技术路线

### 2.1 总体架构

```text
发件人
  ↓
Cloudflare Email Routing
  ↓
Cloudflare Email Worker
  ↓ HTTP POST JSON
FastAPI 后端
  ↓
MySQL 数据库
  ↓
Web 管理界面 / 邮件查看页面
```

### 2.2 当前阶段不做的事情

第一阶段不要做完整大系统，避免复杂度过高。

暂时不做：

- 发邮件功能
- SMTP 服务
- IMAP / POP3 服务
- 用户登录后台
- 附件下载接口
- MySQL 持久化
- Web 前端页面

第一阶段只做：

```text
Cloudflare Worker → FastAPI 接收接口 → 解析 raw 邮件 → 返回解析结果 JSON
```

---

## 3. 为什么必须使用 Cloudflare Email Worker

Cloudflare Email Routing 有两种主要使用方式：

1. 直接把邮件转发到真实邮箱，比如 Gmail / Outlook。
2. 把邮件交给 Email Worker 处理。

如果只是普通转发，FastAPI 后端无法感知邮件到达，也无法把邮件写入自己的 MySQL。

所以本项目必须使用 Email Worker。Worker 的职责非常轻：

```text
接收邮件 → 读取基本信息和 raw 原始邮件 → POST 到 FastAPI → 失败时转发到备用邮箱
```

复杂逻辑不要放在 Worker 里，例如：

- MIME 解析
- 正文提取
- HTML 清洗
- 附件存储
- 数据库操作

这些都应该放在 FastAPI 后端。

---

## 4. 已经完成的工作

### 4.1 已经完成 Cloudflare Email Worker 代码

已经得到一份可用 Worker，核心能力包括：

- 使用 `email(message, env, ctx)` 作为 Email Worker 入口。
- 读取：
  - `message.from`
  - `message.to`
  - `message.headers`
  - `message.raw`
  - `message.rawSize`
- 使用 `message.rawSize` 判断邮件大小。
- raw 不超限时，将原始邮件读取为 ArrayBuffer。
- 将 raw 转成 base64。
- 计算 `raw_sha256`。
- POST 到 `FASTAPI_URL`。
- 请求头携带：
  - `X-Secret-Key`
  - `X-Worker-Timestamp`
  - `X-Worker-Signature`
  - `X-Worker-Version`
- 后端推送失败时，使用 `message.forward(FALLBACK_EMAIL)` 兜底转发。
- raw 超出自定义上限时，可以只推送元数据，并将完整邮件转发到备用邮箱。

### 4.2 已经手动配置 Cloudflare

手动配置流程如下：

```text
Cloudflare Dashboard
→ 选择域名
→ Email Routing
→ 启用 Email Routing
→ 添加并验证 Destination Address
→ 创建 Email Worker
→ 粘贴 Worker 代码
→ 配置 Variables and Secrets
→ 创建 Routing Rule
→ Action 选择 Send to a Worker
```

### 4.3 已经用 Webhook.site 调试成功

由于当时还没有 FastAPI 后端，所以临时使用 Webhook.site 作为接收器。

调试方式：

1. 打开 Webhook.site，复制临时 URL。
2. 将 Cloudflare Worker 的 `FASTAPI_URL` 设置为这个 Webhook URL。
3. 发一封真实测试邮件到域名邮箱地址。
4. Webhook.site 成功收到 Worker POST 出来的 JSON。

这说明链路已经跑通：

```text
Cloudflare Email Routing → Email Worker → HTTP POST
```

---

## 5. 已验证的真实 Worker Payload 摘要

测试邮件已经成功进入 Worker，并 POST 到 Webhook.site。

真实 payload 主要字段如下：

```json
{
  "source": "cloudflare-email-worker",
  "worker_version": "1.0.0",
  "request_id": "9b91e905-0989-4ffe-865d-5b7b50c915f4",

  "envelope_from": "bilalbetesman@gmail.com",
  "envelope_to": "sdfsaf@wic.edu.kg",

  "header_from": "\"Bilalbetesman\" <bilalbetesman@gmail.com>",
  "header_to": "sdfsaf@wic.edu.kg",
  "header_cc": "",
  "header_reply_to": "",

  "subject": "asdadad",
  "message_id": "<CACt6hnH06kd3WGy8LUP0B2ZRB3rHBz2nBxFWLxQ=QRZ0arTKkg@mail.gmail.com>",
  "date": "Mon, 8 Jun 2026 10:25:16 +0800",

  "headers": {
    "content-type": "multipart/alternative; boundary=\"00000000000052eee00653b4b9ed\"",
    "date": "Mon, 8 Jun 2026 10:25:16 +0800",
    "from": "\"Bilalbetesman\" <bilalbetesman@gmail.com>",
    "message-id": "<CACt6hnH06kd3WGy8LUP0B2ZRB3rHBz2nBxFWLxQ=QRZ0arTKkg@mail.gmail.com>",
    "mime-version": "1.0",
    "subject": "asdadad",
    "to": "sdfsaf@wic.edu.kg",
    "x-cf-spamh-score": "1"
  },

  "raw_size": 6930,
  "raw": "base64 encoded raw email content",
  "raw_encoding": "base64",
  "raw_sha256": "b341e634e2426b23e3ff82b3d45e4803b04e55488b01477a6bf76c40f6effd1f",
  "raw_too_large": false,
  "received_at": "2026-06-08T02:25:30.228Z"
}
```

注意：真实 payload 中的 `raw` 非常长，不建议直接写入项目说明文件。测试时可单独保存为：

```text
tests/fixtures/cloudflare_payload_real.json
```

---

## 6. `SECRET_KEY` 的作用

`SECRET_KEY` 是 Worker 和 FastAPI 后端共享的一串密钥。

作用：

```text
防止陌生人直接向公开的 FastAPI 接口伪造邮件数据。
```

未来 FastAPI 接口会暴露在公网，例如：

```text
https://api.wic.edu.kg/api/inbound/cloudflare
```

如果没有校验，任何人都可以直接 POST 假数据到接口，导致数据库被写入伪造邮件。

Worker 请求时会带：

```http
X-Secret-Key: your-secret-key
```

FastAPI 需要检查：

```python
if x_secret_key != settings.CLOUDFLARE_EMAIL_SECRET_KEY:
    raise HTTPException(status_code=403)
```

`SECRET_KEY` 不是邮箱密码，也不是 Cloudflare 密码。它只是 Worker 和 FastAPI 之间的共享暗号。

建议使用类似下面的方式生成：

```bash
openssl rand -hex 32
```

---

## 7. FastAPI 后端第一阶段目标

Claude Code 当前需要构建的是 **后端 MVP**。

### 7.1 必须实现的接口

```http
POST /api/inbound/cloudflare
```

功能：

1. 接收 Cloudflare Email Worker POST 的 JSON。
2. 校验请求头 `X-Secret-Key`。
3. 兼容 Worker payload 字段。
4. 如果 `raw_encoding == "base64"` 且 `raw` 不为空：
   - base64 解码 raw。
   - 使用 Python 标准库解析邮件。
5. 提取邮件内容：
   - subject
   - from
   - to
   - text/plain 正文
   - text/html 正文
   - 附件元数据
6. 第一阶段暂时不入库，只返回解析结果 JSON。

### 7.2 Python 邮件解析方式

不要使用：

```python
email.message_from_string(payload.raw)
```

因为 Worker 传来的 raw 是 base64，并且邮件可能包含中文、HTML、附件和二进制内容。

应该使用：

```python
import base64
import email
from email import policy

raw_bytes = base64.b64decode(payload.raw)
msg = email.message_from_bytes(raw_bytes, policy=policy.default)
```

---

## 8. 建议的 FastAPI 项目结构

请 Claude Code 创建下面结构：

```text
wicmail-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── inbound.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── inbound.py
│   └── services/
│       ├── __init__.py
│       └── mail_parser.py
├── tests/
│   ├── test_inbound.py
│   └── fixtures/
│       ├── cloudflare_payload_sample.json
│       └── cloudflare_payload_real.json
├── .env.example
├── requirements.txt
└── README.md
```

---

## 9. 建议的依赖

`requirements.txt` 第一阶段可以包含：

```text
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-dotenv
pytest
httpx
```

如果后续接 MySQL，再增加：

```text
sqlalchemy
alembic
asyncmy
```

---

## 10. 环境变量设计

`.env.example`：

```env
APP_NAME=WicMail Backend
APP_ENV=development
CLOUDFLARE_EMAIL_SECRET_KEY=change-me
```

第一阶段只需要 `CLOUDFLARE_EMAIL_SECRET_KEY`。

后续 MySQL 阶段再加入：

```env
DATABASE_URL=mysql+asyncmy://user:password@127.0.0.1:3306/wicmail
```

---

## 11. Pydantic Schema 要求

建议创建：

```python
from typing import Any
from pydantic import BaseModel, Field

class CloudflareInboundEmail(BaseModel):
    source: str | None = None
    worker_version: str | None = None
    request_id: str

    envelope_from: str
    envelope_to: str

    header_from: str | None = None
    header_to: str | None = None
    header_cc: str | None = None
    header_reply_to: str | None = None

    subject: str | None = None
    message_id: str | None = None
    date: str | None = None

    headers: dict[str, Any] = Field(default_factory=dict)

    raw_size: int | None = None
    raw: str | None = None
    raw_encoding: str | None = None
    raw_sha256: str | None = None
    raw_too_large: bool = False

    received_at: str | None = None
```

要求：

- 兼容真实 Worker payload。
- 如果未来 Worker 多传字段，不要轻易报错。
- 字段缺失时尽量给合理默认值。

---

## 12. 邮件解析服务要求

建议创建：

```text
app/services/mail_parser.py
```

核心函数：

```python
def parse_raw_email(raw_bytes: bytes) -> ParsedEmail:
    ...
```

需要提取：

```text
subject
from
to
cc
reply_to
text_body
html_body
attachments
```

附件元数据格式：

```json
{
  "filename": "example.pdf",
  "content_type": "application/pdf",
  "size": 12345
}
```

第一阶段不需要保存附件文件，只要识别元数据即可。

---

## 13. 接口返回格式建议

成功时返回：

```json
{
  "status": "ok",
  "request_id": "...",
  "raw_too_large": false,
  "parsed": {
    "subject": "asdadad",
    "from": "Bilalbetesman <bilalbetesman@gmail.com>",
    "to": "sdfsaf@wic.edu.kg",
    "text_body": "...",
    "html_body": "...",
    "attachments": []
  }
}
```

密钥错误时返回 HTTP 403。

raw 缺失但 `raw_too_large == true` 时，不要报 500，应该返回：

```json
{
  "status": "metadata_only",
  "request_id": "...",
  "raw_too_large": true
}
```

---

## 14. 本地运行命令

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Windows PowerShell 可用：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 15. 本地 curl 测试方式

保存真实 Worker payload 到：

```text
tests/fixtures/cloudflare_payload_real.json
```

然后执行：

```bash
curl -X POST "http://127.0.0.1:8000/api/inbound/cloudflare" \
  -H "Content-Type: application/json" \
  -H "X-Secret-Key: test-secret-123456" \
  --data @tests/fixtures/cloudflare_payload_real.json
```

`.env` 中应该有：

```env
CLOUDFLARE_EMAIL_SECRET_KEY=test-secret-123456
```

---

## 16. Pytest 测试要求

Claude Code 需要创建测试：

```text
tests/test_inbound.py
```

测试点：

1. `POST /api/inbound/cloudflare` 在密钥正确时返回 200。
2. 密钥错误时返回 403。
3. 使用 sample fixture 能解析 text/plain。
4. 使用 real fixture 能兼容真实 payload。
5. `raw_encoding == base64` 时能正确解码。
6. `raw_too_large == true` 且 raw 为空时不会 500。

运行：

```bash
pytest
```

---

## 17. 给 Claude Code 的第一条提示词

在项目目录运行：

```bash
claude
```

然后粘贴：

```text
请读取当前目录的说明文档，然后从零创建 FastAPI 后端 MVP。

目标是实现 Cloudflare Email Worker 的入站邮件接收接口：

POST /api/inbound/cloudflare

要求：
1. 使用 FastAPI + Pydantic。
2. 从请求头读取 X-Secret-Key，并和 .env 里的 CLOUDFLARE_EMAIL_SECRET_KEY 比较。
3. 请求体字段按说明文档里的 Worker 请求格式建 Pydantic 模型。
4. 如果 raw_encoding == "base64" 且 raw 不为空，base64 解码 raw。
5. 使用 email.message_from_bytes(raw_bytes, policy=policy.default) 解析邮件。
6. 提取 subject、from、to、text/plain、text/html、attachments 元数据。
7. 暂时不接 MySQL，先返回解析结果 JSON。
8. 创建 requirements.txt、.env.example、README.md。
9. 创建 pytest 测试。
10. 创建 tests/fixtures/cloudflare_payload_sample.json，先放一个简化版测试 payload，不要包含超长 raw。
11. 预留 tests/fixtures/cloudflare_payload_real.json 给真实 Webhook payload。
12. 最后告诉我如何本地运行和测试。

请先给出你准备创建的目录结构，然后再开始修改文件。
```

---

## 18. 给 Claude Code 的第二条提示词：接入真实 Payload

当第一版生成后，把 Webhook.site 收到的真实 JSON 保存为：

```text
tests/fixtures/cloudflare_payload_real.json
```

然后对 Claude Code 说：

```text
我已经把真实 Cloudflare Worker 请求体保存到了 tests/fixtures/cloudflare_payload_real.json。

请你：
1. 读取这个 fixture。
2. 更新 Pydantic schema，确保能兼容真实 payload。
3. 更新测试，让 test_inbound.py 使用真实 fixture 调用 POST /api/inbound/cloudflare。
4. 验证 raw base64 可以被成功解析。
5. 验证能提取 text/plain 和 text/html 正文。
6. 如果真实 payload 里有 Gmail/Cloudflare 的额外 headers，不要因为字段多而报错。
7. 跑 pytest，如果失败请修复。
```

---

## 19. 后续 MySQL 阶段设计

第一阶段通过后，再接 MySQL。

### 19.1 推荐表结构

#### mailboxes

```text
id
address          唯一，例如 sdfsaf@wic.edu.kg
display_name
is_active
created_at
updated_at
```

#### email_messages

```text
id
mailbox_id
request_id
message_id
raw_sha256
envelope_from
envelope_to
header_from
header_to
header_cc
header_reply_to
subject
sent_at
received_at
raw_size
raw_too_large
headers_json
body_text
body_html
parse_status      received / parsed / failed
parse_error
is_read
created_at
updated_at
```

#### attachments

```text
id
email_id
filename
content_type
size
storage_path
created_at
```

### 19.2 推荐索引

```text
mailboxes.address unique
email_messages.message_id
email_messages.raw_sha256
email_messages.mailbox_id + received_at
attachments.email_id
```

### 19.3 给 Claude Code 的 MySQL 提示词

```text
现在入站接口已经可以解析 Cloudflare Worker 的 payload。

请在现有项目基础上接入 MySQL，要求：

1. 使用 SQLAlchemy 2.x async。
2. 使用 asyncmy 作为 MySQL async driver。
3. 添加 app/database.py。
4. 添加 models：Mailbox、EmailMessage、Attachment。
5. 添加 Alembic 迁移。
6. POST /api/inbound/cloudflare 成功解析后：
   - 根据 envelope_to 获取或创建 mailbox。
   - 保存邮件基础信息。
   - 保存 text/plain、text/html、headers_json、raw_sha256、message_id。
   - 保存附件元数据，附件内容暂时不落盘。
7. message_id 或 raw_sha256 重复时不要重复入库。
8. 添加 GET /api/emails 邮件列表接口。
9. 添加 GET /api/emails/{email_id} 邮件详情接口。
10. 添加测试。
11. 更新 README。
```

---

## 20. 后续 Worker 环境变量正式配置

调试阶段曾经使用 Webhook.site 作为 `FASTAPI_URL`。

当 FastAPI 后端部署成功后，需要把 Cloudflare Worker 的变量改成真实后端地址：

```text
FASTAPI_URL=https://api.wic.edu.kg/api/inbound/cloudflare
SECRET_KEY=与 FastAPI .env 中 CLOUDFLARE_EMAIL_SECRET_KEY 相同的密钥
FALLBACK_EMAIL=已经在 Cloudflare Email Routing 验证过的备用邮箱
MAX_RAW_SIZE_MB=10
REQUEST_TIMEOUT_MS=20000
FORWARD_TOO_LARGE=true
REJECT_ON_FAILURE=false
```

正式上线前建议重新生成新的 `SECRET_KEY`，不要继续使用测试密钥。

---

## 21. 当前最重要的验收标准

第一阶段验收标准非常明确：

```text
1. pytest 通过。
2. uvicorn 能启动。
3. curl 使用真实 payload 调接口返回 status=ok。
4. 返回结果中能看到 text/plain 正文。
5. 返回结果中能看到 text/html 正文。
6. 密钥错误时返回 403。
7. raw_too_large 情况不会导致 500。
```

只有第一阶段通过后，再进入 MySQL 阶段。

---

## 22. 关键提醒

1. Worker 不负责解析邮件，只负责转发 raw。
2. FastAPI 必须先 base64 解码 raw，再 `message_from_bytes`。
3. `SECRET_KEY` 只是 Worker 和 FastAPI 之间的共享密钥，不是邮箱密码。
4. Webhook.site 只用于测试，不要长期用于真实邮件。
5. 真实邮件内容可能包含隐私，测试完成后应删除第三方 Webhook 里的记录。
6. 第一阶段不要急着接数据库，先把解析链路跑通。
7. 数据库阶段要考虑 `message_id` / `raw_sha256` 去重，避免重复入库。

---

## 23. 一句话总结

当前项目已经完成并验证了：

```text
Cloudflare Email Routing → Email Worker → Webhook 调试接收器
```

下一步 Claude Code 应该构建：

```text
FastAPI POST /api/inbound/cloudflare
```

让它可以接收 Worker JSON、校验密钥、base64 解码 raw、解析邮件正文和附件元数据。第一阶段通过后，再接入 MySQL 和邮件管理接口。
