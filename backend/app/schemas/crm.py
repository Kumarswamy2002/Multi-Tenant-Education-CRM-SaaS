from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    lead_source_id: Optional[str] = None
    assigned_counselor_person_id: Optional[str] = None
    academic_interest_program_id: Optional[str] = None
    custom_fields: Dict[str, Any] = Field(default_factory=dict)


class LeadResponse(BaseModel):
    id: str
    tenant_id: str
    person_id: str
    status: str
    stage: str
    lead_source_id: Optional[str] = None
    assigned_counselor_person_id: Optional[str] = None
    score: float
    academic_interest_program_id: Optional[str] = None
    custom_fields: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    person_id: str
    activity_type: str  # call, email, meeting, note, task
    subject: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class CaseCreate(BaseModel):
    title: str
    description: str
    category: str = "academic"  # academic, admission, finance, documentation, tech, hostel, career
    priority: str = "medium"  # low, medium, high, urgent
    reporter_person_id: str
    assigned_person_id: Optional[str] = None
    department_id: Optional[str] = None


class CaseResponse(BaseModel):
    id: str
    tenant_id: str
    ticket_number: str
    title: str
    description: str
    category: str
    priority: str
    status: str
    reporter_person_id: str
    assigned_person_id: Optional[str] = None
    department_id: Optional[str] = None
    resolution_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
