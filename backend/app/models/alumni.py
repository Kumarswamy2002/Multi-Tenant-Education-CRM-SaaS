from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean
from app.models.base import TenantBaseModel


class MentorshipMatch(TenantBaseModel):
    __tablename__ = "mentorship_matches"

    alumni_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    student_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    focus_area = Column(String(100), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="active", nullable=False)  # requested, active, completed, terminated


class AlumniEventRegistration(TenantBaseModel):
    __tablename__ = "alumni_event_registrations"

    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    alumni_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    attendance_status = Column(String(50), default="registered", nullable=False)  # registered, attended, canceled
