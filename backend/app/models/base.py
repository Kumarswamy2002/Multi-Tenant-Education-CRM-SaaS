import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import declared_attr
from app.database import Base
from app.context import TenantContext


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BaseModel(Base):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=generate_uuid)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    created_by = Column(String(36), nullable=True)


class TenantBaseModel(BaseModel):
    __abstract__ = True

    tenant_id = Column(String(36), index=True, nullable=False)

    @declared_attr
    def __table_args__(cls):
        return (
            Index(f"ix_{cls.__tablename__}_tenant_id", "tenant_id"),
        )

    def __init__(self, **kwargs):
        if "tenant_id" not in kwargs or not kwargs["tenant_id"]:
            kwargs["tenant_id"] = TenantContext.require_tenant_id()
        super().__init__(**kwargs)
