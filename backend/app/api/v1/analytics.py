from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.crm import Lead, Case
from app.models.admissions import Application
from app.models.person import StudentProfile

router = APIRouter(prefix="/analytics", tags=["Analytics & BI Engine"])


@router.get("/admissions-funnel")
async def get_admissions_funnel_analytics(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    # Query counts for each funnel stage
    lead_count = await db.scalar(select(func.count(Lead.id)).where(Lead.tenant_id == tenant_id)) or 0
    app_count = await db.scalar(select(func.count(Application.id)).where(Application.tenant_id == tenant_id)) or 0
    student_count = await db.scalar(select(func.count(StudentProfile.id)).where(StudentProfile.tenant_id == tenant_id)) or 0
    open_cases = await db.scalar(select(func.count(Case.id)).where(Case.tenant_id == tenant_id, Case.status == "OPEN")) or 0

    conversion_rate = round((student_count / max(1, lead_count)) * 100, 2)

    return {
        "tenant_id": tenant_id,
        "funnel_metrics": {
            "total_leads": lead_count,
            "total_applications": app_count,
            "total_enrolled_students": student_count,
            "lead_to_student_conversion_rate_percentage": conversion_rate,
            "open_support_cases": open_cases
        }
    }
