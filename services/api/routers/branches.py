"""
Trimly API — Multi-Branch Management Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from core.responses import success
from core.auth import get_current_user, CurrentUser

router = APIRouter()


class BranchCreate(BaseModel):
    name: str
    address: str
    city: str
    phone: str
    is_main_branch: bool = False


@router.get("")
async def list_branches(current_user: CurrentUser = Depends(get_current_user)):
    """List all salon branches associated with the tenant."""
    branches = [
        {
            "id": "br-1",
            "name": "Main Branch — Gulshan-e-Ravi",
            "address": "Shop #12, Main Boulevard, Gulshan-e-Ravi, Lahore",
            "city": "Lahore",
            "phone": "0300-1234567",
            "barbers_count": 4,
            "is_main_branch": True,
            "active_chairs": 4,
        },
        {
            "id": "br-2",
            "name": "DHA Phase 5 Branch",
            "address": "Plaza 45, Commercial Area, DHA Phase 5, Lahore",
            "city": "Lahore",
            "phone": "0321-9876543",
            "barbers_count": 3,
            "is_main_branch": False,
            "active_chairs": 4,
        },
    ]
    return success(data=branches)


@router.post("")
async def create_branch(
    body: BranchCreate,
    current_user: CurrentUser = Depends(get_current_user),
):
    """Create a new salon branch (Requires Professional or Enterprise Plan)."""
    if current_user.plan not in ["PROFESSIONAL", "ENTERPRISE"] and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "PLAN_REQUIRED", "message": "Multi-branch requires Professional or Enterprise plan"},
        )

    new_branch = {
        "id": f"br-{Date.now()}" if "Date" in globals() else "br-new",
        "name": body.name,
        "address": body.address,
        "city": body.city,
        "phone": body.phone,
        "barbers_count": 0,
        "is_main_branch": body.is_main_branch,
    }
    return success(data=new_branch)
