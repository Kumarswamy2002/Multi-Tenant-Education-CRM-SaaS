from sqlalchemy import Column, String, Date, JSON, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import TenantBaseModel


class Person(TenantBaseModel):
    __tablename__ = "people"

    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True, index=True)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    nationality = Column(String(100), nullable=True)
    address = Column(JSON, default=dict, nullable=False)
    avatar_url = Column(String(500), nullable=True)
    primary_role = Column(String(50), default="prospect", nullable=False)  # prospect, applicant, student, parent, counselor, faculty, alumni, recruiter
    metadata_fields = Column(JSON, default=dict, nullable=False)


class StudentProfile(TenantBaseModel):
    __tablename__ = "student_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    student_identifier = Column(String(50), index=True, nullable=False)  # University Student ID
    enrollment_status = Column(String(50), default="enrolled", nullable=False)  # enrolled, active, suspended, graduated, withdrawn
    academic_program_id = Column(String(36), ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    admission_year = Column(String(10), nullable=True)
    expected_graduation_year = Column(String(10), nullable=True)
    gpa = Column(Float, nullable=True)
    counselor_person_id = Column(String(36), ForeignKey("people.id", ondelete="SET NULL"), nullable=True)
    academic_advisor_person_id = Column(String(36), ForeignKey("people.id", ondelete="SET NULL"), nullable=True)


class ParentProfile(TenantBaseModel):
    __tablename__ = "parent_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    occupation = Column(String(100), nullable=True)
    employer = Column(String(100), nullable=True)
    preferred_communication_channel = Column(String(50), default="email", nullable=False)


class ApplicantProfile(TenantBaseModel):
    __tablename__ = "applicant_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    target_program_id = Column(String(36), ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    entry_term = Column(String(50), nullable=True)  # Fall 2026, Spring 2027
    highest_qualification = Column(String(100), nullable=True)
    gpa_score = Column(Float, nullable=True)
    test_scores = Column(JSON, default=dict, nullable=False)  # SAT, GRE, GMAT, TOEFL, IELTS
    counselor_person_id = Column(String(36), ForeignKey("people.id", ondelete="SET NULL"), nullable=True)


class CounselorProfile(TenantBaseModel):
    __tablename__ = "counselor_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    assigned_lead_capacity = Column(String(50), default="100", nullable=False)
    specialties = Column(JSON, default=list, nullable=False)


class FacultyProfile(TenantBaseModel):
    __tablename__ = "faculty_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(100), nullable=True)  # Professor, Associate Professor, Lecturer
    office_location = Column(String(100), nullable=True)


class AlumniProfile(TenantBaseModel):
    __tablename__ = "alumni_profiles"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), unique=True, nullable=False)
    graduation_year = Column(String(10), nullable=False)
    program_graduated_id = Column(String(36), ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    current_company = Column(String(100), nullable=True)
    current_title = Column(String(100), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    willing_to_mentor = Column(Boolean, default=True, nullable=False)
