from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.workflow import WorkflowDefinition, WorkflowExecution
from app.engine.workflow_engine import WorkflowAutomationEngine
from pydantic import BaseModel, Field

router = APIRouter(prefix="/workflows", tags=["Workflow Automation Engine"])


class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    trigger_event: str  # ApplicationSubmitted, DocumentUploaded, LeadCreated, CaseCreated
    conditions_tree: Dict[str, Any] = Field(default_factory=dict)
    action_steps: List[Dict[str, Any]] = Field(default_factory=list)


class TriggerPayload(BaseModel):
    trigger_event: str
    entity_id: str
    event_payload: Dict[str, Any] = Field(default_factory=dict)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    wf = WorkflowDefinition(
        tenant_id=tenant_id,
        name=payload.name,
        description=payload.description,
        trigger_event=payload.trigger_event,
        conditions_tree=payload.conditions_tree,
        action_steps=payload.action_steps,
        is_active=True
    )
    db.add(wf)
    await db.commit()
    await db.refresh(wf)
    return wf


@router.get("/")
async def list_workflows(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    stmt = select(WorkflowDefinition).where(WorkflowDefinition.tenant_id == tenant_id)
    res = await db.execute(stmt)
    return res.scalars().all()


@router.post("/trigger")
async def trigger_workflow(
    payload: TriggerPayload,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    executions = await WorkflowAutomationEngine.process_trigger(
        db=db,
        trigger_event=payload.trigger_event,
        entity_id=payload.entity_id,
        event_payload=payload.event_payload
    )
    return {
        "message": f"Processed trigger '{payload.trigger_event}'. Triggered {len(executions)} workflows.",
        "execution_ids": [e.id for e in executions]
    }
