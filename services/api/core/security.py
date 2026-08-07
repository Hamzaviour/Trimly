"""
Trimly API — Security utilities (JWT, OTP)
"""
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ── OTP ───────────────────────────────────────────────────────────────────────

def generate_otp(length: int = settings.OTP_LENGTH) -> str:
    """Generate a numeric OTP code."""
    return "".join(random.choices(string.digits, k=length))


# ── JWT ───────────────────────────────────────────────────────────────────────

def create_access_token(
    user_id: str,
    salon_id: Optional[str] = None,
    role: str = "CUSTOMER",
    plan: str = "STARTER",
    extra: dict = {},
) -> str:
    """Create a short-lived JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": user_id,
        "salon_id": salon_id,
        "role": role,
        "plan": plan,
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        **extra,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a long-lived JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise ValueError("Invalid or expired token")


# ── Phone normalization ───────────────────────────────────────────────────────

def normalize_phone(phone: str) -> str:
    """Normalize Pakistani phone numbers to E.164 format (+92XXXXXXXXXX)."""
    phone = phone.strip().replace(" ", "").replace("-", "")
    
    if phone.startswith("0"):
        phone = "+92" + phone[1:]
    elif phone.startswith("92"):
        phone = "+" + phone
    elif not phone.startswith("+"):
        phone = "+92" + phone
    
    return phone
