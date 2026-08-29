"""
Executive Analytics and KPI Reporting Service.
Aggregates lead conversion funnels, retention trends, and cohort metrics across tenants.
"""

from typing import List, Dict, Any
from datetime import datetime, timezone
from backend.app.schemas.analytics_kpi import ExecutiveKpiReport, ConversionFunnelStage, CohortRetentionMetric

class AnalyticsKpiService:
    @staticmethod
    def calculate_funnel_metrics(
        leads: int,
        counseled: int,
        applied: int,
        admitted: int,
        enrolled: int
    ) -> List[ConversionFunnelStage]:
        stages_data = [
            ("Lead Capture", leads),
            ("Counseling", counseled),
            ("Application", applied),
            ("Admitted", admitted),
            ("Enrolled", enrolled),
        ]
        
        stages: List[ConversionFunnelStage] = []
        base_count = max(leads, 1)
        
        for i, (name, count) in enumerate(stages_data):
            conv_rate = round((count / base_count) * 100.0, 2)
            if i == 0:
                drop_rate = 0.0
            else:
                prev_count = max(stages_data[i - 1][1], 1)
                drop_rate = round(max(0.0, ((prev_count - count) / prev_count) * 100.0), 2)
            
            stages.append(
                ConversionFunnelStage(
                    stage_name=name,
                    count=count,
                    conversion_rate=conv_rate,
                    drop_off_rate=drop_rate
                )
            )
        return stages

    @classmethod
    def generate_executive_report(
        cls,
        tenant_id: str,
        leads: int = 1250,
        counseled: int = 940,
        applied: int = 680,
        admitted: int = 420,
        enrolled: int = 350,
        retention_rate: float = 91.5,
        avg_days: float = 18.4,
        avg_tuition: float = 12500.0
    ) -> ExecutiveKpiReport:
        funnel = cls.calculate_funnel_metrics(leads, counseled, applied, admitted, enrolled)
        overall_conversion = round((enrolled / max(leads, 1)) * 100.0, 2)
        revenue_forecast = round(enrolled * avg_tuition, 2)
        
        return ExecutiveKpiReport(
            tenant_id=tenant_id,
            total_leads=leads,
            total_applications=applied,
            total_enrollments=enrolled,
            overall_conversion_rate=overall_conversion,
            retention_rate=retention_rate,
            average_time_to_enroll_days=avg_days,
            funnel_stages=funnel,
            revenue_forecast=revenue_forecast,
            generated_at=datetime.now(timezone.utc)
        )

    @classmethod
    def analyze_cohort_retention(
        cls,
        cohorts: List[Dict[str, Any]]
    ) -> List[CohortRetentionMetric]:
        metrics = []
        for c in cohorts:
            start = c.get("starting_headcount", 100)
            active = c.get("active_headcount", 90)
            pct = round((active / max(start, 1)) * 100.0, 2)
            
            if pct >= 90.0:
                risk = "LOW"
            elif pct >= 75.0:
                risk = "MODERATE"
            else:
                risk = "CRITICAL"
                
            metrics.append(
                CohortRetentionMetric(
                    cohort_year=c.get("year", 2025),
                    cohort_term=c.get("term", "Fall"),
                    starting_headcount=start,
                    active_headcount=active,
                    retention_rate_pct=pct,
                    risk_level=risk
                )
            )
        return metrics
