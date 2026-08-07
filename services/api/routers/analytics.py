"""Trimly API — Analytics Router"""
from fastapi import APIRouter
from core.responses import success
router = APIRouter()
@router.get("")
async def get_analytics(): return success(data={})
