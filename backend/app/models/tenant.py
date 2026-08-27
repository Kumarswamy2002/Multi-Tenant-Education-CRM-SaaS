from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Tenant(BaseModel):
    __tablename__ = "tenants"

    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    plan_tier = Column(String(50), default="standard", nullable=False)  # standard, professional, enterprise
    max_users = Column(Integer, default=50, nullable=False)
    max_students = Column(Integer, default=5000, nullable=False)
    settings = Column(JSON, default=dict, nullable=False)


class TenantSubscription(BaseModel):
    __tablename__ = "tenant_subscriptions"

    tenant_id = Column(String(36), index=True, nullable=False)
    plan_name = Column(String(100), nullable=False)
    status = Column(String(50), default="active", nullable=False)  # active, past_due, canceled, trialing
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    billing_email = Column(String(255), nullable=False)
    payment_method = Column(String(50), nullable=True)
