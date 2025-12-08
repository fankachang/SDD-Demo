from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Contact(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    group: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class Program(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class RecipientInput(BaseModel):
    email: EmailStr
    type: str


class ReleaseCreate(BaseModel):
    program_id: int
    version: str
    notes: Optional[str]
    recipients: List[RecipientInput]


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
