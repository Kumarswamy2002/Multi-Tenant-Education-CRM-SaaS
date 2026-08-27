from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class TenantCreate(BaseModel):
    name: str = Field(..., example="Harvard University")
    slug: str = Field(..., example="harvard")
    domain: Optional[str] = Field(None, example="harvard.edu")
    plan_tier: str = Field("standard", example="enterprise")
    max_users: int = Field(50, ge=1)
    max_students: int = Field(5000, ge=1)
    settings: Dict[str, Any] = Field(default_factory=dict)

    # Initial Admin details
    admin_email: EmailStr = Field(..., example="admin@harvard.edu")
    admin_first_name: str = Field(..., example="John")
    admin_last_name: str = Field(..., example="Harvard")
    admin_password: str = Field(..., min_length=8)


class TenantResponse(BaseModel):
    id: str
    name: str
    slug: str
    domain: Optional[str] = None
    is_active: bool
    plan_tier: str
    max_users: int
    max_students: int
    settings: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
