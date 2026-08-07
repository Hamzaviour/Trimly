"""
Trimly API — Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import sentry_sdk

from core.config import settings
from core.database import engine
from routers import (
    auth,
    salons,
    branches,
    barbers,
    customers,
    appointments,
    queue,
    services,
    inventory,
    expenses,
    reviews,
    loyalty,
    analytics,
    notifications,
    campaigns,
    ai,
    billing,
)


# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.APP_ENV,
        traces_sample_rate=0.1,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    # Startup
    print(f"🚀 Trimly API starting in {settings.APP_ENV} mode")
    yield
    # Shutdown
    await engine.dispose()
    print("✅ Trimly API shutdown complete")


app = FastAPI(
    title="Trimly API",
    description="AI-powered salon management SaaS for Pakistan",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["api.trimly.pk", "api-staging.trimly.pk"],
    )

# ── Routers ───────────────────────────────────────────────────────────────────

API_V1 = "/v1"

app.include_router(auth.router, prefix=f"{API_V1}/auth", tags=["Authentication"])
app.include_router(salons.router, prefix=f"{API_V1}/salons", tags=["Salons"])
app.include_router(branches.router, prefix=f"{API_V1}/branches", tags=["Branches"])
app.include_router(barbers.router, prefix=f"{API_V1}/barbers", tags=["Barbers"])
app.include_router(customers.router, prefix=f"{API_V1}/customers", tags=["Customers"])
app.include_router(appointments.router, prefix=f"{API_V1}/appointments", tags=["Appointments"])
app.include_router(queue.router, prefix=f"{API_V1}/queue", tags=["Queue"])
app.include_router(services.router, prefix=f"{API_V1}/services", tags=["Services"])
app.include_router(inventory.router, prefix=f"{API_V1}/inventory", tags=["Inventory"])
app.include_router(expenses.router, prefix=f"{API_V1}/expenses", tags=["Expenses"])
app.include_router(reviews.router, prefix=f"{API_V1}/reviews", tags=["Reviews"])
app.include_router(loyalty.router, prefix=f"{API_V1}/loyalty", tags=["Loyalty"])
app.include_router(analytics.router, prefix=f"{API_V1}/analytics", tags=["Analytics"])
app.include_router(notifications.router, prefix=f"{API_V1}/notifications", tags=["Notifications"])
app.include_router(campaigns.router, prefix=f"{API_V1}/campaigns", tags=["Campaigns"])
app.include_router(ai.router, prefix=f"{API_V1}/ai", tags=["AI"])
app.include_router(billing.router, prefix=f"{API_V1}/billing", tags=["Billing"])


# ── Health Check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "trimly-api", "version": "1.0.0"}


@app.get("/", tags=["System"])
async def root():
    return {"message": "Trimly API", "docs": "/docs"}
