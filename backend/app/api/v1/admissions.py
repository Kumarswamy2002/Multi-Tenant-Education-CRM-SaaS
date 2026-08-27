import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.core.security import get_current_user
from app.context import TenantContext
from app.models.crm import Lead
from app.models.person import Person, StudentProfile, ApplicantProfile
from app.models.admissions import (
    CounselingSession, Application, ApplicationDocument, OfferLetter
)
from app.models.relationship import Relationship
from app.models.timeline import TimelineEvent
from app.schemas.admissions import (
    CounselingSessionCreate, ApplicationCreate, ApplicationResponse,
    DocumentCreate, DocumentResponse
)

router = APIRouter(prefix="/admissions", tags=["Counseling & Admissions"])


@router.post("/counseling", status_code=status.HTTP_201_CREATED)
async def record_counseling_session(
    payload: CounselingSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    session = CounselingSession(
        tenant_id=tenant_id,
        lead_id=payload.lead_id,
        counselor_person_id=payload.counselor_person_id,
        session_date=payload.session_date,
        notes=payload.notes,
        academic_background=payload.academic_background,
        career_interests=payload.career_interests,
        recommended_program_ids=payload.recommended_program_ids
    )
    db.add(session)

    # Update Lead status
    lead_stmt = select(Lead).where(Lead.id == payload.lead_id, Lead.tenant_id == tenant_id)
    lead_res = await db.execute(lead_stmt)
    lead = lead_res.scalars().first()
    if lead:
        lead.status = "COUNSELING"

        # Record timeline event
        tl = TimelineEvent(
            tenant_id=tenant_id,
            entity_id=lead.person_id,
            entity_type="lead",
            event_type="CounsellingCompleted",
            title="Counseling Session Completed",
            description=f"Counseling recorded by counselor {payload.counselor_person_id}.",
            occurred_at=datetime.now(timezone.utc),
            payload={"notes": payload.notes}
        )
        db.add(tl)

    await db.commit()
    return {"message": "Counseling session recorded successfully", "id": session.id}


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    payload: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()
    app_num = f"APP-{uuid.uuid4().hex[:8].upper()}"

    app_obj = Application(
        tenant_id=tenant_id,
        application_number=app_num,
        applicant_person_id=payload.applicant_person_id,
        program_id=payload.program_id,
        entry_term=payload.entry_term,
        status="SUBMITTED",
        submission_date=datetime.now(timezone.utc),
        form_data=payload.form_data
    )
    db.add(app_obj)

    # Record Timeline Event
    tl = TimelineEvent(
        tenant_id=tenant_id,
        entity_id=payload.applicant_person_id,
        entity_type="application",
        event_type="ApplicationSubmitted",
        title="Application Submitted",
        description=f"Application {app_num} submitted for program {payload.program_id}.",
        occurred_at=datetime.now(timezone.utc),
        payload={"application_number": app_num, "program_id": payload.program_id}
    )
    db.add(tl)

    await db.commit()
    await db.refresh(app_obj)
    return app_obj


@router.post("/applications/{application_id}/convert-to-student")
async def convert_applicant_to_student(
    application_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tenant_id = TenantContext.require_tenant_id()

    # 1. Fetch Application
    app_stmt = select(Application).where(Application.id == application_id, Application.tenant_id == tenant_id)
    app_res = await db.execute(app_stmt)
    app_obj = app_res.scalars().first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    # 2. Update Person primary role
    person_stmt = select(Person).where(Person.id == app_obj.applicant_person_id, Person.tenant_id == tenant_id)
    person_res = await db.execute(person_stmt)
    person = person_res.scalars().first()
    if person:
        person.primary_role = "student"

    # 3. Create Student Profile
    student_id_num = f"STU-{uuid.uuid4().hex[:6].upper()}"
    student_profile = StudentProfile(
        tenant_id=tenant_id,
        person_id=app_obj.applicant_person_id,
        student_identifier=student_id_num,
        enrollment_status="enrolled",
        academic_program_id=app_obj.program_id,
        admission_year="2026",
        expected_graduation_year="2030"
    )
    db.add(student_profile)

    # 4. Create Graph Edge: Student ENROLLED_IN Program
    rel = Relationship(
        tenant_id=tenant_id,
        source_id=app_obj.applicant_person_id,
        source_type="person",
        relationship_type="ENROLLED_IN",
        target_id=app_obj.program_id,
        target_type="program",
        status="active"
    )
    db.add(rel)

    # 5. Update Application Status
    app_obj.status = "ENROLLED"

    # 6. Publish Timeline Event
    tl = TimelineEvent(
        tenant_id=tenant_id,
        entity_id=app_obj.applicant_person_id,
        entity_type="student",
        event_type="EnrollmentCompleted",
        title="Student Enrolled",
        description=f"Applicant converted to student with ID {student_id_num}.",
        occurred_at=datetime.now(timezone.utc),
        payload={"student_identifier": student_id_num, "program_id": app_obj.program_id}
    )
    db.add(tl)

    await db.commit()
    return {
        "message": "Applicant successfully converted to student",
        "student_identifier": student_id_num,
        "person_id": app_obj.applicant_person_id
    }
