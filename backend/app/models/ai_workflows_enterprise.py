"""
AI Engine, Retention Prediction Models, Lead Scoring Algorithms, and Automated Workflows.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, DateTime,
    ForeignKey, Enum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from app.models.base_enterprise import BaseModel, Base


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StudentRetentionRisk(BaseModel):
    """AI Early-Warning & Dropout Risk Assessment for Enrolled Students."""
    __tablename__ = "student_retention_risks"

    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    risk_score = Column(Float, nullable=False) # 0.0 to 100.0
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW, nullable=False)
    academic_risk_factor = Column(Float, default=0.0) # GPA trend, failed assignments
    attendance_risk_factor = Column(Float, default=0.0) # Low presence rate
    financial_risk_factor = Column(Float, default=0.0) # Overdue unpaid invoices
    engagement_risk_factor = Column(Float, default=0.0) # LMS inactivity
    contributing_factors = Column(JSONB, default=list)
    recommended_interventions = Column(JSONB, default=list) # ["Assign Academic Tutor", "Counselor Check-in"]
    assessed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text, nullable=True)


class LeadScoreProfile(BaseModel):
    """AI Propensity & Conversion Scoring for Prospective Admission Leads."""
    __tablename__ = "lead_score_profiles"

    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    propensity_score = Column(Float, nullable=False) # 0.0 to 100.0
    conversion_tier = Column(String(50), default="Warm") # Hot, Warm, Cold
    engagement_frequency_score = Column(Float, default=0.0)
    profile_fit_score = Column(Float, default=0.0)
    preferred_channel = Column(String(50), default="email") # email, whatsapp, call
    optimal_contact_time = Column(String(100), default="Evening (4 PM - 7 PM)")
    signals = Column(JSONB, default=list)
    last_scored_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowAutomation(BaseModel):
    """Event-driven automation rules (e.g. On Lead Stage Change -> Send WhatsApp + Task to Counselor)."""
    __tablename__ = "workflow_automations"

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    trigger_event = Column(String(100), nullable=False) # lead_created, application_submitted, invoice_overdue
    conditions = Column(JSONB, default=list) # [{"field": "status", "operator": "eq", "value": "interested"}]
    actions = Column(JSONB, default=list) # [{"type": "send_email", "template_id": "welcome_1"}, {"type": "create_task"}]
    is_active = Column(Boolean, default=True, nullable=False)
    execution_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime, nullable=True)


class WorkflowExecutionLog(BaseModel):
    """Execution audit trail for workflow runs."""
    __tablename__ = "workflow_execution_logs"

    workflow_id = Column(String(36), ForeignKey("workflow_automations.id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String(100), nullable=False) # lead, student, invoice
    entity_id = Column(String(36), nullable=False)
    status = Column(String(50), default="success") # success, failed, skipped
    execution_duration_ms = Column(Float, default=0.0)
    log_details = Column(JSONB, default=dict)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
