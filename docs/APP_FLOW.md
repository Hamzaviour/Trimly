# Trimly — Application Flow Document

**Version:** 1.0  
**Date:** August 2026

---

## Overview

This document maps every user journey, screen transition, and state flow across all Trimly apps.

---

## 1. Platform Structure

```
TRIMLY ECOSYSTEM
├── marketing-site          (trimly.pk)             → Public landing page
├── owner-dashboard         (owner.trimly.pk)        → Salon management
├── customer-web            (book.trimly.pk)         → Customer booking
├── queue-display           (queue.trimly.pk/[slug]) → Lobby TV display
├── admin-panel             (admin.trimly.pk)        → Trimly ops team
└── mobile-app              (iOS + Android)          → Customer + Owner
```

---

## 2. Authentication Flows

### 2.1 Owner Onboarding (New Signup)

```
Landing Page
    │
    ▼
[Get Started] click
    │
    ▼
Signup Screen
  ├── Enter phone number (Pakistani format)
  ├── Receive OTP (Jazz/Zong SMS)
  ├── Verify OTP (6-digit)
  │
  ▼
Onboarding Wizard [5 steps, progress bar shown]
  │
  Step 1: Your Name + Role
  │    ├── Full Name
  │    └── Role: Owner / Manager
  │
  Step 2: Salon Details
  │    ├── Salon Name
  │    ├── Salon Type (dropdown: Barbershop/Hair Salon/Beauty/Ladies/Spa/Nail)
  │    ├── City (dropdown: major Pakistani cities)
  │    └── Phone Number (for customers to call)
  │
  Step 3: Your Team
  │    ├── How many barbers/staff?
  │    ├── Add barbers (name + phone, can skip and do later)
  │    └── [Add Another] / [Skip for Now]
  │
  Step 4: Your Services
  │    ├── Pre-populated list based on salon type
  │    ├── Check services you offer
  │    ├── Set price per service
  │    └── Estimated duration per service
  │
  Step 5: Choose Plan
       ├── Starter  — Rs. 2,500/mo
       ├── Professional — Rs. 5,000/mo [RECOMMENDED badge]
       └── Enterprise — Rs. 12,000/mo
            │
            └── [Start 14-day Free Trial] (no credit card required)
    │
    ▼
Dashboard (Home) ← FIRST TIME: Welcome banner with quick-start checklist
```

### 2.2 Returning Owner Login

```
Login Screen
  ├── Enter phone number
  ├── Receive OTP
  ├── Verify OTP
  └── → Dashboard (last active salon)
```

### 2.3 Barber Login

```
Login Screen
  ├── Enter phone number
  ├── Receive OTP (must be registered barber)
  └── → Barber Dashboard (own view only)
```

### 2.4 Customer Login

```
Book or Queue page (any salon)
  ├── [Login / Sign Up] click
  ├── Enter phone number
  ├── Receive OTP
  ├── Set name (first time only)
  └── → Continue to booking / queue
```

---

## 3. Owner Dashboard Flows

### 3.1 Navigation Structure

```
SIDEBAR
├── 🏠 Home (Dashboard)
├── 📋 Queue (Live)
├── 📅 Appointments
├── 👥 Customers
├── 💇 Barbers
├── 🛍️ Services
├── 💰 Revenue
├── 📦 Inventory
├── 💸 Expenses
├── ⭐ Reviews
├── 🎁 Loyalty
├── 📢 Campaigns
├── 🤖 AI Features
├── 📊 Analytics
├── 🏪 Branches      (Professional+)
└── ⚙️ Settings
     ├── Profile
     ├── Salon Settings
     ├── Business Hours
     ├── Notifications
     ├── Integrations
     └── Billing
```

### 3.2 Add New Customer Flow

```
Customers Page → [+ Add Customer]
    │
    ▼
Side Drawer (not full page — faster)
  ├── Name* (text)
  ├── Phone* (Pakistani format, auto-format)
  ├── Birthday (optional, triggers birthday campaign)
  ├── Gender
  ├── Preferred Barber (dropdown)
  ├── Notes (free text)
  └── [Save Customer]
    │
    ▼
Customer saved → Toast: "Ahmed added ✓"
Customer auto-opens in panel with [Book Appointment] CTA
```

### 3.3 Book Appointment Flow (Owner-initiated)

```
[+ Book Appointment] (from anywhere)
    │
    ▼
Booking Wizard — Slide-in sheet (full right panel)

STEP 1 — Customer
  ├── Search existing customer (by name/phone)
  ├── [+ Add New Customer] inline
  └── Select → proceed

STEP 2 — Service + Barber + Time
  ├── Select service(s) (multi-select allowed, prices shown)
  ├── Select barber (shows availability, rating)
  ├── Select date + time slot
  │    ├── Today's slots shown first
  │    └── Calendar picker for future dates
  └── Estimated duration shown

STEP 3 — Confirm + Notes
  ├── Summary card (customer, service, barber, time, price)
  ├── Payment method (Cash / Easypaisa / JazzCash)
  ├── Notes for barber
  └── [Confirm Booking]
    │
    ▼
Booking confirmed:
  ├── Added to queue / calendar
  ├── Customer receives SMS confirmation
  ├── Barber receives push notification
  └── Success animation + summary
```

