"""Trimly API — Billing & Subscriptions Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("/plan")
async def get_plan(): return success(data={"plan": "PROFESSIONAL", "price_monthly": 5000})
