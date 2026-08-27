from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.person import Person, StudentProfile
from app.models.timeline import TimelineEvent
from app.models.relationship import Relationship
from app.schemas.person import PersonCreate, PersonResponse, StudentProfileCreate, StudentProfileResponse

router = APIRouter(prefix="/people", tags=["People & Student 360"])


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    payload: PersonCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    person = Person(
        tenant_id=tenant_id,
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        gender=payload.gender,
        date_of_birth=payload.date_of_birth,
        nationality=payload.nationality,
        address=payload.address,
        avatar_url=payload.avatar_url,
        primary_role=payload.primary_role,
        metadata_fields=payload.metadata_fields
    )
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person


@router.get("/", response_model=List[PersonResponse])
async def list_people(
    primary_role: str = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(Person).where(Person.tenant_id == tenant_id)
    if primary_role:
        stmt = stmt.where(Person.primary_role == primary_role)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.get("/{person_id}/360")
async def get_student_360(
    person_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    # 1. Fetch Person record
    p_stmt = select(Person).where(Person.id == person_id, Person.tenant_id == tenant_id)
    p_res = await db.execute(p_stmt)
    person = p_res.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # 2. Fetch Student Profile (if applicable)
    sp_stmt = select(StudentProfile).where(StudentProfile.person_id == person_id, StudentProfile.tenant_id == tenant_id)
    sp_res = await db.execute(sp_stmt)
    student_profile = sp_res.scalars().first()

    # 3. Fetch Graph Relationships
    rel_stmt = select(Relationship).where(
        Relationship.tenant_id == tenant_id,
        (Relationship.source_id == person_id) | (Relationship.target_id == person_id)
    )
    rel_res = await db.execute(rel_stmt)
    relationships = rel_res.scalars().all()

    # 4. Fetch Unified Timeline Events
    timeline_stmt = (
        select(TimelineEvent)
        .where(TimelineEvent.entity_id == person_id, TimelineEvent.tenant_id == tenant_id)
        .order_by(TimelineEvent.occurred_at.desc())
    )
    timeline_res = await db.execute(timeline_stmt)
    timeline_events = timeline_res.scalars().all()

    return {
        "person": person,
        "student_profile": student_profile,
        "relationships": relationships,
        "timeline": timeline_events,
    }
