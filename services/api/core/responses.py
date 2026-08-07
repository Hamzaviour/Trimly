"""
Trimly API — Standard API response schemas
"""
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class Meta(BaseModel):
    """Pagination metadata."""
    page: int = 1
    per_page: int = 20
    total: int = 0
    total_pages: int = 0


class ApiResponse(BaseModel, Generic[T]):
    """Standard success response envelope."""
    success: bool = True
    data: Optional[T] = None
    meta: Optional[Meta] = None


class ApiError(BaseModel):
    """Standard error response envelope."""
    success: bool = False
    error: "ErrorDetail"


class ErrorDetail(BaseModel):
    """Error detail object."""
    code: str
    message: str
    details: Optional[dict] = None


def success(data: Any = None, meta: Optional[Meta] = None) -> dict:
    """Build a standard success response."""
    response = {"success": True, "data": data}
    if meta:
        response["meta"] = meta.model_dump()
    return response


def paginated(
    data: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 20,
) -> dict:
    """Build a paginated success response."""
    total_pages = (total + per_page - 1) // per_page
    return {
        "success": True,
        "data": data,
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


def error(code: str, message: str, details: Optional[dict] = None) -> dict:
    """Build a standard error response."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }


# Common error codes
class ErrorCodes:
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    
    # Auth
    OTP_INVALID = "OTP_INVALID"
    OTP_EXPIRED = "OTP_EXPIRED"
    OTP_LIMIT_EXCEEDED = "OTP_LIMIT_EXCEEDED"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    
    # Appointments
    APPOINTMENT_CONFLICT = "APPOINTMENT_CONFLICT"
    SLOT_UNAVAILABLE = "SLOT_UNAVAILABLE"
    BARBER_UNAVAILABLE = "BARBER_UNAVAILABLE"
    
    # Payments
    PAYMENT_FAILED = "PAYMENT_FAILED"
    INSUFFICIENT_CREDITS = "INSUFFICIENT_CREDITS"
    
    # Queue
    QUEUE_FULL = "QUEUE_FULL"
    NOT_IN_QUEUE = "NOT_IN_QUEUE"