### 3.4 Complete a Service Flow

```
Live Queue → Click chair "BUSY" card
    │
    ▼
Chair detail panel:
  ├── Customer name + service
  ├── Timer (started X min ago)
  ├── [Complete Service ✓]
  └── [Extend Time] / [Add Service]
    │
[Complete Service]
    │
    ▼
Invoice generated:
  ├── Services listed with prices
  ├── Total
  ├── Payment collected (mark Cash/Digital)
  └── [Mark Paid]
    │
    ▼
Service complete:
  ├── Customer earns loyalty points (auto)
  ├── Chair status → FREE
  ├── Next customer auto-assigned (if queue)
  └── Review request SMS sent (2hr delay)
```

### 3.5 Add Expense Flow

```
Expenses → [+ Add Expense]
    │
    ▼
Quick form:
  ├── Category (Rent/Electricity/Salary/Products/Water/Other)
  ├── Amount
  ├── Date
  ├── Description (optional)
  └── Receipt photo (optional)
    │
    ▼
Saved → profit/loss auto-updated
```

### 3.6 AI Campaign Flow

```
AI Features → Campaigns → [+ New Campaign]
    │
    ▼
Campaign Wizard:

Step 1 — Trigger
  ├── 🎂 Birthday (runs daily for next 30 days)
  ├── 💤 Inactive customers (last visit > N days)
  ├── 🎉 Festival (Eid, Ramadan, etc.)
  ├── 📅 Scheduled date
  └── 🔁 Recurring (weekly/monthly)

Step 2 — Audience
  ├── All customers
  ├── Customers with [service] preference
  ├── Customers inactive > [X] days
  ├── Loyalty tier (VIP / Regular / New)
  └── Preview: "32 customers will receive this"

Step 3 — Channel + Message
  ├── Channel: SMS / WhatsApp / AI Call (radio)
  ├── Message template (pre-written in Urdu/English)
  ├── [AI Draft ✨] → auto-generates message
  ├── Personalization tokens: {name}, {barber}, {service}
  └── Preview message

Step 4 — Review + Schedule
  ├── Campaign summary
  ├── Credit cost estimate
  └── [Launch Now] or [Schedule for Date]
```

---

## 4. Barber Dashboard Flows

### 4.1 Barber Home View

```
Barber Dashboard
├── TODAY SECTION
│   ├── Customers served: X
│   ├── Revenue generated: Rs. X
│   ├── Rating today: ★ X.X
│   └── Hours worked: X:XX
│
├── CURRENT CUSTOMER
│   ├── Name + service
│   ├── Timer running
│   └── [Complete]
│
├── QUEUE (next up)
│   ├── Next customer name + service
│   └── Estimated time until their turn
│
└── TODAY'S SCHEDULE (timeline)
    ├── 10:00 – Ahmed Khan – Fade Cut
    ├── 11:30 – Bilal – Beard Trim
    └── ...
```

### 4.2 Barber Profile Flow

```
My Profile
├── Photo upload
├── Name, experience, specialties
├── Services offered
├── Bio (shown to customers booking)
└── [Save Changes]
```

---

## 5. Customer App Flows

### 5.1 Customer Home

```
Customer App Home
├── HERO: Salon name + quick status ("2 chairs free")
├── [Book Appointment] → Booking flow
├── [Live Queue] → Queue view
├── My Points: XXX 🌟
├── Upcoming Appointment card (if any)
└── Active Offers
```

### 5.2 Customer Booking Flow

```
[Book Appointment]
    │
    ▼
Step 1 — Choose Service
  ├── Category tabs (Hair / Beard / Facial / Color / ...)
  ├── Service cards with name, price, duration
  └── Multi-select supported

Step 2 — Choose Barber
  ├── "Any Available" (default)
  ├── Barber cards: photo, name, rating, specialties, availability
  └── Select preferred barber

Step 3 — Choose Time
  ├── Date picker (starting from today)
  ├── Available time slots grid
  └── Greyed out = booked slots

Step 4 — Confirm
  ├── Summary: service, barber, time, total
  ├── Payment: Pay now / Pay at salon
  └── [Confirm Booking]
    │
    ▼
Confirmation screen:
  ├── Booking ID + QR code
  ├── [Add to Calendar]
  ├── [Share]
  └── Navigate to Home
```

### 5.3 Live Queue Flow (Customer)

