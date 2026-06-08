"""WicMail 后端完整测试套件"""
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)

FIXTURE_DIR = Path(__file__).parent / "fixtures"
SAMPLE_PAYLOAD = json.loads((FIXTURE_DIR / "cloudflare_payload_sample.json").read_text())

SECRET = settings.cloudflare_email_secret_key


# ============================================================
# 认证测试
# ============================================================
class TestAuth:
    """登录 / 当前用户测试"""

    def _login(self, username="admin", password="admin123456"):
        return client.post("/api/auth/login", json={
            "username": username,
            "password": password,
        })

    def test_login_success(self):
        resp = self._login()
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        resp = self._login(password="wrongpassword")
        assert resp.status_code == 401

    def test_login_wrong_username(self):
        resp = client.post("/api/auth/login", json={
            "username": "nonexistent",
            "password": "whatever",
        })
        assert resp.status_code == 401

    def test_me_authenticated(self):
        token = self._login().json()["access_token"]
        resp = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "admin"
        assert data["is_active"] is True

    def test_me_unauthenticated(self):
        resp = client.get("/api/auth/me")
        assert resp.status_code in (401, 403)  # HTTPBearer 可能返回 401 或 403

    def test_me_invalid_token(self):
        resp = client.get("/api/auth/me", headers={
            "Authorization": "Bearer invalid.token.here",
        })
        assert resp.status_code == 401


# ============================================================
# 入站接口测试（X-Secret-Key，不需要 JWT）
# ============================================================
class TestInbound:
    """入站邮件接收接口测试"""

    def test_secret_key_valid(self):
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": SECRET},
        )
        assert resp.status_code == 200
        assert "email_id" in resp.json()

    def test_secret_key_invalid(self):
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": "wrong-key"},
        )
        assert resp.status_code == 403

    def test_inbound_no_jwt_needed(self):
        """入站接口不需要 JWT"""
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": SECRET},
        )
        assert resp.status_code == 200

    def test_parse_text_plain(self):
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": SECRET},
        )
        data = resp.json()
        assert data["status"] == "ok"
        assert data["parsed"]["text_body"] is not None

    def test_parse_html_body(self):
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": SECRET},
        )
        data = resp.json()
        assert data["parsed"]["html_body"] is not None

    def test_parse_subject(self):
        resp = client.post(
            "/api/inbound/cloudflare",
            json=SAMPLE_PAYLOAD,
            headers={"X-Secret-Key": SECRET},
        )
        assert resp.json()["parsed"]["subject"] == "Test Email Subject"

    def test_raw_too_large_no_raw(self):
        payload = {**SAMPLE_PAYLOAD, "raw": None, "raw_too_large": True}
        resp = client.post(
            "/api/inbound/cloudflare",
            json=payload,
            headers={"X-Secret-Key": SECRET},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "metadata_only"
        assert data["raw_too_large"] is True


# ============================================================
# 邮件查询测试（需要 JWT）
# ============================================================
class TestEmailQuery:
    """邮件查询接口测试（JWT 保护）"""

    def _get_token(self):
        resp = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "admin123456",
        })
        return resp.json()["access_token"]

    def _auth_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    # --- 权限测试 ---

    def test_list_emails_no_auth(self):
        resp = client.get("/api/emails")
        assert resp.status_code in (401, 403)  # 未认证

    def test_list_emails_invalid_token(self):
        resp = client.get("/api/emails", headers={
            "Authorization": "Bearer bad.token",
        })
        assert resp.status_code == 401

    def test_list_emails_authenticated(self):
        token = self._get_token()
        resp = client.get("/api/emails", headers=self._auth_headers(token))
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "emails" in data
        assert data["total"] >= 1

    def test_detail_no_auth(self):
        resp = client.get("/api/emails/1")
        assert resp.status_code in (401, 403)

    def test_detail_authenticated(self):
        token = self._get_token()
        resp = client.get("/api/emails/1", headers=self._auth_headers(token))
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1

    def test_detail_not_found(self):
        token = self._get_token()
        resp = client.get("/api/emails/999999", headers=self._auth_headers(token))
        assert resp.status_code == 404

    # --- 已读逻辑测试 ---

    def test_detail_does_not_auto_mark_read(self):
        """GET 详情不再自动标记已读"""
        token = self._get_token()

        # 先标记为未读
        client.patch("/api/emails/1/unread", headers=self._auth_headers(token))

        # 查看详情
        resp = client.get("/api/emails/1", headers=self._auth_headers(token))
        assert resp.status_code == 200
        assert resp.json()["is_read"] is False  # 不应自动变为 True

    # --- 分页 ---

    def test_pagination(self):
        token = self._get_token()
        resp = client.get(
            "/api/emails?page=1&page_size=1",
            headers=self._auth_headers(token),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["page_size"] == 1
        assert len(data["emails"]) <= 1


# ============================================================
# 已读/未读标记测试
# ============================================================
class TestReadUnread:
    """标记已读/未读接口测试"""

    def _get_token(self):
        resp = client.post("/api/auth/login", json={
            "username": "admin",
            "password": "admin123456",
        })
        return resp.json()["access_token"]

    def _auth_headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def test_mark_read(self):
        token = self._get_token()
        resp = client.patch("/api/emails/1/read", headers=self._auth_headers(token))
        assert resp.status_code == 200
        assert resp.json()["is_read"] is True

        # 验证
        resp = client.get("/api/emails/1", headers=self._auth_headers(token))
        assert resp.json()["is_read"] is True

    def test_mark_unread(self):
        token = self._get_token()
        resp = client.patch("/api/emails/1/unread", headers=self._auth_headers(token))
        assert resp.status_code == 200
        assert resp.json()["is_read"] is False

        # 验证
        resp = client.get("/api/emails/1", headers=self._auth_headers(token))
        assert resp.json()["is_read"] is False

    def test_mark_read_not_found(self):
        token = self._get_token()
        resp = client.patch("/api/emails/999999/read", headers=self._auth_headers(token))
        assert resp.status_code == 404

    def test_mark_unread_not_found(self):
        token = self._get_token()
        resp = client.patch("/api/emails/999999/unread", headers=self._auth_headers(token))
        assert resp.status_code == 404

    def test_mark_read_no_auth(self):
        resp = client.patch("/api/emails/1/read")
        assert resp.status_code in (401, 403)

    def test_mark_unread_no_auth(self):
        resp = client.patch("/api/emails/1/unread")
        assert resp.status_code in (401, 403)
