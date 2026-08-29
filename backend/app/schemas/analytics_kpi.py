from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone

class ConversionFunnelStage(BaseModel):
    stage_name: str
    count: int
    conversion_rate: float
    drop_off_rate: float

class ExecutiveKpiReport(BaseModel):
    tenant_id: str
    total_leads: int
    total_applications: int
    total_enrollments: int
    overall_conversion_rate: float
    retention_rate: float
    average_time_to_enroll_days: float
    funnel_stages: List[ConversionFunnelStage]
    revenue_forecast: float
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CohortRetentionMetric(BaseModel):
    cohort_year: int
    cohort_term: str
    starting_headcount: int
    active_headcount: int
    retention_rate_pct: float
    risk_level: str
