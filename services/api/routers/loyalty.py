"""Trimly API — Loyalty Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def get_loyalty_config(): return success(data={})
