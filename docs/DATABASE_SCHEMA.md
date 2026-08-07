# Trimly — Backend Database Schema

**Version:** 1.0  
**Date:** August 2026  
**Database:** PostgreSQL 16  
**ORM:** SQLAlchemy 2.x (async)

---

## Overview

All tables use UUID primary keys. Every business table includes `salon_id` for multi-tenancy via Row Level Security (RLS). Soft deletes via `deleted_at` timestamp where specified.

---

## Table of Contents

1. [Core Tables](#core-tables)
   - users
   - salons
   - branches
   - barbers
   - customers
   - services
   - chairs
2. [Operations Tables](#operations-tables)
   - appointments
   - queue_entries
   - invoices
   - invoice_items
   - payments
3. [Engagement Tables](#engagement-tables)
   - reviews
   - loyalty_points
   - loyalty_redemptions
   - campaigns
   - campaign_recipients
4. [Product Tables](#product-tables)
   - inventory_items
   - inventory_transactions
   - expenses
5. [Communication Tables](#communication-tables)
   - notifications
   - sms_logs
   - whatsapp_logs
   - call_logs
   - ai_tasks
6. [Platform Tables](#platform-tables)
   - subscriptions
   - subscription_plans
   - ai_credits
   - audit_logs
7. [Relationships Diagram](#relationships-diagram)
8. [Indexes](#indexes)
9. [Row Level Security Policies](#row-level-security-policies)
10. [Seed Data](#seed-data)

---

## Core Tables

### `users`
Platform users (owners, managers, barbers, receptionists, customers, admins).

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone           VARCHAR(15) NOT NULL UNIQUE,   -- E.164 format: +923001234567
    name            VARCHAR(100),
    email           VARCHAR(255),
    role            VARCHAR(20) NOT NULL DEFAULT 'CUSTOMER',
                    -- SUPER_ADMIN | OWNER | MANAGER | RECEPTIONIST | BARBER | CUSTOMER
    avatar_url      TEXT,
    language        VARCHAR(10) DEFAULT 'ur',      -- 'ur' or 'en'
    timezone        VARCHAR(50) DEFAULT 'Asia/Karachi',
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_role ON users(role);
```

### `salons`
Salon business entities (one owner can have multiple salons).

```sql
CREATE TABLE salons (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id        UUID NOT NULL REFERENCES users(id),
    name            VARCHAR(100) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,    -- URL-friendly: gulshan-barbers
    type            VARCHAR(30) NOT NULL,
                    -- BARBERSHOP | HAIR_SALON | BEAUTY_SALON | LADIES_SALON
                    -- SPA | MASSAGE_CENTER | NAIL_STUDIO
    phone           VARCHAR(15),
    email           VARCHAR(255),
    address         TEXT,
    city            VARCHAR(50),
    area            VARCHAR(100),
    latitude        DECIMAL(10, 8),
    longitude       DECIMAL(11, 8),
    logo_url        TEXT,
    cover_url       TEXT,
    description     TEXT,
    
    -- Business settings
    currency        VARCHAR(5) DEFAULT 'PKR',
    timezone        VARCHAR(50) DEFAULT 'Asia/Karachi',
    opening_time    TIME DEFAULT '09:00:00',
    closing_time    TIME DEFAULT '21:00:00',
    working_days    INTEGER[] DEFAULT '{1,2,3,4,5,6}',  -- 0=Sun, 6=Sat
    
    -- Loyalty config
    points_per_visit        INTEGER DEFAULT 10,
    points_per_rupee        DECIMAL(5,2) DEFAULT 0,     -- optional: points per Rs spent
    loyalty_tiers_config    JSONB DEFAULT '{}',
    
    -- Reminder config
    reminder_days_haircut   INTEGER DEFAULT 21,
    reminder_days_beard     INTEGER DEFAULT 7,
    reminder_days_facial    INTEGER DEFAULT 30,
    reminder_days_color     INTEGER DEFAULT 45,
    
    -- Feature flags
    queue_enabled           BOOLEAN DEFAULT TRUE,
    online_booking_enabled  BOOLEAN DEFAULT TRUE,
    loyalty_enabled         BOOLEAN DEFAULT TRUE,
    ai_reminders_enabled    BOOLEAN DEFAULT FALSE,
    whatsapp_enabled        BOOLEAN DEFAULT FALSE,
    
    is_active       BOOLEAN DEFAULT TRUE,
    plan            VARCHAR(20) DEFAULT 'STARTER',  -- STARTER | PROFESSIONAL | ENTERPRISE
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_salons_owner ON salons(owner_id);
CREATE INDEX idx_salons_city ON salons(city);
CREATE INDEX idx_salons_slug ON salons(slug);
```

### `branches`
Physical branches of a salon (multi-branch support).

```sql
CREATE TABLE branches (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    name            VARCHAR(100) NOT NULL,           -- "Main Branch", "DHA Branch"
    address         TEXT,
    city            VARCHAR(50),
    phone           VARCHAR(15),
    manager_id      UUID REFERENCES users(id),
    
    opening_time    TIME,
    closing_time    TIME,
    working_days    INTEGER[],
    
    is_active       BOOLEAN DEFAULT TRUE,
    is_main_branch  BOOLEAN DEFAULT FALSE,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_branches_salon ON branches(salon_id);
```

### `barbers`
Staff members who provide services.

```sql
CREATE TABLE barbers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    branch_id       UUID REFERENCES branches(id),
    user_id         UUID REFERENCES users(id),       -- linked user account
    
    name            VARCHAR(100) NOT NULL,
    phone           VARCHAR(15),
    avatar_url      TEXT,
    bio             TEXT,
    experience_years INTEGER DEFAULT 0,
    
    -- Skills
    specialties     TEXT[],                          -- ['fade', 'beard', 'color']
    service_ids     UUID[],                          -- services this barber offers
    
    -- Status
    status          VARCHAR(20) DEFAULT 'AVAILABLE',
                    -- AVAILABLE | BUSY | ON_BREAK | OFF_DUTY
    
    -- Stats (denormalized for performance, updated via trigger)
    total_cuts          INTEGER DEFAULT 0,
    total_revenue       DECIMAL(12, 2) DEFAULT 0,
    average_rating      DECIMAL(3, 2) DEFAULT 0,
    total_reviews       INTEGER DEFAULT 0,
    
    -- Settings
    commission_type     VARCHAR(20) DEFAULT 'FIXED',   -- FIXED | PERCENTAGE
    commission_value    DECIMAL(8, 2) DEFAULT 0,
    
    is_active       BOOLEAN DEFAULT TRUE,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_barbers_salon ON barbers(salon_id);
CREATE INDEX idx_barbers_status ON barbers(status);
```

### `customers`
Customer profiles linked to a salon.

```sql
CREATE TABLE customers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    user_id         UUID REFERENCES users(id),       -- linked if customer has app account
    
    name            VARCHAR(100) NOT NULL,
    phone           VARCHAR(15) NOT NULL,
    email           VARCHAR(255),
    birthday        DATE,
    gender          VARCHAR(10),                     -- MALE | FEMALE | OTHER
    avatar_url      TEXT,
    
    -- CRM Data
    favorite_barber_id  UUID REFERENCES barbers(id),
    favorite_service_id UUID,
    hair_preferences    TEXT,                        -- free text: "never use gel"
    notes           TEXT,
    
    -- Stats (denormalized, updated via triggers)
    total_visits        INTEGER DEFAULT 0,
    total_spent         DECIMAL(12, 2) DEFAULT 0,
    loyalty_points      INTEGER DEFAULT 0,
    average_rating_given DECIMAL(3, 2),
    referral_code       VARCHAR(20) UNIQUE,
    referred_by_id      UUID REFERENCES customers(id),
    
    -- Lifecycle
    first_visit_at      TIMESTAMPTZ,
    last_visit_at       TIMESTAMPTZ,
    next_predicted_visit TIMESTAMPTZ,               -- AI-predicted
    churn_risk_score    DECIMAL(3, 2) DEFAULT 0,    -- 0.0 to 1.0
    
    -- Communication preferences
    sms_consent         BOOLEAN DEFAULT TRUE,
    whatsapp_consent    BOOLEAN DEFAULT TRUE,
    call_consent        BOOLEAN DEFAULT TRUE,
    push_consent        BOOLEAN DEFAULT TRUE,
    
    -- Tags / Segments
    tags            TEXT[] DEFAULT '{}',             -- ['VIP', 'Student', 'Monthly']
    
    is_active       BOOLEAN DEFAULT TRUE,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_customers_salon ON customers(salon_id);
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_last_visit ON customers(last_visit_at);
CREATE INDEX idx_customers_churn_risk ON customers(churn_risk_score);
CREATE UNIQUE INDEX idx_customers_salon_phone ON customers(salon_id, phone);
```

### `services`
Service catalog for each salon.

```sql
CREATE TABLE services (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    
    name            VARCHAR(100) NOT NULL,
    name_ur         VARCHAR(200),                    -- Urdu name
    description     TEXT,
    category        VARCHAR(30),                     -- HAIR | BEARD | FACIAL | COLOR | NAIL | OTHER
    
    price           DECIMAL(10, 2) NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    
    image_url       TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    sort_order      INTEGER DEFAULT 0,
    
    -- Reminder config override (if null, uses salon defaults)
    reminder_days   INTEGER,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_services_salon ON services(salon_id);
CREATE INDEX idx_services_category ON services(category);
```

### `chairs`
Physical chairs/stations in a salon/branch.

```sql
CREATE TABLE chairs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    branch_id       UUID REFERENCES branches(id),
    
    name            VARCHAR(50) NOT NULL,            -- "Chair 1", "VIP Chair"
    number          INTEGER,
    
    assigned_barber_id  UUID REFERENCES barbers(id), -- default assigned barber
    current_status      VARCHAR(20) DEFAULT 'FREE',
                        -- FREE | BUSY | ON_BREAK | MAINTENANCE
    current_customer_id UUID REFERENCES customers(id),
    service_started_at  TIMESTAMPTZ,
    service_estimated_end TIMESTAMPTZ,
    
    is_active       BOOLEAN DEFAULT TRUE,
    sort_order      INTEGER DEFAULT 0,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chairs_salon ON chairs(salon_id);
```

---

## Operations Tables

### `appointments`
Scheduled appointments.

```sql
CREATE TABLE appointments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    branch_id       UUID REFERENCES branches(id),
    
    customer_id     UUID NOT NULL REFERENCES customers(id),
    barber_id       UUID REFERENCES barbers(id),
    chair_id        UUID REFERENCES chairs(id),
    
    -- Appointment details
    scheduled_at    TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER NOT NULL,
    
    status          VARCHAR(20) DEFAULT 'PENDING',
                    -- PENDING | CONFIRMED | IN_PROGRESS | COMPLETED | CANCELLED | NO_SHOW
    
    -- Booking source
    source          VARCHAR(20) DEFAULT 'OWNER',     -- OWNER | CUSTOMER_APP | AI | WALK_IN
    
    -- Notes
    customer_notes  TEXT,
    barber_notes    TEXT,
    
    -- Completion details
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    cancelled_at    TIMESTAMPTZ,
    cancellation_reason TEXT,
    
    -- Payment
    invoice_id      UUID,                            -- set after completion
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_appointments_salon ON appointments(salon_id);
CREATE INDEX idx_appointments_customer ON appointments(customer_id);
CREATE INDEX idx_appointments_barber ON appointments(barber_id);
CREATE INDEX idx_appointments_scheduled ON appointments(scheduled_at);
CREATE INDEX idx_appointments_status ON appointments(status);
```

### `appointment_services`
Services within an appointment (many-to-many).

```sql
CREATE TABLE appointment_services (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id  UUID NOT NULL REFERENCES appointments(id),
    service_id      UUID NOT NULL REFERENCES services(id),
    price           DECIMAL(10, 2) NOT NULL,         -- price at time of booking
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `queue_entries`
Real-time queue management.

```sql
CREATE TABLE queue_entries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    branch_id       UUID REFERENCES branches(id),
    
    customer_id     UUID REFERENCES customers(id),
    appointment_id  UUID REFERENCES appointments(id),
    barber_id       UUID REFERENCES barbers(id),
    chair_id        UUID REFERENCES chairs(id),
    
    -- Queue state
    status          VARCHAR(20) DEFAULT 'WAITING',
                    -- WAITING | CALLED | IN_CHAIR | COMPLETED | SKIPPED | REMOVED
    position        INTEGER,
    
    -- Timing
    joined_at       TIMESTAMPTZ DEFAULT NOW(),
    called_at       TIMESTAMPTZ,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    
    estimated_wait_minutes INTEGER,
    
    -- Customer display token
    token_number    VARCHAR(10),
    
    notes           TEXT,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_queue_salon ON queue_entries(salon_id);
CREATE INDEX idx_queue_status ON queue_entries(status);
CREATE INDEX idx_queue_barber ON queue_entries(barber_id);
```

### `invoices`
Billing records after service completion.

```sql
CREATE TABLE invoices (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    
    customer_id     UUID NOT NULL REFERENCES customers(id),
    barber_id       UUID REFERENCES barbers(id),
    appointment_id  UUID REFERENCES appointments(id),
    
    invoice_number  VARCHAR(30) UNIQUE NOT NULL,     -- TRIMLY-2026-00001
    
    subtotal        DECIMAL(12, 2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(12, 2) DEFAULT 0,
    discount_reason TEXT,
    tax_amount      DECIMAL(12, 2) DEFAULT 0,
    total           DECIMAL(12, 2) NOT NULL,
    
    status          VARCHAR(20) DEFAULT 'UNPAID',    -- UNPAID | PAID | PARTIAL | REFUNDED
    
    payment_method  VARCHAR(20),                     -- CASH | EASYPAISA | JAZZCASH | STRIPE | POINTS
    paid_at         TIMESTAMPTZ,
    pdf_url         TEXT,
    
    loyalty_points_earned   INTEGER DEFAULT 0,
    loyalty_points_used     INTEGER DEFAULT 0,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_invoices_salon ON invoices(salon_id);
CREATE INDEX idx_invoices_customer ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);
```

### `invoice_items`
Line items within an invoice.

```sql
CREATE TABLE invoice_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id      UUID NOT NULL REFERENCES invoices(id),
    service_id      UUID REFERENCES services(id),
    
    name            VARCHAR(100) NOT NULL,
    quantity        INTEGER DEFAULT 1,
    unit_price      DECIMAL(10, 2) NOT NULL,
    total           DECIMAL(10, 2) NOT NULL,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `payments`
Payment transaction records.

```sql
CREATE TABLE payments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    invoice_id      UUID REFERENCES invoices(id),
    
    amount          DECIMAL(12, 2) NOT NULL,
    currency        VARCHAR(5) DEFAULT 'PKR',
    
    method          VARCHAR(20) NOT NULL,            -- CASH | EASYPAISA | JAZZCASH | STRIPE
    status          VARCHAR(20) DEFAULT 'PENDING',   -- PENDING | COMPLETED | FAILED | REFUNDED
    
    -- Gateway details
    gateway_transaction_id  TEXT,
    gateway_response        JSONB,
    
    paid_at         TIMESTAMPTZ,
    refunded_at     TIMESTAMPTZ,
    refund_reason   TEXT,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Engagement Tables

### `reviews`
Customer reviews for visits and barbers.

```sql
CREATE TABLE reviews (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    
    customer_id     UUID NOT NULL REFERENCES customers(id),
    barber_id       UUID REFERENCES barbers(id),
    appointment_id  UUID REFERENCES appointments(id),
    
    overall_rating  SMALLINT NOT NULL CHECK (overall_rating BETWEEN 1 AND 5),
    barber_rating   SMALLINT CHECK (barber_rating BETWEEN 1 AND 5),
    comment         TEXT,
    
    -- Quick tags
    tags            TEXT[] DEFAULT '{}',             -- ['great_cut', 'clean', 'friendly']
    
    -- Moderation
    is_visible      BOOLEAN DEFAULT TRUE,
    owner_reply     TEXT,
    replied_at      TIMESTAMPTZ,
    
    -- Source
    source          VARCHAR(20) DEFAULT 'APP',        -- APP | SMS | WHATSAPP | GOOGLE
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reviews_salon ON reviews(salon_id);
CREATE INDEX idx_reviews_barber ON reviews(barber_id);
CREATE INDEX idx_reviews_customer ON reviews(customer_id);
```

### `loyalty_points`
Loyalty points transaction log.

```sql
CREATE TABLE loyalty_points (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    customer_id     UUID NOT NULL REFERENCES customers(id),
    
    points          INTEGER NOT NULL,                -- positive = earned, negative = redeemed
    type            VARCHAR(30) NOT NULL,
                    -- VISIT_REWARD | REVIEW_BONUS | REFERRAL | BIRTHDAY | REDEMPTION | ADJUSTMENT
    
    reference_id    UUID,                            -- appointment_id or invoice_id
    description     TEXT,
    
    balance_after   INTEGER NOT NULL,                -- running balance after this transaction
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_loyalty_salon ON loyalty_points(salon_id);
CREATE INDEX idx_loyalty_customer ON loyalty_points(customer_id);
```

### `campaigns`
Marketing automation campaigns.

```sql
CREATE TABLE campaigns (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    
    name            VARCHAR(100) NOT NULL,
    type            VARCHAR(30) NOT NULL,
                    -- BIRTHDAY | INACTIVE | FESTIVAL | SCHEDULED | RECURRING | CHURN
    
    -- Targeting
    target_segment  JSONB,                           -- {min_days_inactive: 30, tags: ['VIP']}
    estimated_reach INTEGER,
    
    -- Content
    channel         VARCHAR(20) NOT NULL,            -- SMS | WHATSAPP | AI_CALL | PUSH
    message_template TEXT NOT NULL,
    message_ur      TEXT,                            -- Urdu version
    
    -- Discount / offer
    discount_type   VARCHAR(20),                     -- PERCENTAGE | FIXED | FREE_SERVICE
    discount_value  DECIMAL(8, 2),
    coupon_code     VARCHAR(20),
    coupon_expiry   TIMESTAMPTZ,
    
    -- Scheduling
    status          VARCHAR(20) DEFAULT 'DRAFT',     -- DRAFT | SCHEDULED | ACTIVE | COMPLETED | PAUSED
    scheduled_at    TIMESTAMPTZ,
    
    -- Results (updated as campaign runs)
    sent_count      INTEGER DEFAULT 0,
    delivered_count INTEGER DEFAULT 0,
    opened_count    INTEGER DEFAULT 0,
    booked_count    INTEGER DEFAULT 0,               -- appointments generated
    
    -- Credit cost
    credits_used    INTEGER DEFAULT 0,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `campaign_recipients`
Individual campaign sends.

```sql
CREATE TABLE campaign_recipients (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id     UUID NOT NULL REFERENCES campaigns(id),
    customer_id     UUID NOT NULL REFERENCES customers(id),
    
    status          VARCHAR(20) DEFAULT 'PENDING',   -- PENDING | SENT | DELIVERED | FAILED | BOOKED
    sent_at         TIMESTAMPTZ,
    delivered_at    TIMESTAMPTZ,
    booked_at       TIMESTAMPTZ,                     -- set if customer booked after campaign
    
    appointment_id  UUID REFERENCES appointments(id), -- booking generated by campaign
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Product Tables

### `inventory_items`
Products/supplies in salon inventory.

```sql
CREATE TABLE inventory_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    
    name            VARCHAR(100) NOT NULL,
    category        VARCHAR(50),                     -- SHAMPOO | WAX | COLOR | RAZOR | GEL | OTHER
    brand           VARCHAR(100),
    unit            VARCHAR(20) DEFAULT 'piece',     -- piece | ml | gram | bottle
    
    current_quantity    DECIMAL(10, 2) DEFAULT 0,
    low_stock_threshold DECIMAL(10, 2) DEFAULT 5,
    reorder_quantity    DECIMAL(10, 2),
    
    cost_per_unit   DECIMAL(10, 2),
    
    alert_sent_at   TIMESTAMPTZ,                     -- when low stock alert was last sent
    
    is_active       BOOLEAN DEFAULT TRUE,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `inventory_transactions`
Inventory movement log.

```sql
CREATE TABLE inventory_transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    item_id         UUID NOT NULL REFERENCES inventory_items(id),
    
    type            VARCHAR(20) NOT NULL,            -- PURCHASE | USAGE | ADJUSTMENT | RETURN
    quantity        DECIMAL(10, 2) NOT NULL,         -- positive = added, negative = used
    cost            DECIMAL(10, 2),
    
    notes           TEXT,
    created_by      UUID REFERENCES users(id),
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `expenses`
Business expense tracking.

```sql
CREATE TABLE expenses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    branch_id       UUID REFERENCES branches(id),
    
    category        VARCHAR(30) NOT NULL,
                    -- RENT | ELECTRICITY | SALARY | PRODUCTS | WATER | MAINTENANCE | OTHER
    description     TEXT,
    amount          DECIMAL(12, 2) NOT NULL,
    expense_date    DATE NOT NULL,
    
    receipt_url     TEXT,
    notes           TEXT,
    
    created_by      UUID REFERENCES users(id),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_expenses_salon ON expenses(salon_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
```

---

## Communication Tables

### `notifications`
In-app notifications.

```sql
CREATE TABLE notifications (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id),
    salon_id        UUID REFERENCES salons(id),
    
    type            VARCHAR(50) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    body            TEXT NOT NULL,
    
    data            JSONB DEFAULT '{}',              -- action payload
    action_url      TEXT,
    
    is_read         BOOLEAN DEFAULT FALSE,
    read_at         TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
```

### `sms_logs`
SMS delivery tracking.

```sql
CREATE TABLE sms_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID REFERENCES salons(id),
    
    to_phone        VARCHAR(15) NOT NULL,
    message         TEXT NOT NULL,
    
    type            VARCHAR(30),                     -- APPOINTMENT_CONFIRM | REMINDER | CAMPAIGN
    reference_id    UUID,
    
    provider        VARCHAR(20),                     -- JAZZ | ZONG | TWILIO
    provider_message_id TEXT,
    
    status          VARCHAR(20) DEFAULT 'PENDING',   -- PENDING | SENT | DELIVERED | FAILED
    
    sent_at         TIMESTAMPTZ,
    delivered_at    TIMESTAMPTZ,
    
    cost_credits    INTEGER DEFAULT 1,
    error_message   TEXT,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `call_logs`
AI voice call records.

```sql
CREATE TABLE call_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    customer_id     UUID REFERENCES customers(id),
    
    to_phone        VARCHAR(15) NOT NULL,
    direction       VARCHAR(10) DEFAULT 'OUTBOUND',  -- OUTBOUND | INBOUND
    
    type            VARCHAR(30),                     -- REMINDER | REVIEW | CAMPAIGN | RECEPTIONIST
    
    status          VARCHAR(20),                     -- INITIATED | ANSWERED | COMPLETED | FAILED | NO_ANSWER
    
    duration_seconds INTEGER DEFAULT 0,
    
    -- AI details
    ai_provider     VARCHAR(20),                     -- ELEVENLABS | OPENAI | OMNIDIMENSION
    transcript      TEXT,
    recording_url   TEXT,
    
    -- Outcome
    outcome         VARCHAR(30),                     -- BOOKED | DECLINED | NO_ANSWER | CALLBACK
    appointment_id  UUID REFERENCES appointments(id),
    
    cost_credits    INTEGER DEFAULT 5,
    
    initiated_at    TIMESTAMPTZ DEFAULT NOW(),
    answered_at     TIMESTAMPTZ,
    ended_at        TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `ai_tasks`
AI agent task queue and history.

```sql
CREATE TABLE ai_tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    customer_id     UUID REFERENCES customers(id),
    
    task_type       VARCHAR(30) NOT NULL,
                    -- REMINDER | CHURN | BIRTHDAY | REVIEW_REQUEST | CAMPAIGN
    
    status          VARCHAR(20) DEFAULT 'PENDING',
                    -- PENDING | PROCESSING | COMPLETED | FAILED | SKIPPED
    
    priority        INTEGER DEFAULT 5,               -- 1 (highest) to 10 (lowest)
    
    payload         JSONB DEFAULT '{}',
    result          JSONB DEFAULT '{}',
    error_message   TEXT,
    
    scheduled_for   TIMESTAMPTZ,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    
    retry_count     INTEGER DEFAULT 0,
    max_retries     INTEGER DEFAULT 3,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ai_tasks_status ON ai_tasks(status, scheduled_for);
CREATE INDEX idx_ai_tasks_salon ON ai_tasks(salon_id);
```

---

## Platform Tables

### `subscription_plans`
Available Trimly plans.

```sql
CREATE TABLE subscription_plans (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(50) NOT NULL,             -- Starter | Professional | Enterprise
    slug            VARCHAR(30) UNIQUE NOT NULL,
    
    price_monthly   DECIMAL(10, 2) NOT NULL,
    price_yearly    DECIMAL(10, 2),
    currency        VARCHAR(5) DEFAULT 'PKR',
    
    -- Feature limits
    max_branches    INTEGER DEFAULT 1,
    max_barbers     INTEGER DEFAULT 3,
    max_customers   INTEGER DEFAULT 500,
    sms_included    INTEGER DEFAULT 100,
    ai_credits_included INTEGER DEFAULT 0,
    
    -- Features
    features        JSONB DEFAULT '{}',
                    -- {loyalty: true, analytics: true, whatsapp: false, ...}
    
    is_active       BOOLEAN DEFAULT TRUE,
    sort_order      INTEGER DEFAULT 0,
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `subscriptions`
Salon subscription records.

```sql
CREATE TABLE subscriptions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID NOT NULL REFERENCES salons(id),
    plan_id         UUID NOT NULL REFERENCES subscription_plans(id),
    
    status          VARCHAR(20) DEFAULT 'ACTIVE',
                    -- TRIAL | ACTIVE | PAST_DUE | CANCELLED | EXPIRED
    
    trial_ends_at   TIMESTAMPTZ,
    current_period_start TIMESTAMPTZ,
    current_period_end   TIMESTAMPTZ,
    
    -- Payment
    payment_method  VARCHAR(20),
    last_payment_at TIMESTAMPTZ,
    next_billing_at TIMESTAMPTZ,
    
    -- Credits
    sms_credits_remaining   INTEGER DEFAULT 0,
    ai_credits_remaining    INTEGER DEFAULT 0,
    
    cancellation_reason TEXT,
    cancelled_at        TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### `audit_logs`
Complete audit trail for compliance.

```sql
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    salon_id        UUID REFERENCES salons(id),
    
    actor_id        UUID REFERENCES users(id),
    actor_role      VARCHAR(20),
    
    action          VARCHAR(100) NOT NULL,           -- e.g., 'customer.created', 'appointment.cancelled'
    resource_type   VARCHAR(50),
    resource_id     UUID,
    
    changes         JSONB DEFAULT '{}',              -- {before: {...}, after: {...}}
    metadata        JSONB DEFAULT '{}',              -- IP, user agent, etc.
    
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_salon ON audit_logs(salon_id);
CREATE INDEX idx_audit_actor ON audit_logs(actor_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
```

---

## Relationships Diagram

```
users ──────────────────────────── salons (owner_id)
  │                                   │
  │                              branches (salon_id)
  │                                   │
  ├── barbers (user_id) ──────── chairs (barber_id)
  │                                   │
  └── customers (user_id)        appointments
          │                          │
          └────────────────── queue_entries
                                     │
                                  invoices
                                     │
                               invoice_items
                                     │
                                  payments

salons ─── services (salon_id)
       ─── inventory_items
       ─── expenses
       ─── campaigns ─── campaign_recipients ─── customers
       ─── reviews
       ─── loyalty_points ─── customers
       ─── ai_tasks
       ─── call_logs
       ─── sms_logs
       ─── subscriptions ─── subscription_plans
```

---

## Row Level Security Policies

```sql
-- Enable RLS on all tenant tables
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE barbers ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
-- ... (all salon-scoped tables)

-- Policy: Users only see their salon's data
CREATE POLICY salon_isolation_policy ON customers
    FOR ALL
    USING (salon_id = current_setting('app.current_salon_id', true)::uuid
           OR current_setting('app.role', true) = 'SUPER_ADMIN');

-- Barbers: only see their own records + salon public data  
CREATE POLICY barber_own_policy ON barbers
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id', true)::uuid
           OR salon_id = current_setting('app.current_salon_id', true)::uuid);
```

---

## Seed Data

```sql
-- Seed default subscription plans
INSERT INTO subscription_plans (name, slug, price_monthly, max_branches, max_barbers, max_customers, sms_included, ai_credits_included, features) VALUES
('Starter',      'starter',      2500,  1, 3,         500,  100, 0,   '{"loyalty": false, "analytics": false, "whatsapp": false, "ai_reminders": false}'),
('Professional', 'professional', 5000,  1, NULL,      5000, 300, 50,  '{"loyalty": true, "analytics": true, "whatsapp": true, "ai_reminders": true}'),
('Enterprise',   'enterprise',   12000, NULL, NULL,   NULL, 1000, 200, '{"loyalty": true, "analytics": true, "whatsapp": true, "ai_reminders": true, "multi_branch": true, "custom_reports": true}');

-- Seed default service categories and common services (applied at onboarding)
-- These are templates copied into the salon's services table on signup

-- Common Pakistani barbershop services
-- Hair Cut: Rs. 200–400, 30 min
-- Beard Trim: Rs. 100–200, 15 min  
-- Shave: Rs. 100–150, 20 min
-- Facial: Rs. 300–600, 45 min
-- Hair Color: Rs. 500–2000, 90 min
-- Head Massage: Rs. 150–300, 20 min
```
