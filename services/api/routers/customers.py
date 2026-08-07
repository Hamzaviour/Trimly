"""
Trimly API — Customers Router
"""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional
from core.responses import success, paginated
from core.auth import get_current_user, CurrentUser

router = APIRouter()

class CustomerCreate(BaseModel):
    name: str
    phone: str
    notes: Optional[str] = None
    favorite_barber_id: Optional[str] = None

@router.get("")
async def list_customers(
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
):
    mock_list = [
        {
            "id": "c-1",
            "name": "Ahmed Khan",
            "phone": "0300-1234567",
            "total_visits": 17,
            "total_spent": 45200,
            "loyalty_points": 170,
            "last_visit_at": "2026-08-04",
            "favorite_barber": "Ali Ustad",
            "churn_risk": 0.1,
        },
        {
            "id": "c-2",
            "name": "Bilal Ahmed",
            "phone": "0312-9876543",
            "total_visits": 4,
            "total_spent": 8500,
            "loyalty_points": 40,
            "last_visit_at": "2026-07-18",
            "favorite_barber": "Hassan",
            "churn_risk": 0.4,
        },
    ]
    return paginated(data=mock_list, total=2, page=page, per_page=per_page)

@router.post("")
async def create_customer(
    body: CustomerCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    return success(
        data={
            "id": "c-new",
            "name": body.name,
            "phone": body.phone,
            "total_visits": 0,
            "loyalty_points": 10,
        }
    )
