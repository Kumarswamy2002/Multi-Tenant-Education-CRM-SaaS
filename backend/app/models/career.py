from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean
from app.models.base import TenantBaseModel


class Skill(TenantBaseModel):
    __tablename__ = "skills"

    name = Column(String(100), index=True, nullable=False)
    category = Column(String(50), nullable=False)  # technical, soft_skill, language, certification


class CareerProfile(TenantBaseModel):
    __tablename__ = "career_profiles"

    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    headline = Column(String(255), nullable=True)
    resume_url = Column(String(500), nullable=True)
    skills = Column(JSON, default=list, nullable=False)
    preferred_locations = Column(JSON, default=list, nullable=False)
    preferred_roles = Column(JSON, default=list, nullable=False)
    is_seeking_employment = Column(Boolean, default=True, nullable=False)


class JobPosting(TenantBaseModel):
    __tablename__ = "job_postings"

    employer_organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    job_type = Column(String(50), nullable=False)  # full_time, part_time, internship, contract
    location = Column(String(255), nullable=False)
    salary_range = Column(String(100), nullable=True)
    description = Column(String(2000), nullable=False)
    requirements = Column(JSON, default=list, nullable=False)
    status = Column(String(50), default="active", nullable=False)  # active, closed, draft
    application_deadline = Column(DateTime(timezone=True), nullable=True)


class JobApplication(TenantBaseModel):
    __tablename__ = "job_applications"

    job_posting_id = Column(String(36), ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False)
    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="APPLIED", nullable=False)  # APPLIED, SCREENING, INTERVIEWING, OFFERED, REJECTED, ACCEPTED
    resume_version_url = Column(String(500), nullable=True)
    cover_letter = Column(String(2000), nullable=True)


class JobInterview(TenantBaseModel):
    __tablename__ = "job_interviews"

    job_application_id = Column(String(36), ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False)
    interview_type = Column(String(50), nullable=False)  # technical, HR, final
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    location_or_url = Column(String(500), nullable=True)
    feedback = Column(String(2000), nullable=True)
    status = Column(String(50), default="scheduled", nullable=False)


class JobOffer(TenantBaseModel):
    __tablename__ = "job_offers"

    job_application_id = Column(String(36), ForeignKey("job_applications.id", ondelete="CASCADE"), nullable=False)
    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    offer_salary = Column(String(100), nullable=False)
    joining_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="OFFERED", nullable=False)  # OFFERED, ACCEPTED, DECLINED
