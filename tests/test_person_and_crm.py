import pytest
from app.models.person import Person, StudentProfile
from app.models.crm import Lead
from app.models.relationship import Relationship
from app.context import TenantContext


def test_person_single_model_instantiation():
    TenantContext.set_tenant_id("tenant-harvard")

    # Single Person model for prospective applicant
    person = Person(
        first_name="Alex",
        last_name="Johnson",
        email="alex.johnson@example.com",
        primary_role="prospect"
    )
    assert person.tenant_id == "tenant-harvard"
    assert person.first_name == "Alex"
    assert person.primary_role == "prospect"

    # Single Person model updated to student role
    person.primary_role = "student"
    student_profile = StudentProfile(
        tenant_id="tenant-harvard",
        person_id="person-001",
        student_identifier="STU-1001",
        enrollment_status="enrolled"
    )
    assert student_profile.tenant_id == "tenant-harvard"
    assert student_profile.student_identifier == "STU-1001"

    TenantContext.clear()


def test_relationship_edge_creation():
    TenantContext.set_tenant_id("tenant-harvard")

    rel = Relationship(
        source_id="person-student-001",
        source_type="person",
        relationship_type="HAS_PARENT",
        target_id="person-parent-001",
        target_type="person"
    )
    assert rel.tenant_id == "tenant-harvard"
    assert rel.relationship_type == "HAS_PARENT"

    TenantContext.clear()
