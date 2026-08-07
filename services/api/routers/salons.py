"""
Trimly API — Salons Router
"""
from fastapi import APIRouter, Depends
from core.responses import success
from core.auth import get_current_user, CurrentUser

router = APIRouter()

@router.get("/me")
async def get_my_salon(current_user: CurrentUser = Depends(get_current_user)):
    return success(
        data={
            "id": current_user.salon_id or "s-5001",
            "name": "Gulshan Barbers",
            "slug": "gulshan-barbers",
            "city": "Lahore",
            "currency": "PKR",
            "plan": current_user.plan,
        }
    )

@router.get("/me/dashboard")
async def get_dashboard_summary(current_user: CurrentUser = Depends(get_current_user)):
    return success(
        data={
            "today_revenue": 18400,
            "customers_served": 34,
            "in_queue": 7,
            "appointments_today": 12,
            "avg_rating": 4.8,
            "best_barber": "Ali Ustad",
        }
    )
