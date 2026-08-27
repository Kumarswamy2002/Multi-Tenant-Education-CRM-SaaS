import math
from typing import Dict, Any
from app.models.crm import Lead


class LeadScoringEngine:
    """
    Calculates lead scores based on profile completeness, academic fit, engagement activities,
    and lead source quality score.
    """

    SOURCE_WEIGHTS = {
        "referral": 35.0,
        "website_form": 25.0,
        "education_fair": 20.0,
        "social_ad": 15.0,
        "cold_import": 5.0,
    }

    @classmethod
    def calculate_score(cls, lead: Lead, lead_source_name: str = "website_form", activities_count: int = 0) -> float:
        base_score = 10.0

        # 1. Source Quality Weight
        source_score = cls.SOURCE_WEIGHTS.get(lead_source_name.lower(), 15.0)

        # 2. Academic Fit Weight
        program_fit_score = 30.0 if lead.academic_interest_program_id else 5.0

        # 3. Engagement Activity Weight (Diminishing marginal returns)
        engagement_score = min(35.0, math.log1p(activities_count) * 15.0)

        # 4. Profile Completeness Weight
        custom_fields_filled = len(lead.custom_fields.keys()) if lead.custom_fields else 0
        completeness_score = min(20.0, custom_fields_filled * 5.0)

        total_score = base_score + source_score + program_fit_score + engagement_score + completeness_score
        return round(min(100.0, total_score), 2)
