"""
Pydantic Schemas for Academics, Programs, Courses, Sections, Enrollments, Grades, and Attendance.
"""
from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from pydantic import Field
from app.schemas.base_enterprise import BaseSchema, AuditSchema
from app.models.academics_enterprise import ProgramType, CourseType, GradeScale, EnrollmentStatus, AttendanceStatus


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
