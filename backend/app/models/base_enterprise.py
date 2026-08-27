"""
Base database models and mixins with multi-tenancy, soft delete, audit, and UUID support.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TimestampMixin:
    """Provides created_at and updated_at timestamps in UTC."""
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class SoftDeleteMixin:
    """Provides soft-delete capabilities with deletion timestamp and reason."""
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by_id = Column(String(36), nullable=True)
    deletion_reason = Column(String(255), nullable=True)

    def soft_delete(self, user_id: Optional[str] = None, reason: Optional[str] = None) -> None:
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by_id = user_id
        self.deletion_reason = reason

    def restore(self) -> None:
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by_id = None
        self.deletion_reason = None


class TenantAwareMixin:
    """Ensures strict multi-tenant isolation across all university institutions."""
    @declared_attr
    def tenant_id(cls):
        return Column(
            String(36),
            ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )


class AuditMixin:
    """Tracks creating and updating user identities."""
    created_by_id = Column(String(36), nullable=True)
    updated_by_id = Column(String(36), nullable=True)
    version = Column(Integer, default=1, nullable=False)


class CustomFieldsMixin:
    """Supports dynamic EAV / JSONB custom metadata schemas per institution."""
    custom_fields = Column(JSONB, default=dict, nullable=False)
    tags = Column(JSONB, default=list, nullable=False)

    def set_custom_field(self, key: str, value: Any) -> None:
        if self.custom_fields is None:
            self.custom_fields = {}
        fields = dict(self.custom_fields)
        fields[key] = value
        self.custom_fields = fields

    def get_custom_field(self, key: str, default: Any = None) -> Any:
        if not self.custom_fields:
            return default
        return self.custom_fields.get(key, default)


class BaseModel(Base, TimestampMixin, SoftDeleteMixin, TenantAwareMixin, AuditMixin, CustomFieldsMixin):
    """Abstract base class combining multi-tenancy, auditing, soft-delete, and timestamps."""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Serializes standard model columns to a dictionary."""
        result = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if isinstance(val, datetime):
                result[col.name] = val.isoformat()
            else:
                result[col.name] = val
        return result
