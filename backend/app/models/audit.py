from sqlalchemy import Column, String, DateTime, JSON
from app.models.base import TenantBaseModel


class AuditEvent(TenantBaseModel):
    __tablename__ = "audit_events"

    user_id = Column(String(36), index=True, nullable=True)  # WHO
    action = Column(String(100), index=True, nullable=False)  # WHAT (e.g., STUDENT_RECORD_UPDATED, PERMISSION_CHANGED, ADMISSION_APPROVED)
    entity_type = Column(String(100), index=True, nullable=False)
    entity_id = Column(String(36), index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)  # WHERE
    user_agent = Column(String(500), nullable=True)
    before_state = Column(JSON, default=dict, nullable=True)  # BEFORE
    after_state = Column(JSON, default=dict, nullable=True)  # AFTER
    reason = Column(String(500), nullable=True)  # REASON
    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)  # WHEN
