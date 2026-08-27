"""
Comprehensive Billing, Invoicing, Payment Gateway Reconciliations, and Scholarships Service.
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from fastapi import HTTPException

from backend.app.models.billing_enterprise import (
    FeeStructure, FeeStructureItem, StudentInvoice, InvoiceLineItem,
    PaymentTransaction, Scholarship, ScholarshipAward,
    InvoiceStatus, PaymentMethod, TransactionStatus
)
from backend.app.schemas.billing_enterprise import (
    FeeStructureCreate, StudentInvoiceCreate, PaymentTransactionCreate, ScholarshipCreate
)


class BillingService:
    def __init__(self, db: Session, tenant_id: str, current_user_id: Optional[str] = None):
        self.db = db
        self.tenant_id = tenant_id
        self.current_user_id = current_user_id

    def create_fee_structure(self, data: FeeStructureCreate) -> FeeStructure:
        total_calc = sum(item.amount for item in data.items)
        fee_struct = FeeStructure(
            tenant_id=self.tenant_id,
            program_id=data.program_id,
            academic_year=data.academic_year,
            name=data.name,
            code=data.code,
            currency=data.currency,
            total_amount=total_calc,
            fee_frequency=data.fee_frequency,
            due_day_offset=data.due_day_offset,
            created_by_id=self.current_user_id
        )
        self.db.add(fee_struct)
        self.db.flush()

        for item in data.items:
            fee_item = FeeStructureItem(
                tenant_id=self.tenant_id,
                fee_structure_id=fee_struct.id,
                category=item.category,
                description=item.description,
                amount=item.amount,
                is_mandatory=item.is_mandatory,
                is_refundable=item.is_refundable,
                tax_rate_percent=item.tax_rate_percent,
                created_by_id=self.current_user_id
            )
            self.db.add(fee_item)

        self.db.commit()
        self.db.refresh(fee_struct)
        return fee_struct

    def generate_invoice_for_student(self, data: StudentInvoiceCreate) -> StudentInvoice:
        subtotal = sum(item.total_price for item in data.line_items)
        tax = sum((item.total_price * (item.tax_percent / 100.0)) for item in data.line_items)
        total = (subtotal + tax) - data.discount_amount
        if total < 0:
            total = 0.0

        invoice_seq = self.db.query(func.count(StudentInvoice.id)).filter(
            StudentInvoice.tenant_id == self.tenant_id
        ).scalar() or 0
        invoice_number = f"INV-{date.today().year}-{invoice_seq + 1001}"

        invoice = StudentInvoice(
            tenant_id=self.tenant_id,
            student_id=data.student_id,
            fee_structure_id=data.fee_structure_id,
            term_id=data.term_id,
            invoice_number=invoice_number,
            issue_date=date.today(),
            due_date=data.due_date,
            subtotal_amount=subtotal,
            discount_amount=data.discount_amount,
            tax_amount=tax,
            total_amount=total,
            paid_amount=0.0,
            balance_amount=total,
            status=InvoiceStatus.ISSUED,
            currency="USD",
            notes=data.notes,
            created_by_id=self.current_user_id
        )
        self.db.add(invoice)
        self.db.flush()

        for line in data.line_items:
            line_item = InvoiceLineItem(
                tenant_id=self.tenant_id,
                invoice_id=invoice.id,
                description=line.description,
                unit_price=line.unit_price,
                quantity=line.quantity,
                total_price=line.total_price,
                tax_percent=line.tax_percent,
                created_by_id=self.current_user_id
            )
            self.db.add(line_item)

        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def record_payment(self, data: PaymentTransactionCreate) -> PaymentTransaction:
        ref_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        payment = PaymentTransaction(
            tenant_id=self.tenant_id,
            invoice_id=data.invoice_id,
            student_id=data.student_id,
            transaction_reference=ref_id,
            gateway_name=data.gateway_name,
            gateway_transaction_id=data.gateway_transaction_id or f"GATEWAY-{uuid.uuid4().hex[:8]}",
            amount=data.amount,
            currency=data.currency,
            payment_method=data.payment_method,
            status=TransactionStatus.COMPLETED,
            payment_date=datetime.now(timezone.utc),
            created_by_id=self.current_user_id
        )
        self.db.add(payment)

        if data.invoice_id:
            invoice = self.db.query(StudentInvoice).filter(
                StudentInvoice.tenant_id == self.tenant_id,
                StudentInvoice.id == data.invoice_id
            ).first()
            if invoice:
                invoice.paid_amount += data.amount
                invoice.balance_amount = invoice.total_amount - invoice.paid_amount
                if invoice.balance_amount <= 0.01:
                    invoice.balance_amount = 0.0
                    invoice.status = InvoiceStatus.PAID
                else:
                    invoice.status = InvoiceStatus.PARTIALLY_PAID

        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_student_invoices(self, student_id: str) -> List[StudentInvoice]:
        return self.db.query(StudentInvoice).filter(
            StudentInvoice.tenant_id == self.tenant_id,
            StudentInvoice.student_id == student_id,
            StudentInvoice.is_deleted == False
        ).order_by(StudentInvoice.issue_date.desc()).all()
