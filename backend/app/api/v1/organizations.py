from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.organization import Organization, Department, Program
from app.schemas.organization import (
    OrganizationCreate, OrganizationResponse,
    DepartmentCreate, ProgramCreate, ProgramResponse
)

router = APIRouter(prefix="/organizations", tags=["Organizations & Programs"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    org = Organization(
        tenant_id=tenant_id,
        name=payload.name,
        code=payload.code,
        org_type=payload.org_type,
        industry=payload.industry,
        website=payload.website,
        email=payload.email,
        phone=payload.phone,
        address=payload.address,
        parent_id=payload.parent_id
    )
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(Organization).where(Organization.tenant_id == tenant_id)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/programs", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
async def create_program(
    payload: ProgramCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    program = Program(
        tenant_id=tenant_id,
        department_id=payload.department_id,
        name=payload.name,
        code=payload.code,
        degree_level=payload.degree_level,
        duration_months=payload.duration_months,
        credits_required=payload.credits_required,
        tuition_fee=payload.tuition_fee
    )
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return program


@router.get("/programs", response_model=List[ProgramResponse])
async def list_programs(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(Program).where(Program.tenant_id == tenant_id)
    res = await db.execute(stmt)
    return res.scalars().all()
