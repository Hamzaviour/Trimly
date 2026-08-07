"""Trimly API — Reviews Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def list_reviews(): return success(data=[])
