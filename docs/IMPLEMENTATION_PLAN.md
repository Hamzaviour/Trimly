# Trimly — Implementation Plan

**Version:** 1.0  
**Date:** August 2026  
**Total Estimated Duration:** 15 weeks (Phases 1–3)

---

## Overview

This plan follows a phased approach — ship the most valuable features first, validate with real salons, then expand. Each phase produces a shippable product.

---

## Phase 0: Foundation (Week 0 — Before coding)

### Goals
- [ ] Environment setup complete
- [ ] Repository initialized with monorepo structure
- [ ] CI/CD pipelines connected
- [ ] Database provisioned and accessible
- [ ] All team members onboarded

### Tasks

#### Monorepo Setup
- [ ] Initialize Turborepo monorepo in `trimly/`
- [ ] Configure shared `tsconfig`, `eslint`, `prettier`
- [ ] Set up `packages/ui`, `packages/types`, `packages/utils`
- [ ] Configure path aliases

#### Infrastructure
- [ ] Create Neon PostgreSQL instance (staging + prod)
- [ ] Create Upstash Redis instance
- [ ] Set up Cloudflare R2 bucket + CDN
- [ ] Deploy Railway project for backend
- [ ] Connect Vercel for frontend deployments
- [ ] Set up Sentry (frontend + backend)

#### Backend Bootstrap
- [ ] Initialize FastAPI app structure
- [ ] Set up SQLAlchemy async engine + session management
- [ ] Configure Alembic for migrations
- [ ] Set up Celery + Redis broker
- [ ] Configure Clerk webhook receiver
- [ ] Write base models (User, Salon, Branch)
- [ ] Run initial migration

#### Frontend Bootstrap
- [ ] Initialize Next.js 15 owner dashboard app
- [ ] Configure Tailwind CSS + shadcn/ui
- [ ] Set up Framer Motion
- [ ] Configure TanStack Query
- [ ] Configure Zustand stores
- [ ] Set up i18next (en + ur)
- [ ] Build design system: tokens, typography, colors
- [ ] Build core layout: Sidebar + Header shell

#### CI/CD
- [ ] GitHub Actions: lint + typecheck + test on PR
- [ ] Vercel: auto-deploy frontend on merge to main
- [ ] Railway: auto-deploy backend on merge to main (with approval gate for prod)

---

## Phase 1: Core Operations (Weeks 1–6)

**Goal:** A salon can sign up, manage its queue, add customers, and track appointments. This is the MVP.

### Week 1–2: Authentication + Onboarding

#### Backend
- [ ] `POST /v1/auth/otp/send` — send OTP via Jazz/Twilio
- [ ] `POST /v1/auth/otp/verify` — verify OTP, issue JWT
- [ ] `POST /v1/auth/refresh` — refresh access token
- [ ] `DELETE /v1/auth/logout`
- [ ] `POST /v1/onboarding/salon` — create salon during onboarding
- [ ] `POST /v1/onboarding/services` — seed default services
- [ ] `POST /v1/onboarding/barbers` — add initial barbers
- [ ] Clerk webhook integration (user sync)
- [ ] RLS middleware (set `app.current_salon_id` from JWT)

#### Frontend
- [ ] Login screen (phone + OTP)
- [ ] OTP verification screen
- [ ] Onboarding wizard (5 steps)
  - [ ] Step 1: Personal info
  - [ ] Step 2: Salon details
  - [ ] Step 3: Add barbers
  - [ ] Step 4: Services setup
  - [ ] Step 5: Plan selection
- [ ] Protected route wrapper
- [ ] Auth store (Zustand)

### Week 2–3: Salon Dashboard + Queue

#### Backend
- [ ] `GET /v1/salons/me/dashboard` — today's stats
- [ ] `GET /v1/queue` — live queue state
- [ ] `POST /v1/queue/join` — add to queue
- [ ] `PATCH /v1/queue/{id}/status` — update entry status
- [ ] `GET /v1/queue/public/{salon_slug}` — public queue (no auth)
- [ ] `GET /v1/chairs` — list chairs
- [ ] `PATCH /v1/chairs/{id}` — update chair status
- [ ] WebSocket endpoint: `/ws/queue/{salon_id}` — real-time updates
- [ ] Wait time estimation algorithm
- [ ] Chairs seeding during onboarding

#### Frontend (Owner Dashboard)
- [ ] Dashboard home page
  - [ ] Stats cards (revenue, customers, queue, appointments)
  - [ ] Live queue preview widget
  - [ ] Revenue chart (7-day)
  - [ ] Top barbers mini leaderboard
