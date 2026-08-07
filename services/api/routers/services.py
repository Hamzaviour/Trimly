"""Trimly API — Services Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def list_services(): return success(data=[])
