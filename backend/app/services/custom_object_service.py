
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.custom_object import CustomObjectDefinition, CustomFieldDefinition, CustomObjectRecord
from app.context import TenantContext
from fastapi import HTTPException


class CustomObjectService:
    """
    Custom Object Service enabling institutions to define custom entities, dynamic field definitions,
    and persist JSON-validated records.
    """

    @staticmethod
    async def create_object_definition(
        db: AsyncSession,
        name: str,
        api_name: str,
        description: str = ""
    ) -> CustomObjectDefinition:
        tenant_id = TenantContext.require_tenant_id()
        obj_def = CustomObjectDefinition(
            tenant_id=tenant_id,
            name=name,
            api_name=api_name,
            description=description,
            is_active=True
        )
        db.add(obj_def)
        await db.flush()
        return obj_def

    @staticmethod
    async def add_field_definition(
        db: AsyncSession,
        object_id: str,
        field_name: str,
        api_name: str,
        field_type: str = "text",  # text, number, date, dropdown, boolean, lookup
        is_required: bool = False,
        options: List[str] = None
    ) -> CustomFieldDefinition:
        tenant_id = TenantContext.require_tenant_id()
        field_def = CustomFieldDefinition(
            tenant_id=tenant_id,
            object_id=object_id,
            field_name=field_name,
            api_name=api_name,
            field_type=field_type,
            is_required=is_required,
            options=options or []
        )
        db.add(field_def)
        await db.flush()
        return field_def

    @staticmethod
    async def create_record(
        db: AsyncSession,
        object_id: str,
        record_data: Dict[str, Any]
    ) -> CustomObjectRecord:
        tenant_id = TenantContext.require_tenant_id()

        # Validate required fields
        stmt = select(CustomFieldDefinition).where(
            CustomFieldDefinition.object_id == object_id,
            CustomFieldDefinition.tenant_id == tenant_id
        )
        res = await db.execute(stmt)
        fields = res.scalars().all()

        for f in fields:
            if f.is_required and f.api_name not in record_data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Required custom field '{f.field_name}' ({f.api_name}) missing."
                )

        record = CustomObjectRecord(
            tenant_id=tenant_id,
            object_id=object_id,
            record_data=record_data
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record
