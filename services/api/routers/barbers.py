"""Trimly API — Barbers Router"""
from fastapi import APIRouter
from core.responses import success

router = APIRouter()

@router.get("")
async def list_barbers():
    return success(data=[])
