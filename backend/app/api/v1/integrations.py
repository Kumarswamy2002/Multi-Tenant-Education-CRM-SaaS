from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from app.core.security import get_current_user
from app.services.integration_service import IntegrationHubService

router = APIRouter(prefix="/integrations", tags=["Integration Platform & Webhooks"])


class InboundWebhookPayload(BaseModel):
    provider: str  # banner_sis, canvas_lms, slate_crm
    data: Dict[str, Any]


@router.post("/webhooks/inbound")
async def receive_inbound_webhook(
    payload: InboundWebhookPayload,
    x_signature: str = Header(None)
):
    canonical_person = IntegrationHubService.map_to_canonical_person(payload.provider, payload.data)
    return {
        "status": "RECEIVED",
        "provider": payload.provider,
        "canonical_person": canonical_person
    }
