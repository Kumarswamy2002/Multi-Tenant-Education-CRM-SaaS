"""
Career Services, Campus Recruitment Drives, Job Postings, and Placement Tracking.
"""
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, Date, DateTime,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from backend.app.models.base_enterprise import BaseModel, Base


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CO_OP = "co_op"
    CONTRACT = "contract"


class JobApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    ASSESSMENT = "assessment"
    INTERVIEW_ROUND_1 = "interview_round_1"
    INTERVIEW_ROUND_2 = "interview_round_2"
    HR_ROUND = "hr_round"
    OFFER_EXTENDED = "offer_extended"
    OFFER_ACCEPTED = "offer_accepted"
    OFFER_DECLINED = "offer_declined"
    REJECTED = "rejected"


class EmployerCompany(BaseModel):
    """Recruiting company / corporate partner."""
    __tablename__ = "employer_companies"

    company_name = Column(String(200), nullable=False)
    industry = Column(String(100), nullable=False)
    website = Column(String(255), nullable=True)
    headquarters = Column(String(200), nullable=True)
    contact_person_name = Column(String(150), nullable=False)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=True)
    tier = Column(String(50), default="Tier 1") # Tier 1, Tier 2, Dream, Super Dream
    logo_url = Column(String(500), nullable=True)
    is_verified = Column(Boolean, default=True)

    job_postings = relationship("JobPosting", back_populates="company", cascade="all, delete-orphan")
    drives = relationship("CampusPlacementDrive", back_populates="company")


class JobPosting(BaseModel):
    """Job and internship listing published for university students."""
    __tablename__ = "job_postings"

    company_id = Column(String(36), ForeignKey("employer_companies.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    job_type = Column(Enum(JobType), default=JobType.FULL_TIME, nullable=False)
    locations = Column(JSONB, default=list) # ["New York, NY", "Remote"]
    ctc_annual_salary = Column(Float, nullable=True)
    stipend_monthly = Column(Float, nullable=True)
    min_cgpa = Column(Float, default=0.0)
    eligible_departments = Column(JSONB, default=list) # ["CS", "ECE", "ME"]
    required_skills = Column(JSONB, default=list)
    description = Column(Text, nullable=False)
    application_deadline = Column(Date, nullable=False)
    openings_count = Column(Integer, default=1)
    status = Column(String(50), default="active") # active, closed, draft

    company = relationship("EmployerCompany", back_populates="job_postings")
    applications = relationship("JobApplication", back_populates="job_posting", cascade="all, delete-orphan")


class JobApplication(BaseModel):
    """Student application for a campus job or internship."""
    __tablename__ = "job_applications"

    job_posting_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    resume_url = Column(String(500), nullable=True)
    cover_letter = Column(Text, nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(JobApplicationStatus), default=JobApplicationStatus.APPLIED, nullable=False)
    current_round = Column(String(100), default="Application Review")
    feedback_notes = Column(Text, nullable=True)
    offered_ctc = Column(Float, nullable=True)
    offer_letter_url = Column(String(500), nullable=True)

    job_posting = relationship("JobPosting", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("tenant_id", "job_posting_id", "student_id", name="uq_job_student_application"),
    )


class CampusPlacementDrive(BaseModel):
    """Coordinated on-campus / virtual recruitment event."""
    __tablename__ = "campus_placement_drives"

    company_id = Column(String(36), ForeignKey("employer_companies.id", ondelete="CASCADE"), nullable=False)
    academic_year = Column(String(20), nullable=False)
    drive_title = Column(String(255), nullable=False)
    drive_date = Column(Date, nullable=False)
    venue = Column(String(200), default="Main Auditorium / Online")
    rounds_structure = Column(JSONB, default=list) # ["Aptitude Test", "Technical Interview", "HR Interview"]
    coordinator_name = Column(String(150), nullable=True)
    status = Column(String(50), default="scheduled") # scheduled, ongoing, completed

    company = relationship("EmployerCompany", back_populates="drives")
