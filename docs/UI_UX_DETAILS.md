# Trimly — UI/UX Design System & Guidelines

**Version:** 1.0  
**Date:** August 2026  
**Author:** Trimly Design Team  
**Philosophy:** "Design like it belongs to a billion-dollar startup. Never ship generic."

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Design Inspiration](#design-inspiration)
3. [Color System](#color-system)
4. [Typography System](#typography-system)
5. [Spacing & Layout](#spacing--layout)
6. [Component Library](#component-library)
7. [Screen-by-Screen UX Guide](#screen-by-screen-ux-guide)
8. [AI Feature UX](#ai-feature-ux)
9. [Micro-Interactions & Animations](#micro-interactions--animations)
10. [Responsive Design](#responsive-design)
11. [Accessibility](#accessibility)
12. [Dark Mode](#dark-mode)
13. [Urdu/RTL Support](#urdurtl-support)
14. [Design Tokens (CSS Variables)](#design-tokens-css-variables)
15. [Component Code Patterns](#component-code-patterns)

---

## Design Philosophy

Trimly is designed with the principle: **"Clarity before complexity, speed before decoration."**

Every screen must answer three questions instantly:
1. **What can I do here?**
2. **Where am I in the app?**
3. **What should I click next?**

### Design Mindset Hierarchy
```
Before building any screen, think as:
  1. Senior UX Designer      → Is this the simplest solution?
  2. Product Manager         → Does this solve the user's real problem?
  3. Frontend Architect      → Is this scalable and reusable?
  4. SaaS Founder            → Does this increase retention and revenue?
```

### Design DONTs
- ❌ Never use gradients as backgrounds (use them subtly only for accents)
- ❌ Never overcrowd a screen with information
- ❌ Never use placeholder text as labels (always use floating labels)
- ❌ Never show empty states without a CTA
- ❌ Never use more than 3 font sizes on one screen
- ❌ Never ship without loading skeletons
- ❌ Never ship without error states

### Design DOs
- ✅ Use premium whitespace — breathing room is a feature
- ✅ Minimal borders — use shadows and spacing instead
- ✅ Soft, layered shadows for depth
- ✅ Glass morphism only for overlays, not layouts
- ✅ Animate every meaningful interaction
- ✅ Every empty state must have an illustration + action
- ✅ Always show confirmation feedback

---

## Design Inspiration

| Brand | What We Take |
|---|---|
| **Linear** | Sidebar layout, command palette, keyboard-first UX, motion |
| **Stripe** | Data hierarchy, clean tables, trust signals, typography |
| **Notion** | Comfortable reading typography, block-based layouts |
| **Apple** | Whitespace, product photography, attention to detail |
| **Raycast** | Micro-animations, command bar, instant feedback |
| **Vercel** | Dark mode, deployment UI, status indicators |
| **Clerk** | Onboarding flow, auth screens |
| **Supabase** | Dashboard layout, developer-friendly UI |
| **OpenAI** | AI chat UX, streaming text, simplicity |
| **Arc Browser** | Sidebar, color theming, tab management |

**Design Target Statement:**
> "Use the visual quality of Linear, the clean hierarchy of Stripe, the typography of Notion, the polish of Apple, the interactions of Raycast, and the simplicity of OpenAI. Prioritize speed, clarity, and trust over decorative effects."

---

## Color System

### Base Palette

```css
/* === PRIMARY === */
--color-black:        #09090B;   /* Near-black background */
--color-white:        #FFFFFF;
--color-bg-light:     #FAFAFA;   /* Off-white surface */
--color-bg-dark:      #09090B;   /* Dark mode background */

/* === BRAND EMERALD (Primary Action) === */
--color-emerald-50:   #ECFDF5;
--color-emerald-100:  #D1FAE5;
--color-emerald-200:  #A7F3D0;
--color-emerald-400:  #34D399;
--color-emerald-500:  #10B981;   /* Primary brand color */
--color-emerald-600:  #059669;   /* Hover state */
--color-emerald-700:  #047857;   /* Active state */
--color-emerald-900:  #064E3B;

/* === BRAND BLUE (Secondary Action) === */
--color-blue-500:     #3B82F6;
--color-blue-600:     #2563EB;

/* === ACCENT GOLD (Premium / Loyalty) === */
--color-gold-400:     #FBBF24;
--color-gold-500:     #F59E0B;
--color-gold-600:     #D97706;

/* === GRAY SCALE === */
--color-gray-50:      #F9FAFB;
--color-gray-100:     #F3F4F6;
--color-gray-200:     #E5E7EB;
--color-gray-300:     #D1D5DB;
--color-gray-400:     #9CA3AF;
--color-gray-500:     #6B7280;
--color-gray-600:     #4B5563;
--color-gray-700:     #374151;
--color-gray-800:     #1F2937;
--color-gray-900:     #111827;
--color-gray-950:     #030712;

/* === SEMANTIC COLORS === */
--color-success:      #10B981;
--color-danger:       #EF4444;
--color-warning:      #F59E0B;
--color-info:         #3B82F6;

/* === SLATE (Muted) === */
--color-muted:        #64748B;
--color-muted-light:  #CBD5E1;
```

### Color Usage Guide

| Use Case | Light Mode | Dark Mode |
|---|---|---|
| Page background | `#FAFAFA` | `#09090B` |
| Card background | `#FFFFFF` | `#111111` |
| Card border | `#E5E7EB` | `#1F2937` |
| Primary text | `#09090B` | `#F9FAFB` |
| Secondary text | `#6B7280` | `#9CA3AF` |
| Primary action button | `#10B981` | `#10B981` |
| Primary action hover | `#059669` | `#059669` |
| Destructive action | `#EF4444` | `#EF4444` |
| Success badge | `#D1FAE5` / `#059669` | `#064E3B` / `#34D399` |
| Revenue/Money | `#10B981` (emerald) | `#34D399` |
| AI features | Blue gradient | Blue gradient |
| Loyalty/Premium | Gold | Gold |

---

## Typography System

### Font Stack

```css
/* Primary: Inter — Clean, readable, modern */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Display: Cal Sans or Geist — for large headings */
/* Monospace: JetBrains Mono — for code, IDs, phone numbers */

--font-sans:  'Inter', system-ui, -apple-system, sans-serif;
--font-mono:  'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale

```css
--text-xs:    0.75rem;    /* 12px  — Labels, badges, captions */
--text-sm:    0.875rem;   /* 14px  — Secondary text, table data */
--text-base:  1rem;       /* 16px  — Body text, form inputs */
--text-lg:    1.125rem;   /* 18px  — Card headings */
--text-xl:    1.25rem;    /* 20px  — Section titles */
--text-2xl:   1.5rem;     /* 24px  — Page subtitles */
--text-3xl:   1.875rem;   /* 30px  — Page titles */
--text-4xl:   2.25rem;    /* 36px  — Dashboard metrics */
--text-5xl:   3rem;       /* 48px  — Hero / Marketing */
--text-6xl:   3.75rem;    /* 60px  — Marketing landing */
```

### Font Weight Usage

| Weight | Use Case |
|---|---|
| 400 Regular | Body text, descriptions |
| 500 Medium | Labels, nav items, table headers |
| 600 Semibold | Card headings, button text |
| 700 Bold | Dashboard metrics, section titles |
| 800 Extrabold | Hero headlines, large numbers |

### Typography Rules
- Dashboard metric numbers: `text-4xl font-bold tracking-tight`
- Page titles: `text-3xl font-semibold tracking-tight`
- Section headers: `text-xl font-semibold`
- Table headers: `text-xs font-semibold uppercase tracking-wider text-muted`
- Body: `text-sm font-normal leading-relaxed`
- Urdu text: Use `font-nastaliq` or `font-noto-nastaliq` with `dir="rtl"`

---

## Spacing & Layout

### Spacing Scale (Tailwind-compatible)
```
4px   → gap-1  (tight elements)
8px   → gap-2  (icon to label)
12px  → gap-3  (form fields)
16px  → gap-4  (card padding, common gap)
20px  → gap-5  (section elements)
24px  → gap-6  (card to card)
32px  → gap-8  (section gaps)
48px  → gap-12 (major section separation)
64px  → gap-16 (page sections)
```

### Layout Grid

```
Owner Dashboard:
  Sidebar:     240px fixed (collapsible to 64px)
  Main:        fluid
  Right panel: 320px (optional context panel)

Customer App:
  Single column, max-width 480px centered on desktop
  Full width on mobile

Admin Panel:
  Sidebar:     200px fixed
  Main:        fluid
  Max width:   1400px
```

### Border Radius Scale
```css
--radius-sm:   4px;    /* Badges, tags */
--radius-md:   8px;    /* Buttons, inputs */
--radius-lg:   12px;   /* Cards */
--radius-xl:   16px;   /* Modals, large cards */
--radius-2xl:  24px;   /* Premium cards, hero sections */
--radius-full: 9999px; /* Pills, avatars */
```

### Shadow Scale
```css
--shadow-sm:  0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md:  0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg:  0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl:  0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-card: 0 0 0 1px rgb(0 0 0 / 0.04), 0 2px 8px rgb(0 0 0 / 0.08);
```

---

## Component Library

### Core Components to Build

#### 1. Sidebar Navigation
```
Structure:
  - Logo + salon name (top)
  - Navigation items with icons
  - Collapsible sections (grouped nav)
  - Active state: emerald bg-tint + left border accent
  - Hover state: subtle bg change + smooth 150ms transition
  - Bottom: User avatar + settings + plan badge
  - Collapsed mode: icons only with tooltips
  - Keyboard shortcut hints (like Linear)
```

#### 2. Stats Card
```
Structure:
  - Icon (colored, top-left)
  - Metric (large, bold number)
  - Label (muted small text)
  - Trend indicator (↑ +12% vs last week)
  - Sparkline (optional mini chart)
  
States:
  - Default | Loading skeleton | Error
```

#### 3. Data Table
```
Structure:
  - Sticky header with sort arrows
  - Checkbox for bulk actions
  - Avatar + name column pattern
  - Status badge column
  - Actions column (hover to reveal)
  - Empty state with illustration + CTA
  - Pagination (clean, not cluttered)
  - Search + filter bar above

Interaction:
  - Row click → slide-in detail panel
  - Hover → subtle row highlight
  - Sort → animated arrow + column highlight
```

#### 4. Booking Calendar
```
Structure:
  - Month/Week/Day views
  - Barber filter (avatars at top)
  - Time slots color-coded by barber
  - Drag to reschedule
  - Click to create booking
  - Hover card preview of appointment

Colors:
  - Each barber gets a distinct hue
  - Booked: solid color
  - Available: lighter shade
  - Blocked: gray hatched
```

#### 5. Queue Board
```
Structure:
  - Chair cards (grid layout)
  - Each card shows:
    ├── Chair number/name
    ├── Barber avatar + name
    ├── Status (BUSY / FREE / ON_BREAK)
    ├── Customer name (if busy)
    ├── Service type
    ├── Estimated completion (countdown timer)
    └── Progress bar
  
Status Colors:
  - FREE:     emerald bg
  - BUSY:     blue bg with countdown
  - ON_BREAK: amber bg
```

#### 6. Customer Profile Card
```
Structure:
  - Avatar (large, with loyalty tier badge)
  - Name + phone
  - "Member since" + last visit
  - Stats row: Visits | Spend | Points | Rating
  - Favorite barber + favorite service chips
  - Recent visits timeline
  - Notes section
  - Quick actions: Book | Message | Call | Add Note
```

#### 7. Barber Card (Leaderboard)
```
Structure:
  - Rank badge (1st = gold, 2nd = silver, 3rd = bronze)
  - Avatar with online indicator
  - Name + experience years
  - ★ Rating (large, with count)
  - Stats: Cuts today | Revenue | Reviews
  - Current status chip
  - Revenue bar (relative to top earner)
```

#### 8. AI Feature Panel
```
Structure:
  - Gradient border (emerald to blue)
  - "AI" badge (pulsing dot)
  - Feature name
  - Status: Active | Training | Pending
  - Action button
  - Last activity timestamp
  - Quick stats (calls made, messages sent)
```

#### 9. Notification Bell
```
Structure:
  - Bell icon with unread badge (red dot)
  - Popover with grouped notifications:
    ├── Today
    └── Earlier
  - Notification types with distinct icons
  - Mark all read button
  - Hover animation on bell
```

#### 10. Command Palette
```
Trigger: Cmd/Ctrl + K
Structure:
  - Search input (auto-focused)
  - Results grouped:
    ├── Quick Actions (Book, Add Customer, etc.)
    ├── Navigate (pages)
    ├── Recent customers
    └── Recent appointments
  - Keyboard navigation (↑↓ arrows)
  - Smooth open/close animation (scale + fade)
```

---

## Screen-by-Screen UX Guide

### Screen 1: Owner Dashboard (Home)

**UX Reasoning:**
- Owner checks dashboard first thing in the morning → needs instant insight
- Sequence: Revenue → Customers today → Queue → Alerts → Analytics

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ SIDEBAR │                MAIN CONTENT                    │
│         │  ┌─────────────────────────────────────────┐  │
│  Logo   │  │  Good morning, Usman ☀️  [Today's date]  │  │
│  -----  │  └─────────────────────────────────────────┘  │
│  Home ← │                                                │
│  Queue  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│  Book   │  │ Rev  │ │Cust  │ │Queue │ │ Appt │ Stats    │
│  CRM    │  │today │ │today │ │ now  │ │today │ cards    │
│  Staff  │  └──────┘ └──────┘ └──────┘ └──────┘         │
│  Analy  │                                                │
│  Setup  │  ┌────────────────────┐  ┌─────────────────┐  │
│  -----  │  │ Revenue Graph      │  │  Live Queue     │  │
│  [User] │  │ (7-day chart)      │  │  Chair 1: BUSY  │  │
│         │  │                    │  │  Chair 2: FREE  │  │
└─────────┘  └────────────────────┘  └─────────────────┘  │
             ┌────────────────────┐  ┌─────────────────┐  │
             │ Top Barbers        │  │  Today's Appts  │  │
             │ (leaderboard mini) │  │  (timeline)     │  │
             └────────────────────┘  └─────────────────┘  │
```

**Key UX Decisions:**
- Stats cards are clickable → navigate to detail page
- Revenue graph defaults to last 7 days, easy toggle to 30/90 days
- Live queue updates in real-time (no refresh needed)
- AI insight banner: "⚡ 3 customers haven't visited in 30+ days" → one click to act

---

### Screen 2: Live Queue

**UX Reasoning:**
- Primary use: barber checks next customer; owner monitors flow
- Needs to be glanceable in 2 seconds
- Large text for across-room viewing

**Layout:**
```
┌────────────────────────────────────────────────────────┐
│  Live Queue            [Add Walk-in] [Manage]          │
├────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ CHAIR 1 🟢   │  │ CHAIR 2 🔵   │  │ CHAIR 3 🟡   │ │
│  │ Ali Barber   │  │ Hassan       │  │ ON BREAK     │ │
│  │              │  │ Ahmed Khan   │  │ Returns 3:30 │ │
│  │   FREE       │  │ Fade Cut     │  │              │ │
│  │              │  │ ████████░░   │  │              │ │
│  │ [Assign]     │  │ Ends ~14 min │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├────────────────────────────────────────────────────────┤
│  WAITING (3)                                           │
│  ┌──────────────────────────────────────────────────┐ │
│  │ #1  Bilal Ahmed   Beard Trim     ~14 min  [Assign]│ │
│  │ #2  Sara Khan     Hair Color     ~29 min  [Assign]│ │
│  │ #3  Walk-in       Not specified  ~45 min  [Assign]│ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

### Screen 3: Customer CRM

**UX Reasoning:**
- Owner needs to quickly find any customer and take action
- Most common action: search → view → book or message

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Customers                    [+ Add Customer] [Import]  │
│ ─────────────────────────────────────────────────────── │
│ 🔍 Search by name or phone...  [Filter ▾] [Sort ▾]     │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ □  CUSTOMER        VISITS  LAST VISIT  SPENT  STATUS│ │
│ │ □  Ahmed Khan      17      3 days      Rs.45k  VIP  │ │
│ │ □  Bilal Ahmed     4       21 days     Rs.8k   ⚠️   │ │  
│ │ □  Sara Malik      1       45 days     Rs.2k   Lost │ │
│ └─────────────────────────────────────────────────────┘ │
│                                         (click row →)   │
└─────────────────────────────────────────────────────────┘
                                    ┌──────────────────────┐
                            SLIDE   │  Ahmed Khan          │
                            IN      │  0300-1234567        │
                            PANEL → │  ──────────────────  │
                                    │  17 visits  Rs.45k   │
                                    │  ──────────────────  │
                                    │  Last: Fade Cut      │
                                    │  Barber: Ali         │
                                    │  Points: 170 🌟      │
                                    │  ──────────────────  │
                                    │  [Book] [Message]    │
                                    │  [AI Call] [History] │
                                    └──────────────────────┘
```

**Customer Status Tags:**
| Tag | Condition | Color |
|---|---|---|
| 🌟 VIP | 10+ visits OR Rs.20k+ spent | Gold |
| ✅ Active | Last visit < 21 days | Emerald |
| ⚠️ At Risk | Last visit 21–45 days | Amber |
| 🔴 Lost | Last visit > 45 days | Red |
| 🆕 New | First visit | Blue |

---

### Screen 4: Appointment Booking (Owner view)

**Flow (3-step wizard):**
```
Step 1: Customer          Step 2: Service + Barber     Step 3: Confirm
┌────────────┐            ┌────────────────────┐        ┌──────────────┐
│ Search or  │            │ Services:          │        │ Summary:     │
│ Add new    │     →      │ ○ Hair Cut  Rs.300 │   →    │ Ahmed Khan   │
│ customer   │            │ ● Beard    Rs.150  │        │ Beard Trim   │
│            │            │ ○ Facial   Rs.500  │        │ Ali Barber   │
│ [Ahmed ✓]  │            │ ─────────────────  │        │ Today 3:00pm │
└────────────┘            │ Barber:            │        │              │
                          │ [Ali] [Hassan] [Any│        │ Rs. 150      │
                          │ ─────────────────  │        │ [Confirm ✓]  │
                          │ Time: 3:00 PM ✓    │        └──────────────┘
                          └────────────────────┘
```

---

### Screen 5: Analytics Dashboard

**Layout — 6 key sections:**
```
1. Revenue Overview (graph + period toggle)
2. Customer Retention (cohort or returning %)
3. Barber Performance (bar chart + table)
4. Popular Services (pie/donut chart)
5. Busy Hours Heatmap (7×24 grid)
6. AI Insights Panel (auto-generated insights)
```

**AI Insights Panel Example:**
```
┌─────────────────────────────────────────────────┐
│ ⚡ AI Insights                      Powered by AI│
│ ──────────────────────────────────────────────  │
│ 📈 Revenue is up 23% vs last month. Ali Barber  │
│    is your top performer (Rs. 45,000 this week).│
│                                                 │
│ ⚠️  12 customers haven't visited in 30+ days.   │
│    [Start AI Reminder Campaign →]               │
│                                                 │
│ 🕐 Your busiest hour is 4–6 PM on Fridays.      │
│    Consider dynamic pricing or staff planning.  │
└─────────────────────────────────────────────────┘
```

---

### Screen 6: Customer App — Home

**UX Reasoning:**
- Customer's primary goal: book quickly or check queue
- Keep it to 2 taps maximum to book

**Layout:**
```
┌─────────────────────────────┐
│  Trimly          🔔  [User] │
│                             │
│  ┌─────────────────────────┐│
│  │ Gulshan Barbers          ││
│  │ 2 chairs free • ~5 min  ││
│  │ [Book Now →]            ││
│  └─────────────────────────┘│
│                             │
│  Your Points: 170 🌟        │
│  Next reward: 30 pts away   │
│  ────────────────────────── │
│  Upcoming:                  │
│  Tue Aug 12, 3:00 PM        │
│  Fade Cut • Ali Barber      │
│  ────────────────────────── │
│  Live Queue                 │
│  [See live queue →]         │
│                             │
│  Offers for you 🎁           │
│  [20% off Facial →]         │
└─────────────────────────────┘
│ 🏠  📅  🎫  ⭐  👤 │ (nav)
```

---

### Screen 7: Public Queue Board (TV/Customer display)

**Purpose:** Displayed on a TV screen in the salon lobby

**Design:** Dark theme, large text, minimal, auto-refreshing

```
┌──────────────────────────────────────────────────────────┐
│                   GULSHAN BARBERS                         │
│                   ─────────────                           │
│                                                           │
│   CHAIR 1 🔵            CHAIR 2 🟢                        │
│   ─────────             ─────────                         │
│   Ali Barber            Hassan                            │
│   Ahmed Khan            FREE                              │
│   Fade Cut              Ready in 2 min                    │
│   ████████░░  14 min                                      │
│                                                           │
│   CHAIR 3 🟡            CHAIR 4 🔵                        │
│   ON BREAK              Kamran                            │
│   Resumes 4:00 PM       Bilal Khan                        │
│                         Beard Trim                        │
│                         ████░░░░░░  8 min                 │
│                                                           │
│                WAITING: 3 customers                       │
│           Average wait: approximately 22 min              │
└──────────────────────────────────────────────────────────┘
```

---

## AI Feature UX

### AI Voice Call Panel

```
┌──────────────────────────────────────────┐
│  AI Receptionist              [Active ●] │
│ ──────────────────────────────────────── │
│                                          │
│     🎙️  Calling Ahmed Khan...           │
│         0300-1234567                     │
│                                          │
│     ┌────────────────────────────────┐   │
│     │ AI: "السلام علیکم احمد صاحب۔  │   │
│     │ آپ نے تقریباً ایک مہینہ پہلے   │   │
│     │ ہیئر کٹ کروایا تھا۔ کیا آپ   │   │
│     │ دوبارہ اپائنٹمنٹ لینا چاہیں   │   │
│     │ گے؟"                           │   │
│     └────────────────────────────────┘   │
│                                          │
│     🔊 Audio Wave Animation              │
│     ─────────────────────────           │
│     [Transcript Live] [End Call]         │
└──────────────────────────────────────────┘
```

### AI Campaign Builder

```
Step 1: Choose trigger       Step 2: Audience      Step 3: Message
┌─────────────────┐          ┌─────────────┐       ┌──────────────┐
│ 🎂 Birthday     │    →     │ Customers   │  →    │ Channel:     │
│ 💤 Inactive     │          │ who haven't │       │ ○ SMS        │
│ 🎉 Festival     │          │ visited in  │       │ ● WhatsApp   │
│ 📅 Recurring    │          │ [30] days   │       │ ○ AI Call    │
└─────────────────┘          └─────────────┘       │              │
                                                    │ Message:     │
                                                    │ [AI Draft ✨]│
                                                    │ "Aapko miss  │
                                                    │  kar rahe..."│
                                                    └──────────────┘
```

---

## Micro-Interactions & Animations

### Animation Principles
- Duration: 150ms (hover) → 300ms (transitions) → 500ms (page)
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` for most; `spring` for playful
- Never block the user — all animations must be interruptible

### Animation Catalog

| Interaction | Animation | Duration |
|---|---|---|
| Button hover | Scale 1.02 + shadow lift | 150ms |
| Button click | Scale 0.97 → 1.0 | 100ms |
| Card hover | translateY(-2px) + shadow | 200ms |
| Sidebar expand | width 64px → 240px | 250ms |
| Modal open | scale(0.95) + fade → 1.0 | 200ms |
| Page transition | fade + slight slide up | 300ms |
| Loading skeleton | shimmer pulse | Loop |
| Success state | checkmark draw + scale | 400ms |
| Error shake | horizontal shake (3x) | 400ms |
| Number count | count-up animation | 800ms |
| Chart reveal | draw from left → right | 600ms |
| Toast notification | slide in from right | 300ms |
| Queue countdown | smooth decrement | Real-time |
| AI typing | streaming text effect | Variable |

### Loading Skeletons
Every data-fetching component must have a skeleton:
```tsx
// Pattern: match exact shape of real content
<Skeleton className="h-4 w-32" />  // Text
<Skeleton className="h-8 w-8 rounded-full" />  // Avatar  
<Skeleton className="h-[200px] w-full rounded-xl" />  // Card
```

### Empty States
Every empty state must include:
1. An illustration (SVG, not emoji-only)
2. A descriptive title
3. A helpful subtitle
4. A primary CTA button

```
Example: No customers yet
  [👥 Illustration]
  "No customers yet"
  "Start building your customer list by adding your first customer."
  [+ Add Customer]
```

---

## Responsive Design

### Breakpoints
```css
sm:   640px   /* Large phone */
md:   768px   /* Tablet portrait */
lg:   1024px  /* Tablet landscape / small laptop */
xl:   1280px  /* Desktop */
2xl:  1536px  /* Large desktop */
```

### Mobile Adaptations

| Desktop Component | Mobile Adaptation |
|---|---|
| Sidebar (240px) | Bottom tab bar (5 items) |
| Data Table | Card list with swipe actions |
| Split panel | Full-screen + drawer |
| Calendar (week view) | Day view with scroll |
| Multi-column grid | Single column stack |
| Hover actions | Long press + action sheet |
| Command palette | Floating search bar |

### Owner App Responsive Rules
- **Desktop (xl+):** Full sidebar + main + optional right panel
- **Tablet (md–lg):** Collapsed sidebar (icons) + main
- **Mobile:** Bottom navigation + full-width screens

### Customer App
- Mobile-first: design for 375px first, then expand
- All touch targets minimum 44×44px (iOS HIG)
- Bottom-anchored primary actions

---

## Accessibility

### Requirements (WCAG 2.1 AA)

| Rule | Implementation |
|---|---|
| Color contrast | Minimum 4.5:1 for text, 3:1 for large text |
| Focus visible | Custom focus ring: `ring-2 ring-emerald-500 ring-offset-2` |
| Keyboard navigation | All interactive elements reachable via Tab |
| Screen reader | Proper `aria-label`, `aria-describedby`, `role` on all custom components |
| Form errors | Error linked to input via `aria-describedby` |
| Loading states | `aria-live="polite"` on dynamic content areas |
| Images | Descriptive `alt` text on all meaningful images |
| Touch targets | Minimum 44×44px on mobile |

### ARIA Patterns
```tsx
// Status badge
<span role="status" aria-label="Chair status: Busy">
  <span aria-hidden="true">🔵</span> Busy
</span>

// Live queue (auto-announces updates)
<div aria-live="polite" aria-atomic="false">
  {queueItems}
</div>

// Modal
<dialog aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Book Appointment</h2>
</dialog>
```

---

## Dark Mode

### Implementation
- CSS variables for all colors (no hardcoded values)
- `next-themes` for Next.js theme management
- System preference detection + manual toggle
- Persist preference in localStorage

### Dark Mode Color Mappings
```css
:root {
  --bg-primary:    #FAFAFA;
  --bg-secondary:  #FFFFFF;
  --text-primary:  #09090B;
  --text-muted:    #6B7280;
  --border:        #E5E7EB;
}

.dark {
  --bg-primary:    #09090B;
  --bg-secondary:  #111111;
  --text-primary:  #F9FAFB;
  --text-muted:    #9CA3AF;
  --border:        #1F2937;
}
```

---

## Urdu/RTL Support

### Strategy
- Detect preferred language from user profile
- Apply `dir="rtl"` to HTML root when Urdu active
- Use `rtl:` Tailwind variants for RTL-specific adjustments
- Noto Nastaliq Urdu or Jameel Noori Nastaleeq font for Urdu text

### RTL Adjustments
```css
/* Mirror icons that imply direction */
[dir="rtl"] .icon-arrow-right { transform: scaleX(-1); }

/* Sidebar flips to right */
[dir="rtl"] .sidebar { left: auto; right: 0; }

/* Text alignment */
[dir="rtl"] .text-left { text-align: right; }
```

### Bilingual Components
- All UI strings in `i18n` JSON files
- `en.json` and `ur.json` minimum
- Number formatting: English numerals in both (Pakistani norm)
- Date formatting: `DD/MM/YYYY` (Pakistani norm)

---

## Design Tokens (CSS Variables)

Complete tokens reference:

```css
:root {
  /* Colors */
  --primary:          210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary:        217.2 32.6% 17.5%;
  --accent:           142 76% 36%;          /* Emerald */
  --accent-foreground: 210 40% 98%;
  --destructive:      0 84.2% 60.2%;
  --muted:            217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --card:             222.2 84% 4.9%;
  --border:           217.2 32.6% 17.5%;
  --ring:             142 76% 36%;          /* Focus ring emerald */

  /* Spacing */
  --container-max:    1280px;
  --sidebar-width:    240px;
  --sidebar-collapsed: 64px;
  --header-height:    64px;

  /* Animation */
  --duration-fast:    150ms;
  --duration-normal:  300ms;
  --duration-slow:    500ms;
  --ease-standard:    cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring:      cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## Component Code Patterns

### Stats Card Pattern
```tsx
interface StatsCardProps {
  title: string;
  value: string | number;
  change?: { value: number; period: string };
  icon: LucideIcon;
  iconColor?: string;
  loading?: boolean;
}

const StatsCard = ({ title, value, change, icon: Icon, loading }: StatsCardProps) => {
  if (loading) return <Skeleton className="h-[120px] w-full rounded-2xl" />;
  
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className="bg-card rounded-2xl p-6 shadow-card border border-border"
    >
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <div className="p-2 bg-accent/10 rounded-lg">
          <Icon className="h-4 w-4 text-accent" />
        </div>
      </div>
      <p className="text-3xl font-bold tracking-tight">{value}</p>
      {change && (
        <p className={cn("text-xs mt-1", change.value > 0 ? "text-emerald-500" : "text-red-500")}>
          {change.value > 0 ? "↑" : "↓"} {Math.abs(change.value)}% vs {change.period}
        </p>
      )}
    </motion.div>
  );
};
```

### Page Header Pattern
```tsx
const PageHeader = ({ title, description, actions }: PageHeaderProps) => (
  <div className="flex items-start justify-between mb-8">
    <div>
      <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
      {description && (
        <p className="text-muted-foreground mt-1">{description}</p>
      )}
    </div>
    {actions && (
      <div className="flex items-center gap-3">{actions}</div>
    )}
  </div>
);
```

### Empty State Pattern
```tsx
const EmptyState = ({ icon: Icon, title, description, action }: EmptyStateProps) => (
  <div className="flex flex-col items-center justify-center py-16 px-8 text-center">
    <div className="p-4 bg-muted rounded-2xl mb-4">
      <Icon className="h-8 w-8 text-muted-foreground" />
    </div>
    <h3 className="text-lg font-semibold mb-2">{title}</h3>
    <p className="text-muted-foreground text-sm max-w-sm mb-6">{description}</p>
    {action}
  </div>
);
```

---

*Design system maintained by Trimly Design Team. All UI components must follow these guidelines before shipping.*
