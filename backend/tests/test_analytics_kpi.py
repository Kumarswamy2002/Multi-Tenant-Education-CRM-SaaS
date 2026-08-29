import pytest
from backend.app.services.analytics_kpi_service import AnalyticsKpiService

def test_funnel_metrics_calculation():
    stages = AnalyticsKpiService.calculate_funnel_metrics(
        leads=1000, counseled=800, applied=500, admitted=300, enrolled=250
    )
    assert len(stages) == 5
    assert stages[0].stage_name == "Lead Capture"
    assert stages[0].conversion_rate == 100.0
    assert stages[-1].stage_name == "Enrolled"
    assert stages[-1].count == 250
    assert stages[-1].conversion_rate == 25.0

def test_executive_kpi_report():
    report = AnalyticsKpiService.generate_executive_report(
        tenant_id="tenant-alpha",
        leads=2000,
        counseled=1500,
        applied=1000,
        admitted=600,
        enrolled=500,
        retention_rate=94.2
    )
    assert report.tenant_id == "tenant-alpha"
    assert report.total_leads == 2000
    assert report.total_enrollments == 500
    assert report.overall_conversion_rate == 25.0
    assert report.retention_rate == 94.2
    assert report.revenue_forecast == 500 * 12500.0

def test_cohort_retention_risk_levels():
    cohort_data = [
        {"year": 2024, "term": "Fall", "starting_headcount": 200, "active_headcount": 190},
        {"year": 2023, "term": "Fall", "starting_headcount": 200, "active_headcount": 160},
        {"year": 2022, "term": "Fall", "starting_headcount": 200, "active_headcount": 120},
    ]
    results = AnalyticsKpiService.analyze_cohort_retention(cohort_data)
    assert len(results) == 3
    assert results[0].risk_level == "LOW"
    assert results[1].risk_level == "MODERATE"
    assert results[2].risk_level == "CRITICAL"