```
[View Live Queue]
    │
    ▼
Queue Page (auto-refreshes every 30s)
  ├── Salon name + address
  ├── Average wait: XX min
  │
  ├── CHAIR GRID:
  │   ├── Chair 1: [BUSY] Ali — 14 min remaining
  │   ├── Chair 2: [FREE] Hassan
  │   └── Chair 3: [BUSY] Kamran — 8 min remaining
  │
  └── WAITING LIST:
      ├── Your position: #2 (if in queue)
      └── Estimated wait: ~22 min
```

### 5.4 Review Flow

```
[2 hours after service completion]

Push/SMS: "How was your experience at Gulshan Barbers? ⭐"
    │
    ▼
Review Screen:
  ├── Star rating (1–5 stars, tap)
  ├── Rate your barber (optional: name shown)
  ├── Quick tags: "Great cut" "Clean" "Friendly" "On time"
  ├── Written review (optional)
  └── [Submit Review]
    │
    ▼
Thank you screen:
  ├── Points earned: +5 bonus
  └── [Book again?]
```

---

## 6. Queue Display Flow (TV Board)

```
URL: queue.trimly.pk/gulshan-barbers

Auto-refresh every 10 seconds (WebSocket preferred)

Display:
├── Salon logo + name (top)
├── Real-time chair cards (grid)
├── Waiting count
└── Average wait time

No login required — public page
```

---

## 7. Admin Panel Flows (Trimly Ops)

```
Admin Panel (admin.trimly.pk)

SECTIONS:
├── Dashboard
│   ├── Total salons
│   ├── Active subscriptions
│   ├── MRR
│   ├── Churn rate
│   └── Recent signups
│
├── Salons
│   ├── List with search/filter
│   ├── Salon detail: subscription, usage, contacts
│   ├── [Impersonate] (for support)
│   └── [Suspend] / [Delete]
│
├── Subscriptions
│   ├── All active plans
│   ├── Renewal dates
│   └── Revenue breakdown
│
├── AI Credits
│   ├── Credit usage per salon
│   ├── Top-up manually
│   └── Usage alerts
│
├── SMS Logs
│   ├── All SMS sent (filterable)
│   └── Delivery status
│
├── Support
│   ├── Open tickets
│   └── Dispute resolution
│
└── Settings
    ├── Pricing config
    ├── Feature flags
    └── Broadcast announcements
```

---

## 8. Notification Flows

### 8.1 Appointment Reminder Flow
```
Appointment created
    │
    ▼
Schedule reminder jobs:
  ├── 24 hours before → Push + WhatsApp
  └── 2 hours before  → Push notification
    │
    ▼
Customer taps notification
    │
    └── Opens appointment detail in app
         ├── [Confirm] (I'll be there)
         ├── [Reschedule]
         └── [Cancel]
```

### 8.2 AI Reminder (Churn Prevention) Flow
```
Celery Cron (runs daily at 10 AM PKT)
    │
    ▼
Query customers:
  ├── last_visit > reminder_threshold_days
  └── not reminded in last 7 days
    │
    ▼
For each customer:
  ├── Calculate churn risk score
  ├── Generate personalized message (OpenAI)
  ├── Choose channel (push → WhatsApp → SMS → AI Call)
  └── Schedule message
    │
    ▼
Message sent → log in ai_tasks table
    │
    ▼
Customer responds / books
    │
    └── Cancel future reminders for this customer
```

### 8.3 Birthday Campaign Flow
```
Daily cron at 9 AM:
  ├── Find customers with birthday today
  ├── Generate birthday message: "Eid Mubarak {name}! 20% off today"
  ├── Send via WhatsApp + SMS
  └── Auto-create discount code (1-day validity)
```

---

## 9. State Machines

### Appointment States
```
PENDING ──────────────────────────────────────────┐
  │                                               │
  ▼ (confirmed by owner/staff)                   │
CONFIRMED                                         │
  │         │                                     │
  ▼         ▼ (customer no-show)                  │
IN_PROGRESS  NO_SHOW                              │
  │                                               │
  ▼ (service completed)                           │
COMPLETED ◄─────────────────────────────────────┘ │
  │                                               │
  └── (CANCELLED at any point before IN_PROGRESS)─┘
```

### Queue Position States
```
WAITING → CALLED → IN_CHAIR → COMPLETED
                 → SKIPPED (customer not present)
```

### Barber Chair States
```
FREE → BUSY → FREE (cycle)
FREE → ON_BREAK → FREE
BUSY → EXTENDED → COMPLETED
```

---

## 10. Error States & Edge Cases

| Scenario | Handling |
|---|---|
| OTP not received | Resend after 60s; fallback to voice OTP |
| Booking slot conflict | Real-time validation; show next available slots |
| Payment failure | Retry prompt; fallback to cash option |
| AI call failed | Log failure; fallback to SMS |
| Queue WebSocket disconnected | Fallback to polling every 30s; reconnection indicator |
| Offline mode | Cache last queue state; grey out booking; "You're offline" banner |
| SMS delivery failed | Retry 3x; log failure; alert owner |
| Barber removed mid-service | Reassign queue to another barber or mark free |
