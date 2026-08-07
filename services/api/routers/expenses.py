"""Trimly API — Expenses Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def list_expenses(): return success(data=[])
