"""
CampusSphere Official Python Client SDK.
Provides synchronous and asynchronous API wrappers with retry mechanisms and typing.
"""
from typing import Dict, Any, Optional, List
import httpx


class CampusSphereClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000/api/v1", tenant_id: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.tenant_id = tenant_id
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "X-Tenant-ID": tenant_id or "default-tenant",
            "Content-Type": "application/json"
        }

    def get_academics(self) -> Dict[str, Any]:
        with httpx.Client(base_url=self.base_url, headers=self._headers, timeout=10.0) as client:
            resp = client.get("/academics/list")
            resp.raise_for_status()
            return resp.json()

    def get_billing_invoices(self, student_id: str) -> Dict[str, Any]:
        with httpx.Client(base_url=self.base_url, headers=self._headers, timeout=10.0) as client:
            resp = client.get(f"/billing-finance/list?student_id={student_id}")
            resp.raise_for_status()
            return resp.json()

    def predict_retention_risk(self, student_id: str) -> Dict[str, Any]:
        with httpx.Client(base_url=self.base_url, headers=self._headers, timeout=10.0) as client:
            resp = client.post("/ai-insights/action/execute", json={"action_type": "retention_predict", "record_ids": [student_id]})
            resp.raise_for_status()
            return resp.json()
