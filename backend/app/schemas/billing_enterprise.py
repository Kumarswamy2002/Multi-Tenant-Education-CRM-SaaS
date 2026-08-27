"""
Pydantic Schemas for Tuition Billing, Fee Structures, Invoices, Payments, and Scholarships.
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from pydantic import Field
from app.schemas.base_enterprise import BaseSchema, AuditSchema
from app.models.billing_enterprise import InvoiceStatus, PaymentMethod, TransactionStatus, FeeFrequency


class FeeStructureItemSchema(BaseSchema):
    category: str
    description: str
    amount: float
    is_mandatory: bool = True
    is_refundable: bool = False
    tax_rate_percent: float = 0.0


class FeeStructureCreate(BaseSchema):
    program_id: Optional[str] = None
    academic_year: str
    name: str
    code: str
    currency: str = "USD"
    fee_frequency: FeeFrequency = FeeFrequency.PER_SEMESTER
    due_day_offset: int = 30
    items: List[FeeStructureItemSchema] = Field(default_factory=list)


class FeeStructureRead(AuditSchema):
    program_id: Optional[str] = None
    academic_year: str
    name: str
    code: str
    currency: str
    total_amount: float
    fee_frequency: FeeFrequency
    due_day_offset: int
    is_active: bool
    fee_items: List[FeeStructureItemSchema] = Field(default_factory=list)


class InvoiceLineItemSchema(BaseSchema):
    description: str
    unit_price: float
    quantity: int = 1
    total_price: float
    tax_percent: float = 0.0


class StudentInvoiceCreate(BaseSchema):
    student_id: str
    fee_structure_id: Optional[str] = None
    term_id: Optional[str] = None
    due_date: date
    line_items: List[InvoiceLineItemSchema]
    discount_amount: float = 0.0
    notes: Optional[str] = None


class StudentInvoiceRead(AuditSchema):
    student_id: str
    fee_structure_id: Optional[str] = None
    term_id: Optional[str] = None
    invoice_number: str
    issue_date: date
    due_date: date
    subtotal_amount: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance_amount: float
    status: InvoiceStatus
    currency: str
    late_fee_applied: float
    notes: Optional[str] = None
    line_items: List[InvoiceLineItemSchema] = Field(default_factory=list)
    student_name: Optional[str] = None


class PaymentTransactionCreate(BaseSchema):
    invoice_id: Optional[str] = None
    student_id: str
    amount: float
    currency: str = "USD"
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    gateway_name: str = "Stripe"
    gateway_transaction_id: Optional[str] = None
    notes: Optional[str] = None


class PaymentTransactionRead(AuditSchema):
    invoice_id: Optional[str] = None
    student_id: str
    transaction_reference: str
    gateway_name: str
    gateway_transaction_id: Optional[str] = None
    amount: float
    currency: str
    payment_method: PaymentMethod
    status: TransactionStatus
    payment_date: datetime
    gateway_fee: float
    receipt_url: Optional[str] = None
    failure_reason: Optional[str] = None


class ScholarshipCreate(BaseSchema):
    name: str
    code: str
    donor_name: Optional[str] = None
    total_endowment: float = 0.0
    amount_per_recipient: float
    is_percentage_waiver: bool = False
    waiver_percentage: float = 0.0
    min_cgpa_requirement: float = 3.0
    eligibility_criteria: Dict[str, Any] = Field(default_factory=dict)
    max_recipients: int = 50
    active_year: str


class ScholarshipRead(AuditSchema):
    name: str
    code: str
    donor_name: Optional[str] = None
    total_endowment: float
    amount_per_recipient: float
    is_percentage_waiver: bool
    waiver_percentage: float
    min_cgpa_requirement: float
    eligibility_criteria: Dict[str, Any]
    max_recipients: int
    active_year: str
    is_active: bool
