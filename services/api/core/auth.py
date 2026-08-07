"""
Trimly API — Auth dependency (FastAPI)
Extracts and validates JWT from Authorization header.
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import decode_token
from core.database import AsyncSession, get_db, set_tenant_context


security = HTTPBearer(auto_error=False)


class CurrentUser:
    """Authenticated user context extracted from JWT."""
    
    def __init__(
        self,
        user_id: str,
        salon_id: Optional[str],
        role: str,
        plan: str,
    ):
        self.user_id = user_id
        self.salon_id = salon_id
        self.role = role
        self.plan = plan

    @property
    def is_owner(self) -> bool:
        return self.role in ("OWNER", "SUPER_ADMIN")

    @property
    def is_admin(self) -> bool:
        return self.role == "SUPER_ADMIN"

    @property
    def is_barber(self) -> bool:
        return self.role == "BARBER"

    @property
    def is_customer(self) -> bool:
        return self.role == "CUSTOMER"


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> CurrentUser:
    """Extract and validate JWT token from Authorization header."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Authentication required"},
        )
    
    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "TOKEN_INVALID", "message": "Invalid or expired token"},
        )
    
    user_id = payload.get("sub")
    salon_id = payload.get("salon_id")
    role = payload.get("role", "CUSTOMER")
    plan = payload.get("plan", "STARTER")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "TOKEN_INVALID", "message": "Token missing user ID"},
        )
    
    # Set tenant context for RLS
    if salon_id:
        await set_tenant_context(db, salon_id, user_id, role)
    
    return CurrentUser(
        user_id=user_id,
        salon_id=salon_id,
        role=role,
        plan=plan,
    )


async def require_owner(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Require OWNER or SUPER_ADMIN role."""
    if not current_user.is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Owner access required"},
        )
    return current_user


async def require_admin(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUser:
    """Require SUPER_ADMIN role."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Admin access required"},
        )
    return current_user


def require_plan(*plans: str):
    """Require a specific subscription plan."""
    async def dependency(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.plan not in plans and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "PLAN_REQUIRED",
                    "message": f"This feature requires one of: {', '.join(plans)}",
                },
            )
        return current_user
    return dependency
