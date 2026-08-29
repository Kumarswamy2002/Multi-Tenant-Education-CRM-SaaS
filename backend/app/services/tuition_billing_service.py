"""
Tuition Billing & Invoicing Engine
"""
from decimal import Decimal
from typing import List, Dict, Any

class TuitionBillingService:
    @staticmethod
    def generate_invoice(student_id: str, credit_hours: int, cost_per_credit: float, scholarship_amount: float = 0.0) -> Dict[str, Any]:
        gross_tuition = Decimal(str(credit_hours)) * Decimal(str(cost_per_credit))
        aid = Decimal(str(scholarship_amount))
        net_payable = max(Decimal("0.0"), gross_tuition - aid)
        return {
            "student_id": student_id,
            "credit_hours": credit_hours,
            "gross_tuition": float(gross_tuition),
            "financial_aid_offset": float(aid),
            "net_tuition_due": float(net_payable),
            "status": "ISSUED" if net_payable > 0 else "PAID_BY_AID"
        }