- [ ] Live Queue page
  - [ ] Chair grid cards (status: FREE/BUSY/ON_BREAK)
  - [ ] Countdown timer on busy chairs
  - [ ] Waiting list section
  - [ ] Add walk-in button
  - [ ] Assign to chair flow
  - [ ] Complete service action
- [ ] Queue display page (public TV board)
  - [ ] Auto-refresh via WebSocket
  - [ ] Dark theme, large text
  - [ ] Chair status grid

### Week 3–4: Customer CRM

#### Backend
- [ ] `GET /v1/customers` — list with search, filter, pagination
- [ ] `POST /v1/customers` — add new customer
- [ ] `GET /v1/customers/{id}` — full profile
- [ ] `PUT /v1/customers/{id}` — update customer
- [ ] `DELETE /v1/customers/{id}` — soft delete
- [ ] `GET /v1/customers/{id}/history` — visit history
- [ ] `GET /v1/customers/{id}/loyalty` — points + tier
- [ ] Customer churn risk score calculation (background job)
- [ ] Auto-tag (VIP, At Risk, Lost, New) based on rules
- [ ] Customer stats update trigger (on invoice completion)

#### Frontend
- [ ] Customers list page
  - [ ] Search + filter bar
  - [ ] Sortable table (visits, last visit, spent, status)
  - [ ] Status badge column (VIP/Active/At Risk/Lost/New)
  - [ ] Row click → slide-in detail panel
  - [ ] Bulk actions (tag, message)
  - [ ] Empty state with add CTA
- [ ] Customer detail panel/drawer
  - [ ] Profile header (name, phone, points, tier)
  - [ ] Stats row (visits, spent, rating)
  - [ ] Visit history timeline
  - [ ] Preferences + notes
  - [ ] Quick actions (Book, Message, Call)
- [ ] Add customer drawer (inline)
- [ ] Edit customer form

### Week 4–5: Appointments + Booking

#### Backend
- [ ] `GET /v1/appointments` — list (with date/barber/status filters)
- [ ] `POST /v1/appointments` — create booking
- [ ] `GET /v1/appointments/{id}` — detail
- [ ] `PUT /v1/appointments/{id}` — update
- [ ] `PATCH /v1/appointments/{id}/status` — status transition
- [ ] `DELETE /v1/appointments/{id}` — cancel
- [ ] `GET /v1/barbers/{id}/availability` — available slots
- [ ] `GET /v1/services` — salon services list
- [ ] `POST /v1/services` — add service
- [ ] Invoice auto-generation on appointment completion
- [ ] Loyalty points auto-award on invoice completion

#### Frontend
- [ ] Appointments calendar page
  - [ ] Month/Week/Day view toggle
  - [ ] Appointment cards per barber lane
  - [ ] Click to create new appointment
  - [ ] Drag to reschedule (optional for MVP)
  - [ ] Appointment status colors
- [ ] Booking wizard (slide-in sheet)
  - [ ] Step 1: Customer search/select
  - [ ] Step 2: Service(s) + Barber + Time
  - [ ] Step 3: Confirm + payment type
  - [ ] Success animation
- [ ] Services management page
  - [ ] Service cards grid
  - [ ] Add/edit service form
  - [ ] Toggle active/inactive
  - [ ] Category grouping

### Week 5–6: Barbers + Reviews + Basic Analytics

#### Backend
- [ ] `GET /v1/barbers` — list with stats
- [ ] `POST /v1/barbers` — add barber
- [ ] `PUT /v1/barbers/{id}` — update
- [ ] `GET /v1/barbers/{id}/analytics` — performance stats
- [ ] `GET /v1/reviews` — list reviews
- [ ] `POST /v1/reviews` — submit review (customer)
- [ ] `PATCH /v1/reviews/{id}/reply` — owner reply
- [ ] `GET /v1/analytics/revenue` — revenue stats
- [ ] `GET /v1/analytics/barbers` — barber performance
- [ ] `GET /v1/analytics/services` — popular services

#### Frontend
- [ ] Barbers page
  - [ ] Barber cards with leaderboard ranking
  - [ ] Stats: cuts, revenue, rating, reviews
  - [ ] Status indicator
- [ ] Add/edit barber form
- [ ] Reviews page
  - [ ] Review cards with star ratings
  - [ ] Owner reply inline
  - [ ] Filter by barber
  - [ ] Average rating summary
- [ ] Basic Analytics page
  - [ ] Revenue graph (daily/weekly/monthly toggle)
  - [ ] Top services donut chart
  - [ ] Barber performance bar chart
  - [ ] Key metrics summary

