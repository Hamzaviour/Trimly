"""
Trimly AI — Production WhatsApp Business API Agent
Official Meta WhatsApp Business Cloud API Integration.
Handles interactive button messages, template reminders, digital PDF receipts, and opt-out processing.
"""
import httpx
from typing import Dict, Any, List, Optional
from core.config import settings


class MetaWhatsAppAgent:
    def __init__(
        self,
        token: str = settings.WHATSAPP_TOKEN,
        phone_number_id: str = settings.WHATSAPP_PHONE_ID,
    ):
        self.token = token
        self.phone_number_id = phone_number_id
        self.api_url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def send_interactive_appointment_reminder(
        self,
        to_phone: str,
        customer_name: str,
        barber_name: str,
        scheduled_time: str,
        service_name: str,
    ) -> Dict[str, Any]:
        """
        Send interactive WhatsApp message with quick action buttons: [Confirm] | [Reschedule] | [Cancel]
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {"type": "text", "text": "💈 Gulshan Barbers Reminder"},
                "body": {
                    "text": (
                        f"Assalam-o-Alaikum {customer_name} bhai!\n"
                        f"Aap ki appointment {barber_name} ke sath {scheduled_time} baje ({service_name}) scheduled hai.\n\n"
                        f"Kya aap time pe aaray hain?"
                    )
                },
                "footer": {"text": "Trimly AI Salon Management • Reply STOP to cancel reminders"},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": "btn_confirm", "title": "✅ Confirm"}},
                        {"type": "reply", "reply": {"id": "btn_reschedule", "title": "📅 Reschedule"}},
                        {"type": "reply", "reply": {"id": "btn_cancel", "title": "❌ Cancel"}},
                    ]
                },
            },
        }

        if not self.token or self.token == "XXXXXXXXXXXX":
            # Mock mode for local dev
            return {
                "status": "SENT_MOCK",
                "provider": "META_WHATSAPP_CLOUD_API",
                "to": to_phone,
                "payload": payload,
            }

        async with httpx.AsyncClient() as client:
            res = await client.post(self.api_url, headers=self.get_headers(), json=payload)
            return res.json()

    async def send_digital_receipt(
        self,
        to_phone: str,
        customer_name: str,
        total_amount: float,
        earned_points: int,
        invoice_pdf_url: str,
    ) -> Dict[str, Any]:
        """Send service summary, earned loyalty points, and digital receipt link."""
        message = (
            f"Shukriya {customer_name} bhai! Gulshan Barbers pe aane ka.\n\n"
            f"🧾 Total Bill: Rs. {total_amount:.0f}\n"
            f"🌟 Earned Loyalty Points: +{earned_points} Pts\n"
            f"📄 Digital Receipt: {invoice_pdf_url}\n\n"
            f"Aap ka agla haircut ~21 din baad diew hai. Have a great day!"
        )

        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message},
        }

        if not self.token or self.token == "XXXXXXXXXXXX":
            return {"status": "SENT_MOCK", "to": to_phone, "message": message}

        async with httpx.AsyncClient() as client:
            res = await client.post(self.api_url, headers=self.get_headers(), json=payload)
            return res.json()
