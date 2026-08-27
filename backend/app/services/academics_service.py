"""
Comprehensive Academic Management Service: Courses, Sections, Enrollments, Grades, Transcripts, and Attendance.
"""
from typing import List, Optional, Dict, Any, Tuple
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException, status

from app.models.academics_enterprise import (
    Department, AcademicProgram, AcademicTerm, Course, CourseSection,
    SectionSchedule, StudentEnrollment, AttendanceRecord, CoursePrerequisite,
    EnrollmentStatus, AttendanceStatus, GradeScale
)
from app.schemas.academics_enterprise import (
    DepartmentCreate, DepartmentUpdate, AcademicProgramCreate, AcademicProgramUpdate,
    AcademicTermCreate, AcademicTermUpdate, CourseCreate, CourseUpdate,
    CourseSectionCreate, CourseSectionUpdate, StudentEnrollmentCreate,
    StudentEnrollmentUpdate, AttendanceRecordCreate, BulkAttendanceCreate
)


class AcademicsService:
    def __init__(self, db: Session, tenant_id: str, current_user_id: Optional[str] = None):
        self.db = db
        self.tenant_id = tenant_id
        self.current_user_id = current_user_id

    # --- Department Methods ---
    def create_department(self, data: DepartmentCreate) -> Department:
        existing = self.db.query(Department).filter(
            Department.tenant_id == self.tenant_id,
            Department.code == data.code,
            Department.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Department with code {data.code} already exists")

        dept = Department(
            tenant_id=self.tenant_id,
            created_by_id=self.current_user_id,
            **data.model_dump()
        )
        self.db.add(dept)
        self.db.commit()
        self.db.refresh(dept)
        return dept

    def get_departments(self, skip: int = 0, limit: int = 50, search: Optional[str] = None) -> List[Department]:
        query = self.db.query(Department).filter(
            Department.tenant_id == self.tenant_id,
            Department.is_deleted == False
        )
        if search:
            query = query.filter(
                or_(
                    Department.name.ilike(f"%{search}%"),
                    Department.code.ilike(f"%{search}%")
                )
            )
        return query.offset(skip).limit(limit).all()

    def get_department_by_id(self, department_id: str) -> Department:
        dept = self.db.query(Department).filter(
            Department.tenant_id == self.tenant_id,
            Department.id == department_id,
            Department.is_deleted == False
        ).first()
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return dept

    def update_department(self, department_id: str, data: DepartmentUpdate) -> Department:
        dept = self.get_department_by_id(department_id)
        update_dict = data.model_dump(exclude_unset=True)
        for key, val in update_dict.items():
            setattr(dept, key, val)
        dept.updated_by_id = self.current_user_id
        self.db.commit()
        self.db.refresh(dept)
        return dept

    def delete_department(self, department_id: str) -> None:
        dept = self.get_department_by_id(department_id)
        dept.soft_delete(user_id=self.current_user_id, reason="Admin deleted department")
        self.db.commit()

    # --- Academic Program Methods ---
    def create_program(self, data: AcademicProgramCreate) -> AcademicProgram:
        existing = self.db.query(AcademicProgram).filter(
            AcademicProgram.tenant_id == self.tenant_id,
            AcademicProgram.code == data.code,
            AcademicProgram.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Program with code {data.code} already exists")

        program = AcademicProgram(
            tenant_id=self.tenant_id,
            created_by_id=self.current_user_id,
            **data.model_dump()
        )
        self.db.add(program)
        self.db.commit()
        self.db.refresh(program)
        return program

    def get_programs(self, department_id: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[AcademicProgram]:
        query = self.db.query(AcademicProgram).filter(
            AcademicProgram.tenant_id == self.tenant_id,
            AcademicProgram.is_deleted == False
        )
        if department_id:
            query = query.filter(AcademicProgram.department_id == department_id)
        return query.offset(skip).limit(limit).all()

    # --- Course Catalog Methods ---
    def create_course(self, data: CourseCreate) -> Course:
        existing = self.db.query(Course).filter(
            Course.tenant_id == self.tenant_id,
            Course.code == data.code,
            Course.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Course with code {data.code} already exists")

        course_dict = data.model_dump(exclude={"prerequisite_course_ids"})
        course = Course(
            tenant_id=self.tenant_id,
            created_by_id=self.current_user_id,
            **course_dict
        )
        self.db.add(course)
        self.db.flush()

        for prereq_id in data.prerequisite_course_ids:
            prereq = CoursePrerequisite(
                tenant_id=self.tenant_id,
                course_id=course.id,
                prerequisite_course_id=prereq_id,
                created_by_id=self.current_user_id
            )
            self.db.add(prereq)

        self.db.commit()
        self.db.refresh(course)
        return course

    def get_courses(self, department_id: Optional[str] = None, level: Optional[int] = None, skip: int = 0, limit: int = 50) -> List[Course]:
        query = self.db.query(Course).filter(
            Course.tenant_id == self.tenant_id,
            Course.is_deleted == False
        )
        if department_id:
            query = query.filter(Course.department_id == department_id)
        if level:
            query = query.filter(Course.level == level)
        return query.offset(skip).limit(limit).all()

    # --- Course Sections & Scheduling ---
    def create_section(self, data: CourseSectionCreate) -> CourseSection:
        existing = self.db.query(CourseSection).filter(
            CourseSection.tenant_id == self.tenant_id,
            CourseSection.course_id == data.course_id,
            CourseSection.term_id == data.term_id,
            CourseSection.section_number == data.section_number,
            CourseSection.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Section {data.section_number} already exists for this term")

        section_dict = data.model_dump(exclude={"schedules"})
        section = CourseSection(
            tenant_id=self.tenant_id,
            created_by_id=self.current_user_id,
            **section_dict
        )
        self.db.add(section)
        self.db.flush()

        for sch in data.schedules:
            schedule_row = SectionSchedule(
                tenant_id=self.tenant_id,
                section_id=section.id,
                created_by_id=self.current_user_id,
                **sch.model_dump()
            )
            self.db.add(schedule_row)

        self.db.commit()
        self.db.refresh(section)
        return section

    # --- Student Course Enrollment ---
    def enroll_student(self, data: StudentEnrollmentCreate) -> StudentEnrollment:
        section = self.db.query(CourseSection).filter(
            CourseSection.tenant_id == self.tenant_id,
            CourseSection.id == data.section_id,
            CourseSection.is_deleted == False
        ).first()
        if not section:
            raise HTTPException(status_code=404, detail="Course section not found")

        if section.enrolled_count >= section.capacity:
            if section.waitlist_count < section.waitlist_capacity:
                status_to_assign = EnrollmentStatus.WAITLISTED
                section.waitlist_count += 1
            else:
                raise HTTPException(status_code=400, detail="Course section and waitlist are completely full")
        else:
            status_to_assign = EnrollmentStatus.ENROLLED
            section.enrolled_count += 1

        enrollment = StudentEnrollment(
            tenant_id=self.tenant_id,
            student_id=data.student_id,
            section_id=data.section_id,
            status=status_to_assign,
            created_by_id=self.current_user_id
        )
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    def grade_student(self, enrollment_id: str, letter_grade: str, numeric_score: float, grade_points: float) -> StudentEnrollment:
        enrollment = self.db.query(StudentEnrollment).filter(
            StudentEnrollment.tenant_id == self.tenant_id,
            StudentEnrollment.id == enrollment_id,
            StudentEnrollment.is_deleted == False
        ).first()
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment record not found")

        enrollment.letter_grade = letter_grade
        enrollment.numeric_score = numeric_score
        enrollment.grade_points = grade_points
        enrollment.is_graded = True
        enrollment.status = EnrollmentStatus.COMPLETED if grade_points >= 1.0 else EnrollmentStatus.FAILED
        
        # Pull course credits
        course_credits = enrollment.section.course.credits if enrollment.section and enrollment.section.course else 3.0
        enrollment.credits_earned = course_credits if grade_points >= 1.0 else 0.0

        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment

    # --- Daily Attendance Tracking ---
    def record_bulk_attendance(self, data: BulkAttendanceCreate) -> List[AttendanceRecord]:
        created_records = []
        for item in data.records:
            existing = self.db.query(AttendanceRecord).filter(
                AttendanceRecord.tenant_id == self.tenant_id,
                AttendanceRecord.section_id == data.section_id,
                AttendanceRecord.student_id == item["student_id"],
                AttendanceRecord.session_date == data.session_date,
                AttendanceRecord.is_deleted == False
            ).first()

            if existing:
                existing.status = AttendanceStatus(item.get("status", "present"))
                existing.minutes_late = item.get("minutes_late", 0)
                existing.excuse_reason = item.get("excuse_reason")
                created_records.append(existing)
            else:
                att = AttendanceRecord(
                    tenant_id=self.tenant_id,
                    section_id=data.section_id,
                    student_id=item["student_id"],
                    session_date=data.session_date,
                    status=AttendanceStatus(item.get("status", "present")),
                    minutes_late=item.get("minutes_late", 0),
                    excuse_reason=item.get("excuse_reason"),
                    created_by_id=self.current_user_id
                )
                self.db.add(att)
                created_records.append(att)

        self.db.commit()
        return created_records