#### Barber Dashboard (Separate App or Route)
- [ ] Barber login (OTP)
- [ ] Today's summary (cuts, revenue, rating)
- [ ] Current customer card
- [ ] Upcoming queue list
- [ ] [Complete Service] button

---

## Phase 2: Engagement & Retention (Weeks 7–10)

**Goal:** Keep customers coming back. Add SMS reminders, loyalty, push notifications, full analytics.

### Week 7: SMS Reminders + Push Notifications

#### Backend
- [ ] Jazz/Zong SMS API integration
- [ ] Twilio SMS integration (international fallback)
- [ ] SMS template engine with variable substitution
- [ ] Celery beat scheduler for reminder jobs
- [ ] Reminder Celery task (daily cron):
  - [ ] Query customers past reminder threshold
  - [ ] Generate personalized message
  - [ ] Send SMS + log in sms_logs
- [ ] `GET /v1/sms-logs` — delivery status list
- [ ] Firebase Admin SDK setup
- [ ] Push notification service (via Firebase)
- [ ] Appointment reminder scheduler (24h + 2h before)

#### Frontend
- [ ] Settings → Reminders page
  - [ ] Per-service reminder thresholds (sliders)
  - [ ] Enable/disable SMS reminders
  - [ ] Enable/disable WhatsApp
- [ ] SMS Logs page (delivery status)
- [ ] Notification settings

### Week 8: Loyalty Program

#### Backend
- [ ] Loyalty points award on invoice completion (trigger)
- [ ] `GET /v1/loyalty/tiers` — tier configuration
- [ ] `PUT /v1/loyalty/config` — update points config
- [ ] `GET /v1/customers/{id}/loyalty` — points + history
- [ ] `POST /v1/loyalty/redeem` — redeem points for service
- [ ] `GET /v1/loyalty/leaderboard` — top customers by points
- [ ] Loyalty tier upgrade notifications

#### Frontend
- [ ] Settings → Loyalty page
  - [ ] Points per visit slider
  - [ ] Tier rewards configuration
  - [ ] Enable/disable loyalty
- [ ] Customer profile: loyalty section (points, tier, history)
- [ ] Loyalty leaderboard widget on dashboard

### Week 9: Revenue Analytics + Inventory + Expenses

#### Backend
- [ ] `GET /v1/analytics/revenue` — detailed revenue with filters
- [ ] `GET /v1/analytics/retention` — returning customer cohorts
- [ ] `GET /v1/analytics/heatmap` — busy hours data
- [ ] `GET /v1/analytics/forecast` — revenue forecast (simple moving avg)
- [ ] `GET /v1/inventory` — inventory list
- [ ] `POST /v1/inventory` — add item
- [ ] `PATCH /v1/inventory/{id}/quantity` — update stock
- [ ] Low stock alert Celery task
- [ ] `GET /v1/expenses` — list with filters
- [ ] `POST /v1/expenses` — add expense
- [ ] Profit/loss calculation

#### Frontend
- [ ] Full Analytics dashboard
  - [ ] Revenue graph (period toggle + comparison)
  - [ ] Retention rate card
  - [ ] Busy hours heatmap
  - [ ] Lost customers count
  - [ ] Revenue forecast chart
- [ ] Inventory page
  - [ ] Items table with stock levels
  - [ ] Low stock badges
  - [ ] Add/edit item drawer
  - [ ] Stock adjustment form
- [ ] Expenses page
  - [ ] Expense table by category
  - [ ] Add expense form
  - [ ] Monthly summary
  - [ ] Profit/loss widget

### Week 10: Customer App (Web)

#### Frontend (customer-web app)
- [ ] Customer home page
  - [ ] Salon info + status
  - [ ] [Book Appointment] CTA
  - [ ] [Live Queue] shortcut
  - [ ] Points balance + tier
  - [ ] Upcoming appointment card
  - [ ] Active offers
- [ ] Booking flow (4 steps)
  - [ ] Service selection
  - [ ] Barber selection
  - [ ] Date/time picker
  - [ ] Confirmation + receipt
- [ ] Live queue page (customer view)
- [ ] Booking history
- [ ] Review submission
- [ ] Offers page
- [ ] Profile + settings
- [ ] OTP login flow

---

## Phase 3: AI + WhatsApp + Multi-Branch (Weeks 11–15)

**Goal:** The AI differentiator. Voice calls, WhatsApp automation, AI marketing, multi-branch.

### Week 11–12: AI Voice Receptionist

