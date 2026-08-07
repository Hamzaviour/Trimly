# Trimly — Technical Requirements Document (TRD)

**Version:** 1.0  
**Date:** August 2026  
**Author:** Trimly Engineering Team  
**Status:** Draft

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Tech Stack Decisions](#tech-stack-decisions)
3. [Service Architecture](#service-architecture)
4. [API Design Standards](#api-design-standards)
5. [Authentication & Authorization](#authentication--authorization)
6. [Multi-Tenancy Architecture](#multi-tenancy-architecture)
7. [Real-time Features](#real-time-features)
8. [AI Integration Architecture](#ai-integration-architecture)
9. [Notification System](#notification-system)
10. [Payment Integration](#payment-integration)
11. [Storage & CDN](#storage--cdn)
12. [Security Requirements](#security-requirements)
13. [Performance Targets](#performance-targets)
14. [Infrastructure & Deployment](#infrastructure--deployment)
15. [Monitoring & Observability](#monitoring--observability)
16. [Environment Configuration](#environment-configuration)

---

## System Architecture Overview

```
                              INTERNET
                                 │
                    ┌────────────▼────────────┐
                    │      Cloudflare CDN      │
                    │   (DDoS + Edge Cache)    │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐  ┌────▼──────┐  ┌────────▼────────┐
    │   Owner Dashboard  │  │ Customer  │  │   Admin Panel   │
    │   (Next.js 15)     │  │   Web     │  │   (Next.js 15)  │
    │   Vercel           │  │ (Next.js) │  │   Vercel        │
    └─────────┬─────────┘  └────┬──────┘  └────────┬────────┘
              │                 │                   │
              └─────────────────┼───────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │     API Gateway        │
                    │  (FastAPI + Nginx)     │
                    │  Railway/DigitalOcean  │
                    └───────────┬───────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
 ┌────────▼────────┐  ┌─────────▼────────┐  ┌────────▼────────┐
 │  Core Services  │  │  AI Services     │  │  Background Jobs │
 │  booking-svc    │  │  voice-svc       │  │  Celery Workers  │
 │  crm-svc        │  │  analytics-svc   │  │  Redis Queue     │
 │  auth-svc       │  │  marketing-svc   │  │                  │
 └────────┬────────┘  └─────────┬────────┘  └────────┬────────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
              ┌─────────────────┼─────────────┐
              │                 │             │
   ┌──────────▼──────┐  ┌──────▼──────┐  ┌──▼──────────────┐
   │   PostgreSQL     │  │    Redis     │  │  Cloudflare R2  │
   │  (Supabase/Neon) │  │  (Cache +   │  │  (Media/Files)  │
   │                  │  │   Queues)   │  │                  │
   └──────────────────┘  └─────────────┘  └─────────────────┘
```

---

## Tech Stack Decisions

### Frontend

| Technology | Version | Rationale |
|---|---|---|
| Next.js | 15.x | SSR for SEO, App Router, Server Components for performance |
| React | 19.x | Component model, ecosystem |
| TailwindCSS | 3.x | Utility-first, fast development, consistent design |
| shadcn/ui | Latest | Accessible, customizable component library |
| Framer Motion | 11.x | Premium animations without performance cost |
| React Query (TanStack) | 5.x | Server state management, caching, background sync |
| Zustand | 4.x | Client state management (lightweight) |
| Socket.io Client | Latest | Real-time queue updates |
| i18next | Latest | Urdu/English localization |

### Mobile

| Technology | Version | Rationale |
|---|---|---|
| React Native | 0.75+ | Code sharing with web React patterns |
| Expo | SDK 51+ | Fast development, OTA updates, EAS Build |
| Expo Router | 3.x | File-based routing consistent with Next.js |
| React Native Paper | Latest | Material Design components |

### Backend

| Technology | Version | Rationale |
|---|---|---|
| FastAPI | 0.115+ | High performance, async, auto-generated OpenAPI docs |
| Python | 3.12+ | AI/ML ecosystem, async support |
| SQLAlchemy | 2.x | Async ORM with powerful query capabilities |
| Alembic | Latest | Database migrations |
| Celery | 5.x | Distributed task queue for background jobs |
| Pydantic | 2.x | Data validation, serialization, OpenAPI schema |
| uvicorn | Latest | ASGI server |

### Database

| Technology | Use Case | Rationale |
|---|---|---|
| PostgreSQL 16 | Primary database | ACID compliance, JSON support, Row Level Security |
| Redis 7 | Cache + Queue + Session | Sub-millisecond reads, pub/sub for real-time |
| Supabase / Neon | Managed PostgreSQL | Managed service, connection pooling, branching |

### External Services

| Service | Purpose |
|---|---|
| Clerk | Authentication (JWT, OTP, social login) |
| Firebase Cloud Messaging | Push notifications (mobile + web) |
| ElevenLabs Conversational AI | Urdu/Punjabi AI voice calls |
| OpenAI Realtime API | Fallback AI voice (English) |
| Twilio | International SMS |
| Jazz/Zong APIs | Pakistani SMS |
| Easypaisa API | Pakistani digital payments |
| JazzCash API | Pakistani digital payments |
| Stripe | International payments |
| Google Calendar API | Calendar sync |
| Cloudflare R2 | Object storage (images, recordings) |
| Upstash | Serverless Redis |

---

## Service Architecture

### Monorepo Structure

```
trimly/
├── apps/
│   ├── owner-dashboard/          # Next.js 15 — salon owner web app
│   ├── customer-web/             # Next.js 15 — customer booking web
│   ├── admin-panel/              # Next.js 15 — Trimly admin
│   ├── marketing-site/           # Next.js 15 — landing page
│   └── mobile/                   # Expo React Native
├── services/
│   ├── api/                      # Main FastAPI app (monolith first)
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── salons.py
│   │   │   ├── branches.py
│   │   │   ├── barbers.py
│   │   │   ├── customers.py
│   │   │   ├── appointments.py
│   │   │   ├── queue.py
│   │   │   ├── services.py
│   │   │   ├── inventory.py
│   │   │   ├── expenses.py
│   │   │   ├── loyalty.py
│   │   │   ├── reviews.py
│   │   │   ├── analytics.py
│   │   │   ├── notifications.py
│   │   │   ├── campaigns.py
│   │   │   ├── ai.py
│   │   │   └── billing.py
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   ├── workers/              # Celery tasks
│   │   ├── ai/                   # AI agent modules
│   │   └── core/                 # Config, DB, security
│   └── voice-agent/              # Standalone AI voice service
├── packages/
│   ├── ui/                       # Shared React components
│   ├── types/                    # Shared TypeScript types
│   ├── config/                   # Shared configs (ESLint, TS, etc.)
│   └── utils/                    # Shared utility functions
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── scripts/
└── docs/
```

---

## API Design Standards

### Base URL
```
Production: https://api.trimly.pk/v1
Staging:    https://api-staging.trimly.pk/v1
Local:      http://localhost:8000/v1
```

### Request/Response Format
```json
// Success Response
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "APPOINTMENT_CONFLICT",
    "message": "This time slot is already booked",
    "details": { "conflicting_appointment_id": "uuid" }
  }
}
```

### Versioning
- URL-based versioning: `/v1/`, `/v2/`
- Maintain backwards compatibility for at least 2 major versions

### Key Endpoints

```
AUTH
POST   /v1/auth/otp/send
POST   /v1/auth/otp/verify
POST   /v1/auth/refresh
DELETE /v1/auth/logout

SALONS
GET    /v1/salons/me
PUT    /v1/salons/me
GET    /v1/salons/me/dashboard
GET    /v1/salons/me/analytics

CUSTOMERS
GET    /v1/customers
POST   /v1/customers
GET    /v1/customers/{id}
PUT    /v1/customers/{id}
GET    /v1/customers/{id}/history
GET    /v1/customers/{id}/loyalty

APPOINTMENTS
GET    /v1/appointments
POST   /v1/appointments
GET    /v1/appointments/{id}
PUT    /v1/appointments/{id}
PATCH  /v1/appointments/{id}/status
DELETE /v1/appointments/{id}

QUEUE
GET    /v1/queue                  # Live queue state
POST   /v1/queue/join             # Customer joins queue
PATCH  /v1/queue/{id}/complete    # Mark service complete
GET    /v1/queue/public/{salon_slug}  # Public queue view

BARBERS
GET    /v1/barbers
POST   /v1/barbers
GET    /v1/barbers/{id}
GET    /v1/barbers/{id}/schedule
GET    /v1/barbers/{id}/analytics

AI
POST   /v1/ai/reminder/trigger    # Manual trigger reminder
GET    /v1/ai/calls               # Call logs
POST   /v1/ai/campaigns           # Create AI campaign
GET    /v1/ai/insights            # AI-generated insights
```

---

## Authentication & Authorization

### Auth Flow (Owner/Staff)
```
1. Owner enters phone number
2. OTP sent via SMS (Jazz/Zong)
3. OTP verified → JWT issued (access 15min + refresh 30 days)
4. JWT includes: user_id, salon_id, role, plan
5. API validates JWT on every request
6. Role checked via RBAC middleware
```

### Auth Flow (Customer)
```
1. Customer enters phone number
2. OTP sent via SMS
3. OTP verified → Customer session created
4. Optional: link to salon for loyalty tracking
```

### Role-Based Access Control (RBAC)

| Role | Permissions |
|---|---|
| `SUPER_ADMIN` | All — Trimly admin panel access |
| `OWNER` | Full access to their salon(s) |
| `MANAGER` | All owner permissions except billing and deletion |
| `RECEPTIONIST` | Customers, appointments, queue — no financials |
| `BARBER` | Own schedule, current queue, own analytics only |
| `CUSTOMER` | Own profile, booking, queue view, history |

### JWT Payload
```json
{
  "sub": "user_uuid",
  "salon_id": "salon_uuid",
  "branch_ids": ["branch_uuid_1"],
  "role": "OWNER",
  "plan": "PROFESSIONAL",
  "iat": 1234567890,
  "exp": 1234568790
}
```

---

## Multi-Tenancy Architecture

### Strategy: Schema-per-tenant approach with Row Level Security

```sql
-- Every table has salon_id foreign key
-- PostgreSQL Row Level Security enforced at DB level

ALTER TABLE customers ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON customers
  USING (salon_id = current_setting('app.current_salon_id')::uuid);
```

### Tenant Context Injection
```python
# FastAPI middleware sets tenant context
async def set_tenant_context(request: Request, call_next):
    salon_id = extract_salon_id_from_jwt(request)
    await db.execute(
        f"SET app.current_salon_id = '{salon_id}'"
    )
    response = await call_next(request)
    return response
```

### Data Isolation Rules
1. All primary business tables include `salon_id` (UUID)
2. All queries automatically filtered by `salon_id` via RLS
3. Cross-salon queries only allowed for `SUPER_ADMIN` role
4. Backup and export scoped per salon

---

## Real-time Features

### Technology: WebSockets via Socket.io

#### Queue Updates
```
Client connects to: wss://api.trimly.pk/ws/queue/{salon_id}
Server emits:
  - queue:updated     → Full queue state
  - chair:status      → Single chair update
  - appointment:added → New appointment in queue
  - wait:estimated    → Updated wait time estimate
```

#### Barber Dashboard
```
Client connects to: wss://api.trimly.pk/ws/barber/{barber_id}
Server emits:
  - next:customer     → Upcoming customer details
  - appointment:new   → New booking assigned
```

### Wait Time Calculation Algorithm
```python
def estimate_wait_time(chair_id: str, position: int) -> int:
    """
    Returns estimated wait time in minutes.
    Uses:
    - Current service duration remaining
    - Average service time per barber (rolling 7-day)
    - Number of customers ahead in queue
    """
    remaining = get_current_service_remaining(chair_id)
    avg_service_time = get_barber_avg_time(chair_id)
    ahead = get_customers_ahead(chair_id, position)
    return remaining + (ahead * avg_service_time)
```

---

## AI Integration Architecture

### AI Reminder Agent (Celery + Cron)

```
Every hour:
  1. Query: customers where last_visit > (now - reminder_threshold)
  2. Filter: not already reminded in last 7 days
  3. For each customer:
     a. Generate personalized message (GPT-4o-mini)
     b. Choose channel: Push > WhatsApp > SMS > AI Call
     c. Schedule notification
     d. Log in ai_tasks table
```

### AI Voice Receptionist (ElevenLabs)

```
Architecture:
  Incoming call → Twilio webhook → voice-agent service
  voice-agent:
    1. Lookup customer by phone
    2. Load context (last visit, preferred barber, services)
    3. Initialize ElevenLabs Conversational AI session
    4. Inject customer context as system prompt
    5. Handle conversation turn-by-turn
    6. If booking intent detected → call booking API
    7. Log full transcript to call_logs table
```

### Message Generation Prompt Template
```
System: You are Trimly AI, a friendly salon assistant in Pakistan.
Always respond in {customer_language}.
Customer name: {name}
Last visit: {last_visit_days} days ago
Last service: {last_service}
Favorite barber: {favorite_barber}
Salon: {salon_name}

Goal: Remind the customer it's time for their next {service}.
Be warm, brief, and offer to book an appointment.
If customer says yes (ہاں / haan / yes), collect preferred time and book.
```

### Churn Detection Agent
```python
# Risk score calculation
def calculate_churn_risk(customer: Customer) -> float:
    days_since_visit = (now - customer.last_visit).days
    avg_frequency = customer.avg_visit_frequency_days
    overdue_ratio = days_since_visit / avg_frequency
    
    if overdue_ratio < 1.2:  return 0.1   # On track
    if overdue_ratio < 1.5:  return 0.4   # Slightly late
    if overdue_ratio < 2.0:  return 0.7   # At risk
    return 0.9                             # High churn risk
```

---

## Notification System

### Notification Priority Chain
```
1. Push Notification (free, instant) — if app installed
2. WhatsApp Message (low cost) — if WhatsApp available
3. SMS (fallback) — always deliverable
4. AI Voice Call (highest cost) — for high-value churn risk
```

### Notification Types
| Type | Trigger | Channel |
|---|---|---|
| Appointment Confirmed | Booking created | Push + SMS |
| Appointment Reminder | 24h + 2h before | Push + WhatsApp |
| Queue Update | Position changes | Push |
| Visit Complete | Service marked done | Push |
| Review Request | 2h after visit | Push + WhatsApp |
| AI Reminder | Days since last visit | Push > WA > SMS > Call |
| Birthday Offer | Customer birthday | SMS + WhatsApp |
| Loyalty Milestone | Points threshold hit | Push |
| Low Inventory | Stock < threshold | Push (owner) |

### SMS Templates (Jazz/Zong compliant)
```
Appointment Confirmation:
"Trimly: Apki appointment confirm ho gayi. {barber_name} k saath {time} baje. 
Queue: trimly.pk/q/{salon_slug}"

Reminder:
"Trimly: {name} sb, {days} din ho gaye hain. 
{salon_name} mein appointment lijiye: trimly.pk/book/{salon_slug}"
```

---

## Payment Integration

### Payment Flow

```
Customer selects payment → Select method (Easypaisa/JazzCash/Cash)
→ Generate order_id
→ Redirect to payment gateway
→ Webhook received on completion
→ Update invoice status
→ Notify customer and owner
→ Sync to analytics
```

### Easypaisa Integration
```python
# Easypaisa Merchant API
POST /api/payment/initiate
{
  "storeId": EASYPAISA_STORE_ID,
  "amount": "500",
  "orderRefNum": "TRIMLY-{invoice_id}",
  "mobileNum": customer.phone,
  "emailAddress": customer.email,
  "returnUrl": "https://trimly.pk/payment/callback"
}
```

### Payment States
```
PENDING → PROCESSING → COMPLETED
                    → FAILED
                    → REFUNDED
                    → CANCELLED
```

---

## Storage & CDN

### Cloudflare R2 Bucket Structure
```
trimly-media/
├── salons/
│   └── {salon_id}/
│       ├── logo.webp
│       ├── cover.webp
│       └── gallery/
├── barbers/
│   └── {barber_id}/
│       └── avatar.webp
├── customers/
│   └── {customer_id}/
│       └── selfie.webp          # For future AI hair preview
├── invoices/
│   └── {invoice_id}/
│       └── invoice.pdf
└── voice/
    └── {call_log_id}/
        └── recording.mp3
```

### Upload Policy
- Max image size: 5MB
- Accepted formats: JPEG, PNG, WebP
- Auto-compress to WebP on upload
- Signed upload URLs (never expose R2 credentials to client)
- CDN URL prefix: `https://media.trimly.pk/{path}`

---

## Security Requirements

### Transport Security
- TLS 1.3 minimum for all connections
- HSTS headers on all responses
- Certificate pinning on mobile app

### Data Security
- All PII encrypted at rest (PostgreSQL encryption)
- Passwords never stored (OTP-only authentication)
- JWT signed with RS256
- Refresh tokens stored in httpOnly cookies only

### API Security
- Rate limiting: 100 req/min per IP (unauthenticated), 1000/min (authenticated)
- CORS: Whitelist-only origins
- SQL injection prevention: ORM only, no raw queries
- Input validation: Pydantic on all inputs
- File upload: Mime-type validation + virus scan

### Pakistani Data Compliance
- Customer data stored in data center with Pakistan region preference
- Right to deletion: Customer can request data purge
- Audit log: All data access logged in audit_logs table
- Consent: Explicit SMS/call consent captured at registration

### OWASP Top 10 Mitigations
| Vulnerability | Mitigation |
|---|---|
| Injection | Parameterized queries via SQLAlchemy |
| Broken Auth | JWT + OTP, no passwords, short expiry |
| Sensitive Data Exposure | Encryption at rest, TLS in transit |
| XXE | No XML parsing |
| Broken Access Control | RBAC + RLS at DB level |
| Security Misconfiguration | Automated security scanning in CI |
| XSS | CSP headers, React's auto-escaping |
| Insecure Deserialization | Pydantic validation |
| Vulnerable Components | Dependabot automated updates |
| Insufficient Logging | Structured logging + audit trail |

---

## Performance Targets

| Metric | Target | Measurement |
|---|---|---|
| API P50 latency | < 100ms | Prometheus |
| API P95 latency | < 500ms | Prometheus |
| API P99 latency | < 1000ms | Prometheus |
| Dashboard load (3G) | < 2.5s | Lighthouse |
| Queue page load | < 1.5s | Lighthouse |
| Concurrent connections | 10,000 | Load test |
| DB query time P95 | < 50ms | pg_stat_statements |
| WebSocket message delay | < 200ms | Custom metric |

### Optimization Strategies
- Redis cache for frequently accessed data (salon config, service list)
- Database connection pooling (PgBouncer)
- CDN for all static assets (Cloudflare)
- Image optimization (WebP, lazy loading)
- API response pagination (max 100 items/page)
- Background processing for non-critical tasks (Celery)
- Read replicas for analytics queries

---

## Infrastructure & Deployment

### Environments

| Environment | Frontend | Backend | DB |
|---|---|---|---|
| Development | localhost:3000 | localhost:8000 | Local PostgreSQL |
| Staging | staging.trimly.pk | api-staging.trimly.pk | Neon (staging) |
| Production | trimly.pk | api.trimly.pk | Neon (prod) |

### Deployment Pipeline

```
Push to feature branch
  → GitHub Actions: lint + type check + unit tests
  → PR created
  → Staging deploy (auto)
  → Integration tests
  → PR review
  → Merge to main
  → Production deploy (auto for frontend, manual approval for backend)
  → Smoke tests
  → Rollback if smoke tests fail
```

### Container Setup
```dockerfile
# Backend Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Scaling Strategy
- **Horizontal:** Multiple API instances behind load balancer
- **Vertical:** Start small (Railway $25/mo) → scale as needed
- **DB:** Connection pooling via PgBouncer; read replicas for analytics
- **Cache:** Redis cluster for high availability

---

## Monitoring & Observability

### Logging
- **Format:** JSON structured logs
- **Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Tool:** Loguru (Python) + Winston (Next.js)
- **Destination:** Railway logs → Logtail / Betterstack

### Metrics
- **Tool:** Prometheus + Grafana
- **Key metrics:** Request rate, error rate, latency, queue depth, active salons

### Alerting
- PagerDuty for critical alerts (P0/P1)
- Slack for non-critical alerts (P2/P3)

### Error Tracking
- **Tool:** Sentry (frontend + backend)
- **Sampling:** 100% for errors, 10% for transactions

### Uptime Monitoring
- **Tool:** Better Uptime / UptimeRobot
- **Frequency:** Every 30 seconds
- **Alerts:** Email + SMS to on-call team

---

## Environment Configuration

### Required Environment Variables

```env
# Application
APP_NAME=trimly
APP_ENV=production
SECRET_KEY=<32-byte-random>
ALLOWED_ORIGINS=https://trimly.pk,https://owner.trimly.pk

# Database
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...

# Authentication
CLERK_SECRET_KEY=
CLERK_PUBLISHABLE_KEY=

# AI Services
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_AGENT_ID=

# SMS
JAZZ_API_KEY=
JAZZ_SENDER_ID=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=

# Payments
EASYPAISA_STORE_ID=
EASYPAISA_HASH_KEY=
JAZZCASH_MERCHANT_ID=
JAZZCASH_PASSWORD=
STRIPE_SECRET_KEY=

# Storage
CLOUDFLARE_R2_ACCOUNT_ID=
CLOUDFLARE_R2_ACCESS_KEY=
CLOUDFLARE_R2_SECRET_KEY=
CLOUDFLARE_R2_BUCKET=trimly-media
CDN_URL=https://media.trimly.pk

# Firebase
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=

# Monitoring
SENTRY_DSN=
```

---

*Document maintained by Trimly Engineering Team. All architectural decisions must be reviewed before changing.*
