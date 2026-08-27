from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer
from app.models.base import TenantBaseModel


class IntegrationConfig(TenantBaseModel):
    __tablename__ = "integration_configs"

    provider_name = Column(String(100), index=True, nullable=False)  # canvas_lms, banner_sis, stripe_payments, twilio_sms, sendgrid_email
    integration_type = Column(String(50), nullable=False)  # lms, sis, erp, payment, communication, identity
    auth_credentials = Column(JSON, default=dict, nullable=False)
    settings = Column(JSON, default=dict, nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)


class WebhookEndpoint(TenantBaseModel):
    __tablename__ = "webhook_endpoints"

    url = Column(String(500), nullable=False)
    secret_key = Column(String(255), nullable=False)
    subscribed_events = Column(JSON, default=list, nullable=False)  # ["ApplicationSubmitted", "StudentGraduated"]
    is_active = Column(Boolean, default=True, nullable=False)


class WebhookDeliveryLog(TenantBaseModel):
    __tablename__ = "webhook_delivery_logs"

    endpoint_id = Column(String(36), index=True, nullable=False)
    event_id = Column(String(36), nullable=False)
    event_type = Column(String(100), nullable=False)
    request_payload = Column(JSON, default=dict, nullable=False)
    response_status_code = Column(Integer, nullable=True)
    response_body = Column(String(2000), nullable=True)
    status = Column(String(50), default="DELIVERED", nullable=False)  # DELIVERED, FAILED, RETRYING
    attempt_count = Column(Integer, default=1, nullable=False)
    delivered_at = Column(DateTime(timezone=True), nullable=True)


class SyncJob(TenantBaseModel):
    __tablename__ = "sync_jobs"

    integration_id = Column(String(36), index=True, nullable=False)
    job_type = Column(String(50), nullable=False)  # inbound_student_sync, outbound_grades_sync
    status = Column(String(50), default="RUNNING", nullable=False)  # RUNNING, COMPLETED, FAILED
    records_processed = Column(Integer, default=0, nullable=False)
    error_summary = Column(String(2000), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
