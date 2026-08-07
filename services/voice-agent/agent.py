"""
Trimly Voice Agent Service — ElevenLabs Conversational AI & OpenAI Realtime Integration
Handles incoming & outgoing Urdu/Punjabi phone calls for salon booking.
"""
from typing import Dict, Any, Optional


class ElevenLabsVoiceAgent:
    def __init__(self, api_key: str = "mock-key", agent_id: str = "mock-agent-id"):
        self.api_key = api_key
        self.agent_id = agent_id

    def build_customer_context_prompt(
        self,
        customer_name: str,
        last_service: str,
        favorite_barber: str,
        days_since_visit: int,
    ) -> str:
        """Inject customer context into ElevenLabs Conversational AI prompt."""
        return f"""
System Prompt for Trimly Voice Receptionist:
You are Sara, the friendly AI voice receptionist for Gulshan Barbers in Pakistan.
Always speak warmly in Urdu and Roman Urdu.

Customer Profile:
- Name: {customer_name}
- Last Visit: {days_since_visit} days ago
- Preferred Service: {last_service}
- Favorite Barber Stylist: {favorite_barber}

Goal:
1. Greet the customer: "السلام علیکم {customer_name} صاحب! گُلشن باربرز سے بات ہو رہی ہے۔"
2. Remind them their {last_service} is due.
3. Ask if they'd like to book an appointment with {favorite_barber}.
4. If customer says yes ("ہاں" / "haan" / "yes"), collect preferred time and confirm booking.
5. Keep answers short, natural, and polite.
"""

    async def initiate_outbound_call(
        self,
        to_phone: str,
        customer_name: str,
        favorite_barber: str = "Ali Ustad",
    ) -> Dict[str, Any]:
        """Initiate outbound phone call via Twilio + ElevenLabs."""
        prompt = self.build_customer_context_prompt(
            customer_name=customer_name,
            last_service="Fade Cut",
            favorite_barber=favorite_barber,
            days_since_visit=30,
        )

        return {
            "call_sid": "CA-elevenlabs-mock-sid",
            "status": "INITIATED",
            "to": to_phone,
            "provider": "ELEVENLABS_CONVERSATIONAL_AI",
            "system_prompt": prompt,
            "agent_id": self.agent_id,
        }
