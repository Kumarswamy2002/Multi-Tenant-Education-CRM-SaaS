from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_slug: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    user_id: str
    tenant_id: str
    roles: List[str]


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    role_code: str = "counselor"
    person_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    tenant_id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_super_admin: bool
    person_id: Optional[str] = None
    last_login_at: Optional[datetime] = None
    roles: List[str] = []

    class Config:
        from_attributes = True
