"""Trimly API — Inventory Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def list_inventory(): return success(data=[])
