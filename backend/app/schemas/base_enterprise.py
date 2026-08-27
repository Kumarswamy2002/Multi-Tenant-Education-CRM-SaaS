"""
Base Pydantic Schemas with generic responses, pagination, filtering, and audit fields.
"""
from typing import Generic, TypeVar, Optional, List, Any, Dict
from datetime import datetime, date, time
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TimestampSchema(BaseSchema):
    created_at: datetime
    updated_at: datetime


class AuditSchema(TimestampSchema):
    id: str
    tenant_id: str
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_by_id: Optional[str] = None
    updated_by_id: Optional[str] = None
    version: int = 1
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class APIResponse(BaseSchema, Generic[T]):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None
    error_code: Optional[str] = None
