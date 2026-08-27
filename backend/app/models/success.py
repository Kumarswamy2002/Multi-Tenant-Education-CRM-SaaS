from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Float
from app.models.base import TenantBaseModel


class StudentGoal(TenantBaseModel):
    __tablename__ = "student_goals"

    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # academic, career, skill, personal
    target_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="in_progress", nullable=False)  # in_progress, achieved, missed


class SuccessPlan(TenantBaseModel):
    __tablename__ = "success_plans"

    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    advisor_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    risk_level = Column(String(20), default="low", nullable=False)  # low, medium, high, critical
    risk_indicators = Column(JSON, default=list, nullable=False)
    status = Column(String(50), default="active", nullable=False)


class ProgressMilestone(TenantBaseModel):
    __tablename__ = "progress_milestones"

    plan_id = Column(String(36), ForeignKey("success_plans.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    is_completed = Column(String(50), default="pending", nullable=False)


class AdvisorIntervention(TenantBaseModel):
    __tablename__ = "advisor_interventions"

    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    advisor_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    intervention_type = Column(String(50), nullable=False)  # academic_warning, counseling_referral, tutoring, attendance_flag
    notes = Column(String(2000), nullable=False)
    outcome = Column(String(1000), nullable=True)
