from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    """登入請求 Schema"""

    email: EmailStr
    password: str


class Contact(BaseModel):
    """聯絡人 Schema - 用於 CRUD 操作"""

    id: Optional[int] = None
    name: str
    email: EmailStr
    group: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """驗證名稱不為空"""
        if not v or not v.strip():
            raise ValueError("名稱不能為空")
        return v.strip()

    @field_validator("group")
    @classmethod
    def validate_group(cls, v):
        """驗證群組名稱（如果提供）"""
        if v is not None and v.strip():
            return v.strip()
        return v


class Program(BaseModel):
    """程式 Schema - 用於 CRUD 操作"""

    id: Optional[int] = None
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        """驗證程式名稱不為空"""
        if not v or not v.strip():
            raise ValueError("程式名稱不能為空")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        """驗證描述（如果提供）"""
        if v is not None and v.strip():
            return v.strip()
        return v


class RecipientInput(BaseModel):
    """收件人輸入 Schema - 用於建立 release 或發送郵件時指定收件人"""

    email: EmailStr
    type: str  # 'to', 'cc', 'bcc'

    model_config = ConfigDict(from_attributes=True)


class ReleaseRecipientOut(BaseModel):
    """收件人快照輸出 Schema - 顯示已儲存的收件人資訊"""

    id: int
    email: str
    recipient_type: str

    model_config = ConfigDict(from_attributes=True)


class ReleaseCreate(BaseModel):
    """建立 Release 的輸入 Schema"""

    program_id: int
    version: str
    notes: Optional[str] = None
    recipients: Optional[List[RecipientInput]] = None


class ReleaseCreateSchema(BaseModel):
    """建立 Release 的完整輸入 Schema（別名，與 ReleaseCreate 相同）"""

    program_id: int
    version: str
    notes: Optional[str] = None
    recipients: Optional[List[RecipientInput]] = None


class ReleasePreviewSchema(BaseModel):
    """Release 預覽輸出 Schema - 包含渲染後的郵件內容"""

    release_id: int
    program_name: str
    version: str
    notes: Optional[str] = None
    subject: str
    body_html: str
    body_text: Optional[str] = None
    recipient_count: int
    recipients: List[ReleaseRecipientOut]

    model_config = ConfigDict(from_attributes=True)


class ReleaseOut(BaseModel):
    id: int
    program_id: int
    version: str
    notes: Optional[str]
    status: str

    model_config = ConfigDict(from_attributes=True)


class SendLogOut(BaseModel):
    id: int
    release_id: int
    sent_at: datetime
    result: str
    detail: Optional[str]

    model_config = ConfigDict(from_attributes=True)
