"""邮箱申请相关模型"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MailboxApplyRequest(BaseModel):
    prefix: str = Field(..., min_length=3, max_length=30, description="邮箱前缀，如 abc → abc@wic.edu.kg")
    display_name: Optional[str] = None
    reason: Optional[str] = None


class MailboxApplicationResponse(BaseModel):
    id: int
    requested_address: str
    display_name: Optional[str] = None
    status: str
    reason: Optional[str] = None
    review_comment: Optional[str] = None
    created_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MailboxResponse(BaseModel):
    id: int
    address: str
    display_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ApplicationListResponse(BaseModel):
    total: int
    applications: List[MailboxApplicationResponse]
