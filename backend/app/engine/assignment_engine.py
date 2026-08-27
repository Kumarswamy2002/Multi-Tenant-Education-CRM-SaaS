from typing import List, Optional
import random
from app.models.person import CounselorProfile


class CounselorAssignmentEngine:
    """
    Assigns leads to active admissions counselors using round-robin and capacity balancing algorithms.
    """

    @staticmethod
    def assign_counselor_round_robin(counselors: List[CounselorProfile]) -> Optional[str]:
        if not counselors:
            return None
        # Select counselor with lowest current load
        selected = min(counselors, key=lambda c: int(c.assigned_lead_capacity or 100))
        return selected.person_id
