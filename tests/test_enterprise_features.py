import pytest
from app.core.mfa import MFAEngine
from app.services.communication_service import CommunicationEngine
from app.services.integration_service import IntegrationHubService
from app.services.ml_service import MLIntelligenceService
from app.context import TenantContext


def test_mfa_totp_generation_and_verification():
    secret = MFAEngine.generate_secret()
    assert len(secret) > 10

    code = MFAEngine.generate_totp(secret)
    assert len(code) == 6
    assert MFAEngine.verify_totp(secret, code) is True
    assert MFAEngine.verify_totp(secret, "000000") is False


def test_communication_engine_template_rendering():
    TenantContext.set_tenant_id("tenant-harvard")
    rendered = CommunicationEngine.render_template(
        "lead_welcome",
        {
            "first_name": "Alex",
            "institution_name": "Harvard University",
            "program_name": "Computer Science B.S.",
            "counselor_name": "Sarah Connor"
        }
    )
    assert "Harvard University" in rendered["subject"]
    assert "Alex" in rendered["body"]
    assert "Computer Science B.S." in rendered["body"]
    TenantContext.clear()


def test_integration_canonical_data_mapping():
    # Banner SIS Payload Mapping
    banner_raw = {
        "banner_id": "B00948201",
        "first_name": "Emily",
        "last_name": "Watson",
        "email_address": "emily.watson@example.com",
        "phone_num": "+1-555-9482"
    }
    canonical = IntegrationHubService.map_to_canonical_person("banner_sis", banner_raw)
    assert canonical["first_name"] == "Emily"
    assert canonical["external_id"] == "B00948201"
    assert canonical["provider"] == "banner_sis"


def test_integration_hmac_signature_verification():
    secret = "my-secret-webhook-key"
    payload = b'{"event": "ApplicationSubmitted"}'

    import hmac, hashlib
    expected_sig = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()

    assert IntegrationHubService.verify_webhook_signature(payload, expected_sig, secret) is True
    assert IntegrationHubService.verify_webhook_signature(payload, "invalid_sig", secret) is False


def test_ml_intelligence_service():
    ml = MLIntelligenceService()

    # High fit student conversion probability
    high_prob = ml.predict_conversion_probability(has_academic_interest=True, engagement_score=15.0, custom_fields_count=3)
    low_prob = ml.predict_conversion_probability(has_academic_interest=False, engagement_score=1.0, custom_fields_count=0)

    assert high_prob > low_prob

    # Skill Similarity Matcher
    skill_sim = ml.calculate_skill_similarity(
        candidate_skills=["Python", "SQL", "Machine Learning", "FastAPI"],
        required_skills=["Python", "SQL", "Docker"]
    )
    assert skill_sim == 66.67
