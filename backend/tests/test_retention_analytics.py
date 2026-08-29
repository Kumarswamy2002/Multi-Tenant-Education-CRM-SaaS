from backend.app.services.retention_analytics_service import RetentionRiskCalculator

def test_retention_risk_safe():
    res = RetentionRiskCalculator.calculate_risk(0.95, 3.8, 5)
    assert res["risk_tier"] == "LOW"
    assert res["requires_academic_advisor"] is False

def test_retention_risk_high():
    res = RetentionRiskCalculator.calculate_risk(0.60, 1.8, 1)
    assert res["risk_tier"] == "HIGH"
    assert res["requires_academic_advisor"] is True