#### Backend
- [ ] ElevenLabs Conversational AI integration
- [ ] Twilio inbound call handler (webhook)
- [ ] Twilio outbound call initiator
- [ ] Voice agent session manager
- [ ] Customer context builder (for AI system prompt)
- [ ] Booking intent detector
- [ ] Appointment booking via AI
- [ ] Call transcript storage
- [ ] `GET /v1/ai/calls` — call history
- [ ] `POST /v1/ai/calls/initiate` — manual trigger
- [ ] AI credits deduction system
- [ ] Call outcome tracking

#### Frontend
- [ ] AI Features page
  - [ ] AI Receptionist toggle + config
  - [ ] Call logs table (with transcript view)
  - [ ] Credits usage indicator
- [ ] AI Call details drawer (transcript + recording player)
- [ ] AI Credits top-up flow

### Week 12–13: WhatsApp Automation

#### Backend
- [ ] WhatsApp Business API integration
- [ ] Template message management
- [ ] WhatsApp reminder Celery task
- [ ] WhatsApp campaign sender
- [ ] `GET /v1/whatsapp-logs` — message history
- [ ] Opt-out handler (customer replies STOP)

#### Frontend
- [ ] Settings → WhatsApp page
  - [ ] Connect WhatsApp Business number
  - [ ] Template management
  - [ ] Enable/disable per message type
- [ ] WhatsApp logs page

### Week 13–14: AI Marketing Campaigns

#### Backend
- [ ] Campaign CRUD endpoints
- [ ] Campaign audience builder (segment query)
- [ ] AI message generator (OpenAI + Urdu/English)
- [ ] Campaign scheduler Celery task
- [ ] Campaign execution engine
- [ ] Campaign analytics tracker
- [ ] Churn Agent implementation
- [ ] Birthday campaign auto-runner

#### Frontend
- [ ] Campaigns page
  - [ ] Campaign list (status, reach, conversion)
  - [ ] Campaign cards with stats
  - [ ] [+ New Campaign] button
- [ ] Campaign wizard (4 steps)
  - [ ] Trigger selection
  - [ ] Audience builder
  - [ ] Channel + message (with AI draft)
  - [ ] Schedule + review
- [ ] Campaign detail analytics page

### Week 14–15: Multi-Branch Support

#### Backend
- [ ] Branch CRUD endpoints
- [ ] Cross-branch analytics aggregation
- [ ] Branch-level staff assignment
- [ ] Branch-level queue isolation
- [ ] Combined dashboard stats

#### Frontend
- [ ] Branch switcher in sidebar (dropdown)
- [ ] Branch management page (settings)
- [ ] Combined analytics view (all branches)
- [ ] Branch-level filter on all list pages

---

## Phase 4: Future (Post-Launch)

### Customer Marketplace
- [ ] Discovery page: map view of nearby salons
- [ ] Salon profile pages
- [ ] Search by service, area, rating
- [ ] Public reviews + photos

### Advanced AI
- [ ] AI hairstyle preview from selfie (image generation)
- [ ] Predictive demand forecasting
- [ ] Automatic staff scheduling
- [ ] Dynamic pricing for peak hours
- [ ] AI-powered upsell suggestions

### Platform
- [ ] White-label version for chains
- [ ] Franchise management module
- [ ] API for third-party integrations
- [ ] Google Calendar sync
- [ ] POS terminal integration

---

## Technology Checklist

### Dependencies to Install

#### Owner Dashboard (Next.js)
```bash
npx create-next-app@latest owner-dashboard --typescript --tailwind --app
cd owner-dashboard
npx shadcn@latest init
npm install framer-motion @tanstack/react-query zustand i18next react-i18next next-themes
npm install lucide-react recharts date-fns react-hook-form @hookform/resolvers zod
npm install socket.io-client @clerk/nextjs
```

#### Backend (FastAPI)
```bash
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic
pip install pydantic[email] python-jose[cryptography] celery redis
pip install httpx python-multipart pillow
pip install openai elevenlabs twilio firebase-admin
pip install loguru sentry-sdk
```

---

## Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Jazz/Zong API unreliable | Medium | High | Twilio as fallback; retry logic |
| ElevenLabs Urdu quality poor | Medium | High | Test early; keep OpenAI as fallback |
| Easypaisa API approval delayed | High | Medium | Start with Cash only; add digital later |
| WebSocket scaling issues | Low | High | Use Redis pub/sub; Nginx websocket config |
| Customer adoption slow | Medium | High | Onboarding support; demo videos in Urdu |
| Multi-tenancy data leak | Low | Critical | RLS from day 1; automated tests |

---

*Plan updated as phases complete. Track progress in TRACKER.md.*
