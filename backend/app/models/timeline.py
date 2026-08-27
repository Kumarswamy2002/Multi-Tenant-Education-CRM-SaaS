from sqlalchemy import Column, String, DateTime, JSON, Boolean
from app.models.base import TenantBaseModel, BaseModel


class TimelineEvent(TenantBaseModel):
    __tablename__ = "timeline_events"

    entity_id = Column(String(36), index=True, nullable=False)  # Person ID, Lead ID, Application ID, Student ID
    entity_type = Column(String(50), index=True, nullable=False)  # person, lead, application, student, parent, alumni
    event_type = Column(String(100), index=True, nullable=False)  # LeadCreated, CounsellingCompleted, ApplicationSubmitted, DocumentVerified, AdmissionApproved, EnrollmentCompleted, CaseCreated, JobApplied, OfferReceived
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    performed_by_person_id = Column(String(36), nullable=True)
    payload = Column(JSON, default=dict, nullable=False)
    occurred_at = Column(DateTime(timezone=True), index=True, nullable=False)


class OutboxEvent(TenantBaseModel):
    __tablename__ = "outbox_events"

    event_id = Column(String(36), unique=True, index=True, nullable=False)
    aggregate_type = Column(String(100), nullable=False)
    aggregate_id = Column(String(36), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON, default=dict, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
