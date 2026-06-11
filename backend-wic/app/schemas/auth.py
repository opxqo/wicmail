"""认证相关请求/响应模型"""
import re
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# --- 注册 ---
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名：小写字母、数字、下划线、横线")
    student_id: str = Field(..., min_length=1, max_length=20, description="学号")
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9_-]+$", v):
            raise ValueError("用户名只能包含小写字母、数字、下划线和横线")
        return v

    @field_validator("student_id")
    @classmethod
    def validate_student_id(cls, v: str) -> str:
        # 存储为大写
        v = v.upper()
        if not re.match(r"^[A-Z0-9]+$", v):
            raise ValueError("学号只能包含字母和数字")
        return v


# --- 登录 ---
class LoginRequest(BaseModel):
    username: str
    password: str


# --- Token ---
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- 用户基本信息 ---
class UserResponse(BaseModel):
    id: int
    username: str
    student_id: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    real_name: Optional[str] = None
    is_active: bool
    is_admin: bool

    model_config = {"from_attributes": True}


# --- 完整资料 ---
class ProfileResponse(BaseModel):
    id: int
    username: str
    student_id: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    grade: Optional[str] = None
    profile_complete: bool
    missing_fields: List[str]
    is_active: bool
    is_admin: bool

    model_config = {"from_attributes": True}


# --- 资料更新（单字段） ---
class ProfileUpdateRequest(BaseModel):
    email: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    real_name: Optional[str] = Field(None, min_length=1, max_length=50)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    major: Optional[str] = Field(None, min_length=1, max_length=100)
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    grade: Optional[str] = Field(None, min_length=1, max_length=10)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("邮箱格式不正确")
        return v
