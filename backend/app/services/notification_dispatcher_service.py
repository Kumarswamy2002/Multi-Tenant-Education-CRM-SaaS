"""
Omni-Channel Notification Hub & Dispatcher Service.
Handles template interpolation, priority queue simulation, and multi-channel routing.
"""

import uuid
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from backend.app.schemas.notification_dispatcher import (
    NotificationPayload,
    DispatchReceipt,
    ChannelType,
    DispatchStatus,
    DispatchPriority,
)

class NotificationDispatcherService:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._templates: Dict[str, str] = {
            "admissions.welcome": "Hello {{first_name}}, welcome to {{institution_name}}! Your application ID is {{application_id}}.",
            "payment.reminder": "Dear {{first_name}}, a tuition invoice of ${{amount}} is due on {{due_date}}.",
            "student.grade_alert": "Grade posted for {{course_code}}: {{grade_letter}}.",
            "emergency.broadcast": "EMERGENCY ALERT: {{alert_message}}. Please follow safety protocol immediately."
        }
        self._sent_receipts: List[DispatchReceipt] = []

    def register_template(self, key: str, raw_template: str) -> None:
        self._templates[key] = raw_template

    def render_template(self, template_key: str, context: Dict[str, Any]) -> str:
        raw = self._templates.get(template_key)
        if not raw:
            raise ValueError(f"Template '{template_key}' not registered for tenant {self.tenant_id}")
        
        def replace_var(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, f"{{{{{var_name}}}}}"))

        return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", replace_var, raw)

    def dispatch(self, payload: NotificationPayload) -> DispatchReceipt:
        dispatch_id = f"disp_{uuid.uuid4().hex[:12]}"
        
        try:
            rendered = self.render_template(payload.template_key, payload.template_context)
            receipt = DispatchReceipt(
                dispatch_id=dispatch_id,
                tenant_id=self.tenant_id,
                recipient_id=payload.recipient_id,
                channel=payload.channel,
                status=DispatchStatus.DELIVERED,
                rendered_body=rendered,
                sent_at=datetime.now(timezone.utc),
                error_message=None
            )
        except Exception as ex:
            receipt = DispatchReceipt(
                dispatch_id=dispatch_id,
                tenant_id=self.tenant_id,
                recipient_id=payload.recipient_id,
                channel=payload.channel,
                status=DispatchStatus.FAILED,
                rendered_body="",
                sent_at=datetime.now(timezone.utc),
                error_message=str(ex)
            )

        self._sent_receipts.append(receipt)
        return receipt

    def dispatch_bulk(self, payloads: List[NotificationPayload]) -> List[DispatchReceipt]:
        # Sort by priority before dispatch
        priority_order = {
            DispatchPriority.URGENT: 0,
            DispatchPriority.HIGH: 1,
            DispatchPriority.NORMAL: 2,
            DispatchPriority.LOW: 3
        }
        sorted_payloads = sorted(payloads, key=lambda p: priority_order.get(p.priority, 2))
        return [self.dispatch(p) for p in sorted_payloads]

    def get_history(self) -> List[DispatchReceipt]:
        return list(self._sent_receipts)
