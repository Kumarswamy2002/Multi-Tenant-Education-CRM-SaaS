"""
Student Retention Analytics & Early Intervention Service
"""
from typing import Dict, Any

class RetentionRiskCalculator:
    @staticmethod
    def calculate_risk(attendance_rate: float, current_gpa: float, lms_logins_per_week: int) -> Dict[str, Any]:
        # Risk score from 0 (Safe) to 100 (High Risk)
        risk = 0.0
        if attendance_rate < 0.75:
            risk += 40.0
        elif attendance_rate < 0.85:
            risk += 20.0

        if current_gpa < 2.0:
            risk += 40.0
        elif current_gpa < 2.8:
            risk += 20.0

        if lms_logins_per_week < 2:
            risk += 20.0

        tier = "HIGH" if risk >= 50 else ("MEDIUM" if risk >= 25 else "LOW")
        return {
            "risk_score": min(100.0, risk),
            "risk_tier": tier,
            "requires_academic_advisor": tier in ["HIGH", "MEDIUM"]
        }
