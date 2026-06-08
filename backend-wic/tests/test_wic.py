"""backend-wic 完整测试"""
import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def uid():
    """生成唯一后缀避免重复"""
    return uuid.uuid4().hex[:6]


class TestHealth:
    def test_health(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


# ============================================================
# 认证测试
# ============================================================
class TestAuth:
    def _register(self, username=None, student_id=None, password="testpass123"):
        username = username or f"user_{uid()}"
        student_id = student_id or f"SID{uid().upper()}"
        return client.post("/api/auth/register", json={
            "username": username,
            "student_id": student_id,
            "password": password,
        }), username

    def _login(self, username, password="testpass123"):
        return client.post("/api/auth/login", json={
            "username": username,
            "password": password,
        })

    def test_register_success(self):
        resp, name = self._register()
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == name
        assert data["is_admin"] is False

    def test_register_requires_student_id(self):
        """注册必须提供学号"""
        resp = client.post("/api/auth/register", json={
            "username": f"u_{uid()}",
            "password": "password123",
        })
        assert resp.status_code == 422

    def test_register_duplicate_username(self):
        resp, name = self._register()
        resp2, _ = self._register(username=name)
        assert resp2.status_code == 400

    def test_register_duplicate_student_id(self):
        sid = f"DUP{uid().upper()}"
        self._register(student_id=sid)
        resp2, _ = self._register(student_id=sid)
        assert resp2.status_code == 400

    def test_register_invalid_username(self):
        resp, _ = self._register(username="BAD USER!")
        assert resp.status_code == 422

    def test_register_short_password(self):
        resp, _ = self._register(password="12345")
        assert resp.status_code == 422

    def test_login_success(self):
        _, name = self._register()
        resp = self._login(name)
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_login_wrong_password(self):
        _, name = self._register()
        resp = self._login(name, password="wrongpassword")
        assert resp.status_code == 401

    def test_me_authenticated(self):
        _, name = self._register()
        token = self._login(name).json()["access_token"]
        resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["username"] == name

    def test_me_unauthenticated(self):
        resp = client.get("/api/auth/me")
        assert resp.status_code in (401, 403)


# ============================================================
# 个人资料测试
# ============================================================
class TestProfile:
    def _register_and_login(self):
        name = f"prof_{uid()}"
        sid = f"PROF{uid().upper()}"
        client.post("/api/auth/register", json={
            "username": name, "student_id": sid, "password": "password123",
        })
        resp = client.post("/api/auth/login", json={"username": name, "password": "password123"})
        return resp.json()["access_token"]

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def test_profile_incomplete_after_register(self):
        """注册后资料不完整"""
        token = self._register_and_login()
        resp = client.get("/api/auth/profile", headers=self._auth(token))
        assert resp.status_code == 200
        data = resp.json()
        assert data["profile_complete"] is False
        assert len(data["missing_fields"]) > 0

    def test_profile_update_single_field(self):
        """单字段更新"""
        token = self._register_and_login()
        resp = client.patch("/api/auth/profile",
            json={"real_name": "张三"}, headers=self._auth(token))
        assert resp.status_code == 200
        assert resp.json()["real_name"] == "张三"

    def test_profile_update_multiple_fields(self):
        """多字段更新"""
        token = self._register_and_login()
        resp = client.patch("/api/auth/profile",
            json={
                "email": f"{uid()}@test.com",
                "real_name": "李四",
                "department": "计算机学部",
                "major": "软件工程",
                "class_name": "软工2301",
                "grade": "2023",
            },
            headers=self._auth(token),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["profile_complete"] is True
        assert len(data["missing_fields"]) == 0

    def test_profile_no_update_fields(self):
        """不传任何字段应报错"""
        token = self._register_and_login()
        resp = client.patch("/api/auth/profile", json={}, headers=self._auth(token))
        assert resp.status_code == 400

    def test_profile_invalid_email(self):
        token = self._register_and_login()
        resp = client.patch("/api/auth/profile",
            json={"email": "not-an-email"}, headers=self._auth(token))
        assert resp.status_code == 422


# ============================================================
# 邮箱申请测试
# ============================================================
class TestMailbox:
    def _get_token(self, complete_profile=False):
        name = f"mb_{uid()}"
        sid = f"MB{uid().upper()}"
        client.post("/api/auth/register", json={
            "username": name, "student_id": sid, "password": "password123",
        })
        resp = client.post("/api/auth/login", json={"username": name, "password": "password123"})
        token = resp.json()["access_token"]

        if complete_profile:
            client.patch("/api/auth/profile", json={
                "email": f"{uid()}@test.com",
                "real_name": "测试用户",
                "department": "计算机学部",
                "major": "软件工程",
                "class_name": "软工2301",
                "grade": "2023",
            }, headers={"Authorization": f"Bearer {token}"})

        return token

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def test_apply_incomplete_profile_rejected(self):
        """资料不完整不能申请邮箱"""
        token = self._get_token(complete_profile=False)
        resp = client.post(
            "/api/mailbox/apply",
            json={"prefix": f"test{uid()}"},
            headers=self._auth(token),
        )
        assert resp.status_code == 400
        assert "完善个人资料" in resp.json()["detail"]

    def test_apply_mailbox(self):
        token = self._get_token(complete_profile=True)
        prefix = f"test{uid()}"
        resp = client.post(
            "/api/mailbox/apply",
            json={"prefix": prefix, "reason": "test"},
            headers=self._auth(token),
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["requested_address"] == f"{prefix}@wic.edu.kg"
        assert data["status"] == "pending"

    def test_apply_duplicate_address(self):
        token = self._get_token(complete_profile=True)
        prefix = f"dup{uid()}"
        client.post("/api/mailbox/apply", json={"prefix": prefix}, headers=self._auth(token))
        resp = client.post("/api/mailbox/apply", json={"prefix": prefix}, headers=self._auth(token))
        assert resp.status_code == 400

    def test_apply_invalid_prefix(self):
        token = self._get_token(complete_profile=True)
        resp = client.post("/api/mailbox/apply", json={"prefix": ".bad"}, headers=self._auth(token))
        assert resp.status_code == 400

    def test_list_applications(self):
        token = self._get_token(complete_profile=True)
        client.post("/api/mailbox/apply", json={"prefix": f"list{uid()}"}, headers=self._auth(token))
        resp = client.get("/api/mailbox/applications", headers=self._auth(token))
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    def test_apply_no_auth(self):
        resp = client.post("/api/mailbox/apply", json={"prefix": "noauth123"})
        assert resp.status_code in (401, 403)


# ============================================================
# 邮件查看测试（用户隔离）
# ============================================================
class TestEmails:
    def _get_user_token(self):
        name = f"em_{uid()}"
        sid = f"EM{uid().upper()}"
        client.post("/api/auth/register", json={
            "username": name, "student_id": sid, "password": "password123",
        })
        resp = client.post("/api/auth/login", json={"username": name, "password": "password123"})
        return resp.json()["access_token"]

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def test_email_list_no_mailbox(self):
        token = self._get_user_token()
        resp = client.get("/api/emails", headers=self._auth(token))
        assert resp.status_code == 200
        assert resp.json()["total"] == 0

    def test_email_list_no_auth(self):
        resp = client.get("/api/emails")
        assert resp.status_code in (401, 403)


# ============================================================
# 管理员测试
# ============================================================
class TestAdmin:
    def _get_admin_token(self):
        resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123456"})
        return resp.json()["access_token"]

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def _complete_profile(self, token):
        """辅助方法：为用户补全资料"""
        client.patch("/api/auth/profile", json={
            "email": f"{uid()}@test.com",
            "real_name": "测试用户",
            "department": "计算机学部",
            "major": "软件工程",
            "class_name": "软工2301",
            "grade": "2023",
        }, headers={"Authorization": f"Bearer {token}"})

    def test_admin_list_applications(self):
        token = self._get_admin_token()
        resp = client.get("/api/admin/applications", headers=self._auth(token))
        assert resp.status_code == 200

    def test_admin_list_users(self):
        token = self._get_admin_token()
        resp = client.get("/api/admin/users", headers=self._auth(token))
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_non_admin_forbidden(self):
        name = f"noadm_{uid()}"
        sid = f"NA{uid().upper()}"
        client.post("/api/auth/register", json={
            "username": name, "student_id": sid, "password": "password123",
        })
        resp = client.post("/api/auth/login", json={"username": name, "password": "password123"})
        token = resp.json()["access_token"]
        resp = client.get("/api/admin/users", headers=self._auth(token))
        assert resp.status_code == 403

    def test_admin_approve_flow(self):
        """完整流程：用户注册 → 补全资料 → 申请邮箱 → 管理员批准 → 用户看到邮箱"""
        prefix = f"flow{uid()}"

        # 用户注册 + 登录
        name = f"flow_{uid()}"
        sid = f"FL{uid().upper()}"
        client.post("/api/auth/register", json={
            "username": name, "student_id": sid, "password": "password123",
        })
        resp = client.post("/api/auth/login", json={"username": name, "password": "password123"})
        user_token = resp.json()["access_token"]
        user_auth = {"Authorization": f"Bearer {user_token}"}

        # 补全资料
        self._complete_profile(user_token)

        # 申请邮箱
        client.post("/api/mailbox/apply", json={"prefix": prefix}, headers=user_auth)

        # 管理员批准
        admin_token = self._get_admin_token()
        admin_auth = {"Authorization": f"Bearer {admin_token}"}

        resp = client.get("/api/admin/applications?status=pending", headers=admin_auth)
        apps = resp.json()
        flow_app = next((a for a in apps if a["requested_address"] == f"{prefix}@wic.edu.kg"), None)
        assert flow_app is not None

        resp = client.patch(
            f"/api/admin/applications/{flow_app['id']}/approve",
            json={"comment": "approved"},
            headers=admin_auth,
        )
        assert resp.status_code == 200

        # 用户查看已批准邮箱
        resp = client.get("/api/mailbox", headers=user_auth)
        assert resp.status_code == 200
        mailboxes = resp.json()
        assert any(m["address"] == f"{prefix}@wic.edu.kg" for m in mailboxes)
