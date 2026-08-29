import pytest
from backend.app.schemas.compliance_audit import ComplianceStandard, AuditSeverity
from backend.app.services.compliance_audit_service import ComplianceAuditService

def test_audit_event_recording_and_chaining():
    service = ComplianceAuditService(tenant_id="tenant_stanford")
    e1 = service.record_event(
        actor_id="user_admin_1",
        actor_email="admin@stanford.edu",
        action="STUDENT_TRANSCRIPT_VIEWED",
        resource_type="Transcript",
        resource_id="trx_9901",
        compliance_standard=ComplianceStandard.FERPA,
        severity=AuditSeverity.INFO,
        payload_snapshot={"student_id": "stu_404"}
    )
    
    assert e1.event_id.startswith("evt_")
    assert e1.prev_hash.startswith("GENESIS_")
    assert len(e1.event_hash) == 64

    e2 = service.record_event(
        actor_id="user_admin_1",
        actor_email="admin@stanford.edu",
        action="STUDENT_GRADE_MODIFIED",
        resource_type="Grade",
        resource_id="grd_5521",
        compliance_standard=ComplianceStandard.FERPA,
        severity=AuditSeverity.HIGH,
        payload_snapshot={"old_grade": "B", "new_grade": "A"}
    )
    
    assert e2.prev_hash == e1.event_hash
    assert len(service.get_audit_trail()) == 2

def test_audit_integrity_verification_pass():
    service = ComplianceAuditService(tenant_id="tenant_mit")
    for i in range(5):
        service.record_event(
            actor_id=f"user_{i}",
            actor_email=f"user_{i}@mit.edu",
            action="EXPORT_STUDENT_PII",
            resource_type="Student",
            resource_id=f"stu_{i}",
            compliance_standard=ComplianceStandard.GDPR,
            severity=AuditSeverity.WARNING
        )
    
    result = service.verify_integrity()
    assert result.is_valid is True
    assert result.total_events == 5
    assert result.corrupted_event_id is None

def test_audit_integrity_verification_tamper_detected():
    service = ComplianceAuditService(tenant_id="tenant_mit")
    service.record_event(
        actor_id="user_1",
        actor_email="user_1@mit.edu",
        action="ACCESS_FINANCIAL_AID",
        resource_type="AidRecord",
        resource_id="aid_1"
    )
    service.record_event(
        actor_id="user_2",
        actor_email="user_2@mit.edu",
        action="ACCESS_FINANCIAL_AID",
        resource_type="AidRecord",
        resource_id="aid_2"
    )
    
    # Simulate malicious tamper in memory
    service._ledger[0].action = "MALICIOUS_TAMPERED_ACTION"
    
    result = service.verify_integrity()
    assert result.is_valid is False
    assert result.corrupted_event_id == service._ledger[0].event_id
