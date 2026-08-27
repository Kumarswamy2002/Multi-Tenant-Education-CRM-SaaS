from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.person import Person
from app.models.crm import Lead
from app.models.timeline import TimelineEvent
from app.schemas.crm import LeadCreate, LeadResponse

router = APIRouter(prefix="/leads", tags=["Lead CRM"])


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    # 1. Create or query Person record
    person = Person(
        tenant_id=tenant_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        primary_role="prospect"
    )
    db.add(person)
    await db.flush()

    # 2. Create Lead
    lead = Lead(
        tenant_id=tenant_id,
        person_id=person.id,
        status="NEW",
        stage="prospecting",
        lead_source_id=payload.lead_source_id,
        assigned_counselor_person_id=payload.assigned_counselor_person_id,
        academic_interest_program_id=payload.academic_interest_program_id,
        score=50.0,  # Base initial score
        custom_fields=payload.custom_fields
    )
    db.add(lead)
    await db.flush()

    # 3. Publish Timeline Event
    timeline_ev = TimelineEvent(
        tenant_id=tenant_id,
        entity_id=person.id,
        entity_type="lead",
        event_type="LeadCreated",
        title="Lead Captured",
        description=f"Prospect {payload.first_name} {payload.last_name} created in system.",
        occurred_at=datetime.now(timezone.utc),
        payload={"lead_id": lead.id, "source": payload.lead_source_id}
    )
    db.add(timeline_ev)
    await db.commit()
    await db.refresh(lead)

    return lead


@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    status_filter: str = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(Lead).where(Lead.tenant_id == tenant_id)
    if status_filter:
        stmt = stmt.where(Lead.status == status_filter)
    res = await db.execute(stmt)
    return res.scalars().all()
