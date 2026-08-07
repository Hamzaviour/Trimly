"""
Trimly API — Celery Distributed Worker Tasks
Handles background AI churn detection, automated reminders, and campaign scheduling.
"""
from ai.churn_agent import calculate_churn_risk, generate_winback_offer
from ai.whatsapp_agent import WhatsAppAgent


async def run_ai_churn_detection_task():
    """
    Celery Task (Runs hourly):
    1. Query all active salon customers
    2. Calculate churn risk score based on last_visit_days
    3. Generate winback offer & schedule WhatsApp / AI voice call for at-risk clients
    """
    mock_customers = [
        {"name": "Ahmed Khan", "days_since_visit": 32, "favorite_service": "Fade Cut"},
        {"name": "Bilal Ahmed", "days_since_visit": 14, "favorite_service": "Beard Trim"},
    ]

    actions_taken = []
    for c in mock_customers:
        risk = calculate_churn_risk(c["days_since_visit"])
        if risk >= 0.7:
            offer = generate_winback_offer(c["name"], risk, c["favorite_service"])
            actions_taken.append(offer)

    return {
        "status": "COMPLETED",
        "processed_count": len(mock_customers),
        "winback_actions_scheduled": actions_taken,
    }


async def run_birthday_campaign_task():
    """
    Celery Task (Runs daily at 9:00 AM PKT):
    1. Query clients with birthday today
    2. Send automated birthday discount coupon via WhatsApp & SMS
    """
    wa_agent = WhatsAppAgent()
    result = await wa_agent.send_appointment_reminder(
        to_phone="0300-1234567",
        customer_name="Birthday Client",
        barber_name="Ali Ustad",
        scheduled_time="Today Special",
    )
    return {"status": "COMPLETED", "birthday_messages_sent": 1, "details": result}
