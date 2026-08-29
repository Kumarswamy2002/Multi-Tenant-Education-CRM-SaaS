from backend.app.services.enrollment_service import EnrollmentWorkflowService

def test_enrollment_readiness_complete():
    docs = ["photo_id", "high_school_transcript", "immunization_record"]
    res = EnrollmentWorkflowService.evaluate_readiness("stu-1", docs)
    assert res["ready_for_admission"] is True
    assert len(res["missing_documents"]) == 0

def test_enrollment_readiness_missing():
    docs = ["photo_id"]
    res = EnrollmentWorkflowService.evaluate_readiness("stu-2", docs)
    assert res["ready_for_admission"] is False
    assert "high_school_transcript" in res["missing_documents"]
