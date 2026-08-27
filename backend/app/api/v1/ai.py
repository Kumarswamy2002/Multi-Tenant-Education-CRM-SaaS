from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.core.security import get_current_user
from app.engine.rag_engine import TenantScopedAIEngine

router = APIRouter(prefix="/ai", tags=["AI & Machine Learning Platform"])


class CounselorBriefRequest(BaseModel):
    prospect_name: str
    academic_interest: str
    counseling_notes: List[str] = []


class StudentRiskAnalysisRequest(BaseModel):
    student_name: str
    gpa: float = 3.2
    attendance_percentage: float = 85.0
    open_cases_count: int = 0


@router.post("/counselor-brief")
async def generate_counselor_brief(
    payload: CounselorBriefRequest,
    current_user = Depends(get_current_user)
):
    return TenantScopedAIEngine.generate_counselor_assistant_summary(
        prospect_name=payload.prospect_name,
        academic_interest=payload.academic_interest,
        counseling_notes=payload.counseling_notes
    )


@router.post("/student-risk-analysis")
async def analyze_student_risk(
    payload: StudentRiskAnalysisRequest,
    current_user = Depends(get_current_user)
):
    return TenantScopedAIEngine.generate_student_success_risk_analysis(
        student_name=payload.student_name,
        gpa=payload.gpa,
        attendance_percentage=payload.attendance_percentage,
        open_cases_count=payload.open_cases_count
    )
