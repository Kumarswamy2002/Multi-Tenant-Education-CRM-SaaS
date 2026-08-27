import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.crm import Case, CaseComment
from app.models.timeline import TimelineEvent
from app.schemas.crm import CaseCreate, CaseResponse

router = APIRouter(prefix="/cases", tags=["Case & Support Management"])


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    payload: CaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    ticket_num = f"TICK-{uuid.uuid4().hex[:8].upper()}"

    case_obj = Case(
        tenant_id=tenant_id,
        ticket_number=ticket_num,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        priority=payload.priority,
        status="OPEN",
        reporter_person_id=payload.reporter_person_id,
        assigned_person_id=payload.assigned_person_id,
        department_id=payload.department_id
    )
    db.add(case_obj)
    await db.flush()

    # Timeline event
    tl = TimelineEvent(
        tenant_id=tenant_id,
        entity_id=payload.reporter_person_id,
        entity_type="person",
        event_type="CaseCreated",
        title=f"Support Case {ticket_num} Opened",
        description=f"Ticket '{payload.title}' created under {payload.category}.",
        occurred_at=datetime.now(timezone.utc),
        payload={"ticket_number": ticket_num, "category": payload.category}
    )
    db.add(tl)

    await db.commit()
    await db.refresh(case_obj)
    return case_obj


@router.get("/", response_model=List[CaseResponse])
async def list_cases(
    status_filter: str = None,
    category_filter: str = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(Case).where(Case.tenant_id == tenant_id)
    if status_filter:
        stmt = stmt.where(Case.status == status_filter)
    if category_filter:
        stmt = stmt.where(Case.category == category_filter)
    res = await db.execute(stmt)
    return res.scalars().all()
