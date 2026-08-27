from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit import AuditEvent
from app.context import TenantContext


class AuditService:
    """
    Central Audit Service capturing security and data modification operations
    (WHO, WHAT, WHEN, WHERE, BEFORE, AFTER, REASON).
    """

    @staticmethod
    async def log_event(
        db: AsyncSession,
        action: str,
        entity_type: str,
        entity_id: str,
        before_state: Optional[Dict[str, Any]] = None,
        after_state: Optional[Dict[str, Any]] = None,
        reason: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AuditEvent:
        tenant_id = TenantContext.require_tenant_id()
        user_id = TenantContext.get_user_id()

        audit_ev = AuditEvent(
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            user_agent=user_agent,
            before_state=before_state,
            after_state=after_state,
            reason=reason,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(audit_ev)
        await db.flush()
        return audit_ev
