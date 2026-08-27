from sqlalchemy import Column, String, JSON, Boolean
from app.models.base import TenantBaseModel


class CustomObjectDefinition(TenantBaseModel):
    __tablename__ = "custom_object_definitions"

    name = Column(String(100), nullable=False)
    api_name = Column(String(100), index=True, nullable=False)  # scholarship_application, hostel_request
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class CustomFieldDefinition(TenantBaseModel):
    __tablename__ = "custom_field_definitions"

    object_id = Column(String(36), index=True, nullable=False)
    field_name = Column(String(100), nullable=False)
    api_name = Column(String(100), nullable=False)
    field_type = Column(String(50), nullable=False)  # text, number, date, dropdown, boolean, lookup
    is_required = Column(Boolean, default=False, nullable=False)
    options = Column(JSON, default=list, nullable=False)


class CustomObjectRecord(TenantBaseModel):
    __tablename__ = "custom_object_records"

    object_id = Column(String(36), index=True, nullable=False)
    record_data = Column(JSON, default=dict, nullable=False)
