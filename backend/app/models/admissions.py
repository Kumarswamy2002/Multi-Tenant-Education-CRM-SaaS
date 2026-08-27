from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Boolean, Float
from app.models.base import TenantBaseModel


class CounselingSession(TenantBaseModel):
    __tablename__ = "counseling_sessions"

    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    counselor_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    session_date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(String(2000), nullable=True)
    academic_background = Column(JSON, default=dict, nullable=False)
    career_interests = Column(JSON, default=list, nullable=False)
    recommended_program_ids = Column(JSON, default=list, nullable=False)
    status = Column(String(50), default="completed", nullable=False)


class Application(TenantBaseModel):
    __tablename__ = "applications"

    application_number = Column(String(50), unique=True, index=True, nullable=False)
    applicant_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(String(36), ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    entry_term = Column(String(50), nullable=False)
    status = Column(String(50), default="SUBMITTED", index=True, nullable=False)  # DRAFT, SUBMITTED, UNDER_REVIEW, DOCS_PENDING, ELIGIBLE, OFFERED, ACCEPTED, REJECTED, ENROLLED
    submission_date = Column(DateTime(timezone=True), nullable=True)
    form_data = Column(JSON, default=dict, nullable=False)
    is_documents_verified = Column(Boolean, default=False, nullable=False)


class ApplicationDocument(TenantBaseModel):
    __tablename__ = "application_documents"

    application_id = Column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String(100), nullable=False)  # transcript, passport, recommendation_letter, resume, portfolio
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size_bytes = Column(String(50), nullable=True)
    verification_status = Column(String(50), default="PENDING", nullable=False)  # PENDING, VERIFIED, REJECTED
    verifier_person_id = Column(String(36), nullable=True)
    rejection_reason = Column(String(500), nullable=True)


class ApplicationReview(TenantBaseModel):
    __tablename__ = "application_reviews"

    application_id = Column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    reviewer_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=True)
    recommendation = Column(String(50), nullable=False)  # approve, reject, waitlist, request_more_info
    comments = Column(String(2000), nullable=True)


class OfferLetter(TenantBaseModel):
    __tablename__ = "offer_letters"

    application_id = Column(String(36), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    applicant_person_id = Column(String(36), ForeignKey("people.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(String(36), ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    offer_date = Column(DateTime(timezone=True), nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=False)
    tuition_amount = Column(String(50), nullable=False)
    scholarship_amount = Column(String(50), default="0", nullable=False)
    status = Column(String(50), default="OFFERED", nullable=False)  # OFFERED, ACCEPTED, DECLINED, EXPIRED


class SeatAllocation(TenantBaseModel):
    __tablename__ = "seat_allocations"

    program_id = Column(String(36), ForeignKey("programs.id", ondelete="CASCADE"), nullable=False)
    entry_term = Column(String(50), nullable=False)
    total_capacity = Column(Float, default=100, nullable=False)
    allocated_seats = Column(Float, default=0, nullable=False)
    confirmed_seats = Column(Float, default=0, nullable=False)
