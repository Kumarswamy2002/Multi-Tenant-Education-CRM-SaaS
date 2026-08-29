from backend.app.services.campus_messaging_service import CampusMessagingGateway

def test_messaging_dispatch():
    res = CampusMessagingGateway.dispatch_alert("sms", "+15551234567", "Exam Notice", "Midterm starts tomorrow at 9 AM.")
    assert res["status"] == "QUEUED"
    assert res["channel"] == "sms"
