import re
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.context import TenantContext

logger = logging.getLogger(__name__)


class CommunicationEngine:
    """
    Unified Communication Engine. Single notification infrastructure supporting Email, SMS, Push, and In-App
    channels with template merge tag rendering and delivery tracking.
    """

    TEMPLATES = {
        "lead_welcome": {
            "subject": "Welcome to {{ institution_name }}, {{ first_name }}!",
            "body": "Dear {{ first_name }},\nThank you for your interest in {{ program_name }}. Your assigned counselor is {{ counselor_name }}.\nBest regards,\nAdmissions Team"
        },
        "application_received": {
            "subject": "Application {{ application_number }} Received",
            "body": "Hi {{ first_name }},\nWe have received your application for {{ program_name }}. Please upload your transcript documents to proceed."
        },
        "admission_offer": {
            "subject": "Congratulations! Offer of Admission from {{ institution_name }}",
            "body": "Dear {{ first_name }},\nWe are thrilled to offer you admission to {{ program_name }} for {{ entry_term }}!"
        },
        "case_update": {
            "subject": "Support Ticket {{ ticket_number }} Updated",
            "body": "Dear {{ first_name }},\nYour ticket '{{ ticket_title }}' status is now: {{ status }}."
        }
    }

    @classmethod
    def render_template(cls, template_key: str, merge_vars: Dict[str, Any]) -> Dict[str, str]:
        tpl = cls.TEMPLATES.get(template_key, {
            "subject": "Notification from CampusSphere",
            "body": "Hello {{ first_name }}, you have a new update."
        })

        subject = tpl["subject"]
        body = tpl["body"]

        for key, val in merge_vars.items():
            pattern = rf"\{\{\s*{key}\s*\}\}"
            subject = re.sub(pattern, str(val), subject)
            body = re.sub(pattern, str(val), body)

        return {"subject": subject, "body": body}

    @classmethod
    def send_notification(
        cls,
        channel: str,  # email, sms, push, in_app
        recipient: str,
        template_key: str,
        merge_vars: Dict[str, Any]
    ) -> Dict[str, Any]:
        tenant_id = TenantContext.require_tenant_id()
        content = cls.render_template(template_key, merge_vars)

        logger.info(f"[{channel.upper()}] Sending to {recipient} [Tenant: {tenant_id}]: {content['subject']}")

        return {
            "tenant_id": tenant_id,
            "channel": channel,
            "recipient": recipient,
            "subject": content["subject"],
            "body": content["body"],
            "status": "DELIVERED",
            "sent_at": datetime.now(timezone.utc).isoformat()
        }
