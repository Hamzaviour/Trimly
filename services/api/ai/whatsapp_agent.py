"""
Trimly AI — WhatsApp Automation Agent
Handles automated WhatsApp reminders, invoices, review requests, and opt-out processing.
"""
from typing import Dict, Any, Optional


class WhatsAppAgent:
    def __init__(self, token: str = "mock-token", phone_number_id: str = "mock-id"):
        self.token = token
        self.phone_number_id = phone_number_id

    async def send_appointment_reminder(
        self,
        to_phone: str,
        customer_name: str,
        barber_name: str,
        scheduled_time: str,
        booking_url: str = "https://trimly.pk/q/gulshan",
    ) -> Dict[str, Any]:
        """Send automated appointment reminder via WhatsApp in Roman Urdu."""
        message = (
            f"Assalam-o-Alaikum {customer_name} bhai! 👋\n"
            f"Gulshan Barbers se reminder: Aap ki appointment {barber_name} ke sath {scheduled_time} baje scheduled hai.\n"
            f"Live queue check karne ke liye: {booking_url}\n"
            f"Reply STOP to unsubscribe."
        )
        return {
            "status": "SENT",
            "provider": "WHATSAPP",
            "to": to_phone,
            "message": message,
        }

    async def send_invoice_pdf(
        self,
        to_phone: str,
        customer_name: str,
        total_amount: float,
        invoice_pdf_url: str,
    ) -> Dict[str, Any]:
        """Send digital receipt & invoice PDF after service completion."""
        message = (
            f"Shukriya {customer_name} bhai! Gulshan Barbers pe aane ka.\n"
            f"Aap ka kul bill: Rs. {total_amount:.0f}.\n"
            f"Digital invoice download karein: {invoice_pdf_url}\n"
            f"Aap ko 10 Loyalty Points mile hain! 🌟"
        )
        return {
            "status": "SENT",
            "provider": "WHATSAPP",
            "to": to_phone,
            "message": message,
        }

    async def handle_opt_out(self, from_phone: str, user_message: str) -> bool:
        """Check if customer replied STOP / nahi / na."""
        text = user_message.strip().lower()
        if text in ["stop", "unsubscribe", "nahi", "na", "mat karo"]:
            # In production: update customer.whatsapp_consent = False in DB
            return True
        return False
