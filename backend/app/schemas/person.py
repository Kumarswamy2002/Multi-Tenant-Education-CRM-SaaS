from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import date, datetime


class PersonCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    address: Dict[str, Any] = Field(default_factory=dict)
    avatar_url: Optional[str] = None
    primary_role: str = "prospect"
    metadata_fields: Dict[str, Any] = Field(default_factory=dict)


class PersonResponse(BaseModel):
    id: str
    tenant_id: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    address: Dict[str, Any]
    avatar_url: Optional[str] = None
    primary_role: str
    metadata_fields: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class StudentProfileCreate(BaseModel):
    person_id: str
    student_identifier: str
    enrollment_status: str = "enrolled"
    academic_program_id: Optional[str] = None
    department_id: Optional[str] = None
    admission_year: Optional[str] = "2026"
    expected_graduation_year: Optional[str] = "2030"
    gpa: Optional[float] = 3.8
    counselor_person_id: Optional[str] = None
    academic_advisor_person_id: Optional[str] = None


class StudentProfileResponse(BaseModel):
    id: str
    tenant_id: str
    person_id: str
    student_identifier: str
    enrollment_status: str
    academic_program_id: Optional[str] = None
    department_id: Optional[str] = None
    admission_year: Optional[str] = None
    expected_graduation_year: Optional[str] = None
    gpa: Optional[float] = None
    counselor_person_id: Optional[str] = None
    academic_advisor_person_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
