import pytest
from datetime import datetime, timezone
from app.engine.scoring_engine import LeadScoringEngine
from app.engine.sla_engine import CaseSLAEngine
from app.engine.workflow_engine import WorkflowAutomationEngine
from app.engine.rag_engine import TenantScopedAIEngine
from app.models.crm import Lead, Case
from app.context import TenantContext


def test_lead_scoring_engine():
    lead = Lead(
        tenant_id="tenant-001",
        person_id="p-1",
        academic_interest_program_id="prog-cs-01",
        custom_fields={"high_school": "Central High", "gpa": "3.9"}
    )
    score = LeadScoringEngine.calculate_score(lead, lead_source_name="referral", activities_count=3)
    assert score > 50.0
    assert score <= 100.0


def test_case_sla_engine():
    now = datetime.now(timezone.utc)
    due_urgent = CaseSLAEngine.calculate_due_date("urgent", now)
    due_low = CaseSLAEngine.calculate_due_date("low", now)
    assert (due_urgent - now).total_seconds() == 4 * 3600
    assert (due_low - now).total_seconds() == 48 * 3600


def test_workflow_condition_evaluator():
    cond_tree = {
        "operator": "AND",
        "conditions": [
            {"field": "score", "value": 50, "comparison": "greater_than"},
            {"field": "status", "value": "NEW", "comparison": "equals"}
        ]
    }
    match_payload = {"score": 75, "status": "NEW"}
    fail_payload = {"score": 30, "status": "NEW"}

    assert WorkflowAutomationEngine.evaluate_condition_node(cond_tree, match_payload) is True
    assert WorkflowAutomationEngine.evaluate_condition_node(cond_tree, fail_payload) is False


def test_ai_engine_tenant_scoped():
    TenantContext.set_tenant_id("tenant-harvard")
    res = TenantScopedAIEngine.generate_counselor_assistant_summary(
        prospect_name="Jane Doe",
        academic_interest="Computer Science",
        counseling_notes=["Strong background in Math", "Wants merit scholarship"]
    )
    assert res["tenant_id"] == "tenant-harvard"
    assert "Jane Doe" in res["prospect_name"]
    TenantContext.clear()
