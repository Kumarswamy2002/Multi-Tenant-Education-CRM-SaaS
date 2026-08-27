"""
Pydantic Schemas for Career Services, AI Retention/Scoring, and Workflow Automations.
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import Field
from backend.app.schemas.base_enterprise import BaseSchema, AuditSchema
from backend.app.models.career_enterprise import JobType, JobApplicationStatus
from backend.app.models.ai_workflows_enterprise import RiskLevel


# Career & Jobs
class JobPostingCreate(BaseSchema):
    company_id: str
    title: str
    job_type: JobType = JobType.FULL_TIME
    locations: List[str] = Field(default_factory=list)
    ctc_annual_salary: Optional[float] = None
    stipend_monthly: Optional[float] = None
    min_cgpa: float = 0.0
    eligible_departments: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    description: str
    application_deadline: date
    openings_count: int = 1


class JobPostingRead(AuditSchema):
    company_id: str
    company_name: Optional[str] = None
    title: str
    job_type: JobType
    locations: List[str]
    ctc_annual_salary: Optional[float] = None
    stipend_monthly: Optional[float] = None
    min_cgpa: float
    eligible_departments: List[str]
    required_skills: List[str]
    description: str
    application_deadline: date
    openings_count: int
    status: str


class JobApplicationCreate(BaseSchema):
    job_posting_id: str
    student_id: str
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None


class JobApplicationRead(AuditSchema):
    job_posting_id: str
    student_id: str
    student_name: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    resume_url: Optional[str] = None
    applied_at: datetime
    status: JobApplicationStatus
    current_round: str
    feedback_notes: Optional[str] = None
    offered_ctc: Optional[float] = None


# AI & Predictions
class StudentRetentionRiskRead(AuditSchema):
    student_id: str
    student_name: Optional[str] = None
    risk_score: float
    risk_level: RiskLevel
    academic_risk_factor: float
    attendance_risk_factor: float
    financial_risk_factor: float
    engagement_risk_factor: float
    contributing_factors: List[str]
    recommended_interventions: List[str]
    assessed_at: datetime
    is_resolved: bool
    resolution_notes: Optional[str] = None


class LeadScoreProfileRead(AuditSchema):
    lead_id: str
    propensity_score: float
    conversion_tier: str
    engagement_frequency_score: float
    profile_fit_score: float
    preferred_channel: str
    optimal_contact_time: str
    signals: List[str]
    last_scored_at: datetime


# Workflow Automations
class WorkflowAutomationCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    is_active: bool = True


class WorkflowAutomationRead(AuditSchema):
    name: str
    description: Optional[str] = None
    trigger_event: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    is_active: bool
    execution_count: int
    last_triggered_at: Optional[datetime] = None
