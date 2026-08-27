"""
CampusSphere Python SDK Resource: Workflows API Resource.
"""
from typing import Dict, Any, List, Optional
import httpx


class WorkflowsResource:
    """Provides methods for managing workflows endpoints."""

    def __init__(self, client):
        self.client = client
        self.base_endpoint = "/workflows"

    def list(self, page: int = 1, page_size: int = 50, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Retrieves paginated list of workflows entities."""
        params = {"page": page, "page_size": page_size}
        if filters:
            params.update(filters)
        with httpx.Client(base_url=self.client.base_url, headers=self.client._headers, timeout=15.0) as http:
            resp = http.get(f"{self.base_endpoint}/list", params=params)
            resp.raise_for_status()
            return resp.json()

    def get_by_id(self, entity_id: str) -> Dict[str, Any]:
        """Retrieves single workflows entity by identifier."""
        with httpx.Client(base_url=self.client.base_url, headers=self.client._headers, timeout=15.0) as http:
            resp = http.get(f"{self.base_endpoint}/{entity_id}")
            resp.raise_for_status()
            return resp.json()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates new workflows record."""
        with httpx.Client(base_url=self.client.base_url, headers=self.client._headers, timeout=15.0) as http:
            resp = http.post(f"{self.base_endpoint}/", json=payload)
            resp.raise_for_status()
            return resp.json()

    def update(self, entity_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Updates existing workflows record."""
        with httpx.Client(base_url=self.client.base_url, headers=self.client._headers, timeout=15.0) as http:
            resp = http.patch(f"{self.base_endpoint}/{entity_id}", json=payload)
            resp.raise_for_status()
            return resp.json()

    def delete(self, entity_id: str) -> Dict[str, Any]:
        """Soft-deletes workflows record."""
        with httpx.Client(base_url=self.client.base_url, headers=self.client._headers, timeout=15.0) as http:
            resp = http.delete(f"{self.base_endpoint}/{entity_id}")
            resp.raise_for_status()
            return resp.json()
