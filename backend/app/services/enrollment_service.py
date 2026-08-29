"""
Student Enrollment Lifecycle & Workflow Service
"""
from enum import Enum
from typing import Dict, Any, List

class EnrollmentStatus(Enum):
    LEAD = "LEAD"
    APPLIED = "APPLIED"
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED"
    ADMITTED = "ADMITTED"
    ENROLLED = "ENROLLED"
    REJECTED = "REJECTED"

class EnrollmentWorkflowService:
    REQUIRED_DOCS = ["photo_id", "high_school_transcript", "immunization_record"]

    @classmethod
    def evaluate_readiness(cls, student_id: str, submitted_docs: List[str]) -> Dict[str, Any]:
        missing = [doc for doc in cls.REQUIRED_DOCS if doc not in submitted_docs]
        ready = len(missing) == 0
        return {
            "student_id": student_id,
            "ready_for_admission": ready,
            "missing_documents": missing,
            "next_status": EnrollmentStatus.ADMITTED.value if ready else EnrollmentStatus.APPLIED.value
        }
