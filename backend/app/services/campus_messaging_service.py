"""
Campus Multichannel Messaging Gateway
"""
from typing import Dict, Any, List
import time

class CampusMessagingGateway:
    SUPPORTED_CHANNELS = ["email", "sms", "push_notification"]

    @classmethod
    def dispatch_alert(cls, channel: str, recipient: str, title: str, content: str) -> Dict[str, Any]:
        if channel not in cls.SUPPORTED_CHANNELS:
            raise ValueError(f"Unsupported channel: {channel}")
        return {
            "message_id": f"msg_{int(time.time()*1000)}",
            "channel": channel,
            "recipient": recipient,
            "status": "QUEUED",
            "title": title,
            "dispatched_at": time.time()
        }
