from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
from enum import Enum

class ChannelType(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"
    WHATSAPP = "WHATSAPP"

class DispatchPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

class DispatchStatus(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"

class NotificationPayload(BaseModel):
    recipient_id: str
    recipient_destination: str  # email, phone, or push token
    channel: ChannelType
    priority: DispatchPriority = DispatchPriority.NORMAL
    template_key: str
    template_context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DispatchReceipt(BaseModel):
    dispatch_id: str
    tenant_id: str
    recipient_id: str
    channel: ChannelType
    status: DispatchStatus
    rendered_body: str
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_message: Optional[str] = None
