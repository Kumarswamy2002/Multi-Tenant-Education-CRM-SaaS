"""
Generates complete Pydantic v2 schemas and DTOs for the Enterprise Multi-Tenant Education CRM SaaS.
"""
import os

def generate_schemas(base_dir):
    schemas_dir = os.path.join(base_dir, "backend", "app", "schemas")
    os.makedirs(schemas_dir, exist_ok=True)

    # 1. Base Schemas
    base_schemas = '''"""
Base Pydantic Schemas with generic responses, pagination, filtering, and audit fields.
"""
from typing import Generic, TypeVar, Optional, List, Any, Dict
from datetime import datetime, date, time
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class AuditSchema(TimestampSchema):
    id: str
    tenant_id: str
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by_id: Optional[str] = None
    updated_by_id: Optional[str] = None
    version: int = 1
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class APIResponse(BaseSchema, Generic[T]):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None
    error_code: Optional[str] = None
'''
    with open(os.path.join(schemas_dir, "base_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(base_schemas)

    # 2. Academics Schemas
    academics_schemas = '''"""
Pydantic Schemas for Academics, Programs, Courses, Sections, Enrollments, Grades, and Attendance.
"""
from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from pydantic import Field
from backend.app.schemas.base_enterprise import BaseSchema, AuditSchema
from backend.app.models.academics_enterprise import ProgramType, CourseType, GradeScale, EnrollmentStatus, AttendanceStatus


# Department Schemas
class DepartmentBase(BaseSchema):
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    head_of_department_id: Optional[str] = None
    building_location: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    budget_annual: float = 0.0
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseSchema):
    name: Optional[str] = None
    head_of_department_id: Optional[str] = None
    building_location: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    budget_annual: Optional[float] = None
    is_active: Optional[bool] = None


class DepartmentRead(DepartmentBase, AuditSchema):
    pass


# Academic Program Schemas
class AcademicProgramBase(BaseSchema):
    department_id: str
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    program_type: ProgramType = ProgramType.UNDERGRADUATE
    duration_years: float = 4.0
    total_credits_required: int = 120
    degree_awarded: str
    description: Optional[str] = None
    grading_scale: GradeScale = GradeScale.LETTER_4_0
    min_cgpa_for_graduation: float = 2.0
    is_active: bool = True


class AcademicProgramCreate(AcademicProgramBase):
    pass


class AcademicProgramUpdate(BaseSchema):
    name: Optional[str] = None
    duration_years: Optional[float] = None
    total_credits_required: Optional[int] = None
    description: Optional[str] = None
    min_cgpa_for_graduation: Optional[float] = None
    is_active: Optional[bool] = None


class AcademicProgramRead(AcademicProgramBase, AuditSchema):
    department_name: Optional[str] = None


# Academic Term Schemas
class AcademicTermBase(BaseSchema):
    program_id: Optional[str] = None
    name: str
    code: str
    academic_year: str
    start_date: date
    end_date: date
    registration_start_date: Optional[date] = None
    registration_end_date: Optional[date] = None
    add_drop_deadline: Optional[date] = None
    withdrawal_deadline: Optional[date] = None
    grade_submission_deadline: Optional[date] = None
    is_current: bool = False
    is_closed: bool = False


class AcademicTermCreate(AcademicTermBase):
    pass


class AcademicTermUpdate(BaseSchema):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    is_closed: Optional[bool] = None


class AcademicTermRead(AcademicTermBase, AuditSchema):
    pass


# Course Schemas
class CourseBase(BaseSchema):
    department_id: str
    code: str
    title: str
    description: Optional[str] = None
    credits: float = 3.0
    lecture_hours: float = 3.0
    lab_hours: float = 0.0
    course_type: CourseType = CourseType.LECTURE
    level: int = 100
    syllabus_url: Optional[str] = None
    learning_outcomes: List[str] = Field(default_factory=list)
    is_repeatable: bool = False
    max_repeats: int = 0
    is_active: bool = True


class CourseCreate(CourseBase):
    prerequisite_course_ids: List[str] = Field(default_factory=list)


class CourseUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[float] = None
    lecture_hours: Optional[float] = None
    lab_hours: Optional[float] = None
    syllabus_url: Optional[str] = None
    is_active: Optional[bool] = None


class CourseRead(CourseBase, AuditSchema):
    department_code: Optional[str] = None


# Course Section Schemas
class SectionScheduleSchema(BaseSchema):
    day_of_week: int
    start_time: time
    end_time: time
    room_number: Optional[str] = None
    building_name: Optional[str] = None


class CourseSectionBase(BaseSchema):
    course_id: str
    term_id: str
    section_number: str
    instructor_id: Optional[str] = None
    capacity: int = 30
    waitlist_capacity: int = 10
    classroom: Optional[str] = None
    schedule_summary: Optional[str] = None
    delivery_mode: str = "in_person"
    status: str = "open"


class CourseSectionCreate(CourseSectionBase):
    schedules: List[SectionScheduleSchema] = Field(default_factory=list)


class CourseSectionUpdate(BaseSchema):
    instructor_id: Optional[str] = None
    capacity: Optional[int] = None
    classroom: Optional[str] = None
    status: Optional[str] = None


class CourseSectionRead(CourseSectionBase, AuditSchema):
    enrolled_count: int
    waitlist_count: int
    course_title: Optional[str] = None
    course_code: Optional[str] = None
    instructor_name: Optional[str] = None


# Student Enrollment Schemas
class StudentEnrollmentCreate(BaseSchema):
    student_id: str
    section_id: str


class StudentEnrollmentUpdate(BaseSchema):
    status: Optional[EnrollmentStatus] = None
    grade_points: Optional[float] = None
    letter_grade: Optional[str] = None
    numeric_score: Optional[float] = None
    remarks: Optional[str] = None


class StudentEnrollmentRead(AuditSchema):
    student_id: str
    section_id: str
    enrollment_date: date
    status: EnrollmentStatus
    grade_points: Optional[float] = None
    letter_grade: Optional[str] = None
    numeric_score: Optional[float] = None
    attendance_percentage: float
    credits_earned: float
    is_graded: bool
    remarks: Optional[str] = None
    course_code: Optional[str] = None
    course_title: Optional[str] = None


# Attendance Record Schemas
class AttendanceRecordCreate(BaseSchema):
    section_id: str
    student_id: str
    session_date: date
    status: AttendanceStatus = AttendanceStatus.PRESENT
    minutes_late: int = 0
    excuse_reason: Optional[str] = None


class BulkAttendanceCreate(BaseSchema):
    section_id: str
    session_date: date
    records: List[Dict[str, Any]] # [{"student_id": "...", "status": "present", "minutes_late": 0}]


class AttendanceRecordRead(AuditSchema):
    section_id: str
    student_id: str
    session_date: date
    status: AttendanceStatus
    minutes_late: int
    excuse_reason: Optional[str] = None
    student_name: Optional[str] = None
'''
    with open(os.path.join(schemas_dir, "academics_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(academics_schemas)

    # 3. Billing Schemas
    billing_schemas = '''"""
Pydantic Schemas for Tuition Billing, Fee Structures, Invoices, Payments, and Scholarships.
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import Field
from backend.app.schemas.base_enterprise import BaseSchema, AuditSchema
from backend.app.models.billing_enterprise import InvoiceStatus, PaymentMethod, TransactionStatus, FeeFrequency


class FeeStructureItemSchema(BaseSchema):
    category: str
    description: str
    amount: float
    is_mandatory: bool = True
    is_refundable: bool = False
    tax_rate_percent: float = 0.0


class FeeStructureCreate(BaseSchema):
    program_id: Optional[str] = None
    academic_year: str
    name: str
    code: str
    currency: str = "USD"
    fee_frequency: FeeFrequency = FeeFrequency.PER_SEMESTER
    due_day_offset: int = 30
    items: List[FeeStructureItemSchema] = Field(default_factory=list)


class FeeStructureRead(AuditSchema):
    program_id: Optional[str] = None
    academic_year: str
    name: str
    code: str
    currency: str
    total_amount: float
    fee_frequency: FeeFrequency
    due_day_offset: int
    is_active: bool
    fee_items: List[FeeStructureItemSchema] = Field(default_factory=list)


class InvoiceLineItemSchema(BaseSchema):
    description: str
    unit_price: float
    quantity: int = 1
    total_price: float
    tax_percent: float = 0.0


class StudentInvoiceCreate(BaseSchema):
    student_id: str
    fee_structure_id: Optional[str] = None
    term_id: Optional[str] = None
    due_date: date
    line_items: List[InvoiceLineItemSchema]
    discount_amount: float = 0.0
    notes: Optional[str] = None


class StudentInvoiceRead(AuditSchema):
    student_id: str
    fee_structure_id: Optional[str] = None
    term_id: Optional[str] = None
    invoice_number: str
    issue_date: date
    due_date: date
    subtotal_amount: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance_amount: float
    status: InvoiceStatus
    currency: str
    late_fee_applied: float
    notes: Optional[str] = None
    line_items: List[InvoiceLineItemSchema] = Field(default_factory=list)
    student_name: Optional[str] = None


class PaymentTransactionCreate(BaseSchema):
    invoice_id: Optional[str] = None
    student_id: str
    amount: float
    currency: str = "USD"
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    gateway_name: str = "Stripe"
    gateway_transaction_id: Optional[str] = None
    notes: Optional[str] = None


class PaymentTransactionRead(AuditSchema):
    invoice_id: Optional[str] = None
    student_id: str
    transaction_reference: str
    gateway_name: str
    gateway_transaction_id: Optional[str] = None
    amount: float
    currency: str
    payment_method: PaymentMethod
    status: TransactionStatus
    payment_date: datetime
    gateway_fee: float
    receipt_url: Optional[str] = None
    failure_reason: Optional[str] = None


class ScholarshipCreate(BaseSchema):
    name: str
    code: str
    donor_name: Optional[str] = None
    total_endowment: float = 0.0
    amount_per_recipient: float
    is_percentage_waiver: bool = False
    waiver_percentage: float = 0.0
    min_cgpa_requirement: float = 3.0
    eligibility_criteria: Dict[str, Any] = Field(default_factory=dict)
    max_recipients: int = 50
    active_year: str


class ScholarshipRead(AuditSchema):
    name: str
    code: str
    donor_name: Optional[str] = None
    total_endowment: float
    amount_per_recipient: float
    is_percentage_waiver: bool
    waiver_percentage: float
    min_cgpa_requirement: float
    eligibility_criteria: Dict[str, Any]
    max_recipients: int
    active_year: str
    is_active: bool
'''
    with open(os.path.join(schemas_dir, "billing_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(billing_schemas)

    # 4. Career, AI, Workflows Schemas
    other_schemas = '''"""
Pydantic Schemas for Career Services, AI Retention/Scoring, and Workflow Automations.
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import Field
from backend.app.schemas.base_enterprise import BaseSchema, AuditSchema
from backend.app.models.career_enterprise import JobType, JobApplicationStatus
from backend.app.models.ai_workflows_enterprise import RiskLevel


# Career & Jobs
class JobPostingCreate(BaseSchema):
    company_id: str
    title: str
    job_type: JobType = JobType.FULL_TIME
    locations: List[str] = Field(default_factory=list)
    ctc_annual_salary: Optional[float] = None
    stipend_monthly: Optional[float] = None
    min_cgpa: float = 0.0
    eligible_departments: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    description: str
    application_deadline: date
    openings_count: int = 1


class JobPostingRead(AuditSchema):
    company_id: str
    company_name: Optional[str] = None
    title: str
    job_type: JobType
    locations: List[str]
    ctc_annual_salary: Optional[float] = None
    stipend_monthly: Optional[float] = None
    min_cgpa: float
    eligible_departments: List[str]
    required_skills: List[str]
    description: str
    application_deadline: date
    openings_count: int
    status: str


class JobApplicationCreate(BaseSchema):
    job_posting_id: str
    student_id: str
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None


class JobApplicationRead(AuditSchema):
    job_posting_id: str
    student_id: str
    student_name: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    resume_url: Optional[str] = None
    applied_at: datetime
    status: JobApplicationStatus
    current_round: str
    feedback_notes: Optional[str] = None
    offered_ctc: Optional[float] = None


# AI & Predictions
class StudentRetentionRiskRead(AuditSchema):
    student_id: str
    student_name: Optional[str] = None
    risk_score: float
    risk_level: RiskLevel
    academic_risk_factor: float
    attendance_risk_factor: float
    financial_risk_factor: float
    engagement_risk_factor: float
    contributing_factors: List[str]
    recommended_interventions: List[str]
    assessed_at: datetime
    is_resolved: bool
    resolution_notes: Optional[str] = None


class LeadScoreProfileRead(AuditSchema):
    lead_id: str
    propensity_score: float
    conversion_tier: str
    engagement_frequency_score: float
    profile_fit_score: float
    preferred_channel: str
    optimal_contact_time: str
    signals: List[str]
    last_scored_at: datetime


# Workflow Automations
class WorkflowAutomationCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    is_active: bool = True


class WorkflowAutomationRead(AuditSchema):
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    is_active: bool
    execution_count: int
    last_triggered_at: Optional[datetime] = None
'''
    with open(os.path.join(schemas_dir, "career_ai_workflows_enterprise.py"), "w", encoding="utf-8") as f:
        f.write(other_schemas)

    print("Generated enterprise schemas successfully.")

if __name__ == "__main__":
    generate_schemas(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
