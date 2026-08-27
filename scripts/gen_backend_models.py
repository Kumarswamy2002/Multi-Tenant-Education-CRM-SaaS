"""
Generates complete backend SQLAlchemy models for the Enterprise Multi-Tenant Education CRM SaaS.
"""
import os

def generate_models(base_dir):
    models_dir = os.path.join(base_dir, "backend", "app", "models")
    os.makedirs(models_dir, exist_ok=True)

    # 1. Base Model & Extensions
    base_code = '''"""
Base database models and mixins with multi-tenancy, soft delete, audit, and UUID support.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TimestampMixin:
    """Provides created_at and updated_at timestamps in UTC."""
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:
    """Provides soft-delete capabilities with deletion timestamp and reason."""
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by_id = Column(String(36), nullable=True)
    deletion_reason = Column(String(255), nullable=True)

    def soft_delete(self, user_id: Optional[str] = None, reason: Optional[str] = None) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by_id = user_id
        self.deletion_reason = reason

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_id = None
        self.deletion_reason = None


class TenantAwareMixin:
    """Ensures strict multi-tenant isolation across all university institutions."""
    @declared_attr
    def tenant_id(cls):
        return Column(
            String(36),
            ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )


class AuditMixin:
    """Tracks creating and updating user identities."""
    created_by_id = Column(String(36), nullable=True)
    updated_by_id = Column(String(36), nullable=True)
    version = Column(Integer, default=1, nullable=False)


class CustomFieldsMixin:
    """Supports dynamic EAV / JSONB custom metadata schemas per institution."""
    custom_fields = Column(JSONB, default=dict, nullable=False)
    tags = Column(JSONB, default=list, nullable=False)

    def set_custom_field(self, key: str, value: Any) -> None:
        if self.custom_fields is None:
            self.custom_fields = {}
        fields = dict(self.custom_fields)
        fields[key] = value
        self.custom_fields = fields

    def get_custom_field(self, key: str, default: Any = None) -> Any:
        if not self.custom_fields:
            return default
        return self.custom_fields.get(key, default)


class BaseModel(Base, TimestampMixin, SoftDeleteMixin, TenantAwareMixin, AuditMixin, CustomFieldsMixin):
    """Abstract base class combining multi-tenancy, auditing, soft-delete, and timestamps."""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Serializes standard model columns to a dictionary."""
        result = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if isinstance(val, datetime):
                result[col.name] = val.isoformat()
            else:
                result[col.name] = val
        return result
'''
    with open(os.path.join(models_dir, "base_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(base_code)

    # 2. Academics Models (Programs, Courses, Enrollments, Grades, Timetables, Attendance)
    academics_code = '''"""
Academics, Curriculum, Course Catalog, Enrollment, Gradebook, and Attendance Models.
"""
from datetime import date, time, datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, Date, Time, DateTime,
    ForeignKey, Enum, UniqueConstraint, CheckConstraint, Table
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from backend.app.models.base_enterprise import BaseModel, Base


class ProgramType(str, enum.Enum):
    UNDERGRADUATE = "undergraduate"
    POSTGRADUATE = "postgraduate"
    DOCTORATE = "doctorate"
    DIPLOMA = "diploma"
    CERTIFICATE = "certificate"
    EXECUTIVE = "executive"


class CourseType(str, enum.Enum):
    LECTURE = "lecture"
    LAB = "lab"
    SEMINAR = "seminar"
    STUDIO = "studio"
    INTERNSHIP = "internship"
    DISSERTATION = "dissertation"
    ONLINE = "online"


class GradeScale(str, enum.Enum):
    LETTER_4_0 = "letter_4_0"
    PERCENTAGE_100 = "percentage_100"
    POINTS_10 = "points_10"
    PASS_FAIL = "pass_fail"


class EnrollmentStatus(str, enum.Enum):
    REGISTERED = "registered"
    ENROLLED = "enrolled"
    WAITLISTED = "waitlisted"
    DROPPED = "dropped"
    WITHDRAWN = "withdrawn"
    AUDIT = "audit"
    COMPLETED = "completed"
    FAILED = "failed"


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"
    HALF_DAY = "half_day"


class Department(BaseModel):
    """Academic Department (e.g. Computer Science, Mechanical Engineering)."""
    __tablename__ = "departments"

    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    head_of_department_id = Column(String(36), ForeignKey("persons.id", ondelete="SET NULL"), nullable=True)
    building_location = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    budget_annual = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True, nullable=False)

    programs = relationship("AcademicProgram", back_populates="department", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="department")

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_department_tenant_code"),
    )


class AcademicProgram(BaseModel):
    """Academic Degree / Program (e.g. Bachelor of Science in Computer Science)."""
    __tablename__ = "academic_programs"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    program_type = Column(Enum(ProgramType), default=ProgramType.UNDERGRADUATE, nullable=False)
    duration_years = Column(Float, default=4.0, nullable=False)
    total_credits_required = Column(Integer, default=120, nullable=False)
    degree_awarded = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    grading_scale = Column(Enum(GradeScale), default=GradeScale.LETTER_4_0, nullable=False)
    min_cgpa_for_graduation = Column(Float, default=2.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", back_populates="programs")
    terms = relationship("AcademicTerm", back_populates="program")
    curricula = relationship("CurriculumPlan", back_populates="program")

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_program_tenant_code"),
    )


class AcademicTerm(BaseModel):
    """Academic Term / Semester (e.g. Fall 2026, Spring 2027)."""
    __tablename__ = "academic_terms"

    program_id = Column(String(36), ForeignKey("academic_programs.id", ondelete="CASCADE"), nullable=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)
    academic_year = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    registration_start_date = Column(Date, nullable=True)
    registration_end_date = Column(Date, nullable=True)
    add_drop_deadline = Column(Date, nullable=True)
    withdrawal_deadline = Column(Date, nullable=True)
    grade_submission_deadline = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)

    program = relationship("AcademicProgram", back_populates="terms")
    sections = relationship("CourseSection", back_populates="term")

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_term_tenant_code"),
    )


class Course(BaseModel):
    """Course catalog definition."""
    __tablename__ = "courses"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False)
    code = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Float, default=3.0, nullable=False)
    lecture_hours = Column(Float, default=3.0)
    lab_hours = Column(Float, default=0.0)
    course_type = Column(Enum(CourseType), default=CourseType.LECTURE, nullable=False)
    level = Column(Integer, default=100) # 100, 200, 300, 400
    syllabus_url = Column(String(500), nullable=True)
    learning_outcomes = Column(JSONB, default=list)
    is_repeatable = Column(Boolean, default=False)
    max_repeats = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", back_populates="courses")
    sections = relationship("CourseSection", back_populates="course")
    prerequisites = relationship("CoursePrerequisite", foreign_keys="CoursePrerequisite.course_id", back_populates="course")

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_course_tenant_code"),
    )


class CoursePrerequisite(BaseModel):
    """Prerequisites and corequisites for courses."""
    __tablename__ = "course_prerequisites"

    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    prerequisite_course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    min_grade = Column(String(10), default="C")
    is_corequisite = Column(Boolean, default=False)
    can_be_taken_concurrently = Column(Boolean, default=False)

    course = relationship("Course", foreign_keys=[course_id], back_populates="prerequisites")
    prerequisite_course = relationship("Course", foreign_keys=[prerequisite_course_id])


class CourseSection(BaseModel):
    """Specific section/offering of a course during an academic term."""
    __tablename__ = "course_sections"

    course_id = Column(String(36), ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False)
    term_id = Column(String(36), ForeignKey("academic_terms.id", ondelete="RESTRICT"), nullable=False)
    section_number = Column(String(20), nullable=False)
    instructor_id = Column(String(36), ForeignKey("persons.id", ondelete="SET NULL"), nullable=True)
    capacity = Column(Integer, default=30, nullable=False)
    enrolled_count = Column(Integer, default=0, nullable=False)
    waitlist_capacity = Column(Integer, default=10, nullable=False)
    waitlist_count = Column(Integer, default=0, nullable=False)
    classroom = Column(String(100), nullable=True)
    schedule_summary = Column(String(255), nullable=True) # e.g. Mon, Wed 10:00 - 11:30
    delivery_mode = Column(String(50), default="in_person") # in_person, hybrid, online_async, online_sync
    status = Column(String(50), default="open") # open, closed, cancelled

    course = relationship("Course", back_populates="sections")
    term = relationship("AcademicTerm", back_populates="sections")
    enrollments = relationship("StudentEnrollment", back_populates="section", cascade="all, delete-orphan")
    schedules = relationship("SectionSchedule", back_populates="section", cascade="all, delete-orphan")
    attendance_records = relationship("AttendanceRecord", back_populates="section")

    __table_args__ = (
        UniqueConstraint("tenant_id", "course_id", "term_id", "section_number", name="uq_section_term_course"),
    )


class SectionSchedule(BaseModel):
    """Detailed weekly schedule slot for a section."""
    __tablename__ = "section_schedules"

    section_id = Column(String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0=Monday ... 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_number = Column(String(100), nullable=True)
    building_name = Column(String(100), nullable=True)

    section = relationship("CourseSection", back_populates="schedules")


class StudentEnrollment(BaseModel):
    """Student registration in a course section."""
    __tablename__ = "student_enrollments"

    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    section_id = Column(String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False)
    enrollment_date = Column(Date, default=date.today, nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ENROLLED, nullable=False)
    grade_points = Column(Float, nullable=True)
    letter_grade = Column(String(10), nullable=True)
    numeric_score = Column(Float, nullable=True)
    attendance_percentage = Column(Float, default=100.0)
    credits_earned = Column(Float, default=0.0)
    is_graded = Column(Boolean, default=False)
    remarks = Column(Text, nullable=True)

    section = relationship("CourseSection", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("tenant_id", "student_id", "section_id", name="uq_student_section_enrollment"),
    )


class AttendanceRecord(BaseModel):
    """Daily/Session attendance tracking record."""
    __tablename__ = "attendance_records"

    section_id = Column(String(36), ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    session_date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT, nullable=False)
    minutes_late = Column(Integer, default=0)
    excuse_reason = Column(String(255), nullable=True)
    verified_by_id = Column(String(36), nullable=True)
    biometric_log_id = Column(String(100), nullable=True)

    section = relationship("CourseSection", back_populates="attendance_records")

    __table_args__ = (
        UniqueConstraint("tenant_id", "section_id", "student_id", "session_date", name="uq_attendance_student_session"),
    )


class CurriculumPlan(BaseModel):
    """Structured sequence of recommended courses per semester for a degree."""
    __tablename__ = "curriculum_plans"

    program_id = Column(String(36), ForeignKey("academic_programs.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    effective_year = Column(String(20), nullable=False)
    total_semesters = Column(Integer, default=8, nullable=False)
    plan_matrix = Column(JSONB, default=dict) # {"sem_1": ["CS101", "MATH101"], ...}

    program = relationship("AcademicProgram", back_populates="curricula")
'''
    with open(os.path.join(models_dir, "academics_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(academics_code)

    # 3. Billing, Invoicing, Scholarships, Gateways
    billing_code = '''"""
Tuition Fee Structures, Invoices, Payment Gateways, Scholarships, and Ledger Transactions.
"""
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, Date, DateTime,
    ForeignKey, Enum, UniqueConstraint, Numeric
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from backend.app.models.base_enterprise import BaseModel, Base


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    UPI = "upi"
    ACH = "ach"
    WIRE_TRANSFER = "wire_transfer"
    CHECK = "check"
    CASH = "cash"
    SCHOLARSHIP = "scholarship"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    REFUNDED = "refunded"


class FeeFrequency(str, enum.Enum):
    ONE_TIME = "one_time"
    PER_SEMESTER = "per_semester"
    ANNUAL = "annual"
    MONTHLY = "monthly"
    PER_CREDIT = "per_credit"


class FeeStructure(BaseModel):
    """Institutional Fee Structure (Tuition, Lab, Library, Hostel, Transport, Tech fees)."""
    __tablename__ = "fee_structures"

    program_id = Column(String(36), ForeignKey("academic_programs.id", ondelete="CASCADE"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    fee_frequency = Column(Enum(FeeFrequency), default=FeeFrequency.PER_SEMESTER, nullable=False)
    due_day_offset = Column(Integer, default=30)
    is_active = Column(Boolean, default=True, nullable=False)

    fee_items = relationship("FeeStructureItem", back_populates="fee_structure", cascade="all, delete-orphan")
    invoices = relationship("StudentInvoice", back_populates="fee_structure")


class FeeStructureItem(BaseModel):
    """Individual breakdown component within a fee structure."""
    __tablename__ = "fee_structure_items"

    fee_structure_id = Column(String(36), ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False) # Tuition, Lab, Sports, Insurance, Campus Facility
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    is_refundable = Column(Boolean, default=False)
    tax_rate_percent = Column(Float, default=0.0)

    fee_structure = relationship("FeeStructure", back_populates="fee_items")


class StudentInvoice(BaseModel):
    """Invoice billed to a student for academic terms or incidental fees."""
    __tablename__ = "student_invoices"

    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    fee_structure_id = Column(String(36), ForeignKey("fee_structures.id", ondelete="SET NULL"), nullable=True)
    term_id = Column(String(36), ForeignKey("academic_terms.id", ondelete="SET NULL"), nullable=True)
    invoice_number = Column(String(100), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    subtotal_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    paid_amount = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.ISSUED, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    late_fee_applied = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

    fee_structure = relationship("FeeStructure", back_populates="invoices")
    line_items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("PaymentTransaction", back_populates="invoice")

    __table_args__ = (
        UniqueConstraint("tenant_id", "invoice_number", name="uq_invoice_tenant_number"),
    )


class InvoiceLineItem(BaseModel):
    """Line item in a student invoice."""
    __tablename__ = "invoice_line_items"

    invoice_id = Column(String(36), ForeignKey("student_invoices.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(255), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, nullable=False)
    tax_percent = Column(Float, default=0.0)

    invoice = relationship("StudentInvoice", back_populates="line_items")


class PaymentTransaction(BaseModel):
    """Payment transaction processed via payment gateway or manual cashier."""
    __tablename__ = "payment_transactions"

    invoice_id = Column(String(36), ForeignKey("student_invoices.id", ondelete="CASCADE"), nullable=True)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    transaction_reference = Column(String(150), nullable=False)
    gateway_name = Column(String(50), nullable=False) # Stripe, Razorpay, PayPal, Cashier
    gateway_transaction_id = Column(String(200), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CREDIT_CARD, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.COMPLETED, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    gateway_fee = Column(Float, default=0.0)
    gateway_response = Column(JSONB, default=dict)
    receipt_url = Column(String(500), nullable=True)
    failure_reason = Column(String(255), nullable=True)

    invoice = relationship("StudentInvoice", back_populates="payments")


class Scholarship(BaseModel):
    """Financial Aid, Merit Grants, Endowments, and Tuition Waivers."""
    __tablename__ = "scholarships"

    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    donor_name = Column(String(200), nullable=True)
    total_endowment = Column(Float, default=0.0)
    amount_per_recipient = Column(Float, nullable=False)
    is_percentage_waiver = Column(Boolean, default=False)
    waiver_percentage = Column(Float, default=0.0)
    min_cgpa_requirement = Column(Float, default=3.0)
    eligibility_criteria = Column(JSONB, default=dict)
    max_recipients = Column(Integer, default=50)
    active_year = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    awards = relationship("ScholarshipAward", back_populates="scholarship")


class ScholarshipAward(BaseModel):
    """Scholarship awarded to a student."""
    __tablename__ = "scholarship_awards"

    scholarship_id = Column(String(36), ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(String(36), ForeignKey("academic_terms.id", ondelete="SET NULL"), nullable=True)
    awarded_amount = Column(Float, nullable=False)
    disbursement_date = Column(Date, default=date.today, nullable=False)
    status = Column(String(50), default="approved") # approved, disbursed, revoked

    scholarship = relationship("Scholarship", back_populates="awards")
'''
    with open(os.path.join(models_dir, "billing_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(billing_code)

    # 4. Career, Placements, Jobs, Mentorship
    career_code = '''"""
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
'''
    with open(os.path.join(models_dir, "career_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(career_code)

    # 5. Hostel, Facilities, Library, Transport
    campus_ops_code = '''"""
Campus Operations Models: Hostel Accommodation, Library Catalog, and Fleet Transport.
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


class RoomType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    DORMITORY = "dormitory"


class HostelBuilding(BaseModel):
    """Hostel / Dormitory Hall of Residence."""
    __tablename__ = "hostel_buildings"

    name = Column(String(150), nullable=False)
    code = Column(String(50), nullable=False)
    gender_type = Column(String(50), default="co-ed") # male, female, co-ed
    warden_name = Column(String(150), nullable=True)
    warden_contact = Column(String(50), nullable=True)
    total_floors = Column(Integer, default=4)
    total_rooms = Column(Integer, default=100)
    amenities = Column(JSONB, default=list) # ["WiFi", "Laundry", "Gym", "Mess"]

    rooms = relationship("HostelRoom", back_populates="building", cascade="all, delete-orphan")


class HostelRoom(BaseModel):
    """Room inside a hostel building."""
    __tablename__ = "hostel_rooms"

    building_id = Column(String(36), ForeignKey("hostel_buildings.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(50), nullable=False)
    floor_number = Column(Integer, default=1)
    room_type = Column(Enum(RoomType), default=RoomType.DOUBLE, nullable=False)
    capacity = Column(Integer, default=2, nullable=False)
    occupied_count = Column(Integer, default=0, nullable=False)
    monthly_rent = Column(Float, default=500.0)
    has_attached_bath = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    building = relationship("HostelBuilding", back_populates="rooms")
    allocations = relationship("BedAllocation", back_populates="room")


class BedAllocation(BaseModel):
    """Student bed allocation in a hostel room."""
    __tablename__ = "bed_allocations"

    room_id = Column(String(36), ForeignKey("hostel_rooms.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    bed_number = Column(String(20), nullable=False)
    start_date = Column(Date, default=date.today, nullable=False)
    end_date = Column(Date, nullable=True)
    is_vacated = Column(Boolean, default=False)

    room = relationship("HostelRoom", back_populates="allocations")


class LibraryBook(BaseModel):
    """Library book catalog item."""
    __tablename__ = "library_books"

    isbn = Column(String(50), nullable=False)
    title = Column(String(300), nullable=False)
    author = Column(String(255), nullable=False)
    publisher = Column(String(200), nullable=True)
    edition = Column(String(50), nullable=True)
    publication_year = Column(Integer, nullable=True)
    genre = Column(String(100), nullable=True)
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    shelf_location = Column(String(100), nullable=True)

    issues = relationship("BookIssue", back_populates="book")


class BookIssue(BaseModel):
    """Borrowing record for a library book."""
    __tablename__ = "book_issues"

    book_id = Column(String(36), ForeignKey("library_books.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    fine_amount = Column(Float, default=0.0)
    status = Column(String(50), default="issued") # issued, returned, lost, overdue

    book = relationship("LibraryBook", back_populates="issues")


class TransportRoute(BaseModel):
    """Campus shuttle / bus transit route."""
    __tablename__ = "transport_routes"

    route_name = Column(String(150), nullable=False)
    route_code = Column(String(50), nullable=False)
    vehicle_number = Column(String(50), nullable=False)
    driver_name = Column(String(150), nullable=True)
    driver_contact = Column(String(50), nullable=True)
    total_capacity = Column(Integer, default=40)
    stops = Column(JSONB, default=list) # [{"stop_name": "Downtown", "time": "07:30 AM", "lat": 0, "lng": 0}]
'''
    with open(os.path.join(models_dir, "campus_ops_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(campus_ops_code)

    # 6. AI, Predictive Models, Lead Scoring, Workflows
    ai_workflows_code = '''"""
AI Engine, Retention Prediction Models, Lead Scoring Algorithms, and Automated Workflows.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, DateTime,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from backend.app.models.base_enterprise import BaseModel, Base


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StudentRetentionRisk(BaseModel):
    """AI Early-Warning & Dropout Risk Assessment for Enrolled Students."""
    __tablename__ = "student_retention_risks"

    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    risk_score = Column(Float, nullable=False) # 0.0 to 100.0
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW, nullable=False)
    academic_risk_factor = Column(Float, default=0.0) # GPA trend, failed assignments
    attendance_risk_factor = Column(Float, default=0.0) # Low presence rate
    financial_risk_factor = Column(Float, default=0.0) # Overdue unpaid invoices
    engagement_risk_factor = Column(Float, default=0.0) # LMS inactivity
    contributing_factors = Column(JSONB, default=list)
    recommended_interventions = Column(JSONB, default=list) # ["Assign Academic Tutor", "Counselor Check-in"]
    assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)


class LeadScoreProfile(BaseModel):
    """AI Propensity & Conversion Scoring for Prospective Admission Leads."""
    __tablename__ = "lead_score_profiles"

    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    propensity_score = Column(Float, nullable=False) # 0.0 to 100.0
    conversion_tier = Column(String(50), default="Warm") # Hot, Warm, Cold
    engagement_frequency_score = Column(Float, default=0.0)
    profile_fit_score = Column(Float, default=0.0)
    preferred_channel = Column(String(50), default="email") # email, whatsapp, call
    optimal_contact_time = Column(String(100), default="Evening (4 PM - 7 PM)")
    signals = Column(JSONB, default=list)
    last_scored_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowAutomation(BaseModel):
    """Event-driven automation rules (e.g. On Lead Stage Change -> Send WhatsApp + Task to Counselor)."""
    __tablename__ = "workflow_automations"

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    trigger_event = Column(String(100), nullable=False) # lead_created, application_submitted, invoice_overdue
    conditions = Column(JSONB, default=list) # [{"field": "status", "operator": "eq", "value": "interested"}]
    actions = Column(JSONB, default=list) # [{"type": "send_email", "template_id": "welcome_1"}, {"type": "create_task"}]
    is_active = Column(Boolean, default=True, nullable=False)
    execution_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime, nullable=True)


class WorkflowExecutionLog(BaseModel):
    """Execution audit trail for workflow runs."""
    __tablename__ = "workflow_execution_logs"

    workflow_id = Column(String(36), ForeignKey("workflow_automations.id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String(100), nullable=False) # lead, student, invoice
    entity_id = Column(String(36), nullable=False)
    status = Column(String(50), default="success") # success, failed, skipped
    execution_duration_ms = Column(Float, default=0.0)
    log_details = Column(JSONB, default=dict)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
'''
    with open(os.path.join(models_dir, "ai_workflows_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(ai_workflows_code)

    print("Generated enterprise database models successfully.")

if __name__ == "__main__":
    generate_models(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
