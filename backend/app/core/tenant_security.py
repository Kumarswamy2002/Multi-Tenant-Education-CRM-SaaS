"""
Multi-Tenant Security & Tenant Isolation Policy Engine
"""
from typing import Dict, Any, Optional

class TenantSecurityException(Exception):
    pass

class TenantIsolationPolicyEngine:
    @staticmethod
    def assert_tenant_access(current_tenant_id: str, record_tenant_id: str):
        if not current_tenant_id or not record_tenant_id:
            raise TenantSecurityException("Tenant ID cannot be empty.")
        if current_tenant_id != record_tenant_id:
            raise TenantSecurityException(f"Cross-tenant access violation: {current_tenant_id} -> {record_tenant_id}")
        return True

    @staticmethod
    def build_tenant_filter(tenant_id: str, base_query: Dict[str, Any]) -> Dict[str, Any]:
        scoped_query = dict(base_query)
        scoped_query["tenant_id"] = tenant_id
        return scoped_query
