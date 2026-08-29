import pytest
from backend.app.schemas.notification_dispatcher import (
    NotificationPayload,
    ChannelType,
    DispatchPriority,
    DispatchStatus,
)
from backend.app.services.notification_dispatcher_service import NotificationDispatcherService

def test_template_rendering_and_single_dispatch():
    dispatcher = NotificationDispatcherService(tenant_id="tenant_harvard")
    payload = NotificationPayload(
        recipient_id="usr_101",
        recipient_destination="john@harvard.edu",
        channel=ChannelType.EMAIL,
        priority=DispatchPriority.NORMAL,
        template_key="admissions.welcome",
        template_context={
            "first_name": "John",
            "institution_name": "Harvard University",
            "application_id": "APP-2026-99"
        }
    )
    receipt = dispatcher.dispatch(payload)
    assert receipt.status == DispatchStatus.DELIVERED
    assert "Hello John, welcome to Harvard University!" in receipt.rendered_body
    assert "APP-2026-99" in receipt.rendered_body
    assert len(dispatcher.get_history()) == 1

def test_custom_template_registration():
    dispatcher = NotificationDispatcherService(tenant_id="tenant_oxford")
    dispatcher.register_template("custom.survey", "Hi {{name}}, please rate your advisor {{advisor_name}}.")
    payload = NotificationPayload(
        recipient_id="usr_202",
        recipient_destination="+15551234567",
        channel=ChannelType.SMS,
        priority=DispatchPriority.LOW,
        template_key="custom.survey",
        template_context={"name": "Alice", "advisor_name": "Dr. Watson"}
    )
    receipt = dispatcher.dispatch(payload)
    assert receipt.status == DispatchStatus.DELIVERED
    assert receipt.rendered_body == "Hi Alice, please rate your advisor Dr. Watson."

def test_bulk_priority_dispatch():
    dispatcher = NotificationDispatcherService(tenant_id="tenant_mit")
    p1 = NotificationPayload(
        recipient_id="usr_1",
        recipient_destination="u1@mit.edu",
        channel=ChannelType.EMAIL,
        priority=DispatchPriority.LOW,
        template_key="payment.reminder",
        template_context={"first_name": "Bob", "amount": "500", "due_date": "2026-09-01"}
    )
    p2 = NotificationPayload(
        recipient_id="usr_2",
        recipient_destination="+1999888777",
        channel=ChannelType.SMS,
        priority=DispatchPriority.URGENT,
        template_key="emergency.broadcast",
        template_context={"alert_message": "Tornado Warning"}
    )
    
    receipts = dispatcher.dispatch_bulk([p1, p2])
    assert len(receipts) == 2
    # Urgent first in processed order
    assert receipts[0].recipient_id == "usr_2"
    assert "EMERGENCY ALERT" in receipts[0].rendered_body
    assert receipts[1].recipient_id == "usr_1"
