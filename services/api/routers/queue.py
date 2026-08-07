"""
Trimly API — Live Queue Router
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.responses import success
from core.auth import get_current_user, CurrentUser

router = APIRouter()

class QueueJoinRequest(BaseModel):
    customer_name: str
    phone: str
    service_name: str

@router.get("")
async def get_live_queue(current_user: CurrentUser = Depends(get_current_user)):
    return success(
        data={
            "chairs": [
                {"id": 1, "name": "Chair 1", "barber": "Ali Ustad", "status": "busy", "customer": "Ahmed Khan", "minutes_left": 12},
                {"id": 2, "name": "Chair 2", "barber": "Hassan", "status": "free", "customer": None, "minutes_left": 0},
            ],
            "waiting": [
                {"position": 1, "customer_name": "Zain Ali", "service": "Hair Cut", "est_wait": 5},
            ],
        }
    )

@router.post("/join")
async def join_queue(body: QueueJoinRequest):
    return success(
        data={"position": 2, "token": "Q-104", "est_wait_minutes": 15}
    )
