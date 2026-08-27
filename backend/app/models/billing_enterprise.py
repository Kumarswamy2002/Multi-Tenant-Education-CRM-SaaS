"""
Tuition Fee Structures, Invoices, Payment Gateways, Scholarships, and Ledger Transactions.
"""
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, Date, DateTime,
    ForeignKey, Enum, UniqueConstraint, Numeric
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum
from app.models.base_enterprise import BaseModel, Base


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    ISSUED = "issued"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    UPI = "upi"
    ACH = "ach"
    WIRE_TRANSFER = "wire_transfer"
    CHECK = "check"
    CASH = "cash"
    SCHOLARSHIP = "scholarship"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    REFUNDED = "refunded"


class FeeFrequency(str, enum.Enum):
    ONE_TIME = "one_time"
    PER_SEMESTER = "per_semester"
    ANNUAL = "annual"
    MONTHLY = "monthly"
    PER_CREDIT = "per_credit"


class FeeStructure(BaseModel):
    """Institutional Fee Structure (Tuition, Lab, Library, Hostel, Transport, Tech fees)."""
    __tablename__ = "fee_structures"

    program_id = Column(String(36), ForeignKey("academic_programs.id", ondelete="CASCADE"), nullable=True)
    academic_year = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    fee_frequency = Column(Enum(FeeFrequency), default=FeeFrequency.PER_SEMESTER, nullable=False)
    due_day_offset = Column(Integer, default=30)
    is_active = Column(Boolean, default=True, nullable=False)

    fee_items = relationship("FeeStructureItem", back_populates="fee_structure", cascade="all, delete-orphan")
    invoices = relationship("StudentInvoice", back_populates="fee_structure")


class FeeStructureItem(BaseModel):
    """Individual breakdown component within a fee structure."""
    __tablename__ = "fee_structure_items"

    fee_structure_id = Column(String(36), ForeignKey("fee_structures.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False) # Tuition, Lab, Sports, Insurance, Campus Facility
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    is_refundable = Column(Boolean, default=False)
    tax_rate_percent = Column(Float, default=0.0)

    fee_structure = relationship("FeeStructure", back_populates="fee_items")


class StudentInvoice(BaseModel):
    """Invoice billed to a student for academic terms or incidental fees."""
    __tablename__ = "student_invoices"

    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    fee_structure_id = Column(String(36), ForeignKey("fee_structures.id", ondelete="SET NULL"), nullable=True)
    term_id = Column(String(36), ForeignKey("academic_terms.id", ondelete="SET NULL"), nullable=True)
    invoice_number = Column(String(100), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    subtotal_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    paid_amount = Column(Float, default=0.0, nullable=False)
    balance_amount = Column(Float, default=0.0, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.ISSUED, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    late_fee_applied = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)

    fee_structure = relationship("FeeStructure", back_populates="invoices")
    line_items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("PaymentTransaction", back_populates="invoice")

    __table_args__ = (
        UniqueConstraint("tenant_id", "invoice_number", name="uq_invoice_tenant_number"),
    )


class InvoiceLineItem(BaseModel):
    """Line item in a student invoice."""
    __tablename__ = "invoice_line_items"

    invoice_id = Column(String(36), ForeignKey("student_invoices.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(255), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_price = Column(Float, nullable=False)
    tax_percent = Column(Float, default=0.0)

    invoice = relationship("StudentInvoice", back_populates="line_items")


class PaymentTransaction(BaseModel):
    """Payment transaction processed via payment gateway or manual cashier."""
    __tablename__ = "payment_transactions"

    invoice_id = Column(String(36), ForeignKey("student_invoices.id", ondelete="CASCADE"), nullable=True)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    transaction_reference = Column(String(150), nullable=False)
    gateway_name = Column(String(50), nullable=False) # Stripe, Razorpay, PayPal, Cashier
    gateway_transaction_id = Column(String(200), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CREDIT_CARD, nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.COMPLETED, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    gateway_fee = Column(Float, default=0.0)
    gateway_response = Column(JSONB, default=dict)
    receipt_url = Column(String(500), nullable=True)
    failure_reason = Column(String(255), nullable=True)

    invoice = relationship("StudentInvoice", back_populates="payments")


class Scholarship(BaseModel):
    """Financial Aid, Merit Grants, Endowments, and Tuition Waivers."""
    __tablename__ = "scholarships"

    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=False)
    donor_name = Column(String(200), nullable=True)
    total_endowment = Column(Float, default=0.0)
    amount_per_recipient = Column(Float, nullable=False)
    is_percentage_waiver = Column(Boolean, default=False)
    waiver_percentage = Column(Float, default=0.0)
    min_cgpa_requirement = Column(Float, default=3.0)
    eligibility_criteria = Column(JSONB, default=dict)
    max_recipients = Column(Integer, default=50)
    active_year = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    awards = relationship("ScholarshipAward", back_populates="scholarship")


class ScholarshipAward(BaseModel):
    """Scholarship awarded to a student."""
    __tablename__ = "scholarship_awards"

    scholarship_id = Column(String(36), ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(36), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    term_id = Column(String(36), ForeignKey("academic_terms.id", ondelete="SET NULL"), nullable=True)
    awarded_amount = Column(Float, nullable=False)
    disbursement_date = Column(Date, default=date.today, nullable=False)
    status = Column(String(50), default="approved") # approved, disbursed, revoked

    scholarship = relationship("Scholarship", back_populates="awards")
