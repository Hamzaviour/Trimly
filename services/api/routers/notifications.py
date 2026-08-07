"""Trimly API — Notifications Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def list_notifications(): return success(data=[])
