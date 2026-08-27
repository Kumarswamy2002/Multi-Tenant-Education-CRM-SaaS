from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str
    code: Optional[str] = None
    org_type: str = "institution"  # institution, employer, partner, external
    industry: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Dict[str, Any] = Field(default_factory=dict)
    parent_id: Optional[str] = None


class OrganizationResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    code: Optional[str] = None
    org_type: str
    industry: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Dict[str, Any]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DepartmentCreate(BaseModel):
    organization_id: str
    campus_id: Optional[str] = None
    name: str
    code: str
    head_person_id: Optional[str] = None


class ProgramCreate(BaseModel):
    department_id: str
    name: str
    code: str
    degree_level: str = "bachelors"
    duration_months: int = 36
    credits_required: int = 120
    tuition_fee: Optional[str] = "15000 USD"


class ProgramResponse(BaseModel):
    id: str
    tenant_id: str
    department_id: str
    name: str
    code: str
    degree_level: str
    duration_months: int
    credits_required: int
    tuition_fee: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
