# Trimly 💈

> AI-powered salon management SaaS for Pakistan

Trimly is a full-stack SaaS platform that helps salon owners automate operations, retain customers, and grow revenue — powered by AI that speaks Urdu, Punjabi, and English.

---

## What is Trimly?

| For Owners | For Barbers | For Customers |
|---|---|---|
| Dashboard & Analytics | Real-time queue | Online booking |
| Customer CRM | Today's schedule | Live wait time |
| AI reminders | Income tracking | Loyalty points |
| Marketing campaigns | Rating + reviews | Offers & coupons |
| Inventory & Expenses | Leaderboard | Review submission |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, Tailwind CSS, shadcn/ui, Framer Motion |
| Mobile | React Native + Expo |
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 (Neon) |
| Cache + Queue | Redis (Upstash) + Celery |
| Auth | Clerk |
| AI Voice | ElevenLabs Conversational AI |
| SMS | Jazz / Zong / Twilio |
| Payments | Easypaisa / JazzCash / Stripe |
| Storage | Cloudflare R2 |
| Deployment | Vercel (frontend) + Railway (backend) |

---

## Repository Structure

```
trimly/
├── apps/
│   ├── owner-dashboard/    # Next.js 15 — salon owner web app
│   ├── customer-web/       # Next.js 15 — customer booking
│   ├── admin-panel/        # Next.js 15 — Trimly ops
│   └── marketing-site/     # Next.js 15 — landing page
├── services/
│   └── api/                # FastAPI backend
├── packages/
│   ├── ui/                 # Shared React components
│   ├── types/              # Shared TypeScript types
│   └── utils/              # Shared utilities
├── docs/                   # All documentation
│   ├── PRD.md              # Product Requirements
│   ├── TRD.md              # Technical Requirements
│   ├── UI_UX_DETAILS.md    # Design System
│   ├── APP_FLOW.md         # User Journeys
│   ├── DATABASE_SCHEMA.md  # DB Schema
│   ├── IMPLEMENTATION_PLAN.md
│   ├── RULES.md            # Dev Rules
│   └── TRACKER.md          # Progress Tracker
└── README.md
```

---

## Getting Started

### Prerequisites
- Node.js >= 20
- Python 3.12+
- PostgreSQL (or Neon account)
- Redis (or Upstash account)

### Development Setup

```bash
# 1. Clone repository
git clone https://github.com/your-org/trimly.git
cd trimly

# 2. Install dependencies
npm install

# 3. Setup environment variables
cp apps/owner-dashboard/.env.example apps/owner-dashboard/.env.local
cp services/api/.env.example services/api/.env

# 4. Run database migrations
cd services/api
pip install -r requirements.txt
alembic upgrade head

# 5. Start all apps
npm run dev
```

---

## Documentation

| Document | Description |
|---|---|
| [PRD.md](./docs/PRD.md) | Product requirements, personas, revenue model |
| [TRD.md](./docs/TRD.md) | Technical architecture, API design, security |
| [UI_UX_DETAILS.md](./docs/UI_UX_DETAILS.md) | Design system, colors, components, UX flows |
| [APP_FLOW.md](./docs/APP_FLOW.md) | All user journeys and screen transitions |
| [DATABASE_SCHEMA.md](./docs/DATABASE_SCHEMA.md) | PostgreSQL schema with all tables |
| [IMPLEMENTATION_PLAN.md](./docs/IMPLEMENTATION_PLAN.md) | 15-week build plan |
| [RULES.md](./docs/RULES.md) | Engineering rules and code standards |
| [TRACKER.md](./docs/TRACKER.md) | Development progress tracker |

---

## Revenue Model

| Plan | Price | Target |
|---|---|---|
| Starter | Rs. 2,500/month | Small barbershops (1–3 barbers) |
| Professional | Rs. 5,000/month | Growing salons |
| Enterprise | Rs. 12,000/month | Multi-branch chains |

---

## Key AI Features

- 🎙️ **AI Voice Receptionist** — Calls customers in Urdu, Punjabi, English, Roman Urdu
- 🧠 **AI Retention Engine** — Predicts visit frequency, sends reminders at perfect time
- 📢 **AI Marketing** — Auto-generates Urdu/English campaign messages
- 📊 **AI Analytics** — Revenue forecasts, churn detection, barber performance insights
- 💬 **WhatsApp Automation** — Reminders, invoices, review requests, promotions

---

*Built for Pakistan. Designed to be the Linear/Stripe of salon software.*
