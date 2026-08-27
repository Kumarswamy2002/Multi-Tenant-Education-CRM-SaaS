from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey, Boolean, Integer
from app.models.base import TenantBaseModel


class LeadSource(TenantBaseModel):
    __tablename__ = "lead_sources"

    name = Column(String(100), nullable=False)
    channel = Column(String(50), nullable=False)  # website, social, event, referral, ad_campaign, partner
    description = Column(String(255), nullable=True)


class Lead(TenantBaseModel):
    __tablename__ = "leads"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="NEW", index=True, nullable=False)  # NEW, CONTACTED, QUALIFIED, COUNSELING, APPLICATION, CONVERTED, DISQUALIFIED
    stage = Column(String(50), default="prospecting", nullable=False)
    lead_source_id = Column(String(36), ForeignKey("lead_sources.id", ondelete="SET NULL"), nullable=True)
    assigned_counselor_person_id = Column(String(36), ForeignKey("people.id", ondelete="SET NULL"), nullable=True)
    score = Column(Float, default=0.0, nullable=False)
    academic_interest_program_id = Column(String(36), ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    custom_fields = Column(JSON, default=dict, nullable=False)


class Activity(TenantBaseModel):
    __tablename__ = "activities"

    person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # call, email, meeting, note, task, counseling_session
    subject = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    status = Column(String(50), default="completed", nullable=False)  # scheduled, completed, canceled
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    performed_by_person_id = Column(String(36), nullable=True)


class Case(TenantBaseModel):
    __tablename__ = "cases"

    ticket_number = Column(String(50), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=False)
    category = Column(String(50), index=True, nullable=False)  # academic, admission, finance, documentation, tech, hostel, career
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    status = Column(String(50), default="OPEN", index=True, nullable=False)  # OPEN, TRIAGED, ASSIGNED, INVESTIGATING, WAITING, RESOLVED, CLOSED
    reporter_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    assigned_person_id = Column(String(36), ForeignKey("people.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    resolution_notes = Column(String(2000), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class CaseComment(TenantBaseModel):
    __tablename__ = "case_comments"

    case_id = Column(String(36), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    author_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    comment = Column(String(2000), nullable=False)
    is_internal = Column(Boolean, default=False, nullable=False)


class Campaign(TenantBaseModel):
    __tablename__ = "campaigns"

    name = Column(String(255), nullable=False)
    campaign_type = Column(String(50), nullable=False)  # admission, student_engagement, event, alumni, career
    status = Column(String(50), default="draft", nullable=False)  # draft, scheduled, active, completed, paused
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    target_audience_segment = Column(JSON, default=dict, nullable=False)
    metrics = Column(JSON, default=dict, nullable=False)


class Event(TenantBaseModel):
    __tablename__ = "events"

    title = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)  # admission, orientation, workshop, career_fair, webinar, alumni
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=True)
    is_virtual = Column(Boolean, default=False, nullable=False)
    meeting_url = Column(String(500), nullable=True)
    max_capacity = Column(Integer, default=100, nullable=False)
    registered_count = Column(Integer, default=0, nullable=False)
    status = Column(String(50), default="upcoming", nullable=False)
