"""
Trimly API — Appointments Router
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from core.responses import success
from core.auth import get_current_user, CurrentUser

router = APIRouter()

class AppointmentCreate(BaseModel):
    customer_name: str
    phone: str
    service_id: str
    barber_id: str
    scheduled_at: str

@router.get("")
async def list_appointments(current_user: CurrentUser = Depends(get_current_user)):
    return success(
        data=[
            {
                "id": "app-101",
                "time_slot": "09:00 AM",
                "customer_name": "Ahmed Khan",
                "service_name": "Fade Cut & Beard",
                "barber_name": "Ali Ustad",
                "price": 450,
                "status": "completed",
            },
            {
                "id": "app-102",
                "time_slot": "10:00 AM",
                "customer_name": "Zain Ali",
                "service_name": "Hair Cut",
                "barber_name": "Ali Ustad",
                "price": 300,
                "status": "in-progress",
            },
        ]
    )

@router.post("")
async def create_appointment(
    body: AppointmentCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    return success(
        data={
            "id": "app-new",
            "customer_name": body.customer_name,
            "scheduled_at": body.scheduled_at,
            "status": "confirmed",
        }
    )
