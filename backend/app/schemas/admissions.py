from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class CounselingSessionCreate(BaseModel):
    lead_id: str
    counselor_person_id: str
    session_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    academic_background: Dict[str, Any] = Field(default_factory=dict)
    career_interests: List[str] = Field(default_factory=list)
    recommended_program_ids: List[str] = Field(default_factory=list)


class ApplicationCreate(BaseModel):
    applicant_person_id: str
    program_id: str
    entry_term: str = "Fall 2026"
    form_data: Dict[str, Any] = Field(default_factory=dict)


class ApplicationResponse(BaseModel):
    id: str
    tenant_id: str
    application_number: str
    applicant_person_id: str
    program_id: str
    entry_term: str
    status: str
    submission_date: Optional[datetime] = None
    form_data: Dict[str, Any]
    is_documents_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    application_id: str
    document_type: str
    file_name: str
    file_url: str
    file_size_bytes: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str
    tenant_id: str
    application_id: str
    document_type: str
    file_name: str
    file_url: str
    verification_status: str
    rejection_reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
