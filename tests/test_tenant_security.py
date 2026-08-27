import pytest
from app.context import TenantContext
from fastapi import HTTPException


def test_tenant_context_management():
    TenantContext.clear()
    assert TenantContext.get_tenant_id() is None

    TenantContext.set_tenant_id("tenant-123")
    assert TenantContext.get_tenant_id() == "tenant-123"
    assert TenantContext.require_tenant_id() == "tenant-123"

    TenantContext.clear()
    assert TenantContext.get_tenant_id() is None
    with pytest.raises(HTTPException):
        TenantContext.require_tenant_id()


def test_super_admin_bypass():
    TenantContext.clear()
    TenantContext.set_super_admin(True)
    assert TenantContext.require_tenant_id() == "system"
    TenantContext.clear()
