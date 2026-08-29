"""
Enterprise Cryptographic Compliance & Audit Service.
Maintains a tamper-evident, SHA-256 chained audit trail for FERPA, GDPR, and HIPAA compliance.
"""

import hashlib
import json
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from backend.app.schemas.compliance_audit import (
    ComplianceAuditEvent,
    ComplianceStandard,
    AuditSeverity,
    AuditVerificationResult,
)

class ComplianceAuditService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._ledger: List[ComplianceAuditEvent] = []
        self._last_hash: str = "GENESIS_ROOT_HASH_000000000000000000000000000000000000000000000000000000"

    def _compute_hash(self, prev_hash: str, payload_str: str) -> str:
        data = f"{prev_hash}|{payload_str}".encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def record_event(
        self,
        actor_id: str,
        actor_email: str,
        action: str,
        resource_type: str,
        resource_id: str,
        compliance_standard: ComplianceStandard = ComplianceStandard.FERPA,
        severity: AuditSeverity = AuditSeverity.INFO,
        payload_snapshot: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> ComplianceAuditEvent:
        payload = payload_snapshot or {}
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)
        
        raw_payload = json.dumps(
            {
                "event_id": event_id,
                "tenant_id": self.tenant_id,
                "actor_id": actor_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "timestamp": now.isoformat(),
                "payload": payload,
            },
            sort_keys=True
        )
        
        event_hash = self._compute_hash(self._last_hash, raw_payload)
        
        event = ComplianceAuditEvent(
            event_id=event_id,
            tenant_id=self.tenant_id,
            actor_id=actor_id,
            actor_email=actor_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            compliance_standard=compliance_standard,
            severity=severity,
            payload_snapshot=payload,
            ip_address=ip_address,
            user_agent=user_agent,
            prev_hash=self._last_hash,
            event_hash=event_hash,
            timestamp=now
        )
        
        self._ledger.append(event)
        self._last_hash = event_hash
        return event

    def get_audit_trail(self, limit: int = 100) -> List[ComplianceAuditEvent]:
        return list(reversed(self._ledger[-limit:]))

    def verify_integrity(self) -> AuditVerificationResult:
        expected_prev = "GENESIS_ROOT_HASH_000000000000000000000000000000000000000000000000000000"
        
        for event in self._ledger:
            if event.prev_hash != expected_prev:
                return AuditVerificationResult(
                    is_valid=False,
                    total_events=len(self._ledger),
                    corrupted_event_id=event.event_id
                )
            
            raw_payload = json.dumps(
                {
                    "event_id": event.event_id,
                    "tenant_id": event.tenant_id,
                    "actor_id": event.actor_id,
                    "action": event.action,
                    "resource_type": event.resource_type,
                    "resource_id": event.resource_id,
                    "timestamp": event.timestamp.isoformat(),
                    "payload": event.payload_snapshot,
                },
                sort_keys=True
            )
            recalculated = self._compute_hash(event.prev_hash, raw_payload)
            if recalculated != event.event_hash:
                return AuditVerificationResult(
                    is_valid=False,
                    total_events=len(self._ledger),
                    corrupted_event_id=event.event_id
                )
            expected_prev = event.event_hash

        return AuditVerificationResult(
            is_valid=True,
            total_events=len(self._ledger),
            corrupted_event_id=None
        )
