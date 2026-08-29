from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from enum import Enum

class ComplianceStandard(str, Enum):
    FERPA = "FERPA"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    SOC2 = "SOC2"

class AuditSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ComplianceAuditEvent(BaseModel):
    event_id: str
    tenant_id: str
    actor_id: str
    actor_email: str
    action: str
    resource_type: str
    resource_id: str
    compliance_standard: ComplianceStandard
    severity: AuditSeverity
    payload_snapshot: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    prev_hash: str
    event_hash: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AuditVerificationResult(BaseModel):
    is_valid: bool
    total_events: int
    corrupted_event_id: Optional[str] = None
    verified_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
