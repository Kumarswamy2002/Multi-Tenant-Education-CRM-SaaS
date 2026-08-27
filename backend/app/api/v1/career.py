from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from pydantic import BaseModel
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.career import JobPosting, JobApplication, JobOffer
from app.models.timeline import TimelineEvent
from datetime import datetime, timezone

router = APIRouter(prefix="/career", tags=["Career & Placement CRM"])


class JobPostingCreate(BaseModel):
    employer_organization_id: str
    title: str
    job_type: str = "full_time"  # full_time, part_time, internship, contract
    location: str
    salary_range: str = "70,000 - 90,000 USD"
    description: str
    requirements: List[str] = []


class JobApplicationCreate(BaseModel):
    job_posting_id: str
    student_person_id: str
    cover_letter: str = ""


@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_job_posting(
    payload: JobPostingCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    job = JobPosting(
        tenant_id=tenant_id,
        employer_organization_id=payload.employer_organization_id,
        title=payload.title,
        job_type=payload.job_type,
        location=payload.location,
        salary_range=payload.salary_range,
        description=payload.description,
        requirements=payload.requirements,
        status="active"
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/jobs")
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(JobPosting).where(JobPosting.tenant_id == tenant_id)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/applications", status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    payload: JobApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    app_obj = JobApplication(
        tenant_id=tenant_id,
        job_posting_id=payload.job_posting_id,
        student_person_id=payload.student_person_id,
        cover_letter=payload.cover_letter,
        status="APPLIED"
    )
    db.add(app_obj)

    # Timeline event
    tl = TimelineEvent(
        tenant_id=tenant_id,
        entity_id=payload.student_person_id,
        entity_type="student",
        event_type="JobApplied",
        title="Applied for Placement Opportunity",
        description=f"Student applied for Job ID {payload.job_posting_id}.",
        occurred_at=datetime.now(timezone.utc),
        payload={"job_posting_id": payload.job_posting_id}
    )
    db.add(tl)

    await db.commit()
    await db.refresh(app_obj)
    return app_obj
