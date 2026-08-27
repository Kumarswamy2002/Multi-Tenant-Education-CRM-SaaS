"""
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
