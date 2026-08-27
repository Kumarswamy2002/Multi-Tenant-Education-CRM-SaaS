from sqlalchemy import Column, String, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import TenantBaseModel


class Organization(TenantBaseModel):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), nullable=True, index=True)
    org_type = Column(String(50), nullable=False)  # institution, employer, partner, external
    industry = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(JSON, default=dict, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    parent_id = Column(String(36), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)


class Campus(TenantBaseModel):
    __tablename__ = "campuses"

    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    address = Column(JSON, default=dict, nullable=False)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    is_main = Column(Boolean, default=False, nullable=False)


class Department(TenantBaseModel):
    __tablename__ = "departments"

    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    campus_id = Column(String(36), ForeignKey("campuses.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    head_person_id = Column(String(36), nullable=True)


class Program(TenantBaseModel):
    __tablename__ = "programs"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), nullable=False, index=True)
    degree_level = Column(String(50), nullable=False)  # bachelors, masters, doctorate, diploma, certificate
    duration_months = Column(Integer, default=36, nullable=False)
    credits_required = Column(Integer, default=120, nullable=False)
    tuition_fee = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)


class Course(TenantBaseModel):
    __tablename__ = "courses"

    department_id = Column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(String(36), ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, index=True)
    credits = Column(Integer, default=3, nullable=False)
    syllabus_description = Column(String(1000), nullable=True)
