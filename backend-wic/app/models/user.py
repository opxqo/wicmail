"""用户模型 - 与 backend-mail 共享 users 表"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

import bcrypt
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    student_id: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    real_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    major: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    class_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    grade: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.hashed_password.encode("utf-8"),
        )

    @property
    def profile_complete(self) -> bool:
        """资料是否完整（全部必填字段已填）"""
        return all([
            self.email,
            self.real_name,
            self.student_id,
            self.department,
            self.major,
            self.class_name,
            self.grade,
        ])

    def get_missing_fields(self) -> list[str]:
        """返回未填写的必填字段名"""
        field_map = {
            "email": "邮箱",
            "real_name": "真实姓名",
            "student_id": "学号",
            "department": "学部",
            "major": "专业",
            "class_name": "班级",
            "grade": "年级",
        }
        return [
            label for field, label in field_map.items()
            if not getattr(self, field)
        ]
