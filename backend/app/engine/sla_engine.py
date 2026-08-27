from datetime import datetime, timedelta, timezone
from app.models.crm import Case


class CaseSLAEngine:
    """
    Calculates target resolution dates and SLA statuses based on priority levels.
    """

    SLA_HOURS = {
        "urgent": 4,
        "high": 12,
        "medium": 24,
        "low": 48
    }

    @classmethod
    def calculate_due_date(cls, priority: str, created_at: datetime) -> datetime:
        hours = cls.SLA_HOURS.get(priority.lower(), 24)
        return created_at + timedelta(hours=hours)

    @classmethod
    def is_sla_breached(cls, case_obj: Case) -> bool:
        if case_obj.status in ["RESOLVED", "CLOSED"]:
            return False
        due = cls.calculate_due_date(case_obj.priority, case_obj.created_at)
        return datetime.now(timezone.utc) > due
