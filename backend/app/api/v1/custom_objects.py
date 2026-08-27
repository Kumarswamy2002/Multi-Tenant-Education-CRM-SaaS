from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
from pydantic import BaseModel
from app.database import get_db
from app.core.security import get_current_user
from app.services.custom_object_service import CustomObjectService

router = APIRouter(prefix="/custom-objects", tags=["Custom Object Platform"])


class ObjectDefinitionCreate(BaseModel):
    name: str
    api_name: str
    description: str = ""


class FieldDefinitionCreate(BaseModel):
    object_id: str
    field_name: str
    api_name: str
    field_type: str = "text"
    is_required: bool = False
    options: List[str] = []


class RecordCreate(BaseModel):
    object_id: str
    record_data: Dict[str, Any]


@router.post("/definitions", status_code=status.HTTP_201_CREATED)
async def create_object_definition(
    payload: ObjectDefinitionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await CustomObjectService.create_object_definition(
        db, payload.name, payload.api_name, payload.description
    )


@router.post("/fields", status_code=status.HTTP_201_CREATED)
async def add_field_definition(
    payload: FieldDefinitionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await CustomObjectService.add_field_definition(
        db, payload.object_id, payload.field_name, payload.api_name,
        payload.field_type, payload.is_required, payload.options
    )


@router.post("/records", status_code=status.HTTP_201_CREATED)
async def create_record(
    payload: RecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await CustomObjectService.create_record(
        db, payload.object_id, payload.record_data
    )
