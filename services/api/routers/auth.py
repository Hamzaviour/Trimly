"""
Trimly API — Authentication Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from core.responses import success, error, ErrorCodes
from core.security import generate_otp, create_access_token, create_refresh_token, normalize_phone

router = APIRouter()


class SendOtpRequest(BaseModel):
    phone: str


class VerifyOtpRequest(BaseModel):
    phone: str
    otp: str


@router.post("/otp/send")
async def send_otp(req: SendOtpRequest):
    """Send 6-digit OTP to Pakistani phone number via SMS."""
    phone = normalize_phone(req.phone)
    # In production: call Jazz/Zong/Twilio SMS service
    # For dev mode: static test OTP '123456'
    return success(
        data={"phone": phone, "message": "OTP sent successfully", "expires_in_seconds": 300}
    )


@router.post("/otp/verify")
async def verify_otp(req: VerifyOtpRequest):
    """Verify OTP and issue JWT access & refresh tokens."""
    phone = normalize_phone(req.phone)
    
    # Dev verification rule
    if req.otp != "123456" and req.otp != "654321":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error(ErrorCodes.OTP_INVALID, "Invalid OTP code entered"),
        )
    
    # Mock user token generation
    mock_user_id = "u-1001"
    mock_salon_id = "s-5001"
    
    access_token = create_access_token(
        user_id=mock_user_id,
        salon_id=mock_salon_id,
        role="OWNER",
        plan="PROFESSIONAL",
    )
    refresh_token = create_refresh_token(user_id=mock_user_id)
    
    return success(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": mock_user_id,
                "phone": phone,
                "role": "OWNER",
                "salon_id": mock_salon_id,
            },
        }
    )
