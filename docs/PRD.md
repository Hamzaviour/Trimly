# Trimly — Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** August 2026  
**Author:** Trimly Product Team  
**Status:** Draft

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Solution Overview](#solution-overview)
4. [Target Market](#target-market)
5. [User Personas](#user-personas)
6. [Product Goals & Success Metrics](#product-goals--success-metrics)
7. [Revenue Model](#revenue-model)
8. [Feature Requirements](#feature-requirements)
9. [User Stories](#user-stories)
10. [Non-Functional Requirements](#non-functional-requirements)
11. [Constraints & Assumptions](#constraints--assumptions)
12. [Roadmap Summary](#roadmap-summary)

---

## Executive Summary

**Trimly** is an AI-powered salon management SaaS platform designed for Pakistan's beauty and grooming industry. It unifies owner operations, barber workflows, and customer engagement into a single intelligent ecosystem — featuring an AI Voice Receptionist that speaks Urdu, Punjabi, English, and Roman Urdu.

Trimly transforms informal, memory-based salon operations into data-driven, automated businesses that retain customers, maximize revenue, and reduce wasted time.

---

## Problem Statement

Pakistan has over **200,000+ salons, barbershops, and beauty parlors**, yet most operate with:

| Pain Point | Impact |
|---|---|
| No customer database | Owners forget returning clients; no personalization |
| No automated reminders | Customers forget to revisit; revenue bleeds |
| No loyalty program | Zero retention incentive; high churn |
| No analytics | Owners don't know what's working |
| No queue visibility | Customers don't know wait times; walkouts happen |
| Phone-based booking | Time wasted; missed calls = missed revenue |
| No digital payments | Cash-only limits tracking and reporting |
| No marketing tools | No way to run promotions or reach inactive customers |
| Language barrier | Most salon tech is in English — not accessible |

> **Result:** An average salon loses 40–60% of first-time customers because there is no system to bring them back.

---

## Solution Overview

Trimly is a **multi-app, multi-role platform**:

```
┌─────────────────────────────────────────────────────┐
│                    TRIMLY PLATFORM                   │
├──────────────┬──────────────┬────────────────────────┤
│  Owner App   │  Barber App  │   Customer App          │
│  Dashboard   │  Dashboard   │   Booking + Queue       │
├──────────────┴──────────────┴────────────────────────┤
│           AI Voice Receptionist (Urdu/Punjabi)        │
├──────────────────────────────────────────────────────┤
│    CRM + Marketing Automation + Business Analytics    │
└──────────────────────────────────────────────────────┘
```

### Core Value Propositions
1. **Never lose a customer again** — AI tracks visit cycles and calls/messages automatically
2. **Zero-effort marketing** — Automated birthday, festival, and churn-prevention campaigns
3. **Live queue transparency** — Customers see estimated wait times from their phone
4. **Urdu-first AI** — Voice receptionist speaks the local language
5. **Complete business intelligence** — Revenue, barber performance, and retention insights

---

## Target Market

### Primary Market
- **Country:** Pakistan
- **Cities (Phase 1):** Lahore, Karachi, Islamabad, Faisalabad, Rawalpindi

### Business Types
| Type | Estimated Count in Pakistan |
|---|---|
| Barbershops | 120,000+ |
| Hair Salons (Men) | 40,000+ |
| Beauty Salons (Women) | 35,000+ |
| Ladies Salons | 20,000+ |
| Spas & Massage Centers | 5,000+ |
| Nail Studios | 3,000+ |

### Total Addressable Market (TAM)
- ~200,000+ salons in Pakistan
- Even 1% penetration = 2,000 salons × Rs. 5,000/month = **Rs. 10M/month ARR**

### Ideal Customer Profile (ICP)
- Salon with **2–15 staff members**
- Located in **urban or semi-urban area**
- Owner is **smartphone literate**
- Has **50–500 regular customers**
- Revenue between **Rs. 50,000–500,000/month**

---

## User Personas

### Persona 1: Salon Owner — "Usman Bhai"
- **Age:** 32–50
- **Tech Level:** Basic smartphone user
- **Goals:** Grow revenue, manage staff, stop customer loss
- **Frustrations:** Doesn't know which barber performs best, forgets to call inactive customers, can't track expenses
- **Language:** Urdu primary

### Persona 2: Barber — "Ali"
- **Age:** 20–35
- **Tech Level:** Low-medium
- **Goals:** Serve customers efficiently, track earnings, build reputation
- **Frustrations:** Manual scheduling, no visibility into tips or ratings
- **Language:** Urdu / Punjabi

### Persona 3: Customer — "Ahmed"
- **Age:** 18–45
- **Tech Level:** Medium (WhatsApp, social media user)
- **Goals:** Book without calling, skip long queues, save money with offers
- **Frustrations:** Not knowing wait times, forgetting to book, no loyalty rewards
- **Language:** Urdu / Roman Urdu

### Persona 4: Receptionist — "Sara"
- **Age:** 22–35
- **Tech Level:** Medium
- **Goals:** Manage walk-ins, record customer info, handle appointments
- **Frustrations:** Paper registers, missed calls, no customer history
- **Language:** Urdu / English

---

## Product Goals & Success Metrics

### 6-Month Goals
| Goal | Target |
|---|---|
| Onboarded salons | 500 |
| Paid subscribers | 200 |
| MRR | Rs. 1,000,000 |
| Avg customer retention improvement | +35% |
| AI voice calls completed | 10,000/month |

### Key Performance Indicators (KPIs)
- **Customer Retention Rate** — % of customers who return within 45 days
- **Booking Conversion Rate** — % of AI reminders that result in bookings
- **Salon Churn Rate** — % of salons who cancel subscription monthly
- **NPS Score** — Measured quarterly per segment (owner, barber, customer)
- **Average Revenue Per Salon** — MRR / Active Salons
- **AI Call Answer Rate** — % of AI calls picked up by customers

---

## Revenue Model

### SaaS Subscription Tiers

| Plan | Price | Features |
|---|---|---|
| **Starter** | Rs. 2,500/month | 1 branch, up to 3 barbers, basic CRM, SMS reminders, queue management |
| **Professional** | Rs. 5,000/month | 1 branch, unlimited barbers, full CRM, loyalty, analytics, WhatsApp |
| **Enterprise** | Rs. 12,000/month | Multi-branch, all features, priority support, custom reports |

### Add-On Revenue
| Add-On | Price |
|---|---|
| AI Voice Calls | Rs. 500 for 100 calls |
| Extra SMS Pack | Rs. 200 for 100 SMS |
| WhatsApp Messages | Rs. 300 for 100 messages |
| Extra Branch | Rs. 2,000/branch/month |
| Marketing Automation | Rs. 1,500/month |
| Custom Domain | Rs. 500/month |
| White Label | Custom enterprise pricing |

---

## Feature Requirements

### MVP Scope (Phase 1)

#### Owner Dashboard
| Feature | Priority | Description |
|---|---|---|
| Today's Overview | P0 | Revenue, customers served, waiting count, appointments |
| Customer Management | P0 | Add, edit, view customer profiles with full history |
| Appointment Booking | P0 | Manual and online booking with barber/service selection |
| Live Queue | P0 | Real-time chair status with estimated wait times |
| Barber Management | P0 | Add barbers, assign services, track performance |
| Service Catalog | P0 | Define services with names, prices, durations |
| Basic Reports | P1 | Daily/weekly/monthly revenue reports |
| Reviews | P1 | Collect and display customer ratings |
| Expenses Tracking | P1 | Log rent, salary, products, utilities |
| Inventory | P2 | Track products, set low-stock alerts |
| Loyalty Program | P2 | Points system, redemption rules |
| Branch Management | P2 | Multi-branch setup and combined analytics |

#### Customer App
| Feature | Priority | Description |
|---|---|---|
| Book Appointment | P0 | Choose service, barber, time slot |
| Live Queue View | P0 | See chair statuses and estimated wait time |
| Booking History | P1 | Past and upcoming appointments |
| Reviews | P1 | Rate and review after visit |
| Offers & Coupons | P1 | View active promotions |
| Loyalty Points | P2 | Points balance and redemption |
| Notifications | P0 | Appointment reminders, queue updates |
| OTP Login | P0 | Pakistani phone number verification |

#### Barber Dashboard
| Feature | Priority | Description |
|---|---|---|
| Current Customer | P0 | See who is currently being served |
| Queue | P0 | See upcoming appointments |
| Today's Summary | P0 | Customers served, revenue, rating |
| Profile & Rating | P1 | Public profile with experience and reviews |
| Income Summary | P1 | Daily/weekly earnings breakdown |

### Phase 2 Features
- SMS Reminders (configurable by service type)
- Push Notifications
- WhatsApp messages
- Loyalty points & rewards
- Full revenue analytics
- Inventory low-stock alerts

### Phase 3 Features
- AI Urdu Voice Receptionist
- WhatsApp automation campaigns
- AI marketing campaigns
- Multi-branch with combined analytics
- AI-powered churn detection

### Phase 4 (Future)
- Customer marketplace (discover nearby salons)
- AI hairstyle preview from selfie
- Franchise management
- White-label version

---

## User Stories

### Owner Stories

```
As a salon owner,
I want to see today's revenue, customers, and queue on one screen
So that I can manage my business without asking staff for updates.

As a salon owner,
I want to add a new customer with their name and phone number
So that I can track their visits and send them reminders.

As a salon owner,
I want to configure loyalty points per visit
So that I can reward returning customers automatically.

As a salon owner,
I want to view which barber generates the most revenue
So that I can reward top performers and coach underperformers.

As a salon owner,
I want to receive alerts when inventory is running low
So that I can reorder before running out.

As a salon owner,
I want to set up birthday discount campaigns
So that customers feel valued on their birthdays.
```

### Customer Stories

```
As a customer,
I want to book an appointment from my phone
So that I don't have to call the salon.

As a customer,
I want to see live chair status and estimated wait time
So that I can decide whether to walk in or wait.

As a customer,
I want to choose my favorite barber
So that I always get the style I prefer.

As a customer,
I want to earn points on every visit
So that I can redeem them for free services.

As a customer,
I want to receive a reminder when it's time for my next haircut
So that I don't forget and my hair stays fresh.
```

### Barber Stories

```
As a barber,
I want to see my upcoming appointments
So that I can prepare and manage my time.

As a barber,
I want to see my total earnings for the day
So that I know how I'm performing.

As a barber,
I want to see my customer reviews
So that I can understand what clients appreciate.
```

---

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | Page load < 2s on 3G; API response < 500ms for 95th percentile |
| **Availability** | 99.9% uptime SLA; planned maintenance windows at 3–5 AM PKT |
| **Scalability** | Support 10,000 concurrent salons; horizontal scaling |
| **Security** | Encrypted data at rest and in transit; OWASP Top 10 compliance |
| **Multi-tenancy** | Complete data isolation per salon (row-level security) |
| **Offline Support** | Basic operations (queue view, check-in) work offline with sync |
| **Localization** | Urdu (RTL) and English support from launch |
| **Accessibility** | WCAG 2.1 AA for customer-facing web app |
| **Mobile First** | All interfaces optimized for mobile; minimum iOS 14, Android 10 |
| **Low Bandwidth** | Optimized for 3G; images lazy-loaded; minimal JS bundles |

---

## Constraints & Assumptions

### Constraints
- Pakistani telecom SMS APIs (Jazz, Zong) have character limits and throttling
- Easypaisa/JazzCash APIs require business verification (plan for Stripe fallback)
- AI voice calls cost money per minute — implement credit system
- PDMA (Pakistan's data law) compliance required for storing customer data

### Assumptions
- Salon owners have Android smartphones (primary target device)
- Customers have WhatsApp installed
- Internet connectivity is available at salon premises (WiFi/data)
- Owners will enter customer data manually initially (no import tool in MVP)
- Barbers share a tablet/screen at the salon (not individual devices in Phase 1)

---

## Roadmap Summary

| Phase | Timeline | Focus |
|---|---|---|
| Phase 1 | Weeks 1–6 | Core salon ops: CRM, queue, booking, dashboard |
| Phase 2 | Weeks 7–10 | Engagement: SMS, push, loyalty, analytics |
| Phase 3 | Weeks 11–15 | AI: Voice receptionist, WhatsApp, multi-branch |
| Phase 4 | Future | Marketplace, AI previews, franchise, white-label |

---

*Document maintained by Trimly Product Team. Update version number with each significant change.*
