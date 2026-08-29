from backend.app.services.tuition_billing_service import TuitionBillingService

def test_tuition_invoice_generation():
    inv = TuitionBillingService.generate_invoice("stu-88", 15, 300.0, 1000.0)
    assert inv["gross_tuition"] == 4500.0
    assert inv["financial_aid_offset"] == 1000.0
    assert inv["net_tuition_due"] == 3500.0
    assert inv["status"] == "ISSUED"
