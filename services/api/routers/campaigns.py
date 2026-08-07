"""Trimly API — Campaigns Router"""
from fastapi import APIRouter
from core.responses import success

router = APIRouter()

@router.get("")
async def list_campaigns():
    return success(data=[])
