from sqlalchemy import Column, String, Boolean, DateTime, JSON, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models.base import TenantBaseModel, BaseModel


class User(TenantBaseModel):
    __tablename__ = "users"

    email = Column(String(255), index=True, nullable=False)
    username = Column(String(100), index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_super_admin = Column(Boolean, default=False, nullable=False)
    person_id = Column(String(36), index=True, nullable=True)  # Links user to unified Person record
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(100), nullable=True)


class Role(TenantBaseModel):
    __tablename__ = "roles"

    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False)  # admin, admissions_manager, counselor, faculty, student, parent, employer, alumni
    description = Column(String(255), nullable=True)
    is_system_role = Column(Boolean, default=False, nullable=False)


class Permission(BaseModel):
    __tablename__ = "permissions"

    name = Column(String(100), nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)  # e.g., leads:read, leads:write, leads:delete
    module = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(String(36), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)


class UserRole(TenantBaseModel):
    __tablename__ = "user_roles"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)


class UserSession(TenantBaseModel):
    __tablename__ = "user_sessions"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
