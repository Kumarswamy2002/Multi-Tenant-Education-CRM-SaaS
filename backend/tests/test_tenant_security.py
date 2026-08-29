import pytest
from backend.app.core.tenant_security import TenantIsolationPolicyEngine, TenantSecurityException

def test_tenant_isolation_success():
    assert TenantIsolationPolicyEngine.assert_tenant_access("tenant-10", "tenant-10") is True

def test_tenant_isolation_violation():
    with pytest.raises(TenantSecurityException):
        TenantIsolationPolicyEngine.assert_tenant_access("tenant-10", "tenant-20")
