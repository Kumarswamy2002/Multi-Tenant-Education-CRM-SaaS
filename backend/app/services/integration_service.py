import hmac
import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.context import TenantContext

logger = logging.getLogger(__name__)


class IntegrationHubService:
    """
    Integration Platform Hub & Webhook Gateway. Converts provider payloads to Canonical Education Data Model,
    verifies HMAC signatures, and manages webhook deliveries.
    """

    @staticmethod
    def verify_webhook_signature(payload_bytes: bytes, signature_header: str, secret: str) -> bool:
        if not signature_header or not secret:
            return False
        expected_sig = hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, signature_header)

    @classmethod
    def map_to_canonical_person(cls, provider: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps external provider payloads (Banner SIS, Canvas LMS, Slate CRM) into internal Canonical Person Model.
        """
        if provider == "banner_sis":
            return {
                "first_name": payload.get("first_name"),
                "last_name": payload.get("last_name"),
                "email": payload.get("email_address"),
                "phone": payload.get("phone_num"),
                "external_id": payload.get("banner_id"),
                "provider": "banner_sis"
            }
        elif provider == "canvas_lms":
            name_parts = payload.get("name", "").split(" ", 1)
            return {
                "first_name": name_parts[0] if name_parts else "",
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "email": payload.get("primary_email"),
                "external_id": payload.get("sis_user_id"),
                "provider": "canvas_lms"
            }
        else:
            return {
                "first_name": payload.get("first_name", ""),
                "last_name": payload.get("last_name", ""),
                "email": payload.get("email"),
                "external_id": payload.get("id"),
                "provider": provider
            }
