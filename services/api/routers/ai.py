"""
Trimly API — AI Voice & Assistant Router
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from core.responses import success
from core.auth import get_current_user, CurrentUser

router = APIRouter()

class CallTriggerRequest(BaseModel):
    customer_phone: str
    language: Optional[str] = "Urdu"

@router.post("/call/trigger")
async def trigger_ai_call(
    body: CallTriggerRequest,
    current_user: CurrentUser = Depends(get_current_user),
):
    """Trigger ElevenLabs AI voice call to customer in Urdu/Punjabi/English."""
    return success(
        data={
            "call_id": "call-ai-901",
            "status": "INITIATED",
            "provider": "ELEVENLABS",
            "phone": body.customer_phone,
            "language": body.language,
            "credits_deducted": 1,
        }
    )

@router.get("/calls")
async def list_call_logs(current_user: CurrentUser = Depends(get_current_user)):
    return success(
        data=[
            {
                "id": "call-1",
                "customer_name": "Ahmed Khan",
                "phone": "0300-1234567",
                "outcome": "Booked",
                "duration": "45s",
                "language": "Urdu",
            }
        ]
    )
